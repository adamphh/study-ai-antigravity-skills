---
name: WebPOS Event Observer
description: Hướng dẫn sử dụng Event/Observer trong WebPOS
---

# WebPOS Event Observer

Event system cho phép tạo customize point và execute custom code.

## Fire Event (trong Core)

```js
import { fire } from "../src/event-bus";

// Fire event với data
fire('order_place_after', { order: orderData });

// Fire event không có data
fire('checkout_complete');
```

## Listen Event (trong Extension)

```js
import { listen } from "../src/event-bus";

// Listen event
listen('order_place_after', (eventData) => {
    console.log('Order placed:', eventData.order);
    // Custom logic
}, 'my_extension_order_listener');
```

## Tham số của listen()

| Param | Mô tả |
|-------|-------|
| `name_of_event` | Tên event (phải khớp với fire) |
| `observer` | Function xử lý event, nhận `eventData` |
| `listener_tag` | ID định danh listener (tránh duplicate) |

## Event Naming Convention

Format: `[object_type]_[object_name]_[action]_[position]`

| Event Name | Giải thích |
|------------|------------|
| `model_customer_save_after` | Sau khi save customer model |
| `service_order_validate_before` | Trước khi validate order |
| `component_cart_render_after` | Sau khi render cart component |
| `checkout_payment_select` | Khi chọn payment method |

## Ví dụ thực tế

### Logging order

```js
import { listen } from "../src/event-bus";

// Log tất cả orders
listen('order_place_after', (eventData) => {
    const { order } = eventData;
    console.log(`Order #${order.id} placed. Total: ${order.total}`);
    
    // Send to analytics
    analytics.track('order_placed', {
        orderId: order.id,
        total: order.total
    });
}, 'analytics_order_tracking');
```

### Validate before action

```js
listen('checkout_submit_before', (eventData) => {
    const { cart } = eventData;
    
    if (cart.items.length === 0) {
        throw new Error('Cart is empty');
    }
    
    // Thêm validation logic
}, 'custom_checkout_validation');
```

### Modify data

```js
listen('product_add_to_cart_before', (eventData) => {
    const { product, qty } = eventData;
    
    // Apply custom discount
    if (product.category === 'clearance') {
        product.price = product.price * 0.8;
    }
    
    return eventData;
}, 'clearance_discount_handler');
```

## Listener Tag

Listeners với cùng tag sẽ bị override. Chỉ listener cuối cùng với tag đó active:

```js
// Listener 1 - bị override
listen('order_save', handler1, 'order_handler');

// Listener 2 - active
listen('order_save', handler2, 'order_handler');
```

## Best Practices

1. **Naming**: Dùng format chuẩn cho event name
2. **Tag**: Dùng unique tag để tránh conflict
3. **Performance**: Không làm heavy logic trong observer
4. **Error handling**: Wrap logic trong try/catch
