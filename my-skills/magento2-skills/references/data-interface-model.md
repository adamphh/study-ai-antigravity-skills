# Sinh Data Interface + Model + Preference (tự động từ field bảng)

Đây là tác vụ có thể **tự động hoá bằng script** thay vì viết tay từng
getter/setter — dùng `scripts/generate_data_interface.py` để đảm bảo chính
xác 100% theo field, không bỏ sót, không sai kiểu dữ liệu.

## Khi nào dùng script này

Dùng khi người dùng cần: Api Data Interface (chứa hằng số field + khai báo
getter/setter) + Model implement interface đó + đoạn `di.xml` preference
tương ứng, dựa trên field của 1 bảng đã có (hoặc sắp có).

## Thông tin cần có trước khi chạy script

- Vendor, Module, tên entity/class (VD: Vendor=Magestore, Module=Webpos,
  Name=OrderSyncQueue)
- Tên bảng
- Danh sách field: lấy từ 1 trong 2 nguồn:
  - **Có sẵn `db_schema.xml`**: hỏi người dùng đường dẫn file, hoặc nếu
    người dùng đã paste nội dung trong hội thoại, lưu ra file tạm rồi dùng
    `--schema-file`
  - **Chưa có file**: hỏi người dùng liệt kê field (tên + kiểu dữ liệu:
    int/varchar/text/decimal/timestamp/datetime/boolean...), tự tạo file
    JSON tạm theo mẫu bên dưới rồi dùng `--fields-json`

## Cách chạy

```bash
# Cách 1: đọc từ db_schema.xml có sẵn
python3 scripts/generate_data_interface.py \
    --schema-file /path/to/db_schema.xml \
    --table {ten_bang} \
    --vendor {Vendor} --module {Module} --name {Name} \
    --output-dir ./output

# Cách 2: tự khai báo field qua JSON khi chưa có db_schema.xml
python3 scripts/generate_data_interface.py \
    --fields-json fields.json \
    --table {ten_bang} \
    --vendor {Vendor} --module {Module} --name {Name} \
    --output-dir ./output
```

Mẫu `fields.json`:

```json
[
  {"name": "entity_id", "xsi_type": "int", "primary": true},
  {"name": "order_id", "xsi_type": "int"},
  {"name": "status", "xsi_type": "varchar"},
  {"name": "synced_at", "xsi_type": "timestamp"}
]
```

Các `xsi_type` được hỗ trợ (map sang PHP type tương ứng): `int`, `smallint`,
`tinyint` → `int`; `boolean` → `bool`; `decimal` → `float`; `varchar`,
`text`, `mediumtext`, `longtext`, `date`, `datetime`, `timestamp`, `blob`
→ `string`.

## Output của script

3 file trong thư mục `--output-dir`:
- `{Name}Interface.php` — Api Data Interface với const field + khai báo
  getter/setter
- `{Name}.php` — Model extends `AbstractModel`, implement Interface, dùng
  `$this->getData()`/`$this->setData()` cho từng field
- `di_xml_snippet.xml` — đoạn `<preference>` cần thêm vào `etc/di.xml`

## Việc cần làm SAU khi chạy script (Claude tự thực hiện tiếp)

1. Đọc lại nội dung 3 file vừa sinh, hiển thị cho người dùng
2. Nhắc rằng Model cần có `ResourceModel` tương ứng
   (`Model/ResourceModel/{Name}.php` extends `AbstractDb`) — nếu chưa có,
   hỏi người dùng có cần sinh luôn không (tham khảo `db-schema.md`)
3. Nhắc người dùng merge đoạn `<preference>` trong `di_xml_snippet.xml`
   vào file `etc/di.xml` thật của module (không tự ý ghi đè toàn bộ
   `di.xml` nếu file đó đã có nội dung khác)
4. Review lại kiểu dữ liệu PHP được suy ra có đúng nghiệp vụ không (VD:
   trường `status` có thể cần là enum/const thay vì string thuần — hỏi
   lại người dùng nếu cần bổ sung validate)

## Giới hạn cần lưu ý

- Script không tự tạo `ResourceModel`/`Collection` — chỉ tập trung vào
  Interface + Model + preference. Nếu cần đủ bộ (bao gồm bảng, resource
  model, collection), kết hợp với `db-schema.md`
- Trường có thể NULL sẽ có getter trả về kiểu `?type` (nullable) — nếu
  field bắt buộc luôn có giá trị, có thể điều chỉnh lại bỏ dấu `?` sau khi
  sinh xong
