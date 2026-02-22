"""Normalize and dedupe items into master items.json"""
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent.parent.parent

def generate_slug(item):
    """Generate URL slug for item"""
    # Format: {yyyy-mm-dd}-{player}-{short-title}
    date = item.get("publish_date") or item.get("discovered_at", "")[:10]
    player = item["players"][0] if item.get("players") else "other"
    
    # Create short title (first 3-5 words)
    title = item.get("title", "")
    words = title.lower().split()[:5]
    short_title = "-".join(
        "".join(c for c in word if c.isalnum())
        for word in words
    )
    
    return f"{date}-{player}-{short_title}"

def is_duplicate(new_item, existing_items):
    """Check if item is a duplicate"""
    new_url = new_item.get("link", "")
    
    for existing in existing_items:
        # Exact URL match
        if existing.get("canonical_source") == new_url:
            return True
        
        # Fuzzy match: same domain + similar title + within 30 days
        if urlparse(new_url).netloc == urlparse(existing.get("canonical_source", "")).netloc:
            # Simple title similarity (can be improved)
            new_title = set(new_item.get("title", "").lower().split())
            existing_title = set(existing.get("title", "").lower().split())
            
            if new_title and existing_title:
                similarity = len(new_title & existing_title) / len(new_title | existing_title)
                
                if similarity > 0.7:  # 70% word overlap
                    return True
    
    return False

def calculate_score(item):
    """Calculate relevance score for ranking"""
    score = 0
    
    # Confidence weighting
    confidence_scores = {"high": 10, "medium": 5, "low": 2}
    score += confidence_scores.get(item.get("confidence", "low"), 0)
    
    # Artifact type weighting
    type_scores = {
        "product": 8,
        "case-study": 7,
        "press": 5,
        "event": 6,
        "standard": 9,
        "doc": 6,
    }
    score += type_scores.get(item.get("artifact_type", "other"), 3)
    
    # Multiple players = higher value
    score += len(item.get("players", [])) * 2
    
    # Multiple topics = higher value
    score += len(item.get("topics", [])) * 1
    
    # Recency bonus (last 7 days)
    discovered_date = item.get("discovered_at", "")[:10]
    try:
        days_ago = (datetime.now() - datetime.fromisoformat(discovered_date)).days
        if days_ago <= 7:
            score += 5
        elif days_ago <= 14:
            score += 3
    except:
        pass
    
    return score

def run_normalize():
    """Normalize and dedupe extracted items"""
    print("Running normalize...")
    
    # Load master items list
    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    if items_file.exists():
        with open(items_file) as f:
            existing_items = json.load(f)
        print(f"Loaded {len(existing_items)} existing items")
    else:
        existing_items = []
        print("No existing items, starting fresh")
    
    # Load extracted items
    extracted_dir = PROJECT_ROOT / "data" / "pulse" / "extracted"
    if not extracted_dir.exists():
        print("No extracted items to normalize")
        return
    
    extracted_files = sorted(extracted_dir.glob("extracted_*.json"))
    if not extracted_files:
        print("No extracted files found")
        return
    
    # Process most recent extraction
    latest_extracted = extracted_files[-1]
    print(f"Processing: {latest_extracted.name}")
    
    with open(latest_extracted) as f:
        new_items = json.load(f)
    
    added_count = 0
    skipped_count = 0
    
    for item in new_items:
        # Skip low confidence items
        if item.get("confidence") == "low":
            print(f"  Skipping low confidence: {item.get('title', '')[:50]}")
            skipped_count += 1
            continue
        
        # Check for duplicates
        if is_duplicate(item, existing_items):
            print(f"  Duplicate: {item.get('title', '')[:50]}")
            skipped_count += 1
            continue
        
        # Normalize item
        normalized_item = {
            "id": len(existing_items) + added_count + 1,
            "slug": generate_slug(item),
            "title": item.get("title"),
            "description": item.get("description"),
            "canonical_source": item.get("link"),
            "artifact_type": item.get("artifact_type", "other"),
            "publish_date": item.get("publish_date"),
            "discovered_at": item.get("discovered_at"),
            "players": item.get("players", []),
            "topics": item.get("topics", []),
            "value_levers": item.get("value_levers", []),
            "confidence": item.get("confidence"),
            "summary": item.get("summary"),
            "score": calculate_score(item),
        }
        
        existing_items.append(normalized_item)
        added_count += 1
        print(f"  ✓ Added: {normalized_item['title'][:50]} (score: {normalized_item['score']})")
    
    # Sort by score (descending) and date (descending)
    existing_items.sort(key=lambda x: (x.get("score", 0), x.get("discovered_at", "")), reverse=True)
    
    # Save updated master list
    items_file.parent.mkdir(parents=True, exist_ok=True)
    with open(items_file, "w") as f:
        json.dump(existing_items, f, indent=2)
    
    print(f"\nNormalized: {added_count} added, {skipped_count} skipped")
    print(f"Total items in master list: {len(existing_items)}")

if __name__ == "__main__":
    run_normalize()
