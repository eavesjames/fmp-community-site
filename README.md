# FMP Community Knowledge Base

Automation-first Hugo site for Fault Managed Power (FMP) industry updates and resources.

## Project Structure

```
/content          # Hugo content (Pulse, digests, topics, players, glossary, library)
/data             # JSON data stores (pulse items, claims, library metadata)
/config           # Configuration (sources.yaml, queries.yaml)
/scripts          # Python automation orchestrator
  /lib            # Automation modules
/. github/workflows  # GitHub Actions (daily_pulse.yml, weekly_digest.yml)
/themes/congo     # Hugo Congo theme (submodule)
```

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd fmp-site
git submodule update --init --recursive
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys:
# - ANTHROPIC_API_KEY
# - SERP_API_KEY
```

### 3. Test locally

```bash
hugo server --buildDrafts
```

Visit: http://localhost:1313

## Automation

### Daily Workflow (GitHub Actions)

Runs at 9 AM UTC daily:
1. Intake: Fetch new content from configured sources
2. Extract: Enrich metadata using Claude
3. Normalize: Dedupe and score items
4. Render: Generate one Pulse page per item
5. Open PR for human review

Manual trigger:
```bash
cd scripts
python3 run.py daily
```

### Weekly Workflow (GitHub Actions)

Runs 10 AM UTC every Monday:
1. Generate weekly digest
2. Update evergreen topic pages
3. Suggest new glossary terms
4. Generate social media drafts
5. Open PR for human review

Manual trigger:
```bash
cd scripts
python3 run.py weekly
```

## CLI Commands

```bash
cd scripts

# Individual steps
python3 run.py intake                # Fetch content
python3 run.py extract               # Extract metadata
python3 run.py normalize             # Dedupe and normalize
python3 run.py render_pulse_pages    # Generate Pulse pages
python3 run.py digest_weekly         # Generate weekly digest
python3 run.py evergreen_update      # Update topic hubs
python3 run.py glossary_suggest      # Suggest glossary terms
python3 run.py social_drafts         # Generate social drafts

# Full workflows
python3 run.py daily    # Run full daily workflow
python3 run.py weekly   # Run full weekly workflow

# PR management
python3 run.py open_pr --title "Update title" --body "Description"
```

## Content Types

### Pulse Items (`/pulse/{slug}/`)
One page per industry update. Auto-generated from sources.

### Weekly Digests (`/digests/{slug}/`)
Curated summary of top Pulse items with implications.

### Topic Hubs (`/topics/{slug}/`)
Evergreen pages that update over time (e.g., safety-model, estimating).

### Player Pages (`/players/{slug}/`)
Organization profiles (VoltServer, Panduit, Cisco, FMP Alliance).

### Glossary (`/glossary/{term}/`)
Term definitions for SEO.

### Library (`/library/{slug}/`)
Landing pages for calculators, templates, whitepapers.

## Deployment

Site deploys to Cloudflare Pages from `main` branch:
- **Production**: https://faultmanagedpower.org
- **Preview**: Auto-generated for PRs

### Cloudflare Pages Configuration

- Framework: Hugo
- Build command: `hugo --minify`
- Build output: `public`
- Root directory: `/`
- Environment variables:
  - `HUGO_VERSION` = `0.156.0`

## Evidence Gate

Major content (digests, original posts, evergreen updates) requires claim tables:
- Location: `/data/claims/{artifact_id}.json`
- Format: claim_id, claim_text, evidence_urls, assumptions, confidence

## Contributing

1. Agents open PRs with generated content
2. Human reviews PR (check claims, quality, relevance)
3. Human merges PR or requests changes
4. Cloudflare Pages auto-deploys on merge

## Frozen Frame Policy

**Automated PRs can modify**:
- `/content/**` 
- `/data/**`
- `/config/sources.yaml`
- `/config/queries.yaml`

**Site maintenance PRs only** (manual):
- `/layouts/**`
- Hugo config
- Theme code
- Deployment settings

## License

Content: CC BY 4.0
Code: MIT
