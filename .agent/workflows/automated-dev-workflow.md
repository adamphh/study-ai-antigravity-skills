# Automated End-to-End Development Workflow & Quality Pipeline

## 1. Stage 1: Ticket Selection & Git Environment Setup
- Khi bắt đầu phiên làm việc hoặc chọn ticket: AI sử dụng `jira_get_my_open_issues` để hiển thị và gợi ý ticket.
- AI tự động checkout hoặc đề xuất lệnh checkout branch chuẩn: `{mã_dự_án}-{mã_issue}-{slug_task}` xuất phát từ nhánh **`release`**.
- AI tự động kiểm tra và nạp tài liệu `docs/data-flows/` và các quy tắc dự án liên quan.

## 2. Stage 2: Research & Planning with Subagent
- AI tự động triệu hồi Subagent `research` để điều tra nguyên nhân gốc rễ và sử dụng `grep_search` kiểm tra xung đột Mixin/Plugin/Rewrite trong `src/extension/`.
- Tạo tệp Plan: `Plans/{mã_dự_án}-{mã_issue}-{nội_dung_task_tom_tat_20_ki_tu}.md`.
- Tạo artifact `implementation_plan.md` với `RequestFeedback: true` và dừng chờ lập trình viên duyệt (`proceed`).

## 3. Stage 3: Coding Standards & Testability
- Mã PHP (Magento 2): Tuân thủ PSR-12, Magento Coding Standards, thêm Copyright Header, DocBlock có Description, cú pháp `::class`, độ dài dòng <= 120 ký tự, cấu trúc module `FixBug` / `Custom`.
- Mã JS (WebPOS Client): Tuân thủ ESLint (`import/no-anonymous-default-export`), nạp dependency bằng `require("...").default` trong thân hàm, độ dài dòng <= 120 ký tự, cấu trúc `src/extension/webpos-fix/`.
- Mã nguồn phải được thiết kế dạng module hóa, dễ dàng viết Unit Test (decoupled, dependency injection).

## 4. Stage 4: Automated Code Review Subagent & Testing
- **Bước 4.1 - Automated Code Review Subagent**:
  - Trước khi chạy test và commit, AI BẮT BUỘC triệu hồi Subagent `code-reviewer` để kiểm định độc lập:
    + **Hiệu năng (Performance)**: Phát hiện query SQL nặng, N+1 query, lặp query trong vòng lặp, memory leak, lặp array map thừa.
    + **Bảo mật (Security)**: Kiểm tra SQL Injection, XSS, unescaped output PHTML/HTML, CSRF, strict validation.
    + **Chuẩn mã nguồn**: Kiểm tra tuân thủ Magento 2 Standards & ESLint rules.
- **Bước 4.2 - Automated Testing & Clean Commit**:
  - Thiết kế và viết Unit Test tự động cho hàm/logic vừa sửa.
  - Thực thi test qua `run_command` (`CI=true npm test` hoặc `phpunit`).
  - Ghi nhật ký kết quả chạy test thực tế vào `walkthrough.md`.
  - Tự động dọn dẹp xóa các tệp Unit Test tạm thời (KHÔNG commit tệp test tạm).
  - Rà soát `git status` & `git diff`.
  - Kiểm tra `git log -n 5`: Sử dụng `git commit --amend` nếu trên branch đã có commit trước đó thuộc cùng task; nếu chưa có thì dùng `git commit -m "{Fix/Feat} [{mã_dự_án} - {mã_issue}]: {tóm_tắt_task}"`.

## 5. Stage 5: Push & GitLab Merge Request Automation
- Tự động thực thi `git push origin <current_branch>`.
- Tự động tạo Merge Request từ nhánh hiện tại vào nhánh **`develop`** trên GitLab (qua GitLab API hoặc CLI/URL).
- Báo cáo hoàn tất kèm link Merge Request cho lập trình viên.
