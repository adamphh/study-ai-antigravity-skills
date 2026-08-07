# 📚 Danh mục Luồng Dữ liệu (Data Flow Documentation Index)

Chào mừng bạn đến với tài liệu **Data Flow (Luồng xử lý dữ liệu)** cho hệ thống **Magestore WebPOS** (bao gồm WebPOS Client React/Redux và Backend Magento 2).

Mục đích của bộ tài liệu này nhằm cung cấp cho lập trình viên cái nhìn trực quan, dễ hiểu nhất về cách dữ liệu vận hành từ màn hình giao diện (UI Client) qua các lớp dịch vụ (Service/Epic/Redux) xuống tới Backend Magento 2 và Database.

---

## 🗺️ Danh sách các luồng dữ liệu (Data Flows)

| STT | Tên Luồng (Flow Name) | Mô tả tóm tắt | File Tài liệu |
| :--- | :--- | :--- | :--- |
| **01** | **Search Product by Barcode** | Luồng quét/nhập mã vạch sản phẩm, tìm kiếm từ giỏ hàng / IndexedDB / Server API và tự động thêm vào giỏ hàng. | [01-search-product-by-barcode.md](file:///mnt/projects/p1177-storksplows-com/docs/data-flows/01-search-product-by-barcode.md) |
| **02** | **Data Sync Mechanism** | Cơ chế đồng bộ dữ liệu ban đầu và định kỳ giữa Magento Backend và Client IndexedDB (Products, Categories, Customers, Stock,...). | [02-data-sync-mechanism.md](file:///mnt/projects/p1177-storksplows-com/docs/data-flows/02-data-sync-mechanism.md) |
| **03** | **Cart & Quote Lifecycle** | Vòng đời của Quote (Giỏ hàng): tạo mới, thêm/sửa/xóa item, tính giá, thuế, chiết khấu và custom price. | [03-cart-quote-lifecycle.md](file:///mnt/projects/p1177-storksplows-com/docs/data-flows/03-cart-quote-lifecycle.md) |
| **04** | **Checkout, Payment & Shipment** | Luồng thanh toán (Cash, Tyro/EFTPOS, Split Payment), tạo Order, xuất kho (Shipment) và hoàn tiền (Refund). | [04-checkout-payment-shipment.md](file:///mnt/projects/p1177-storksplows-com/docs/data-flows/04-checkout-payment-shipment.md) |

---

## 💡 Hướng dẫn xem & Đóng góp tài liệu

1. **Vẽ sơ đồ (Diagram):** Tất cả các luồng đều sử dụng chuẩn sơ đồ **Mermaid Sequence Diagram** giúp dễ dàng hình dung thứ tự gọi hàm.
2. **Quy ước ký hiệu:**
   - **Client App (React/Redux/Epic):** Nằm ở phía Frontend WebPOS.
   - **Offline Storage (IndexedDB):** Kho lưu trữ dữ liệu tại trình duyệt WebPOS.
   - **Server REST API (Magento 2):** Các API Endpoint xử lý ở backend PHP.
