# 🧠 Bộ Não Thứ 2 (Knowledge Base & Business Logic Index)

Chào mừng bạn đến với **Knowledge Base** - Hệ thống lưu trữ bài học nghiệp vụ, luồng dữ liệu (Data Flows) và các trường hợp biên (Edge Cases) sâu của hệ thống **Magestore WebPOS & Magento 2**.

---

## 🗺️ Bảng Tra Cứu Bài Học Nghiệp Vụ (Knowledge Index)

<!-- KB_INDEX_START -->
| Mã ID | Tiêu đề Bài học (Title) | Domain | Phạm vi nghiệp vụ tóm tắt | Ngày cập nhật |
| :--- | :--- | :--- | :--- | :--- |
| [KB-CHK-001](file:///mnt/projects/study-ai-antigravity-skills/docs/knowledge-base/checkout-payment/creditmemo-order-state-machine-cache.md) | **Xử lý Hoàn tiền Đơn hàng (Creditmemo), Trạng thái Order State Machine và Tránh Stale RAM Cache trong Magento 2** | `checkout-payment` | Xử lý Order State (Closed/Complete), tính QtyToShip khi hoàn tiền và tránh Stale Entity Cache trong Magento 2 OrderRepository | 2026-10-08 |
| [KB-OPT-001](file:///mnt/projects/study-ai-antigravity-skills/docs/knowledge-base/agent-optimization/token-and-cost-optimization-architecture.md) | **Nghệ Thuật Tối Ưu Hóa Chi Phí Token & Hiệu Năng Cho AI Agent (Antigravity Architecture)** | `agent-optimization` | Cắt giảm 50-70% token bằng Prompt Clarity Gate, di dời bảng mapping sang JSON, dùng Skill linter 0.2s thay Subagent và Git Suggestion Block | 2026-10-14 |
<!-- KB_INDEX_END -->

---

## 💡 Hướng dẫn Đóng góp Tri thức (/save-kb)
Khi gặp một ca lỗi nghiệp vụ khó hoặc phát hiện một luồng logic phức tạp có giá trị tái sử dụng cao, hãy sử dụng lệnh `/save-kb` hoặc `/adam-save-kb` để tự động đóng gói thành thẻ tri thức chuẩn hóa.
