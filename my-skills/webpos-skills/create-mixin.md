---
name: WebPOS Mixin
description: Hướng dẫn tạo Mixin để thêm method vào class trong WebPOS
---

# WebPOS Mixin Mechanism

Mixin cho phép **thêm method mới** vào một class từ `core` hoặc `module khác`.

## Sự khác biệt với Plugin

| Mixin | Plugin |
|-------|--------|
| **Thêm** method mới | **Modify** method có sẵn |
| Method chưa tồn tại | Method đã tồn tại |

## Đăng ký Mixin

`etc/config.js`

```js
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class MyExtensionConfig extends ModuleConfigAbstract {
    module = ['myextension'];
    
    mixin = {
        component: {
            MenuComponent: {
                // Thêm instance method
                setOrder: function(order) {
                    this.order = order;
                    return this;
                },
                
                getOrder: function() {
                    return this.order;
                },
                
                calculateTotal: function(items) {
                    return items.reduce((sum, item) => sum + item.price, 0);
                },
                
                // Thêm static methods
                static: {
                    plus: function(a, b) {
                        return a + b;
                    },
                    
                    formatCurrency: function(amount) {
                        return '$' + amount.toFixed(2);
                    }
                }
            }
        },
        
        service: {
            OrderService: {
                // Thêm method vào service
                validateOrder: function(order) {
                    return order.items && order.items.length > 0;
                }
            }
        }
    };
}

export default (new MyExtensionConfig());
```

## Các loại class có thể mixin

| Type | Ví dụ |
|------|-------|
| `service` | UserService, OrderService |
| `resource_model` | CustomerResourceModel |
| `repository` | ProductRepository |
| `container` | LoginContainer |
| `component` | MenuComponent |
| `data_resource` | ConfigDataResource |

## Sử dụng method đã mixin

```js
// Sau khi mixin, có thể gọi method mới
const component = ComponentFactory.get(MenuComponent);
component.setOrder(5);
console.log(component.getOrder()); // 5

// Static method
const result = MenuComponent.plus(1, 2); // 3
```

## Khi nào dùng Mixin?

- Thêm helper methods vào class có sẵn
- Thêm logic mới không modify code gốc
- Extend functionality của core class
