---
name: WebPOS Layout
description: Hướng dẫn sử dụng Layout để thêm UI vào WebPOS
---

# WebPOS Layout Mechanism

Layout cho phép thêm UI vào screen/page thông qua các customize point.

## Customize Point trong Core

Core component tạo customize point bằng `layout()`:

```jsx
import layout from "../../../framework/Layout";

export class Login extends CoreComponent {
    static className = 'Login';

    template() {
        return (
            <Fragment>
                <form className="wrapper-login">
                    <div className="form-login">
                        {/* Customize point: cho phép thêm UI trước title */}
                        {layout('user')('login_title_before')()(this)}
                        
                        <h2 className="page-title">{this.props.t('Login')}</h2>
                        
                        {/* Customize point: cho phép thêm UI sau title */}
                        {layout('user')('login_title_after')()(this)}
                        
                        {/* Form fields */}
                    </div>
                </form>
            </Fragment>
        );
    }
}
```

## Layout Syntax

```js
layout('user')('login_title_before')()(this)
```

| Part | Mô tả |
|------|-------|
| `layout('user')` | Layout function cho namespace `user` |
| `('login_title_before')` | Layout point name |
| `()` | Options (thường để trống) |
| `(this)` | Pass component context |

Có thể viết gọn: `layout('user.login_title_before')()(this)`

## Thêm UI qua Layout

`etc/config.js`

```js
import ModuleConfigAbstract from "../../ModuleConfigAbstract";
import MyCustomComponent from "../view/MyCustomComponent";

class MyExtensionConfig extends ModuleConfigAbstract {
    module = ['myextension'];
    
    layout = {
        user: {
            // Thêm UI vào login_title_before
            login_title_before: [
                // Plain text
                'STATUS: ',
                
                // Function nhận component context
                function(component) {
                    return component.state.active ? 'Active' : 'Inactive';
                },
                
                // React component
                <span className="badge">New</span>,
                
                // Custom component
                <MyCustomComponent />,
            ],
            
            // Thêm UI vào điểm khác
            login_form_after: [
                function(component) {
                    return (
                        <div className="extra-options">
                            <a href="#">Forgot Password?</a>
                        </div>
                    );
                }
            ]
        },
        
        // Namespace khác
        checkout: {
            cart_items_after: [
                function(component) {
                    return <TotalSummary cart={component.props.cart} />;
                }
            ]
        }
    };
}

export default (new MyExtensionConfig());
```

## Layout với Component phức tạp

```js
import React from 'react';

// Component riêng
const CustomBanner = ({ component }) => {
    const { t } = component.props;
    
    return (
        <div className="promo-banner">
            <h3>{t('Special Offer')}</h3>
            <p>{t('Get 20% off today!')}</p>
        </div>
    );
};

// Trong config
layout = {
    checkout: {
        header_after: [
            function(component) {
                return <CustomBanner component={component} />;
            }
        ]
    }
};
```

## Kết quả

Layout function trả về array các elements đã được render:

```js
// Input
layout('user')('login_title_before')()(this)

// Output (sau khi xử lý)
['STATUS: ', 'Active', <span>New</span>, <MyCustomComponent />]
```
