#!/usr/bin/env python3
"""
Build a flat knowledge index from YAML knowledge files.

Reads all .yaml files from the knowledge directory, extracts IDs, tags,
key_claims, confidence, and relevant text, and writes a single JSON index
to data/knowledge_index.json.

Usage:
    python3 build_knowledge_index.py

Run whenever the YAML knowledge files change.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_DIR = Path("/Users/jameseaves/VoltServer Dropbox/James Eaves/06_BizDev/FMP_System/knowledge")
OUTPUT_FILE = PROJECT_ROOT / "data" / "knowledge_index.json"


def _extract_id(data: dict, filename: str) -> str:
    """Extract the block ID from the YAML data, falling back to filename."""
    for key in ("id", "knowledge.id", "data.id"):
        if key in data:
            return str(data[key])
    # Try nested keys
    if "knowledge" in data and isinstance(data["knowledge"], dict):
        if "id" in data["knowledge"]:
            return str(data["knowledge"]["id"])
    if "data" in data and isinstance(data["data"], dict):
        if "id" in data["data"]:
            return str(data["data"]["id"])
    # Fall back to filename without extension
    return Path(filename).stem


def _extract_tags(data: dict, raw_text: str = "") -> list[str]:
    """
    Extract tags list from YAML data.
    Falls back to raw text regex scan because bare #tag syntax is treated
    as a YAML comment by the parser, leaving tags: null.
    """
    tags = data.get("tags")

    # Parsed value is usable
    if isinstance(tags, str) and tags.strip():
        return re.findall(r"[\w-]+", tags)
    if isinstance(tags, list) and any(t is not None for t in tags):
        return [str(t).lstrip("#") for t in tags if t is not None]

    # Fall back: scan the raw file text.
    # Handles two formats:
    #   tags: #foo, #bar           (single line, value treated as comment by PyYAML)
    #   tags:                      (list format, items also treated as comments)
    #     - #foo
    #     - #bar
    if raw_text:
        lines = raw_text.splitlines()
        in_tags_block = False
        found = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("tags:"):
                in_tags_block = True
                # Same-line tags: "tags: #foo, #bar"
                same_line = re.findall(r"#([\w-]+)", line)
                found.extend(same_line)
                continue
            if in_tags_block:
                # List items: "  - #foo"
                if re.match(r"^\s+-\s+#", line):
                    tag = re.search(r"#([\w-]+)", line)
                    if tag:
                        found.append(tag.group(1))
                elif stripped and not stripped.startswith("-"):
                    # End of tags block
                    in_tags_block = False
        if found:
            return found
    return []


def _extract_key_claim(data: dict) -> str:
    """Extract the primary claim text."""
    for key in ("key_claim", "summary.what_it_is", "title"):
        if key in data and data[key]:
            return str(data[key])
    # Try nested
    if "summary" in data and isinstance(data["summary"], dict):
        for subkey in ("what_it_is", "core_message"):
            if subkey in data["summary"] and data["summary"][subkey]:
                return str(data["summary"][subkey])
    return ""


def _extract_block_type(data: dict, filename: str) -> str:
    """Extract block type."""
    for key in ("type", "knowledge.type"):
        if key in data:
            return str(data[key])
    if "knowledge" in data and isinstance(data["knowledge"], dict):
        if "type" in data["knowledge"]:
            return str(data["knowledge"]["type"])
    # Infer from filename prefix
    stem = Path(filename).stem
    for prefix in ("CLAIM_", "MAP_", "RULESET_", "DATA_", "PROC_", "CHK_", "OBJ_", "EXPL_"):
        if stem.startswith(prefix):
            return prefix.rstrip("_").lower()
    return "document"


def _extract_confidence(data: dict) -> str:
    """Extract confidence level."""
    for key in ("confidence", "status.confidence"):
        if key in data:
            return str(data[key])
    if "status" in data and isinstance(data["status"], dict):
        if "confidence" in data["status"]:
            return str(data["status"]["confidence"])
    return "unknown"


def _extract_bullets(data: dict) -> list[str]:
    """Extract bullet points / key supporting claims."""
    bullets = data.get("bullets", [])
    if isinstance(bullets, list):
        return [str(b) for b in bullets]
    return []


def _extract_text_summary(data: dict) -> str:
    """Build a short text summary for embedding / search."""
    parts = []
    claim = _extract_key_claim(data)
    if claim:
        parts.append(claim)
    bullets = _extract_bullets(data)
    parts.extend(bullets[:3])  # First 3 bullets
    return " | ".join(parts)


def build_index() -> list[dict]:
    """Read all YAML files and build flat index entries."""
    if not KNOWLEDGE_DIR.exists():
        print(f"ERROR: Knowledge directory not found: {KNOWLEDGE_DIR}")
        sys.exit(1)

    yaml_files = sorted(KNOWLEDGE_DIR.glob("*.yaml"))
    print(f"Found {len(yaml_files)} YAML files in {KNOWLEDGE_DIR.name}/")

    index = []
    errors = []

    for yaml_file in yaml_files:
        try:
            with open(yaml_file, encoding="utf-8") as f:
                raw = f.read()

            # PyYAML: use safe_load; handle multi-document files
            data = yaml.safe_load(raw)
            if not isinstance(data, dict):
                errors.append(f"  Skipping {yaml_file.name}: not a dict at top level")
                continue

            block_id = _extract_id(data, yaml_file.name)
            tags = _extract_tags(data, raw)
            block_type = _extract_block_type(data, yaml_file.name)
            confidence = _extract_confidence(data)
            key_claim = _extract_key_claim(data)
            text_summary = _extract_text_summary(data)

            entry = {
                "id":           block_id,
                "file":         yaml_file.name,
                "type":         block_type,
                "tags":         tags,
                "confidence":   confidence,
                "key_claim":    key_claim,
                "text_summary": text_summary,
                "raw":          data,   # Full parsed YAML for prompt injection
            }
            index.append(entry)
            print(f"  ✓ {block_id}  [{block_type}]  tags={tags}")

        except yaml.YAMLError as e:
            errors.append(f"  YAML error in {yaml_file.name}: {e}")
        except Exception as e:
            errors.append(f"  Error in {yaml_file.name}: {e}")

    if errors:
        print("\nWarnings:")
        for e in errors:
            print(e)

    return index


def main():
    print("Building knowledge index...")
    index = build_index()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(index, f, indent=2)

    print(f"\nIndex built: {len(index)} blocks → {OUTPUT_FILE}")

    # Print tag summary
    all_tags = {}
    for entry in index:
        for tag in entry["tags"]:
            all_tags[tag] = all_tags.get(tag, 0) + 1
    print("\nTag coverage:")
    for tag, count in sorted(all_tags.items(), key=lambda x: -x[1]):
        print(f"  #{tag}: {count} block(s)")


if __name__ == "__main__":
    main()
