---
name: Create Admin UI Component Grid
description: Hướng dẫn tạo UI Component Grid trong Admin Magento 2
---

# Tạo Admin UI Component Grid

## Cấu trúc thư mục

```
{Vendor}/{ModuleName}/
├── etc/
│   └── di.xml
├── view/adminhtml/
│   ├── layout/
│   │   └── {route_id}_{controller}_{action}.xml
│   └── ui_component/
│       └── {entity}_listing.xml
└── Ui/
    └── Component/
        └── Listing/
            └── Column/
                └── {EntityName}Actions.php
```

## 1. Tạo UI Component Grid

`view/adminhtml/ui_component/{entity}_listing.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<listing xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Ui:etc/ui_configuration.xsd">
    
    <argument name="data" xsi:type="array">
        <item name="js_config" xsi:type="array">
            <item name="provider" xsi:type="string">{entity}_listing.{entity}_listing_data_source</item>
        </item>
    </argument>
    
    <settings>
        <buttons>
            <button name="add">
                <url path="*/*/new"/>
                <class>primary</class>
                <label translate="true">Add New</label>
            </button>
        </buttons>
        <spinner>{entity}_columns</spinner>
        <deps>
            <dep>{entity}_listing.{entity}_listing_data_source</dep>
        </deps>
    </settings>
    
    <dataSource name="{entity}_listing_data_source" component="Magento_Ui/js/grid/provider">
        <settings>
            <storageConfig>
                <param name="indexField" xsi:type="string">entity_id</param>
            </storageConfig>
            <updateUrl path="mui/index/render"/>
        </settings>
        <aclResource>{Vendor}_{ModuleName}::{entity}</aclResource>
        <dataProvider class="Magento\Framework\View\Element\UiComponent\DataProvider\DataProvider" 
                      name="{entity}_listing_data_source">
            <settings>
                <requestFieldName>id</requestFieldName>
                <primaryFieldName>entity_id</primaryFieldName>
            </settings>
        </dataProvider>
    </dataSource>
    
    <listingToolbar name="listing_top">
        <bookmark name="bookmarks"/>
        <columnsControls name="columns_controls"/>
        <filterSearch name="fulltext"/>
        <filters name="listing_filters"/>
        <massaction name="listing_massaction">
            <action name="delete">
                <settings>
                    <url path="*/*/massDelete"/>
                    <type>delete</type>
                    <label translate="true">Delete</label>
                    <confirm>
                        <title translate="true">Delete items</title>
                        <message translate="true">Are you sure?</message>
                    </confirm>
                </settings>
            </action>
        </massaction>
        <paging name="listing_paging"/>
    </listingToolbar>
    
    <columns name="{entity}_columns">
        <selectionsColumn name="ids">
            <settings>
                <indexField>entity_id</indexField>
            </settings>
        </selectionsColumn>
        
        <column name="entity_id">
            <settings>
                <filter>textRange</filter>
                <label translate="true">ID</label>
                <sorting>asc</sorting>
            </settings>
        </column>
        
        <column name="name">
            <settings>
                <filter>text</filter>
                <label translate="true">Name</label>
            </settings>
        </column>
        
        <column name="status" component="Magento_Ui/js/grid/columns/select">
            <settings>
                <filter>select</filter>
                <dataType>select</dataType>
                <label translate="true">Status</label>
                <options class="{Vendor}\{ModuleName}\Model\Source\Status"/>
            </settings>
        </column>
        
        <actionsColumn name="actions" class="{Vendor}\{ModuleName}\Ui\Component\Listing\Column\Actions">
            <settings>
                <indexField>entity_id</indexField>
            </settings>
        </actionsColumn>
    </columns>
</listing>
```

## 2. Đăng ký DataProvider trong di.xml

```xml
<type name="Magento\Framework\View\Element\UiComponent\DataProvider\CollectionFactory">
    <arguments>
        <argument name="collections" xsi:type="array">
            <item name="{entity}_listing_data_source" xsi:type="string">
                {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName}\Grid\Collection
            </item>
        </argument>
    </arguments>
</type>
```

## 3. Tạo Actions Column

```php
<?php
namespace {Vendor}\{ModuleName}\Ui\Component\Listing\Column;

use Magento\Framework\UrlInterface;
use Magento\Framework\View\Element\UiComponent\ContextInterface;
use Magento\Framework\View\Element\UiComponentFactory;
use Magento\Ui\Component\Listing\Columns\Column;

class Actions extends Column
{
    private UrlInterface $urlBuilder;

    public function __construct(
        ContextInterface $context,
        UiComponentFactory $uiComponentFactory,
        UrlInterface $urlBuilder,
        array $components = [],
        array $data = []
    ) {
        $this->urlBuilder = $urlBuilder;
        parent::__construct($context, $uiComponentFactory, $components, $data);
    }

    public function prepareDataSource(array $dataSource): array
    {
        if (isset($dataSource['data']['items'])) {
            foreach ($dataSource['data']['items'] as &$item) {
                $item[$this->getData('name')] = [
                    'edit' => [
                        'href' => $this->urlBuilder->getUrl('*/*/edit', ['id' => $item['entity_id']]),
                        'label' => __('Edit')
                    ],
                    'delete' => [
                        'href' => $this->urlBuilder->getUrl('*/*/delete', ['id' => $item['entity_id']]),
                        'label' => __('Delete'),
                        'confirm' => ['title' => __('Delete'), 'message' => __('Are you sure?')]
                    ]
                ];
            }
        }
        return $dataSource;
    }
}
```
