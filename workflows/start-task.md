---
description: Khoi tao va bat dau task theo dung quy trinh 10 buoc (Tu dong chuyen project workspace, auto-init, auto-index, checkout branch, fetch Jira, tao plan)
---

# Slash Command: /start-task [MÃ_TASK]

Workflow khoi tao phien lam viec cho task moi theo dung quy chuan:

## Huong dan thuc thi cho Agent:

1. **Buoc 0: Dinh vi Du An, Chuyen Workspace & Kiem Tra Prompt**
   - **Kiem tra Prompt (Prompt Clarity Gate)**: Danh gia xem yeu cau cua nguoi dung da ro rang ve muc tieu va ket qua mong muon chua. Neu mo ho, dung lai hoi ngay lap tuc.
   - Trich xuat ma du an `{ma_du_an}` tu tham so task ID (vi du: `P1150-39` -> `P1150`).
   - Lay duong dan thu muc du an bang lenh:
     ```bash
     python3 /mnt/projects/study-ai-antigravity-skills/scripts/sync_project_mapping.py query {ma_du_an}
     ```
   - Dat `Cwd` truc tiep vao thu muc du an tra ve cho toan bo cac lenh tool call tiep theo.

2. **Buoc 1: Kiem Tra & Khoi Tao Moi Truong Du An (Hard Requirement: Auto-Init & Auto-Index)**
   - BẮT BUỘC kiem tra su ton tai cua symlink `.agent` va tep chi muc `docs/data-flows/INDEX.md` ngay lap tuc sau khi chuyen workspace.
   - Neu chua co hoac chua khoi tao, NGAY LẬP TỨC thuc thi:
     ```bash
     ln -sf /mnt/projects/study-ai-antigravity-skills/.agent .agent && /mnt/projects/study-ai-antigravity-skills/scripts/index-refresh
     ```
   - **Uu tien Indexer**: Tra cuu vi tri class/method qua index truoc, khong nap file lon vao context.

3. **Buoc 2: Chuan bi Git Branch (Auto-Skill: `adam-git-branch`)**
   - AI BẮT BUỘC goi script cua skill `adam-git-branch` trong 1 lenh shell duy nhat:
     ```bash
     python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-git-branch/scripts/prepare_branch.py {ma_du_an}-{ma_issue} "{noi_dung_tom_tat}" [--bug|--feature]
     ```

4. **Buoc 3: Doc Thong tin Task tu Jira & Chuyen Trang Thai**
   - Goi tool MCP `jira_get_issue` voi `issueIdOrKey: {MÃ_TASK}`.
   - Neu trang thai la `To Do` (hoac `Open`, `Backlog`): Tu dong chuyen sang `In Progress` qua `jira_transition_issue`.
   - Neu trang thai khac: Khong thay doi trang thai Jira.

5. **Buoc 4: Soi Xung Dot (Auto-Skill: `adam-conflict-auditor`) & Lap Ke Hoach (Auto-Skill: `adam-plan-scaffold`)**
   - **Kiem tra Xung dot Plugin/Rewrite**: Truoc khi code, chay:
     ```bash
     python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-conflict-auditor/scripts/audit_conflict.py --target-class "<CLASS_OR_COMPONENT_NAME>"
     ```
   - **Khoi tao Ke hoach chuan hoa**:
     ```bash
     python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-plan-scaffold/scripts/scaffold_plan.py {ma_du_an} {ma_issue} "{noi_dung_tom_tat_20_ki_tu}" [--bug|--feature]
     ```
   - Cap nhat noi dung nghiep vu vao file Plan vua sinh, tao artifact `implementation_plan.md` va cho nguoi dung phe duyet truoc khi code.

6. **Buoc 5: Quy Chuan Ket Thuc Task, Linter, Review & Toi Uu Token**
   - **Chay Linter Tu Dong (Auto-Skill: `adam-code-linter`)**: Bắt buộc chạy script kiểm tra (hỗ trợ cờ `--staged` hoặc truyền danh sách file cụ thể để đầu ra luôn gọn gàng, tránh quét file untracked cũ):
     ```bash
     python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-code-linter/scripts/lint_diff.py --staged
     # Hoặc chỉ định rõ file vừa sửa:
     # python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-code-linter/scripts/lint_diff.py path/to/file.php
     ```
     kiem tra 120 ky tu, XML match, EOF newline trong 0.2s. Neu fail phai sua ngay.
   - **Ra Soat Logic (Auto-Skill: `adam-code-review`)**: Main Agent tu doi soat theo Ma tran 6 tieu chi (SQL injection, N+1 query, constructor backward compatibility, null-pointer, extension attributes, in-function require).
   - **Quyet dinh Subagent**: Chi goi Subagent Review voi cac task rui ro cao (Payment, Stock, Sync, Core API).
   - Truoc khi tao `walkthrough.md`, nhac nguoi dung chay `/compact`.
   - Chi xuat **Khoi goi y lenh Git (Git Suggestion Block)** cho nguoi dung tu chay o terminal ngoai.
