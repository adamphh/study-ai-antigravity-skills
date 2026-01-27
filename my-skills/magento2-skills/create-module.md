---
name: Create Magento 2 Module
description: Hướng dẫn tạo một module Magento 2 mới với cấu trúc chuẩn
---

# Tạo Module Magento 2 Mới

## Cấu trúc thư mục cơ bản

Một module Magento 2 cần có cấu trúc sau:

```
app/code/{Vendor}/{ModuleName}/
├── etc/
│   └── module.xml
├── registration.php
└── composer.json (optional)
```

## Bước 1: Tạo file registration.php

```php
<?php
/**
 * Copyright © {Vendor} All rights reserved.
 */

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    '{Vendor}_{ModuleName}',
    __DIR__
);
```

## Bước 2: Tạo file etc/module.xml

```xml
<?xml version="1.0"?>
<!--
/**
 * Copyright © {Vendor} All rights reserved.
 */
-->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="{Vendor}_{ModuleName}" setup_version="1.0.0">
        <sequence>
            <!-- Thêm các module dependencies ở đây -->
            <!-- <module name="Magento_Catalog"/> -->
        </sequence>
    </module>
</config>
```

## Bước 3: Tạo file composer.json (Optional)

```json
{
    "name": "{vendor}/{module-name}",
    "description": "Mô tả module của bạn",
    "type": "magento2-module",
    "version": "1.0.0",
    "license": "proprietary",
    "autoload": {
        "files": [
            "registration.php"
        ],
        "psr-4": {
            "{Vendor}\\{ModuleName}\\": ""
        }
    }
}
```

## Bước 4: Kích hoạt module

```bash
# Kiểm tra module đã được nhận diện
bin/magento module:status

# Kích hoạt module
bin/magento module:enable {Vendor}_{ModuleName}

# Chạy setup upgrade
bin/magento setup:upgrade

# Compile DI (production mode)
bin/magento setup:di:compile

# Deploy static content (production mode)
bin/magento setup:static-content:deploy -f

# Xóa cache
bin/magento cache:flush
```

## Lưu ý quan trọng

1. **Tên Vendor**: Sử dụng PascalCase (VD: `Bss`, `MyCompany`)
2. **Tên Module**: Sử dụng PascalCase, không có dấu gạch dưới trong tên (VD: `CustomerReview`, `OrderExport`)
3. **Dependencies**: Luôn khai báo các module phụ thuộc trong `<sequence>` để đảm bảo thứ tự load đúng
4. **Version**: Tuân theo semantic versioning (MAJOR.MINOR.PATCH)
