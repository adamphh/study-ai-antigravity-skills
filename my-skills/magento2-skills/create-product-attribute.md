---
name: Create Product Attribute
description: Hướng dẫn tạo Product Attribute (EAV) trong Magento 2
---

# Tạo Product Attribute trong Magento 2

## Data Patch để tạo Attribute

`Setup/Patch/Data/Add{AttributeName}Attribute.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Setup\Patch\Data;

use Magento\Catalog\Model\Product;
use Magento\Eav\Model\Entity\Attribute\ScopedAttributeInterface;
use Magento\Eav\Setup\EavSetup;
use Magento\Eav\Setup\EavSetupFactory;
use Magento\Framework\Setup\ModuleDataSetupInterface;
use Magento\Framework\Setup\Patch\DataPatchInterface;

class Add{AttributeName}Attribute implements DataPatchInterface
{
    private ModuleDataSetupInterface $moduleDataSetup;
    private EavSetupFactory $eavSetupFactory;

    public function __construct(
        ModuleDataSetupInterface $moduleDataSetup,
        EavSetupFactory $eavSetupFactory
    ) {
        $this->moduleDataSetup = $moduleDataSetup;
        $this->eavSetupFactory = $eavSetupFactory;
    }

    public function apply()
    {
        $this->moduleDataSetup->startSetup();
        
        /** @var EavSetup $eavSetup */
        $eavSetup = $this->eavSetupFactory->create(['setup' => $this->moduleDataSetup]);

        $eavSetup->addAttribute(
            Product::ENTITY,
            '{attribute_code}',
            [
                'type' => 'varchar',              // varchar, int, text, decimal, datetime
                'label' => 'Attribute Label',
                'input' => 'text',                // text, textarea, select, multiselect, boolean, date
                'required' => false,
                'sort_order' => 100,
                'global' => ScopedAttributeInterface::SCOPE_STORE,
                'visible' => true,
                'user_defined' => true,
                'searchable' => false,
                'filterable' => false,
                'comparable' => false,
                'visible_on_front' => true,
                'used_in_product_listing' => true,
                'unique' => false,
                'group' => 'General',             // Attribute group name
                'apply_to' => '',                 // simple, configurable, virtual, bundle, downloadable, grouped
            ]
        );

        $this->moduleDataSetup->endSetup();
        return $this;
    }

    public static function getDependencies(): array
    {
        return [];
    }

    public function getAliases(): array
    {
        return [];
    }
}
```

## Các loại Input Types

| Input Type | Backend Type | Mô tả |
|------------|--------------|-------|
| `text` | `varchar` | Text field ngắn |
| `textarea` | `text` | Text field dài |
| `select` | `int` | Dropdown single select |
| `multiselect` | `varchar` | Multiple select |
| `boolean` | `int` | Yes/No |
| `date` | `datetime` | Date picker |
| `price` | `decimal` | Price field |
| `media_image` | `varchar` | Image upload |
| `weee` | `decimal` | Fixed product tax |

## Tạo Attribute với Options (Select/Multiselect)

```php
$eavSetup->addAttribute(
    Product::ENTITY,
    'custom_select',
    [
        'type' => 'int',
        'label' => 'Custom Select',
        'input' => 'select',
        'source' => \Magento\Eav\Model\Entity\Attribute\Source\Table::class,
        'required' => false,
        'global' => ScopedAttributeInterface::SCOPE_STORE,
        'visible' => true,
        'user_defined' => true,
        'option' => [
            'values' => [
                'Option 1',
                'Option 2', 
                'Option 3'
            ]
        ]
    ]
);
```

## Custom Source Model

```php
<?php
namespace {Vendor}\{ModuleName}\Model\Config\Source;

use Magento\Eav\Model\Entity\Attribute\Source\AbstractSource;

class CustomOptions extends AbstractSource
{
    public function getAllOptions(): array
    {
        if ($this->_options === null) {
            $this->_options = [
                ['value' => '', 'label' => __('-- Please Select --')],
                ['value' => 'option1', 'label' => __('Option 1')],
                ['value' => 'option2', 'label' => __('Option 2')],
            ];
        }
        return $this->_options;
    }
}
```

Sử dụng: `'source' => \{Vendor}\{ModuleName}\Model\Config\Source\CustomOptions::class`

## Đọc/Ghi Attribute Value

```php
// Đọc giá trị
$product->getData('{attribute_code}');
$product->getCustomAttribute('{attribute_code}')?->getValue();

// Ghi giá trị
$product->setData('{attribute_code}', 'value');
$product->setCustomAttribute('{attribute_code}', 'value');
```
