---
name: adam-code-linter
description: Tự động chạy script Python kiểm tra định dạng chuẩn code (độ dài dòng <= 120 ký tự, thẻ XML khớp 100%, copyright header, strict_types, EOF single newline) trên git diff trong 0.2s. Sử dụng khi kết thúc code, trước khi commit hoặc khi gõ /adam-code-linter.
---

# Kỹ năng Kiểm Tra Chuẩn Định Dạng Code (/adam-code-linter)

Kỹ năng này cung cấp cơ chế kiểm tra định dạng và chuẩn mã nguồn hoàn toàn tự động, xác định (deterministic) thông qua script Python siêu nhẹ thay thế cho việc gọi Subagent, giúp tiết kiệm ~50.000 tokens mỗi lần rà soát.

---

## 🎯 Các Tiêu Chuẩn Được Kiểm Tra (Invariants)
1. **Độ dài dòng tối đa (Max Line Length $\le$ 120 ký tự)**:
   - Bao gồm cả khoảng trắng thụt lề (Indentation) ở đầu dòng.
   - Áp dụng cho: `.php`, `.js`, `.xml`, `.css`, `.less`, `.json`.
2. **Khớp thẻ XML 100% (XML Tag Matching)**:
   - Đảm bảo cú pháp XML hợp lệ, tất cả các thẻ mở đều có thẻ đóng khớp nhau, tránh lỗi nuốt thẻ khi sửa partial text.
3. **Khai báo Strict Types & Copyright Header (PHP)**:
   - Có `declare(strict_types=1);` sau comment Copyright Header.
   - Có khối `Copyright © Magestore`.
4. **Copyright Header trong XML**:
   - Kiểm tra header bản quyền trong các tệp XML cấu hình (`etc/*.xml`).
5. **Ký tự kết thúc tệp (EOF Newline)**:
   - Đảm bảo chính xác 1 dòng trống / newline ở cuối tệp, không để thừa nhiều dòng trống gây lỗi linter PHPCS.

---

## 🚀 Hướng Dẫn Kích Hoạt Tự Động Cho AI Agent

### 1. Thời điểm kích hoạt:
- **Tự động kích hoạt tại Bước 8** của quy trình làm task (ngay sau khi hoàn thành code và chạy test xong).
- Hoặc khi người dùng gõ lệnh `/adam-code-linter`.

### 2. Lệnh thực thi:
AI chạy lệnh terminal sau trên workspace của dự án hiện tại:

```bash
# Mặc định: Lint tất cả file đã thay đổi (staged & unstaged trong commit hiện tại, loại trừ untracked cũ)
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-code-linter/scripts/lint_diff.py

# Chỉ lint các file đã add vào staging area (Khuyên dùng trước khi commit):
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-code-linter/scripts/lint_diff.py --staged

# Chỉ định danh sách file cụ thể (nhanh nhất và sạch nhất):
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-code-linter/scripts/lint_diff.py path/to/file1.php path/to/file2.xml
```

### 3. Xử lý kết quả:
- **Nếu PASS (Exit code 0)**: AI tiếp tục quy trình chuyển sang Bước 9 (Review logic).
- **Nếu FAIL (Exit code 1)**: Script sẽ chỉ rõ chính xác tên file, số dòng và lỗi vi phạm. AI BẮT BUỘC sửa ngay các lỗi linter này trước khi tiếp tục.
