"""Open GitHub PR"""
import subprocess

def open_pr(title, body=None):
    """Open a PR using gh CLI"""
    try:
        cmd = ["gh", "pr", "create", "--title", title]
        if body:
            cmd.extend(["--body", body])
        else:
            cmd.extend(["--body", "Automated content update"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"PR created: {result.stdout.strip()}")
        else:
            print(f"Error creating PR: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
