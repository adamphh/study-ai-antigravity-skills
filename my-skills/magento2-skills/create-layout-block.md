---
name: Create Layout XML and Block
description: Hướng dẫn tạo Layout XML, Block và Template trong Magento 2
---

# Tạo Layout XML, Block và Template

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── Block/
│   └── {BlockName}.php
└── view/
    └── frontend/ (hoặc adminhtml/)
        ├── layout/
        │   └── {route_id}_{controller}_{action}.xml
        └── templates/
            └── {template_name}.phtml
```

## 1. Layout XML

`view/frontend/layout/{route_id}_{controller}_{action}.xml`

```xml
<?xml version="1.0"?>
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    
    <!-- Page Title -->
    <head>
        <title>Page Title</title>
        <css src="{Vendor}_{ModuleName}::css/custom.css"/>
        <script src="{Vendor}_{ModuleName}::js/custom.js"/>
    </head>
    
    <body>
        <!-- Reference existing container -->
        <referenceContainer name="content">
            <!-- Add block with template -->
            <block class="{Vendor}\{ModuleName}\Block\{BlockName}"
                   name="{vendor}.{modulename}.{blockname}"
                   template="{Vendor}_{ModuleName}::{template_name}.phtml">
                <!-- Child block -->
                <block class="Magento\Framework\View\Element\Template"
                       name="{vendor}.{modulename}.child"
                       template="{Vendor}_{ModuleName}::child.phtml"/>
            </block>
        </referenceContainer>
        
        <!-- Reference existing block -->
        <referenceBlock name="product.info.main">
            <action method="setTemplate">
                <argument name="template" xsi:type="string">{Vendor}_{ModuleName}::custom_product.phtml</argument>
            </action>
        </referenceBlock>
        
        <!-- Remove block -->
        <referenceBlock name="block.to.remove" remove="true"/>
        
        <!-- Move block -->
        <move element="block.name" destination="new.container" after="-"/>
    </body>
</page>
```

## 2. Block Class

`Block/{BlockName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Block;

use Magento\Framework\View\Element\Template;
use Magento\Framework\View\Element\Template\Context;

class {BlockName} extends Template
{
    protected $_template = '{Vendor}_{ModuleName}::{template_name}.phtml';

    public function __construct(
        Context $context,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * Get custom data for template
     */
    public function getCustomData(): array
    {
        return [
            'title' => 'Custom Title',
            'items' => ['Item 1', 'Item 2', 'Item 3']
        ];
    }

    /**
     * Get formatted price
     */
    public function getFormattedPrice(float $price): string
    {
        return $this->_storeManager->getStore()->getBaseCurrency()
            ->formatPrecision($price, 2);
    }
}
```

## 3. Template (PHTML)

`view/frontend/templates/{template_name}.phtml`

```php
<?php
/**
 * @var \{Vendor}\{ModuleName}\Block\{BlockName} $block
 */
?>
<div class="custom-block">
    <h2><?= $block->escapeHtml(__('Title')) ?></h2>
    
    <?php $data = $block->getCustomData(); ?>
    <ul>
        <?php foreach ($data['items'] as $item): ?>
            <li><?= $block->escapeHtml($item) ?></li>
        <?php endforeach; ?>
    </ul>
    
    <!-- Render child block -->
    <?= $block->getChildHtml('child') ?>
    
    <!-- URL và Assets -->
    <a href="<?= $block->escapeUrl($block->getUrl('route/controller/action')) ?>">Link</a>
    <img src="<?= $block->escapeUrl($block->getViewFileUrl('images/logo.png')) ?>" alt="Logo"/>
    
    <!-- Form key cho form submission -->
    <input type="hidden" name="form_key" value="<?= $block->escapeHtmlAttr($block->getFormKey()) ?>"/>
</div>
```

## Layout Handles phổ biến

| Handle | Mô tả |
|--------|-------|
| `default.xml` | Áp dụng cho tất cả pages |
| `cms_index_index.xml` | Homepage |
| `catalog_category_view.xml` | Category page |
| `catalog_product_view.xml` | Product page |
| `checkout_cart_index.xml` | Cart page |
| `checkout_index_index.xml` | Checkout page |
| `customer_account_login.xml` | Login page |

## Containers phổ biến

| Container | Vị trí |
|-----------|--------|
| `header.container` | Header |
| `page.top` | Trên content |
| `content` | Main content |
| `sidebar.main` | Sidebar chính |
| `sidebar.additional` | Sidebar phụ |
| `footer` | Footer |

## Escape Functions

```php
$block->escapeHtml($string)      // HTML content
$block->escapeHtmlAttr($string)  // HTML attributes
$block->escapeUrl($url)          // URLs
$block->escapeJs($string)        // JavaScript
$block->escapeCss($string)       // CSS
```
