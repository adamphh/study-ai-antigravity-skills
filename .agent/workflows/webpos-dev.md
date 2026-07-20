---
description: Phát triển WebPOS Extension với hướng dẫn từ skills
---

# WebPOS Development Workflow

Khi nhận yêu cầu customize WebPOS, hãy làm theo các bước sau:

## 1. Xác định loại tác vụ

Đọc skill tương ứng trước khi bắt đầu code:

| Tác vụ | Skill file |
|--------|------------|
| Modify method behavior | `my-skills/webpos-skills/create-plugin.md` |
| Thêm method mới | `my-skills/webpos-skills/create-mixin.md` |
| Thêm UI vào page | `my-skills/webpos-skills/create-layout.md` |
| Xử lý event | `my-skills/webpos-skills/create-event.md` |
| Replace class | `my-skills/webpos-skills/create-rewrite.md` |
| Tạo page/feature mới | `my-skills/webpos-skills/create-component-reducer.md` |

## 2. Chọn mechanism phù hợp

Thứ tự ưu tiên:
1. **Plugin** - Modify method (ít conflict nhất)
2. **Mixin** - Thêm method mới
3. **Event** - Execute code tại các điểm
4. **Layout** - Inject UI
5. **Rewrite** - Cuối cùng, khi không có cách khác

## 3. Cấu trúc extension

```
src/extension/{extension_name}/
├── etc/config.js
├── view/
├── service/
├── locales/
└── package.json
```

## 4. Sau khi tạo code

// turbo
```bash
npm run upgrade
```

// turbo
```bash
npm start
```
