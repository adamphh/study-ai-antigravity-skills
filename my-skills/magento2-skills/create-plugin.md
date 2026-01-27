---
name: Create Plugin (Interceptor)
description: Hướng dẫn tạo Plugin/Interceptor trong Magento 2 để modify behavior của class
---

# Tạo Plugin (Interceptor) trong Magento 2

Plugin là cách mạnh mẽ để modify behavior của public methods trong Magento 2 mà không cần override class.

## Các loại Plugin

| Loại | Method Prefix | Thời điểm chạy |
|------|---------------|----------------|
| Before | `before` | Trước khi method gốc chạy |
| After | `after` | Sau khi method gốc chạy |
| Around | `around` | Wrap method gốc |

---

## Before Plugin

Modify input parameters trước khi method thực thi.

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Plugin;

use Magento\Catalog\Model\Product;

class ProductBeforePlugin
{
    /**
     * Before get name - modify arguments
     *
     * @param Product $subject
     * @return array|null
     */
    public function beforeSetName(Product $subject, string $name): array
    {
        // Modify the input parameter
        $modifiedName = strtoupper($name);
        
        // Return modified arguments as array
        return [$modifiedName];
    }
}
```

### Quy tắc Before Plugin:
- Method name: `before` + PascalCase của method gốc
- Parameter đầu tiên: `$subject` (object chứa method gốc)
- Các parameters tiếp theo: giống method gốc
- Return: `array` chứa modified arguments hoặc `null` để giữ nguyên

---

## After Plugin

Modify kết quả trả về sau khi method thực thi.

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Plugin;

use Magento\Catalog\Model\Product;

class ProductAfterPlugin
{
    /**
     * After get name - modify result
     *
     * @param Product $subject
     * @param string $result
     * @return string
     */
    public function afterGetName(Product $subject, string $result): string
    {
        // Modify the result
        return $result . ' - Modified';
    }
}
```

### Quy tắc After Plugin:
- Method name: `after` + PascalCase của method gốc
- Parameter đầu tiên: `$subject`
- Parameter thứ hai: `$result` (kết quả từ method gốc)
- Return: Modified result

---

## Around Plugin

Wrap toàn bộ method gốc, có thể thay đổi cả input và output.

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Plugin;

use Magento\Catalog\Model\Product;

class ProductAroundPlugin
{
    /**
     * Around get name - full control
     *
     * @param Product $subject
     * @param callable $proceed
     * @param mixed ...$args
     * @return string
     */
    public function aroundGetName(Product $subject, callable $proceed): string
    {
        // Code before original method
        $beforeValue = 'Before: ';
        
        // Call original method
        $result = $proceed();
        
        // Code after original method
        return $beforeValue . $result . ' :After';
    }
    
    /**
     * Around method with parameters
     *
     * @param Product $subject
     * @param callable $proceed
     * @param string $name
     * @return Product
     */
    public function aroundSetName(Product $subject, callable $proceed, string $name): Product
    {
        // Modify input
        $modifiedName = strtoupper($name);
        
        // Call original with modified input
        $result = $proceed($modifiedName);
        
        return $result;
    }
}
```

### Quy tắc Around Plugin:
- Method name: `around` + PascalCase của method gốc
- Parameter đầu tiên: `$subject`
- Parameter thứ hai: `$proceed` (callable đến method gốc)
- Các parameters tiếp theo: giống method gốc
- **PHẢI gọi `$proceed()`** nếu muốn method gốc chạy

---

## Cấu hình Plugin trong di.xml

`etc/di.xml` hoặc `etc/frontend/di.xml` hoặc `etc/adminhtml/di.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    
    <!-- Basic Plugin -->
    <type name="Magento\Catalog\Model\Product">
        <plugin name="{vendor}_{modulename}_product_plugin"
                type="{Vendor}\{ModuleName}\Plugin\ProductPlugin"
                sortOrder="10"
                disabled="false"/>
    </type>
    
    <!-- Multiple Plugins on same class -->
    <type name="Magento\Checkout\Model\Cart">
        <plugin name="{vendor}_{modulename}_cart_before"
                type="{Vendor}\{ModuleName}\Plugin\Cart\BeforeAddPlugin"
                sortOrder="10"/>
        <plugin name="{vendor}_{modulename}_cart_after"
                type="{Vendor}\{ModuleName}\Plugin\Cart\AfterAddPlugin"
                sortOrder="20"/>
    </type>
    
</config>
```

---

## Ví dụ thực tế: Modify Product Price

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Plugin\Catalog;

use Magento\Catalog\Model\Product;

class ProductPricePlugin
{
    /**
     * Add 10% to all product prices
     *
     * @param Product $subject
     * @param float $result
     * @return float
     */
    public function afterGetPrice(Product $subject, $result): float
    {
        if ($result === null) {
            return 0.0;
        }
        
        // Add 10% markup
        return (float)$result * 1.10;
    }
}
```

---

## Thứ tự thực thi Plugin

```
1. Before Plugins (theo sortOrder tăng dần)
2. Around Plugin (phần trước $proceed())
3. Original Method
4. Around Plugin (phần sau $proceed())
5. After Plugins (theo sortOrder tăng dần)
```

---

## Lưu ý quan trọng

> [!WARNING]
> **Around Plugin**: Cẩn thận khi sử dụng, vì nếu quên gọi `$proceed()` sẽ block method gốc hoàn toàn!

> [!IMPORTANT]
> **Không thể Plugin**:
> - Final methods
> - Final classes
> - Non-public methods
> - Static methods
> - `__construct`
> - Virtual types

> [!TIP]
> **Best Practice**:
> - Ưu tiên sử dụng Before/After thay vì Around
> - Đặt sortOrder hợp lý để kiểm soát thứ tự thực thi
> - Sử dụng area-specific di.xml (frontend/adminhtml) khi cần
