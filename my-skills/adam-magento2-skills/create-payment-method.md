---
name: Create Payment Method
description: Hướng dẫn tạo Payment Method trong Magento 2
---

# Tạo Payment Method trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── config.xml
│   ├── adminhtml/
│   │   └── system.xml
│   └── payment.xml
├── Model/
│   └── Payment/
│       └── {PaymentMethod}.php
├── Gateway/
│   ├── Config/
│   │   └── Config.php
│   ├── Http/
│   │   └── Client.php
│   ├── Request/
│   │   └── AuthorizationRequest.php
│   └── Response/
│       └── ResponseHandler.php
└── view/
    └── frontend/
        ├── layout/
        │   └── checkout_index_index.xml
        └── web/
            └── js/
                └── view/payment/
                    └── {method}.js
```

## 1. Khai báo Payment Method

`etc/payment.xml`

```xml
<?xml version="1.0"?>
<payment xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Payment:etc/payment.xsd">
    <methods>
        <method name="{payment_code}">
            <allow_multiple_address>1</allow_multiple_address>
        </method>
    </methods>
</payment>
```

## 2. Config mặc định

`etc/config.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Store:etc/config.xsd">
    <default>
        <payment>
            <{payment_code}>
                <active>1</active>
                <model>{Vendor}\{ModuleName}\Model\Payment\{PaymentMethod}</model>
                <title>Payment Method Title</title>
                <order_status>pending</order_status>
                <payment_action>authorize_capture</payment_action>
                <allowspecific>0</allowspecific>
                <sort_order>100</sort_order>
            </{payment_code}>
        </payment>
    </default>
</config>
```

## 3. Payment Model

`Model/Payment/{PaymentMethod}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Payment;

use Magento\Payment\Model\Method\AbstractMethod;
use Magento\Quote\Api\Data\CartInterface;

class {PaymentMethod} extends AbstractMethod
{
    protected $_code = '{payment_code}';
    protected $_isOffline = true;
    
    protected $_canAuthorize = true;
    protected $_canCapture = true;
    protected $_canRefund = true;
    protected $_canVoid = true;
    protected $_canUseCheckout = true;
    protected $_canUseInternal = true;

    /**
     * Check if payment method is available
     */
    public function isAvailable(CartInterface $quote = null): bool
    {
        if (!parent::isAvailable($quote)) {
            return false;
        }
        
        // Custom availability logic
        return true;
    }

    /**
     * Authorize payment
     */
    public function authorize(\Magento\Payment\Model\InfoInterface $payment, $amount)
    {
        $order = $payment->getOrder();
        
        // Authorization logic here
        $payment->setTransactionId('txn_' . time());
        $payment->setIsTransactionClosed(false);
        
        return $this;
    }

    /**
     * Capture payment
     */
    public function capture(\Magento\Payment\Model\InfoInterface $payment, $amount)
    {
        // Capture logic here
        $payment->setTransactionId('capture_' . time());
        
        return $this;
    }

    /**
     * Refund payment
     */
    public function refund(\Magento\Payment\Model\InfoInterface $payment, $amount)
    {
        // Refund logic here
        return $this;
    }
}
```

## 4. Admin System Config

`etc/adminhtml/system.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Config:etc/system_file.xsd">
    <system>
        <section id="payment">
            <group id="{payment_code}" translate="label" sortOrder="100" showInDefault="1" showInWebsite="1" showInStore="1">
                <label>Payment Method Title</label>
                
                <field id="active" translate="label" type="select" sortOrder="10" showInDefault="1" showInWebsite="1">
                    <label>Enabled</label>
                    <source_model>Magento\Config\Model\Config\Source\Yesno</source_model>
                </field>
                
                <field id="title" translate="label" type="text" sortOrder="20" showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Title</label>
                </field>
                
                <field id="order_status" translate="label" type="select" sortOrder="30" showInDefault="1" showInWebsite="1">
                    <label>New Order Status</label>
                    <source_model>Magento\Sales\Model\Config\Source\Order\Status\NewStatus</source_model>
                </field>
                
                <field id="allowspecific" translate="label" type="allowspecific" sortOrder="40" showInDefault="1" showInWebsite="1">
                    <label>Payment From Applicable Countries</label>
                    <source_model>Magento\Payment\Model\Config\Source\Allspecificcountries</source_model>
                </field>
                
                <field id="specificcountry" translate="label" type="multiselect" sortOrder="50" showInDefault="1" showInWebsite="1">
                    <label>Payment From Specific Countries</label>
                    <source_model>Magento\Directory\Model\Config\Source\Country</source_model>
                </field>
                
                <field id="sort_order" translate="label" type="text" sortOrder="100" showInDefault="1" showInWebsite="1">
                    <label>Sort Order</label>
                </field>
            </group>
        </section>
    </system>
</config>
```

## 5. Frontend JS Component

`view/frontend/web/js/view/payment/{method}.js`

```javascript
define([
    'Magento_Checkout/js/view/payment/default'
], function (Component) {
    'use strict';

    return Component.extend({
        defaults: {
            template: '{Vendor}_{ModuleName}/payment/{method}'
        },

        getMailingAddress: function () {
            return window.checkoutConfig.payment.{payment_code}.mailingAddress;
        },

        getInstructions: function () {
            return window.checkoutConfig.payment.{payment_code}.instructions;
        }
    });
});
```

## Payment Actions

| Action | Mô tả |
|--------|-------|
| `authorize` | Chỉ authorize, capture sau |
| `authorize_capture` | Authorize và capture cùng lúc |
| `order` | Tạo order transaction |
