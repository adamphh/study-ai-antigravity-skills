---
name: Create Magento 2 Controller
description: Hướng dẫn tạo Controller trong Magento 2 (Frontend và Admin)
---

# Tạo Controller Magento 2

## Cấu trúc URL trong Magento 2

```
{base_url}/{frontName}/{controller}/{action}
```

Ví dụ: `https://example.com/catalog/product/view` 
- frontName: `catalog`
- controller: `product`
- action: `view`

---

## Frontend Controller

### Bước 1: Khai báo routes trong etc/frontend/routes.xml

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="standard">
        <route id="{route_id}" frontName="{front_name}">
            <module name="{Vendor}_{ModuleName}" />
        </route>
    </router>
</config>
```

### Bước 2: Tạo Controller Action

Đường dẫn: `Controller/{ControllerName}/{ActionName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Controller\{ControllerName};

use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\App\RequestInterface;
use Magento\Framework\View\Result\PageFactory;
use Magento\Framework\View\Result\Page;

class {ActionName} implements HttpGetActionInterface
{
    /**
     * @var PageFactory
     */
    private PageFactory $resultPageFactory;

    /**
     * @var RequestInterface
     */
    private RequestInterface $request;

    /**
     * @param PageFactory $resultPageFactory
     * @param RequestInterface $request
     */
    public function __construct(
        PageFactory $resultPageFactory,
        RequestInterface $request
    ) {
        $this->resultPageFactory = $resultPageFactory;
        $this->request = $request;
    }

    /**
     * Execute action
     *
     * @return Page
     */
    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->getConfig()->getTitle()->set(__('Page Title'));
        
        return $resultPage;
    }
}
```

---

## Admin Controller

### Bước 1: Khai báo routes trong etc/adminhtml/routes.xml

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="admin">
        <route id="{route_id}" frontName="{front_name}">
            <module name="{Vendor}_{ModuleName}" />
        </route>
    </router>
</config>
```

### Bước 2: Tạo Admin Controller Action

Đường dẫn: `Controller/Adminhtml/{ControllerName}/{ActionName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Controller\Adminhtml\{ControllerName};

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\View\Result\PageFactory;
use Magento\Framework\View\Result\Page;

class {ActionName} extends Action
{
    /**
     * Authorization level
     */
    public const ADMIN_RESOURCE = '{Vendor}_{ModuleName}::{resource_id}';

    /**
     * @var PageFactory
     */
    private PageFactory $resultPageFactory;

    /**
     * @param Context $context
     * @param PageFactory $resultPageFactory
     */
    public function __construct(
        Context $context,
        PageFactory $resultPageFactory
    ) {
        parent::__construct($context);
        $this->resultPageFactory = $resultPageFactory;
    }

    /**
     * Execute action
     *
     * @return Page
     */
    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu('{Vendor}_{ModuleName}::{menu_id}');
        $resultPage->getConfig()->getTitle()->prepend(__('Admin Page Title'));
        
        return $resultPage;
    }
}
```

---

## Các loại Action Interface

| Interface | HTTP Method | Mục đích |
|-----------|-------------|----------|
| `HttpGetActionInterface` | GET | Lấy dữ liệu, hiển thị trang |
| `HttpPostActionInterface` | POST | Gửi form, tạo dữ liệu |
| `HttpPutActionInterface` | PUT | Cập nhật dữ liệu |
| `HttpDeleteActionInterface` | DELETE | Xóa dữ liệu |

---

## Các loại Result Type

```php
// Page Result
$this->resultPageFactory->create();

// JSON Result
$this->resultJsonFactory->create()->setData(['success' => true]);

// Redirect Result
$this->resultRedirectFactory->create()->setPath('*/*/index');

// Raw Result
$this->resultRawFactory->create()->setContents('raw content');

// Forward Result
$this->resultForwardFactory->create()->forward('anotherAction');
```

---

## Lưu ý quan trọng

1. **CSRF Protection**: POST actions tự động được bảo vệ CSRF trong Magento 2.4+
2. **ACL**: Admin controllers phải định nghĩa `ADMIN_RESOURCE` để kiểm tra quyền truy cập
3. **Naming Convention**: Tên file Action phải trùng với tên class
4. **Request Validation**: Sử dụng `$this->getRequest()->getParams()` để lấy parameters
