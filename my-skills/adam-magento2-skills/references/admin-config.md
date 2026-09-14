# Tạo Cấu hình Trang Admin (system.xml)

## Quy trình thực hiện

1. Tạo file cấu hình `etc/adminhtml/system.xml` để định nghĩa giao diện cấu hình trong admin.
2. Tạo file `etc/config.xml` để định nghĩa giá trị cấu hình mặc định (default values).
3. Tạo class config reader (thường đặt ở `Model/Config.php` hoặc `Helper/Data.php`) để lấy giá trị từ database (`ScopeConfigInterface`).

## Cấu trúc mẫu

### etc/adminhtml/system.xml
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Config:etc/system_file.xsd">
    <system>
        <section id="payment" translate="label" type="text" sortOrder="400" showInDefault="1" showInWebsite="1" showInStore="1">
            <group id="custom_payment" translate="label" type="text" sortOrder="10" showInDefault="1" showInWebsite="1" showInStore="1">
                <label>Custom Payment Method</label>
                <field id="active" translate="label" type="select" sortOrder="1" showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Enabled</label>
                    <source_model>Magento\Config\Model\Config\Source\Yesno</source_model>
                </field>
                <field id="api_key" translate="label" type="password" sortOrder="2" showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>API Key</label>
                    <backend_model>Magento\Config\Model\Config\Backend\Encrypted</backend_model>
                </field>
            </group>
        </section>
    </system>
</config>
```

### etc/config.xml (Mặc định)
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Store:etc/config.xsd">
    <default>
        <payment>
            <custom_payment>
                <active>0</active>
            </custom_payment>
        </payment>
    </default>
</config>
```

### Model/Config.php (Class đọc cấu hình)
```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Model;

use Magento\Framework\App\Config\ScopeConfigInterface;
use Magento\Store\Model\ScopeInterface;
use Magento\Framework\Encryption\EncryptorInterface;

class Config
{
    private const XML_PATH_ACTIVE = 'payment/custom_payment/active';
    private const XML_PATH_API_KEY = 'payment/custom_payment/api_key';

    public function __construct(
        private readonly ScopeConfigInterface $scopeConfig,
        private readonly EncryptorInterface $encryptor
    ) {
    }

    /**
     * Check if payment method is enabled
     */
    public function isActive(int $storeId = null): bool
    {
        return $this->scopeConfig->isSetFlag(
            self::XML_PATH_ACTIVE,
            ScopeInterface::SCOPE_STORE,
            $storeId
        );
    }

    /**
     * Get decrypted API Key
     */
    public function getApiKey(int $storeId = null): string
    {
        $encryptedValue = $this->scopeConfig->getValue(
            self::XML_PATH_API_KEY,
            ScopeInterface::SCOPE_STORE,
            $storeId
        );
        return $encryptedValue ? $this->encryptor->decrypt($encryptedValue) : '';
    }
}
```

## Checklist trước khi trả lời

- [ ] Các config quan trọng (nhạy cảm) như API Key, Password, Secret Key phải khai báo sử dụng `<backend_model>Magento\Config\Model\Config\Backend\Encrypted</backend_model>` để mã hoá dữ liệu trong Database.
- [ ] Luôn khai báo giá trị mặc định (thường là Disable) trong `etc/config.xml`.
- [ ] Khi tiêm dependency `ScopeConfigInterface`, tránh tiêm trực tiếp vào các class Object có vòng đời ngắn (như Data Model), ưu tiên tạo class Config riêng để tăng tính tái sử dụng và dễ test.
