"""Phase 1: Send review digest email via Resend with direct GitHub links.

Environment variables required:
  RESEND_API_KEY       — Resend API key
  REVIEW_EMAIL_TO      — recipient address (defaults to james.eaves@voltserver.com)
  GITHUB_REPO          — owner/repo slug (e.g. jameseaves/fmp-site); used to build links
  GITHUB_BRANCH        — branch name for today's run (e.g. daily-generate-20260227)
"""
import json
import os
from datetime import datetime
from pathlib import Path

try:
    import requests as _requests
    _USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    _USE_REQUESTS = False

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

RESEND_API_URL = "https://api.resend.com/emails"
FROM_ADDRESS   = "FMP Bot <james@faultmanagedpower.org>"
DEFAULT_TO     = "james.eaves@voltserver.com"

FLAG_EMOJI = {
    "high_impact":     "🔥",
    "low_confidence":  "⚠️",
    "press_release":   "📰",
    "weak_evidence":   "🔍",
    "old_source":      "📅",
    "duplicate_risk":  "🔁",
}


def _github_url(repo: str, branch: str, path: str) -> str:
    """Build a GitHub blob URL for a file on a branch."""
    return f"https://github.com/{repo}/blob/{branch}/{path}"


def _build_html(
    today: str,
    candidates: list,
    approval_path: str,
    candidates_path: str,
    insight_registry: list,
    branch: str,
    repo: str,
) -> str:
    """Build the HTML body for the review email."""

    # ── Candidate rows ────────────────────────────────────────────────────────
    high_impact = [c for c in candidates if "high_impact" in c.get("flags", [])]
    other       = [c for c in candidates if "high_impact" not in c.get("flags", [])]
    ordered     = high_impact + other

    rows = ""
    for c in ordered:
        flags = c.get("flags", [])
        flag_icons = " ".join(FLAG_EMOJI.get(f, f) for f in flags)
        score = c.get("score", 0)
        title = c.get("title") or "(no title)"
        link  = c.get("link") or "#"
        cid   = c.get("candidate_id", "")
        rows += (
            f"<tr>"
            f"<td style='font-family:monospace;font-size:12px;color:#666'>{cid}</td>"
            f"<td>{flag_icons}</td>"
            f"<td style='text-align:right'>{score}</td>"
            f"<td><a href='{link}'>{title[:80]}</a></td>"
            f"</tr>\n"
        )

    # ── Insight draft links ───────────────────────────────────────────────────
    insight_rows = ""
    for entry in insight_registry:
        draft_path = entry.get("draft_path", "")
        gh_url = _github_url(repo, branch, draft_path) if repo and branch else "#"
        status = entry.get("status", "DRAFT")
        iid    = entry.get("insight_id", "")
        title  = entry.get("working_title", "")
        insight_rows += (
            f"<tr>"
            f"<td>{iid}</td>"
            f"<td><a href='{gh_url}'>{title}</a></td>"
            f"<td>{status}</td>"
            f"</tr>\n"
        )

    # ── Approval + candidates links ───────────────────────────────────────────
    approval_url   = _github_url(repo, branch, approval_path)   if repo and branch else "#"
    candidates_url = _github_url(repo, branch, candidates_path) if repo and branch else "#"

    flag_legend = " ".join(f"{v} {k.replace('_', ' ')}" for k, v in FLAG_EMOJI.items())

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:sans-serif;max-width:800px;margin:0 auto;padding:24px">

<h2>FMP Pulse Review — {today}</h2>
<p>{len(candidates)} candidate(s) ready for review.</p>

<h3>How to approve</h3>
<ol>
  <li>Open <a href="{approval_url}"><strong>approval.json</strong></a> on GitHub</li>
  <li>Click the pencil (Edit) icon</li>
  <li>Move candidate IDs from <code>pending_candidate_ids</code> to <code>approved_candidate_ids</code></li>
  <li>Commit directly to the branch: <code>{branch or 'daily-generate-…'}</code></li>
  <li>Run the <strong>daily_publish</strong> workflow (manual trigger in GitHub Actions)</li>
