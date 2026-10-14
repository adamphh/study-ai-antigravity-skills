# Proactive Subagent Delegation & Context Management Rules

## 1. Proactive Subagent Delegation Rule
AI BẮT BUỘC phải chủ động tự động gọi Subagent (`invoke_subagent`) để xử lý ngầm mà KHÔNG cần đợi người dùng yêu cầu đối với các trường hợp sau:
- Tra cứu, đọc mã nguồn hoặc quét thông tin trên diện rộng (nhiều file/thư mục).
- Kiểm tra đối soát xung đột Plugin / Mixin / Rewrite giữa các extension.
- Nghiên cứu logic hệ thống phức tạp trước khi lập kế hoạch.
- **Review Code & Kiểm toán Kiến trúc cuối Workflow (Conditional Reviewer)**:
  Sau khi hoàn thành việc triển khai mã nguồn và chạy test:
  1. **Với Task Rủi Ro Cao (BẮT BUỘC gọi Subagent `Role: Code Reviewer & Architecture Auditor`)**:
     Áp dụng cho các thay đổi liên quan đến Payment, Stock/Inventory, Đồng bộ IndexedDB, Realtime Reindex, hoặc Core API Override. Subagent sẽ:
     - Rà soát toàn bộ diff/file mới, đánh giá các rủi ro tiềm ẩn (Memory Leak, Race Condition, Null Pointer Safety...).
     - **Kiểm toán Bảo mật & Hiệu năng SQL**: Chống SQL Injection, chặn lỗi N+1 query, tránh DB lock/deadlock.
     - **Kiểm toán Hệ thống & Kiến trúc**: Đánh giá pattern mới hoặc điểm nghẽn trong rule.
  2. **Với Task Thông Thường / Rủi Ro Thấp (TỐI ƯU TOKEN)**:
     UI/UX, CSS, đổi label, filter grid, validation form: Main Agent tự đối soát diff theo checklist chuẩn mà KHÔNG gọi Subagent, tiết kiệm ~50.000 tokens.

Sau khi Subagent hoàn thành (nếu có gọi), AI chính chỉ nhận kết quả tóm tắt tinh gọn để trả lời cho người dùng, giúp bảo vệ Context Window của phiên chính luôn sạch sẽ.

## 2. Context Threshold Warning Rule
AI phải chủ động theo dõi độ dài lịch sử cuộc hội thoại. Khi phát hiện phiên chat chính đã thực hiện nhiều bước (nhiều log/snippet lớn), AI BẮT BUỘC phải tự động đính kèm cảnh báo ở cuối câu trả lời:

`⚠️ Cảnh báo Context: Dung lượng hội thoại phiên này đã khá dài. Bạn nên bắt đầu một phiên chat mới hoặc giao việc cho Subagent để đảm bảo AI xử lý chính xác 100% quy tắc.`
