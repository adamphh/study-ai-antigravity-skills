# Kế Hoạch Dọn Dẹp Và Đồng Bộ Hóa Global Skills

Kế hoạch này thực hiện việc loại bỏ thư mục cấu hình `.gemini/` thừa trong repository và đồng bộ hóa bộ kỹ năng mới từ `my-skills/` vào thư mục cấu hình toàn cục thật của hệ thống (`/home/bss/.gemini/config/skills/`).

## User Review Required

> [!IMPORTANT]
> - Sẽ xóa thư mục `.gemini/` trong dự án hiện hành để tránh gây trùng lặp cấu hình.
> - Sẽ cập nhật/sao chép đè nội dung kỹ năng mới từ `my-skills/` vào thư mục cấu hình toàn cục `/home/bss/.gemini/config/skills/`.

## Proposed Changes

---

### [Workspace Cleanups]

#### [DELETE] `.gemini/`
- Xóa thư mục `.gemini/` thừa nằm ở thư mục root của dự án `/mnt/projects/study-ai-antigravity-skills/`.

---

### [Global Synchronization]

#### [MODIFY] `/home/bss/.gemini/config/skills`
- Tạo liên kết động (symbolic link) từ `/mnt/projects/study-ai-antigravity-skills/my-skills` trỏ tới `/home/bss/.gemini/config/skills` để tự động cập nhật mọi thay đổi ở thư mục gốc.

---

## Verification Plan

### Automated Tests
- Chạy `git status` để kiểm tra việc xóa thư mục `.gemini/` trong repository.
- Kiểm tra danh sách các file trong `/home/bss/.gemini/config/skills/` sau khi đồng bộ.
