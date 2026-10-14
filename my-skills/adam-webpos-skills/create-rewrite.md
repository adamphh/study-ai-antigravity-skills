---
name: WebPOS Rewrite
description: Hướng dẫn Rewrite class trong WebPOS
---

# WebPOS Rewrite Mechanism

Rewrite cho phép thay thế hoàn toàn một class từ `core` hoặc `module khác`.

## Khi nào dùng Rewrite?

| Mechanism | Use Case |
|-----------|----------|
| **Plugin** | Modify một method cụ thể |
| **Mixin** | Thêm method mới |
| **Rewrite** | Thay đổi lớn, cần override nhiều methods |

> ⚠️ **Cảnh báo**: Rewrite có thể gây conflict. Ưu tiên dùng Plugin/Mixin trước.

## Đăng ký Rewrite

`etc/config.js`

```js
import rewriteMenu from "../view/menu";
import rewriteOrderService from "../service/OrderService";
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class MyExtensionConfig extends ModuleConfigAbstract {
    module = ['myextension'];
    
    rewrite = {
        service: {
            OrderService: rewriteOrderService
        },
        container: {
            // LoginContainer: rewriteLogin
        },
        component: {
            MenuComponent: rewriteMenu
        },
    };
}

export default (new MyExtensionConfig());
```

## Implement Rewrite - Component/Class

`view/menu.js`

```js
import React, { Fragment } from "react";

/**
 * Rewrite MenuComponent
 *
 * @param {MenuComponent} MenuComponent - Class gốc
 * @returns {class} - Class mới extend từ class gốc
 */
export default function(MenuComponent) {
    return class RewriteMenuComponent extends MenuComponent {
        
        // Override method
        template() {
            let originalTemplate = super.template();
            return (
                <Fragment>
                    <div className="custom-header">Hello World!</div>
                    {originalTemplate}
                </Fragment>
            );
        }
        
        // Override với logic hoàn toàn mới
        handleClick(item) {
            console.log('Custom click handler');
            // Có thể gọi super nếu cần
            // super.handleClick(item);
        }
        
        // Thêm method mới
        customMethod() {
            return 'Custom';
        }
    }
}
```

## Implement Rewrite - Epic (Function)

Epic là **Function** không phải Class, cần xử lý khác:

`epic/LocationEpic.js`

```js
import { Observable } from "rxjs/Rx";
import UserConstant from "../../../view/constant/UserConstant";
import LocationAction from "../../../view/action/LocationAction";

export default function() {
    // Epic là function, không phải class
    let LocationEpic = function(action$) {
        let LocationService = require("../../../service/LocationService").default;
        
        return action$.ofType(UserConstant.USER_ASSIGN_POS)
            .mergeMap(action => Observable.from(
                LocationService.assignPos(
                    action.posId, 
                    action.locationId, 
                    action.currentStaffId
                ))
                .map((response) => {
                    console.log('Custom response handling:', response);
                    return LocationAction.assignPosResponse();
                })
                .catch((error) => {
                    return Observable.of(LocationAction.assignPosError(error.message));
                })
            );
    };
    
    // Quan trọng: set className cho Epic
    LocationEpic.className = "LocationEpic";
    
    return LocationEpic;
}
```

## Các loại class có thể rewrite

| Type | Ví dụ |
|------|-------|
| `service` | UserService, OrderService |
| `resource_model` | CustomerResourceModel |
| `repository` | ProductRepository |
| `epic` | LocationEpic, OrderEpic |
| `container` | LoginContainer |
| `component` | MenuComponent |
| `data_resource` | ConfigDataResource |

## Best Practices

1. **Ưu tiên Plugin/Mixin** trước khi dùng Rewrite
2. **Luôn extend** từ class gốc (dùng `super`)
3. **Gọi super** trong methods để giữ logic gốc
4. **Set className** cho Epic rewrites
5. **Test kỹ** vì rewrite có thể break functionality
