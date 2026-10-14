# Script Indexer — Router Hub (Tầng 1)

> Tra cứu nhanh vị trí các Class, Service, Epic, UI Component và Module trong hệ thống.
> Sử dụng Router Hub này để tìm đúng file index chi tiết trước khi đọc code.

---

## 1. Client Index (WebPOS Frontend)

| File Index | Phạm vi / Mô tả chức năng | Trạng thái |
| :--- | :--- | :--- |
| [`client/webpos-core/core-services.md`](client/webpos-core/core-services.md) | WebPOS Core Services (PrinterService, SessionService, CustomerService...) | ✅ Sẵn sàng |
| `client/webpos-core/core-epics-actions.md` | Redux Actions & Epics (Sync, Checkout, Cart, Order, Payment) | 🔲 TODO |
| `client/webpos-core/core-indexeddb.md` | IndexedDB Models, ObjectStores, Data Repositories | 🔲 TODO |
| `client/webpos-core/core-components.md` | WebPOS React UI Components, Modals, Forms, Layout Containers | 🔲 TODO |

---

## 2. Server Index (Magento 2 / Magestore Backend)

| File Index | Modules & Phạm vi chức năng | Trạng thái |
| :--- | :--- | :--- |
| [`server/vendor/magestore/payment.md`](server/vendor/magestore/payment.md) | Payment, PaymentOffline, WebposTyro, WebposZippay, WebposStripe, WebposStripeTerminal, WebposAuthorizenet, WebposPaynl | ✅ Sẵn sàng |
| [`server/vendor/magestore/customer-reward.md`](server/vendor/magestore/customer-reward.md) | Rewardpoints, RewardpointsGraphQl, WebposAmastyRewards | ✅ Sẵn sàng |
| [`server/vendor/magestore/giftvoucher.md`](server/vendor/magestore/giftvoucher.md) | Giftvoucher, GiftvoucherGraphQl | ✅ Sẵn sàng |
| [`server/vendor/magestore/report-analytics.md`](server/vendor/magestore/report-analytics.md) | PosReports, ReportSuccess, FulfilReport, WebposPerformance (AdminUi/Api) | ✅ Sẵn sàng |
| [`server/vendor/magestore/barcode.md`](server/vendor/magestore/barcode.md) | BarcodeSuccess | ✅ Sẵn sàng |
| [`server/vendor/magestore/click-and-collect.md`](server/vendor/magestore/click-and-collect.md) | ClickAndCollect (Admin/Frontend/API/GraphQL) | ✅ Sẵn sàng |
| [`server/vendor/magestore/foundation-support.md`](server/vendor/magestore/foundation-support.md) | Core, Logger, LoggerApi, LoggerGraphQl | ✅ Sẵn sàng |
| [`server/vendor/magestore/overview.md`](server/vendor/magestore/overview.md) | **Tất cả modules còn lại** (Webpos, OrderSuccess, BranchRequest, Inventory...) | ⚠️ Chưa tách (1.2MB) |
| `server/vendor/magestore/pos-core.md` | Webpos, WebposIntegration, WebposMobile, WebposShipping... | 🔲 TODO (tách từ overview) |
| `server/vendor/magestore/sales-order.md` | OrderSuccess, ProductExchange | 🔲 TODO (tách từ overview) |
| `server/vendor/magento/checkout.md` | Magento 2 Core Checkout & Sales APIs/Plugins | 🔲 TODO |
| `server/vendor/magento/inventory.md` | Magento 2 MSI (Multi-Source Inventory) APIs/Plugins | 🔲 TODO |

---

## 3. Project Indexes (Tầng 2 — theo dự án)

| Dự án | Router file | Trạng thái |
| :--- | :--- | :--- |
| P1115 — cremagarage-com-au | [`/mnt/projects/p1115-cremagarage-com-au/docs/data-flows/INDEX.md`](file:///mnt/projects/p1115-cremagarage-com-au/docs/data-flows/INDEX.md) | ✅ Sẵn sàng |
