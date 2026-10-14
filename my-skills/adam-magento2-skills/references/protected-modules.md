# Danh sách Module Core Magestore — KHÔNG được sửa trực tiếp

File này liệt kê các module core thuộc Magestore/Webpos. Khi sinh hoặc
chỉnh sửa code, Claude PHẢI kiểm tra file này trước — nếu đường dẫn/class
liên quan thuộc 1 trong các module dưới đây, KHÔNG được:

- Sửa trực tiếp file trong thư mục module đó
- Thêm/xoá method, đổi logic trong class gốc của module đó
- Ghi đè (preference) lên class của module đó trừ khi được yêu cầu rõ ràng
  và đã cảnh báo rủi ro

Thay vào đó, PHẢI đề xuất 1 trong các cách sau (đặt trong module custom
RIÊNG, không đặt trong module core):

- Dùng **Plugin** (xem `plugin.md`) để can thiệp before/after/around
- Dùng **Observer** (xem `event-observer.md`) nếu có event phù hợp
- Dùng **Virtual Type** (xem `preference-virtualtype.md`) nếu chỉ cần đổi
  dependency được inject, không cần đổi class
- Chỉ dùng **Preference** khi thực sự bắt buộc, và phải cảnh báo rõ rủi ro
  conflict + khó nâng cấp

---

## Danh sách module core (điền theo dự án thực tế của bạn)

| Vendor_Module | Đường dẫn (app/code hoặc vendor) | Ghi chú |
|---|---|---|
| Magestore_Core | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Appadmin | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_BarcodeSuccess | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_BranchRequest | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposIntegration | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Webpos | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_ClickAndCollectApi | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_ClickAndCollect | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_ClickAndCollectGraphQl | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_ClickAndCollectHyva | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_AdjustStock | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_CoreFrontend | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Customercredit | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_CustomercreditGraphQl | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_CustomercreditHyva | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_Deli | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_OrderSuccess | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_FulfilSuccess | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_FulfilReport | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Giftvoucher | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_GiftvoucherGraphQl | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_GiftvoucherHyva | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_InventoryMovement | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_InventoryMovementAdminUi | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_InventoryMovementApi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_LoggerApi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Logger | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_LoggerGraphQl | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_SupplierSuccess | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Payment | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_PaymentOffline | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_ReportSuccess | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_DropshipSuccess | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_PosReports | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Rewardpoints | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_RewardpointsGraphQl | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_RewardpointsHyva | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_SalesReport | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_SecondDisplay | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_Stocktaking | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_PurchaseOrderSuccess | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_TransferStock | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_ClickAndCollectAdminUi | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposAdyenTerminal | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_WebposAmastyRewards | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposAuthorizenet | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposStripe | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposClarity | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposDojo | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposDojoAdminUi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposImport | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_ClickAndCollectFrontend | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposMobile | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_WebposMonerisApi | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposPerformanceAdminUi | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposMoneris | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_WebposMonerisGraphQl | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposPaynl | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPaynlCore | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPaynlTerminalApi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPaynlTerminalAdminUi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPaynlTerminal | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPaynlTerminalGraphQl | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPerformance | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_WebposMonerisAdminUi | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposPerformanceApi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPusherApi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPusherAdminUi | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposPusher | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposSellPrePrintedGiftCard | app/code/Magestore/Core | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposShipping | app/code/Magestore/Webpos | Module lõi POS, không sửa trực tiếp |
| Magestore_WebposSquareApi | app/code/Magestore/WebposSuccess | Module core license/success page |
| Magestore_WebposSquareAdminUi | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposSquare | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposSquareGraphQl | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposStripeTerminal | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposTyro | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |
| Magestore_WebposZippay | app/code/Magestore/Webposgraphql | Module core GraphQL cho Webpos |

> Đây là ví dụ mẫu — hãy thay bằng danh sách module core thật của dự án bạn
> (chạy `ls app/code/Magestore/` hoặc `bin/magento module:status` để lấy
> danh sách chính xác, rồi cập nhật bảng trên).

---

## Cách Claude phải xử lý khi phát hiện yêu cầu đụng vào module trong danh sách

1. Dừng lại, không sinh code sửa trực tiếp vào module đó
2. Thông báo rõ cho người dùng: "Class/method này thuộc module core
   {Tên module}, không nên sửa trực tiếp"
3. Đề xuất phương án thay thế (Plugin/Observer/Virtual Type) đặt trong
   module custom riêng (hỏi tên module custom nếu chưa rõ, hoặc dùng
   module custom mặc định của dự án nếu đã biết)
4. Chỉ tiến hành sửa trực tiếp nếu người dùng xác nhận rõ ràng là cố ý
   muốn sửa module core (VD: đang phát triển ngay trong module đó, không
   phải mở rộng từ module khác)
