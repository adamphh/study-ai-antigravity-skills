# Kế Hoạch Cấu Hình Tự Động Chạy Jira Summary Khi Khởi Chạy CLI / IDE

Kế hoạch này thực hiện việc bổ sung quy chuẩn hành vi vào tệp quy tắc toàn cục `AGENTS.md` nhằm giúp AI tự động nhận diện lượt tương tác đầu tiên khi khởi chạy Antigravity CLI (`agy`) hoặc Antigravity IDE, từ đó tự động thực thi MCP tool Jira (`jira_get_my_open_issues`) và hiển thị bản tổng hợp ticket (Jira Summary) lên màn hình cho lập trình viên.

---

## User Review Required

> [!IMPORTANT]
> - Nguyên nhân: Trước đó trong tệp `AGENTS.md` chưa có quy tắc bắt buộc AI phải chạy Jira Summary khi bắt đầu phiên làm việc.
> - Sửa đổi: Cập nhật tệp [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md) tại mục **2. Planning, Workflow & Proactive Actions** để bổ sung quy định **"Tự động chạy Jira Summary khi khởi chạy (Auto Run Jira Summary on Startup)"**.
> - Tuân thủ: Hành động tự động này tuân thủ 100% quy định **MCP Jira Read-Only Mandate** (chỉ gọi các API đọc/tra cứu như `jira_get_my_open_issues`).

---

## Proposed Changes

### [Rules & Workflow]

#### [MODIFY] [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md)
- Bổ sung quy định tự động chạy Jira Summary vào mục **2. Planning, Workflow & Proactive Actions**:
  ```markdown
  - **Tự động chạy Jira Summary khi khởi chạy (Auto Run Jira Summary on Startup):** Tại lượt tương tác đầu tiên của mỗi phiên chat khi bắt đầu phiên làm việc trên CLI (`agy`) hoặc Antigravity IDE, AI BẮT BUỘC phải tự động gọi MCP tool Jira read-only (`jira_get_my_open_issues` hoặc `jira_search_issues_summary`) để lấy danh sách các ticket Jira đang mở được phân công cho người dùng, sau đó tổng hợp ngắn gọn (Mã ticket, Tiêu đề, Trạng thái, Ưu tiên) và hiển thị trực quan ra màn hình chat cho lập trình viên mà không cần đợi yêu cầu.
  ```

---

## Verification Plan

### Manual Verification
1. Kiểm tra file [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md) sau khi chỉnh sửa đảm bảo quy tắc rõ ràng, đúng format và vị trí.
2. Thử nghiệm chạy trực tiếp tool `jira_get_my_open_issues` hoặc `jira_search_issues_summary` để kiểm tra kết quả trả về từ Jira MCP server và xác minh format hiển thị Jira Summary.
