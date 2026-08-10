# Study AI Antigravity Skills & Rules Repository
---

Repository lưu trữ toàn bộ Quy tắc (Rules), Kỹ năng (Skills) và Hướng dẫn Kiến trúc (AGENTS.md) dùng chung cho Antigravity AI Assistant.

---

## 🛠️ Hướng dẫn Khôi phục & Thiết lập Symlink khi cài lại Ubuntu / Máy mới

Khi cài lại Ubuntu hoặc thiết lập trên máy làm việc mới, thực hiện các bước sau để liên kết bộ Quy tắc & Kỹ năng vào Antigravity CLI:

### Bước 1: Clone Repository về máy
```bash
cd /mnt/projects
git clone <URL_REPOSITORY_CỦA_BẠN> study-ai-antigravity-skills
```

### Bước 2: Tạo thư mục cấu hình Antigravity toàn cục
```bash
mkdir -p ~/.gemini/config
```

### Bước 3: Xóa các file/folder mặc định (nếu có)
```bash
rm -rf ~/.gemini/config/AGENTS.md ~/.gemini/config/rules ~/.gemini/config/skills
```

### Bước 4: Tạo các liên kết mềm (Symlink)
Thực hiện chạy 3 câu lệnh `ln -s` sau:
```bash
# 1. Link file hướng dẫn kiến trúc chung AGENTS.md
ln -s /mnt/projects/study-ai-antigravity-skills/AGENTS.md ~/.gemini/config/AGENTS.md

# 2. Link thư mục chứa tất cả Quy tắc (Rules)
ln -s /mnt/projects/study-ai-antigravity-skills/rules ~/.gemini/config/rules

# 3. Link thư mục chứa tất cả Kỹ năng (Skills)
ln -s /mnt/projects/study-ai-antigravity-skills/my-skills ~/.gemini/config/skills
```

*(Tùy chọn: Nếu muốn đồng bộ cấu hình MCP server)*:
```bash
ln -s /mnt/projects/study-ai-antigravity-skills/mcp_config.json ~/.gemini/config/mcp_config.json
```

### Bước 5: Kiểm tra kết quả thiết lập Symlink
```bash
ls -la ~/.gemini/config
```
Kết quả hiển thị đúng dạng mũi tên trỏ sang `/mnt/projects/study-ai-antigravity-skills/...` là đã thành công.

---

## 📁 Cấu trúc Thư mục

- `AGENTS.md` - Quy định chung và phím tắt AI
- `rules/` - Danh mục các quy tắc toàn cục (Git workflow, Magento 2, WebPOS extension rules, conflict check...)
- `my-skills/` - Danh mục các kỹ năng & cheatsheet (Mageworx, Tyro, Adyen, POS integration...)
- `docs/` - Tài liệu kiến trúc và hướng dẫn phát triển hệ thống
- `scripts/` - Các script tự động hóa hỗ trợ
- `Plans/` - Lưu trữ các bản kế hoạch mẫu

---

## 🚀 Cách sử dụng Skills & Commands
1. **Dùng Slash Commands trong chat**:
   - `/magento-dev` hoặc `/m2` - Phát triển Magento 2 Backend
   - `/react-dev` hoặc `/react` - Phát triển ReactJS Frontend
   - `/webpos-dev` hoặc `/pos` - Phát triển WebPOS Extension
   - `/skills` - Liệt kê danh sách kỹ năng khả dụng
   - `/learn` - Đề xuất ghi nhớ bài học / quy tắc mới vào hệ thống