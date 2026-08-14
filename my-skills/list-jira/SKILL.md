---
name: list-jira
description: >-
  Lists open Jira issues assigned to current user with automatic caching and field optimization.
  Use when user types `/list-jira`, `list jira`, `my open issues`, or requests Jira task list.
---

# List Jira Issues Skill

This skill provides optimized listing of open Jira issues assigned to the current user using local caching (TTL 30 minutes) and minimal field querying to save tokens.

## Workflow

1. **Check Cache First**:
   - Run command: `python3 ~/.agent/scripts/manage_jira_cache.py check`
   - If output is `VALID` and user did not specify `--refresh` or `force`:
     - Run command: `python3 ~/.agent/scripts/manage_jira_cache.py read`
     - Display the output Markdown table directly to user.

2. **If Expired or Refresh Requested**:
   - Call `jira_search_issues` via `call_mcp_tool` with arguments:
     - `jql`: `"assignee = currentUser() AND statusCategory != Done ORDER BY priority DESC"`
     - `fields`: `["summary", "status", "priority"]`
     - `maxResults`: `50`
   - Pass the output JSON to `manage_jira_cache.py save` using pipe:
     `python3 ~/.agent/scripts/manage_jira_cache.py save`
   - Run `python3 ~/.agent/scripts/manage_jira_cache.py read` and display the formatted table.
