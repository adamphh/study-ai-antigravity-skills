---
name: adam-code-review
description: Ma trận kiểm tra và rà soát logic mã nguồn (SQL injection, N+1 query, constructor backward compatibility, null-pointer, extension attributes, in-function require) dành cho Main Agent tự rà soát trước khi kết thúc task. Kích hoạt khi review code hoặc gõ /adam-code-review.
---

# Kỹ năng Rà Soát Logic Mã Nguồn & An Toàn (/adam-code-review)

Kỹ năng này cung cấp **Ma trận Rà Soát Nhanh (Fast Review Matrix)** cho Main Agent tự kiểm tra trực tiếp diff của mình sau khi `adam-code-linter` đã PASS, giúp thay thế Subagent cho các task thông thường và tiết kiệm ~50.000 tokens.

---

## 📋 Ma Trận Rà Soát Logic (Fast Review Matrix)

Main Agent tự đối soát diff của mình qua 6 chốt chặn sau:

### 1. Backend Magento 2 (PHP):
- [ ] **Tương thích ngược Constructor**: Tham số mới có được khai báo nullable ở cuối cùng (`?TypeInterface $param = null`) và fallback qua `ObjectManager` không?
- [ ] **SQL Injection & Query Performance**: Có nối chuỗi thô vào query không? Bắt buộc dùng `quoteInto` hoặc bind variables. Không query trong vòng lặp (N+1).
- [ ] **Extension Attributes Rule**: Không được gọi `getData()` / `setData()` trên Extension Interface. Bắt buộc dùng camelCase getter/setter chuẩn (`getWorkStation()`).
- [ ] **Reindex Realtime**: Observer reindex realtime có dùng event `_commit_after` và bọc `try-catch` kèm check `!$indexer->isScheduled()` không?
- [ ] **No Empty Catch**: Khối `catch (\Exception $e)` có ghi log hoặc fallback không, tuyệt đối không để rỗng.

### 2. Frontend WebPOS Client (JS/React):
- [ ] **In-function Require**: Ngoại trừ React, các Core Service/Helper có được nạp bằng `require("...").default` bên trong thân hàm không?
- [ ] **No Anonymous Default Export**: Có khai báo biến/hằng số có tên trước khi `export default` không (tránh lỗi ESLint)?
- [ ] **Tồn kho khả dụng (Available Qty)**: Kiểm tra tồn kho có dùng `Math.min(salableQty, qtyInLocation)` không?

---

## 🚦 Quy Tắc Chuyển Tiếp (Transition Decision)
- **Nếu là Task thông thường (UI/UX, CSS, đổi label, filter grid, validation đơn giản)**:
  - Main Agent tự tích đủ 6 tiêu chí trên $\rightarrow$ **PASS 100%** $\rightarrow$ Chuyển thẳng sang bước hiển thị Git Suggestion Block.
- **Nếu là Task Rủi Ro Cao (Payment, MSI Inventory, Offline IndexedDB Sync, Reindex realtime)**:
  - Main Agent sau khi tự rà soát xong $\rightarrow$ **BẮT BUỘC gọi Subagent Reviewer độc lập** theo đúng quy định phân cấp rủi ro.
