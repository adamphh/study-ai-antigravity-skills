---
name: Local Development Skills
description: Tập hợp tất cả các kỹ năng và quy trình chuẩn phục vụ cho việc phát triển và customize Magento 2, ReactJS và WebPOS của dự án.
---

# Local Development Skills

Chào mừng đến với hệ thống Kỹ năng của dự án. Bộ kỹ năng này được thiết kế để định hình hành vi và chuẩn hóa code do AI sinh ra, giúp bạn thực hiện công việc phát triển nhanh chóng và an toàn.

## Danh sách Kỹ năng chính

### 1. [Magento 2 Development Skills](file:///mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/SKILL.md)
* Hướng dẫn chi tiết tạo Module, Controller, Model/Repository, CLI, Cron, APIs, Payment, Shipping, Email, Unit Testing.
* Đi kèm kịch bản tự động hóa sinh Data Interface/Model và cơ chế bảo vệ core modules.

### 2. [ReactJS Development Skills](file:///mnt/projects/study-ai-antigravity-skills/my-skills/reactjs-skills/SKILL.md)
* Quy chuẩn lập trình ReactJS, cấu trúc component, hooks, form, API calls, tối ưu hiệu năng.

### 3. [WebPOS Customization Skills](file:///mnt/projects/study-ai-antigravity-skills/my-skills/webpos-skills/SKILL.md)
* Các cơ chế mở rộng POS framework thông qua Plugin (can thiệp method), Mixin (thêm method), Event/Observer, Layout UI Injection và Rewrite.

### 4. [Init Project Skill](file:///mnt/projects/study-ai-antigravity-skills/my-skills/init-project/SKILL.md)
* Tự động hóa thiết lập dự án mới bằng cách liên kết thư mục `.agent` và sao chép thư mục `docs/` template.

---

## Nguyên tắc cốt lõi khi làm việc

1. **Tuyệt đối không sửa trực tiếp Core Files:** Luôn kiểm tra [protected-modules.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/references/protected-modules.md) trước khi sửa code backend. Đối với WebPOS client, tuân thủ đúng thứ tự ưu tiên mở rộng (Plugin -> Mixin -> Event -> Layout -> Rewrite).
2. **Kế hoạch trước khi thực hiện (Planning Mode):** Luôn tạo tài liệu kế hoạch triển khai tại thư mục `Plans/` và nhận sự phê duyệt của lập trình viên trước khi sửa đổi source code.
3. **Tận dụng Script Tự động hóa:** Tiết kiệm thời gian và đảm bảo chính xác bằng cách chạy script tự sinh Data Interface & Model tại [data-interface-model.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/references/data-interface-model.md).
