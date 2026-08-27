# Quy định Ưu tiên Định vị và Tìm kiếm Dự án / Workspace

## 1. Cơ chế Chặn cứng Trước khi Thực thi Lệnh (Pre-Execution CWD Guardrail)
- **Cấm Tuyệt đối Thực thi Shell tại `/home/bss`:**
  - AI **TUYỆT ĐỐI KHÔNG ĐƯỢC CHẠY BẤT KỲ LỆNH SHELL NÀO** (`run_command` như `git`, `find`, `npm`, `docker`, `ls`...) với `Cwd` là `/home/bss` hoặc bất kỳ thư mục con nào của `/home/*`.
  - Mọi thao tác bắt đầu task, kiểm tra git, chạy build hay test BẮT BUỘC phải thực hiện với `Cwd` nằm bên trong `/mnt/projects/<ma_du_an>-*`.

## 2. Phản xạ Bước 0: Tra cứu In-Memory từ Bảng Ánh Xạ Dự Án (Zero-Step Project Resolution)
- Ngay khi nhận được lệnh chứa mã Task/Issue (ví dụ `P1115-401`, `P1062-537`, `P1146-145`, `PE4-922`...):
  1. **Tra cứu In-Memory từ `project-mapping.md`**: Trích xuất tiền tố dự án (ví dụ `P1115`, `P1062`, `P1146`, `PE4`) và lấy đường dẫn thư mục dự án tương ứng trong file rule `~/.agent/rules/project-mapping.md` (ví dụ `P1115` -> `/mnt/projects/p1115-cremagarage-com-au`). **KHÔNG CHẠY LỆNH SHELL ĐỂ TÌM KIẾM.**
  2. **Thiết lập Cwd làm việc:** Gán ngay lập tức `Cwd: <Đường_dẫn_dự_án>` cho TOÀN BỘ các lệnh tool call tiếp theo trong suốt phiên làm việc.

## 3. Quy định về Phạm vi Quét Thư mục:
- Nghiêm cấm mọi hành vi `find` hoặc quét toàn bộ `/home/bss`.
- Trường hợp có dự án mới chưa có trong bảng ánh xạ: Sử dụng script `python3 ~/.agent/scripts/sync_project_mapping.py` để cập nhật lại bảng ánh xạ.
