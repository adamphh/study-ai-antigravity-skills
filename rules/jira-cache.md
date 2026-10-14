# Quy định Caching & Tối ưu Token cho Lệnh List Jira

1. **Kích hoạt tự động khi xem danh sách Jira**:
   Khi người dùng gõ lệnh `/list-jira`, `list jira`, `danh sách jira` hoặc xem danh sách Jira Issue ở đầu phiên chat:
   - Ưu tiên sử dụng kịch bản `~/.agent/scripts/manage_jira_cache.py` kiểm tra cache local
     (`~/.agent/cache/jira_open_issues.json`).
   - Nếu cache hợp lệ (TTL < 3 tiếng / 180 phút) và không có cờ `--refresh`, `refresh` hoặc yêu cầu làm mới
     từ người dùng: Đọc trực tiếp từ cache qua `manage_jira_cache.py read --source cache` mà không gọi MCP Jira.

2. **Tối ưu hóa trường dữ liệu (Field Filtering) khi fetch mới**:
   Khi cache hết hạn hoặc người dùng yêu cầu làm mới (`--refresh` / `refresh` / `force`):
   - Khi gọi MCP tool `jira_search_issues`, **BẮT BUỘC** truyền tham số `fields: ["summary", "status", "priority"]`
     để chỉ lấy 3 trường cần thiết, tuyệt đối không lấy toàn bộ payload JSON thô.
   - Sau khi fetch thành công, lưu lại vào `~/.agent/cache/jira_open_issues.json` qua `manage_jira_cache.py save`.
   - Xuất dữ liệu qua `manage_jira_cache.py read --source fresh`.

3. **Chuẩn hóa định dạng hiển thị & Trạng thái Nguồn dữ liệu**:
   - Bảng danh sách Jira xuất ra bao gồm 4 cột (không có cột STT): **Mã Issue (Key)**,
     **Priority (Độ ưu tiên)**, **Status (Trạng thái)**, và **Tiêu đề (Summary)**, sắp xếp theo thứ tự ưu tiên giảm dần.
   - **Mặc định lọc Priority:** Mặc định chỉ hiển thị các issue có độ ưu tiên `Highest` và `High` để tối ưu token.
     Hỗ trợ cờ `--all` khi muốn hiển thị toàn bộ độ ưu tiên (bao gồm Medium, Low, Lowest).
   - **Khi lấy từ Cache:** BẮT BUỘC hiển thị dòng thông tin nguồn dữ liệu Cache local kèm thời gian cập nhật,
     thời gian còn hiệu lực và hướng dẫn lệnh làm mới:
     `💡 Để làm mới danh sách trực tiếp từ Jira, vui lòng chạy lệnh: /list-jira --refresh`.
   - **Khi lấy mới từ Jira:** BẮT BUỘC hiển thị dòng thông báo dữ liệu vừa được lấy mới trực tiếp từ Jira API.
