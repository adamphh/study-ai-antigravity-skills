---
name: Create System Configuration
description: Hướng dẫn tạo System Configuration trong Admin Magento 2
---

# Tạo System Configuration trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── adminhtml/
│   │   └── system.xml
│   └── config.xml
└── Model/
    └── Config/
        └── Source/
            └── {SourceModel}.php
```

## 1. Tạo system.xml

`etc/adminhtml/system.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Config:etc/system_file.xsd">
    
    <system>
        <!-- Tab (optional, có thể dùng tab có sẵn) -->
        <tab id="{vendor}" translate="label" sortOrder="100">
            <label>{Vendor Name}</label>
        </tab>
        
        <!-- Section -->
        <section id="{vendor}_{modulename}" translate="label" 
                 sortOrder="10" showInDefault="1" showInWebsite="1" showInStore="1">
            <label>{Module Name}</label>
            <tab>{vendor}</tab>
            <resource>{Vendor}_{ModuleName}::config</resource>
            
            <!-- Group -->
            <group id="general" translate="label" sortOrder="10" 
                   showInDefault="1" showInWebsite="1" showInStore="1">
                <label>General Settings</label>
                
                <!-- Enable/Disable -->
                <field id="enabled" translate="label comment" 
                       type="select" sortOrder="10" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Enable Module</label>
                    <source_model>Magento\Config\Model\Config\Source\Yesno</source_model>
                    <comment>Enable or disable the module</comment>
                </field>
                
                <!-- Text field -->
                <field id="title" translate="label" 
                       type="text" sortOrder="20" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Title</label>
                    <validate>required-entry</validate>
                </field>
                
                <!-- Textarea -->
                <field id="description" translate="label" 
                       type="textarea" sortOrder="30" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Description</label>
                </field>
                
                <!-- Select với custom source -->
                <field id="display_mode" translate="label" 
                       type="select" sortOrder="40" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Display Mode</label>
                    <source_model>{Vendor}\{ModuleName}\Model\Config\Source\DisplayMode</source_model>
                </field>
                
                <!-- Multiselect -->
                <field id="categories" translate="label" 
                       type="multiselect" sortOrder="50" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Categories</label>
                    <source_model>Magento\Catalog\Model\Category\Attribute\Source\Mode</source_model>
                </field>
                
                <!-- Password/Encrypted -->
                <field id="api_key" translate="label" 
                       type="obscure" sortOrder="60" 
                       showInDefault="1" showInWebsite="1" showInStore="0">
                    <label>API Key</label>
                    <backend_model>Magento\Config\Model\Config\Backend\Encrypted</backend_model>
                </field>
                
                <!-- Depends (hiển thị khi điều kiện thỏa) -->
                <field id="advanced_option" translate="label" 
                       type="text" sortOrder="70" 
                       showInDefault="1" showInWebsite="1" showInStore="1">
                    <label>Advanced Option</label>
                    <depends>
                        <field id="enabled">1</field>
                    </depends>
                </field>
            </group>
        </section>
    </system>
</config>
```

## 2. Tạo config.xml (Default values)

`etc/config.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Store:etc/config.xsd">
    <default>
        <{vendor}_{modulename}>
            <general>
                <enabled>1</enabled>
                <title>Default Title</title>
                <display_mode>grid</display_mode>
            </general>
        </{vendor}_{modulename}>
    </default>
</config>
```

## 3. Tạo Source Model

`Model/Config/Source/DisplayMode.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Config\Source;

use Magento\Framework\Data\OptionSourceInterface;

class DisplayMode implements OptionSourceInterface
{
    public function toOptionArray(): array
    {
        return [
            ['value' => 'grid', 'label' => __('Grid')],
            ['value' => 'list', 'label' => __('List')],
            ['value' => 'carousel', 'label' => __('Carousel')]
        ];
    }
}
```

## 4. Đọc Config Values

```php
<?php
use Magento\Framework\App\Config\ScopeConfigInterface;
use Magento\Store\Model\ScopeInterface;

class Helper
{
    private ScopeConfigInterface $scopeConfig;
    
    private const XML_PATH_ENABLED = '{vendor}_{modulename}/general/enabled';
    private const XML_PATH_TITLE = '{vendor}_{modulename}/general/title';

    public function __construct(ScopeConfigInterface $scopeConfig)
    {
        $this->scopeConfig = $scopeConfig;
    }

    public function isEnabled($storeId = null): bool
    {
        return $this->scopeConfig->isSetFlag(
            self::XML_PATH_ENABLED,
            ScopeInterface::SCOPE_STORE,
            $storeId
        );
    }

    public function getTitle($storeId = null): ?string
    {
        return $this->scopeConfig->getValue(
            self::XML_PATH_TITLE,
            ScopeInterface::SCOPE_STORE,
            $storeId
        );
    }
}
```
