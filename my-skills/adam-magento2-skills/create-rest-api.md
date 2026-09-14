---
name: Create REST API
description: Hướng dẫn tạo REST API trong Magento 2
---

# Tạo REST API trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── Api/
│   ├── Data/
│   │   └── {EntityName}Interface.php
│   └── {EntityName}RepositoryInterface.php
├── Model/
│   └── {EntityName}Repository.php
└── etc/
    ├── di.xml
    └── webapi.xml
```

## 1. Định nghĩa API trong webapi.xml

`etc/webapi.xml`

```xml
<?xml version="1.0"?>
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Webapi:etc/webapi.xsd">
    
    <!-- GET single entity -->
    <route url="/V1/{vendor}/{entity}/:id" method="GET">
        <service class="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface" method="getById"/>
        <resources>
            <resource ref="anonymous"/>
        </resources>
    </route>
    
    <!-- GET list -->
    <route url="/V1/{vendor}/{entities}" method="GET">
        <service class="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface" method="getList"/>
        <resources>
            <resource ref="{Vendor}_{ModuleName}::view"/>
        </resources>
    </route>
    
    <!-- POST create -->
    <route url="/V1/{vendor}/{entity}" method="POST">
        <service class="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface" method="save"/>
        <resources>
            <resource ref="{Vendor}_{ModuleName}::manage"/>
        </resources>
    </route>
    
    <!-- PUT update -->
    <route url="/V1/{vendor}/{entity}/:id" method="PUT">
        <service class="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface" method="save"/>
        <resources>
            <resource ref="{Vendor}_{ModuleName}::manage"/>
        </resources>
    </route>
    
    <!-- DELETE -->
    <route url="/V1/{vendor}/{entity}/:id" method="DELETE">
        <service class="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface" method="deleteById"/>
        <resources>
            <resource ref="{Vendor}_{ModuleName}::delete"/>
        </resources>
    </route>
    
</routes>
```

## 2. Resource References

| Resource | Mô tả |
|----------|-------|
| `anonymous` | Public access, không cần authentication |
| `self` | Customer đăng nhập (chỉ truy cập data của mình) |
| `{Vendor}_{ModuleName}::resource_id` | Admin với ACL cụ thể |

## 3. API Interface

```php
<?php
namespace {Vendor}\{ModuleName}\Api;

interface {EntityName}RepositoryInterface
{
    /**
     * Get entity by ID
     *
     * @param int $id
     * @return \{Vendor}\{ModuleName}\Api\Data\{EntityName}Interface
     * @throws \Magento\Framework\Exception\NoSuchEntityException
     */
    public function getById(int $id);

    /**
     * Save entity
     *
     * @param \{Vendor}\{ModuleName}\Api\Data\{EntityName}Interface $entity
     * @return \{Vendor}\{ModuleName}\Api\Data\{EntityName}Interface
     * @throws \Magento\Framework\Exception\CouldNotSaveException
     */
    public function save(\{Vendor}\{ModuleName}\Api\Data\{EntityName}Interface $entity);

    /**
     * Delete by ID
     *
     * @param int $id
     * @return bool
     * @throws \Magento\Framework\Exception\NoSuchEntityException
     * @throws \Magento\Framework\Exception\CouldNotDeleteException
     */
    public function deleteById(int $id);

    /**
     * Get list
     *
     * @param \Magento\Framework\Api\SearchCriteriaInterface $searchCriteria
     * @return \Magento\Framework\Api\SearchResultsInterface
     */
    public function getList(\Magento\Framework\Api\SearchCriteriaInterface $searchCriteria);
}
```

## 4. Test API

```bash
# GET - Anonymous
curl -X GET "https://example.com/rest/V1/{vendor}/{entity}/1"

# GET - With admin token
TOKEN=$(curl -X POST "https://example.com/rest/V1/integration/admin/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

curl -X GET "https://example.com/rest/V1/{vendor}/{entities}" \
  -H "Authorization: Bearer $TOKEN"

# POST - Create
curl -X POST "https://example.com/rest/V1/{vendor}/{entity}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity":{"name":"New Item","status":1}}'

# PUT - Update
curl -X PUT "https://example.com/rest/V1/{vendor}/{entity}/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity":{"entity_id":1,"name":"Updated Name"}}'

# DELETE
curl -X DELETE "https://example.com/rest/V1/{vendor}/{entity}/1" \
  -H "Authorization: Bearer $TOKEN"
```

## Lưu ý

- Các `@param` và `@return` annotations trong Interface **bắt buộc** để Magento serialize/deserialize data
- Sử dụng SearchCriteria để filter/sort/paginate trong getList
