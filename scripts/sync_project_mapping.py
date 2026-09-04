#!/usr/bin/env python3
import os
import re
from pathlib import Path

PROJECTS_DIR = Path('/mnt/projects')
OUTPUT_RULE_FILE = Path('/mnt/projects/study-ai-antigravity-skills/rules/project-mapping.md')

def extract_project_code(dir_name):
    # Match patterns like P1115, p1062, PE4, POS, etc.
    match = re.match(r'^([pP]\d+|[a-zA-Z]+-?[pP]\d+|pos-[a-zA-Z0-9_-]+|PE4)', dir_name, re.IGNORECASE)
    if match:
        raw_code = match.group(1).upper()
        # Clean up p1062 -> P1062, etc.
        m_code = re.search(r'([P]\d+|PE4|POS)', raw_code)
        if m_code:
            return m_code.group(1)
        return raw_code
    return None

def main():
    if not PROJECTS_DIR.exists():
        print(f"Error: {PROJECTS_DIR} does not exist.")
        return

    entries = []
    for item in sorted(PROJECTS_DIR.iterdir(), key=lambda p: p.name.lower()):
        if item.is_dir() and not item.name.startswith('.'):
            dir_name = item.name
            proj_code = extract_project_code(dir_name)
            entries.append((proj_code or 'OTHER', str(item.resolve()), dir_name))

    # Sort entries by project code, placing P-codes first
    def sort_key(item):
        code = item[0]
        m = re.match(r'P(\d+)', code)
        if m:
            return (0, int(m.group(1)), item[1])
        if code in ('PE4', 'POS'):
            return (1, 0, item[1])
        return (2, 0, item[1])

    entries.sort(key=sort_key)

    lines = [
        "# Bảng Ánh Xạ Mã Dự Án Sang Thư Mục Dự Án (Project Root Mapping)",
        "",
        "## Quy định Bắt buộc (Mandatory Guardrail):",
        "1. **Tra cứu In-Memory 0 Lệnh Shell**: Khi người dùng yêu cầu bắt đầu task (ví dụ: `P1115-401`, `P1062-537`, `P1146-145`...), AI **BẮT BUỘC** tra cứu trực tiếp bảng ánh xạ dưới đây để lấy đường dẫn thư mục dự án.",
        "2. **Cwd Guardrail**: Thiết lập `Cwd: <Đường_dẫn_thư_mục>` cho toàn bộ các lệnh tool call tiếp theo. **TUYỆT ĐỐI KHÔNG** chạy bất kỳ lệnh `run_command` (git, find, ls...) tại `/home/bss`.",
        "",
        "| Mã Dự Án (Prefix) | Thư Mục Dự Án (Cwd) | Tên Thư Mục Gốc |",
        "|---|---|---|"
    ]

    for code, full_path, dir_name in entries:
        lines.append(f"| `{code}` | `{full_path}` | `{dir_name}` |")

    lines.append("")
    lines.append("> 💡 *Tệp này được tự động cập nhật bởi `~/.agent/scripts/sync_project_mapping.py` mỗi khi có dự án mới.*")
    lines.append("")

    OUTPUT_RULE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_RULE_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Successfully generated {OUTPUT_RULE_FILE} with {len(entries)} projects.")

if __name__ == '__main__':
    main()
