# README — Skill `magento-webpos-dev`

Hướng dẫn nhanh cách gọi từng phần của skill. Không cần nhớ prompt chính xác —
chỉ cần mô tả đúng ý, Claude sẽ tự chọn đúng reference phù hợp bên dưới.

---

## 1. Tạo module mới (module scaffold)

**Dùng khi:** cần khung module cơ bản để hoạt động (registration.php,
module.xml, composer.json...)

**Ví dụ câu hỏi:**
- "Tạo module mới tên WebposSync, vendor Magestore, phụ thuộc Magento_Sales"
- "Sinh khung module Magestore_Webpos cơ bản, chưa cần chức năng gì"

**File tham chiếu:** `references/module-scaffold.md`

**Output:** `registration.php`, `etc/module.xml`, `composer.json`, gợi ý
`README.md`, lệnh `bin/magento` cần chạy sau khi tạo.

---

## 2. Sinh Data Interface + Model + Preference (tự động từ field bảng)

**Dùng khi:** cần Api Data Interface (const field + getter/setter) + Model
implement interface đó + đoạn preference trong di.xml, dựa theo field của
1 bảng.

**Ví dụ câu hỏi:**
- "Sinh Data Interface và Model cho bảng webpos_order_sync_queue, vendor
  Magestore, module Webpos, tên OrderSyncQueue" (kèm nội dung db_schema.xml
  nếu có, hoặc liệt kê field: entity_id int, order_id int, status varchar,
  synced_at timestamp)

**File tham chiếu:** `references/data-interface-model.md`
**Script chạy thật:** `scripts/generate_data_interface.py`

**Output:** `{Name}Interface.php`, `{Name}.php`, `di_xml_snippet.xml`

**Lưu ý:** script không tự sinh ResourceModel/Collection — cần kết hợp
thêm mục 3 bên dưới nếu bảng chưa tồn tại.

---

## 3. Tạo Database Schema (bảng mới)

**Dùng khi:** cần tạo bảng mới, thêm cột, hoặc cần Model/ResourceModel/Collection
đầy đủ cho 1 entity.

**Ví dụ câu hỏi:**
- "Tạo bảng webpos_order_sync_queue với các cột: entity_id, order_id,
  status, created_at"
- "Thêm Repository pattern cho bảng webpos_order_sync_queue"

**File tham chiếu:** `references/db-schema.md`

**Output:** `db_schema.xml`, `db_schema_whitelist.json` (nhắc lệnh generate),
Model, ResourceModel, Collection, (tuỳ chọn) Repository + Api Data Interface.

---

## 4. Tạo Plugin (Interceptor)

**Dùng khi:** cần can thiệp trước/sau/quanh 1 method của class có sẵn
(core hoặc module khác), mà không cần sửa trực tiếp class gốc.

**Ví dụ câu hỏi:**
- "Tạo plugin sau khi Order::place() chạy xong, ghi order_id vào bảng
  webpos_order_sync_queue"
- "Can thiệp vào Quote::collectTotals() để thêm phí POS"

**File tham chiếu:** `references/plugin.md`

**Output:** Plugin class (before/after/around) + đoạn `di.xml`.

---

## 5. Tạo Observer / Event

**Dùng khi:** cần lắng nghe 1 event có sẵn của Magento (không cần can
thiệp sâu vào input/output của 1 method cụ thể như Plugin).

**Ví dụ câu hỏi:**
- "Lắng nghe event sales_order_place_after để gửi thông báo cho Webpos"
- "Tạo observer cho event customer_login"

**File tham chiếu:** `references/event-observer.md`

**Output:** Observer class + `etc/events.xml`.

---

## 6. Tạo REST API

**Dùng khi:** cần thêm 1 endpoint REST mới cho module (VD: để Webpos
client gọi vào Magento).

**Ví dụ câu hỏi:**
- "Tạo REST API POST /V1/webpos/order/sync, input gồm order_id, pos_id"

**File tham chiếu:** `references/rest-api.md`

**Output:** `etc/webapi.xml`, Api Interface, Class xử lý logic, `di.xml`
preference.

---

## 7. Tạo GraphQL Query/Mutation

**Dùng khi:** cần thêm query hoặc mutation GraphQL mới.

**Ví dụ câu hỏi:**
- "Tạo GraphQL query webposOrderStatus, input order_id, trả về status
  và synced_at"

**File tham chiếu:** `references/graphql.md`

**Output:** `schema.graphqls`, Resolver class.

---

## 8. Tạo Cron Job

**Dùng khi:** cần 1 tác vụ chạy định kỳ (VD: đồng bộ dữ liệu theo lịch).

**Ví dụ câu hỏi:**
- "Tạo cron job chạy mỗi 5 phút, đọc các bản ghi status=pending trong
  webpos_order_sync_queue và gọi API đồng bộ"

**File tham chiếu:** `references/cron.md`

**Output:** `etc/crontab.xml`, Cron class (có xử lý batch + logging).

---

## 9. Preference / Virtual Type

**Dùng khi:** cần override toàn bộ 1 class (Preference) hoặc chỉ đổi
dependency được inject vào class đó (Virtual Type) — chỉ dùng khi Plugin
không đáp ứng được.

**Ví dụ câu hỏi:**
- "Override class Magento\Checkout\Model\Cart vì cần đổi hoàn toàn logic
  addProduct()"
- "Tạo virtual type cho Quote với logger riêng"

**File tham chiếu:** `references/preference-virtualtype.md`

**Output:** Class override hoặc `<virtualType>`, cảnh báo rủi ro conflict.

---

## 10. Review code / diff

**Dùng khi:** cần review code trước khi merge.

**Ví dụ câu hỏi:**
- "Review đoạn diff này giúp tôi" (kèm paste code)

**File tham chiếu:** `references/code-review.md`

**Output:** Phân loại theo Vấn đề nghiêm trọng / Nên cải thiện / Góp ý nhỏ.

---

## 11. Debug lỗi

**Dùng khi:** gặp lỗi/exception cần tìm nguyên nhân và cách fix.

**Ví dụ câu hỏi:**
- "Tôi gặp lỗi này khi đặt hàng POS, giúp tôi debug" (kèm stack trace + code)

**File tham chiếu:** `references/debugging.md`

**Output:** Nguyên nhân gốc, class/method liên quan, đề xuất fix, cảnh báo
rủi ro.

---

## Mẹo dùng skill hiệu quả

- Không cần nhớ đúng từ khoá — mô tả đúng nghiệp vụ là đủ, Claude tự chọn
  reference phù hợp.
- Nếu Claude chọn sai hoặc không tự áp dụng skill, nói rõ hơn: *"dùng skill
  magento-webpos-dev, phần [tên mục ở trên]"*.
- Luôn cung cấp: tên Vendor/Module, tên class/bảng liên quan — nếu thiếu,
  Claude sẽ hỏi lại thay vì tự đoán.
- Gặp tác vụ lặp lại lần thứ 2 mà chưa có trong danh sách trên? Thêm 1 file
  `.md` mới vào `references/`, rồi thêm 1 mục vào file README này để lần
  sau không quên.
