# User Workflow, Environment & Personal Goals Rules

## 1. Environment & Execution Setup
- **Project Root Location**: TẤT CẢ các dự án mã nguồn của lập trình viên đều nằm tại `/mnt/projects/` (ví dụ:
  `/mnt/projects/p1062-jw.com.au`, `/mnt/projects/p1115-cremagarage-com-au`, ...).
  - TUYỆT ĐỐI KHÔNG tìm kiếm, quét file hoặc chạy lệnh git trong `/home/bss`.
  - Khi bắt đầu bất kỳ task nào, AI BẮT BUỘC truy cập trực tiếp vào `/mnt/projects/<ma_du_an>-*`.
- **Frontend (WebPOS Client)**: Run directly using `npm` (`npm run upgrade`, `npm run test`...).
- **Backend (Magento 2 PHP)**: PHP is NOT installed on the host machine. All PHP/Magento CLI and PHP unit test
  commands MUST be run via Docker container (e.g. `docker exec ...`).

## 2. Task Initialization & Project Navigation Workflow
Whenever the user specifies a task ID to start working (e.g., `P1062-537`, `P1115-398` hoặc `bắt đầu issue ...`), AI
MUST strictly follow this sequence:

```mermaid
flowchart TD
    A["Lệnh: Bắt đầu làm task (Ví dụ: P1062-537)"] --> B["0. Conversation Check: Tra cứu/Resume hoặc Đặt tên phiên"]
    B --> C["1. Locate & Navigate: Chuyển Cwd sang /mnt/projects/p1062-*"]
    C --> D["2. Auto-Init Check: Kiểm tra .agent & docs (chạy init-project nếu thiếu)"]
    D --> E["3. Auto Read Data Flows: Đọc docs/data-flows/ (nếu có)"]
    E --> F["4. Fetch Jira Task: Tra cứu thông tin task trên Jira (jira_get_issue)"]
    F --> G["5. Codebase & Conflict Audit: Check Git branch, Allowed Scope & grep_search trùng lặp"]
    G --> H["6. Plan & Review: Hỏi làm rõ + Tạo tệp Plan + Self-Review + Trình duyệt"]
    H --> I["7. Execution & Testing: Triển khai Code + Test Docker/NPM + Dọn dẹp tệp test tạm"]
    I --> J["8. Walkthrough & Testing Verification: Viết Walkthrough + Check Git Diff"]
    J --> K["9. Subagent Code Review: Gọi Subagent rà soát toàn bộ file thay đổi & xuất báo cáo rủi ro"]
    K --> L["10. Git Commit & Proactive Learning: Format Commit + Gợi ý /learn"]
```

0. **Conversation History Lookup & Auto-Naming**:
   - **Tra cứu Conversation cũ (Auto-Resume Check)**: Kiểm tra danh sách Conversation History xem đã có phiên hội thoại
     nào trước đó liên quan đến mã task `{ma_du_an}-{ma_issue}` hay chưa.
     - Nếu ĐÃ CÓ: Lập tức hiển thị thông tin tóm tắt và dẫn link Markdown dạng `[Tên phiên](conversation://<id>)` để
       lập trình viên có thể click chuyển sang resume ngữ cảnh cũ ngay.
     - Nếu CHƯA CÓ (phiên mới): Tự động lấy tiêu đề Jira Task (`jira_get_issue`) để định danh/đặt tên hiển thị cho phiên
       làm việc theo chuẩn `[{ma_du_an}-{ma_issue}] {Tiêu đề Jira Task}` giúp dễ dàng quản lý và trace lại sau này.
1. **Locate & Navigate to Project Directory**:
   - Extract project code (e.g. `P1062`, `P1115`) from task ID.
   - Truy cập trực tiếp vào thư mục tương ứng trong `/mnt/projects/<ma_du_an>-*`
     (ví dụ `/mnt/projects/p1062-jw.com.au`).
   - Đặt Cwd cho tất cả các thao tác file/terminal vào thư mục dự án đó.
   - Nghiêm cấm mọi hành vi `find` hoặc quét thư mục dưới `/home/bss`.
2. **Auto-Init Check & Execution**:
   - Check if `.agent` and `docs` directories exist in the target project folder.
   - If missing, automatically execute skill `init-project` to generate symlinks and templates.
3. **Auto Read Data Flows**:
   - Check if `docs/data-flows/` exists. If present, read `README.md` and related data flow specs.
4. **Fetch & Analyze Jira Task**:
   - Query Jira MCP (`jira_get_issue`) using task ID to read summary, description, comments, and criteria.
5. **Git Branch, Codebase & Plugin Conflict Audit**:
   - Check current git branch.
   - Inspect codebase strictly adhering to Allowed Scope: `app/code/Magestore/*Bug*`, `app/code/Magestore/*Fix*`,
     `app/code/Magestore/*Custom*`, `client/pos/src/extension/*fix*`, `client/pos/src/extension/*bug*`,
     `client/pos/src/extension/*custom*`.
   - Run `grep_search` to audit for existing plugin/rewrite conflicts before planning.
6. **Plan Creation, Self-Review & User Approval**:
   - Ask proactive clarifying questions if anything is ambiguous.
   - Create plan file: `Plans/{ma_du_an}-{ma_issue}-{noi_dung_task_tom_tat_20_ki_tu}.md` and `implementation_plan.md`.
   - Audit own plan (Allowed scope, line length <= 120, copyright headers, plugin conflicts).
   - Present plan for user review & approval before writing any code.
7. **Execution, Automated Testing & Test Cleanup**:
   - Implement extension/plugin code upon user approval.
   - Run automated tests (`npm` for JS, `docker exec` for PHP).
   - Clean up all temporary test files before proceeding to git status/commit.
8. **Walkthrough & Testing Verification**:
   - Write execution summary & test evidence to `walkthrough.md`.
   - Review `git status` and `git diff`.
9. **Subagent Code Review & Risk Analysis (Mandatory Final Review Step)**:
   - Sau khi hoàn thành triển khai mã nguồn và kiểm thử ở bước 7 & 8, AI BẮT BUỘC phải gọi một Subagent chuyên biệt
     (Role: `Code Reviewer & Risk Analyst`) để rà soát toàn bộ các tệp vừa chỉnh sửa / tạo mới.
   - Subagent phải kiểm tra và đánh giá chi tiết các rủi ro tiềm ẩn: Memory Leak, Async Race Condition,
     Null Pointer Safety, Unhandled Edge Cases, DOM Manipulation Errors,...
   - Trình bày Báo cáo Code Review chi tiết cho lập trình viên và tiến hành khắc phục hoàn thiện mã nguồn trước
     khi commit.
10. **Git Commit Standards & Proactive Learning**:
    - Format commit: `{Fix/Feat} [{mã dự án} - {issue id}]: {ticket ID/summary}`.
    - Proactively suggest `/learn` if task involved complex bug fixes or reusable patterns.

## 3. Communication & Clarification Mandate
- **Strict Clarification Rule**: Always ask the user directly for clarification whenever a requirement, design
  detail, error log, or task description is ambiguous, missing, or unclear. Never make blind assumptions or patch
  symptoms silently.

## 4. Automation & Code Optimization Objectives
- **Phase 1 (Time & Workflow Optimization)**: Maximize automation in daily tasks (auto-tracing, proactive subagents,
  docker/npm testing, self-review, handover notes).
- **Phase 2 (WebPOS Codebase Audit & Performance Optimization)**: Proactively observe and audit WebPOS
  client/backend code during tasks to identify bottlenecks, race conditions, offline IndexedDB sync issues, or
  anti-patterns, and propose refactoring/optimization recommendations.
