# Tạo GraphQL Query / Mutation

## Thông tin cần hỏi người dùng nếu chưa có

- Loại: query hay mutation
- Tên field
- Input arguments (tên, kiểu, required hay không)
- Output type/fields mong muốn
- Có cần authentication (customer token) không

## Cấu trúc output cần sinh

1. `etc/schema.graphqls` — khai báo type, input, query/mutation
2. `Model/Resolver/{Name}Resolver.php` implement
   `Magento\Framework\GraphQl\Query\ResolverInterface`
3. Nếu cần output type phức tạp, cân nhắc thêm
   `Model/Resolver/DataProvider/{Name}.php` để tách logic lấy data ra khỏi resolver

## Mẫu cấu trúc

```graphql
type Query {
    {fieldName}(
        {arg}: String! @doc(description: "{mô tả}")
    ): {OutputType} @resolver(class: "{Vendor}\\{Module}\\Model\\Resolver\\{Name}Resolver") @doc(description: "{mô tả}")
}

type {OutputType} {
    {field}: String @doc(description: "{mô tả}")
}
```

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Model\Resolver;

use Magento\Framework\GraphQl\Config\Element\Field;
use Magento\Framework\GraphQl\Exception\GraphQlInputException;
use Magento\Framework\GraphQl\Exception\GraphQlNoSuchEntityException;
use Magento\Framework\GraphQl\Query\ResolverInterface;
use Magento\Framework\GraphQl\Schema\Type\ResolveInfo;

class {Name}Resolver implements ResolverInterface
{
    public function __construct(
        private readonly SomeDependencyInterface $dependency
    ) {
    }

    public function resolve(
        Field $field,
        $context,
        ResolveInfo $info,
        array $value = null,
        array $args = null
    ) {
        if (empty($args['{arg}'])) {
            throw new GraphQlInputException(__('{arg} is required'));
        }

        // logic, throw GraphQlNoSuchEntityException nếu không tìm thấy entity

        return [
            '{field}' => $result,
        ];
    }
}
```

## Checklist trước khi trả lời

- [ ] Dùng đúng exception chuẩn GraphQL (GraphQlInputException,
      GraphQlNoSuchEntityException, GraphQlAuthorizationException)
- [ ] Validate input đầy đủ trước khi xử lý logic
- [ ] Không dùng ObjectManager trực tiếp
