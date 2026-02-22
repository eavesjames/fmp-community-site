# Deployment Guide

## Step 1: Create GitHub Repository

Go to https://github.com/new and create a new repository:
- **Name**: `fmp-community-site`
- **Description**: "Automation-first Hugo site for Fault Managed Power"
- **Visibility**: Public
- **Initialize**: DO NOT initialize (we already have code)

Then push your local code:

```bash
cd /Users/jameseaves/Documents/Python/Code/Automation/FMP_org/fmp-site
git remote add origin https://github.com/YOUR_USERNAME/fmp-community-site.git
git branch -M main
git push -u origin main
```

## Step 2: Configure GitHub Secrets

Go to: `Settings` → `Secrets and variables` → `Actions`

Add these secrets:
- `ANTHROPIC_API_KEY`: Your Claude API key
- `SERP_API_KEY`: Your SerpAPI key

## Step 3: Set up Cloudflare Pages

1. Go to https://dash.cloudflare.com/
2. Navigate to: **Pages** → **Create a project**
3. Connect Git: Select your GitHub account → Select `fmp-community-site`
4. Configure build:
   - **Framework preset**: Hugo
   - **Build command**: `hugo --minify`
   - **Build output directory**: `public`
   - **Root directory**: `/` (leave empty)
5. Environment variables:
   - `HUGO_VERSION` = `0.156.0`
6. Click: **Save and Deploy**

## Step 4: Connect Custom Domain

1. In Cloudflare Pages project: **Custom domains** → **Set up a custom domain**
2. Enter: `faultmanagedpower.org` and `www.faultmanagedpower.org`
3. DNS will auto-configure (domain is already in Cloudflare)
4. SSL certificate will be provisioned automatically

## Step 5: Test Automation

### Test daily workflow locally:
```bash
cd /Users/jameseaves/Documents/Python/Code/Automation/FMP_org/fmp-site
cp .env.example .env
# Edit .env with your API keys

pip install -r requirements.txt
cd scripts
python3 run.py daily
```

### Test weekly workflow locally:
```bash
cd scripts
python3 run.py weekly
```

### Trigger GitHub Actions manually:
1. Go to: **Actions** tab in GitHub
2. Select workflow: `Daily Pulse Update` or `Weekly Digest`
3. Click: **Run workflow**

## Step 6: Verify Deployment

Visit:
- Production: https://faultmanagedpower.org
- Check: Sitemap at /sitemap.xml
- Check: RSS at /index.xml
- Check: Player pages at /players/voltserver/

## Next Steps

1. **Test intake**: Run `python3 run.py intake` to fetch first batch of content
2. **Review sources**: Edit `config/sources.yaml` to refine search queries
3. **Monitor Actions**: GitHub Actions will run daily at 9 AM UTC
4. **Review PRs**: Agents will open PRs for you to review and merge

## Troubleshooting

### Hugo build fails
- Check `HUGO_VERSION` is set to `0.156.0` in Cloudflare Pages
- Verify Congo theme submodule is properly initialized

### GitHub Actions fail
- Check secrets are configured correctly
- Review workflow logs in Actions tab

### No search results
- Verify `SERP_API_KEY` is valid
- Check query syntax in `config/queries.yaml`
- Increase `recency_days` in queries.yaml settings

## Cost Estimates

- **Cloudflare Pages**: Free (unlimited bandwidth, 500 builds/month)
- **SerpAPI**: Free tier = 100 searches/month
- **Anthropic API**: ~$5-10/month (daily extraction + weekly digest)
- **Total**: ~$5-10/month

## Support

For issues or questions, see README.md or open an issue in the repository.
