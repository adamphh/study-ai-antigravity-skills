# Kế Hoạch Cải Tiến File Cấu Hình Workflow Triển Khai POS

Kế hoạch này thực hiện việc cập nhật file cấu hình workflow `deploy_pos.md` nhằm loại bỏ mật khẩu SSH plaintext và chuyển đổi các đường dẫn cố định thành các placeholder động `{ProjectCode}` và `{ProjectName}`.

## User Review Required

> [!IMPORTANT]
> - Sẽ xóa bỏ hoàn toàn mật khẩu plaintext của server khỏi file cấu hình để đảm bảo an toàn thông tin.
> - Sẽ thiết lập cơ chế tự động phân tích ngữ cảnh dự án (Git branch & Workspace name) để AI tự sinh đường dẫn deploy chính xác.

## Proposed Changes

---

### [Workflows]

#### [MODIFY] [deploy_pos.md](file:///mnt/projects/study-ai-antigravity-skills/.agent/workflows/deploy_pos.md)
- Xóa các dòng chứa mật khẩu SSH plaintext.
- Đổi đường dẫn `/var/www/html/p1062-jw/envs/jw-sc-20240115/...` thành `/var/www/html/{ProjectCode}-{ProjectName}/envs/default/...`.
- Thêm phần "Quy tắc xử lý Context" hướng dẫn AI cách tự động phân tích Git branch và tên thư mục workspace để gán giá trị cho các biến `{ProjectCode}` và `{ProjectName}`.

---

## Verification Plan

### Manual Verification
- Kiểm tra lại cú pháp và các liên kết trong file `.agent/workflows/deploy_pos.md` mới.
- Kiểm tra tính chính xác của tài liệu hướng dẫn ngữ cảnh dành cho AI.
