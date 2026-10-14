# Tạo Observer / Event

## Thông tin cần hỏi người dùng nếu chưa có

- Tên event cần lắng nghe (VD: `sales_order_place_after`)
- Mục đích nghiệp vụ
- Area cần áp dụng: global / frontend / adminhtml / webapi_rest / webapi_soap
- Tên module (mặc định Magestore_Webpos)

## Lưu ý khi chọn Observer vs Plugin

- Dùng **Observer** khi: event đã có sẵn (core dispatch sẵn), muốn nhiều
  module cùng lắng nghe độc lập mà không cần biết nhau tồn tại
- Dùng **Plugin** khi: cần can thiệp sâu vào input/output của 1 method cụ thể,
  hoặc method đó không có event tương ứng

## Cấu trúc output cần sinh

1. `etc/events.xml` (đặt đúng area tương ứng, VD `etc/frontend/events.xml`
   nếu chỉ cần frontend)
2. Observer class implement `Magento\Framework\Event\ObserverInterface`
   - Method `execute(Observer $observer)`
   - Lấy data qua `$observer->getEvent()->getData('key')` hoặc
     `$observer->getEvent()->getOrder()` v.v. tùy event
   - Có docblock giải thích event này dispatch ở đâu (nếu biết) và
     data truyền vào có gì

## Mẫu cấu trúc

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    <event name="{event_name}">
        <observer name="{module}_{purpose}_observer"
                  instance="{Vendor}\{Module}\Observer\{Name}Observer"/>
    </event>
</config>
```

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Observer;

use Magento\Framework\Event\Observer;
use Magento\Framework\Event\ObserverInterface;

/**
 * Lắng nghe event {event_name}, dispatch tại {nơi dispatch nếu biết}
 */
class {Name}Observer implements ObserverInterface
{
    public function __construct(
        private readonly SomeDependencyInterface $dependency
    ) {
    }

    public function execute(Observer $observer): void
    {
        $entity = $observer->getEvent()->getData('{key}');
        // logic
    }
}
```

## Checklist trước khi trả lời

- [ ] Chọn đúng area (global/frontend/adminhtml) cho events.xml
- [ ] Giải thích rõ observer này chạy đồng bộ (mặc định) hay cần chạy async
      (nếu nghiệp vụ nặng, đề xuất dùng message queue thay vì observer đồng bộ)
- [ ] Không dùng ObjectManager trực tiếp
