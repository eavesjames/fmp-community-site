#!/usr/bin/env python3
"""
FMP Community Site Automation Orchestrator
Handles: intake, extract, normalize, render_pulse_pages,
         insights, social_drafts, digest_weekly, evergreen_update,
         glossary_suggest, open_pr, open_daily_pr
"""

import argparse
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from lib.intake import run_intake
from lib.extract import run_extract
from lib.normalize import run_normalize
from lib.render_pulse import render_pulse_pages
from lib.insights import run_insights
from lib.social import generate_social_drafts
from lib.digest import generate_weekly_digest
from lib.evergreen import update_evergreen
from lib.glossary import suggest_glossary_terms
from lib.pr import open_pr, open_daily_pr


def main():
    parser = argparse.ArgumentParser(
        description="FMP Community Site Automation Orchestrator"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Daily pipeline stages
    subparsers.add_parser("intake",            help="Fetch new content from SerpAPI")
    subparsers.add_parser("extract",           help="Extract metadata via Claude")
    subparsers.add_parser("normalize",         help="Normalize and de-dupe items")
    subparsers.add_parser("render_pulse_pages", help="Generate Pulse markdown pages")
    subparsers.add_parser("insights",          help="Run Stage 3.5 multi-agent insights")
    subparsers.add_parser("social_drafts",     help="Run Stage 3.6 social draft generation")

    # Weekly workflow
    subparsers.add_parser("digest_weekly",     help="Generate weekly digest pages")
    subparsers.add_parser("evergreen_update",  help="Update evergreen topic pages")
    subparsers.add_parser("glossary_suggest",  help="Suggest new glossary terms")

    # PR commands
    pr_parser = subparsers.add_parser("open_pr", help="Open a GitHub PR")
    pr_parser.add_argument("--title", required=True, help="PR title")
    pr_parser.add_argument("--body", help="PR body text")

    subparsers.add_parser(
        "open_daily_pr",
        help="Open daily PR with rich auto-built body (reads today's artifacts)"
    )

    # Full workflows
    subparsers.add_parser("daily",  help="Run full daily pipeline")
    subparsers.add_parser("weekly", help="Run full weekly workflow")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "intake":
            run_intake()

        elif args.command == "extract":
            run_extract()

        elif args.command == "normalize":
            run_normalize()

        elif args.command == "render_pulse_pages":
            render_pulse_pages()

        elif args.command == "insights":
            run_insights()

        elif args.command == "social_drafts":
            generate_social_drafts()

        elif args.command == "digest_weekly":
            generate_weekly_digest()

        elif args.command == "evergreen_update":
            update_evergreen()

        elif args.command == "glossary_suggest":
            suggest_glossary_terms()

        elif args.command == "open_pr":
            open_pr(title=args.title, body=args.body)

        elif args.command == "open_daily_pr":
            open_daily_pr()

        elif args.command == "daily":
            print("Running daily workflow...")
            run_intake()
            run_extract()
            stats = run_normalize()
            render_pulse_pages()

            new_items = (stats or {}).get("new_items", [])
            if new_items:
                print(f"\nRunning insights + social for {len(new_items)} new item(s)...")
                run_insights(new_items)
                generate_social_drafts()
            else:
                print("\nNo new items — skipping insights and social drafts")

            print("\nDaily workflow complete.")
            print("  Artifacts in data/insights/ and data/social/")
            print("  Run: python3 run.py open_daily_pr   (or handled by CI)")

        elif args.command == "weekly":
            print("Running weekly workflow...")
            generate_weekly_digest()
            update_evergreen()
            suggest_glossary_terms()
            generate_social_drafts()
            print("Weekly workflow complete.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
