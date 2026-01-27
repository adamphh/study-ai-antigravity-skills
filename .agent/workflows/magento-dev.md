---
description: Phát triển module Magento 2 với hướng dẫn từ skills
---

# Magento 2 Development Workflow

Khi nhận yêu cầu phát triển Magento 2, hãy làm theo các bước sau:

## 1. Xác định loại tác vụ

Đọc skill tương ứng trước khi bắt đầu code:

| Tác vụ | Skill file |
|--------|------------|
| Tạo module mới | `Source/my-skills/magento2-skills/create-module.md` |
| Tạo Controller | `Source/my-skills/magento2-skills/create-controller.md` |
| Tạo Model/Repository | `Source/my-skills/magento2-skills/create-model-repository.md` |
| Tạo Plugin | `Source/my-skills/magento2-skills/create-plugin.md` |
| Tạo Observer | `Source/my-skills/magento2-skills/create-observer.md` |
| Tạo Database Schema | `Source/my-skills/magento2-skills/create-db-schema.md` |
| Tạo Admin Grid | `Source/my-skills/magento2-skills/create-ui-grid.md` |
| Tạo Admin Form | `Source/my-skills/magento2-skills/create-ui-form.md` |
| Tạo System Config | `Source/my-skills/magento2-skills/create-system-config.md` |
| Tạo ACL | `Source/my-skills/magento2-skills/create-acl.md` |
| Tạo REST API | `Source/my-skills/magento2-skills/create-rest-api.md` |
| Tạo GraphQL | `Source/my-skills/magento2-skills/create-graphql.md` |
| Tạo CLI Command | `Source/my-skills/magento2-skills/create-cli-command.md` |
| Tạo Cron Job | `Source/my-skills/magento2-skills/create-cron.md` |
| Tạo Email | `Source/my-skills/magento2-skills/create-email.md` |
| Tạo Payment Method | `Source/my-skills/magento2-skills/create-payment-method.md` |
| Tạo Shipping Method | `Source/my-skills/magento2-skills/create-shipping-method.md` |
| Tạo Widget | `Source/my-skills/magento2-skills/create-widget.md` |
| Tạo Layout/Block | `Source/my-skills/magento2-skills/create-layout-block.md` |
| Tạo Product Attribute | `Source/my-skills/magento2-skills/create-product-attribute.md` |
| Message Queue | `Source/my-skills/magento2-skills/create-message-queue.md` |
| Frontend JS | `Source/my-skills/magento2-skills/frontend-javascript.md` |
| Unit Testing | `Source/my-skills/magento2-skills/unit-testing.md` |

## 2. Thay thế placeholders

Khi sử dụng code từ skills, thay thế các placeholder:

- `{Vendor}` → Tên vendor (VD: `Bss`, `Custom`)
- `{ModuleName}` → Tên module (VD: `CustomerReview`)
- `{EntityName}` → Tên entity (VD: `Review`, `Order`)
- `{entity_name}` → Tên entity snake_case (VD: `customer_review`)
- `{table_name}` → Tên bảng (VD: `bss_customer_review`)

## 3. Chạy lệnh sau khi tạo code

// turbo
```bash
bin/magento setup:upgrade
```

// turbo
```bash
bin/magento setup:di:compile
```

// turbo
```bash
bin/magento cache:clean
```
