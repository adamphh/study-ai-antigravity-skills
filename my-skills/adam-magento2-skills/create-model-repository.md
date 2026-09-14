---
name: Create Model and Repository
description: Hướng dẫn tạo Model, ResourceModel, Collection và Repository Pattern trong Magento 2
---

# Tạo Model, ResourceModel, Collection và Repository

## Cấu trúc thư mục

```
{Vendor}/{ModuleName}/
├── Api/
│   ├── Data/
│   │   └── {EntityName}Interface.php
│   └── {EntityName}RepositoryInterface.php
├── Model/
│   ├── {EntityName}.php
│   ├── {EntityName}Repository.php
│   └── ResourceModel/
│       ├── {EntityName}.php
│       └── {EntityName}/
│           └── Collection.php
└── etc/
    └── di.xml
```

---

## Bước 1: Tạo Data Interface

`Api/Data/{EntityName}Interface.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Api\Data;

interface {EntityName}Interface
{
    public const ENTITY_ID = 'entity_id';
    public const NAME = 'name';
    public const STATUS = 'status';
    public const CREATED_AT = 'created_at';
    public const UPDATED_AT = 'updated_at';

    /**
     * Get entity ID
     *
     * @return int|null
     */
    public function getEntityId(): ?int;

    /**
     * Set entity ID
     *
     * @param int $entityId
     * @return $this
     */
    public function setEntityId(int $entityId): self;

    /**
     * Get name
     *
     * @return string|null
     */
    public function getName(): ?string;

    /**
     * Set name
     *
     * @param string $name
     * @return $this
     */
    public function setName(string $name): self;

    /**
     * Get status
     *
     * @return int|null
     */
    public function getStatus(): ?int;

    /**
     * Set status
     *
     * @param int $status
     * @return $this
     */
    public function setStatus(int $status): self;
}
```

---

## Bước 2: Tạo Model

`Model/{EntityName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model;

use Magento\Framework\Model\AbstractModel;
use {Vendor}\{ModuleName}\Api\Data\{EntityName}Interface;
use {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName} as ResourceModel;

class {EntityName} extends AbstractModel implements {EntityName}Interface
{
    /**
     * @var string
     */
    protected $_eventPrefix = '{vendor}_{entity_name}';

    /**
     * Initialize resource model
     *
     * @return void
     */
    protected function _construct(): void
    {
        $this->_init(ResourceModel::class);
    }

    /**
     * @inheritdoc
     */
    public function getEntityId(): ?int
    {
        return $this->getData(self::ENTITY_ID) ? (int)$this->getData(self::ENTITY_ID) : null;
    }

    /**
     * @inheritdoc
     */
    public function setEntityId($entityId): self
    {
        return $this->setData(self::ENTITY_ID, $entityId);
    }

    /**
     * @inheritdoc
     */
    public function getName(): ?string
    {
        return $this->getData(self::NAME);
    }

    /**
     * @inheritdoc
     */
    public function setName(string $name): self
    {
        return $this->setData(self::NAME, $name);
    }

    /**
     * @inheritdoc
     */
    public function getStatus(): ?int
    {
        return $this->getData(self::STATUS) ? (int)$this->getData(self::STATUS) : null;
    }

    /**
     * @inheritdoc
     */
    public function setStatus(int $status): self
    {
        return $this->setData(self::STATUS, $status);
    }
}
```

---

## Bước 3: Tạo ResourceModel

`Model/ResourceModel/{EntityName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\ResourceModel;

use Magento\Framework\Model\ResourceModel\Db\AbstractDb;

class {EntityName} extends AbstractDb
{
    /**
     * @var string
     */
    protected $_eventPrefix = '{vendor}_{entity_name}_resource';

    /**
     * Initialize resource model
     *
     * @return void
     */
    protected function _construct(): void
    {
        $this->_init('{table_name}', 'entity_id');
    }
}
```

---

## Bước 4: Tạo Collection

`Model/ResourceModel/{EntityName}/Collection.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName};

use Magento\Framework\Model\ResourceModel\Db\Collection\AbstractCollection;
use {Vendor}\{ModuleName}\Model\{EntityName} as Model;
use {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName} as ResourceModel;

class Collection extends AbstractCollection
{
    /**
     * @var string
     */
    protected $_eventPrefix = '{vendor}_{entity_name}_collection';

    /**
     * @var string
     */
    protected $_idFieldName = 'entity_id';

    /**
     * Initialize collection
     *
     * @return void
     */
    protected function _construct(): void
    {
        $this->_init(Model::class, ResourceModel::class);
    }
}
```

---

## Bước 5: Tạo Repository Interface

`Api/{EntityName}RepositoryInterface.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Api;

use Magento\Framework\Api\SearchCriteriaInterface;
use Magento\Framework\Api\SearchResultsInterface;
use Magento\Framework\Exception\LocalizedException;
use Magento\Framework\Exception\NoSuchEntityException;
use {Vendor}\{ModuleName}\Api\Data\{EntityName}Interface;

interface {EntityName}RepositoryInterface
{
    /**
     * Get entity by ID
     *
     * @param int $entityId
     * @return {EntityName}Interface
     * @throws NoSuchEntityException
     */
    public function getById(int $entityId): {EntityName}Interface;

    /**
     * Save entity
     *
     * @param {EntityName}Interface $entity
     * @return {EntityName}Interface
     * @throws LocalizedException
     */
    public function save({EntityName}Interface $entity): {EntityName}Interface;

    /**
     * Delete entity
     *
     * @param {EntityName}Interface $entity
     * @return bool
     * @throws LocalizedException
     */
    public function delete({EntityName}Interface $entity): bool;

    /**
     * Delete entity by ID
     *
     * @param int $entityId
     * @return bool
     * @throws NoSuchEntityException
     * @throws LocalizedException
     */
    public function deleteById(int $entityId): bool;

    /**
     * Get list
     *
     * @param SearchCriteriaInterface $searchCriteria
     * @return SearchResultsInterface
     */
    public function getList(SearchCriteriaInterface $searchCriteria): SearchResultsInterface;
}
```

