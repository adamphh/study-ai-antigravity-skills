#!/usr/bin/env python3
"""
adam-git-branch: Prepares and creates a clean git branch from origin/release.
Usage:
  python3 prepare_branch.py <TASK_KEY> <TASK_SUMMARY> [--bug|--feature]
"""

import sys
import re
import subprocess
import unicodedata

def slugify(text, max_len=30):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text[:max_len].rstrip('-')

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 prepare_branch.py <TASK_KEY> [TASK_SUMMARY] [--bug|--feature]")
        sys.exit(1)

    task_key = sys.argv[1].strip()
    is_bug = False
    args = sys.argv[2:]

    if "--bug" in args:
        is_bug = True
        args.remove("--bug")
    elif "--feature" in args:
        is_bug = False
        args.remove("--feature")

    summary_raw = " ".join(args).strip() if args else "task"
    summary_slug = slugify(summary_raw)
    branch_type = "fix" if is_bug or task_key.lower().startswith("bug") else "feature"
    branch_name = f"{branch_type}/{task_key}-{summary_slug}"

    print(f"🌿 Target Branch: {branch_name}")

    # Check git status
    code, out, _ = run_cmd("git status -s")
    if out:
        print(f"⚠️ Working tree is dirty. Please commit or stash changes before creating branch:\n{out}")
        sys.exit(1)

    # Fetch origin/release
    print("📡 Fetching origin/release...")
    code, _, err = run_cmd("git fetch origin release")
    if code != 0:
        print(f"⚠️ Warning: Could not fetch origin release: {err}")

    # Check if branch exists
    code, out, _ = run_cmd(f"git rev-parse --verify {branch_name}")
    if code == 0:
        print(f"🔄 Branch {branch_name} already exists. Checking out...")
        code, out, err = run_cmd(f"git checkout {branch_name}")
    else:
        print(f"✨ Creating and checking out new branch from origin/release...")
        code, out, err = run_cmd(f"git checkout -b {branch_name} origin/release")
        if code != 0:
            print("⚠️ Falling back to local release...")
            code, out, err = run_cmd(f"git checkout -b {branch_name} release")

    if code == 0:
        print(f"✅ Successfully checked out branch: {branch_name}")
        sys.exit(0)
    else:
        print(f"❌ Failed to checkout branch: {err}")
        sys.exit(code)

if __name__ == "__main__":
    main()
