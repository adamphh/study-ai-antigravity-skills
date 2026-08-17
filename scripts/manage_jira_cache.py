#!/usr/bin/env python3
"""
Jira Cache Manager for Antigravity CLI.
Manages caching of Jira open issues, TTL checking, and Markdown table formatting.
"""

import json
import os
import sys
import time

CACHE_FILE = os.path.expanduser("~/.agent/cache/jira_open_issues.json")
DEFAULT_TTL = 10800  # 3 hours (180 minutes) in seconds

PRIORITY_ORDER = {
    "Highest": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
    "Lowest": 5
}


def ensure_cache_dir():
    """Ensure cache directory exists."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)


def is_cache_valid(ttl=DEFAULT_TTL):
    """Check if cache file exists and is still valid within TTL."""
    if not os.path.exists(CACHE_FILE):
        return False
    data = get_cached_data()
    if data and "updated_at" in data:
        return (time.time() - data["updated_at"]) < ttl
    mtime = os.path.getmtime(CACHE_FILE)
    return (time.time() - mtime) < ttl


def get_cached_data():
    """Read cached Jira issues from file."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_cache_data(issues):
    """Save issues list to cache file."""
    ensure_cache_dir()
    payload = {
        "updated_at": time.time(),
        "total": len(issues),
        "issues": issues
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def sort_issues(issues):
    """Sort issues by priority DESC (Highest -> High -> Medium -> Low -> Lowest)."""
    valid_issues = [item for item in issues if isinstance(item, dict)]
    return sorted(
        valid_issues,
        key=lambda x: PRIORITY_ORDER.get(x.get("priority") or "Lowest", 99)
    )


def format_markdown_table(issues, source_type="cache", updated_at=None):
    """Format issues into Markdown table with source note and refresh instructions."""
    sorted_list = sort_issues(issues)
    lines = [
        "| STT | Mã Issue (Key) | Priority (Độ ưu tiên) | Status (Trạng thái) | Tiêu đề (Summary) |",
        "|---|---|---|---|---|"
    ]
    for idx, item in enumerate(sorted_list, 1):
        if not isinstance(item, dict):
            continue
        key = item.get("key", "")
        priority = item.get("priority") or "N/A"
        status = item.get("status") or "N/A"
        raw_summary = item.get("summary") or ""
        summary = str(raw_summary).replace("|", "\\|")
        lines.append(f"| {idx} | **{key}** | {priority} | {status} | {summary} |")

    lines.append("")
    if source_type == "fresh":
        now_str = time.strftime("%H:%M:%S", time.localtime(time.time()))
        lines.append(
            f"> 🔄 **Nguồn dữ liệu:** Vừa **lấy mới** trực tiếp từ Jira API "
            f"(đã lưu cache lúc {now_str}, hiệu lực 3 tiếng)."
        )
    else:
        if updated_at:
            elapsed_sec = max(0, int(time.time() - updated_at))
            elapsed_min = elapsed_sec // 60
            remaining_min = max(0, (DEFAULT_TTL - elapsed_sec) // 60)
            cache_time = time.strftime("%H:%M:%S", time.localtime(updated_at))

            if elapsed_min < 1:
                time_ago_str = "vừa xong"
            else:
                time_ago_str = f"cách đây {elapsed_min} phút"

            remaining_str = (
                f"còn khoảng {remaining_min} phút"
                if remaining_min > 0
                else "đã hết hạn"
            )
            lines.append(
                f"> 📦 **Nguồn dữ liệu:** Lấy từ **Cache local** "
                f"(cập nhật lúc {cache_time} - {time_ago_str}, "
                f"hiệu lực 3 tiếng - {remaining_str})."
            )
        else:
            lines.append("> 📦 **Nguồn dữ liệu:** Lấy từ **Cache local** (hiệu lực 3 tiếng).")

        lines.append(
            "> 💡 *Để làm mới danh sách trực tiếp từ Jira, vui lòng chạy lệnh:* `/list-jira --refresh`"
        )

    return "\n".join(lines)


def parse_issue_item(item):
    """Parse single issue item handling both raw API fields and flattened dict."""
    if not isinstance(item, dict):
        return {}
    if "fields" not in item:
        return item

    fields = item.get("fields") or {}
    status_raw = fields.get("status") or "N/A"
    status_name = status_raw.get("name", "N/A") if isinstance(status_raw, dict) else str(status_raw)

    priority_raw = fields.get("priority") or "Lowest"
    priority_name = (
        priority_raw.get("name", "Lowest")
        if isinstance(priority_raw, dict)
        else str(priority_raw)
    )

    return {
        "key": item.get("key", ""),
        "summary": fields.get("summary") or "",
        "status": status_name,
        "priority": priority_name
    }


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "check":
        if is_cache_valid():
            print("VALID")
        else:
            print("EXPIRED")

    elif action == "read":
        source = "cache"
        if "--source" in sys.argv:
            idx = sys.argv.index("--source")
            if idx + 1 < len(sys.argv):
                source = sys.argv[idx + 1]
        elif "--fresh" in sys.argv or "fresh" in sys.argv:
            source = "fresh"

        data = get_cached_data()
        if data and "issues" in data:
            print(format_markdown_table(
                data["issues"],
                source_type=source,
                updated_at=data.get("updated_at")
            ))
        else:
            print("NO_CACHE")

    elif action == "save":
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print("ERROR: Empty input")
            sys.exit(0)

        try:
            parsed = json.loads(raw_input)
            if isinstance(parsed, list):
                raw_issues = parsed
            elif isinstance(parsed, dict):
                raw_issues = parsed.get("issues", [])
            else:
                raw_issues = []

            cleaned_issues = [
                parsed_item
                for item in raw_issues
                for parsed_item in [parse_issue_item(item)]
                if parsed_item and parsed_item.get("key")
            ]
            save_cache_data(cleaned_issues if cleaned_issues else raw_issues)
            print("SAVED")
        except Exception as e:
            print(f"ERROR: {e}")
