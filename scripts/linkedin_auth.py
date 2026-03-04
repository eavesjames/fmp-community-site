#!/usr/bin/env python3
"""
One-time LinkedIn OAuth flow to get an access token.

Usage:
    python3 scripts/linkedin_auth.py

Reads LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET from .env
Prints the access token to add to .env as LINKEDIN_ACCESS_TOKEN
"""
import json
import os
import ssl
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CLIENT_ID     = os.getenv("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI  = "http://localhost:8080/callback"
SCOPES        = ["w_member_social"]

_auth_code = None


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if "code" in params:
            _auth_code = params["code"][0]
            self.wfile.write(b"<h2>Authorization complete. You can close this tab.</h2>")
        elif "error" in params:
            error = params.get("error", ["unknown"])[0]
            desc  = params.get("error_description", ["no description"])[0]
            msg   = f"<h2>LinkedIn error: {error}</h2><p>{desc}</p><p>Full params: {dict(params)}</p>"
            self.wfile.write(msg.encode())
            print(f"\nLinkedIn returned error: {error} — {desc}")
            print(f"Full callback params: {dict(params)}")
        else:
            self.wfile.write(f"<h2>Unexpected callback</h2><p>Params: {dict(params)}</p>".encode())
            print(f"\nUnexpected callback params: {dict(params)}")

    def log_message(self, format, *args):
        pass  # suppress request logs


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in .env first.")
        sys.exit(1)

    # Build authorization URL
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id":     CLIENT_ID,
        "redirect_uri":  REDIRECT_URI,
        "scope":         " ".join(SCOPES),
        "state":         "fmp_auth",
    })
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{params}"

    # Start local server
    server = HTTPServer(("localhost", 8080), _CallbackHandler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.start()

    print(f"\nOpening LinkedIn authorization in your browser...")
    print(f"If it doesn't open automatically, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    server_thread.join(timeout=120)

    if not _auth_code:
        print("ERROR: No authorization code received within 2 minutes.")
        sys.exit(1)

    # Exchange code for token
    print("Exchanging authorization code for access token...")
    token_data = urllib.parse.urlencode({
        "grant_type":    "authorization_code",
        "code":          _auth_code,
        "redirect_uri":  REDIRECT_URI,
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode()

    req = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as resp:
        token_resp = json.loads(resp.read())

    access_token = token_resp.get("access_token")
    expires_in   = token_resp.get("expires_in", 0)

    if not access_token:
        print(f"ERROR: No access token in response: {token_resp}")
        sys.exit(1)

    print("\n✓ Success! Add this to your .env file:")
    print(f"\nLINKEDIN_ACCESS_TOKEN={access_token}")
    print(f"\nToken expires in {expires_in // 86400} days (~{expires_in // 2592000} months).")
    print("\nAlso ensure these are in .env:")
    print(f"  LINKEDIN_CLIENT_ID={CLIENT_ID}")
    print(f"  LINKEDIN_COMPANY_ID=111938931")


if __name__ == "__main__":
    main()
