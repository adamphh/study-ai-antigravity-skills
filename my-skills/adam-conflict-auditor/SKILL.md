---
name: adam-conflict-auditor
description: Tự động rà soát xem class PHP hoặc React Component mục tiêu đã có module nào khác đăng ký plugin/rewrite/mixin trước đó chưa (trong di.xml hoặc config.js). Sử dụng trước khi lập plan/code hoặc gõ /adam-conflict-auditor.
---

# Kỹ năng Rà Soát Xung Đột Extension (/adam-conflict-auditor)

Kỹ năng này quét tự động các file cấu hình `di.xml` (Backend) và `config.js` (WebPOS Frontend) để phát hiện xem class/component bạn định can thiệp đã có module nào khác plugin hay rewrite trước đó hay chưa, thay thế cho việc dùng `grep_search` lan man.

---

## 🚀 Hướng Dẫn Thực Thi

```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-conflict-auditor/scripts/audit_conflict.py --target-class "<CLASS_OR_COMPONENT_NAME>"
```

### Ví dụ:
- Backend:
  ```bash
  python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-conflict-auditor/scripts/audit_conflict.py --target-class "Magento\Sales\Model\Order"
  ```
- Frontend:
  ```bash
  python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-conflict-auditor/scripts/audit_conflict.py --target-class "PaymentService"
  ```

### Kết quả:
Trả về danh sách plugin/extension đang can thiệp trong 0.1s. Nếu không có xung đột, trả về `✅ NO CONFLICTS FOUND`.