</ol>

<p>See all candidates: <a href="{candidates_url}">candidates.json</a></p>

<h3>Candidates ({len(candidates)})</h3>
<p style="font-size:12px;color:#666">{flag_legend}</p>
<table border="0" cellpadding="4" cellspacing="0" width="100%"
       style="border-collapse:collapse;font-size:13px">
  <tr style="background:#f0f0f0">
    <th align="left">ID</th>
    <th align="left">Flags</th>
    <th align="right">Score</th>
    <th align="left">Title</th>
  </tr>
  {rows}
</table>

{"<h3>Insight Drafts</h3><table border='0' cellpadding='4' cellspacing='0' width='100%' style='border-collapse:collapse;font-size:13px'><tr style='background:#f0f0f0'><th align='left'>ID</th><th align='left'>Title</th><th align='left'>Status</th></tr>" + insight_rows + "</table>" if insight_rows else ""}

<hr>
<p style="font-size:11px;color:#999">Generated by FMP Bot · {today}</p>
</body>
</html>"""
    return html


def send_review_email(
    candidates_result: dict | None = None,
    insights_result: dict | None = None,
    date: str | None = None,
    branch: str | None = None,
) -> bool:
    """
    Send the Phase 1 review digest email.

    candidates_result: return value from run_candidates()
    insights_result: return value from run_insights()
    branch: git branch name (e.g. 'daily-generate-20260227')

    Returns True on success, False on failure (non-fatal).
    """
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("  Warning: RESEND_API_KEY not set — skipping email")
        return False

    today  = date or datetime.now().strftime("%Y-%m-%d")
    repo   = os.getenv("GITHUB_REPO", "")
    branch = branch or os.getenv("GITHUB_BRANCH", f"daily-generate-{today.replace('-', '')}")
    to     = os.getenv("REVIEW_EMAIL_TO", DEFAULT_TO)

    # ── Gather data from result dicts or fall back to reading files ───────────
    candidates = []
    approval_path   = f"data/review/{today}_approval.json"
    candidates_path = f"data/review/{today}_candidates.json"
    insight_registry = []

    if candidates_result:
        candidates = candidates_result.get("candidates", [])
    else:
        cfile = PROJECT_ROOT / "data" / "review" / f"{today}_candidates.json"
        if cfile.exists():
            with open(cfile) as f:
                candidates = json.load(f)

    if insights_result:
        registry_path = insights_result.get("registry_file")
        if registry_path:
            try:
                with open(registry_path) as f:
                    insight_registry = json.load(f).get("insights", [])
            except Exception:
                pass
    else:
        rfile = PROJECT_ROOT / "data" / "review" / f"{today}_insights_registry.json"
        if rfile.exists():
            try:
                with open(rfile) as f:
                    insight_registry = json.load(f).get("insights", [])
            except Exception:
                pass

    # ── Build email ───────────────────────────────────────────────────────────
    html = _build_html(
        today=today,
        candidates=candidates,
        approval_path=approval_path,
        candidates_path=candidates_path,
        insight_registry=insight_registry,
        branch=branch,
        repo=repo,
    )

    n = len(candidates)
    subject = f"FMP Pulse Review — {today} ({n} candidate{'s' if n != 1 else ''})"

    payload_dict = {
        "from":    FROM_ADDRESS,
        "to":      [to],
        "subject": subject,
        "html":    html,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    }

    try:
        if _USE_REQUESTS:
            resp = _requests.post(RESEND_API_URL, json=payload_dict, headers=headers, timeout=15)
            if resp.ok:
                print(f"  Email sent to {to} (status {resp.status_code})")
                return True
            else:
                print(f"  Email failed: HTTP {resp.status_code} — {resp.text}", flush=True)
                return False
        else:
            data = json.dumps(payload_dict).encode()
            req = urllib.request.Request(RESEND_API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"  Email sent to {to} (status {resp.status})")
                return True
    except Exception as e:
        print(f"  Email failed: {e}")
        return False


if __name__ == "__main__":
    send_review_email()
