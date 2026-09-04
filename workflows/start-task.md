---
description: Khoi tao va bat dau task theo dung quy trinh 10 buoc (Tu dong chuyen project workspace, checkout branch, fetch Jira, tao plan)
---

# Slash Command: /start-task [MÃ_TASK]

Workflow khoi tao phien lam viec cho task moi theo dung 10 buoc quy chuan:

## Huong dan thuc thi cho Agent:

1. **Buoc 0: Dinh vi Du An & Chuyen Workspace (In-Memory Lookup & Fallback Auto-Scan)**
   - Trich xuat ma du an `{ma_du_an}` tu tham so task ID (vi du: `P689-32` -> `P689`).
   - Tra cuu bang anh xa trong `/mnt/projects/study-ai-antigravity-skills/rules/project-mapping.md`:
     - **Neu tim thay**: Su dung ngay duong dan `/mnt/projects/<ma_du_an>-*` (0 lenh shell).
     - **Neu KHONG tim thay**: Tu dong chay lenh `python3 /mnt/projects/study-ai-antigravity-skills/scripts/sync_project_mapping.py` de quet lai thu muc `/mnt/projects/`, cap nhat lai `project-mapping.md` va lay duong dan moi nhat.
   - Dat `Cwd` truc tiep vao thu muc du an do cho toan bo cac lenh tool call tiep theo.


2. **Buoc 1: Chuan bi Git Branch**
   - Kiem tra git status trong thu muc du an.
   - Dam bao branch bat dau tu `origin/release`:
     ```bash
     git fetch origin release && git checkout -b {ma_du_an}-{ma_issue}-{noi_dung_tom_tat} origin/release
     ```

3. **Buoc 2: Doc Thong tin Task tu Jira**
   - Goi tool MCP `jira_get_issue` voi `issueIdOrKey: {MÃ_TASK}`.
   - Neu trang thai la `To Do` (hoac `Open`, `Backlog`): Tu dong chuyen sang `In Progress` qua `jira_transition_issue`.
   - Neu trang thai khac: Khong thay doi trang thai Jira.

4. **Buoc 3: Khoi tao Workspace Symlink & Data Flow Index**
   - Kiem tra `.agent` va `docs/data-flows/INDEX.md`. Neu chua co, chay:
     ```bash
     ln -sf /mnt/projects/study-ai-antigravity-skills/.agent .agent && /mnt/projects/study-ai-antigravity-skills/scripts/index-refresh
     ```

5. **Buoc 4: Lap Ke Hoach (Plan)**
   - Tao file ke hoach `Plans/{ma_du_an}-{ma_issue}-{noi_dung_tom_tat}.md` va artifact `implementation_plan.md`.
   - Bao cao ngan gon cho nguoi dung va cho duyet ke hoach truoc khi code.
