"""Phase 1: Score extracted items, apply flags, write candidates.json + approval stub.

This module replaces the normalize→render sequence in the daily pipeline.
Nothing is written to items.json or content/ here — those writes happen only
after James approves items via data/review/YYYY-MM-DD_approval.json.
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

from normalize import (
    calculate_score,
    generate_slug,
    is_duplicate,
    is_too_old,
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
REVIEW_DIR = PROJECT_ROOT / "data" / "review"
HIGH_IMPACT_SCORE_THRESHOLD = 18

# Flags applied per item
FLAG_LOW_CONFIDENCE  = "low_confidence"
FLAG_PRESS_RELEASE   = "press_release"
FLAG_WEAK_EVIDENCE   = "weak_evidence"
FLAG_OLD_SOURCE      = "old_source"
FLAG_DUPLICATE_RISK  = "duplicate_risk"
FLAG_HIGH_IMPACT     = "high_impact"


def _candidate_id(item: dict) -> str:
    """Stable 12-char hex ID derived from canonical URL (or title fallback)."""
    key = item.get("link") or item.get("title") or str(item)
    return hashlib.sha256(key.encode()).hexdigest()[:12]


def _apply_flags(item: dict, score: int, existing_items: list) -> list[str]:
    """Return list of flag strings for this candidate."""
    flags = []
    if item.get("confidence") == "low":
        flags.append(FLAG_LOW_CONFIDENCE)
    if item.get("artifact_type") == "press":
        flags.append(FLAG_PRESS_RELEASE)
    if not item.get("evidence"):
        flags.append(FLAG_WEAK_EVIDENCE)
    if is_too_old(item):
        flags.append(FLAG_OLD_SOURCE)
    if is_duplicate(item, existing_items):
        flags.append(FLAG_DUPLICATE_RISK)
    if score >= HIGH_IMPACT_SCORE_THRESHOLD:
        flags.append(FLAG_HIGH_IMPACT)
    return flags


def run_candidates() -> dict:
    """
    Read latest extracted_*.json, score + flag each item, write:
      data/review/YYYY-MM-DD_candidates.json
      data/review/YYYY-MM-DD_approval.json  (pending IDs pre-filled; approved empty)

    Returns dict with counts and file paths.
    """
    print("Running candidates (Phase 1)...")

    # ── Load extracted items ──────────────────────────────────────────────────
    extracted_dir = PROJECT_ROOT / "data" / "pulse" / "extracted"
    if not extracted_dir.exists():
        print("No extracted dir found")
        return {}

    extracted_files = sorted(extracted_dir.glob("extracted_*.json"))
    if not extracted_files:
        print("No extracted files found")
        return {}

    latest = extracted_files[-1]
    print(f"Processing: {latest.name}")
    with open(latest) as f:
        raw_items = json.load(f)

    # ── Load master items (for duplicate detection only) ──────────────────────
    items_file = PROJECT_ROOT / "data" / "pulse" / "items.json"
    existing_items = []
    if items_file.exists():
        with open(items_file) as f:
            existing_items = json.load(f)
        print(f"Loaded {len(existing_items)} existing items for duplicate check")

    # ── Score + flag each item ────────────────────────────────────────────────
    candidates = []
    for item in raw_items:
        score = calculate_score(item)
        flags = _apply_flags(item, score, existing_items)
        candidate_id = _candidate_id(item)

        candidate = {
            "candidate_id":   candidate_id,
            "title":          item.get("title"),
            "link":           item.get("link"),
            "artifact_type":  item.get("artifact_type", "other"),
            "confidence":     item.get("confidence", "medium"),
            "score":          score,
            "flags":          flags,
            "players":        item.get("players", []),
            "topics":         item.get("topics", []),
            "value_levers":   item.get("value_levers", []),
            "vertical":       item.get("vertical"),
            "persona":        item.get("persona"),
            "source_name":    item.get("source_name"),
            "source_date":    item.get("source_date") or item.get("publish_date"),
            "publish_date":   item.get("publish_date"),
            "discovered_at":  item.get("discovered_at"),
            "summary":        item.get("summary"),
            "description":    item.get("description"),
            "why_it_matters": item.get("why_it_matters"),
            "so_what":        item.get("so_what"),
            "evidence":       item.get("evidence", []),
            "open_questions": item.get("open_questions", []),
        }
        candidates.append(candidate)

        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"  {candidate_id}  score={score:>3}{flag_str}  {item.get('title', '')[:60]}")

    # Sort: high-impact first, then by score desc
    candidates.sort(key=lambda c: (FLAG_HIGH_IMPACT in c["flags"], c["score"]), reverse=True)

    # ── Write candidates.json ─────────────────────────────────────────────────
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    candidates_file = REVIEW_DIR / f"{today}_candidates.json"
    with open(candidates_file, "w") as f:
        json.dump(candidates, f, indent=2)
    print(f"\n  Saved {len(candidates)} candidates → {candidates_file.name}")

    # ── Write approval stub ───────────────────────────────────────────────────
    approval_file = REVIEW_DIR / f"{today}_approval.json"

    # Do NOT overwrite if James has already edited the file today
    if approval_file.exists():
        print(f"  Approval file already exists — not overwriting: {approval_file.name}")
    else:
        all_ids = [c["candidate_id"] for c in candidates]
        approval = {
            "date":              today,
            "generated_at":      datetime.now().isoformat(timespec="seconds"),
            "instructions":      (
                "Move candidate IDs from pending_candidate_ids to approved_candidate_ids "
                "to publish them. Move unwanted IDs to rejected_candidate_ids (or leave "
                "in pending — they will not be published either way)."
            ),
            "pending_candidate_ids":  all_ids,
            "approved_candidate_ids": [],
            "rejected_candidate_ids": [],
        }
        with open(approval_file, "w") as f:
            json.dump(approval, f, indent=2)
        print(f"  Saved approval stub → {approval_file.name}")

    # Flag summary
    all_flags = [f for c in candidates for f in c["flags"]]
    flag_counts = {}
    for fl in all_flags:
        flag_counts[fl] = flag_counts.get(fl, 0) + 1
    print(f"  Flag summary: {flag_counts}")

    high_impact = [c for c in candidates if FLAG_HIGH_IMPACT in c["flags"]]
    print(f"  High-impact candidates: {len(high_impact)}")

    return {
        "total":            len(candidates),
        "high_impact":      len(high_impact),
        "flag_counts":      flag_counts,
        "candidates_file":  str(candidates_file),
        "approval_file":    str(approval_file),
        "candidates":       candidates,
    }


if __name__ == "__main__":
    run_candidates()
