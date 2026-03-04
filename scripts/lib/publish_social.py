"""Publish approved LinkedIn social drafts via the LinkedIn Posts API.

Posts as the authenticated member (personal account). Each draft is posted
once and marked with posted_at to prevent double-posting.

Environment variables required:
  LINKEDIN_ACCESS_TOKEN  — OAuth token from linkedin_auth.py (expires ~60 days)
  LINKEDIN_COMPANY_ID    — Company Page ID (used in post commentary as a tag)

Usage:
  python3 scripts/run.py social_publish
  python3 scripts/lib/publish_social.py --date 2026-03-03 --dry-run
"""
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SOCIAL_DIR   = PROJECT_ROOT / "data" / "social"
POSTS_API    = "https://api.linkedin.com/v2/ugcPosts"
PROFILE_API  = "https://api.linkedin.com/v2/userinfo"


def _ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _get_member_urn(token: str) -> str:
    """Fetch the authenticated member's URN."""
    req = urllib.request.Request(
        PROFILE_API,
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, context=_ssl_ctx()) as resp:
        data = json.loads(resp.read())
    sub = data.get("sub")
    if not sub:
        raise ValueError(f"Could not get member URN from userinfo: {data}")
    return f"urn:li:person:{sub}"


def _post_to_linkedin(token: str, author_urn: str, text: str, link: str | None) -> dict:
    """Create a LinkedIn UGC post. Returns the API response dict."""
    share_content: dict = {
        "shareCommentary": {"text": text},
        "shareMediaCategory": "NONE",
    }

    if link:
        share_content["shareMediaCategory"] = "ARTICLE"
        share_content["media"] = [
            {
                "status": "READY",
                "originalUrl": link,
            }
        ]

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": share_content,
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        POSTS_API,
        data=data,
        headers={
            "Authorization":  f"Bearer {token}",
            "Content-Type":   "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, context=_ssl_ctx()) as resp:
        body = resp.read()
        post_id = resp.headers.get("x-restli-id", "")
    return {"post_id": post_id, "body": body.decode() if body else ""}


def publish_social_drafts(date: str | None = None, dry_run: bool = False) -> dict:
    """
    Read today's social drafts, post all unposted linkedin drafts.

    Returns dict with posted/skipped/failed counts.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    if not token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not set in .env")
        print("Run: python3 scripts/linkedin_auth.py")
        return {"posted": 0, "skipped": 0, "failed": 0}

    today = date or datetime.now().strftime("%Y-%m-%d")
    drafts_file = SOCIAL_DIR / f"{today}_social_drafts.json"

    if not drafts_file.exists():
        print(f"No social drafts found for {today} — run: python3 scripts/run.py generate")
        return {"posted": 0, "skipped": 0, "failed": 0}

    with open(drafts_file) as f:
        data = json.load(f)

    drafts = data.get("drafts", [])
    linkedin_drafts = [d for d in drafts if d.get("channel") == "linkedin"]

    if not linkedin_drafts:
        print(f"No LinkedIn drafts in {drafts_file.name}")
        return {"posted": 0, "skipped": 0, "failed": 0}

    print(f"Found {len(linkedin_drafts)} LinkedIn draft(s) for {today}")

    # Get member URN
    if not dry_run:
        try:
            author_urn = _get_member_urn(token)
            print(f"  Posting as: {author_urn}")
        except Exception as e:
            print(f"ERROR: Could not fetch member URN: {e}")
            print("Your token may have expired. Run: python3 scripts/linkedin_auth.py")
            return {"posted": 0, "skipped": 0, "failed": 0}

    posted = skipped = failed = 0

    for draft in linkedin_drafts:
        draft_id = draft.get("draft_id", "?")

        if draft.get("posted_at"):
            print(f"  {draft_id}: already posted at {draft['posted_at']} — skipping")
            skipped += 1
            continue

        text  = draft.get("text", "")
        links = draft.get("links", [])
        link  = links[0] if links else None

        if dry_run:
            print(f"\n  [DRY RUN] {draft_id}:")
            print(f"  Text ({len(text)} chars): {text[:120]}...")
            if link:
                print(f"  Link: {link}")
            posted += 1
            continue

        try:
            result = _post_to_linkedin(token, author_urn, text, link)
            draft["posted_at"] = datetime.now().isoformat()
            draft["linkedin_post_id"] = result.get("post_id", "")
            print(f"  {draft_id}: posted ✓ (id: {result.get('post_id', 'unknown')})")
            posted += 1
        except Exception as e:
            print(f"  {draft_id}: FAILED — {e}")
            failed += 1

    # Save updated drafts file with posted_at timestamps
    if not dry_run and posted > 0:
        with open(drafts_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nUpdated {drafts_file.name} with posted_at timestamps")

    print(f"\nDone: {posted} posted, {skipped} skipped, {failed} failed")
    return {"posted": posted, "skipped": skipped, "failed": failed}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date",    help="Override date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Print posts without publishing")
    args = parser.parse_args()
    publish_social_drafts(date=args.date, dry_run=args.dry_run)
