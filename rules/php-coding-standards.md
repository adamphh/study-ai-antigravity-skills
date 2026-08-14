# PHP Coding Standards & Formatting Invariants

## 1. Strict Types Declaration
Mỗi file `.php` khi được sinh mới hoặc tùy chỉnh phải khai báo `declare(strict_types=1);` ngay phía dưới khối comment Copyright Header, cách 1 dòng trống trước `namespace`:

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

declare(strict_types=1);

namespace Magestore\FixBug\...;
```

## 2. No Class DocBlock / Comment Rule
Tuyệt đối KHÔNG viết khối comment (DocBlock) cho `class`. Khai báo `class` trực tiếp ngay sau khối `use`.

## 3. Customization Inline Comment Rule
Luôn bổ sung comment bằng tiếng Anh giải thích đoạn code được tùy chỉnh/ghi đè so với class gốc, bao gồm logic gốc và logic tùy chỉnh mới.

## 4. Magento 2 Realtime Reindex Observer Invariants
Khi viết Observer cho các sự kiện Reindex dữ liệu realtime (Update on Save) sang Search Engine (Elasticsearch / OpenSearch):

1. **Bắt buộc dùng Event `_commit_after`**:
   - Luôn sử dụng sự kiện `_commit_after` (ví dụ: `sales_order_save_commit_after`, `catalog_product_save_commit_after`) thay vì `_save_after`.
   - *Lý do*: Đảm bảo CSDL đã `COMMIT` giao dịch trước khi thực thi I/O request API sang Search Engine, tránh rủi ro kéo dài DB Transaction Lock và Stale Data Race Condition.

2. **Bắt buộc bọc `try-catch` & Logger**:
   - Khối reindex trong Observer BẮT BUỘC phải bọc trong `try { ... } catch (\Throwable $e) { $this->logger->error(...); }`.
   - *Lý do*: Ngăn chặn việc dịch vụ Search Engine gặp sự cố tạm thời (timeout, connection refused) làm gián đoạn hoặc Rollback toàn bộ luồng tạo đơn hàng của khách.

3. **Kiểm tra Indexer Mode (`!$indexer->isScheduled()`)**:
   - Luôn sử dụng `Magento\Framework\Indexer\IndexerRegistry` kiểm tra `if (!$indexer->isScheduled())` trước khi gọi `executeList()`.
   - *Lý do*: Đảm bảo chỉ reindex realtime khi hệ thống ở chế độ **Update on Save**, tránh chạy trùng lặp với mview cron khi ở chế độ **Update on Schedule**.

## 5. Strict Indentation-Aware Line Length Check
Khi tính độ dài dòng code:
- Tổng số ký tự của một dòng = `Số khoảng trắng thụt lề (Leading Spaces) + Độ dài phần văn bản (Content Length)`.
- Nếu tổng vượt quá 120 ký tự, BẮT BUỘC phải ngắt dòng (multiline wrap) đối với các tham số hàm, mảng, hoặc chuỗi log.

## 6. End of File (EOF) Single Newline Rule
Mỗi file code khi lưu BẮT BUỘC chỉ có chính xác 1 dòng trống / ký tự xuống dòng (1 newline) ở cuối file. Tuyệt đối không để thừa 2 hoặc nhiều dòng trống ở EOF để tránh cảnh báo PHPCS: `Expected 1 blank line at end of file; X found`.

## 7. Magento 2 Extension Attributes Access Invariants
Các class Extension Interface (như `ProductExtensionInterface`, `ItemExtensionInterface`, ...) được Magento sinh tự động từ `\Magento\Framework\Api\AbstractSimpleObject`, **KHÔNG kế thừa** từ `\Magento\Framework\DataObject`.
- **Tuyệt đối KHÔNG** gọi `getData()` hoặc `setData()` trên đối tượng extension attributes.
- **Bắt buộc** sử dụng getter/setter chuẩn dạng camelCase được sinh tự động theo khai báo attribute (ví dụ `getWorkStation()`, `setWorkStation($val)`) hoặc kiểm tra `method_exists()` trước khi gọi.

## 8. No Empty Catch Block Rule
Trong các khối `try ... catch (\Exception $e)` (hoặc `\Throwable $e` cho Observer/Critical I/O), TUYỆT ĐỐI KHÔNG để khối `catch` rỗng không có câu lệnh xử lý (gây cảnh báo PHPCS `Empty CATCH statement detected`). Phải ghi log lỗi qua `$this->logger->error(...)` hoặc có câu lệnh gán biến fallback (ví dụ `$result = null;`).
