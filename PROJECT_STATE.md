# FMP Community Site — Project State
<!-- INSTRUCTIONS FOR CLAUDE: This file must be kept current at the end of every working session.
     Update "Current Status", "Pending Decisions", and "Next Steps" whenever anything changes.
     Do not summarize or compress history — keep all sections accurate and complete. -->

**Last updated:** 2026-02-26
**Project:** FMP Community Knowledge Base — faultmanagedpower.org
**Owner:** James Eaves, PhD — Director of Building Electrification, VoltServer

---

## What This Project Is

An automation-first public knowledge base for Fault Managed Power (FMP / NEC Class 4) technology. A Hugo static site deployed on Cloudflare Pages, with Python automation that runs daily via GitHub Actions to find, extract, score, and publish industry news as "Pulse" items — reducing three frictions for FMP adopters:

1. **Decision friction** — when does FMP make sense vs conventional AC?
2. **Estimating friction** — pricing and comparison tools
3. **Coordination/approval friction** — specs and deployment guides

**Live URL:** https://faultmanagedpower.org
**Requirements doc:** `/Users/jameseaves/Documents/Python/Code/Automation/FMP_org/Claude Code Requirements: FMP Community Site + FMP Pulse (Hugo + Cloudflare Pages).html`

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Static site generator | Hugo 0.156.0 |
| Theme | PaperMod (git submodule) |
| Hosting | Cloudflare Pages (free tier) |
| Automation | Python 3.11 + GitHub Actions |
| Search/intake | SerpAPI |
| AI extraction | Anthropic Claude Sonnet 4.5 |
| Deployment | GitHub → Cloudflare auto-build |

---

## Current Status (2026-03-30)

### Overall Completion: ~70%
Phase 1 site redesign complete (homepage layout rewrite). New FMP-branded homepage is live locally: Hero → Tools (email gate) → Learn (5 guides) → Standards (4 cards) → About strip. Phase 2 RCP layout preserved on /pulse/ and archive pages. Foundation, daily automation pipeline, and all key layout templates working.

### Phase 1 Homepage Redesign ✅ (2026-03-30)
- `layouts/index.html` — fully rewritten: Hero / Tools / Learn / Standards / About
- `assets/css/extended/rcp.css` — `.fmp-*` classes appended; original `.rcp-*` classes intact
- `content/tools/_index.md` — created (title: "FMP Tools")
- All 5 guide front matters updated: weight 1–5 and spec-matched summaries
- `hugo --minify` → 341 pages, zero errors, zero warnings
- Homepage confirmed rendering all sections at http://localhost:1313/

### What's Working ✅
- Hugo site builds and deploys to Cloudflare Pages
- **Full daily pipeline:** SerpAPI intake → Claude extraction → normalize/dedupe → render Pulse markdown → GitHub PR
- 15 Pulse items published (12 legacy + 3 Phase 2 example posts)
- 2 Player pages: VoltServer, Panduit
- GitHub Actions workflows for daily (9 AM UTC) and weekly (Mon 10 AM UTC)
- `data/pulse/items.json` master list with scoring
- `.env` with working API keys (ANTHROPIC_API_KEY, SERP_API_KEY)
- **Phase 2 RCP layout** — all 7 commits pushed to main and live on Cloudflare:
  - 3-column homepage by vertical (edge-power-ups / data-centers / building-electrification)
  - `so_what` line on every row
  - Originals strip on homepage (hidden when empty)
  - Source_date sort (newest source first)
  - Vertical hub pages (`/verticals/<term>/`) with Start Here guides + pulse feed
  - Taxonomy index pages (`/verticals/`, `/topics/`, `/personas/`)
  - Paginated pulse list at `/pulse/` (50/page)
  - `data/players.yaml` canonical player registry
  - `scripts/validate.py` — front matter validator with controlled vocabularies
  - `layouts/pulse/single.html` — individual pulse page with Open Source button, so_what quote, related items
  - Player attribution fixed: rows show source domain from `canonical_source`, not players[0]

