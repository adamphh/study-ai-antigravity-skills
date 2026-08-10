---
name: Script Indexer Architecture
description: Kiến trúc và quy chuẩn thiết kế bộ lập chỉ mục mã nguồn 2 tầng (Magento PHP & WebPOS JS) tối ưu Token cho AI Assistant
---

# Script Indexer Architecture (Antigravity Modular 2-Tier Script Indexing)

Tài liệu hướng dẫn kiến trúc và quy chuẩn thiết kế bộ lập chỉ mục mã nguồn 2 tầng cho Magento 2 Backend (PHP/XML) và WebPOS Client Frontend (React JS/Redux/IndexedDB).

---

## 1. Mục đích & Nguyên lý Tối ưu Token
- **Khắc phục Triệt để Vấn đề Tốn Token**: Loại bỏ 95% - 99% các câu lệnh `grep` rà soát mã nguồn thừa thãi vốn làm tràn Context Window và ngốn lượng lớn Token của AI.
- **Tăng Tốc độ Phản hồi**: Giúp AI định vị chính xác vị trí file, class, plugin và signature hàm trong **1 giây** thay vì mất 2-5 phút đọc mò mẫm qua nhiều lượt grep.
- **Tái sử dụng Vĩnh viễn (Cross-Project Reusability)**: Đảm bảo bộ chỉ mục Core (Magento & Magestore) được lập 1 lần và dùng lại cho 100% dự án khác mà không phải quét lại từ đầu.

---

## 2. Mô hình Kiến trúc 2 Tầng (2-Tier Architecture)

```
                                  ┌──────────────────────────────────────────────────────────┐
                                  │      AI AGENT TRA CỨU 2 TẦNG (Tiered Index Lookup)       │
                                  └────────────────────────────┬─────────────────────────────┘
                                                               │
                       ┌───────────────────────────────────────┴───────────────────────────────────────┐
                       ▼                                                                               ▼
┌───────────────────────────────────────────────┐                               ┌───────────────────────────────────────────────┐
│     TẦNG 1: CHỈ MỤC DÙNG CHUNG (Core Index)    │                               │    TẦNG 2: CHỈ MỤC DỰ ÁN (Project Index)     │
│ (Lưu tại: study-ai-antigravity-skills/)       │                               │ (Lưu tại: {project_root}/docs/data-flows/)    │
├───────────────────────────────────────────────┤                               ├───────────────────────────────────────────────┤
│ • Magestore Backend Core (`app/code/Magestore`)│                               │ • Magento Backend FixBug/Custom (`FixBug...`) │
│ • Magento 2 Framework & Vendor (`vendor/`)    │                               │ • WebPOS Client Extensions (`src/extension/`) │
│ • WebPOS Client Core (`client/pos/src/`)      │                               │ • Override Matrix riêng của từng dự án        │
└───────────────────────────────────────────────┘                               └───────────────────────────────────────────────┘
```

### Cấu trúc Phân tách Tường minh Theo Vendor Namespace & Server/Client

#### A. Tầng 1: Shared Core Index (`study-ai-antigravity-skills/indexes/`)
```
study-ai-antigravity-skills/indexes/
├── README.md                                    # Main Router Index Hub
├── server/                                      # 🖥️ SERVER SIDE CORE
│   └── vendor/
│       ├── magento/                             # Magento 2 Official Core Framework
│       │   ├── catalog.md
│       │   └── checkout.md
│       ├── magestore/                           # Magestore Core Backend
│       │   └── webpos-server.md
│       └── third-party/                         # Amasty, Aheadworks...
└── client/                                      # 📱 CLIENT SIDE CORE (WebPOS React JS)
    └── webpos-core/
        ├── core-services.md                     # ProductService, QuoteService, AddProductService...
        ├── core-epics-actions.md                # SearchProductByBarcodeEpic, AddProductEpic...
        └── core-indexeddb.md                    # IndexedDbProduct, IndexedDbStock...
```

#### B. Tầng 2: Project Local Index (`{project_root}/docs/data-flows/`)
```
{project_root}/docs/data-flows/
├── INDEX.md                                     # Project Router Index
├── server/project-custom/                       # 🖥️ SERVER FIXBUGS & CUSTOM
│   ├── magestore-fixbug.md                      # app/code/Magestore/FixBug... (PHP)
│   └── magestore-custom.md                      # app/code/Magestore/*Custom... (PHP)
└── client/project-extensions/                   # 📱 CLIENT EXTENSIONS
    ├── extension-plugins.md                     # Plugin (around/before/after)
    ├── extension-mixins.md                      # Mixin
    ├── extension-rewrites.md                    # Rewrite
    └── extension-observers.md                   # Observer on event-bus
```

---

