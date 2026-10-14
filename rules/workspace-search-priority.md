# Quy định Ưu tiên Định vị và Tìm kiếm Dự án / Workspace

## 1. Cơ chế Chặn cứng Trước khi Thực thi Lệnh (Pre-Execution CWD Guardrail)
- **Cấm Tuyệt đối Thực thi Shell tại thư mục Home gốc `/home/bss`:**
  - AI **TUYỆT ĐỐI KHÔNG ĐƯỢC CHẠY CÁC LỆNH DỰ ÁN** (`git`, `npm`, `docker`, `ls`, `composer`...) với `Cwd` là `/home/bss` khi chưa trỏ vào đúng thư mục dự án.
  - Mọi thao tác bắt đầu task, kiểm tra git, chạy build hay test BẮT BUỘC phải thực hiện với `Cwd` nằm bên trong thư mục dự án tương ứng (tại `/mnt/projects/<ma_du_an>-*`, `/var/www/<ma_du_an>-*` hoặc `/home/bss/<ma_du_an>-*`).

## 2. Phản xạ Bước 0: Tra cứu In-Memory từ Bảng Ánh Xạ Dự Án (Zero-Step Project Resolution)
- Ngay khi nhận được lệnh chứa mã Task/Issue (ví dụ `P1115-401`, `P1062-537`, `P1146-145`, `PE4-922`...):
  1. **Tra cứu In-Memory từ `project-mapping.md`**: Trích xuất tiền tố dự án (ví dụ `P1115`, `P1062`, `P1146`, `PE4`) và lấy đường dẫn thư mục dự án tương ứng trong file rule `~/.agent/rules/project-mapping.md` (ví dụ `P1115` -> `/mnt/projects/p1115-cremagarage-com-au`). **KHÔNG CHẠY LỆNH SHELL ĐỂ TÌM KIẾM.**
  2. **Thiết lập Cwd làm việc:** Gán ngay lập tức `Cwd: <Đường_dẫn_dự_án>` cho TOÀN BỘ các lệnh tool call tiếp theo trong suốt phiên làm việc.

## 3. Quy định về Phạm vi Quét và Dò Tìm Thư mục Gốc:
- Khi dò tìm dự án mới chưa có trong bảng ánh xạ: Quét song song qua 3 thư mục gốc hợp lệ gồm: `/mnt/projects/`, `/var/www/`, `/home/bss/`.
- Tự động cập nhật bảng ánh xạ bằng lệnh: `python3 ~/.agent/scripts/sync_project_mapping.py`.

## 4. Quy định Nghiêm ngặt về Phạm vi Tìm kiếm (Search Scope Guardrail)
- **Tuyệt đối Không Quét Đệ quy Thư mục `/home/bss`**:
  - Mọi thao tác tìm kiếm mã nguồn hoặc tài liệu (`grep_search`, `find_by_name`, `list_dir`) BẮT BUỘC chỉ được thực thi
    bên trong Workspace dự án (ví dụ `/mnt/projects/<ma_du_an>-*`).
  - Khi cần đọc cấu hình Antigravity, MCP Schema hoặc Kỹ năng (Skills), AI BẮT BUỘC truy cập ĐÍCH DANH đường dẫn tệp
    cụ thể bên trong `/home/bss/.gemini/` (hoặc `~/.gemini/`), TUYỆT ĐỐI KHÔNG thực hiện quét/grep toàn bộ `/home/bss`.
