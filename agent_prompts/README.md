# Agent Prompts

Prompt templates and output schemas for the FMP pipeline's multi-agent insight and social draft stages.

## File naming convention

Every agent has two files:

| File | Contents |
|------|----------|
| `{name}.md` | Human-readable prompt text. May include `{{PLACEHOLDER}}` variables. |
| `{name}_output.md` | Pure JSON — the output schema the model must match. **No other content.** |

`SHARED_HEADER.md` is injected into every analyst/moderator prompt via `{{SHARED_HEADER}}`.

## Required files

```
SHARED_HEADER.md
analyst_installer.md          analyst_installer_output.md
analyst_owner_operator.md     analyst_owner_operator_output.md
analyst_compliance.md         analyst_compliance_output.md
analyst_mep.md                analyst_mep_output.md
analyst_finance.md            analyst_finance_output.md
moderator_synthesis.md        moderator_synthesis_output.md
social_drafts.md              social_drafts_output.md
```

## Prompt placeholders

| Placeholder | Used in |
|-------------|---------|
| `{{SHARED_HEADER}}` | All analyst + moderator prompts |
| `{{RUN_DATE}}` | All prompts |
| `{{VERTICAL_COVERAGE_STATS}}` | All analyst + moderator prompts |
| `{{PULSE_ITEMS_JSON}}` | All analyst + moderator prompts |
| `{{ANALYST_OUTPUTS_JSON}}` | `moderator_synthesis.md` only |
| `{{MODERATOR_OUTPUT_JSON}}` | `social_drafts.md` only |
| `{{TOP_PULSE_ITEMS_JSON}}` | `social_drafts.md` only |

## Validate all output schemas

Run from the repo root:

```bash
python3 -c "
import json
from pathlib import Path
d = Path('agent_prompts')
errors = 0
for f in sorted(d.glob('*_output.md')):
    try:
        json.loads(f.read_text())
        print(f'  ok  {f.name}')
    except json.JSONDecodeError as e:
        print(f'  FAIL {f.name}: {e}')
        errors += 1
exit(errors)
"
```

## How the loader works

`scripts/lib/prompt_loader.py` assembles the final prompt:

1. Reads `{name}.md`
2. Substitutes `{{SHARED_HEADER}}` with `SHARED_HEADER.md` content
3. Substitutes all `{{VARIABLE}}` placeholders with caller-provided values
4. Appends `\nSCHEMA:\n` + contents of `{name}_output.md`

The assembled string is sent directly to the Claude API.
