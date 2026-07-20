# Kế Hoạch Tích Hợp Cơ Chế Nhắc Nhở Chủ Động Vào AGENTS.md

Kế hoạch này thực hiện việc bổ sung quy chuẩn hành vi vào tệp quy tắc toàn cục `AGENTS.md` nhằm giúp AI tự động đánh giá độ phức tạp của task để đặt câu hỏi (thay cho `/grill-me`), tự động chạy test xác minh bắt buộc (gợi ý 3) và nhắc nhở đúc rút bài học (thay cho `/learn`).

## User Review Required

> [!IMPORTANT]
> Sẽ sửa đổi file [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md) để huấn luyện AI ba phản xạ chủ động và bắt buộc:
> 1. Tự động phỏng vấn làm rõ thiết kế (Proactive Planning Questions) đối với các task phức tạp.
> 2. **Bắt buộc tự động chạy test và xác minh (Mandatory Automated Verification):** Sau khi sinh code, AI phải tự chạy các lệnh test tự động liên quan và đính kèm kết quả vào `walkthrough.md` mà không cần lập trình viên yêu cầu.
> 3. Tự động đánh giá và gợi ý chạy lệnh `/learn` sau khi giải quyết xong các case khó.

## Proposed Changes

---

### [Rules]

#### [MODIFY] [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md)
- Bổ sung quy định về phỏng vấn kế hoạch chủ động, bắt buộc tự chạy test xác minh và gợi ý học hỏi vào phần `# Custom Rules` ở cuối file.

---

## Verification Plan

### Manual Verification
- Xác minh các quy tắc mới được cập nhật vào tệp [AGENTS.md](file:///mnt/projects/study-ai-antigravity-skills/AGENTS.md) chính xác và rõ ràng.

