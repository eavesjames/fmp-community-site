"""Phase 2: Publish only approved candidates from today's approval.json.

Strict validation: any malformed or missing approval file causes exit(1).
Nothing is published if approved_candidate_ids is empty.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
REVIEW_DIR = PROJECT_ROOT / "data" / "review"


def _load_or_die(path: Path, label: str) -> dict | list:
    """Load JSON or exit(1) with a clear message."""
    if not path.exists():
        print(f"ERROR: {label} not found: {path}", file=sys.stderr)
        print("Run `python3 run.py generate` first to create review files.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {label} is not valid JSON: {e}", file=sys.stderr)
        print(f"File: {path}", file=sys.stderr)
        sys.exit(1)


def _validate_approval(approval: dict, date: str) -> list[str]:
    """
    Validate approval JSON schema. Returns approved_candidate_ids on success.
    Calls sys.exit(1) on any structural problem.
    """
    required_keys = {"date", "pending_candidate_ids", "approved_candidate_ids", "rejected_candidate_ids"}
    missing = required_keys - set(approval.keys())
    if missing:
        print(f"ERROR: approval.json is missing required keys: {missing}", file=sys.stderr)
        sys.exit(1)

    if approval.get("date") != date:
        print(
            f"ERROR: approval.json date '{approval.get('date')}' does not match today '{date}'.",
            file=sys.stderr,
        )
        print("If running after midnight, use the --date flag.", file=sys.stderr)
        sys.exit(1)

    approved_ids = approval["approved_candidate_ids"]
    if not isinstance(approved_ids, list):
        print("ERROR: approved_candidate_ids must be a JSON array.", file=sys.stderr)
        sys.exit(1)

    return approved_ids


def run_publish_approved(date: str | None = None) -> dict:
    """
    Phase 2: read approval.json → filter approved candidates →
    write to items.json → render pulse pages.

    Returns dict with stats.
    """
    # Local imports here to avoid circular imports when this module is imported
    from normalize import write_approved_to_master
    from render_pulse import render_pulse_pages

    today = date or datetime.now().strftime("%Y-%m-%d")
    print(f"Running publish_approved for {today}...")

    # ── Load and validate approval file ──────────────────────────────────────
    approval_file = REVIEW_DIR / f"{today}_approval.json"
    approval = _load_or_die(approval_file, "approval.json")
    approved_ids = _validate_approval(approval, today)

    if not approved_ids:
        print("No approved_candidate_ids in approval.json — nothing to publish.")
        return {"published": 0, "skipped": 0, "new_items": []}

    print(f"  Approved IDs: {approved_ids}")

    # ── Load candidates ───────────────────────────────────────────────────────
    candidates_file = REVIEW_DIR / f"{today}_candidates.json"
    all_candidates = _load_or_die(candidates_file, "candidates.json")
    if not isinstance(all_candidates, list):
        print("ERROR: candidates.json must be a JSON array.", file=sys.stderr)
        sys.exit(1)

    # Build id → candidate map
    cand_by_id = {c["candidate_id"]: c for c in all_candidates if "candidate_id" in c}

    # Filter to approved
    approved_candidates = []
    missing_ids = []
    for cid in approved_ids:
        if cid in cand_by_id:
            approved_candidates.append(cand_by_id[cid])
        else:
            missing_ids.append(cid)

    if missing_ids:
        print(
            f"WARNING: {len(missing_ids)} approved ID(s) not found in candidates.json: {missing_ids}",
            file=sys.stderr,
        )

    if not approved_candidates:
        print("No matching candidates found for approved IDs — nothing to publish.")
        return {"published": 0, "skipped": 0, "new_items": []}

    print(f"  Publishing {len(approved_candidates)} approved candidate(s)...")

    # ── Write approved candidates to items.json ───────────────────────────────
    write_result = write_approved_to_master(approved_candidates)
    new_items = write_result.get("new_items", [])

    # ── Render pulse pages for all items in items.json ────────────────────────
    render_pulse_pages()

    # ── Flip insight drafts to READY if registry exists ───────────────────────
    _maybe_update_insight_registry(today)

    print(f"\nPublish complete: {write_result['written']} published, {write_result['skipped']} skipped")
    return {
        "published":  write_result["written"],
        "skipped":    write_result["skipped"],
        "new_items":  new_items,
    }


def _maybe_update_insight_registry(today: str):
    """
    Mark DRAFT insights as READY in the registry if their draft .md files exist.
    This is a best-effort step — we do not exit on failure.
    """
    registry_file = REVIEW_DIR / f"{today}_insights_registry.json"
    if not registry_file.exists():
        return

    try:
        with open(registry_file) as f:
            registry = json.load(f)

        updated = False
        for entry in registry.get("insights", []):
            if entry.get("status") == "DRAFT":
                draft_path = PROJECT_ROOT / entry.get("draft_path", "")
                if draft_path.exists():
                    # Check if draft: false has been set (manual signal it's ready)
                    content = draft_path.read_text()
                    if "draft: false" in content:
                        entry["status"] = "READY"
                        updated = True
                        print(f"  Insight {entry['insight_id']} marked READY")

        if updated:
            with open(registry_file, "w") as f:
                json.dump(registry, f, indent=2)
    except Exception as e:
        print(f"  Warning: could not update insights registry: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Override date (YYYY-MM-DD)")
    args = parser.parse_args()
    run_publish_approved(date=args.date)
