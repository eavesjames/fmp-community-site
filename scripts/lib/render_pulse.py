"""Render Pulse pages from normalized items"""
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent

PULSE_BODY = """\

## What it is

{summary}

## Why it matters

{why_it_matters}
{evidence_section}
## Links

- **Canonical source**: [{canonical_source}]({canonical_source})
{player_link}{topic_links}

## Open questions

{open_questions}
"""


def build_front_matter(item):
    """Build YAML front matter, including Phase 2 fields when present."""
    date = item.get("publish_date") or item.get("discovered_at", "")[:10]
    lastmod = item.get("discovered_at", "")[:10]
    title = item.get("title", "").replace('"', '\\"')
    desc = item.get("description", "").replace('"', '\\"')
    source_url = item.get("canonical_source", "")

    summary = item.get("summary", "").replace('"', '\\"')

    lines = [
        "---",
        f'title: "{title}"',
        f"date: {date}",
        f"lastmod: {lastmod}",
        f'description: "{desc}"',
        f'summary: "{summary}"',
        "",
        'type: "pulse"',
        f'artifact_type: "{item.get("artifact_type", "other")}"',
        "",
    ]

    # Phase 2 fields — only written when present
    phase2 = []
    if source_url:
        phase2.append(f'source_url: "{source_url}"')
    if item.get("source_name"):
        phase2.append(f'source_name: "{item["source_name"]}"')
    if item.get("source_date"):
        phase2.append(f"source_date: {item['source_date']}")
    if item.get("vertical"):
        phase2.append(f'vertical: "{item["vertical"]}"')
    if item.get("persona"):
        phase2.append(f'persona: "{item["persona"]}"')
    if item.get("so_what"):
        so_what = item["so_what"].replace('"', '\\"')
        phase2.append(f'so_what: "{so_what}"')

    if phase2:
        lines.extend(phase2)
        lines.append("")

    players_str = json.dumps(item.get("players", []))
    topics_str = json.dumps(item.get("topics", []))
    value_levers_str = json.dumps(item.get("value_levers", []))

    lines.extend([
        f"players: {players_str}",
        f"topics: {topics_str}",
        f"value_levers: {value_levers_str}",
        "",
        f'canonical_source: "{source_url}"',
        "sources:",
        f'  - "{source_url}"',
        "",
        f'confidence: "{item.get("confidence", "medium")}"',
        "---",
    ])

    return "\n".join(lines)

def get_why_it_matters(item):
    """Return grounded why_it_matters from item, or a minimal fallback."""
    return item.get("why_it_matters") or "See source for details."


def get_open_questions(item):
    """Return open_questions as bullet list from item, or a minimal fallback."""
    questions = item.get("open_questions") or []
    if questions:
        return "\n".join(f"- {q}" for q in questions)
    return "- What are the practical implications for FMP practitioners?"


def get_evidence_section(item):
    """Return evidence bullets block, or empty string if none."""
    bullets = item.get("evidence") or []
    if not bullets:
        return ""
    lines = ["", "**Evidence from source:**", ""]
    lines.extend(f"- {b}" for b in bullets)
    lines.append("")
    return "\n".join(lines)

def render_pulse_pages():
    """Generate markdown files for new Pulse items"""
    print("Rendering Pulse pages...")
    
    # Load master items list
    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    if not items_file.exists():
        print("No items.json found")
        return
    
    with open(items_file) as f:
        items = json.load(f)
    
    # Check which items already have pages
    pulse_dir = PROJECT_ROOT / "content" / "pulse"
    pulse_dir.mkdir(parents=True, exist_ok=True)
    
    existing_slugs = set(f.stem for f in pulse_dir.glob("*.md"))
    
    new_pages = 0
    
    for item in items:
        slug = item.get("slug")
        
        if not slug:
            print(f"  Skipping item without slug: {item.get('title', '')[:50]}")
            continue
        
        if slug in existing_slugs:
            continue  # Already rendered
        
        # Prepare body variables
        canonical_source = item.get("canonical_source", "")
        topics = item.get("topics", [])
        topic_links = "\n".join(f"- **Topic**: /topics/{topic}/" for topic in topics[:2])

        players = item.get("players", [])
        primary_player = players[0] if players else None
        player_link = f"- **Player**: /players/{primary_player}/\n" if primary_player else ""

        # Render page
        front_matter = build_front_matter(item)
        body = PULSE_BODY.format(
            summary=item.get("summary", ""),
            why_it_matters=get_why_it_matters(item),
            evidence_section=get_evidence_section(item),
            canonical_source=canonical_source,
            player_link=player_link,
            topic_links=topic_links,
            open_questions=get_open_questions(item),
        )
        content = front_matter + body
        
        # Write file
        output_file = pulse_dir / f"{slug}.md"
        with open(output_file, "w") as f:
            f.write(content)
        
        new_pages += 1
        print(f"  ✓ Created: {slug}.md")
    
    print(f"\nRendered {new_pages} new Pulse pages")

if __name__ == "__main__":
    render_pulse_pages()
