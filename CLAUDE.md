# CLAUDE.md — FMP Community Site

Updated each session. Always read this first for full project context.

---

## Project Overview

**FMP Community Knowledge Base** — automation-first Hugo site for the Fault Managed Power (FMP) industry.

- **Live URL**: https://faultmanagedpower.org
- **Repo**: `eavesjames/fmp-community-site` on GitHub (Cloudflare Pages auto-deploys from `main`)
- **Local path**: `/Users/jameseaves/Documents/Python/Code/Automation/FMP_org/fmp-site`
- **Hugo theme**: Congo (git submodule)
- **Python**: 3.11

---

## Architecture

```
/content
  /pulse          # Auto-generated industry updates (1 page per item)
  /analysis       # Original in-depth articles
  /insights       # Short insight posts (draft:true until published)
  /guides         # Evergreen how-to guides
  /players        # Organization profiles
  /digests        # Weekly curated summaries (NOT YET POPULATED)
  /glossary       # Term definitions (NOT YET POPULATED)
  /topics         # Evergreen topic hubs (NOT YET POPULATED)
  /library        # Calculators, whitepapers (NOT YET POPULATED)
/data
  /pulse/raw/           # Raw SerpAPI intake results
  /pulse/extracted/     # Claude-enriched metadata
  /pulse/items.json     # Master normalized list
  /review/              # Approval files: YYYY-MM-DD_candidates.json, _approval.json, _insights_registry.json
  /insights/            # YYYY-MM-DD_analysts.json, _moderator.json
  /social/              # YYYY-MM-DD_social_drafts.json
  /claims/              # Evidence tables for major content
  /knowledge_index.json # Built by build_knowledge_index.py
  /article_type_requirements.yaml
/config
  sources.yaml    # Players + site config
  queries.yaml    # SerpAPI search queries
/scripts
  run.py                  # CLI entrypoint
  build_knowledge_index.py
  validate.py
  linkedin_auth.py
  lib/                    # Pipeline modules (see below)
/.github/workflows/       # GitHub Actions (committed, active)
  daily_generate.yml      # Phase 1 — 9 AM UTC daily
  daily_publish.yml       # Phase 2 — manual trigger only
  daily_pulse.yml         # Legacy fallback — manual only
  weekly_digest.yml       # Mondays 10 AM UTC
```

### Pipeline Modules (`scripts/lib/`)

| Module | Purpose |
|---|---|
| `intake.py` | Fetch content via SerpAPI |
| `extract.py` | Enrich metadata with Claude |
| `normalize.py` | Dedupe + score items (legacy daily flow) |
| `candidates.py` | Score items, write candidates + approval stub |
| `render_pulse.py` | Generate Pulse markdown pages |
| `insights.py` | Multi-agent insights engine |
| `social.py` | Generate social media drafts |
| `digest.py` | Weekly digest generation |
| `evergreen.py` | Update topic hub pages |
| `glossary.py` | Suggest glossary terms |
| `knowledge.py` | Knowledge grounding system |
| `pr.py` | GitHub PR automation |
| `publish_approved.py` | Publish approved candidates |
| `publish_social.py` | Post LinkedIn drafts |
| `email_digest.py` | Send review email (uses Resend API) |
| `prompt_loader.py` | File-based prompt loading |

### Two-Phase Daily Workflow

**Phase 1 — Generate** (automated, 9 AM UTC via `daily_generate.yml`):
1. `intake` → `extract` → `candidates` → `insights` → `social_drafts`
2. Push branch `daily-generate-YYYYMMDD`
3. Send review email with links to approval file

**Phase 2 — Publish** (manual, triggered via `daily_publish.yml`):
1. You edit `data/review/YYYY-MM-DD_approval.json` to approve/reject candidates
2. Trigger `Daily Publish` workflow in GitHub Actions with the branch name
3. Pipeline publishes approved items, renders pages, opens PR
4. You review and merge PR → Cloudflare auto-deploys

