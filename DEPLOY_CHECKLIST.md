# FMP Community Site - Deployment Checklist

## ✅ Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `fmp-community-site` (Public)
3. Push code:
   ```bash
   git remote add origin https://github.com/eavesjames/fmp-community-site.git
   git push -u origin main
   ```

## ✅ Step 2: Configure GitHub Secrets

Go to: Settings → Secrets and variables → Actions

Add two secrets:
- `ANTHROPIC_API_KEY` (from your .env file)
- `SERP_API_KEY` (from your .env file)

## ✅ Step 3: Set Up Cloudflare Pages

1. Go to https://dash.cloudflare.com/ → Pages → Create project
2. Connect GitHub → Select `fmp-community-site`
3. Configure:
   - Framework: **Hugo**
   - Build command: `hugo --minify`
   - Output directory: `public`
   - Env variable: `HUGO_VERSION` = `0.156.0`
4. Click **Save and Deploy**

## ✅ Step 4: Connect Domain

1. Custom domains → Add `faultmanagedpower.org`
2. DNS auto-configures
3. SSL provisions automatically

## ✅ Step 5: Test

Visit:
- https://faultmanagedpower.org
- https://faultmanagedpower.org/pulse/

## 📊 Costs

- Cloudflare Pages: $0 (free)
- GitHub Actions: $0 (free)
- SerpAPI: $0 (under 100/month)
- Anthropic API: ~$10-15/month

## 🎯 Daily Automation

GitHub Actions runs at 9 AM UTC daily:
- Searches for FMP content
- Extracts metadata with Claude
- Generates Pulse pages
- Opens PR for review
- You merge → Auto-deploys

See README.md for full details.
