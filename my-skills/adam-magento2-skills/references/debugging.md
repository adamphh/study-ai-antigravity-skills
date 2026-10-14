# Debug lỗi Magento

## Quy trình phân tích

1. Đọc kỹ stack trace, xác định:
   - File/class/method nơi lỗi xảy ra
   - Đây là code core (`vendor/magento/...`) hay code custom
     (`app/code/...`) của người dùng
2. Nếu lỗi nằm ở custom code: phân tích trực tiếp đoạn code được cung cấp
3. Nếu lỗi nằm ở core: xác định core class đó đang được gọi từ đâu trong
   custom code (thường do Plugin/Observer/Preference can thiệp sai)
4. Đề xuất fix, LUÔN ưu tiên phương án không sửa core:
   - Sửa trong Plugin/Observer của module custom
   - Nếu bắt buộc phải thay đổi hành vi core, cân nhắc lại giữa
     Plugin (an toàn hơn, dễ maintain khi upgrade) và Preference
     (rủi ro conflict cao hơn)

## Các lỗi thường gặp cần lưu ý đặc biệt

- **"Area code not set"**: thường do chạy script/cron ngoài context chuẩn
  của Magento, cần set area code trước khi dùng service
- **Lỗi DI "Circular dependency"**: do 2 class inject lẫn nhau, cần refactor
  tách interface hoặc dùng Proxy
- **Lỗi sau khi upgrade Magento**: kiểm tra core class liên quan có đổi
  signature method không (nhất là khi dùng Preference/Plugin trên class đó)
- **Lỗi liên quan Webpos sync**: kiểm tra thứ tự transaction — order có
  được commit vào DB trước khi job đồng bộ đọc không (race condition)

## Định dạng câu trả lời

1. Nguyên nhân gốc (root cause) — ngắn gọn, rõ ràng
2. Class/method liên quan (core hoặc custom)
3. Đề xuất fix cụ thể kèm code nếu cần
4. Cảnh báo rủi ro nếu fix có thể ảnh hưởng chỗ khác
