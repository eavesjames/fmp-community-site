"""Stage 3.5: Multi-agent insight synthesis from daily Pulse items"""
import json
import os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ANALYST_PERSONAS = [
    {
        "key": "installer_electrical_contractor",
        "label": "Installer / Electrical Contractor",
        "lens": (
            "You look at every item through the lens of: code friction, pathways/install "
            "complexity, labor productivity, AHJ approval difficulty, pre-bid clarity, "
            "and schedule risk. What makes jobs harder or easier to estimate and execute?"
        ),
    },
    {
        "key": "owner_operator_facilities",
        "label": "Owner / Operator / Facilities Manager",
        "lens": (
            "You look at every item through the lens of: system reliability, maintenance "
            "burden, runtime/resilience, commissioning complexity, lifecycle cost, and "
            "disruption during retrofit. What affects uptime and tenant/occupant experience?"
        ),
    },
    {
        "key": "compliance_ahj",
        "label": "Compliance / AHJ / Safety Inspector",
        "lens": (
            "You look at every item through the lens of: code changes, inspection protocols, "
            "approval pathways, standards conflicts, safety model clarity, and enforcement "
            "risk. What creates uncertainty or friction in the permitting and inspection process?"
        ),
    },
    {
        "key": "mep_system_designer",
        "label": "MEP / Systems Designer",
        "lens": (
            "You look at every item through the lens of: design integration, load management, "
            "co-routing constraints, system sizing, interoperability, and specification clarity. "
            "What affects the drawing set, coordination with other trades, and design decisions?"
        ),
    },
    {
        "key": "finance_roi_skeptic",
        "label": "Finance / ROI Skeptic",
        "lens": (
            "You look at every item through the lens of: total cost, payback period, "
            "incentive availability, competing budget priorities, risk of early adoption, "
            "and cost of delay. What affects the business case for or against FMP deployment?"
        ),
    },
]

ANALYST_PROMPT = """\
You are the {label} analyst for faultmanagedpower.org — a knowledge base for Fault Managed Power \
(FMP / NEC Class 4 / Digital Electricity), edge infrastructure power, data center power, and \
building electrification.

{lens}

Below are {n} new Pulse items published to the FMP Community Knowledge Base today.

NEW PULSE ITEMS:
{items_json}

TASK
Analyze these items strictly from your persona's perspective. Be concrete and grounded — \
only make claims supported by the items above. Do not invent facts.

Minimum requirements per output field:
- top_constraints: 2–4 concrete constraints or barriers visible in these items
- tensions: 1–2 tensions between competing forces or stakeholders
- hypotheses: 1–2 testable hypotheses your persona would form
- article_angles: 1–2 article angles (must cite must_cite item IDs from the list above)
- questions_for_owner: 1–2 questions a practitioner should investigate next

OUTPUT — respond with valid JSON only, no markdown:
{{
  "persona": "{key}",
  "top_constraints": ["constraint 1", "constraint 2"],
  "tensions": ["tension between competing forces"],
  "hypotheses": ["testable hypothesis"],
  "article_angles": [
    {{
      "title": "Specific concrete article title <= 80 chars",
      "thesis": "1–2 sentence thesis statement",
      "outline": ["Section 1", "Section 2", "Section 3"],
      "must_cite": ["item_id"],
      "missing_evidence": ["what would be needed to fully support this thesis"]
    }}
  ],
  "questions_for_owner": ["question 1"]
}}"""

