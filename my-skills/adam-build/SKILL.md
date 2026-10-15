---
name: adam-build
description: Tự động biên dịch WebPOS client và nén build.tar chuẩn bị deploy chỉ trong 1 turn shell duy nhất không log bloat. Kích hoạt khi gõ /adam-build hoặc yêu cầu build client.
---

# Kỹ năng Biên Dịch & Đóng Gói WebPOS Client (/adam-build)

Kỹ năng này tự động hóa toàn bộ quy trình kiểm tra git, biên dịch React client (`npm run build`), và đóng gói `build.tar` chỉ trong **1 lệnh terminal duy nhất (1 turn)** với output sạch sẽ, loại bỏ hoàn toàn log bloat từ `tar -v` và tiết kiệm tới **90% token** so với quy trình cũ.

---

## 🚀 Hướng Dẫn Thực Thi Cho AI Agent

AI chạy script Python của skill trong workspace hiện tại (hoặc truyền `--path` tới thư mục dự án):

### 1. Build nhánh develop (Mặc định):
Mặc định script sẽ tự động checkout nhánh `develop` và pull mã nguồn mới nhất trước khi build:
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-build/scripts/build_pos.py
```

### 2. Build nhánh hiện tại (Dùng cờ `--keep-branch`):
Nếu muốn giữ nguyên và build trên nhánh hiện tại (không checkout sang `develop`):
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-build/scripts/build_pos.py --keep-branch
```

### 3. Build từ nhánh tùy chọn khác (Ví dụ `release` hoặc nhánh fix):
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-build/scripts/build_pos.py --branch release
```

### 4. Build ngay mã nguồn hiện tại không cần pull:
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-build/scripts/build_pos.py --keep-branch --no-pull
```

### 5. Tự động đăng ký extension mới trước khi build (`npm run upgrade`):
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-build/scripts/build_pos.py --upgrade
```

---

## 📊 Kết Quả Đầu Ra
Script tự động nén `build.tar` (chế độ im lặng không log chi tiết từng file) và in ra báo cáo ngắn gọn:
- Đường dẫn file `build.tar`
- Dung lượng file
- Thời gian biên dịch và đóng gói
- Thông báo sẵn sàng deploy lên môi trường dev/staging
