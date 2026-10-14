# Tạo Database Schema (Declarative Schema)

## Thông tin cần hỏi người dùng nếu chưa có

- Tên bảng
- Danh sách cột + kiểu dữ liệu
- Khoá chính
- Index / Foreign key cần thiết
- Có cần Repository pattern đầy đủ (Api interface) hay chỉ cần Model/ResourceModel/Collection đơn giản

## Nguyên tắc

- LUÔN dùng `db_schema.xml` (declarative schema), KHÔNG dùng
  `InstallSchema`/`UpgradeSchema` (pattern cũ, không nên dùng cho module mới)
- Nếu cần data mặc định (seed data), dùng `Setup/Patch/Data/{Name}.php`
  implement `DataPatchInterface`, KHÔNG dùng `InstallData`
- Nếu cần thay đổi schema sau này, thêm patch mới trong
  `Setup/Patch/Schema/`, KHÔNG sửa trực tiếp `db_schema.xml` cũ (phải thêm
  version mới trong `db_schema_whitelist.json` khi generate)

## Cấu trúc output cần sinh

1. `etc/db_schema.xml`
2. `etc/db_schema_whitelist.json` (nhắc người dùng chạy lệnh
   `bin/magento setup:db-declaration:generate-whitelist` để tự sinh,
   không tự bịa nội dung file này)
3. Model (`Model/{Name}.php`) extends `AbstractModel`
4. ResourceModel (`Model/ResourceModel/{Name}.php`) extends `AbstractDb`
5. Collection (`Model/ResourceModel/{Name}/Collection.php`) extends
   `AbstractCollection`
6. Nếu người dùng cần Repository pattern: sinh thêm
   `Api/Data/{Name}Interface.php`, `Api/{Name}RepositoryInterface.php`,
   `Model/{Name}Repository.php`, và khai báo trong `etc/di.xml`
   (preference cho interface)

## Mẫu cấu trúc db_schema.xml

```xml
<?xml version="1.0"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Setup/Declaration/Schema/etc/schema.xsd">
    <table name="{table_name}" resource="default" engine="innodb"
           comment="{Mô tả bảng}">
        <column xsi:type="int" name="entity_id" unsigned="true" nullable="false"
                identity="true" comment="Entity ID"/>
        <!-- các cột khác -->
        <constraint xsi:type="primary" referenceId="PRIMARY">
            <column name="entity_id"/>
        </constraint>
    </table>
</schema>
```

## Checklist trước khi trả lời

- [ ] Dùng declarative schema, không dùng InstallSchema
- [ ] Có nhắc người dùng chạy `setup:upgrade` sau khi thêm file
- [ ] Nếu có foreign key tới bảng core (VD: `sales_order`), cân nhắc
      `onDelete` phù hợp (thường là CASCADE hoặc SET NULL tùy nghiệp vụ)
