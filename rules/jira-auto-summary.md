# Rule: Global Auto Jira Summary on Session Start
trigger: session_start
always_on: true

Nội dung chỉ dẫn:
Tại lượt tương tác đầu tiên của mỗi phiên chat mới (bất kỳ dự án nào):
1. Tự động gọi Jira Read-only MCP Tool (`jira_get_my_open_issues`) để lấy danh sách các issue chưa hoàn thành của tài khoản người dùng (`adam@magestore.com`).
2. Hiển thị bảng tổng hợp danh sách công việc bao gồm: Mã Issue (Key), Tiêu đề (Summary), Trạng thái (Status), Độ ưu tiên (Priority), và Hạn chót (Due date).
