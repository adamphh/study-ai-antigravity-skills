# Tạo Module Cơ Bản (Module Scaffold)

## Thông tin cần hỏi người dùng nếu chưa có

- Tên Vendor (VD: `Magestore`)
- Tên Module (VD: `Webpos`, hoặc tên module con mới VD: `WebposSync`)
- Mục đích module (mô tả ngắn, dùng cho composer.json + README)
- Có cần phụ thuộc (`depends`) vào module nào khác không (VD: `Magento_Sales`,
  `Magento_Catalog`, hoặc chính `Magestore_Webpos` nếu là module con)
- Có cần setup sẵn ACL, menu admin, hay chỉ cần module rỗng hoạt động được

## Nguyên tắc

- Một module Magento 2 **bắt buộc tối thiểu** phải có 2 file để được nhận diện:
  `registration.php` và `etc/module.xml`. Thiếu 1 trong 2 file này module
  sẽ không được Magento nhận diện.
- Không tự ý thêm các thư mục/file không cần thiết ngay từ đầu (VD: đừng
  sinh sẵn `Controller/`, `Block/` nếu người dùng chưa nói cần) — chỉ sinh
  bộ khung tối thiểu + các phần người dùng yêu cầu rõ.
- Luôn hỏi rõ nếu tên Vendor/Module người dùng đưa có khoảng trắng hoặc
  ký tự đặc biệt — namespace Magento chỉ dùng chữ cái, số, không dấu gạch
  dưới ở giữa tên (VD: `Magestore\WebposSync`, không phải `Web_Pos_Sync`)

## Bộ file tối thiểu cần sinh

```
app/code/{Vendor}/{Module}/
├── registration.php
├── composer.json
├── etc/
│   └── module.xml
└── README.md   (khuyến khích, không bắt buộc)
```

Nếu người dùng cần thêm các phần cụ thể (ACL, menu admin, DI...), bổ sung
thêm theo yêu cầu:

```
├── etc/
│   ├── di.xml              (nếu cần khai báo Plugin/Preference — có thể để trống ban đầu)
│   ├── acl.xml             (nếu cần phân quyền admin)
│   └── adminhtml/
│       └── menu.xml        (nếu cần thêm menu trong admin panel)
├── i18n/
│   └── en_US.csv           (nếu cần đa ngôn ngữ cho label)
```

## Mẫu nội dung từng file

### registration.php

```php
<?php
use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    '{Vendor}_{Module}',
    __DIR__
);
```

### etc/module.xml

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="{Vendor}_{Module}" setup_version="1.0.0">
        <sequence>
            <!-- liệt kê module phụ thuộc, VD: -->
            <module name="Magento_Sales"/>
            <module name="Magestore_Webpos"/>
        </sequence>
    </module>
</config>
```

Lưu ý: chỉ thêm `<sequence>` nếu module thực sự phụ thuộc thứ tự load với
module khác (VD: cần extend/plugin class của module đó). Nếu không có
phụ thuộc, bỏ hẳn thẻ `<sequence>`.

### composer.json

```json
{
    "name": "{vendor-lowercase}/module-{module-lowercase}",
    "description": "{Mô tả ngắn mục đích module}",
    "type": "magento2-module",
    "license": ["OSL-3.0", "AFL-3.0"],
    "require": {
        "php": "~8.1.0||~8.2.0",
        "magento/framework": "*"
    },
    "autoload": {
        "files": ["registration.php"],
        "psr-4": {
            "{Vendor}\\{Module}\\": ""
        }
    }
}
```

### etc/di.xml (khung rỗng, mở rộng sau khi có Plugin/Preference)

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
</config>
```

### README.md (khuyến khích, giúp dev khác hiểu nhanh module)

```markdown
# {Vendor}_{Module}

## Mục đích
{Mô tả ngắn gọn module này làm gì}

## Phụ thuộc
- {Danh sách module phụ thuộc nếu có}

## Cài đặt
\`\`\`
bin/magento module:enable {Vendor}_{Module}
bin/magento setup:upgrade
bin/magento setup:di:compile
bin/magento cache:flush
\`\`\`
```

## Các bước sau khi sinh xong (nhắc người dùng)

1. Chạy `bin/magento module:enable {Vendor}_{Module}`
2. Chạy `bin/magento setup:upgrade`
3. Chạy `bin/magento setup:di:compile` (nếu có thêm class trong di.xml)
4. Chạy `bin/magento cache:flush`
5. Kiểm tra module đã active: `bin/magento module:status {Vendor}_{Module}`

## Checklist trước khi trả lời

- [ ] Namespace Vendor/Module hợp lệ, không có ký tự đặc biệt
- [ ] Chỉ sinh `<sequence>` trong module.xml nếu thực sự có phụ thuộc thứ tự
- [ ] Không sinh sẵn Controller/Block/Model rỗng nếu người dùng chưa yêu cầu —
      module scaffold chỉ nên tối thiểu, phần chức năng cụ thể dùng các
      reference khác trong skill này (plugin.md, rest-api.md, db-schema.md...)
- [ ] Có hướng dẫn các lệnh `bin/magento` cần chạy sau khi tạo xong
