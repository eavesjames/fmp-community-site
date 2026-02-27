"""Stage 3.6: Social draft generation from daily insights + top Pulse items"""
import json
import os
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SITE_URL = "https://faultmanagedpower.org"

SOCIAL_PROMPT = """\
You are a social media writer for faultmanagedpower.org — a knowledge base for FMP \
(Fault Managed Power / NEC Class 4 / Digital Electricity) serving electrical contractors, \
facilities managers, MEP engineers, and building owners.

TODAY'S TOP INSIGHTS (from the AI analyst team):
{insights_json}

TOP NEW PULSE ITEMS PUBLISHED TODAY:
{items_json}

GUARDRAILS — every draft must follow ALL of these:
1. No hype words: revolutionary, game-changing, cutting-edge, disruptive, transformative, \
groundbreaking, unprecedented, exciting
2. Reference at least one concrete constraint lever: pathways/install, monitoring/telemetry, \
UPS/resilience, code/standards, labor/schedule, retrofit disruption, power density
3. Include a specific link (pulse item URL or topic page from the items above)
4. End with a question that invites practitioner engagement
5. Cite which composite insight index (0-based) or item id motivated the draft

LINKEDIN FORMAT (3 drafts):
- 150–400 words each
- 2–3 short paragraphs + question at end
- Professional practitioner tone, no emoji spam (0–1 emoji max per post)
- Different angles: target different personas or constraint levers across the 3 drafts

X/TWITTER FORMAT (3 drafts):
- Entire text including link must be under 240 characters
- One concrete constraint or tension + link + question
- No hashtag spam (0–1 hashtag max)
- Each draft must use a different item or insight as source

DISCUSSION PROMPT FORMAT (1 draft):
- A single strong question for LinkedIn/community forums
- Must reference a specific constraint or tension visible in today's items
- 1–3 sentences max

OUTPUT — valid JSON only, no markdown wrapper:
{{
  "date": "{date}",
  "linkedin_drafts": [
    {{
      "draft": "full post text",
      "source_insight": "composite insight index 0-based, or item id",
      "link": "full URL from site",
      "lever": "constraint lever this addresses",
      "notes": "who this targets / why this angle"
    }},
    {{
      "draft": "...",
      "source_insight": "...",
      "link": "...",
      "lever": "...",
      "notes": "..."
    }},
    {{
      "draft": "...",
      "source_insight": "...",
      "link": "...",
      "lever": "...",
      "notes": "..."
    }}
  ],
  "x_drafts": [
    {{
      "draft": "tweet text + link (under 240 chars total)",
      "source_insight": "...",
      "link": "...",
      "lever": "..."
    }},
    {{
      "draft": "...",
      "source_insight": "...",
      "link": "...",
      "lever": "..."
    }},
    {{
      "draft": "...",
      "source_insight": "...",
      "link": "...",
      "lever": "..."
    }}
  ],
  "discussion_prompt": {{
    "draft": "question text",
    "source_insight": "...",
    "link": "...",
    "lever": "..."
  }}
}}"""


def generate_social_drafts(insights_date=None):
    """
    Stage 3.6: generate social drafts from today's moderator insights + top Pulse items.
    insights_date: YYYY-MM-DD string. Defaults to today.
    Returns path to output file, or None on failure.
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

    # Load top pulse items for context
    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    if not items_file.exists():
        print("  No items.json found")
        return None
    with open(items_file) as f:
        all_items = json.load(f)

    # Top 5 most recently discovered, with full URLs
    all_items.sort(key=lambda x: x.get("discovered_at", ""), reverse=True)
    items_for_prompt = [
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

    insights_for_prompt = {
        "composite_insights": moderator.get("composite_insights", [])[:3],
        "ranked_angles": moderator.get("ranked_angles", [])[:2],
        "new_perspective": moderator.get("new_perspective"),
    }

    client = anthropic.Anthropic(api_key=api_key)
    prompt = SOCIAL_PROMPT.format(
        insights_json=json.dumps(insights_for_prompt, indent=2),
        items_json=json.dumps(items_for_prompt, indent=2),
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

        drafts = json.loads(text)

        social_dir = PROJECT_ROOT / "data" / "social"
        social_dir.mkdir(parents=True, exist_ok=True)
        output_file = social_dir / f"{today}_social_drafts.json"
        with open(output_file, "w") as f:
            json.dump(drafts, f, indent=2)

        li_count = len(drafts.get("linkedin_drafts", []))
        x_count = len(drafts.get("x_drafts", []))
        print(f"  Saved: {li_count} LinkedIn, {x_count} X drafts → {output_file.name}")
        return str(output_file)

    except Exception as e:
        print(f"  Error generating social drafts: {e}")
        return None


if __name__ == "__main__":
    generate_social_drafts()
