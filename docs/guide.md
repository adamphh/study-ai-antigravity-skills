1. Chuẩn hoá input cho AI (Repo Brain)
Tạo 3 file sống cùng repo (cực kỳ quan trọng): đặt trong thư mục docs/

1.1 SYSTEM.md

Mô tả hệ thống ở mức kiến trúc, không code.

Ví dụ:

This is an offline-first POS system.
- Magento is the source of truth.
- Browser IndexedDB is the local store.
- POS must work without internet.
- Data consistency > real-time freshness.
- Snapshot + delta sync model.

1.2 INVARIANTS.md

Những luật không được phá.

- Product ID is immutable.
- Price shown at POS must be derivable from catalogrule.
- Offline sales must never be rejected due to missing data.
- Sync must be resumable and idempotent.

1.3 SYNC_SPEC.md

Spec bằng tiếng người, không PHP, không React.

Goal:
- Sync 1M+ records without overloading server.

Constraints:
- Multiple POS sync concurrently.
- Browser storage is IndexedDB.
- Network may drop anytime.

Strategy:
- Server builds snapshot.
- Client downloads snapshot in parts.
- Client applies deltas incrementally.

2. Link các file quan trọng vào trong README.md
## System Design
- docs/system.md – High-level system architecture
- docs/invariants.md – Non-negotiable system rules
- docs/sync_spec.md – POS sync strategy (snapshot + delta)

3. Đổi cách "prompt" → Agent Task
# Thay vì viết: 
    "Hãy viết code sync catalogrule"

# Hãy dùng task dạng agent:
    You are an AI engineer inside this repo.

    Task:
    - Audit current WebPOS sync flow.
    - Identify parts that violate snapshot + delta pattern.
    - Propose a new flow aligned with SYSTEM.md and INVARIANTS.md.

    Output:
    - High-level flow
    - Tables to keep / drop
    - Risk analysis

3.1 TASK_SYNC_CATALOG.md

Title: Sync Catalog to POS

Goal:
- Download catalog from Magento to POS.

Steps:
1. Call GET /api/pos/sync/catalog?since=0
2. Parse JSON response
3. Insert into IndexedDB.products
4. Update sync_state

Constraints:
- Use batching for large catalogs
- Handle network errors gracefully
- Idempotent operation

3.2 TASK_SYNC_ORDERS.md

Title: Sync Orders to Magento

Goal:
- Upload offline orders to Magento.

Steps:
1. Read orders from IndexedDB.orders where status = "pending"
2. POST to /api/pos/sync/orders
3. On success, update status = "synced"

Constraints:
- Retry on network errors
- Keep client-side orders until server confirms
- Handle duplicate detection

4. Agent Loop (trái tim của Antigravity)
Mỗi task luôn chạy vòng này:

Read

AI đọc repo

đọc schema

đọc docs

Plan

vẽ flow

chỉ ra trade-off

xác định failure modes

Act

viết code

viết migration

viết test

Verify

tự giả lập lỗi

đề xuất retry / resume

Hand-off

bạn review diff + logic

Bạn không nhảy vào giữa vòng.
Bạn chỉ xuất hiện ở bước 5.

5. Ví dụ task đúng kiểu Antigravity (rất quan trọng)
# TASK: POS Sync Engine
Context:
- Magento backend
- ReactJS POS client
- IndexedDB local store

Objective:
- Design a resumable snapshot download mechanism.

Rules:
- No request should fetch more than 500 records.
- Client must detect missing parts.
- Server must not recompute snapshot per POS.

Deliverables:
- Manifest format
- Part format
- Pseudocode for client sync engine

6. Chia nhỏ task theo chiều trí tuệ, không theo file
Sai lầm phổ biến:

“Viết file A, rồi file B”

Đúng kiểu Antigravity:

Task 1: define data contract

Task 2: define failure model

Task 3: define recovery

Task 4: implement

AI cực mạnh ở thiết kế tầng logic, đừng bắt nó làm việc tay chân trước.

7. Review như kiến trúc sư, không như coder
Khi AI trả code, bạn không hỏi:

đúng syntax chưa?

Bạn hỏi:

có phá invariant không?

có idempotent không?

mất mạng ở giữa thì sao?

10 POS sync cùng lúc có chết DB không?

8. Dấu hiệu bạn đã làm đúng Antigravity-style
Bạn biết mình đi đúng hướng khi:

AI chủ động đề xuất

bạn ít gõ code hơn nhưng hiểu hệ thống sâu hơn

code review giống review thiết kế

bạn nói “không” với AI nhiều hơn “ok”