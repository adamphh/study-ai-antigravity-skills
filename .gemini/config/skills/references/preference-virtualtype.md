# Preference / Virtual Type

## Khi nào dùng Preference

Chỉ dùng khi thực sự cần thay đổi hoàn toàn behavior của class (không thể
làm bằng Plugin), vì Preference có rủi ro:
- Chỉ 1 module được preference 1 class tại 1 thời điểm (nếu module khác
  cũng preference cùng class → conflict, module sau load sẽ ghi đè)
- Khi Magento upgrade, nếu core class đổi cấu trúc, class override dễ bị
  lỗi mà không có cảnh báo rõ ràng

## Khi nào dùng Virtual Type thay vì Preference

Dùng `virtualType` khi chỉ cần 1 instance của class với **cấu hình
constructor khác** (VD: đổi 1 dependency được inject), mà không cần đổi
toàn bộ class — an toàn hơn Preference rất nhiều vì không ảnh hưởng
các nơi khác đang dùng class gốc.

## Cấu trúc output cần sinh

### Preference

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Model;

use {OriginalClassNamespace};

class {Name} extends {OriginalClass}
{
    // override method cụ thể, gọi parent:: nếu chỉ cần bổ sung logic
}
```

```xml
<preference for="{OriginalClass}" type="{Vendor}\{Module}\Model\{Name}"/>
```

### Virtual Type

```xml
<virtualType name="{Vendor}{Module}Custom{Name}" type="{OriginalClass}">
    <arguments>
        <argument name="{constructorArgName}" xsi:type="object">
            {Vendor}\{Module}\Model\{CustomDependency}
        </argument>
    </arguments>
</virtualType>
```

## Checklist trước khi trả lời

- [ ] Đã cân nhắc và giải thích rõ tại sao không dùng Plugin được
- [ ] Đã cảnh báo rủi ro conflict nếu dùng Preference trên class quan trọng
      (Order, Quote, Product...)
- [ ] Đề xuất Virtual Type nếu chỉ cần đổi dependency, không cần đổi class