### Phase 2 Schema (required for new Pulse posts)
New posts must include these fields beyond the legacy schema:
```yaml
source_name: "Publication Name"
source_url: "https://..."
source_date: YYYY-MM-DD
vertical: "edge-power-ups" | "data-centers" | "building-electrification"
topics: ["code-standards", ...]   # see VALID_TOPICS in scripts/validate.py
persona: "owner-operator"         # see VALID_PERSONAS in scripts/validate.py
so_what: "One-sentence insight, max 160 chars"
summary: "2-3 sentence summary for SEO/description"
```

### What's Stubbed (code exists, not implemented) 🔧
| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/lib/digest.py` | Weekly digest pages | TODO stub |
| `scripts/lib/evergreen.py` | Update topic hubs | TODO stub |
| `scripts/lib/glossary.py` | Suggest glossary terms | TODO stub |
| `scripts/lib/social.py` | LinkedIn/X draft posts | TODO stub |

### What Doesn't Exist Yet ❌
- Originals content (`/content/originals/`) — section stub exists, 0 articles
- Guides content (`/content/guides/`) — section stub exists, 0 guides
- Glossary pages (`/content/glossary/`) — 0
- Weekly digest pages (`/content/digests/`) — 0
- Library pages (`/content/library/`) — 0
- Player pages for Cisco and FMP Alliance — 0 of 2 remaining
- Claims/evidence gate (`/data/claims/`) — empty
- Social drafts data (`/data/social/`) — empty

---

## Content Counts

| Content Type | Have | Need |
|-------------|------|------|
| Pulse items | 15 (12 legacy + 3 Phase 2) | ongoing daily |
| Player pages | 2 (VoltServer, Panduit) | 4 total (add Cisco, FMP Alliance) |
| Originals | 0 | ongoing |
| Guides | 0 | ongoing |
| Digests | 0 | weekly |
| Glossary terms | 0 | ongoing |
| Library items | 0 | ongoing |

**Pulse items by vertical (Phase 2 posts):**
- `edge-power-ups`: 1 (NEC 2026 Class 4 draft)
- `data-centers`: 1 (AI workloads & UPS)
- `building-electrification`: 1 (NYC LL97 heat pumps)

---

## Controlled Vocabularies

Run `python3 scripts/validate.py` to enforce. Source of truth: `scripts/validate.py`.

**Verticals (3):** `edge-power-ups`, `data-centers`, `building-electrification`

**Personas (7):** `owner-operator`, `facilities`, `it-network`, `security-integrator`, `ot-controls`, `gc-mep`, `electrical-contractor`

**Topics (18):** `safety-model`, `code-standards`, `pathways-install`, `estimating`, `schedule-value`, `monitoring-telemetry`, `ups-resilience`, `ot-controls-plc`, `physical-security`, `power-quality-surge`, `dc-distribution`, `commissioning`, `reliability-uptime`, `prefab-modular`, `labor-productivity`, `ai-infrastructure`, `incentives-policy`, `retrofits-mdus`

**Players (5):** `voltserver`, `panduit`, `cisco`, `fmp-alliance`, `other` (from `data/players.yaml`)

---

## Key File Paths

| File/Dir | Purpose |
|----------|---------|
| `hugo.toml` | Hugo config: base URL, taxonomies, nav, permalinks |
| `config/sources.yaml` | Player orgs: VoltServer, Panduit, Cisco, FMP Alliance |
| `config/queries.yaml` | SerpAPI search queries (5 queries, 10 results each, 21-day recency) |
| `.env` | API keys — ANTHROPIC_API_KEY, SERP_API_KEY |
| `scripts/run.py` | CLI entry point — all subcommands |
| `scripts/validate.py` | Front matter validator — run before committing content |
| `scripts/lib/intake.py` | SerpAPI fetch → `data/pulse/raw/` |
| `scripts/lib/extract.py` | Claude extraction → `data/pulse/extracted/` |
| `scripts/lib/normalize.py` | Dedupe + score → `data/pulse/items.json` |
| `scripts/lib/render_pulse.py` | Generate `content/pulse/*.md` |
| `scripts/lib/pr.py` | Opens GitHub PR via `gh` CLI |
| `data/pulse/items.json` | Master normalized Pulse item list |
| `data/players.yaml` | Canonical player registry |
| `layouts/index.html` | RCP homepage (3 columns + originals strip + main stream) |
| `layouts/partials/rcp_row.html` | Shared row renderer (date / title+sowhat / source) |
| `layouts/pulse/list.html` | Paginated /pulse/ list |
| `layouts/pulse/single.html` | Individual pulse item page |
| `layouts/_default/taxonomy.html` | Vertical/topic/persona hub pages |
| `layouts/_default/terms.html` | Taxonomy index pages |
| `assets/css/extended/rcp.css` | All RCP layout styles |
| `content/pulse/` | 15 published Pulse markdown files |
| `content/originals/` | Section stub only (_index.md) |
| `content/guides/` | Section stub only (_index.md) |
| `content/players/` | voltserver.md, panduit.md |
| `.github/workflows/daily_pulse.yml` | Daily GitHub Action (9 AM UTC) |
| `.github/workflows/weekly_digest.yml` | Weekly GitHub Action (Mon 10 AM UTC) |

---

## Run Commands

```bash
cd /Users/jameseaves/Documents/Python/Code/Automation/FMP_org/fmp-site

# Full daily pipeline (intake → extract → normalize → render)
python3 scripts/run.py daily

# Individual steps
python3 scripts/run.py intake
python3 scripts/run.py extract
python3 scripts/run.py normalize
python3 scripts/run.py render_pulse_pages

# Validate front matter before committing
python3 scripts/validate.py content/pulse/          # all pulse
python3 scripts/validate.py content/               # everything
python3 scripts/validate.py --strict content/      # fail on warnings too

# Weekly (digest + evergreen + glossary + social) — NOT YET IMPLEMENTED
python3 scripts/run.py weekly

# Open PR
python3 scripts/run.py open_pr

# Local Hugo preview
hugo server -D
```

---

## Estimated Monthly Cost

| Service | Cost |
|---------|------|
| Cloudflare Pages | $0 (free) |
| GitHub Actions | $0 (free) |
| SerpAPI | $0–$10 (free under 100 searches/month) |
| Anthropic Claude | ~$9/month |
| **Total** | **~$10–15/month** |

---

## Next Steps (in priority order)

1. **Update `render_pulse.py`** — make the daily pipeline write Phase 2 schema fields (`vertical`, `source_name`, `source_date`, `persona`, `so_what`) from extracted metadata so new auto-generated posts populate the 3 columns.
2. **Create first Original** — a synthesis article in `/content/originals/` to populate the originals strip on the homepage.
3. **Create first Guide** — an evergreen how-to in `/content/guides/` (e.g., "How to spec FMP for a heat pump retrofit") to populate vertical hub Start Here sections.
4. **Add Cisco and FMP Alliance player pages** — mirrors the existing VoltServer/Panduit structure in `content/players/`.
5. **Implement `digest.py`** — generate `/content/digests/{slug}.md` weekly summaries from top Pulse items.
6. **Implement `evergreen.py`** — auto-update topic hubs with latest relevant Pulse items.
7. **Implement `glossary.py`** — suggest and generate glossary term pages.
8. **Implement `social.py`** — LinkedIn/X draft generation per digest.

---

## Pending Decisions

| Decision | Status |
|----------|--------|
| Is the site currently live/deployed to Cloudflare? | **Yes — Phase 2 deployed 2026-02-26** |
| Is the GitHub Actions pipeline actively running? | Assumed yes (site is live) |
| Should `render_pulse.py` be updated to write Phase 2 fields, or keep manual? | To be decided with James |
| Should Originals/Guides be written manually or auto-generated? | To be decided |
