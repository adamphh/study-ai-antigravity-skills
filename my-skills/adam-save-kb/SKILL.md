---
name: adam-save-kb
description: Trích xuất và lưu trữ luồng dữ liệu nghiệp vụ (Data Flows) và cơ chế vận hành hệ thống vào Bộ Não Thứ 2 (docs/knowledge-base/) và tự động cập nhật bảng tra cứu README.md. Trigger bằng /adam-save-kb hoặc /save-kb.
---

# Kỹ năng Lưu Trữ Luồng Nghiệp Vụ (/adam-save-kb)

Kỹ năng này giúp chuẩn hóa và lưu trữ các luồng dữ liệu (Data Flows), quy trình vận hành hệ thống (System Workflows) và logic nghiệp vụ cốt lõi vào **Bộ Não Thứ 2** tại `docs/knowledge-base/`, đồng thời tự động cập nhật bảng tra cứu `docs/knowledge-base/README.md`.

---

## 📋 Quy Trình Thực Hiện (Workflow)

### Bước 1: Thu thập & Phân tích Luồng Dữ liệu
AI tự động trích xuất các thông tin nghiệp vụ sau từ ngữ cảnh hội thoại hiện tại (hoặc hỏi lập trình viên nếu thiếu dữ liệu):
1. **Tiêu đề luồng (`title`)**: Nêu bật bản chất quy trình/luồng dữ liệu (Ví dụ: *"Luồng đồng bộ dữ liệu Offline"*).
2. **Domain nghiệp vụ (`domain`)**:
   - `sync-offline` (Đồng bộ, IndexedDB, Chế độ offline)
   - `inventory` (Tồn kho, MSI, Salable Qty, Backorder)
   - `search` (Tìm kiếm sản phẩm, OpenSearch, Elastic, MySQL)
   - `checkout-payment` (Đặt hàng, Split payment, Terminal)
   - `pricing-tax` (Tính giá, Khuyến mãi, Thuế)
   - *Hoặc domain nghiệp vụ mới do người dùng đặt.*
3. **Mục tiêu & Bản chất nghiệp vụ (Business Context & Purpose)**.
4. **Sơ đồ Luồng Dữ Liệu (Mermaid Sequence Diagram / Flowchart)**.
5. **Các giai đoạn vận hành chi tiết (Step-by-step Lifecycle Phases)**: Mô tả dữ liệu di chuyển từ đâu tới đâu qua từng trạm.
6. **Cấu trúc Dữ liệu & Biến đổi Trạng thái (Data Schemas & State Transitions)**.
7. **Điều kiện Phân nhánh & Ngoại lệ (Branching Conditions & Business Exceptions)**.

---

### Bước 2: Sinh Mã Định Danh Luồng (Data Flow ID)
- Cú pháp ID: `DF-<DOMAIN_PREFIX>-<NUMBER>` (Ví dụ: `DF-SNC-01`, `DF-INV-01`, `DF-SRC-01`, `DF-CHK-01`, `DF-PRC-01`).

---

### Bước 3: Tạo Tệp Luồng Dữ Liệu
Tạo file mới tại: `docs/knowledge-base/<domain>/<kebab-case-slug>.md` bằng công cụ `write_to_file`.

---

### Bước 4: Cập Nhật Bảng Mục Lục README.md
1. Mở file `docs/knowledge-base/README.md`.
2. Chèn 1 dòng mới vào bảng `<!-- KB_INDEX_START --> ... <!-- KB_INDEX_END -->`:
   ```markdown
   | [<ID>](file:///home/bss/docs/knowledge-base/<domain>/<slug>.md) | **<Title>** | `<domain>` | <Phạm vi nghiệp vụ tóm tắt> | <YYYY-MM-DD> |
   ```

---

### Bước 5: Bàn Giao & Thông Báo
Gửi phản hồi xác nhận cho lập trình viên kèm đường link mở trực tiếp tệp luồng dữ liệu vừa tạo.
