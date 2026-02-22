#!/usr/bin/env python3
"""
FMP Community Site Automation Orchestrator
Handles: intake, extract, normalize, render_pulse_pages, digest_weekly, 
evergreen_update, glossary_suggest, social_drafts, open_pr
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
from lib.digest import generate_weekly_digest
from lib.evergreen import update_evergreen
from lib.glossary import suggest_glossary_terms
from lib.social import generate_social_drafts
from lib.pr import open_pr

def main():
    parser = argparse.ArgumentParser(
        description="FMP Community Site Automation Orchestrator"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Daily workflow commands
    subparsers.add_parser("intake", help="Fetch new content from sources")
    subparsers.add_parser("extract", help="Extract metadata from fetched content")
    subparsers.add_parser("normalize", help="Normalize and de-dupe items")
    subparsers.add_parser("render_pulse_pages", help="Generate Pulse page markdown files")
    
    # Weekly workflow commands
    subparsers.add_parser("digest_weekly", help="Generate weekly digest")
    subparsers.add_parser("evergreen_update", help="Update evergreen topic pages")
    subparsers.add_parser("glossary_suggest", help="Suggest new glossary terms")
    subparsers.add_parser("social_drafts", help="Generate social media drafts")
    
    # PR management
    pr_parser = subparsers.add_parser("open_pr", help="Open GitHub PR with changes")
    pr_parser.add_argument("--title", required=True, help="PR title")
    pr_parser.add_argument("--body", help="PR body description")
    
    # Full workflows
    subparsers.add_parser("daily", help="Run full daily workflow")
    subparsers.add_parser("weekly", help="Run full weekly workflow")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    try:
        if args.command == "intake":
            run_intake()
        elif args.command == "extract":
            run_extract()
        elif args.command == "normalize":
            run_normalize()
        elif args.command == "render_pulse_pages":
            render_pulse_pages()
        elif args.command == "digest_weekly":
            generate_weekly_digest()
        elif args.command == "evergreen_update":
            update_evergreen()
        elif args.command == "glossary_suggest":
            suggest_glossary_terms()
        elif args.command == "social_drafts":
            generate_social_drafts()
        elif args.command == "open_pr":
            open_pr(title=args.title, body=args.body)
        elif args.command == "daily":
            print("Running daily workflow...")
            run_intake()
            run_extract()
            run_normalize()
            render_pulse_pages()
            print("Daily workflow complete. Review changes and run: python3 run.py open_pr --title 'Daily Pulse Update'")
        elif args.command == "weekly":
            print("Running weekly workflow...")
            generate_weekly_digest()
            update_evergreen()
            suggest_glossary_terms()
            generate_social_drafts()
            print("Weekly workflow complete. Review changes and run: python3 run.py open_pr --title 'Weekly Digest + Updates'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
