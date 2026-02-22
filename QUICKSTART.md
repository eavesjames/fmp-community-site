# Quick Start Guide

## Test the Automation Pipeline Locally

### 1. Set up environment

```bash
cd /Users/jameseaves/Documents/Python/Code/Automation/FMP_org/fmp-site

# Copy your API keys to .env
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
echo "SERP_API_KEY=your_serpapi_key" >> .env

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the full daily workflow

```bash
cd scripts
python3 run.py daily
```

This will:
1. **Intake**: Search for FMP content via SerpAPI
2. **Extract**: Use Claude to analyze each URL and extract metadata
3. **Normalize**: Dedupe items and calculate scores
4. **Render**: Generate markdown files at `/content/pulse/`

### 3. View generated content

```bash
# See what was created
ls -la ../content/pulse/

# Check the master items list
cat ../data/pulse/items.json | jq '.[0]'

# Preview the site
cd ..
hugo server
# Visit: http://localhost:1313
```

### 4. Expected output structure

```
data/pulse/
├── raw/
│   └── intake_20260222_150000.json       # Raw search results
├── extracted/
│   └── extracted_20260222_150500.json    # Claude-enriched metadata
└── items.json                             # Master normalized list

content/pulse/
├── 2026-02-22-voltserver-new-product.md
├── 2026-02-22-panduit-class-4-update.md
└── ...
```

### 5. Test individual steps

```bash
cd scripts

# Just fetch content (no Claude API calls)
python3 run.py intake

# Extract metadata from raw results
python3 run.py extract

# Normalize and dedupe
python3 run.py normalize

# Generate markdown files
python3 run.py render_pulse_pages
```

## Troubleshooting

### No search results
- **Issue**: SerpAPI returns empty results
- **Fix**: Check queries in `config/queries.yaml`, increase `recency_days`

### Claude extraction fails
- **Issue**: API errors or rate limits
- **Fix**: Check `ANTHROPIC_API_KEY`, add retries in `extract.py`

### Duplicate pages
- **Issue**: Same content appears multiple times
- **Fix**: Deduplication logic in `normalize.py` checks URL and title similarity

### Missing metadata
- **Issue**: Claude doesn't extract all fields
- **Fix**: Refine extraction prompt in `extract.py`, add validation

## Cost Estimates (Daily Run)

Assuming 10 search queries × 10 results = 100 URLs per day:

- **SerpAPI**: ~10 queries/day = 300/month (under free tier: 100 searches/month)
  - **Actual cost**: $0 if under free tier, or ~$5-10/month if over
- **Anthropic**: ~100 URLs × $0.003/URL = $0.30/day = ~$9/month
  - Uses Claude Sonnet 4.5, ~1K tokens per extraction

**Total**: ~$10-15/month for daily automation

## Next Steps

1. **Refine queries**: Edit `config/queries.yaml` based on results
2. **Test weekly workflow**: `python3 run.py weekly`
3. **Push to GitHub**: Follow `DEPLOY.md` to set up CI/CD
4. **Deploy to Cloudflare Pages**: See `DEPLOY.md` step 3

## Manual Testing Tips

### Test with small batch
Edit `config/queries.yaml`:
```yaml
settings:
  max_results_per_query: 2  # Reduce from 10
  recency_days: 7           # Last week only
```

### Inspect raw search results
```bash
cat data/pulse/raw/intake_*.json | jq '.[] | {title, link, player}'
```

### Check extraction quality
```bash
cat data/pulse/extracted/extracted_*.json | jq '.[] | {title, artifact_type, confidence, topics}'
```

### Verify deduplication
```bash
# Check for duplicate canonical_source
cat data/pulse/items.json | jq '.[].canonical_source' | sort | uniq -d
```

## Sample Workflow Output

```
$ python3 run.py daily

Running intake...
  Searching: VoltServer FMP updates
    Found 8 results
  Searching: Panduit Class 4 updates
    Found 5 results
Saved 13 results to data/pulse/raw/intake_20260222_150000.json

Running extract...
Processing: intake_20260222_150000.json
Found 13 items to extract
  [1/13] Extracting: VoltServer Announces New Digital...
    ✓ Confidence: high, Type: product
  [2/13] Extracting: Panduit Introduces Class 4...
    ✓ Confidence: high, Type: press
  ...
Saved 13 extracted items to data/pulse/extracted/extracted_20260222_150500.json

Running normalize...
Loaded 0 existing items, starting fresh
Processing: extracted_20260222_150500.json
  ✓ Added: VoltServer Announces New Digital Power... (score: 23)
  ✓ Added: Panduit Introduces Class 4 Distribution... (score: 18)
  Skipping low confidence: Cisco General Update...
Normalized: 11 added, 2 skipped
Total items in master list: 11

Rendering Pulse pages...
  ✓ Created: 2026-02-22-voltserver-new-digital-power.md
  ✓ Created: 2026-02-22-panduit-class-4-distribution.md
  ...
Rendered 11 new Pulse pages

Daily workflow complete!
```
