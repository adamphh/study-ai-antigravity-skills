# Proactive Subagent Delegation & Context Management Rules

## 1. Proactive Subagent Delegation Rule
AI BẮT BUỘC phải chủ động tự động gọi Subagent (`invoke_subagent`) để xử lý ngầm mà KHÔNG cần đợi người dùng yêu cầu đối với các trường hợp sau:
- Tra cứu, đọc mã nguồn hoặc quét thông tin trên diện rộng (nhiều file/thư mục).
- Kiểm tra đối soát xung đột Plugin / Mixin / Rewrite giữa các extension.
- Nghiên cứu logic hệ thống phức tạp trước khi lập kế hoạch.

Sau khi Subagent hoàn thành, AI chính chỉ nhận kết quả tóm tắt tinh gọn để trả lời cho người dùng, giúp bảo vệ Context Window của phiên chính luôn sạch sẽ.

## 2. Context Threshold Warning Rule
AI phải chủ động theo dõi độ dài lịch sử cuộc hội thoại. Khi phát hiện phiên chat chính đã thực hiện nhiều bước (nhiều log/snippet lớn), AI BẮT BUỘC phải tự động đính kèm cảnh báo ở cuối câu trả lời:

`⚠️ Cảnh báo Context: Dung lượng hội thoại phiên này đã khá dài. Bạn nên bắt đầu một phiên chat mới hoặc giao việc cho Subagent để đảm bảo AI xử lý chính xác 100% quy tắc.`
