---
name: WebPOS Plugin
description: Hướng dẫn tạo Plugin để modify method trong WebPOS
---

# WebPOS Plugin Mechanism

Plugin cho phép modify một method của class từ `core` hoặc `module khác`.

## Cấu trúc

```
src/extension/{extension_name}/
├── etc/
│   └── config.js          # Đăng ký plugin
└── ...
```

## Đăng ký Plugin

`etc/config.js`

```js
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class MyExtensionConfig extends ModuleConfigAbstract {
    module = ['myextension'];
    
    plugin = {
        component: {
            MenuComponent: {
                // method: plugins
                changeRoute: {
                    // plugin_name: plugin_config
                    myPlugin: {
                        sortOrder: 20,
                        disabled: false,
                        
                        // Before plugin - modify arguments
                        before: (item) => {
                            console.log('Before:', item.path);
                            // Có thể modify item trước khi method chạy
                            return item;
                        },
                        
                        // Around plugin - wrap method
                        around: (proceed, item) => {
                            console.log('Around Before');
                            let result = proceed(item); // Gọi method gốc
                            console.log('Around After');
                            return result;
                        },
                        
                        // After plugin - modify result
                        after: (result, item) => {
                            console.log('After:', result);
                            // Có thể modify result trước khi return
                            return result;
                        },
                    },
                },
            }
        }
    };
}

export default (new MyExtensionConfig());
```

## Các loại class có thể plugin

| Type | Factory | Ví dụ |
|------|---------|-------|
| `service` | ServiceFactory | UserService |
| `resource_model` | ResourceModelFactory | CustomerResourceModel |
| `repository` | RepositoryFactory | ProductRepository |
| `container` | ContainerFactory | LoginContainer |
| `component` | ComponentFactory | MenuComponent |
| `data_resource` | DataResourceFactory | ConfigDataResource |

## Xác định loại class

Tìm Factory type trong source code:

```js
// Đây là component vì dùng ComponentFactory
const component = ComponentFactory.get(MenuComponent);

// Đây là service vì dùng ServiceFactory
const service = ServiceFactory.get(UserService);
```

## Plugin Order

Plugin chạy theo thứ tự `sortOrder` (số nhỏ chạy trước):

1. **before** plugins chạy trước (modify arguments)
2. **around** plugins wrap method gốc
3. Method gốc chạy
4. **after** plugins chạy sau (modify result)

## Lưu ý quan trọng

- Dùng `this` để reference đến object gốc (không cần `$subject` như Magento)
- Mỗi plugin (before/around/after) là một function
- `disabled: true` để tạm tắt plugin
