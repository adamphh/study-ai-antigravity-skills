---
name: RequireJS and KnockoutJS
description: Hướng dẫn sử dụng RequireJS và KnockoutJS trong Magento 2
---

# RequireJS và KnockoutJS trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
└── view/
    └── frontend/
        ├── requirejs-config.js
        ├── web/
        │   └── js/
        │       ├── {component}.js
        │       └── view/
        │           └── {ko-component}.js
        └── templates/
            └── {template}.phtml
```

## 1. RequireJS Config

`view/frontend/requirejs-config.js`

```javascript
var config = {
    // Map custom modules
    map: {
        '*': {
            '{alias}': '{Vendor}_{ModuleName}/js/{component}',
            'customSlider': '{Vendor}_{ModuleName}/js/slider'
        }
    },
    
    // Paths for external libraries
    paths: {
        'customLib': 'https://cdn.example.com/lib'
    },
    
    // Shim for non-AMD scripts
    shim: {
        'customLib': {
            deps: ['jquery'],
            exports: 'CustomLib'
        }
    },
    
    // Mixins
    config: {
        mixins: {
            'Magento_Checkout/js/view/shipping': {
                '{Vendor}_{ModuleName}/js/view/shipping-mixin': true
            }
        }
    }
};
```

## 2. Simple JS Component

`view/frontend/web/js/{component}.js`

```javascript
define([
    'jquery',
    'mage/translate'
], function ($, $t) {
    'use strict';

    return function (config, element) {
        var options = $.extend({
            delay: 1000,
            message: $t('Default message')
        }, config);

        $(element).on('click', function () {
            alert(options.message);
        });
    };
});
```

### Sử dụng trong Template

```html
<div id="my-element" 
     data-mage-init='{"<alias>": {"delay": 2000, "message": "Custom message"}}'>
    Click me
</div>

<!-- Hoặc dùng script -->
<script type="text/x-magento-init">
{
    "#selector": {
        "{Vendor}_{ModuleName}/js/{component}": {
            "option1": "value1"
        }
    }
}
</script>
```

## 3. jQuery Widget

```javascript
define([
    'jquery',
    'jquery-ui-modules/widget'
], function ($) {
    'use strict';

    $.widget('{vendor}.{widgetName}', {
        options: {
            speed: 500,
            activeClass: 'active'
        },

        _create: function () {
            this._bind();
        },

        _bind: function () {
            this._on({
                'click .item': this._onClick
            });
        },

        _onClick: function (event) {
            $(event.currentTarget).toggleClass(this.options.activeClass);
        },

        // Public method
        refresh: function () {
            this.element.trigger('refresh');
        }
    });

    return $.{vendor}.{widgetName};
});
```

## 4. KnockoutJS UI Component

`view/frontend/web/js/view/{ko-component}.js`

```javascript
define([
    'uiComponent',
    'ko',
    'jquery'
], function (Component, ko, $) {
    'use strict';

    return Component.extend({
        defaults: {
            template: '{Vendor}_{ModuleName}/{template-name}',
            items: [],
            selectedItem: null
        },

        initialize: function () {
            this._super();
            
            // Make observables
            this.items = ko.observableArray(this.items);
            this.selectedItem = ko.observable(this.selectedItem);
            this.isLoading = ko.observable(false);
            
            // Computed observable
            this.itemCount = ko.computed(function () {
                return this.items().length;
            }, this);

            return this;
        },

        selectItem: function (item) {
            this.selectedItem(item);
        },

        loadItems: function () {
            var self = this;
            this.isLoading(true);

            $.ajax({
                url: '/rest/V1/items',
                method: 'GET',
                success: function (response) {
                    self.items(response);
                },
                complete: function () {
                    self.isLoading(false);
                }
            });
        }
    });
});
```

### KnockoutJS Template

`view/frontend/web/template/{template-name}.html`

```html
<div class="ko-component" data-bind="visible: items().length > 0">
    <h3 data-bind="text: $t('Items')"></h3>
    
    <!-- Loading indicator -->
    <div data-bind="visible: isLoading()">Loading...</div>
    
    <!-- Items list -->
    <ul data-bind="foreach: items">
        <li data-bind="text: name, click: $parent.selectItem.bind($parent, $data)"></li>
    </ul>
    
    <!-- Selected item -->
    <div data-bind="if: selectedItem()">
        <p>Selected: <span data-bind="text: selectedItem().name"></span></p>
    </div>
    
    <!-- Item count -->
    <p>Total: <span data-bind="text: itemCount()"></span> items</p>
</div>
```

### Sử dụng Component

```html
<div data-bind="scope: 'my-component'">
    <!-- ko template: getTemplate() --><!-- /ko -->
</div>

<script type="text/x-magento-init">
{
    "*": {
        "Magento_Ui/js/core/app": {
            "components": {
                "my-component": {
                    "component": "{Vendor}_{ModuleName}/js/view/{ko-component}",
                    "items": []
                }
            }
        }
    }
}
</script>
```

## 5. Mixin (Extend existing JS)

`view/frontend/web/js/view/shipping-mixin.js`

```javascript
define([], function () {
    'use strict';

    return function (originalComponent) {
        return originalComponent.extend({
            defaults: {
                customOption: 'value'
            },

            initialize: function () {
                this._super();
                console.log('Mixin initialized');
                return this;
            },

            // Override method
            selectShippingMethod: function (shippingMethod) {
                console.log('Custom logic before');
                this._super(shippingMethod);
                console.log('Custom logic after');
            }
        });
    };
});
```

## Useful Magento JS Libraries

| Module | Mô tả |
|--------|-------|
| `mage/translate` | Translation helper `$t()` |
| `mage/url` | URL builder |
| `mage/storage` | AJAX helper |
| `Magento_Customer/js/customer-data` | Customer section data |
| `Magento_Ui/js/modal/modal` | Modal dialogs |
| `Magento_Ui/js/modal/confirm` | Confirmation dialogs |
