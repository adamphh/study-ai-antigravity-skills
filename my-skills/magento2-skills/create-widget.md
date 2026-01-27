---
name: Create CMS Widget
description: Hướng dẫn tạo CMS Widget trong Magento 2
---

# Tạo CMS Widget trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   └── widget.xml
├── Block/
│   └── Widget/
│       └── {WidgetName}.php
└── view/
    └── frontend/
        └── templates/
            └── widget/
                └── {widget_template}.phtml
```

## 1. Định nghĩa Widget

`etc/widget.xml`

```xml
<?xml version="1.0"?>
<widgets xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Widget:etc/widget.xsd">
    
    <widget id="{vendor}_{modulename}_{widget_id}" 
            class="{Vendor}\{ModuleName}\Block\Widget\{WidgetName}"
            placeholder_image="Magento_Widget::placeholder.gif">
        <label translate="true">Custom Widget</label>
        <description translate="true">Widget description here</description>
        
        <parameters>
            <!-- Text Input -->
            <parameter name="title" xsi:type="text" visible="true" sort_order="10">
                <label translate="true">Title</label>
            </parameter>
            
            <!-- Required Field -->
            <parameter name="identifier" xsi:type="text" required="true" visible="true" sort_order="20">
                <label translate="true">Identifier</label>
            </parameter>
            
            <!-- Select Dropdown -->
            <parameter name="display_type" xsi:type="select" visible="true" sort_order="30">
                <label translate="true">Display Type</label>
                <options>
                    <option name="default" value="grid" selected="true">
                        <label translate="true">Grid</label>
                    </option>
                    <option name="list" value="list">
                        <label translate="true">List</label>
                    </option>
                </options>
            </parameter>
            
            <!-- Number Input -->
            <parameter name="items_count" xsi:type="text" visible="true" sort_order="40">
                <label translate="true">Number of Items</label>
                <value>5</value>
            </parameter>
            
            <!-- Category Chooser -->
            <parameter name="category_id" xsi:type="block" visible="true" sort_order="50">
                <label translate="true">Category</label>
                <block class="Magento\Catalog\Block\Adminhtml\Category\Widget\Chooser">
                    <data>
                        <item name="button" xsi:type="array">
                            <item name="open" xsi:type="string">Select Category...</item>
                        </item>
                    </data>
                </block>
            </parameter>
            
            <!-- Template Chooser -->
            <parameter name="template" xsi:type="select" visible="true" sort_order="100">
                <label translate="true">Template</label>
                <options>
                    <option name="default" value="{Vendor}_{ModuleName}::widget/default.phtml" selected="true">
                        <label translate="true">Default Template</label>
                    </option>
                    <option name="minimal" value="{Vendor}_{ModuleName}::widget/minimal.phtml">
                        <label translate="true">Minimal Template</label>
                    </option>
                </options>
            </parameter>
        </parameters>
        
        <!-- Supported Containers -->
        <containers>
            <container name="content">
                <template name="default" value="default"/>
            </container>
            <container name="sidebar.main">
                <template name="sidebar" value="minimal"/>
            </container>
        </containers>
    </widget>
    
</widgets>
```

## 2. Widget Block Class

`Block/Widget/{WidgetName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Block\Widget;

use Magento\Framework\View\Element\Template;
use Magento\Widget\Block\BlockInterface;

class {WidgetName} extends Template implements BlockInterface
{
    protected $_template = '{Vendor}_{ModuleName}::widget/default.phtml';

    /**
     * Get widget title
     */
    public function getTitle(): string
    {
        return (string)$this->getData('title');
    }

    /**
     * Get display type
     */
    public function getDisplayType(): string
    {
        return $this->getData('display_type') ?: 'grid';
    }

    /**
     * Get items count
     */
    public function getItemsCount(): int
    {
        return (int)($this->getData('items_count') ?: 5);
    }

    /**
     * Get category ID
     */
    public function getCategoryId(): ?int
    {
        $categoryId = $this->getData('category_id');
        return $categoryId ? (int)$categoryId : null;
    }

    /**
     * Get items to display
     */
    public function getItems(): array
    {
        // Your logic to get items
        return [];
    }
}
```

## 3. Widget Template

`view/frontend/templates/widget/default.phtml`

```php
<?php
/**
 * @var \{Vendor}\{ModuleName}\Block\Widget\{WidgetName} $block
 */
?>
<div class="widget custom-widget <?= $block->escapeHtmlAttr($block->getDisplayType()) ?>">
    <?php if ($block->getTitle()): ?>
        <h3 class="widget-title"><?= $block->escapeHtml($block->getTitle()) ?></h3>
    <?php endif; ?>
    
    <div class="widget-content">
        <?php $items = $block->getItems(); ?>
        <?php if (!empty($items)): ?>
            <ul class="items-list">
                <?php foreach ($items as $item): ?>
                    <li class="item"><?= $block->escapeHtml($item->getName()) ?></li>
                <?php endforeach; ?>
            </ul>
        <?php else: ?>
            <p><?= $block->escapeHtml(__('No items found.')) ?></p>
        <?php endif; ?>
    </div>
</div>
```

## Sử dụng Widget

### Trong CMS Block/Page

```
{{widget type="{Vendor}\{ModuleName}\Block\Widget\{WidgetName}" title="My Widget" display_type="grid" items_count="10"}}
```

### Trong Layout XML

```xml
<referenceContainer name="content">
    <block class="{Vendor}\{ModuleName}\Block\Widget\{WidgetName}" name="custom.widget">
        <arguments>
            <argument name="title" xsi:type="string">Widget Title</argument>
            <argument name="items_count" xsi:type="number">10</argument>
        </arguments>
    </block>
</referenceContainer>
```

### Admin: Content > Widgets

Vào Admin → Content → Widgets → Add Widget để tạo widget instance.