---

## Bước 6: Tạo Repository Implementation

`Model/{EntityName}Repository.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model;

use Magento\Framework\Api\SearchCriteria\CollectionProcessorInterface;
use Magento\Framework\Api\SearchCriteriaInterface;
use Magento\Framework\Api\SearchResultsInterface;
use Magento\Framework\Api\SearchResultsInterfaceFactory;
use Magento\Framework\Exception\CouldNotDeleteException;
use Magento\Framework\Exception\CouldNotSaveException;
use Magento\Framework\Exception\NoSuchEntityException;
use {Vendor}\{ModuleName}\Api\Data\{EntityName}Interface;
use {Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface;
use {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName} as ResourceModel;
use {Vendor}\{ModuleName}\Model\ResourceModel\{EntityName}\CollectionFactory;

class {EntityName}Repository implements {EntityName}RepositoryInterface
{
    /**
     * @var ResourceModel
     */
    private ResourceModel $resourceModel;

    /**
     * @var {EntityName}Factory
     */
    private {EntityName}Factory $entityFactory;

    /**
     * @var CollectionFactory
     */
    private CollectionFactory $collectionFactory;

    /**
     * @var CollectionProcessorInterface
     */
    private CollectionProcessorInterface $collectionProcessor;

    /**
     * @var SearchResultsInterfaceFactory
     */
    private SearchResultsInterfaceFactory $searchResultsFactory;

    /**
     * @param ResourceModel $resourceModel
     * @param {EntityName}Factory $entityFactory
     * @param CollectionFactory $collectionFactory
     * @param CollectionProcessorInterface $collectionProcessor
     * @param SearchResultsInterfaceFactory $searchResultsFactory
     */
    public function __construct(
        ResourceModel $resourceModel,
        {EntityName}Factory $entityFactory,
        CollectionFactory $collectionFactory,
        CollectionProcessorInterface $collectionProcessor,
        SearchResultsInterfaceFactory $searchResultsFactory
    ) {
        $this->resourceModel = $resourceModel;
        $this->entityFactory = $entityFactory;
        $this->collectionFactory = $collectionFactory;
        $this->collectionProcessor = $collectionProcessor;
        $this->searchResultsFactory = $searchResultsFactory;
    }

    /**
     * @inheritdoc
     */
    public function getById(int $entityId): {EntityName}Interface
    {
        $entity = $this->entityFactory->create();
        $this->resourceModel->load($entity, $entityId);
        
        if (!$entity->getEntityId()) {
            throw new NoSuchEntityException(
                __('The entity with ID "%1" does not exist.', $entityId)
            );
        }
        
        return $entity;
    }

    /**
     * @inheritdoc
     */
    public function save({EntityName}Interface $entity): {EntityName}Interface
    {
        try {
            $this->resourceModel->save($entity);
        } catch (\Exception $exception) {
            throw new CouldNotSaveException(
                __('Could not save the entity: %1', $exception->getMessage())
            );
        }
        
        return $entity;
    }

    /**
     * @inheritdoc
     */
    public function delete({EntityName}Interface $entity): bool
    {
        try {
            $this->resourceModel->delete($entity);
        } catch (\Exception $exception) {
            throw new CouldNotDeleteException(
                __('Could not delete the entity: %1', $exception->getMessage())
            );
        }
        
        return true;
    }

    /**
     * @inheritdoc
     */
    public function deleteById(int $entityId): bool
    {
        return $this->delete($this->getById($entityId));
    }

    /**
     * @inheritdoc
     */
    public function getList(SearchCriteriaInterface $searchCriteria): SearchResultsInterface
    {
        $collection = $this->collectionFactory->create();
        $this->collectionProcessor->process($searchCriteria, $collection);

        $searchResults = $this->searchResultsFactory->create();
        $searchResults->setSearchCriteria($searchCriteria);
        $searchResults->setItems($collection->getItems());
        $searchResults->setTotalCount($collection->getSize());

        return $searchResults;
    }
}
```

---

## Bước 7: Cấu hình DI (di.xml)

`etc/di.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:ObjectManager/etc/config.xsd">
    
    <!-- Preference for Data Interface -->
    <preference for="{Vendor}\{ModuleName}\Api\Data\{EntityName}Interface"
                type="{Vendor}\{ModuleName}\Model\{EntityName}"/>
    
    <!-- Preference for Repository Interface -->
    <preference for="{Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface"
                type="{Vendor}\{ModuleName}\Model\{EntityName}Repository"/>
                
</config>
```

---

## Lưu ý quan trọng

1. **Interface-based Programming**: Luôn sử dụng Interface để đảm bảo loose coupling
2. **Factory Pattern**: Magento tự động generate Factory classes, chỉ cần inject `{EntityName}Factory`
3. **Collection Processor**: Xử lý tự động các filter, sort, pagination từ SearchCriteria
4. **Event Prefix**: Đặt `_eventPrefix` để có thể dispatch events
