# Hướng dẫn Rewrite (Preference) Class trong Magento 2 Backend

Tài liệu này hướng dẫn cách thực hiện Rewrite (Preference) cho các Class (Model, ResourceModel, Controller, Block,
Helper) trong Magento 2 Backend bằng cơ chế Dependency Injection (DI) Preference.

---

## ⚠️ Nguyên tắc quan trọng & Thứ tự ưu tiên

1. **Ưu tiên Plugin (Interceptor) đầu tiên:**
   - Luôn ưu tiên dùng **Plugin (Before, After, Around)** hoặc **Observer** nếu có thể.
   - **CHỈ NÊN DÙNG Preference (Rewrite)** khi:
     - Cần thay đổi logic `protected` / `private` hoặc luồng xử lý bên trong một phương thức phức tạp.
     - Cần thay đổi Constructor (`__construct`) hoặc Override lại Interface binding.
2. **Quy định Phạm vi Sửa đổi (Allowed Scope):**
   - **TUYỆT ĐỐI KHÔNG** chỉnh sửa trực tiếp các file Core của Magento hoặc Magestore (`app/code/Magestore/`).
   - Các file Rewrite CHỈ ĐƯỢC PHÉP nằm trong module chứa từ `FixBug` (ví dụ `Magestore\WebposFixBug`) hoặc có hậu
     tố `Custom` (ví dụ `Magestore\WebposCustom`).
3. **Quy định Cú pháp Code PHP & XML:**
   - Khi tham chiếu class trong PHP, BẮT BUỘC dùng cú pháp `ClassName::class` thay vì chuỗi literal.
   - Copyright Header: Bắt buộc có ở đầu mỗi tệp PHP và XML.
   - Độ dài dòng: Tối đa **120 ký tự** trên mỗi dòng code.
   - DocBlock: Dòng đầu tiên là Description, có chính xác 1 dòng trống trước `@param` / `@return`.

---

## 📋 Bước 1: Khai báo Preference trong `etc/di.xml`

Trong module của bạn (ví dụ `app/code/Magestore/WebposFixBug`), khai báo thẻ `<preference>` trong file `etc/di.xml`
(hoặc `etc/frontend/di.xml`, `etc/adminhtml/di.xml` tùy scope).

```xml
<!--
  ~ Copyright © Magestore. All rights reserved.
  ~ See COPYING.txt for license details.
  -->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    <!-- Rewrite Class Model / Helper / Controller / Block -->
    <preference for="Magestore\Webpos\Model\Cart\CartManagement"
                type="Magestore\WebposFixBug\Model\Cart\CartManagement" />
</config>
```

---

## 💻 Bước 2: Tạo Class Rewrite (Child Class)

Class Rewrite phải kế thừa (`extends`) từ Class gốc và chỉ override lại phương thức cần thay đổi.

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

namespace Magestore\WebposFixBug\Model\Cart;

use Magestore\Webpos\Model\Cart\CartManagement as TargetCartManagement;

/**
 * Custom CartManagement to fix calculation bug.
 */
class CartManagement extends TargetCartManagement
{
    /**
     * Override save quote method to handle custom logic.
     *
     * @param \Magento\Quote\Api\Data\CartInterface $quote
     * @return bool
     */
    public function saveQuote($quote)
    {
        // Custom logic before core execution
        if (!$quote->getItemsCount()) {
            return false;
        }

        // Call parent method when needed
        return parent::saveQuote($quote);
    }
}
```

---

## 🛠️ Ví dụ các trường hợp Rewrite phổ biến

### 1. Rewrite Controller Action
Khai báo trong `etc/frontend/di.xml` hoặc `etc/adminhtml/di.xml`:

```xml
<!--
  ~ Copyright © Magestore. All rights reserved.
  ~ See COPYING.txt for license details.
  -->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    <preference for="Magestore\Webpos\Controller\Index\Index"
                type="Magestore\WebposFixBug\Controller\Index\Index" />
</config>
```

Class Rewrite Controller:
```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

namespace Magestore\WebposFixBug\Controller\Index;

use Magestore\Webpos\Controller\Index\Index as TargetIndex;
use Magento\Framework\Controller\ResultFactory;

/**
 * Custom Webpos Index Controller.
 */
class Index extends TargetIndex
{
    /**
     * Execute action with custom validation.
     *
     * @return \Magento\Framework\Controller\ResultInterface
     */
    public function execute()
    {
        // Add custom check or delegate to parent
        return parent::execute();
    }
}
```

### 2. Rewrite Block Class
Khai báo trong `etc/di.xml`:

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

namespace Magestore\WebposFixBug\Block;

use Magestore\Webpos\Block\Checkout as TargetCheckout;

/**
 * Custom Checkout Block.
 */
class Checkout extends TargetCheckout
{
    /**
     * Get custom template config.
     *
     * @return array
     */
    public function getConfig()
    {
        $config = parent::getConfig();
        $config['custom_param'] = true;
        return $config;
    }
}
```

---

## 🔍 Checklist Kiểm định sau khi Rewrite

- [ ] **XML Validation:** Sử dụng `view_file` kiểm tra 100% các thẻ XML mở/đóng đã khớp nhau.
- [ ] **Class Reference:** Đảm bảo sử dụng `TargetClass::class` hoặc `::class` khi truyền class name trong PHP.
- [ ] **Copyright Header:** Tệp PHP và XML đã có Header Magestore chuẩn.
- [ ] **Line Length:** Không có dòng nào vượt quá 120 ký tự.
- [ ] **Comment giải thích:** Thêm comment bằng tiếng Anh giải thích điểm khác biệt so với class gốc.
- [ ] **Compile & Cache:** Chạy `bin/magento setup:di:compile` và `bin/magento cache:clean` để áp dụng preference.
