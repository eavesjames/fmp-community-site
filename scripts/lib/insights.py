"""Stage 3.5: Multi-agent insight synthesis from daily Pulse items."""
import json
import os
import re
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import anthropic
from dotenv import load_dotenv
from prompt_loader import load_prompt

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Maps persona key → prompt file name in agent_prompts/
ANALYST_PERSONAS = [
    {"key": "installer_electrical_contractor", "prompt_file": "analyst_installer"},
    {"key": "owner_operator_facilities",       "prompt_file": "analyst_owner_operator"},
    {"key": "compliance_ahj",                  "prompt_file": "analyst_compliance"},
    {"key": "mep_system_designer",             "prompt_file": "analyst_mep"},
    {"key": "finance_roi_skeptic",             "prompt_file": "analyst_finance"},
]


def _slim_items(items):
    """Minimal item representation for prompts — keeps token count down."""
    return [
        {
            "id": item["id"],
            "title": item["title"],
            "vertical": item.get("vertical"),
            "so_what": item.get("so_what"),
            "summary": item.get("summary"),
            "why_it_matters": item.get("why_it_matters"),
            "topics": item.get("topics", []),
            "evidence": item.get("evidence", []),
        }
        for item in items
    ]


def _vertical_stats(items):
    """Return a JSON string summarising item counts per vertical."""
    counts = {}
    for item in items:
        v = item.get("vertical") or "unknown"
        counts[v] = counts.get(v, 0) + 1
    return json.dumps(counts)


def _parse_json_response(text):
    """Strip optional markdown fences and parse JSON."""
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return json.loads(text)


def _run_analyst(persona, items_json, coverage_stats, client):
    """Run one analyst agent. Called in a thread pool."""
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = load_prompt(
        persona["prompt_file"],
        RUN_DATE=today,
        VERTICAL_COVERAGE_STATS=coverage_stats,
        PULSE_ITEMS_JSON=items_json,
    )
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_response(message.content[0].text)
    except Exception as e:
        print(f"    Error in analyst {persona['key']}: {e}")
        return {"agent": persona["key"], "error": str(e)}


def _run_moderator(analyst_outputs, items_json, coverage_stats, client):
    """Run the moderator after all analysts complete."""
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = load_prompt(
        "moderator_synthesis",
        RUN_DATE=today,
        VERTICAL_COVERAGE_STATS=coverage_stats,
        PULSE_ITEMS_JSON=items_json,
        ANALYST_OUTPUTS_JSON=json.dumps(analyst_outputs, indent=2),
    )
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_response(message.content[0].text)
    except Exception as e:
        print(f"    Error in moderator: {e}")
        return None


def _angle_slug(working_title: str, date: str) -> str:
    """Convert working_title to a URL-safe slug prefixed with date."""
    slug = re.sub(r"[^a-z0-9]+", "-", working_title.lower()).strip("-")[:50]
    return f"{date}-{slug}"


def _write_insight_draft(angle: dict, angle_idx: int, date: str, items_by_id: dict) -> str:
    """
    Write a draft markdown file for one ranked_original_angle.
    Returns the relative path (from project root) of the file.
    """
    insights_dir = PROJECT_ROOT / "content" / "insights"
    insights_dir.mkdir(parents=True, exist_ok=True)

    working_title = angle.get("working_title", f"Insight {angle_idx + 1}")
    slug = _angle_slug(working_title, date)
    insight_id = angle.get("insight_id") or f"{date}-A{angle_idx + 1:02d}"

    # Build must-cite item list
    must_cite = angle.get("must_cite_items", [])
    cite_lines = []
    for item_id in must_cite:
        item = items_by_id.get(item_id) or items_by_id.get(str(item_id))
        if item:
            cite_lines.append(f"- item {item_id}: {item.get('title', '')}")
        else:
            cite_lines.append(f"- item {item_id}")

    must_cite_md = "\n".join(cite_lines) if cite_lines else "_None specified_"

    # Recommended questions
    questions = angle.get("recommended_owner_questions", [])
    questions_md = "\n".join(f"- {q}" for q in questions) if questions else "_None_"

    # Evidence gaps
    missing = angle.get("missing_evidence_to_find", [])
    missing_md = "\n".join(f"- {m}" for m in missing) if missing else "_None_"

    levers = angle.get("levers", [])
    levers_yaml = json.dumps(levers)
    who_cares = angle.get("who_cares", "")
    verticals = angle.get("which_verticals", [])
    verticals_yaml = json.dumps(verticals)
    confidence = angle.get("confidence", "")
    safe_title = working_title.replace('"', '\\"')

    content = f"""---
title: "{safe_title}"
date: {date}
draft: true
insight_id: "{insight_id}"
status: "DRAFT"
levers: {levers_yaml}
which_verticals: {verticals_yaml}
confidence: "{confidence}"
must_cite_items: {json.dumps(must_cite)}
---

## Thesis

{angle.get("thesis", "_Add thesis here._")}

## Why this is new

{angle.get("why_it_is_new", "_Explain why this angle is original._")}

## Who cares

{who_cares or "_Specify target audience._"}

## Recommended questions to research

{questions_md}

## Evidence gaps to fill

{missing_md}

## Must-cite items

{must_cite_md}
"""

    out_path = insights_dir / f"{slug}.md"
    with open(out_path, "w") as f:
        f.write(content)

    # Return path relative to project root
    return str(out_path.relative_to(PROJECT_ROOT))


