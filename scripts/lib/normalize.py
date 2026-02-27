"""Normalize and dedupe items into master items.json"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Maximum age for content to be included (days)
MAX_CONTENT_AGE_DAYS = 30

def is_too_old(item, max_age_days=MAX_CONTENT_AGE_DAYS):
    """Check if content is older than the threshold"""
    # Check publish_date first, then fall back to discovered_at
    date_str = item.get("publish_date") or item.get("discovered_at", "")[:10]

    if not date_str:
        return False  # If no date, allow it through

    try:
        content_date = datetime.fromisoformat(date_str)
        age_days = (datetime.now() - content_date).days
        return age_days > max_age_days
    except:
        return False  # If date parsing fails, allow it through

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
        "linkedin-post": 5,
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
    newly_added = []
    skip_reasons = {"low_confidence": 0, "too_old": 0, "duplicate": 0}

    for item in new_items:
        # Skip low confidence items
        if item.get("confidence") == "low":
            print(f"  Skipping low confidence: {item.get('title', '')[:50]}")
            skip_reasons["low_confidence"] += 1
            skipped_count += 1
            continue

        # Skip old content
        if is_too_old(item):
            pub_date = item.get("publish_date") or item.get("discovered_at", "")[:10]
            print(f"  Skipping old content ({pub_date}): {item.get('title', '')[:50]}")
            skip_reasons["too_old"] += 1
            skipped_count += 1
            continue

        # Check for duplicates
        if is_duplicate(item, existing_items):
            print(f"  Duplicate: {item.get('title', '')[:50]}")
            skip_reasons["duplicate"] += 1
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
            # Phase 2 fields (Claude's vertical takes priority; query_vertical is the intake hint)
            "query_vertical": item.get("query_vertical") or None,
            "vertical": item.get("vertical") or None,
            "source_name": item.get("source_name") or None,
            "source_date": item.get("source_date") or item.get("publish_date") or item.get("discovered_at", "")[:10] or None,
            "persona": item.get("persona") or None,
            "so_what": item.get("so_what") or None,
            # Grounded body fields
            "why_it_matters": item.get("why_it_matters") or None,
            "open_questions": item.get("open_questions") or [],
            "evidence": item.get("evidence") or [],
        }
        
        existing_items.append(normalized_item)
        newly_added.append(normalized_item)
        added_count += 1
        print(f"  ✓ Added: {normalized_item['title'][:50]} (score: {normalized_item['score']})")
    
    # Sort by score (descending) and date (descending)
    existing_items.sort(key=lambda x: (x.get("score", 0), x.get("discovered_at", "")), reverse=True)
    
    # Save updated master list
    items_file.parent.mkdir(parents=True, exist_ok=True)
    with open(items_file, "w") as f:
        json.dump(existing_items, f, indent=2)
    
    # Tally by vertical for the PR body
    by_vertical = {}
    for item in newly_added:
        v = item.get("vertical")
        if v:
            by_vertical[v] = by_vertical.get(v, 0) + 1

    print(f"\nNormalized: {added_count} added, {skipped_count} skipped")
    print(f"Total items in master list: {len(existing_items)}")

    return {
        "added": added_count,
        "skipped": skipped_count,
        "new_items": newly_added,
        "skip_reasons": skip_reasons,
        "by_vertical": by_vertical,
    }

def write_approved_to_master(approved_candidates: list) -> dict:
    """
    Write a list of approved candidate dicts into items.json.

    Candidates come from data/review/YYYY-MM-DD_candidates.json and have
    already been scored + flagged by candidates.py.  This function normalises
    them into the items.json schema, skips any that are now duplicates, assigns
    sequential IDs, and saves the master list.

    Returns dict: {written, skipped, new_items}.
    """
    print("Writing approved candidates to master items list...")

    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    if items_file.exists():
        with open(items_file) as f:
            existing_items = json.load(f)
    else:
        existing_items = []

    written = 0
    skipped = 0
    new_items = []

    for cand in approved_candidates:
        # Re-check for duplicates against items that may have been added since
        # the candidates.json was generated.
        if is_duplicate(cand, existing_items):
            print(f"  Skipping duplicate: {(cand.get('title') or '')[:60]}")
            skipped += 1
            continue

        # Build a minimal "extracted" dict so generate_slug() works
        slug_source = {
            "publish_date": cand.get("publish_date"),
            "discovered_at": cand.get("discovered_at", ""),
            "players": cand.get("players", []),
            "title": cand.get("title", ""),
        }

        normalized = {
            "id":              len(existing_items) + written + 1,
            "slug":            generate_slug(slug_source),
            "title":           cand.get("title"),
            "description":     cand.get("description"),
            "canonical_source": cand.get("link"),
            "artifact_type":   cand.get("artifact_type", "other"),
            "publish_date":    cand.get("publish_date"),
            "discovered_at":   cand.get("discovered_at"),
            "players":         cand.get("players", []),
            "topics":          cand.get("topics", []),
            "value_levers":    cand.get("value_levers", []),
            "confidence":      cand.get("confidence", "medium"),
            "summary":         cand.get("summary"),
            "score":           cand.get("score", 0),
            "query_vertical":  cand.get("vertical"),
            "vertical":        cand.get("vertical"),
            "source_name":     cand.get("source_name"),
            "source_date":     cand.get("source_date"),
            "persona":         cand.get("persona"),
            "so_what":         cand.get("so_what"),
            "why_it_matters":  cand.get("why_it_matters"),
            "open_questions":  cand.get("open_questions", []),
            "evidence":        cand.get("evidence", []),
        }

        existing_items.append(normalized)
        new_items.append(normalized)
        written += 1
        print(f"  ✓ Added: {normalized['title'][:60]} (score: {normalized['score']})")

    # Sort by score desc, then discovered_at desc
    existing_items.sort(
        key=lambda x: (x.get("score", 0), x.get("discovered_at", "")),
        reverse=True,
    )

    items_file.parent.mkdir(parents=True, exist_ok=True)
    with open(items_file, "w") as f:
        json.dump(existing_items, f, indent=2)

    print(f"  Master list updated: {written} added, {skipped} skipped → {len(existing_items)} total")
    return {"written": written, "skipped": skipped, "new_items": new_items}


if __name__ == "__main__":
    run_normalize()
