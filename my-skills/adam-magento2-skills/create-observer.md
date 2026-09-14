---
name: Create Observer
description: Hướng dẫn tạo Observer trong Magento 2 để lắng nghe và xử lý events
---

# Tạo Observer trong Magento 2

Observer pattern cho phép bạn thực thi code khi một event cụ thể được dispatch trong hệ thống.

## Cấu trúc

```
{Vendor}/{ModuleName}/
├── etc/
│   ├── events.xml           # Global events
│   ├── frontend/
│   │   └── events.xml       # Frontend events
│   └── adminhtml/
│       └── events.xml       # Admin events
└── Observer/
    └── {ObserverName}.php
```

---

## Bước 1: Đăng ký Observer trong events.xml

### Global (cả frontend và admin)

`etc/events.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    
    <event name="catalog_product_save_after">
        <observer name="{vendor}_{modulename}_product_save"
                  instance="{Vendor}\{ModuleName}\Observer\ProductSaveObserver"/>
    </event>
    
</config>
```

### Frontend only

`etc/frontend/events.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    
    <event name="customer_login">
        <observer name="{vendor}_{modulename}_customer_login"
                  instance="{Vendor}\{ModuleName}\Observer\CustomerLoginObserver"/>
    </event>
    
</config>
```

### Admin only

`etc/adminhtml/events.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Event/etc/events.xsd">
    
    <event name="admin_user_authenticate_after">
        <observer name="{vendor}_{modulename}_admin_login"
                  instance="{Vendor}\{ModuleName}\Observer\AdminLoginObserver"/>
    </event>
    
</config>
```

---

## Bước 2: Tạo Observer Class

`Observer/{ObserverName}.php`

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Observer;

use Magento\Framework\Event\Observer;
use Magento\Framework\Event\ObserverInterface;
use Psr\Log\LoggerInterface;

class ProductSaveObserver implements ObserverInterface
{
    /**
     * @var LoggerInterface
     */
    private LoggerInterface $logger;

    /**
     * @param LoggerInterface $logger
     */
    public function __construct(
        LoggerInterface $logger
    ) {
        $this->logger = $logger;
    }

    /**
     * Execute observer
     *
     * @param Observer $observer
     * @return void
     */
    public function execute(Observer $observer): void
    {
        // Get event data
        $product = $observer->getEvent()->getProduct();
        
        // Access data from event
        $productId = $product->getId();
        $productName = $product->getName();
        
        // Your custom logic here
        $this->logger->info(
            sprintf('Product saved: ID=%s, Name=%s', $productId, $productName)
        );
    }
}
```

---

## Các Events phổ biến trong Magento 2

### Product Events

| Event Name | Mô tả | Data Available |
|------------|-------|----------------|
| `catalog_product_save_before` | Trước khi product được save | `product` |
| `catalog_product_save_after` | Sau khi product được save | `product` |
| `catalog_product_delete_before` | Trước khi product bị xóa | `product` |
| `catalog_product_delete_after` | Sau khi product bị xóa | `product` |

### Order Events

| Event Name | Mô tả | Data Available |
|------------|-------|----------------|
| `sales_order_place_before` | Trước khi đặt hàng | `order` |
| `sales_order_place_after` | Sau khi đặt hàng | `order` |
| `sales_order_save_after` | Sau khi order được save | `order` |
| `checkout_submit_all_after` | Sau khi checkout hoàn tất | `order`, `quote` |

### Customer Events

| Event Name | Mô tả | Data Available |
|------------|-------|----------------|
| `customer_login` | Sau khi customer đăng nhập | `customer` |
| `customer_logout` | Sau khi customer đăng xuất | `customer` |
| `customer_register_success` | Sau khi đăng ký thành công | `customer` |
| `customer_save_after` | Sau khi customer được save | `customer_data_object` |

### Cart Events

| Event Name | Mô tả | Data Available |
|------------|-------|----------------|
| `checkout_cart_add_product_complete` | Sau khi add product vào cart | `product`, `request` |
| `checkout_cart_product_add_after` | Sau khi add product vào cart | `quote_item`, `product` |
| `checkout_cart_update_items_before` | Trước khi update cart | `cart`, `info` |

---

## Ví dụ thực tế: Log Order Placement

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Observer\Sales;

use Magento\Framework\Event\Observer;
use Magento\Framework\Event\ObserverInterface;
use Psr\Log\LoggerInterface;
use Magento\Sales\Api\Data\OrderInterface;

class OrderPlaceAfterObserver implements ObserverInterface
{
    /**
     * @var LoggerInterface
     */
    private LoggerInterface $logger;

    /**
     * @param LoggerInterface $logger
     */
    public function __construct(
        LoggerInterface $logger
    ) {
        $this->logger = $logger;
    }

    /**
     * Log order placement
     *
     * @param Observer $observer
     * @return void
     */
    public function execute(Observer $observer): void
    {
        /** @var OrderInterface $order */
        $order = $observer->getEvent()->getOrder();
        
        if (!$order) {
            return;
        }

        $this->logger->info(
            'New Order Placed',
            [
                'order_id' => $order->getEntityId(),
                'increment_id' => $order->getIncrementId(),
                'customer_email' => $order->getCustomerEmail(),
                'grand_total' => $order->getGrandTotal(),
                'status' => $order->getStatus()
            ]
        );
    }
}
```

---

## Dispatch Custom Event

Bạn cũng có thể dispatch event của riêng mình:

```php
<?php
declare(strict_types=1);

namespace {Vendor}\{ModuleName}\Model;

use Magento\Framework\Event\ManagerInterface as EventManager;

class CustomService
{
    /**
     * @var EventManager
     */
    private EventManager $eventManager;

    /**
     * @param EventManager $eventManager
     */
    public function __construct(
        EventManager $eventManager
    ) {
        $this->eventManager = $eventManager;
    }

    /**
     * Process and dispatch event
     *
     * @param array $data
     * @return void
     */
    public function process(array $data): void
    {
        // Process logic here...
        
        // Dispatch custom event
        $this->eventManager->dispatch(
            '{vendor}_{modulename}_custom_event',
            [
                'custom_data' => $data,
                'timestamp' => time()
            ]
        );
    }
}
```

---

## Lưu ý quan trọng

> [!WARNING]
> **Performance**: Observer chạy synchronously, tránh đặt logic nặng trong observer. Sử dụng Message Queue cho heavy processing.

> [!TIP]
> **Best Practice**:
> - Đặt observer ở đúng area (global/frontend/adminhtml)
> - Sử dụng tên observer unique để tránh conflict
> - Return early nếu data không hợp lệ
> - Log errors để debug

> [!IMPORTANT]
> **Observer vs Plugin**:
> - Observer: Dùng khi cần react với event, không cần modify data
> - Plugin: Dùng khi cần modify input/output của method
