---
name: adam-build-clone-site
description: Dựng môi trường Docker và cài đặt website Magento clone từ tệp mã nguồn nén (--source) và database dump (--database). Tự động phân bổ port tránh xung đột, detect phiên bản PHP, sửa lỗi tương thích MySQL 8.4, dọn dẹp orphan ACL rules, và deploy static content đa ngôn ngữ với script tối ưu token.
---

# Workflow: Dựng Môi Trường Docker & Cài Đặt Magento Clone

Sử dụng skill này khi người dùng chạy `/adam-build-clone-site`, `/build-clone-site`, `build clone site`, hoặc yêu cầu dựng website Magento clone từ archive mã nguồn và database dump export.

Skill được tích hợp sẵn bộ script tự động hóa nhằm tối ưu hóa 95% lượng token tiêu thụ và đảm bảo quy trình chạy thông suốt không bị lỗi phân mảnh.

---

## 1. Cú Pháp & Tham Số Hỗ Trợ

```bash
/adam-build-clone-site --source <tên_tệp_nguồn> --database <tên_tệp_csdl> [tùy_chọn]
```

### Các tham số:
- `--source <path>`: Đường dẫn tệp nén mã nguồn (`.tar.gz`, `.zip`, `.tar`). **(Bắt buộc)**
- `--database <path>`: Đường dẫn tệp database dump (`.sql.gz`, `.sql`). **(Bắt buộc)**
- `--template <path>`: Thư mục template Docker (mặc định: `resources/` của skill, fallback `/var/www/magento247p1`).
- `--base-url <url>`: URL cơ sở mong muốn (mặc định: `http://127.0.0.1:<port>/`).
- `--admin-user <user>`: Tên tài khoản quản trị cần tạo (mặc định: `admin`).
- `--admin-pass <pass>`: Mật khẩu quản trị (mặc định: `admin123@`).
- `--admin-email <email>`: Email quản trị (mặc định: `admin@example.com`).
- `--port-nginx <port>`, `--port-pma <port>`, `--port-mailhog <port>`, `--port-es <port>`: Chỉ định port cố định nếu không muốn tự động quét port rảnh.
- `--skip-docker`: Bỏ qua bước tạo Docker configs và khởi động container khi môi trường Docker đã có sẵn trên máy (chỉ extract source, import DB, cấu hình và deploy Magento).
- `--container-prefix <prefix>`: Tiền tố tên container (mặc định lấy theo tên thư mục hiện tại, ví dụ: `<prefix>-php`, `<prefix>-db`). Dùng khi container có sẵn đặt tên khác tên thư mục.

---

## 2. Cách Thực Thi Tối Ưu Token Cho AI Assistant

Khi người dùng kích hoạt skill, AI Assistant **không chạy từng lệnh phân mảnh** vào context. Thay vào đó, AI Assistant thực thi trực tiếp script điều phối:

```bash
bash /home/bss/.gemini/config/skills/adam-build-clone-site/scripts/run_clone.sh \
  --source <source_file> \
  --database <database_file> \
  [các tham số khác nếu có]
```

Toàn bộ chi tiết kỹ thuật nặng (progress bar của compile, deploy, sed SQL dump) sẽ được script tự động ghi ra tệp `clone.log` tại thư mục hiện tại và chỉ in ra màn hình bảng tóm tắt kết quả cuối cùng.

---

## 3. Các Bước Tự Động Hóa Được Đóng Gói Bên Trong Script

1. **Phân bổ cổng mạng thông minh (Dynamic Port Allocation):**
   - Quét danh sách cổng đang lắng nghe (`netstat`/`ss`).
   - Tự động chọn cổng rảnh tiếp theo cho Nginx (bắt đầu từ 2471), phpMyAdmin (8145), MailHog (9445), Elasticsearch (29208).
   - Đặt prefix container và network theo tên thư mục hiện hành.
