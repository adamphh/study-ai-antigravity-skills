Project <domain_name>
---

* Magento Version: 
* POS Initialized Version: 
* POS Current Version: 
 
## System Design
- docs/SYSTEM.md – High-level system architecture
- docs/INVARIANTS.md – Non-negotiable system rules
- docs/SYNC_SPEC.md – POS sync strategy (snapshot + delta)

## Developer Guide
- docs/dev_setup.md – Setting up a development environment
- docs/dev_guide.md – Overview of the codebase and development practices
- docs/antigravity_user_guide.md – Hướng dẫn sử dụng Antigravity AI Engine hiệu quả
- docs/api_spec.md – API specifications for POS and Magento communication
- docs/testing_guide.md – Testing strategies and guidelines
- docs/deployment_guide.md – Deployment procedures and best practices
- docs/performance_optimization.md – Tips for optimizing performance
- docs/contributing.md – Guidelines for contributing to the project

## User Guide
- docs/user_guide.md – Instructions for end-users on how to use the POS system
- docs/faq.md – Frequently Asked Questions
- docs/troubleshooting.md – Common issues and their solutions

# How to use skills?
1. Tham khảo trực tiếp khi code
Mở file skill tương ứng khi bạn cần implement một tính năng cụ thể. Ví dụ:
    - Cần tạo Controller Magento 2? → Mở create-controller.md
    - Cần fetch data trong React? → Mở api-calls.md

2. Sử dụng như Agent Skill (Workflow)
Cấu hình Antigravity để tự động đọc các skills này
# .agent/workflows/magento-dev.md

# Cách sử dụng:
    - Dùng slash command: 
        - Gõ /magento-dev khi cần tạo code Magento
        - Gõ /react-dev trong chat khi cần tạo code reactjs
        - Gõ /webpos-dev - Phát triển WebPOS Extension
        - Gõ /skills để liệt kê ra các skills hiện có
    - Tự động: Khi bạn yêu cầu tôi tạo code Magento 2 hoặc React, tôi sẽ tự động: 
        - Đọc skill file tương ứng
        - Áp dụng patterns và best practices từ skill
        - Thay thế placeholders bằng giá trị thực tế
        - Các lệnh CLI có // turbo sẽ tự động chạy không cần xác nhận

3. Hỏi tôi trực tiếp
Khi cần, bạn có thể mention file skill và yêu cầu tôi:

    - "@create-controller.md Tạo controller cho trang checkout"
    - "Áp dụng pattern trong @component-patterns.md để refactor component này"

| Hiện tại | Đề xuất |
|----------|---------|
| /magento-dev | /m2 hoặc /mage |
| /react-dev | /react |
| /webpos-dev | /pos |
| /skills | /skills (giữ nguyên) |