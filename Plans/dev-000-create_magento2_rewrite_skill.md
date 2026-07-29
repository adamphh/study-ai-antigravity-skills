# Kế hoạch Xây dựng Skill Rewrite/Preference cho Magento 2 (create-rewrite.md)

## 1. Kết quả Review Hiện tại
Sau khi review toàn bộ bộ kỹ năng `magento2-skills`, kết quả cho thấy:
- Đã có skill `create-plugin.md` (hướng dẫn dùng Plugin/Interceptor).
- Đã có file tham chiếu nhỏ `references/preference-virtualtype.md` (59 dòng).
- **CHƯA CÓ** skill chuẩn hóa `create-rewrite.md` trong danh mục chính của `magento2-skills` để hướng dẫn chi tiết quy trình Rewrite/Override Class (Model, Controller, Block, Helper) bằng DI Preference.

## 2. Mục tiêu Triển khai
Xây dựng skill `create-rewrite.md` đầy đủ, chuẩn mực và cập nhật `SKILL.md` index tại cả 2 thư mục:
1. `/mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/`
2. `/home/bss/.gemini/config/skills/magento2-skills/`

## 3. Nội dung Skill `create-rewrite.md` bao gồm:
- **Khái niệm & Nguyên tắc**: Khi nào dùng Rewrite (Preference) vs Plugin vs VirtualType (Cảnh báo rủi ro xung đột override).
- **Tuân thủ Coding Standard của Dự án**:
  - Không sửa trực tiếp core (`app/code/Magestore/`). Chỉ tạo/sửa trong module `FixBug` hoặc `Custom`.
  - Luôn sử dụng cú pháp `Class::class` trong PHP và XML (nếu applicable) theo quy định workspace.
  - Thêm Copyright Header (`Copyright © Magestore`).
  - Đảm bảo độ dài dòng tối đa 120 ký tự.
  - Thêm DocBlock có Description ngắn gọn và 1 dòng trống trước `@param`/`@return`.
- **Hướng dẫn Chi tiết các Trường hợp Rewrite**:
  - Rewrite Model / Resource Model / Helper.
  - Rewrite Controller Action.
  - Rewrite Block & Template.
- **Mẫu Code Chuẩn (Template Code)**:
  - Khai báo `<preference>` trong `etc/di.xml` hoặc `etc/frontend/di.xml` / `etc/adminhtml/di.xml`.
  - Class Rewrite kế thừa (`extends`) class gốc và gọi `parent::method(...)`.
- **Checklist Kiểm tra Chất lượng Code**.

## 4. Các bước Thực hiện
1. Tạo tệp `create-rewrite.md` tại workspace `my-skills/magento2-skills/create-rewrite.md`.
2. Tạo tệp `create-rewrite.md` tại config `/home/bss/.gemini/config/skills/magento2-skills/create-rewrite.md`.
3. Cập nhật bảng danh mục `SKILL.md` tại cả 2 vị trí trên để đưa `create-rewrite.md` vào phần **Customization & Extension**.
