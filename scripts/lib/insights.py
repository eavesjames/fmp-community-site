"""Stage 3.5: Multi-agent insight synthesis from daily Pulse items."""
import json
import os
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
            max_tokens=1400,
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
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        return _parse_json_response(message.content[0].text)
    except Exception as e:
        print(f"    Error in moderator: {e}")
        return None


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
    if moderator_output:
        moderator_file = insights_dir / f"{today}_moderator.json"
        with open(moderator_file, "w") as f:
            json.dump(moderator_output, f, indent=2)
        n_insights = len(moderator_output.get("composite_insights", []))
        n_angles = len(moderator_output.get("ranked_original_angles", []))
        print(f"  Saved moderator output → {moderator_file.name}")
        print(f"  → {n_insights} composite insight(s), {n_angles} ranked angle(s)")
    else:
        print("  Moderator returned no output")

    return {
        "analysts_file": str(analysts_file),
        "moderator_file": str(moderator_file) if moderator_file else None,
    }


if __name__ == "__main__":
    run_insights()