## 3. Quy trình 3 Bước AI Tra cứu & Fallback Protocol (Handling Outdated Index)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AI Nhận Task Tra Cứu (VD: Sửa Bug X)                            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│              BƯỚC 1: Mở Router Index (INDEX.md / README.md) để tìm Symbol              │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                         ┌──────────────────┴──────────────────┐
                         │ Có tìm thấy Symbol trong Index không?│
                         └─────────┬───────────────────┬───────┘
                                CÓ │                   │ KHÔNG (Index bị Outdated / File mới)
                                   ▼                   ▼
              ┌──────────────────────────┐   ┌──────────────────────────────────────────────┐
              │ Mở trực tiếp File bằng   │   │  BƯỚC 2: Tự động chạy Refresh Index Script:  │
              │ `view_file` (0% grep)    │   │  `python3 scripts/index_project.py` (1s)     │
              └──────────────────────────┘   └──────────────────────┬───────────────────────┘
                                                                    │
                                                 ┌──────────────────┴──────────────────┐
                                                 │ Tìm thấy Symbol trong Index vừa mới? │
                                                 └─────────┬───────────────────┬───────┘
                                                        CÓ │                   │ KHÔNG
                                                           ▼                   ▼
                                      ┌──────────────────────────┐   ┌──────────────────────────┐
                                      │ Mở trực tiếp File bằng   │   │ BƯỚC 3 (Fallback): Grep  │
                                      │ `view_file`              │   │ khoanh vùng hẹp thư mục  │
                                      └──────────────────────────┘   └──────────────────────────┘
```

1. **Bước 1**: Mở Router Index (`INDEX.md`). Thấy -> mở trực tiếp bằng `view_file` (0% grep).
2. **Bước 2 (Auto-Refresh)**: Không thấy (Index cũ) -> AI tự động chạy `python3 scripts/index_project.py` (1s) để refresh. Sau đó mở lại `INDEX.md`.
3. **Bước 3 (Fallback)**: Vẫn không thấy (File 3rd party hoàn toàn mới) -> AI dùng `grep_search` khoanh vùng hẹp thư mục đó và tự ghi nhận lại vào `INDEX.md`.

---

## 4. Bảng Tổng hợp Băn khoăn & Giải pháp Kỹ thuật

| Băn khoăn | Nguyên nhân | Giải pháp Kỹ thuật |
| :--- | :--- | :--- |
| **File Index bị "béo" tràn Context?** | Quét 100% `vendor/` tạo ra file Markdown hàng nghìn dòng. | **Modular Reference Links**: Chia nhỏ index thành các file module. File tổng `README.md` chỉ dài ~30 dòng. |
| **Quét trùng lặp Core ở dự án mới?** | Mỗi dự án lại phải đi quét lại Magento Core và Magestore Core. | **Kiến trúc 2 Tầng**: Core Index lưu ở Repo kỹ năng dùng chung; Project Index lưu ở repo riêng. |
| **Thiếu tường minh giữa các Vendor?** | Để chung Magento Core và Magestore Core. | **Vendor Namespace Hierarchy**: Chia thư mục theo Vendor: `indexes/server/vendor/{magento,magestore,third-party}/`. |
| **Mất liên kết ngầm qua XML/Config?** | Magento PHP & WebPOS JS liên kết qua `di.xml`, `events.xml`, `config.js`. | **Config & AST Parser**: Script parse trực tiếp XML/JS config để dựng bảng ma trận `Plugin/Rewrite/Observer -> Target Core Class`. |
| **Thiếu Function Signatures & Tham số?** | AI thấy tên class nhưng vẫn phải mở file xem tham số. | **DocBlock & Signature Extraction**: Dùng Regex/AST trích xuất tên phương thức kèm danh sách tham số (`addProduct(quote: Object, data: Object)`). |

---

## 5. Mẫu Định dạng Index Standard Output

### File: `docs/data-flows/client/project-extensions/extension-plugins.md`
```markdown
# WebPOS Client Extension Plugins Matrix

## Extension Module: `webpos-fix` (`src/extension/webpos-fix/`)

### Target Core Service: `QuoteService`
- **Core File**: [`QuoteService.js`](file:///mnt/projects/p1060-graceandmarbel.co.uk/Source/client/pos/src/service/checkout/QuoteService.js)
- **Plugin Registrations**:
  | Method Name & Signature | Plugin Type | Extension Plugin File & Location | Purpose / Description |
  | :--- | :--- | :--- | :--- |
  | `addProduct(quote: Object, data: Object): Observable` | `around` | [`QuoteServicePlugin.js#L56`](file:///mnt/projects/p1060-graceandmarbel.co.uk/Source/client/pos/src/extension/webpos-fix/plugin/service/checkout/QuoteServicePlugin.js#L56) | Support async Promise return in offline mode |
  | `addProductToCurrentQuote(store: Object, product: Object)` | `around` | [`QuoteServicePlugin.js#L15`](file:///mnt/projects/p1060-graceandmarbel.co.uk/Source/client/pos/src/extension/webpos-fix/plugin/service/checkout/QuoteServicePlugin.js#L15) | Validate salable qty before opening product modal |
```
