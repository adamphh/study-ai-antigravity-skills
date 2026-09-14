# Tạo Plugin (Interceptor)

## Khi nào dùng loại nào

- **before**: cần sửa/validate input trước khi method gốc chạy, chưa cần kết quả
- **after**: cần dùng/sửa kết quả trả về sau khi method gốc chạy xong (phổ biến nhất)
- **around**: cần kiểm soát hoàn toàn việc có gọi method gốc hay không, hoặc
  đo thời gian thực thi, wrap try/catch quanh toàn bộ method gốc. Ưu tiên
  tránh dùng `around` nếu `before`/`after` đủ dùng (around có overhead cao hơn
  và dễ gây lỗi nếu quên gọi `$proceed()`)

## Thông tin cần hỏi người dùng nếu chưa có

- Class đích (target class) cần can thiệp
- Method cần can thiệp
- Mục đích nghiệp vụ cụ thể
- Tên module (mặc định Magestore_Webpos nếu không nói khác)

## Cấu trúc output cần sinh

1. `etc/di.xml` — khai báo plugin, có `sortOrder` hợp lý, cân nhắc xung đột
   nếu class đích có thể đã bị plugin bởi module khác (nhắc người dùng kiểm tra)
2. Plugin class trong `Plugin/{Module}/{ClassPath}/`
   - Constructor injection cho mọi dependency
   - Docblock đầy đủ mô tả mục đích
   - Xử lý exception hợp lý: nếu là hành động phụ (side-effect, VD: logging,
     đồng bộ dữ liệu) thì bắt exception và log lại, KHÔNG throw ra ngoài để
     tránh làm vỡ luồng chính (đặc biệt các luồng quan trọng như checkout,
     đặt hàng)

## Mẫu cấu trúc

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Plugin\{Path};

use {TargetClassNamespace};

class {Name}Plugin
{
    public function __construct(
        private readonly SomeDependencyInterface $dependency
    ) {
    }

    /**
     * {Mô tả mục đích}
     */
    public function after{MethodName}(TargetClass $subject, $result)
    {
        // logic
        return $result;
    }
}
```

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    <type name="{TargetClass}">
        <plugin name="{module}_{action}_{method}"
                type="{Vendor}\{Module}\Plugin\{Path}\{Name}Plugin"
                sortOrder="10"/>
    </type>
</config>
```

## Checklist trước khi trả lời

- [ ] Đã chọn đúng loại plugin (before/after/around) và giải thích lý do
- [ ] Không dùng ObjectManager trực tiếp
- [ ] Có xử lý exception hợp lý cho side-effect logic
- [ ] Nhắc người dùng kiểm tra xung đột sortOrder nếu class đích quan trọng
      (Order, Quote, Cart...)
