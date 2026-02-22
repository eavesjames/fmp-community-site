"""Render Pulse pages from normalized items"""
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent

PULSE_TEMPLATE = """---
title: "{title}"
date: {date}
lastmod: {lastmod}
description: "{description}"

type: "pulse"
artifact_type: "{artifact_type}"

players: {players}
topics: {topics}
value_levers: {value_levers}

canonical_source: "{canonical_source}"
sources:
  - "{canonical_source}"

confidence: "{confidence}"
---

## What it is

{summary}

## Why it matters

{why_it_matters}

## Links

- **Canonical source**: [{canonical_source}]({canonical_source})
- **Player**: /players/{primary_player}/
{topic_links}

## Open questions

{open_questions}
"""

def generate_why_it_matters(item):
    """Generate 'Why it matters' section"""
    artifact_type = item.get("artifact_type", "other")
    players = item.get("players", [])
    topics = item.get("topics", [])
    
    # Simple heuristic based on type and topics
    if artifact_type == "product":
        return "New product releases signal market direction and technology evolution in the FMP ecosystem. Product specifications and capabilities help practitioners evaluate fit for specific use cases."
    elif artifact_type == "case-study":
        return "Real-world deployments provide validated evidence of FMP value propositions. Case studies reduce estimating friction by showing actual costs, schedules, and outcomes."
    elif artifact_type == "standard":
        return "Standards and code updates directly impact FMP deployment requirements. Understanding standard changes is critical for specification and compliance."
    elif artifact_type == "event":
        return "Industry events provide networking opportunities and access to latest technical updates. Conference presentations often preview upcoming developments before formal announcements."
    else:
        return "This update provides context on FMP ecosystem development and helps practitioners stay informed on industry direction."

def generate_open_questions(item):
    """Generate open questions"""
    artifact_type = item.get("artifact_type", "other")
    players = item.get("players", [])
    
    questions = []
    
    if artifact_type == "product":
        questions.append("- What are the key specifications and performance characteristics?")
        questions.append("- How does this compare to existing solutions?")
        questions.append("- What use cases is this optimized for?")
    elif artifact_type == "case-study":
        questions.append("- What were the project economics (cost, schedule, labor)?")
        questions.append("- What were the key decision factors for choosing FMP?")
        questions.append("- What lessons learned apply to other projects?")
    elif artifact_type == "event":
        questions.append("- What topics will be covered?")
        questions.append("- Who are the key speakers?")
        questions.append("- Will presentations/recordings be available?")
    else:
        questions.append("- What are the practical implications for FMP practitioners?")
        questions.append("- How does this affect project planning and execution?")
    
    return "\n".join(questions)

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
        
        # Prepare template variables
        date = item.get("publish_date") or item.get("discovered_at", "")[:10]
        lastmod = item.get("discovered_at", "")[:10]
        
        players_str = json.dumps(item.get("players", []))
        topics_str = json.dumps(item.get("topics", []))
        value_levers_str = json.dumps(item.get("value_levers", []))
        
        primary_player = item.get("players", ["other"])[0]
        
        # Generate topic links
        topics = item.get("topics", [])
        if topics:
            topic_links = "\n".join(f"- **Topic**: /topics/{topic}/" for topic in topics[:2])
        else:
            topic_links = ""
        
        # Render page
        content = PULSE_TEMPLATE.format(
            title=item.get("title", "").replace('"', '\\"'),
            date=date,
            lastmod=lastmod,
            description=item.get("description", "").replace('"', '\\"'),
            artifact_type=item.get("artifact_type", "other"),
            players=players_str,
            topics=topics_str,
            value_levers=value_levers_str,
            canonical_source=item.get("canonical_source", ""),
            confidence=item.get("confidence", "medium"),
            summary=item.get("summary", ""),
            why_it_matters=generate_why_it_matters(item),
            primary_player=primary_player,
            topic_links=topic_links,
            open_questions=generate_open_questions(item)
        )
        
        # Write file
        output_file = pulse_dir / f"{slug}.md"
        with open(output_file, "w") as f:
            f.write(content)
        
        new_pages += 1
        print(f"  ✓ Created: {slug}.md")
    
    print(f"\nRendered {new_pages} new Pulse pages")

if __name__ == "__main__":
    render_pulse_pages()
