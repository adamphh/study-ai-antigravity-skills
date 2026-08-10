# Token & Performance Optimization Rules

Quy tắc tối ưu hóa Token và Hiệu năng làm việc dành cho AI Agent trong tất cả các dự án.

---

## 1. Line-Range File Viewing (Chỉ đọc File theo Khoảng Dòng)
- **Quy tắc**: Khi cần xem nội dung một file code dài (>100 dòng), AI **BẮT BUỘC** phải tra cứu vị trí dòng từ tệp `INDEX.md` hoặc `grep` khoanh vùng, sau đó gọi `view_file` với các tham số `StartLine` và `EndLine` cụ thể (ví dụ: khoảng 30-50 dòng xung quanh phương thức target).
- **Tuyệt đối không**: Nạp toàn bộ file 800-1000 dòng vào Context trừ khi phải đọc toàn bộ cấu trúc file.

---

## 2. Log Extraction Efficiency (Lọc Log Lỗi Ngắn Gọn)
- **Quy tắc**: Khi kiểm tra log lỗi/exception (`var/log/system.log`, `var/log/exception.log`), AI **KHÔNG ĐƯỢC** nạp cả tệp log béo.
- **Bắt buộc**: Sử dụng `tail -n 30` hoặc `grep -i -C 5 "exception\|error"` để chỉ trích xuất đúng 10-20 dòng Stack Trace chính.

---

## 3. Fast Local Syntax Check (Kiểm tra Cú pháp Cục bộ trước)
- **Quy tắc**: Sau khi sinh mới hoặc chỉnh sửa mã nguồn file PHP/JS, AI **BẮT BUỘC** chạy kiểm tra cú pháp cục bộ trên đúng 1 tệp vừa sửa trong 0.1s trước khi chạy toàn bộ test suite lớn:
  - PHP: `php -l path/to/file.php`
  - JS: `npx eslint path/to/file.js` hoặc kiểm tra syntax linter.

---

## 4. Task-Based Session Boundary (Phân định Ngữ cảnh theo Task)
- **Quy tắc**: Sau khi hoàn thành 1 Task, thực hiện `git commit` & `git push` và cập nhật tệp `walkthrough.md`, AI nên chủ động gợi ý người dùng khởi tạo Session mới cho Task tiếp theo để đảm bảo bộ nhớ hội thoại luôn sạch sẽ và tối ưu Token.
