"""Stage 3.6: Social draft generation from daily insights + top Pulse items."""
import json
import os
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv
from prompt_loader import load_prompt

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SITE_URL = "https://faultmanagedpower.org"


def generate_social_drafts(insights_date=None):
    """
    Stage 3.6: generate social drafts from today's moderator insights + top Pulse items.

    insights_date: YYYY-MM-DD string. Defaults to today.
    Returns path to output file, or None on failure.

    Output schema: flat drafts[] array with channel = linkedin | x | prompt.
    See agent_prompts/social_drafts_output.md.
    """
    print("Generating social drafts...")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return None

    today = insights_date or datetime.now().strftime("%Y-%m-%d")
    insights_dir = PROJECT_ROOT / "data" / "insights"
    moderator_file = insights_dir / f"{today}_moderator.json"

    if not moderator_file.exists():
        print(f"  No moderator insights found for {today} — skipping social drafts")
        return None

    with open(moderator_file) as f:
        moderator = json.load(f)

    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    if not items_file.exists():
        print("  No items.json found")
        return None
    with open(items_file) as f:
        all_items = json.load(f)

    # Top 5 most recently discovered, with full site URLs
    all_items.sort(key=lambda x: x.get("discovered_at", ""), reverse=True)
    top_items = [
        {
            "id": item["id"],
            "title": item["title"],
            "so_what": item.get("so_what"),
            "vertical": item.get("vertical"),
            "url": f"{SITE_URL}/pulse/{item['slug']}/",
            "topics": item.get("topics", [])[:3],
        }
        for item in all_items[:5]
        if item.get("slug")
    ]

    client = anthropic.Anthropic(api_key=api_key)
    prompt = load_prompt(
        "social_drafts",
        RUN_DATE=today,
        MODERATOR_OUTPUT_JSON=json.dumps(moderator, indent=2),
        TOP_PULSE_ITEMS_JSON=json.dumps(top_items, indent=2),
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

        output = json.loads(text)

        social_dir = PROJECT_ROOT / "data" / "social"
        social_dir.mkdir(parents=True, exist_ok=True)
        output_file = social_dir / f"{today}_social_drafts.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)

        all_drafts = output.get("drafts", [])
        li = sum(1 for d in all_drafts if d.get("channel") == "linkedin")
        x  = sum(1 for d in all_drafts if d.get("channel") == "x")
        print(f"  Saved: {li} LinkedIn, {x} X drafts → {output_file.name}")
        return str(output_file)

    except Exception as e:
        print(f"  Error generating social drafts: {e}")
        return None


if __name__ == "__main__":
    generate_social_drafts()
