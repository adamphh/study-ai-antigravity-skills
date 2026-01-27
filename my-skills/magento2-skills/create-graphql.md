---
name: Create GraphQL API
description: Hướng dẫn tạo GraphQL API trong Magento 2
---

# Tạo GraphQL API trong Magento 2

## Cấu trúc thư mục

```
{Vendor}/{ModuleName}/
├── etc/
│   └── schema.graphqls
└── Model/
    └── Resolver/
        └── {ResolverName}.php
```

## 1. Định nghĩa Schema

`etc/schema.graphqls`

```graphql
type Query {
    # Get single entity by ID
    {entity}(id: Int! @doc(description: "Entity ID")): {EntityName} 
        @resolver(class: "{Vendor}\\{ModuleName}\\Model\\Resolver\\{EntityName}")
        @doc(description: "Get entity by ID")
    
    # Get list with filter
    {entities}(
        filter: {EntityName}FilterInput @doc(description: "Filter options")
        pageSize: Int = 20 @doc(description: "Page size")
        currentPage: Int = 1 @doc(description: "Current page")
    ): {EntityName}Output 
        @resolver(class: "{Vendor}\\{ModuleName}\\Model\\Resolver\\{EntityName}List")
        @doc(description: "Get entities list")
}

type Mutation {
    create{EntityName}(input: {EntityName}Input!): {EntityName}
        @resolver(class: "{Vendor}\\{ModuleName}\\Model\\Resolver\\Create{EntityName}")
        @doc(description: "Create new entity")
}

type {EntityName} @doc(description: "Entity type") {
    id: Int @doc(description: "Entity ID")
    name: String @doc(description: "Name")
    status: Int @doc(description: "Status")
    description: String @doc(description: "Description")
    created_at: String @doc(description: "Created at")
}

type {EntityName}Output {
    items: [{EntityName}] @doc(description: "List of entities")
    total_count: Int @doc(description: "Total count")
}

input {EntityName}Input {
    name: String! @doc(description: "Name")
    status: Int @doc(description: "Status")
    description: String @doc(description: "Description")
}

input {EntityName}FilterInput {
    name: FilterStringInput
    status: FilterIntInput
}

input FilterStringInput {
    eq: String
    like: String
}

input FilterIntInput {
    eq: Int
    in: [Int]
}
```

## 2. Tạo Resolver

`Model/Resolver/{EntityName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\Resolver;

use Magento\Framework\GraphQl\Config\Element\Field;
use Magento\Framework\GraphQl\Query\ResolverInterface;
use Magento\Framework\GraphQl\Schema\Type\ResolveInfo;
use Magento\Framework\GraphQl\Exception\GraphQlInputException;
use Magento\Framework\GraphQl\Exception\GraphQlNoSuchEntityException;
use {Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface;

class {EntityName} implements ResolverInterface
{
    private {EntityName}RepositoryInterface $repository;

    public function __construct({EntityName}RepositoryInterface $repository)
    {
        $this->repository = $repository;
    }

    public function resolve(
        Field $field,
        $context,
        ResolveInfo $info,
        array $value = null,
        array $args = null
    ) {
        if (!isset($args['id'])) {
            throw new GraphQlInputException(__('Entity ID is required'));
        }

        try {
            $entity = $this->repository->getById((int)$args['id']);
            return [
                'id' => $entity->getId(),
                'name' => $entity->getName(),
                'status' => $entity->getStatus(),
                'description' => $entity->getDescription(),
                'created_at' => $entity->getCreatedAt()
            ];
        } catch (\Exception $e) {
            throw new GraphQlNoSuchEntityException(__('Entity not found'));
        }
    }
}
```

## 3. Test GraphQL Query

```graphql
# Query single entity
query {
    entity(id: 1) {
        id
        name
        status
    }
}

# Query list
query {
    entities(pageSize: 10, currentPage: 1) {
        items {
            id
            name
        }
        total_count
    }
}

# Mutation
mutation {
    createEntity(input: { name: "New Entity", status: 1 }) {
        id
        name
    }
}
```

## Lưu ý

- GraphQL endpoint: `/graphql`
- Cần xóa cache sau khi thay đổi schema: `bin/magento cache:clean`
- Sử dụng `@cache` directive để cache results
