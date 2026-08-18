---
name: list-jira
description: >-
  Lists open Jira issues assigned to current user with automatic caching and field optimization.
  Use when user types `/list-jira`, `list jira`, `my open issues`, or requests Jira task list.
---

# List Jira Issues Skill

This skill provides optimized listing of open Jira issues assigned to the current user using
local caching (TTL 3 hours / 180 minutes) and minimal field querying to save tokens.

## Workflow

1. **Check Cache First**:
   - Run command: `python3 ~/.agent/scripts/manage_jira_cache.py check`
   - If output is `VALID` and user did not specify `--refresh`, `refresh`, or `force`:
     - Determine if user requested `--all` / `all`.
     - Run command: `python3 ~/.agent/scripts/manage_jira_cache.py read --source cache` (append `--all` if requested).
     - Display the output Markdown table (4 columns: Key, Priority, Status, Summary) and footer notes.

2. **If Expired or Refresh Requested (`--refresh` / `refresh` / `force`)**:
   - Call `jira_search_issues` via `call_mcp_tool` with arguments:
     - `jql`: `"assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC"`
     - `fields`: `["summary", "status", "priority"]`
     - `maxResults`: `50`
   - Pass the output JSON string from `jira_search_issues` to `manage_jira_cache.py save` via stdin:
     `echo '<json_output>' | python3 ~/.agent/scripts/manage_jira_cache.py save`
   - Determine if user requested `--all` / `all`.
   - Run `python3 ~/.agent/scripts/manage_jira_cache.py read --source fresh` (append `--all` if requested)
     and display the formatted table and footer notes directly to user.

## Display Format Standards
- **4 Columns:** `Mã Issue (Key)`, `Priority (Độ ưu tiên)`, `Status (Trạng thái)`, `Tiêu đề (Summary)`.
- **Default Filter:** Only shows `Highest` and `High` priority issues to save tokens.
- **Flags:**
  - `--all`: Display all priority levels (Highest -> Lowest).
  - `--refresh`: Force fresh fetch from Jira API.
