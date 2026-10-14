# Tạo Data Patch (Setup/Patch/Data)

## Quy trình thực hiện

1. Tạo class Patch trong thư mục `Setup/Patch/Data/` triển khai `Magento\Framework\Setup\Patch\DataPatchInterface`.
2. Định nghĩa các dependencies trong `getDependencies()` nếu patch này cần chạy sau patch khác.
3. Thực thi logic thêm dữ liệu/cấu hình trong `apply()`.

## Cấu trúc mẫu

### Setup/Patch/Data/AddCustomConfigData.php
```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Setup\Patch\Data;

use Magento\Framework\Setup\Patch\DataPatchInterface;
use Magento\Framework\Setup\ModuleDataSetupInterface;
use Magento\Framework\App\Config\Storage\WriterInterface;
use Magento\Framework\App\Config\ScopeConfigInterface;

class AddCustomConfigData implements DataPatchInterface
{
    public function __construct(
        private readonly ModuleDataSetupInterface $moduleDataSetup,
        private readonly WriterInterface $configWriter
    ) {
    }

    /**
     * Run code to apply data patch
     */
    public function apply(): self
    {
        $this->moduleDataSetup->startSetup();

        // Ví dụ: Lưu cấu hình mặc định vào table core_config_data
        $this->configWriter->save(
            'payment/custom_payment/active',
            '1',
            ScopeConfigInterface::SCOPE_TYPE_DEFAULT,
            0
        );

        $this->moduleDataSetup->endSetup();
        return $this;
    }

    /**
     * Get dependencies of this patch
     */
    public static function getDependencies(): array
    {
        // Trả về danh sách class DataPatchInterface khác cần phải chạy TRƯỚC patch này
        return [];
    }

    /**
     * Get aliases
     */
    public function getAliases(): array
    {
        return [];
    }
}
```

## Checklist trước khi trả lời

- [ ] Data Patch chỉ chạy **một lần duy nhất** khi chạy lệnh `setup:upgrade`. Nếu muốn chỉnh sửa lại dữ liệu đã có ở patch cũ, hãy tạo một patch mới.
- [ ] Luôn sử dụng `ModuleDataSetupInterface` bọc trong `startSetup()` và `endSetup()`.
- [ ] Trả về `$this` ở cuối hàm `apply()`.
- [ ] Nếu patch có tạo EAV attribute (Product/Customer), hãy tiêm `Magento\Eav\Setup\EavSetupFactory` để tạo attribute thay vì viết SQL tay.
