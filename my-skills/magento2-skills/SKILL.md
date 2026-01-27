---
name: Magento 2 Development Skills
description: Tập hợp các skills cần thiết cho việc phát triển Magento 2
---

# Magento 2 Development Skills

Đây là tập hợp các hướng dẫn chi tiết cho việc phát triển với Magento 2.

## Danh sách Skills

### Module & Architecture

| Skill | Mô tả |
|-------|-------|
| [create-module.md](./create-module.md) | Tạo module Magento 2 mới với cấu trúc chuẩn |
| [create-controller.md](./create-controller.md) | Tạo Controller (Frontend & Admin) |
| [create-model-repository.md](./create-model-repository.md) | Tạo Model, ResourceModel, Collection và Repository Pattern |

### Customization & Extension

| Skill | Mô tả |
|-------|-------|
| [create-plugin.md](./create-plugin.md) | Tạo Plugin/Interceptor để modify behavior |
| [create-observer.md](./create-observer.md) | Tạo Observer để lắng nghe events |
| [create-product-attribute.md](./create-product-attribute.md) | Tạo Product Attribute (EAV) |

### Database

| Skill | Mô tả |
|-------|-------|
| [create-db-schema.md](./create-db-schema.md) | Tạo database schema với Declarative Schema |

### Admin UI

| Skill | Mô tả |
|-------|-------|
| [create-ui-grid.md](./create-ui-grid.md) | Tạo UI Component Grid trong Admin |
| [create-ui-form.md](./create-ui-form.md) | Tạo UI Component Form trong Admin |
| [create-system-config.md](./create-system-config.md) | Tạo System Configuration trong Admin |
| [create-acl.md](./create-acl.md) | Tạo ACL (Admin Permissions) |

### Frontend

| Skill | Mô tả |
|-------|-------|
| [create-layout-block.md](./create-layout-block.md) | Tạo Layout XML, Block và Template |
| [create-widget.md](./create-widget.md) | Tạo CMS Widget |
| [frontend-javascript.md](./frontend-javascript.md) | RequireJS và KnockoutJS |

### API

| Skill | Mô tả |
|-------|-------|
| [create-rest-api.md](./create-rest-api.md) | Tạo REST API |
| [create-graphql.md](./create-graphql.md) | Tạo GraphQL API |

### CLI & Background Jobs

| Skill | Mô tả |
|-------|-------|
| [create-cli-command.md](./create-cli-command.md) | Tạo CLI Command |
| [create-cron.md](./create-cron.md) | Tạo Cron Job |
| [create-message-queue.md](./create-message-queue.md) | Tạo Message Queue (Async Processing) |

### Payment & Shipping

| Skill | Mô tả |
|-------|-------|
| [create-payment-method.md](./create-payment-method.md) | Tạo Payment Method |
| [create-shipping-method.md](./create-shipping-method.md) | Tạo Shipping Method |

### Communication

| Skill | Mô tả |
|-------|-------|
| [create-email.md](./create-email.md) | Tạo và gửi Email |

### Testing

| Skill | Mô tả |
|-------|-------|
| [unit-testing.md](./unit-testing.md) | Unit Test và Integration Test với PHPUnit |

### Reference

| Skill | Mô tả |
|-------|-------|
| [useful-commands.md](./useful-commands.md) | Các lệnh CLI thường dùng |

---

## Cách sử dụng

1. Đọc skill tương ứng với tác vụ bạn cần thực hiện
2. Thay thế các placeholder như `{Vendor}`, `{ModuleName}`, `{EntityName}` bằng giá trị thực tế
3. Làm theo các bước hướng dẫn

## Naming Conventions

| Loại | Convention | Ví dụ |
|------|------------|-------|
| Vendor Name | PascalCase | `Bss`, `MyCompany` |
| Module Name | PascalCase | `CustomerReview`, `OrderExport` |
| Table Name | lowercase_underscore | `bss_customer_review` |
| Event Name | lowercase_underscore | `customer_login` |
| Config Path | lowercase_underscore | `bss_module/general/enabled` |
| Controller Action | PascalCase | `Index`, `Save`, `Delete` |
| Block Class | PascalCase | `ProductList`, `CustomerInfo` |
