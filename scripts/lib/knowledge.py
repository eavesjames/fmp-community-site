"""
Knowledge retrieval for article-writing agents.

Loads data/knowledge_index.json and provides retrieval functions
that return relevant blocks for grounding article drafts.

Usage:
    from knowledge import retrieve_blocks, format_blocks_for_prompt

    blocks = retrieve_blocks(tags=["installation", "compliance"], article_type="overview")
    context = format_blocks_for_prompt(blocks)
    # Pass context into your writing prompt
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
INDEX_FILE = PROJECT_ROOT / "data" / "knowledge_index.json"

# Required tag categories per article type.
# If an article type requires a category and zero blocks are found for it,
# retrieve_blocks() raises InsufficientKnowledgeError.
ARTICLE_TYPE_REQUIREMENTS = {
    "overview": {
        "required_tags": ["definition", "architecture", "safety", "fit"],
        "min_blocks": 8,
    },
    "installation-guide": {
        "required_tags": ["installation", "technical-specs", "compliance"],
        "min_blocks": 5,
    },
    "compliance-guide": {
        "required_tags": ["compliance", "code", "installation"],
        "min_blocks": 4,
    },
    "case-study": {
        "required_tags": [],       # At least one vertical tag required (checked separately)
        "min_blocks": 3,
    },
    "market-analysis": {
        "required_tags": ["fit", "roi"],
        "min_blocks": 4,
    },
}


class InsufficientKnowledgeError(Exception):
    """Raised when retrieval cannot satisfy minimum block requirements."""
    pass


def load_index() -> list[dict]:
    """Load the knowledge index. Raises FileNotFoundError if not built yet."""
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge index not found at {INDEX_FILE}. "
            "Run: python3 scripts/build_knowledge_index.py"
        )
    with open(INDEX_FILE) as f:
        return json.load(f)


def retrieve_blocks(
    tags: list[str] | None = None,
    block_ids: list[str] | None = None,
    article_type: str | None = None,
    min_confidence: str | None = None,
    limit: int | None = None,
) -> list[dict]:
    """
    Retrieve knowledge blocks matching the given criteria.

    tags:           Return blocks matching ANY of these tags (OR logic)
    block_ids:      Return specific blocks by ID
    article_type:   Apply required-category enforcement from ARTICLE_TYPE_REQUIREMENTS
    min_confidence: Filter to blocks at or above this level ('low' < 'medium' < 'high')
    limit:          Max blocks to return (sorted by confidence desc)

    Raises InsufficientKnowledgeError if article_type requirements are not met.
    """
    index = load_index()
    confidence_rank = {"low": 0, "medium": 1, "high": 2, "unknown": -1}

    # Filter by explicit ID list first
    if block_ids:
        id_set = set(block_ids)
        index = [b for b in index if b["id"] in id_set]

    # Filter by confidence
    if min_confidence:
        min_rank = confidence_rank.get(min_confidence, 0)
        index = [b for b in index if confidence_rank.get(b["confidence"], -1) >= min_rank]

    # Filter by tags (OR logic)
    if tags:
        tag_set = {t.lstrip("#").lower() for t in tags}
        matched = [b for b in index if set(b.get("tags", [])) & tag_set]
    else:
        matched = index[:]

    # Apply article_type enforcement
    if article_type and article_type in ARTICLE_TYPE_REQUIREMENTS:
        reqs = ARTICLE_TYPE_REQUIREMENTS[article_type]
        required_tags = reqs.get("required_tags", [])
        min_blocks = reqs.get("min_blocks", 3)

        # Check required tag coverage
        missing_categories = []
        for req_tag in required_tags:
            tag_blocks = [b for b in matched if req_tag in b.get("tags", [])]
            if not tag_blocks:
                missing_categories.append(req_tag)

        if missing_categories:
            raise InsufficientKnowledgeError(
                f"INSUFFICIENT_KNOWLEDGE_CONTEXT: No blocks found for required "
                f"categories: {missing_categories}. "
                f"Add YAML blocks tagged with: {missing_categories}"
            )

        if len(matched) < min_blocks:
            raise InsufficientKnowledgeError(
                f"INSUFFICIENT_KNOWLEDGE_CONTEXT: Article type '{article_type}' "
                f"requires at least {min_blocks} blocks; only {len(matched)} found."
            )

    # Sort: high confidence first, then by id alphabetically for stability
    matched.sort(key=lambda b: (-confidence_rank.get(b["confidence"], -1), b["id"]))

    if limit:
        matched = matched[:limit]

    return matched


def format_blocks_for_prompt(blocks: list[dict], include_raw: bool = False) -> str:
    """
    Format retrieved knowledge blocks as a text block for injection into prompts.

    include_raw: If True, include the full parsed YAML dict (verbose but complete).
                 If False, include only key_claim + bullets (compact).
    """
    lines = ["=== RETRIEVED KNOWLEDGE BLOCKS ===", ""]

    for block in blocks:
        lines.append(f"[BLOCK_ID: {block['id']}]")
        lines.append(f"Type: {block['type']}")
        lines.append(f"Confidence: {block['confidence']}")
        lines.append(f"Tags: {', '.join('#' + t for t in block.get('tags', []))}")
        lines.append(f"Key claim: {block['key_claim']}")

        if include_raw and block.get("raw"):
            raw = block["raw"]
            # Include bullets if present
            for bullet_key in ("bullets", "items", "checklist_items", "steps"):
                bullets = raw.get(bullet_key, [])
                if bullets:
                    lines.append(f"{bullet_key.capitalize()}:")
                    for b in bullets[:8]:  # Cap at 8 to avoid token bloat
                        lines.append(f"  - {b}")
                    break
            # Include comparison tables if present
            for table_key in ("attributes_table", "mapping", "results.line_items"):
                table = raw.get(table_key)
                if table:
                    lines.append(f"{table_key}:")
                    if isinstance(table, list):
                        for row in table[:6]:
                            lines.append(f"  {row}")
                    break

        lines.append("")  # Blank line between blocks

    lines.append("=== END KNOWLEDGE BLOCKS ===")
    return "\n".join(lines)


def get_block_ids(blocks: list[dict]) -> list[str]:
    """Return list of IDs from a retrieved block list (for knowledge_sources frontmatter)."""
    return [b["id"] for b in blocks]


def check_article_citations(article_text: str, index: list[dict] | None = None) -> dict:
    """
    Validate citations in an article draft.

    Returns a dict with:
      valid_ids:      block IDs cited that exist in index
      unknown_ids:    block IDs cited that do NOT exist in index
      uncited_numbers: lines containing numbers/costs with no adjacent citation
      issues:         list of structured issue dicts
    """
    import re

    if index is None:
        index = load_index()

    known_ids = {b["id"] for b in index}

    # Extract all [BLOCK_ID] style citations
    cited_ids = re.findall(r"\[([A-Z][A-Z0-9_]+)\]", article_text)
    valid_ids = [cid for cid in cited_ids if cid in known_ids]
    unknown_ids = [cid for cid in cited_ids if cid not in known_ids]

    # Scan for lines with numerics that have no citation and aren't labeled [ESTIMATE] or [SYNTHESIS]
    numeric_pattern = re.compile(r"\$[\d,]+|\d+[\d,.]*\s*(?:kW|MW|W|%|ft|m\b|years?|months?|weeks?)")
    issues = []

    for lineno, line in enumerate(article_text.splitlines(), 1):
        if re.search(r"\[ESTIMATE\]|\[SYNTHESIS\]|knowledge_sources|^#|^---", line):
            continue
        if "Synthesis:" in line or "> **" in line:
            continue
        if numeric_pattern.search(line):
            if not re.search(r"\[[A-Z][A-Z0-9_]+\]|\[ESTIMATE\]", line):
                issues.append({
                    "type":   "UNSUPPORTED_NUMERIC_CLAIM",
                    "line":   lineno,
                    "text":   line.strip()[:120],
                })

    return {
        "valid_ids":       valid_ids,
        "unknown_ids":     unknown_ids,
        "uncited_numbers": [i for i in issues if i["type"] == "UNSUPPORTED_NUMERIC_CLAIM"],
        "issues":          issues,
    }
