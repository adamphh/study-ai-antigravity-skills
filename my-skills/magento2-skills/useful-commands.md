---
name: Magento 2 Useful Commands
description: Tổng hợp các lệnh CLI thường dùng trong Magento 2
---

# Các lệnh CLI thường dùng trong Magento 2

## Cache Management

```bash
# Xóa cache
bin/magento cache:clean

# Flush cache (bao gồm external cache như Redis)
bin/magento cache:flush

# Xem trạng thái cache
bin/magento cache:status

# Disable/Enable cache type
bin/magento cache:disable full_page
bin/magento cache:enable full_page
```

## Module Management

```bash
# Xem danh sách module
bin/magento module:status

# Enable/Disable module
bin/magento module:enable Vendor_ModuleName
bin/magento module:disable Vendor_ModuleName

# Xóa module khỏi database
bin/magento module:uninstall Vendor_ModuleName
```

## Setup & Upgrade

```bash
# Upgrade database schema và data
bin/magento setup:upgrade

# Compile DI (bắt buộc cho production)
bin/magento setup:di:compile

# Deploy static content
bin/magento setup:static-content:deploy -f
bin/magento setup:static-content:deploy en_US nl_NL -f

# Dry-run để xem SQL sẽ chạy
bin/magento setup:upgrade --dry-run=1
```

## Index Management

```bash
# Reindex tất cả
bin/magento indexer:reindex

# Reindex cụ thể
bin/magento indexer:reindex catalog_product_price

# Xem trạng thái
bin/magento indexer:status

# Set mode (realtime/schedule)
bin/magento indexer:set-mode schedule
```

## Developer Mode

```bash
# Xem mode hiện tại
bin/magento deploy:mode:show

# Chuyển mode
bin/magento deploy:mode:set developer
bin/magento deploy:mode:set production
```

## Database

```bash
# Export config từ database ra file
bin/magento app:config:dump

# Import config từ file vào database
bin/magento app:config:import

# Generate whitelist cho declarative schema
bin/magento setup:db-declaration:generate-whitelist --module-name=Vendor_ModuleName
```

## Cron

```bash
# Chạy cron manually
bin/magento cron:run

# Xóa cron schedule
bin/magento cron:remove
```

## Maintenance

```bash
# Enable/Disable maintenance mode
bin/magento maintenance:enable
bin/magento maintenance:disable

# Cho phép IP truy cập khi maintenance
bin/magento maintenance:enable --ip=192.168.1.1
```

## Admin

```bash
# Tạo admin user
bin/magento admin:user:create --admin-user="admin" --admin-password="admin123" --admin-email="admin@example.com" --admin-firstname="Admin" --admin-lastname="User"

# Unlock admin account
bin/magento admin:user:unlock admin
```

## Quick Commands Combo

```bash
# Development reload (thường dùng)
bin/magento cache:clean && bin/magento setup:upgrade

# Production deploy
bin/magento maintenance:enable && \
bin/magento setup:upgrade && \
bin/magento setup:di:compile && \
bin/magento setup:static-content:deploy -f && \
bin/magento cache:flush && \
bin/magento maintenance:disable
```
