#!/usr/bin/env python3
"""
Validate front matter for faultmanagedpower.org content files.

Usage:
  python3 scripts/validate.py content/pulse/          # all pulse items
  python3 scripts/validate.py content/                # entire content tree
  python3 scripts/validate.py path/to/post.md         # single file
  python3 scripts/validate.py --strict content/       # fail on warnings too

Exit codes:
  0 — all files valid (warnings may still be printed)
  1 — one or more files have errors (or warnings in --strict mode)
"""

import sys
import re
import yaml
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

# ── Controlled vocabularies ────────────────────────────────────────────────

VALID_VERTICALS = {
    "edge-power-ups",
    "data-centers",
    "building-electrification",
}

VALID_PERSONAS = {
    "owner-operator",
    "facilities",
    "it-network",
    "security-integrator",
    "ot-controls",
    "gc-mep",
    "electrical-contractor",
}

VALID_TOPICS = {
    "safety-model",
    "code-standards",
    "pathways-install",
    "estimating",
    "schedule-value",
    "monitoring-telemetry",
    "ups-resilience",
    "ot-controls-plc",
    "physical-security",
    "power-quality-surge",
    "dc-distribution",
    "commissioning",
    "reliability-uptime",
    "prefab-modular",
    "labor-productivity",
    "ai-infrastructure",
    "incentives-policy",
    "retrofits-mdus",
}

# Required fields per content type
REQUIRED = {
    "pulse":     ["title", "date", "source_name", "source_url", "source_date",
                  "vertical", "topics", "persona", "so_what", "summary"],
    "originals": ["title", "date", "topics", "thesis", "sources"],
    "guides":    ["title", "date", "topics", "summary"],
}

SO_WHAT_MAX = 160


# ── Helpers ────────────────────────────────────────────────────────────────

def load_players(repo_root: Path) -> set:
    """Load valid player keys from data/players.yaml."""
    players_file = repo_root / "data" / "players.yaml"
    if not players_file.exists():
        return set()
    with open(players_file) as f:
        data = yaml.safe_load(f)
    return {p["key"] for p in (data or [])}


def parse_frontmatter(path: Path):
    """Extract YAML front matter from a markdown file. Returns dict or None."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        return yaml.safe_load(text[3:end])
    except yaml.YAMLError as e:
        return {"_yaml_error": str(e)}


def detect_type(path: Path) -> str | None:
    """Detect content type from file path."""
    parts = path.parts
    for i, part in enumerate(parts):
        if part in ("pulse", "originals", "guides"):
            return part
    return None


def is_valid_url(value: str) -> bool:
    try:
        r = urlparse(str(value))
        return r.scheme in ("http", "https") and bool(r.netloc)
    except Exception:
        return False


def is_valid_date(value) -> bool:
    if isinstance(value, datetime):
        return True
    try:
        datetime.strptime(str(value), "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ── Validator ──────────────────────────────────────────────────────────────

def validate_file(path: Path, valid_players: set, strict: bool) -> tuple[int, int]:
    """
    Validate a single markdown file.
    Returns (error_count, warning_count).
    """
    errors = []
    warnings = []

    # Skip section index files — they are not content items
    if path.name == "_index.md":
        return 0, 0

    fm = parse_frontmatter(path)

    if fm is None:
        # No front matter — skip silently
        return 0, 0

    if "_yaml_error" in fm:
        errors.append(f"YAML parse error: {fm['_yaml_error']}")
        _report(path, errors, warnings)
        return len(errors), len(warnings)

    content_type = detect_type(path)
    if content_type is None:
        # Not a managed content type — skip
        return 0, 0

    # Legacy pulse posts (pre-Phase 2 schema) lack source_url — skip strict checks
    if content_type == "pulse" and not fm.get("source_url"):
        print(f"  ↷ LEGACY  {path} (no source_url — skipping Phase 2 field checks)")
        return 0, 0

    required = REQUIRED.get(content_type, [])

    # ── Required fields ──
    for field in required:
        if field not in fm or fm[field] is None or fm[field] == "":
            errors.append(f"Missing required field: '{field}'")

    if errors:
        _report(path, errors, warnings)
        return len(errors), len(warnings)

    # ── Type-specific validation ──
    if content_type == "pulse":

        # source_date format
        if not is_valid_date(fm.get("source_date", "")):
            errors.append(f"source_date must be YYYY-MM-DD, got: {fm.get('source_date')!r}")

        # source_url
        if not is_valid_url(fm.get("source_url", "")):
            errors.append(f"source_url is not a valid URL: {fm.get('source_url')!r}")

        # vertical
        v = fm.get("vertical", "")
        if v not in VALID_VERTICALS:
            errors.append(f"Invalid vertical: {v!r}. Must be one of: {sorted(VALID_VERTICALS)}")

        # persona
        p = fm.get("persona", "")
        if p not in VALID_PERSONAS:
            errors.append(f"Invalid persona: {p!r}. Must be one of: {sorted(VALID_PERSONAS)}")

        # topics
        topics = fm.get("topics") or []
        for t in topics:
            if t not in VALID_TOPICS:
                warnings.append(f"Unknown topic: {t!r}. Known: {sorted(VALID_TOPICS)}")

        # players
        players = fm.get("players") or []
        for pl in players:
            if valid_players and pl not in valid_players:
                warnings.append(f"Unknown player key: {pl!r}. Known: {sorted(valid_players)}")

        # so_what length
        so_what = fm.get("so_what", "")
        if len(so_what) > SO_WHAT_MAX:
            warnings.append(
                f"so_what is {len(so_what)} chars (max {SO_WHAT_MAX}): {so_what[:60]}..."
            )

    elif content_type == "originals":
        sources = fm.get("sources") or []
        for s in sources:
            if not is_valid_url(s):
                warnings.append(f"sources entry is not a valid URL: {s!r}")

    _report(path, errors, warnings)
    return len(errors), len(warnings)


def _report(path: Path, errors: list, warnings: list):
    if not errors and not warnings:
        return
    print(f"\n{path}")
    for e in errors:
        print(f"  ✗ ERROR   {e}")
    for w in warnings:
        print(f"  ⚠ WARNING {w}")


# ── Entry point ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    paths  = [a for a in args if not a.startswith("--")]

    if not paths:
        print("Usage: python3 scripts/validate.py [--strict] <path|dir> ...")
        sys.exit(0)

    # Locate repo root (directory containing data/players.yaml)
    script_dir  = Path(__file__).resolve().parent
    repo_root   = script_dir.parent
    valid_players = load_players(repo_root)

    files = []
    for p in paths:
        target = Path(p)
        if target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
        elif target.is_file():
            files.append(target)
        else:
            print(f"Path not found: {p}")
            sys.exit(1)

    if not files:
        print("No markdown files found.")
        sys.exit(0)

    total_errors   = 0
    total_warnings = 0
    checked        = 0

    for f in files:
        e, w = validate_file(f, valid_players, strict)
        total_errors   += e
        total_warnings += w
        if e == 0 and w == 0:
            checked += 1

    total = len(files)
    print(f"\n{'─'*50}")
    print(f"Checked {total} files — "
          f"{total - total_errors - (total_warnings if strict else 0)} clean, "
          f"{total_errors} error(s), "
          f"{total_warnings} warning(s)")

    if total_errors > 0 or (strict and total_warnings > 0):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
