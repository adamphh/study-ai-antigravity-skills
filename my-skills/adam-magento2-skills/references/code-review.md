# Review Code / Diff

## Checklist review (theo thứ tự ưu tiên)

1. **Kiến trúc/DI**
   - Có dùng `ObjectManager` trực tiếp không (anti-pattern nghiêm trọng)
   - Có leak dependency sai layer không (VD: Model gọi thẳng Controller,
     ResourceModel chứa business logic)
   - Có lạm dụng `preference` khi `plugin` là đủ không

2. **Coding standard**
   - PSR-12 + Magento2 CS: namespace, docblock, type hint đầy đủ
   - Naming convention đúng chuẩn Magento (VD: Interface hậu tố
     `Interface`, Factory hậu tố `Factory`)

3. **Hiệu năng**
   - Có N+1 query không (query trong vòng lặp)
   - Có load Collection không giới hạn (`->getData()` toàn bộ bảng lớn)
     mà không phân trang/batch
   - Có cache được kết quả tính toán nặng lặp lại không

4. **An toàn dữ liệu**
   - Input từ request/API có được validate trước khi dùng không
   - Có nguy cơ SQL injection nếu dùng raw query không (nên dùng
     `getConnection()->select()` với binding thay vì nối chuỗi SQL)

5. **Test**
   - Có unit test cho logic quan trọng chưa (đặc biệt tính giá, tồn kho,
     đồng bộ dữ liệu)

## Định dạng output khi review

Trả lời theo dạng:
- **Vấn đề nghiêm trọng** (phải sửa trước khi merge)
- **Nên cải thiện** (không bắt buộc nhưng nên làm)
- **Góp ý nhỏ** (style, naming...)

Với mỗi vấn đề, chỉ rõ dòng/đoạn code cụ thể và đề xuất cách sửa, không
chỉ nói chung chung.
