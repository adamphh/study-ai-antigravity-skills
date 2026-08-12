---
name: WebPOS Development Skills
description: Tập hợp các skills cần thiết cho việc customize WebPOS
---

# WebPOS Development Skills

Đây là tập hợp các hướng dẫn chi tiết cho việc customize WebPOS application.

## Danh sách Skills

### Customization Mechanisms

| Skill | Mô tả | Khi nào dùng |
|-------|-------|--------------|
| [create-plugin.md](./create-plugin.md) | Modify method có sẵn | Thay đổi behavior của method |
| [create-mixin.md](./create-mixin.md) | Thêm method mới vào class | Extend functionality |
| [create-layout.md](./create-layout.md) | Thêm UI vào customize point | Inject UI components |
| [create-event.md](./create-event.md) | Event/Observer pattern | Execute code tại các điểm |
| [create-rewrite.md](./create-rewrite.md) | Thay thế class hoàn toàn | Override nhiều methods |
| [create-component-reducer.md](./create-component-reducer.md) | Tạo Component, Reducer, Menu | Thêm page/feature mới |

---

## So sánh các Mechanism

| Mechanism | Purpose | Impact Level |
|-----------|---------|--------------|
| **Plugin** | Modify method behavior | Low |
| **Mixin** | Add new methods | Low |
| **Event** | Execute custom code | Low |
| **Layout** | Inject UI | Medium |
| **Rewrite** | Replace entire class | High |

### Thứ tự ưu tiên

1. **Plugin** - Ưu tiên cao nhất, ít conflict
2. **Mixin** - Thêm functionality an toàn
3. **Event** - Decouple logic
4. **Layout** - Cho UI injection
5. **Rewrite** - Cuối cùng, khi không có cách khác

---

## Cấu trúc Extension

```
src/extension/{extension_name}/
├── etc/
│   └── config.js           # Module config (plugin, mixin, layout, event, rewrite)
├── view/
│   ├── index.js            # Exports
│   ├── container.js        # Container components
│   ├── component.js        # Presentational components
│   └── reducer.js          # Redux reducer
├── service/
│   └── MyService.js        # Business logic
├── locales/
│   └── vi_vn/
│       └── translations.json
└── package.json            # Additional dependencies
```

---

## Config Template

```js
import ModuleConfigAbstract from "../../ModuleConfigAbstract";

class MyExtensionConfig extends ModuleConfigAbstract {
    module = ['myextension'];
    
    // Thêm method vào class
    mixin = {};
    
    // Modify method behavior
    plugin = {};
    
    // Inject UI
    layout = {};
    
    // Replace class
    rewrite = {};
    
    // Redux reducer
    reducer = {};
    
    // Menu item
    menu = {};
}

export default (new MyExtensionConfig());
```

---

## Các loại Class có thể customize

| Type | Factory | Ví dụ |
|------|---------|-------|
| `service` | ServiceFactory | UserService, OrderService |
| `resource_model` | ResourceModelFactory | CustomerResourceModel |
| `repository` | RepositoryFactory | ProductRepository |
| `container` | ContainerFactory | LoginContainer |
| `component` | ComponentFactory | MenuComponent |
| `data_resource` | DataResourceFactory | ConfigDataResource |
| `epic` | - | LocationEpic (chỉ rewrite) |

---

## Quy định Nạp Stock Offline & Xử lý Async Promise trong WebPOS Extension

1. **Truy vấn Tồn kho Offline Mode của Variant Product**:
   - Khi nạp sản phẩm con (variant) ở Offline Mode, `ProductService.getById` chỉ đọc từ bảng IndexedDB `db.product` mà không tự động JOIN dữ liệu tồn kho `db.stock`.
   - Nếu `targetProduct.stocks` bị khuyết (`undefined`), BẮT BUỘC phải gọi `StockService.getResourceModel().getResourceOffline().getStockProducts([productId])` để nạp tồn kho từ IndexedDB local trước khi thực thi `validateQty`.

2. **Chuyển đổi Async Promise cho QuoteService trong Redux Epics**:
   - Khi phương thức plugin `around` của `AddConfigurableProductService` (hoặc các AddProductService khác) chuyển thành `async function` (trả về `Promise`), BẮT BUỘC phải bổ sung plugin `around` cho `QuoteService.addProduct` trong `QuoteServicePlugin` để bọc chuyển đổi `Promise` thành RxJS `Observable` (`Observable.from(promise).flatMap(...)`), giúp Redux Epic (`AddProductEpic`) nhận đúng dữ liệu quote đã cập nhật.

---

## Quy tắc Thứ tự Thực thi khi Take Payment và Tạo Invoice (Backend)

1. **Lưu bản ghi thanh toán trước khi tạo Invoice**:
   - Khi viết hoặc tùy biến (`rewrite`/`plugin`) phương thức xử lý thanh toán bổ sung (`takePayment` / `processTakePaymentActionLog`) cho đơn hàng WebPOS, BẮT BUỘC phải thực thi hàm lưu bản ghi thanh toán vào bảng `webpos_order_payment` (`createWebposOrderPayment`) **TRƯỚC** khi gọi khởi tạo Invoice (`processInvoice`).
2. **Đảm bảo dữ liệu Observer đồng bộ**:
   - Không được gọi `processInvoice` khi các bản ghi giao dịch mới chưa được chèn vào bảng `webpos_order_payment`, nhằm tránh việc Observer `Magestore\Webpos\Observer\Order\Invoice\Pay` truy vấn dữ liệu DB cũ và ghi đè `total_paid` làm sai lệch `total_due` của đơn hàng.
3. **Cộng dồn `total_paid` chính xác**:
   - Trong hàm tính toán lại tổng tiền (`addPaymentToOrder`), phải luôn cộng số tiền đợt mới (`$takeAmount`) vào tổng tiền đã trả trước đó (`$oldOrder->getTotalPaid()`), không phụ thuộc đơn lẻ vào biến `pos_pre_total_paid`.

---

## Quy tắc Đặt tên Class cho Plugin, Rewrite và Observer (Class Naming Suffix Standard)

1. **Class Rewrite**: BẮT BUỘC phải thêm hậu tố `Rewrite` ở cuối tên Class.
   - *Ví dụ:* `CheckoutRepositoryRewrite`, `PosOrderRepositoryRewrite`.
2. **Class Plugin**: BẮT BUỘC phải thêm hậu tố `Plugin` ở cuối tên Class.
   - *Ví dụ:* `CheckoutRepositoryPlugin`, `OrderSavePlugin`.
3. **Class Observer**: BẮT BUỘC phải thêm hậu tố `Observer` ở cuối tên Class (hoặc trong thư mục `Observer`).
   - *Ví dụ:* `OrderInvoicePayObserver`, `SavePaymentObserver`.

---

## Commands


```bash
# Install dependencies
npm install

# Apply extension packages & translations
npm run upgrade

# Start development
npm start

# Build production
npm run build
```