2. **Phát hiện phiên bản PHP & SourceGuardian Loader:**
   - Đọc `composer.lock` từ source archive để nhận diện phiên bản PHP yêu cầu (PHP 8.1 vs PHP 8.2).
   - Khởi tạo `php/Dockerfile` tương ứng (`php:8.2-fpm` hoặc `php:8.1-fpm`), tích hợp `libicu-dev` và chép loader SourceGuardian (`ixed.8.2.lin` hoặc `ixed.8.1.lin`) vào đúng thư mục extension nội bộ.
3. **Cấu hình Nginx chống vỡ giao diện:**
   - Khai báo document root tại `$base/pub`.
   - Bổ sung sẵn rewrite rules cho cả `/pub/static/` và `/pub/media/` trỏ về `/static/$1` và `/media/$1` để tương thích ngược 100% với các plugin gọi link cũ.
4. **Giải nén mã nguồn & Cấp quyền:**
   - Nhận diện nếu archive chứa thư mục wrapper gốc (như `magento/app`) để tự động áp dụng `--strip-components=1`.
   - Chuẩn bị đầy đủ các thư mục ghi: `var/`, `generated/`, `pub/static/`, `pub/media/`.
5. **Khởi động Docker & Xử lý tương thích MySQL 8.4:**
   - Khởi chạy các container: `php`, `nginx`, `db` (MySQL 8), `elasticsearch`, `redis`, `phpmyadmin`, `mailhog`.
   - Chờ MySQL sẵn sàng (`mysqladmin ping`).
   - Bật `log_bin_trust_function_creators = 1`.
   - Lọc bỏ cờ `NO_AUTO_CREATE_USER` không còn tồn tại trên MySQL 8+.
   - Tự động sửa lỗi thiếu UNIQUE index trên bảng `indexer_state(indexer_id)` để thỏa mãn ràng buộc khóa ngoại (foreign key) khắt khe của MySQL 8.4 từ bảng `piimega_healthmonitor_indexer_history`.
   - Import dữ liệu database vào MySQL.
6. **Cấu hình `di.xml` & `env.php`:**
   - Bổ sung pattern `^8\.4\.` vào `SqlVersionProvider` trong `app/etc/di.xml`.
   - Tạo `app/etc/env.php` kết nối DB `db`, Redis `redis:6379`, Elasticsearch `elasticsearch:9200` và `piimega_elasticsearch`.
7. **Chuẩn hóa dữ liệu `core_config_data` & Dọn dẹp ACL:**
   - Trỏ `web/unsecure/base_url` và `web/secure/base_url` về Base URL mới.
   - Xóa bỏ các cấu hình gán cứng `base_static_url` và `base_media_url` tránh lỗi 404 static content.
   - Chuyển `caching_application` về 1 (Built-in cache).
   - Dọn dẹp các rule mồ côi (orphan rules) trong `authorization_rule`:
     `DELETE FROM authorization_rule WHERE role_id NOT IN (SELECT role_id FROM authorization_role);`
     tránh lỗi `LogicException: Could not create an acl object: Role '9' not found`.
8. **Biên dịch & Deploy đa ngôn ngữ:**
   - Chạy `setup:upgrade --keep-generated` dưới user `www-data`.
   - Chạy `setup:di:compile` dưới user `www-data`.
   - Tự động phát hiện toàn bộ các locale đang sử dụng trong database (ví dụ `fi_FI`, `sv_SE`, `en_US`, `nb_NO`) và deploy đầy đủ:
     `setup:static-content:deploy -f <locales...>`.
   - Tạo hoặc cập nhật tài khoản quản trị mặc định: `admin` / `admin123@`.
   - Dọn sạch cache và reindex các bảng chính.
9. **Kiểm tra sức khỏe hệ thống (Health Check):**
   - Kiểm tra mã phản hồi HTTP của Frontend và Admin Panel.
   - Xuất bảng thông tin dịch vụ và tài khoản quản trị cho người dùng.
