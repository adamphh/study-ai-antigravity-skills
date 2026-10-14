#!/usr/bin/env python3
import sys
import json
import re
from pathlib import Path

SEARCH_DIRS = [
    Path('/mnt/projects'),
    Path('/var/www/magento249'),
    Path('/home/bss')
]

JSON_DATA_FILE = Path('/mnt/projects/study-ai-antigravity-skills/scripts/data/projects.json')

def extract_project_code(dir_name):
    match = re.match(r'^([pP]\d+|[a-zA-Z]+-?[pP]\d+|pos-[a-zA-Z0-9_-]+|PE4)', dir_name, re.IGNORECASE)
    if match:
        raw_code = match.group(1).upper()
        m_code = re.search(r'([P]\d+|PE4|POS)', raw_code)
        if m_code:
            return m_code.group(1)
        return raw_code
    return None

def sync():
    entries = {}
    seen_paths = set()

    for base_dir in SEARCH_DIRS:
        if not base_dir.exists():
            continue
        try:
            for item in sorted(base_dir.iterdir(), key=lambda p: p.name.lower()):
                if item.is_dir() and not item.name.startswith('.'):
                    full_path = str(item.resolve())
                    if full_path in seen_paths:
                        continue
                    seen_paths.add(full_path)
                    dir_name = item.name
                    proj_code = extract_project_code(dir_name)
                    if proj_code:
                        if proj_code not in entries:
                            entries[proj_code] = []
                        entries[proj_code].append({
                            "path": full_path,
                            "dir_name": dir_name
                        })
        except (PermissionError, OSError):
            continue

    JSON_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    total_projs = sum(len(v) for v in entries.values())
    print(f"✅ Successfully synced {total_projs} projects to {JSON_DATA_FILE}")

def query(project_code):
    if not JSON_DATA_FILE.exists():
        sync()

    code = project_code.strip().upper()
    m = re.match(r'([P]\d+|PE4|POS)', code)
    if m:
        code = m.group(1)

    try:
        with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        sync()
        with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

    if code in data and data[code]:
        # Return primary path (first matched)
        print(data[code][0]["path"])
        sys.exit(0)
    else:
        # Fallback: re-scan once
        sync()
        with open(JSON_DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if code in data and data[code]:
            print(data[code][0]["path"])
            sys.exit(0)

        print(f"NOT_FOUND: {project_code}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        if len(sys.argv) > 2:
            query(sys.argv[2])
        else:
            print("Usage: sync_project_mapping.py query <PROJECT_CODE>", file=sys.stderr)
            sys.exit(1)
    else:
        sync()
