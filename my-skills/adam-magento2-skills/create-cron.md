---
name: Create Cron Job
description: Hướng dẫn tạo Cron Job trong Magento 2
---

# Tạo Cron Job trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── Cron/
│   └── {CronJobName}.php
└── etc/
    ├── crontab.xml
    └── cron_groups.xml (optional)
```

## 1. Tạo Cron Class

`Cron/{CronJobName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Cron;

use Psr\Log\LoggerInterface;

class {CronJobName}
{
    private LoggerInterface $logger;

    public function __construct(LoggerInterface $logger)
    {
        $this->logger = $logger;
    }

    /**
     * Execute cron job
     *
     * @return void
     */
    public function execute(): void
    {
        $this->logger->info('Cron job {CronJobName} started');
        
        try {
            // Your cron logic here
            
            $this->logger->info('Cron job {CronJobName} completed');
        } catch (\Exception $e) {
            $this->logger->error('Cron job error: ' . $e->getMessage());
        }
    }
}
```

## 2. Đăng ký Cron trong crontab.xml

`etc/crontab.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Cron:etc/crontab.xsd">
    
    <group id="default">
        <!-- Run every 5 minutes -->
        <job name="{vendor}_{modulename}_{cronname}" 
             instance="{Vendor}\{ModuleName}\Cron\{CronJobName}" 
             method="execute">
            <schedule>*/5 * * * *</schedule>
        </job>
        
        <!-- Run daily at midnight -->
        <job name="{vendor}_{modulename}_daily" 
             instance="{Vendor}\{ModuleName}\Cron\DailyJob" 
             method="execute">
            <schedule>0 0 * * *</schedule>
        </job>
        
        <!-- Configurable schedule from admin -->
        <job name="{vendor}_{modulename}_configurable" 
             instance="{Vendor}\{ModuleName}\Cron\ConfigurableJob" 
             method="execute">
            <config_path>{vendor}_{modulename}/cron/schedule</config_path>
        </job>
    </group>
    
</config>
```

## Cron Schedule Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

**Ví dụ:**
- `*/5 * * * *` - Mỗi 5 phút
- `0 * * * *` - Mỗi giờ
- `0 0 * * *` - Mỗi ngày lúc 00:00
- `0 0 * * 0` - Mỗi Chủ nhật lúc 00:00
- `0 0 1 * *` - Ngày đầu tiên mỗi tháng

## 3. Custom Cron Group (Optional)

`etc/cron_groups.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Cron:etc/cron_groups.xsd">
    
    <group id="{vendor}_{modulename}">
        <schedule_generate_every>1</schedule_generate_every>
        <schedule_ahead_for>4</schedule_ahead_for>
        <schedule_lifetime>2</schedule_lifetime>
        <history_cleanup_every>10</history_cleanup_every>
        <history_success_lifetime>60</history_success_lifetime>
        <history_failure_lifetime>600</history_failure_lifetime>
        <use_separate_process>0</use_separate_process>
    </group>
    
</config>
```

## Chạy và Debug Cron

```bash
# Chạy tất cả cron
bin/magento cron:run

# Chạy cron group cụ thể
bin/magento cron:run --group="{vendor}_{modulename}"

# Xem lịch sử cron
SELECT * FROM cron_schedule ORDER BY scheduled_at DESC LIMIT 50;

# Xóa lịch sử cron
bin/magento cron:remove
```
