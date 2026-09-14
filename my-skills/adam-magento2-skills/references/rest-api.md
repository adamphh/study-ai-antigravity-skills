# Tạo REST API

## Thông tin cần hỏi người dùng nếu chưa có

- HTTP method + endpoint path (VD: `POST /V1/webpos/order/sync`)
- Input fields (tên, kiểu dữ liệu, bắt buộc hay không)
- Output/response mong muốn
- Yêu cầu quyền truy cập (ACL resource), hay public/customer/admin token

## Cấu trúc output cần sinh

1. `etc/webapi.xml` — khai báo route, method, ACL resource
2. `Api/Data/{Name}Interface.php` — DTO interface cho input/output (nếu cần)
3. `Api/{Name}RepositoryInterface.php` hoặc `Api/{Name}ManagementInterface.php`
   tùy theo là CRUD hay action nghiệp vụ (VD: "sync" là action, không phải CRUD
   thuần, nên đặt tên Interface là `...ManagementInterface`)
4. Class implement interface trên, chứa logic thật
5. Khai báo `preference` trong `etc/di.xml` để map Interface → Class implement

## Mẫu cấu trúc webapi.xml

```xml
<?xml version="1.0"?>
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:Magento_Webapi:etc/webapi.xsd">
    <route url="/V1/{path}" method="{HTTP_METHOD}">
        <service class="{Vendor}\{Module}\Api\{Name}ManagementInterface"
                 method="{methodName}"/>
        <resources>
            <resource ref="{Vendor}_{Module}::{resource_name}"/>
        </resources>
    </route>
</routes>
```

## Lưu ý quan trọng

- Nếu endpoint dùng để POS client gọi (Webpos), cân nhắc:
  - Có cần `anonymous` resource không, hay bắt buộc customer/admin token
  - Idempotency: nếu POS retry request do mất mạng, API có xử lý trùng
    lặp không (VD: kiểm tra order đã sync chưa trước khi tạo lại)
- Validate input rõ ràng, throw `InputException` hoặc
  `LocalizedException` với message dễ hiểu cho client

## Checklist trước khi trả lời

- [ ] ACL resource được khai báo đúng trong `etc/acl.xml` (nhắc thêm nếu resource mới)
- [ ] Có xử lý idempotency nếu tác vụ có thể bị gọi lại nhiều lần
- [ ] Không dùng ObjectManager trực tiếp
