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
- **Quy tắc**: Sau khi hoàn thành 1 Task, hiển thị khối gợi ý lệnh Git và cập nhật tệp `walkthrough.md`, AI nên chủ động gợi ý người dùng khởi tạo Session mới cho Task tiếp theo để đảm bảo bộ nhớ hội thoại luôn sạch sẽ và tối ưu Token.

---

## 5. Prompt Clarity Gate (Bộ Lọc Kiểm Tra Độ Rõ Ràng Đầu Vào)
- **Quy tắc**: Trước khi thực hiện bất kỳ thao tác tra cứu mã nguồn hay sinh code nào, AI BẮT BUỘC phải đánh giá xem Prompt của người dùng đã đủ 3 yếu tố:
  1. Mục tiêu cụ thể (sửa lỗi gì, thêm tính năng gì, ở module nào)?
  2. Điều kiện đầu vào / mong muốn đầu ra rõ ràng?
  3. Vị trí nghi vấn hoặc ngữ cảnh tối thiểu (file, màn hình, mã issue)?
- **Xử lý khi mơ hồ**: TUYỆT ĐỐI KHÔNG tự phán đoán rồi đi quét toàn bộ codebase (gây tốn hàng chục nghìn tokens vô ích). AI phải lập tức dừng lại, dùng công cụ `ask_question` hoặc hỏi trực tiếp các câu hỏi ngắn gọn/trắc nghiệm để người dùng làm rõ.

---

## 6. Mandatory /compact Prompting before Large Documents
- **Quy tắc**: Vì lệnh `/compact` là lệnh UI chỉ người dùng mới có thể kích hoạt, nên TRƯỚC KHI bắt tay vào viết tài liệu dài (`walkthrough.md`) hoặc trước khi tổng kết đúc kết kiến thức (`/learn`), AI BẮT BUỘC phải dừng lại một nhịp và thông báo:
  `📌 Gợi ý tiết kiệm Token: Phiên làm việc đã trải qua nhiều bước. Bạn vui lòng gõ lệnh /compact trong khung chat để nén gọn bộ nhớ context trước khi tôi xuất bản tài liệu chi tiết.`

---

## 7. Git Suggestion Standard (Chỉ Gợi Ý Lệnh Git, Không Chạy Terminal)
- **Quy tắc**: Để tiết kiệm 100% token cho thao tác Git cuối phiên, AI TUYỆT ĐỐI KHÔNG tự chạy chuỗi lệnh `git commit` hay `git push` qua terminal. AI chỉ hiển thị khối lệnh Git chuẩn duy nhất để người dùng copy chạy trên máy của mình.
