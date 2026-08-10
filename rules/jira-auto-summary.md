# Rule: Global Auto Jira Summary on Session Start
trigger: session_start
always_on: true

Nội dung chỉ dẫn:
Tại lượt tương tác đầu tiên của mỗi phiên chat mới hoặc khi người dùng yêu cầu liệt kê danh sách Jira:
1. Tự động gọi Jira Read-only MCP Tool (`jira_search_issues` hoặc `jira_get_my_open_issues`) lấy danh sách issue kèm các thông tin field: `summary`, `status`, `priority`, `updated`.
2. Hiển thị bảng Markdown đầy đủ các cột: **STT**, **Mã Issue (Key)**, **Priority (Độ ưu tiên)**, **Status (Trạng thái)**, và **Tiêu đề (Summary)**.
3. Sắp xếp danh sách theo độ ưu tiên giảm dần (**Priority DESC**: Highest -> High -> Medium -> Low -> Lowest).

