# Proactive Subagent Delegation & Context Management Rules

## 1. Proactive Subagent Delegation Rule
AI BẮT BUỘC phải chủ động tự động gọi Subagent (`invoke_subagent`) để xử lý ngầm mà KHÔNG cần đợi người dùng yêu cầu đối với các trường hợp sau:
- Tra cứu, đọc mã nguồn hoặc quét thông tin trên diện rộng (nhiều file/thư mục).
- Kiểm tra đối soát xung đột Plugin / Mixin / Rewrite giữa các extension.
- Nghiên cứu logic hệ thống phức tạp trước khi lập kế hoạch.
- **Bắt buộc Review Code & Kiểm toán Kiến trúc cuối Workflow (Code Review & Architecture Audit)**:
  Sau khi hoàn thành việc triển khai mã nguồn và chạy test cho bất kỳ task nào, AI BẮT BUỘC phải tự động gọi Subagent
  chuyên biệt (`Role: Code Reviewer & Architecture Auditor`) để:
  1. Rà soát toàn bộ diff/file mới, đánh giá các rủi ro tiềm ẩn (Memory Leak, Race Condition, Null Pointer Safety...).
  2. **Kiểm toán Bảo mật & Hiệu năng SQL (SQL Security & Query Performance Audit)**:
     - **Chống SQL Injection**: Tuyệt đối không nối chuỗi thô vào query; bắt buộc dùng bind variables (`quoteInto`,
       prepared statement, `Zend_Db_Select`).
     - **Hiệu năng Query & Tránh DB Lock**: Phát hiện và chặn lỗi N+1 query trong vòng lặp, query thiếu index, hoặc
       khối transaction dài gây khóa bảng (DB Deadlocks).
     - **Bảo mật Hệ thống (System Security)**: Kiểm tra phân quyền truy xuất theo Store/Location, tránh rò rỉ dữ liệu.
  3. **Kiểm toán Hệ thống & Kiến trúc (System & Architecture Audit)**: Đánh giá xem task vừa làm có phát sinh pattern
     mới đáng đóng gói thành Skill/Rule không, hoặc phát hiện quy tắc nào trong `user_rules` đang gây mâu thuẫn/nghẽn.
  4. Báo cáo kết quả và chỉ đưa ra khuyến nghị cải tiến khi thực sự có giá trị cao.

Sau khi Subagent hoàn thành, AI chính chỉ nhận kết quả tóm tắt tinh gọn để trả lời cho người dùng, giúp bảo vệ Context Window của phiên chính luôn sạch sẽ.

## 2. Context Threshold Warning Rule
AI phải chủ động theo dõi độ dài lịch sử cuộc hội thoại. Khi phát hiện phiên chat chính đã thực hiện nhiều bước (nhiều log/snippet lớn), AI BẮT BUỘC phải tự động đính kèm cảnh báo ở cuối câu trả lời:

`⚠️ Cảnh báo Context: Dung lượng hội thoại phiên này đã khá dài. Bạn nên bắt đầu một phiên chat mới hoặc giao việc cho Subagent để đảm bảo AI xử lý chính xác 100% quy tắc.`
