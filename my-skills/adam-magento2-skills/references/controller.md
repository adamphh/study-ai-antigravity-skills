# Tạo Controller Action (Backend/Frontend)

## Quy trình thực hiện

1. Khai báo route trong `etc/frontend/routes.xml` (Frontend) hoặc `etc/adminhtml/routes.xml` (Adminhtml).
2. Tạo class Controller Action:
   - Frontend: Implement `Magento\Framework\App\Action\HttpGetActionInterface` hoặc `HttpPostActionInterface` (khuyến khích từ Magento 2.3+ thay vì kế thừa class Action cũ).
   - Backend/Adminhtml: Kế thừa từ `Magento\Backend\App\Action`.
3. Thực thi logic xử lý và trả về kết quả (JSON, Page, Redirect) trong `execute()`.

## Cấu trúc mẫu

### etc/frontend/routes.xml (Đăng ký route Frontend)
```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="standard">
        <route id="custom_route" frontName="customroute">
            <module name="{Vendor}_{Module}"/>
        </route>
    </router>
</config>
```

### Controller/Index/CustomJson.php (Frontend Action trả về JSON)
```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Controller\Index;

use Magento\Framework\App\Action\HttpGetActionInterface;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Controller\Result\Json;

class CustomJson implements HttpGetActionInterface
{
    public function __construct(
        private readonly JsonFactory $resultJsonFactory
    ) {
    }

    /**
     * Execute controller action
     */
    public function execute(): Json
    {
        $resultJson = $this->resultJsonFactory->create();
        return $resultJson->setData([
            'success' => true,
            'message' => __('JSON Response from Custom Action')
        ]);
    }
}
```

### Controller/Adminhtml/Index/CustomAdmin.php (Adminhtml Action trả về JSON)
```php
<?php
declare(strict_types=1);

namespace {Vendor}\{Module}\Controller\Adminhtml\Index;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Controller\Result\Json;

class CustomAdmin extends Action
{
    // Khai báo ADMIN_RESOURCE để kiểm tra quyền truy cập ACL trong Admin
    public const ADMIN_RESOURCE = '{Vendor}_{Module}::config';

    public function __construct(
        Context $context,
        private readonly JsonFactory $resultJsonFactory
    ) {
        parent::__construct($context);
    }

    /**
     * Execute admin action
     */
    public function execute(): Json
    {
        $resultJson = $this->resultJsonFactory->create();
        return $resultJson->setData([
            'success' => true,
            'message' => __('Admin Controller Response')
        ]);
    }
}
```

## Checklist trước khi trả lời

- [ ] Đối với Frontend Controller, luôn sử dụng Action Interface cụ thể (`HttpGetActionInterface`, `HttpPostActionInterface`) thay vì kế thừa class `Action` trừu tượng cũ.
- [ ] Đối với Adminhtml Controller, bắt buộc định nghĩa hằng số `ADMIN_RESOURCE` để kiểm tra phân quyền ACL. Nếu bỏ qua sẽ dẫn đến lỗ hổng bảo mật truy cập trái phép.
- [ ] Luôn sử dụng các Result Factory (`JsonFactory`, `PageFactory`, `RedirectFactory`) thông qua constructor injection để khởi tạo đối tượng trả về.
