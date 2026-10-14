# Study AI Antigravity Skills & Rules Repository
---

Repository lưu trữ toàn bộ Quy tắc (Rules), Kỹ năng (Skills) và Hướng dẫn Kiến trúc (AGENTS.md) dùng chung cho Antigravity AI Assistant.

---

## 🛠️ Hướng dẫn Khôi phục & Thiết lập khi cài lại Ubuntu / Máy mới

### Cách 1: Tự động hoàn toàn bằng 1 câu lệnh (Khuyên dùng)
```bash
cd /mnt/projects
git clone git@github.com:adamphh/study-ai-antigravity-skills.git study-ai-antigravity-skills
bash /mnt/projects/study-ai-antigravity-skills/scripts/setup-antigravity.sh
```
*Script sẽ tự động cài đặt dependency, thiết lập toàn bộ symlink cấp thư mục cho cả `~/.gemini/config` và `~/.agent`, phân quyền và tạo index Tầng 1.*

---

### Cách 2: Thiết lập thủ công (Manual Setup)

#### Bước 1: Clone Repository về máy
```bash
cd /mnt/projects
git clone git@github.com:adamphh/study-ai-antigravity-skills.git study-ai-antigravity-skills
```

#### Bước 2: Thiết lập Symlink cấp Thư mục cho `~/.gemini/config`
```bash
mkdir -p ~/.gemini/config
ln -sfn /mnt/projects/study-ai-antigravity-skills/AGENTS.md ~/.gemini/config/AGENTS.md
ln -sfn /mnt/projects/study-ai-antigravity-skills/rules ~/.gemini/config/rules
ln -sfn /mnt/projects/study-ai-antigravity-skills/my-skills ~/.gemini/config/skills
ln -sfn /mnt/projects/study-ai-antigravity-skills/workflows ~/.gemini/config/workflows
```

#### Bước 3: Thiết lập Symlink cấp Thư mục cho `~/.agent`
```bash
mkdir -p ~/.agent
ln -sfn /mnt/projects/study-ai-antigravity-skills/rules ~/.agent/rules
ln -sfn /mnt/projects/study-ai-antigravity-skills/my-skills ~/.agent/skills
ln -sfn /mnt/projects/study-ai-antigravity-skills/scripts ~/.agent/scripts
ln -sfn /mnt/projects/study-ai-antigravity-skills/workflows ~/.agent/workflows
```

#### Bước 4: Kiểm tra kết quả thiết lập
```bash
ls -la ~/.gemini/config ~/.agent
```
Kết quả hiển thị đúng dạng mũi tên trỏ sang `/mnt/projects/study-ai-antigravity-skills/...` là đã thành công. Từ nay, bất kỳ file rule hay skill nào thêm mới vào repo đều được tự động nhận diện 100%.

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