---
name: Unit Testing with PHPUnit
description: Hướng dẫn viết Unit Test và Integration Test trong Magento 2
---

# Unit Testing trong Magento 2

## Cấu trúc

```
{Vendor}/{ModuleName}/
└── Test/
    ├── Unit/
    │   └── Model/
    │       └── {ClassName}Test.php
    └── Integration/
        └── Model/
            └── {ClassName}Test.php
```

## 1. Unit Test cơ bản

`Test/Unit/Model/{ClassName}Test.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Test\Unit\Model;

use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;
use {Vendor}\{ModuleName}\Model\{ClassName};

class {ClassName}Test extends TestCase
{
    /**
     * @var {ClassName}
     */
    private {ClassName} $model;

    /**
     * @var MockObject
     */
    private MockObject $dependencyMock;

    protected function setUp(): void
    {
        // Create mocks for dependencies
        $this->dependencyMock = $this->createMock(DependencyClass::class);
        
        // Create instance with mocked dependencies
        $this->model = new {ClassName}(
            $this->dependencyMock
        );
    }

    public function testGetName(): void
    {
        $expectedName = 'Test Name';
        $this->model->setName($expectedName);
        
        $this->assertEquals($expectedName, $this->model->getName());
    }

    public function testGetNameReturnsNull(): void
    {
        $this->assertNull($this->model->getName());
    }

    /**
     * @dataProvider priceDataProvider
     */
    public function testCalculatePrice(float $input, float $expected): void
    {
        $result = $this->model->calculatePrice($input);
        $this->assertEquals($expected, $result);
    }

    public function priceDataProvider(): array
    {
        return [
            'zero price' => [0.0, 0.0],
            'positive price' => [100.0, 110.0],
            'decimal price' => [99.99, 109.99],
        ];
    }

    public function testMethodThrowsException(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid value');
        
        $this->model->processValue(-1);
    }

    public function testMethodCallsDependency(): void
    {
        // Set up mock expectation
        $this->dependencyMock
            ->expects($this->once())
            ->method('doSomething')
            ->with('expected_argument')
            ->willReturn('mocked_result');
        
        $result = $this->model->process('expected_argument');
        
        $this->assertEquals('mocked_result', $result);
    }
}
```

## 2. Mocking Techniques

```php
// Simple mock
$mock = $this->createMock(SomeClass::class);

// Mock with constructor arguments
$mock = $this->getMockBuilder(SomeClass::class)
    ->setConstructorArgs(['arg1', 'arg2'])
    ->getMock();

// Partial mock (only mock specific methods)
$mock = $this->getMockBuilder(SomeClass::class)
    ->onlyMethods(['methodToMock'])
    ->getMock();

// Mock method return values
$mock->method('getName')->willReturn('Test');
$mock->method('getPrice')->willReturnCallback(function ($id) {
    return $id * 10;
});

// Consecutive returns
$mock->method('getValue')
    ->willReturnOnConsecutiveCalls('first', 'second', 'third');

// Verify method calls
$mock->expects($this->once())->method('save');
$mock->expects($this->exactly(3))->method('process');
$mock->expects($this->never())->method('delete');
```

## 3. Integration Test

`Test/Integration/Model/{ClassName}Test.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Test\Integration\Model;

use Magento\TestFramework\Helper\Bootstrap;
use PHPUnit\Framework\TestCase;
use {Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface;
use {Vendor}\{ModuleName}\Model\{EntityName};

class {ClassName}Test extends TestCase
{
    /**
     * @var {EntityName}RepositoryInterface
     */
    private {EntityName}RepositoryInterface $repository;

    protected function setUp(): void
    {
        $objectManager = Bootstrap::getObjectManager();
        $this->repository = $objectManager->get({EntityName}RepositoryInterface::class);
    }

    /**
     * @magentoDataFixture {Vendor}_{ModuleName}::Test/Integration/_files/entity.php
     */
    public function testGetById(): void
    {
        $entity = $this->repository->getById(1);
        
        $this->assertEquals('Test Entity', $entity->getName());
        $this->assertEquals(1, $entity->getStatus());
    }

    /**
     * @magentoDbIsolation enabled
     */
    public function testSave(): void
    {
        $objectManager = Bootstrap::getObjectManager();
        $entity = $objectManager->create({EntityName}::class);
        $entity->setName('New Entity');
        $entity->setStatus(1);
        
        $savedEntity = $this->repository->save($entity);
        
        $this->assertNotNull($savedEntity->getId());
        $this->assertEquals('New Entity', $savedEntity->getName());
    }

    /**
     * @magentoAppArea adminhtml
     * @magentoConfigFixture current_store {vendor}_{modulename}/general/enabled 1
     */
    public function testWithConfig(): void
    {
        // Test with specific config values
    }
}
```

## 4. Fixture File

`Test/Integration/_files/entity.php`

```php
<?php
use Magento\TestFramework\Helper\Bootstrap;
use {Vendor}\{ModuleName}\Model\{EntityName};
use {Vendor}\{ModuleName}\Api\{EntityName}RepositoryInterface;

$objectManager = Bootstrap::getObjectManager();
$repository = $objectManager->get({EntityName}RepositoryInterface::class);

$entity = $objectManager->create({EntityName}::class);
$entity->setId(1);
$entity->setName('Test Entity');
$entity->setStatus(1);

$repository->save($entity);
```

## Chạy Tests

```bash
# Chạy tất cả unit tests của module
vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist \
    app/code/{Vendor}/{ModuleName}/Test/Unit

# Chạy test file cụ thể
vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist \
    app/code/{Vendor}/{ModuleName}/Test/Unit/Model/{ClassName}Test.php

# Chạy test method cụ thể
vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist \
    --filter testMethodName \
    app/code/{Vendor}/{ModuleName}/Test/Unit/Model/{ClassName}Test.php

# Chạy integration tests
vendor/bin/phpunit -c dev/tests/integration/phpunit.xml.dist \
    app/code/{Vendor}/{ModuleName}/Test/Integration

# Generate code coverage
vendor/bin/phpunit -c dev/tests/unit/phpunit.xml.dist \
    --coverage-html var/coverage \
    app/code/{Vendor}/{ModuleName}/Test/Unit
```

## Common Annotations

| Annotation | Mô tả |
|------------|-------|
| `@magentoDataFixture` | Load fixture data |
| `@magentoDbIsolation enabled` | Rollback DB sau test |
| `@magentoAppArea frontend` | Set app area |
| `@magentoConfigFixture` | Set config values |
| `@magentoCache disabled` | Disable cache |
| `@dataProvider` | Provide test data |
| `@depends` | Test dependencies |
