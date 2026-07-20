---
name: init-project
description: Khởi tạo cấu hình Antigravity cho dự án mới bằng cách liên kết thư mục .agent và sao chép docs/ mẫu. Dùng khi người dùng yêu cầu khởi tạo dự án, setup project hoặc chạy lệnh init.
---

# Kỹ năng Khởi tạo Dự án (Init Project)

Khi người dùng yêu cầu khởi tạo hoặc setup dự án mới, hãy thực hiện các bước sau để cấu hình môi trường phát triển:

## Quy trình thực hiện (Chạy tự động):

1. **Liên kết thư mục phím tắt (.agent):**
   Tạo liên kết động (symbolic link) từ thư mục gốc `/mnt/projects/study-ai-antigravity-skills/.agent` vào thư mục hiện hành:
   ```bash
   ln -s /mnt/projects/study-ai-antigravity-skills/.agent .agent
   ```
   *Lưu ý: Nếu thư mục `.agent` đã tồn tại ở local, bỏ qua bước này.*

2. **Sao chép thư mục tài liệu kiến trúc mẫu (docs):**
   Sao chép thư mục `docs/` template từ thư mục gốc `/mnt/projects/study-ai-antigravity-skills/docs` vào thư mục hiện hành:
   ```bash
   cp -r /mnt/projects/study-ai-antigravity-skills/docs docs
   ```
   *Lưu ý: Nếu thư mục `docs/` đã tồn tại, hãy kiểm tra xem các tệp `SYSTEM.md` và `INVARIANTS.md` đã có chưa; nếu chưa, hãy tạo hoặc bổ sung chúng.*

3. **Thông báo hoàn tất:**
   Báo cáo lại cho lập trình viên bằng tiếng Việt ngắn gọn. Hướng dẫn họ mở các file `docs/SYSTEM.md` và `docs/INVARIANTS.md` vừa được tạo ra ở local để điền hoặc cập nhật các thông tin, ràng buộc đặc thù của dự án đó.
