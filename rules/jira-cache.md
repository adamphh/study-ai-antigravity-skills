# Quy định Caching & Tối ưu Token cho Lệnh List Jira

1. **Kích hoạt tự động khi xem danh sách Jira**:
   Khi người dùng gõ lệnh `/list-jira`, `list jira`, `danh sách jira` hoặc xem danh sách Jira Issue ở đầu phiên chat:
   - Ưu tiên sử dụng kịch bản `.agent/scripts/manage_jira_cache.py` kiểm tra cache local (`~/.agent/cache/jira_open_issues.json`).
   - Nếu cache hợp lệ (TTL < 30 phút) và không có cờ `--refresh` hoặc yêu cầu làm mới từ người dùng: Đọc trực tiếp từ cache mà không gọi API MCP Jira Server.

2. **Tối ưu hóa trường dữ liệu (Field Filtering) khi fetch mới**:
   Khi cache hết hạn hoặc người dùng yêu cầu làm mới (`--refresh` / `force`):
   - Khi gọi MCP tool `jira_search_issues`, **BẮT BUỘC** truyền tham số `fields: ["summary", "status", "priority"]` để chỉ lấy 3 trường cần thiết, tuyệt đối không lấy toàn bộ payload JSON thô.
   - Sau khi fetch thành công, lưu lại vào `.agent/cache/jira_open_issues.json` qua `manage_jira_cache.py save`.

3. **Chuẩn hóa định dạng hiển thị**:
   Bảng danh sách Jira xuất ra phải có đủ các cột: **STT**, **Mã Issue (Key)**, **Priority (Độ ưu tiên)**, **Status (Trạng thái)**, và **Tiêu đề (Summary)**, sắp xếp ưu tiên giảm dần (Highest -> High -> Medium -> Low -> Lowest).
