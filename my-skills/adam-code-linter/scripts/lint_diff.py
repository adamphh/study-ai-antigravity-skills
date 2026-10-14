#!/usr/bin/env python3
"""
adam-code-linter: Fast deterministic diff checker for Antigravity Workspace.
Checks:
1. Max line length <= 120 chars (including indentation).
2. XML matching tags (open/close) for changed XML files.
3. PHP Copyright header and declare(strict_types=1).
4. XML Copyright header.
5. Trailing newlines / Single newline at EOF.
"""

import sys
import os
import subprocess
import xml.etree.ElementTree as ET

MAX_LINE_LENGTH = 120

def get_git_diff_files():
    try:
        # Get files changed in working tree or staged against HEAD/release
        res = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, check=True
        )
        files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
        # Also check untracked files
        res_untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True
        )
        untracked = [f.strip() for f in res_untracked.stdout.splitlines() if f.strip()]
        all_files = sorted(list(set(files + untracked)))
        return all_files
    except Exception as e:
        print(f"Error running git diff: {e}")
        return []

def check_file(file_path):
    issues = []
    if not os.path.isfile(file_path):
        return issues

    # Skip non-source files or vendor/build dirs
    ignored_prefixes = ("vendor/", "node_modules/", "pub/static/", "var/", "generated/", ".git/")
    if any(file_path.startswith(prefix) for prefix in ignored_prefixes):
        return issues

    # Check line length and content
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return [f"Cannot read file: {e}"]

    # 1. Check EOF single newline
    if lines:
        if not lines[-1].endswith("\n"):
            issues.append("Missing newline at end of file (EOF).")
        elif len(lines) >= 2 and lines[-1] == "\n" and lines[-2].endswith("\n") and lines[-2].strip() == "":
            issues.append("Multiple blank lines detected at end of file (EOF). Expected exactly 1.")

    # 2. Check Line Length
    ext = os.path.splitext(file_path)[1].lower()
    for idx, line in enumerate(lines, 1):
        clean_line = line.rstrip("\r\n")
        # Ignore long lines in SVG, compiled or minified assets
        if len(clean_line) > MAX_LINE_LENGTH and ext in (".php", ".js", ".xml", ".css", ".less", ".json"):
            issues.append(f"Line {idx} exceeds {MAX_LINE_LENGTH} characters (length={len(clean_line)}): {clean_line[:60]}...")

    # 3. Check XML Tag Matching
    if ext == ".xml":
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            ET.fromstring(content)
        except ET.ParseError as pe:
            issues.append(f"XML Parse Error (Mismatched tags or malformed XML): {pe}")

    # 4. Check Headers for PHP
    if ext == ".php" and lines:
        content = "".join(lines[:25])
        if "Copyright © Magestore" not in content:
            issues.append("Missing Magestore Copyright header.")
        if "declare(strict_types=1);" not in content:
            issues.append("Missing 'declare(strict_types=1);' declaration.")

    # 5. Check Headers for XML
    if ext == ".xml" and lines:
        content = "".join(lines[:15])
        if "Copyright © Magestore" not in content and "etc/" in file_path:
            issues.append("Missing Magestore Copyright header in XML.")

    return issues

def main():
    target_files = sys.argv[1:] if len(sys.argv) > 1 else get_git_diff_files()
    if not target_files:
        print("✅ No modified files detected to lint.")
        sys.exit(0)

    total_issues = 0
    print(f"🔍 Running adam-code-linter on {len(target_files)} file(s)...\n")

    for f in target_files:
        file_issues = check_file(f)
        if file_issues:
            total_issues += len(file_issues)
            print(f"❌ {f}:")
            for issue in file_issues:
                print(f"   - {issue}")
            print()
        else:
            print(f"✅ {f}: PASS")

    print("-" * 50)
    if total_issues == 0:
        print("🎉 ALL FILES PASSED CODING STANDARDS LINTER!")
        sys.exit(0)
    else:
        print(f"⚠️ FOUND {total_issues} ISSUE(S). Please fix before completing task.")
        sys.exit(1)

if __name__ == "__main__":
    main()