def _write_insights_registry(angles: list, draft_paths: list, date: str) -> str:
    """Write data/review/YYYY-MM-DD_insights_registry.json. Returns file path."""
    registry_entries = []
    for angle, path in zip(angles, draft_paths):
        insight_id = angle.get("insight_id") or f"{date}-A{angles.index(angle) + 1:02d}"
        registry_entries.append({
            "insight_id":    insight_id,
            "working_title": angle.get("working_title", ""),
            "status":        "DRAFT",
            "draft_path":    path,
            "confidence":    angle.get("confidence", ""),
            "levers":        angle.get("levers", []),
        })

    registry = {
        "date":     date,
        "insights": registry_entries,
    }

    registry_file = PROJECT_ROOT / "data" / "review" / f"{date}_insights_registry.json"
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)

    return str(registry_file)


def run_insights(new_items=None):
    """
    Stage 3.5: run 5 analyst agents in parallel, then the moderator.

    new_items: list of normalized item dicts (from run_normalize return value).
               Falls back to 10 most-recently-discovered items from items.json.
    Returns dict with output file paths, or None on failure.
    """
    print("Running insights...")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return None

    if new_items is None:
        items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
        if not items_file.exists():
            print("No items.json found")
            return None
        with open(items_file) as f:
            all_items = json.load(f)
        all_items.sort(key=lambda x: x.get("discovered_at", ""), reverse=True)
        new_items = all_items[:10]

    if not new_items:
        print("No items available for insights")
        return None

    print(f"  Generating insights from {len(new_items)} items")
    client = anthropic.Anthropic(api_key=api_key)

    # Serialise items and coverage stats once; reused across threads
    items_json = json.dumps(_slim_items(new_items), indent=2)
    coverage_stats = _vertical_stats(new_items)

    # ── Run 5 analysts in parallel ─────────────────────────────────────────
    analyst_outputs = []
    print("  Running 5 analyst agents in parallel...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(_run_analyst, persona, items_json, coverage_stats, client): persona["key"]
            for persona in ANALYST_PERSONAS
        }
        for future in as_completed(futures):
            key = futures[future]
            result = future.result()
            analyst_outputs.append(result)
            n_angles = len(result.get("original_angles", []))
            status = "error" if "error" in result else f"{n_angles} angle(s)"
            print(f"    ✓ {key}: {status}")

    # ── Save analyst outputs ───────────────────────────────────────────────
    insights_dir = PROJECT_ROOT / "data" / "insights"
    insights_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    analysts_file = insights_dir / f"{today}_analysts.json"
    with open(analysts_file, "w") as f:
        json.dump(analyst_outputs, f, indent=2)
    print(f"  Saved analyst outputs → {analysts_file.name}")

    # ── Run moderator ──────────────────────────────────────────────────────
    print("  Running moderator agent...")
    moderator_output = _run_moderator(analyst_outputs, items_json, coverage_stats, client)

    moderator_file = None
    draft_paths = []
    registry_file = None

    if moderator_output:
        moderator_file = insights_dir / f"{today}_moderator.json"
        with open(moderator_file, "w") as f:
            json.dump(moderator_output, f, indent=2)
        n_insights = len(moderator_output.get("composite_insights", []))
        n_angles = len(moderator_output.get("ranked_original_angles", []))
        print(f"  Saved moderator output → {moderator_file.name}")
        print(f"  → {n_insights} composite insight(s), {n_angles} ranked angle(s)")

        # ── Write draft insight markdown files ────────────────────────────────
        angles = moderator_output.get("ranked_original_angles", [])
        if angles:
            # Build id → item lookup for must-cite resolution
            items_by_id = {item["id"]: item for item in new_items if "id" in item}
            items_by_id.update({str(k): v for k, v in items_by_id.items()})

            print(f"  Writing {len(angles)} insight draft(s) → content/insights/")
            for idx, angle in enumerate(angles):
                path = _write_insight_draft(angle, idx, today, items_by_id)
                draft_paths.append(path)
                print(f"    ✓ {path}")

            registry_file = _write_insights_registry(angles, draft_paths, today)
            print(f"  Saved insights registry → {Path(registry_file).name}")
    else:
        print("  Moderator returned no output")

    return {
        "analysts_file":   str(analysts_file),
        "moderator_file":  str(moderator_file) if moderator_file else None,
        "draft_paths":     draft_paths,
        "registry_file":   registry_file,
    }


if __name__ == "__main__":
    run_insights()
