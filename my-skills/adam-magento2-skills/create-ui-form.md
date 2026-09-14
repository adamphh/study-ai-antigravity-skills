---
name: Create Admin UI Form
description: Hướng dẫn tạo UI Component Form trong Admin Magento 2
---

# Tạo Admin UI Component Form

## UI Component Form

`view/adminhtml/ui_component/{entity}_form.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<form xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Ui:etc/ui_configuration.xsd">
    
    <argument name="data" xsi:type="array">
        <item name="js_config" xsi:type="array">
            <item name="provider" xsi:type="string">{entity}_form.{entity}_form_data_source</item>
        </item>
        <item name="label" xsi:type="string" translate="true">Entity Information</item>
        <item name="template" xsi:type="string">templates/form/collapsible</item>
    </argument>
    
    <settings>
        <buttons>
            <button name="save" class="{Vendor}\{ModuleName}\Block\Adminhtml\Edit\SaveButton"/>
            <button name="delete" class="{Vendor}\{ModuleName}\Block\Adminhtml\Edit\DeleteButton"/>
            <button name="back" class="{Vendor}\{ModuleName}\Block\Adminhtml\Edit\BackButton"/>
        </buttons>
        <namespace>{entity}_form</namespace>
        <dataScope>data</dataScope>
        <deps>
            <dep>{entity}_form.{entity}_form_data_source</dep>
        </deps>
    </settings>
    
    <dataSource name="{entity}_form_data_source">
        <argument name="data" xsi:type="array">
            <item name="js_config" xsi:type="array">
                <item name="component" xsi:type="string">Magento_Ui/js/form/provider</item>
            </item>
        </argument>
        <settings>
            <submitUrl path="*/*/save"/>
        </settings>
        <dataProvider class="{Vendor}\{ModuleName}\Model\{EntityName}\DataProvider" 
                      name="{entity}_form_data_source">
            <settings>
                <requestFieldName>entity_id</requestFieldName>
                <primaryFieldName>entity_id</primaryFieldName>
            </settings>
        </dataProvider>
    </dataSource>
    
    <fieldset name="general">
        <settings>
            <label translate="true">General Information</label>
        </settings>
        
        <field name="entity_id" formElement="input">
            <settings>
                <dataType>text</dataType>
                <visible>false</visible>
            </settings>
        </field>
        
        <field name="name" formElement="input">
            <settings>
                <dataType>text</dataType>
                <label translate="true">Name</label>
                <validation>
                    <rule name="required-entry" xsi:type="boolean">true</rule>
                </validation>
            </settings>
        </field>
        
        <field name="status" formElement="select">
            <settings>
                <dataType>int</dataType>
                <label translate="true">Status</label>
            </settings>
            <formElements>
                <select>
                    <settings>
                        <options class="{Vendor}\{ModuleName}\Model\Source\Status"/>
                    </settings>
                </select>
            </formElements>
        </field>
        
        <field name="description" formElement="wysiwyg">
            <settings>
                <label translate="true">Description</label>
            </settings>
            <formElements>
                <wysiwyg>
                    <settings>
                        <wysiwyg>true</wysiwyg>
                    </settings>
                </wysiwyg>
            </formElements>
        </field>
    </fieldset>
</form>
```

## DataProvider Class

```php
<?php
namespace {Vendor}\{ModuleName}\Model\{EntityName};

use Magento\Ui\DataProvider\AbstractDataProvider;
use {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName}\CollectionFactory;

class DataProvider extends AbstractDataProvider
{
    private array $loadedData = [];

    public function __construct(
        $name,
        $primaryFieldName,
        $requestFieldName,
        CollectionFactory $collectionFactory,
        array $meta = [],
        array $data = []
    ) {
        $this->collection = $collectionFactory->create();
        parent::__construct($name, $primaryFieldName, $requestFieldName, $meta, $data);
    }

    public function getData(): array
    {
        if (!empty($this->loadedData)) {
            return $this->loadedData;
        }
        
        $items = $this->collection->getItems();
        foreach ($items as $item) {
            $this->loadedData[$item->getId()] = $item->getData();
        }
        
        return $this->loadedData;
    }
}
```

## Button Classes

```php
<?php
// SaveButton.php
namespace {Vendor}\{ModuleName}\Block\Adminhtml\Edit;

use Magento\Framework\View\Element\UiComponent\Control\ButtonProviderInterface;

class SaveButton implements ButtonProviderInterface
{
    public function getButtonData(): array
    {
        return [
            'label' => __('Save'),
            'class' => 'save primary',
            'data_attribute' => [
                'mage-init' => ['button' => ['event' => 'save']],
                'form-role' => 'save',
            ],
            'sort_order' => 90,
        ];
    }
}
```
