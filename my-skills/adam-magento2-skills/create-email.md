---
name: Create Email Template
description: Hướng dẫn tạo và gửi Email trong Magento 2
---

# Tạo Email Template trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   └── email_templates.xml
├── Model/
│   └── Email/
│       └── Sender.php
└── view/
    └── frontend/
        └── email/
            └── {template_name}.html
```

## 1. Đăng ký Email Template

`etc/email_templates.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Email:etc/email_templates.xsd">
    
    <template id="{vendor}_{modulename}_{template_id}"
              label="Template Label"
              file="{template_name}.html"
              type="html"
              module="{Vendor}_{ModuleName}"
              area="frontend"/>
              
</config>
```

## 2. Template HTML

`view/frontend/email/{template_name}.html`

```html
<!--@subject {{trans "Email Subject - %store_name" store_name=$store.frontend_name}} @-->

{{template config_path="design/email/header_template"}}

<table>
    <tr class="email-intro">
        <td>
            <p class="greeting">{{trans "Dear %customer_name," customer_name=$customer_name}}</p>
            <p>{{trans "Your order #%order_id has been placed successfully." order_id=$order.increment_id}}</p>
        </td>
    </tr>
    <tr class="email-information">
        <td>
            {{depend custom_data}}
            <p>{{trans "Custom Data: %data" data=$custom_data}}</p>
            {{/depend}}
            
            {{if show_details}}
            <p>Details section</p>
            {{/if}}
        </td>
    </tr>
</table>

{{template config_path="design/email/footer_template"}}
```

## 3. Email Sender Class

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Email;

use Magento\Framework\App\Area;
use Magento\Framework\Mail\Template\TransportBuilder;
use Magento\Framework\Translate\Inline\StateInterface;
use Magento\Store\Model\StoreManagerInterface;
use Psr\Log\LoggerInterface;

class Sender
{
    private TransportBuilder $transportBuilder;
    private StateInterface $inlineTranslation;
    private StoreManagerInterface $storeManager;
    private LoggerInterface $logger;

    public function __construct(
        TransportBuilder $transportBuilder,
        StateInterface $inlineTranslation,
        StoreManagerInterface $storeManager,
        LoggerInterface $logger
    ) {
        $this->transportBuilder = $transportBuilder;
        $this->inlineTranslation = $inlineTranslation;
        $this->storeManager = $storeManager;
        $this->logger = $logger;
    }

    public function send(
        string $toEmail,
        string $toName,
        array $templateVars,
        int $storeId = null
    ): bool {
        try {
            $storeId = $storeId ?? $this->storeManager->getStore()->getId();
            
            $this->inlineTranslation->suspend();
            
            $transport = $this->transportBuilder
                ->setTemplateIdentifier('{vendor}_{modulename}_{template_id}')
                ->setTemplateOptions([
                    'area' => Area::AREA_FRONTEND,
                    'store' => $storeId
                ])
                ->setTemplateVars($templateVars)
                ->setFromByScope('general')  // or 'sales', 'support', 'custom1', 'custom2'
                ->addTo($toEmail, $toName)
                ->getTransport();
            
            $transport->sendMessage();
            
            $this->inlineTranslation->resume();
            
            return true;
        } catch (\Exception $e) {
            $this->logger->error('Email sending failed: ' . $e->getMessage());
            $this->inlineTranslation->resume();
            return false;
        }
    }
}
```

## 4. Sử dụng Email Sender

```php
$this->emailSender->send(
    'customer@example.com',
    'Customer Name',
    [
        'customer_name' => 'John Doe',
        'order' => $order,
        'custom_data' => 'Some value',
        'store' => $this->storeManager->getStore()
    ]
);
```

## Template Directives

| Directive | Mô tả |
|-----------|-------|
| `{{var variable}}` | Output variable |
| `{{trans "text"}}` | Translatable text |
| `{{depend variable}}...{{/depend}}` | Hiển thị nếu variable có giá trị |
| `{{if condition}}...{{/if}}` | Điều kiện |
| `{{template config_path="..."}}` | Include template khác |
| `{{store url="path"}}` | Store URL |

## Config cho Email Sender

`etc/config.xml`

```xml
<config>
    <default>
        <trans_email>
            <ident_custom1>
                <email>custom@example.com</email>
                <name>Custom Sender</name>
            </ident_custom1>
        </trans_email>
    </default>
</config>
```
