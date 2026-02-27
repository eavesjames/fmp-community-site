"""Load and render agent prompt templates from agent_prompts/ directory."""
from pathlib import Path

# agent_prompts/ lives at the repo root, two levels above scripts/lib/
PROMPTS_DIR = Path(__file__).parent.parent.parent.parent / "agent_prompts"


def load_prompt(name: str, **variables) -> str:
    """
    Assemble a complete agent prompt.

    Steps:
      1. Read  agent_prompts/{name}.md
      2. Inject SHARED_HEADER.md into {{SHARED_HEADER}}
      3. Substitute every {{KEY}} with variables[KEY]
      4. Append agent_prompts/{name}_output.md as the output schema

    Returns the fully assembled prompt string ready to send to Claude.
    Raises FileNotFoundError if the prompt file is missing.
    """
    prompt_path = PROMPTS_DIR / f"{name}.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    text = prompt_path.read_text(encoding="utf-8")

    # Inject shared header first so its content can also contain placeholders
    shared_path = PROMPTS_DIR / "SHARED_HEADER.md"
    if shared_path.exists():
        shared = shared_path.read_text(encoding="utf-8")
        text = text.replace("{{SHARED_HEADER}}", shared)

    # Substitute caller-provided variables
    for key, val in variables.items():
        text = text.replace("{{" + key + "}}", str(val) if val is not None else "")

    # Append output schema
    schema_path = PROMPTS_DIR / f"{name}_output.md"
    if schema_path.exists():
        schema = schema_path.read_text(encoding="utf-8")
        text = text.rstrip() + "\n\nSCHEMA:\n" + schema

    return text
