---
name: init-project
description: Khởi tạo cấu hình Antigravity cho máy mới và dự án mới bằng cách đấu nối Symlinks, Slash Commands và Script Indexer 2 tầng
---

# Antigravity Clean Machine Setup & Project Initialization Guide (`init-project`)

Tài liệu hướng dẫn 5 bước quy chuẩn để khôi phục 100% môi trường Antigravity (Symlinks, Rules, Skills, Native Slash Commands, Script Indexer) trên một máy tính mới hoặc sau khi cài lại HĐH.

---

## 💡 Quy tắc Quản lý Chỉ mục (Zero Manual Copying Invariant)

- **KHÔNG CẦN COPY THỦ CÔNG BẤT KỲ FILE CHỈ MỤC NÀO!**
- **Tầng 1 (Shared Core Index)**: Lưu cố định tại `/mnt/projects/study-ai-antigravity-skills/indexes/`. AI tự mở từ bất kỳ dự án nào thông qua liên kết hệ thống toàn cục.
- **Tầng 2 (Project Local Index)**: Tự động sinh ra tại `{project_root}/docs/data-flows/INDEX.md` khi gõ Slash Command `/index-refresh`.

---

## 📋 Quy trình 5 Bước Khôi phục Môi trường trên Máy Mới

### Bước 1: Clone Repository Kỹ năng dùng chung
```bash
cd /mnt/projects/
git clone <url-repo-study-ai-antigravity-skills> study-ai-antigravity-skills
```

### Bước 2: Thiết lập 4 Symlinks Hệ thống Toàn cục (Global Symlinks)
```bash
mkdir -p ~/.gemini/config/
ln -sf /mnt/projects/study-ai-antigravity-skills/AGENTS.md ~/.gemini/config/AGENTS.md
ln -sf /mnt/projects/study-ai-antigravity-skills/my-skills ~/.gemini/config/skills
ln -sf /mnt/projects/study-ai-antigravity-skills/rules ~/.gemini/config/rules
ln -sf /mnt/projects/study-ai-antigravity-skills/workflows ~/.gemini/config/workflows
```

### Bước 3: Đấu nối Dự án Mới (New Project Workspace Binding)
Tại thư mục gốc của dự án mới (ví dụ: `/mnt/projects/p1060-graceandmarbel.co.uk`):
```bash
cd /mnt/projects/p1060-graceandmarbel.co.uk
ln -sf /mnt/projects/study-ai-antigravity-skills/.agent .agent
```

### Bước 4: Tự động Lập Chỉ Mục 2 Tầng (Zero Manual Copying)
Vào Chat UI Antigravity của dự án mới và gõ Slash Command:
```text
/index-refresh
```
*Script sẽ tự động cập nhật Tầng 1 (Core dùng chung) và tự tạo Tầng 2 (`docs/data-flows/INDEX.md`) cho dự án hiện tại trong 1 giây.*

### Bước 5: Kiểm tra Native Slash Commands
Đảm bảo các lệnh `/index-refresh`, `/skills`, `/magento-dev`, `/webpos-dev` đã xuất hiện và sẵn sàng trong Chat UI.

---

## 🚀 Lệnh Nhanh Bằng Terminal (Option cho Bash)
Nếu muốn chạy trực tiếp bằng Terminal thay vì Slash Command:
```bash
/mnt/projects/study-ai-antigravity-skills/scripts/index-refresh          # Refresh cả 2 tầng
/mnt/projects/study-ai-antigravity-skills/scripts/index-refresh core     # Refresh Tầng 1
/mnt/projects/study-ai-antigravity-skills/scripts/index-refresh project  # Refresh Tầng 2
```
