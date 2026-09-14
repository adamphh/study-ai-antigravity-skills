---
name: Create Database Schema
description: Hướng dẫn tạo database schema trong Magento 2 sử dụng Declarative Schema
---

# Tạo Database Schema trong Magento 2

Từ Magento 2.3+, sử dụng **Declarative Schema** (db_schema.xml) thay vì InstallSchema.

## Tạo db_schema.xml

`etc/db_schema.xml`

```xml
<?xml version="1.0"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Setup/Declaration/Schema/etc/schema.xsd">
    
    <table name="{vendor}_{entity}" resource="default" engine="innodb" comment="Entity Table">
        
        <column xsi:type="int" name="entity_id" unsigned="true" nullable="false" 
                identity="true" comment="Entity ID"/>
        <column xsi:type="varchar" name="name" length="255" nullable="false" comment="Name"/>
        <column xsi:type="text" name="description" nullable="true" comment="Description"/>
        <column xsi:type="int" name="status" unsigned="true" nullable="false" default="1"/>
        <column xsi:type="decimal" name="price" precision="12" scale="4" nullable="true"/>
        <column xsi:type="timestamp" name="created_at" on_update="false" nullable="false" 
                default="CURRENT_TIMESTAMP"/>
        <column xsi:type="timestamp" name="updated_at" on_update="true" nullable="false" 
                default="CURRENT_TIMESTAMP"/>
        
        <constraint xsi:type="primary" referenceId="PRIMARY">
            <column name="entity_id"/>
        </constraint>
        
        <index referenceId="{VENDOR}_{ENTITY}_STATUS" indexType="btree">
            <column name="status"/>
        </index>
    </table>
</schema>
```

## Generate Whitelist

```bash
bin/magento setup:db-declaration:generate-whitelist --module-name={Vendor}_{ModuleName}
bin/magento setup:upgrade
```

## Các loại Column phổ biến

| Type | Mô tả |
|------|-------|
| `int`, `smallint`, `bigint` | Integer |
| `decimal` | Số thập phân (precision, scale) |
| `varchar` | Chuỗi (length) |
| `text`, `mediumtext` | Text dài |
| `timestamp`, `datetime`, `date` | Thời gian |
| `boolean` | True/False |
