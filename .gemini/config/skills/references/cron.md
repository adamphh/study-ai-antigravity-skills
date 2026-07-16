# Tạo Cron Job

## Thông tin cần hỏi người dùng nếu chưa có

- Tần suất chạy (cron expression)
- Mục đích nghiệp vụ
- Nguồn dữ liệu xử lý (bảng, API)
- Ước lượng khối lượng dữ liệu (để quyết định có cần xử lý theo batch không)

## Cấu trúc output cần sinh

1. `etc/crontab.xml`
2. Cron class (`Cron/{Name}.php`) với method `execute()`
   - Logging rõ ràng: bắt đầu, kết thúc, số lượng xử lý, lỗi (dùng
     `Psr\Log\LoggerInterface`, không dùng `var_dump`/`echo`)
   - Nếu số lượng bản ghi có thể lớn: xử lý theo batch (LIMIT/OFFSET hoặc
     cursor), không load hết vào memory cùng lúc
   - Bắt exception cho từng item riêng lẻ (nếu 1 item lỗi, không dừng
     toàn bộ job, log lại và tiếp tục item tiếp theo)

## Mẫu cấu trúc

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Cron:etc/crontab.xsd">
    <group id="default">
        <job name="{module}_{job_code}" instance="{Vendor}\{Module}\Cron\{Name}" method="execute">
            <schedule>{cron_expression}</schedule>
        </job>
    </group>
</config>
```

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Cron;

use Psr\Log\LoggerInterface;

class {Name}
{
    private const BATCH_SIZE = 100;

    public function __construct(
        private readonly SomeCollectionFactory $collectionFactory,
        private readonly LoggerInterface $logger
    ) {
    }

    public function execute(): void
    {
        $this->logger->info('{JobName}: started');
        $processed = 0;

        // xử lý theo batch, catch exception cho từng item

        $this->logger->info(sprintf('{JobName}: finished, processed %d items', $processed));
    }
}
```

## Checklist trước khi trả lời

- [ ] Có xử lý batch nếu dữ liệu lớn
- [ ] Có logging đầy đủ (start/end/count/error)
- [ ] Lỗi 1 item không làm dừng toàn bộ job
