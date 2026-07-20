---
description: Phát triển ReactJS với hướng dẫn từ skills
---

# ReactJS Development Workflow

Khi nhận yêu cầu phát triển React, hãy làm theo các bước sau:

## 1. Xác định loại tác vụ

Đọc skill tương ứng trước khi bắt đầu code:

| Tác vụ | Skill file |
|--------|------------|
| Class Component | `my-skills/reactjs-skills/class-component-basics.md` |
| Function Component + Hooks | `my-skills/reactjs-skills/function-component-hooks.md` |
| Custom Hook | `my-skills/reactjs-skills/custom-hooks.md` |
| React Router | `my-skills/reactjs-skills/react-router.md` |
| Context/State Management | `my-skills/reactjs-skills/context-state-management.md` |
| Form Handling | `my-skills/reactjs-skills/form-handling.md` |
| API Calls | `my-skills/reactjs-skills/api-calls.md` |
| Performance Optimization | `my-skills/reactjs-skills/performance-optimization.md` |
| Error Handling | `my-skills/reactjs-skills/error-handling.md` |
| Component Patterns | `my-skills/reactjs-skills/component-patterns.md` |
| Testing | `my-skills/reactjs-skills/testing.md` |

## 2. Quy tắc chung

### Ưu tiên Function Component
- Dùng Function Component + Hooks cho code mới
- Chỉ dùng Class Component khi cần Error Boundary

### Cấu trúc thư mục
```
src/
├── components/    # Reusable components
├── hooks/         # Custom hooks
├── contexts/      # Context providers
├── pages/         # Page components
├── services/      # API calls
└── utils/         # Helper functions
```

### Naming conventions
- Components: `PascalCase.jsx`
- Hooks: `useCamelCase.js`
- Utils: `camelCase.js`

## 3. Sau khi tạo component

// turbo
```bash
npm run lint
```

// turbo
```bash
npm run test
```
