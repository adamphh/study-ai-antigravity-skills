# PHP Coding Standards & Formatting Invariants

## 1. Strict Types Declaration
Mỗi file `.php` khi được sinh mới hoặc tùy chỉnh phải khai báo `declare(strict_types=1);` ngay phía dưới khối comment Copyright Header, cách 1 dòng trống trước `namespace`:

```php
<?php
/**
 * Copyright © Magestore. All rights reserved.
 * See COPYING.txt for license details.
 */

declare(strict_types=1);

namespace Magestore\Fixbug\...;
```

## 2. No Class DocBlock / Comment Rule
Tuyệt đối KHÔNG viết khối comment (DocBlock) cho `class`. Khai báo `class` trực tiếp ngay sau khối `use`.

## 3. Customization Inline Comment Rule
Luôn bổ sung comment bằng tiếng Anh giải thích đoạn code được tùy chỉnh/ghi đè so với class gốc, bao gồm logic gốc và logic tùy chỉnh mới.