### CLI Commands

```bash
cd scripts

# Modern two-phase workflow
python3 run.py generate              # Phase 1: intake→extract→candidates→insights→email
python3 run.py publish               # Phase 2: publish approved → open PR
python3 run.py publish --date YYYY-MM-DD

# Weekly
python3 run.py weekly                # digest→evergreen→glossary→social drafts

# Individual steps
python3 run.py intake
python3 run.py extract
python3 run.py candidates
python3 run.py insights
python3 run.py social_drafts
python3 run.py digest_weekly
python3 run.py evergreen_update
python3 run.py glossary_suggest

# Other
python3 run.py approve_all           # Approve all candidates then publish
python3 run.py send_review_email
python3 run.py social_publish [--dry-run]
python3 run.py open_daily_pr

# Legacy (no review gate)
python3 run.py daily
```

---

## Players / Sources (`config/sources.yaml`)

- **VoltServer** — Primary OEM / FMP supplier
- **Panduit** — OEM / infrastructure supplier
- **Cisco** — Focus on power/building/OT topics
- **FMP Alliance** — Industry group

Player pages exist for VoltServer and Panduit only. Cisco page not yet created.

---

## Content Status (as of 2026-03-06)

| Section | Count | Status |
|---|---|---|
| Pulse items | 104 | Active, pipeline running |
| Analysis | 7 | Active |
| Insights | 7 (published) | Active — insight drafts in `content/insights/` |
| Guides | 6 | Active |
| Players | 2 | VoltServer + Panduit only |
| Digests | 0 | **Not started** |
| Glossary | 0 | **Not started** |
| Topics | 0 | **Not started** |
| Library | 0 | **Not started** |

Most recent pipeline runs: 2026-02-27, 2026-03-03

---

## Deployment

- **Cloudflare Pages**: Auto-deploys from `main`
- **Build command**: `hugo --minify`
- **Hugo version**: `0.156.0` (env var in Cloudflare)

### Required Secrets (GitHub Actions)

| Secret | Used by |
|---|---|
| `ANTHROPIC_API_KEY` | extract, insights, digest, evergreen, glossary |
| `SERP_API_KEY` | intake |
| `RESEND_API_KEY` | send_review_email |
| `REVIEW_EMAIL_TO` | send_review_email |
| `GH_TOKEN` | auto (github.token for PR creation) |

---

## Frozen Frame Policy

**Automated PRs may modify**: `/content/**`, `/data/**`, `/config/sources.yaml`, `/config/queries.yaml`

**Manual only**: `/layouts/**`, Hugo config, theme code, deployment settings, `.github/workflows/`

---

## Evidence Gate

Major content requires claim tables at `/data/claims/{artifact_id}.json`:
- Fields: `claim_id`, `claim_text`, `evidence_urls`, `assumptions`, `confidence`

---

## What's Left / Next Priorities

1. **Digests** — `/content/digests/` is empty. Run `python3 run.py weekly` or `digest_weekly` to generate first weekly digest
2. **Glossary** — `/content/glossary/` is empty. Run `python3 run.py glossary_suggest` then review
3. **Topics** — `/content/topics/` is empty. Run `python3 run.py evergreen_update` to generate topic hubs
4. **Cisco player page** — `config/sources.yaml` has Cisco configured but no player page in `/content/players/`
5. **Library** — Add calculator/whitepaper landing pages (manual content)
6. **Verify automation is running** — Check GitHub Actions tab to confirm `daily_generate.yml` has been running daily

---

## Key Conventions

- Pulse page filenames: `{date}-{player}-{slug}.md`
- Insight pages: created as `draft: true`, published via Phase 2 approval flow
- Knowledge grounding: major articles must reference YAML knowledge blocks; `build_knowledge_index.py` rebuilds `data/knowledge_index.json`
- Validation: `scripts/validate.py content/pulse/` — non-blocking in CI
