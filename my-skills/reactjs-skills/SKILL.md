---
name: ReactJS Development Skills
description: Tập hợp các skills cần thiết cho việc phát triển React
---

# ReactJS Development Skills

Đây là tập hợp các hướng dẫn chi tiết cho việc phát triển với ReactJS, bao gồm cả Class Components và Function Components với Hooks.

## Danh sách Skills

### Class Component

| Skill | Mô tả |
|-------|-------|
| [class-component-basics.md](./class-component-basics.md) | Class Component cơ bản, Lifecycle, State |

### Function Component với Hooks

| Skill | Mô tả |
|-------|-------|
| [function-component-hooks.md](./function-component-hooks.md) | useState, useEffect, useRef, useMemo, useCallback, useReducer |
| [custom-hooks.md](./custom-hooks.md) | Tạo Custom Hooks tái sử dụng |

### State Management

| Skill | Mô tả |
|-------|-------|
| [context-state-management.md](./context-state-management.md) | Context API cho cả Class và Function Components |

### Routing

| Skill | Mô tả |
|-------|-------|
| [react-router.md](./react-router.md) | React Router, navigation, protected routes |

### Forms & Data

| Skill | Mô tả |
|-------|-------|
| [form-handling.md](./form-handling.md) | Xử lý Form (Controlled/Uncontrolled) |
| [api-calls.md](./api-calls.md) | Gọi API, Data fetching |

### Patterns & Best Practices

| Skill | Mô tả |
|-------|-------|
| [component-patterns.md](./component-patterns.md) | HOC, Render Props, Compound Components |
| [performance-optimization.md](./performance-optimization.md) | memo, useMemo, useCallback, lazy loading |
| [error-handling.md](./error-handling.md) | Error Boundaries, try/catch |

### Testing

| Skill | Mô tả |
|-------|-------|
| [testing.md](./testing.md) | Testing với React Testing Library |

---

## So sánh Class vs Function Component

| Tính năng | Class Component | Function Component |
|-----------|-----------------|-------------------|
| State | `this.state`, `setState` | `useState` hook |
| Lifecycle | `componentDidMount`, etc. | `useEffect` hook |
| Refs | `createRef()` | `useRef()` |
| Context | `contextType`, `Consumer` | `useContext()` |
| Performance | `PureComponent`, `shouldComponentUpdate` | `React.memo`, `useMemo` |
| Error Boundary | ✅ Supported | ❌ Không hỗ trợ |

---

## Khi nào dùng Class Component?

- Cần Error Boundaries (bắt buộc dùng Class)
- Maintain legacy codebase

## Khi nào dùng Function Component?

- Project mới (khuyến nghị)
- Cần sử dụng Hooks
- Code ngắn gọn, dễ đọc hơn
- Performance tốt hơn (không có overhead của class)

---

## Cấu trúc thư mục khuyến nghị

```
src/
├── components/           # Reusable components
│   ├── Button/
│   │   ├── Button.jsx
│   │   ├── Button.test.jsx
│   │   └── index.js
│   └── ...
├── hooks/               # Custom hooks
│   ├── useFetch.js
│   └── useAuth.js
├── contexts/            # Context providers
│   ├── AuthContext.jsx
│   └── ThemeContext.jsx
├── pages/               # Page components
│   ├── Home.jsx
│   └── About.jsx
├── services/            # API calls
│   └── api.js
└── utils/               # Helper functions
    └── helpers.js
```