MODERATOR_PROMPT = """\
You are the Moderator agent for faultmanagedpower.org. Your job is to synthesize outputs from \
5 analyst personas and surface the most important composite insights and original article \
opportunities from today's Pulse items.

NEW PULSE ITEMS:
{items_json}

ANALYST OUTPUTS:
{analysts_json}

TASK
1. Identify 2–4 composite insights that emerge from MULTIPLE analysts viewing the same items. \
   A composite insight must be supported by at least 2 different analyst personas AND cite \
   at least 1 Pulse item by its id field.
2. Rank the top 3 original article angles across all analysts. Prefer angles with: \
   multi-persona relevance, strong evidence support, clear FMP connection.
3. Generate 3 "tomorrow search briefs" — specific search queries to run tomorrow to fill \
   evidence gaps identified by analysts.
4. Identify one "new perspective" that emerges from analyst disagreement or from viewing \
   the same items through multiple lenses simultaneously.

Hard requirements:
- Every composite insight must cite at least 1 Pulse item by id.
- Do not invent facts not present in the Pulse items.
- No hype language: no "revolutionary", "game-changing", "cutting-edge".
- new_perspective must describe a tension or reframing, not a summary.

OUTPUT — respond with valid JSON only, no markdown:
{{
  "date": "{date}",
  "composite_insights": [
    {{
      "insight": "2–3 sentence concrete insight grounded in the items",
      "supporting_items": ["item_id_1"],
      "analyst_sources": ["persona_key_1", "persona_key_2"],
      "lever": "pathways-install | monitoring-telemetry | ups-resilience | code-standards | labor-productivity | retrofits-mdus | ai-infrastructure | incentives-policy"
    }}
  ],
  "ranked_angles": [
    {{
      "rank": 1,
      "title": "Article title <= 80 chars",
      "thesis": "1–2 sentences",
      "target_persona": "primary persona key",
      "must_cite": ["item_id"],
      "missing_evidence": ["what to find"],
      "owner_questions": ["question for the human editor"]
    }}
  ],
  "tomorrow_search_briefs": [
    {{
      "query": "specific search query string",
      "rationale": "what evidence gap this fills"
    }}
  ],
  "new_perspective": "1–2 sentence insight that emerges from disagreement or multi-lens analysis",
  "analyst_disagreements": ["brief note on where analysts saw the same item differently"]
}}"""


def _slim_items(items):
    """Return a minimal representation of items for prompts (keeps token count down)."""
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


def _run_analyst(persona, items_json, client):
    """Run a single analyst agent. Called in a thread."""
    prompt = ANALYST_PROMPT.format(
        key=persona["key"],
        label=persona["label"],
        lens=persona["lens"],
        n=len(json.loads(items_json)),
        items_json=items_json,
    )
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}],
        )
        text = message.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"    Error in analyst {persona['key']}: {e}")
        return {"persona": persona["key"], "error": str(e)}


def _run_moderator(analyst_outputs, items_json, client):
    """Run the moderator agent after all analysts complete."""
    today = datetime.now().strftime("%Y-%m-%d")
    prompt = MODERATOR_PROMPT.format(
        items_json=items_json,
        analysts_json=json.dumps(analyst_outputs, indent=2),
        date=today,
    )
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        text = message.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"    Error in moderator: {e}")
        return None


def run_insights(new_items=None):
    """
    Stage 3.5: run 5 analyst agents in parallel, then the moderator.
    new_items: list of normalized item dicts from run_normalize().
               If None, falls back to the top 10 most-recently-discovered items.json entries.
    Returns dict with paths to output files, or None on failure.
    """
    print("Running insights...")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return None

    # Load items if not passed in
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

    # Serialize items once; reuse across threads
    items_json = json.dumps(_slim_items(new_items), indent=2)

    # ── Run 5 analysts in parallel ────────────────────────────────────────────
    analyst_outputs = []
    print("  Running 5 analyst agents in parallel...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(_run_analyst, persona, items_json, client): persona["key"]
            for persona in ANALYST_PERSONAS
        }
        for future in as_completed(futures):
            key = futures[future]
            result = future.result()
            analyst_outputs.append(result)
            n_angles = len(result.get("article_angles", []))
            status = "error" if "error" in result else f"{n_angles} angle(s)"
            print(f"    ✓ {key}: {status}")

    # ── Save analyst outputs ──────────────────────────────────────────────────
    insights_dir = PROJECT_ROOT / "data" / "insights"
    insights_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    analysts_file = insights_dir / f"{today}_analysts.json"
    with open(analysts_file, "w") as f:
        json.dump(analyst_outputs, f, indent=2)
    print(f"  Saved analyst outputs → {analysts_file.name}")

    # ── Run moderator ─────────────────────────────────────────────────────────
    print("  Running moderator agent...")
    moderator_output = _run_moderator(analyst_outputs, items_json, client)

    moderator_file = None
    if moderator_output:
        moderator_file = insights_dir / f"{today}_moderator.json"
        with open(moderator_file, "w") as f:
            json.dump(moderator_output, f, indent=2)
        n_insights = len(moderator_output.get("composite_insights", []))
        n_angles = len(moderator_output.get("ranked_angles", []))
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
