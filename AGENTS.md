# Workspace Coding Rules & Guidelines

## Core Principles
1. **Never Edit Core Files Directly**: Always use the extensibility mechanisms of the POS framework (Plugins, Rewrites, Mixins, Event Observers) to customize core functionalities. For files in `client/pos/src`, changes are ONLY allowed within the `src/extension/` directory.
2. **Always Create a Plan First**: Always create a plan file (e.g. `Plans/{ma_du_an}-{ma_issue}-{noi_dung_task_tom_tat_20_ki_tu}.md` and `implementation_plan.md` artifact) for the user to review. Do not start implementing code until the user explicitly reviews and approves the plan. trong đó {ma_du_an} và {ma_issue} lấy từ git branch.
3. **Communication Guidelines**:
   - Always explain briefly and concisely in Vietnamese.
   - Comment code in English. Always add comments in rewritten, plugin, or customize files explaining what was changed or customized compared to the original core classes/files to make it easy to review.
   - Always ask the user for clarification if any requirements or issues are not fully understood.
4. **Creating a New Module in Extension**:
   - Create a directory: `src/extension/<module_name>/`.
   - Create a configuration file: `src/extension/<module_name>/etc/config.js` extending `ModuleConfigAbstract`.
   - Enable & Register: Run `npm run upgrade` in the `client/pos` directory. This script automatically enables the module in `modules.json`, updates `src/extension/config.js` imports, and merges any custom dependencies from the extension's local `package.json`.

## Customization Patterns for webpos client

### Rewrite Mechanism
- For overriding class methods or properties, create rewrite files under `src/extension/<extension_name>/rewrite/`.
- Register rewrites in `src/extension/<extension_name>/etc/config.js` under the `rewrite` block.
- Use wrapper functions for rewrites:
  ```javascript
  export default function (BaseClass) {
      return class Rewrite extends BaseClass {
          // Overridden methods or properties
      };
  }
  ```

### Plugins (Before, Around, After)
- Register plugins in the `plugin` block of `etc/config.js` to modify arguments, wrap execution, or alter return values of specific methods.

### Mixins
- Inject new methods or static functions into core classes via `mixin` registration in `etc/config.js`.

### Event Observers
- Subscribe to custom events using `listen` from `event-bus` or dispatch new ones with `fire`.

### Layout Customization Mechanism
- Inject or customize UI elements in screens/pages by declaring them in the `layout` block of `etc/config.js`.
- Layout configurations correspond to the layout hooks defined in core components via `layout('[block]')('[hook]')()(this)`.
- Layout plugins can be plain text, React components, or functions that receive the parent component instance as an argument.

## Git Commit Guidelines
1. **Commit Message Format**:
   - Use the format: `{Fix/Feat} [{mã dự án} - {issue id}]: {ticket ID hoặc user story name}`
     - `{Fix/Feat}`: Use `Fix` for bugs, `Feat` for user stories / features.
     - `{mã dự án}`: Project code (e.g. `P1115` at the start of branch).
     - `{issue id}`: Issue ID (e.g. `391` after project code in branch).
     - Example: `Feat [P1115 - 391]: [US09] Customize Tyro payment popup layout and cancellation flow`.
2. **Review Changes Before Committing**:
   - Always run `git status` and `git diff` to review code modifications.
   - Do not stage or commit temporary build outputs, configs, or dependencies.
3. **Commit Scope**:
   - Only commit files within the defined implementation plan.


# Custom Rules
- Đặt tên file plan theo định dạng: `{mã dự án}-{mã issue}-{nội dung task tóm tắt 20 kí tự}.md` trong đó mã dự án và mã issue lấy từ git branch.
- **Ngôn ngữ giao tiếp:** Luôn giao tiếp bằng tiếng Việt (Vietnamese).
- **Tự động hóa phỏng vấn khi lập kế hoạch (Proactive Planning):** Đối với các task phức tạp hoặc thiếu thông tin thiết kế, AI không cần đợi lệnh `/grill-me`. AI phải chủ động đặt 2-4 câu hỏi làm rõ các điểm nghi vấn ngay trong bước lập kế hoạch để thống nhất với lập trình viên trước khi bắt đầu code.
- **Bắt buộc viết và chạy Automation Test khi sinh code (Mandatory Automated Testing):** Khi sinh mã nguồn cho bất kỳ tính năng mới hoặc chỉnh sửa logic nào, AI BẮT BUỘC phải thiết kế và viết kèm theo bộ kiểm thử tự động (Automation Test - như Unit Test, Integration Test phù hợp cho frontend/backend). Sau khi hoàn thành, AI phải tự động xác định câu lệnh và thực thi các bộ test này, kiểm tra kết quả pass/fail thực tế và đính kèm chi tiết trực tiếp vào tệp `walkthrough.md` trước khi bàn giao cho lập trình viên kiểm thử thủ công.
- **Tự động gợi ý học hỏi (Proactive Learning):** Sau khi hoàn thành một task khó (như sửa bug cấu hình phức tạp, tạo giải pháp bypass lỗi hệ thống, hoặc áp dụng coding pattern mới), AI phải tự đánh giá xem kiến thức này có giá trị tái sử dụng hay không. Nếu có, chủ động gợi ý lập trình viên: *"Tôi thấy task này đã xử lý một lỗi/kiến thức phức tạp X. Bạn có muốn tôi ghi nhớ bài học này vào bộ kỹ năng dùng chung (chạy `/learn`) không?"*.
- **Tự động kiểm tra cấu hình dự án mới (Auto-Init):** Tại lượt tương tác đầu tiên của mỗi phiên chat (hoặc khi bắt đầu làm việc trên một workspace mới), AI phải tự động kiểm tra xem trong thư mục gốc của dự án đã có thư mục `.agent` và `docs` hay chưa. Nếu chưa có, AI phải chủ động thực thi hoặc đề xuất chạy skill `init-project` để thiết lập đầy đủ phím tắt và tài liệu mẫu cho lập trình viên mà không cần đợi yêu cầu.
- **Quy định Copyright Header khi sinh file:**
  - Mỗi file `.php` khi được sinh mới phải có phần copyright ở đầu file:
    ```php
    /**
     * Copyright © Magestore. All rights reserved.
     * See COPYING.txt for license details.
     */
    ```
  - Mỗi file `.xml` khi được sinh mới phải có phần copyright ở đầu file:
    ```xml
    <!--
      ~ Copyright © Magestore. All rights reserved.
      ~ See COPYING.txt for license details.
      -->
    ```
- **Quy định DocBlock / Function Comment:**
  - Dòng đầu tiên trong khối comment của mỗi hàm/phương thức phải có Description mô tả ý nghĩa công việc của hàm đó.
  - Phải có chính xác 1 dòng trống giữa phần Description và phần khai báo `@param` / `@return`.
  - Mẫu minh họa:
    ```php
    /**
     * Concise and meaningful description of function purpose.
     *
     * @param string $paramName
     * @return bool
     */
    ```
- **Dấu hiệu phải hỏi lại (Red Flags):** Nếu thấy bất kỳ yêu cầu nào mơ hồ, mâu thuẫn với ngữ cảnh hiện tại, hoặc yêu cầu thay đổi logic cốt lõi mà chưa có chỉ dẫn cụ thể, hãy chủ động hỏi lại thay vì tự phán đoán.
  - *Ví dụ mâu thuẫn:* Yêu cầu thay đổi giao diện, nhưng lại ghi đè file logic lõi (`Model`, `Controller`) thay vì dùng Plugin/Rewrite.
  - *Ví dụ mơ hồ:* Yêu cầu "thêm validate" mà không nêu rõ điều kiện validate là gì.
- **Tích hợp với CodeRunner - Tự động kiểm tra tính đúng đắn của code:**
  - Sau khi hoàn thành việc sinh hoặc chỉnh sửa mã nguồn, AI phải chủ động gọi CodeRunner để biên dịch (compile) và chạy Unit Test (nếu có thể). 
  - Kết quả thực thi (Pass/Fail và log lỗi) từ CodeRunner phải được đính kèm trực tiếp vào `walkthrough.md` như một bằng chứng xác thực cho chất lượng code trước khi bàn giao.
  - Nếu CodeRunner báo lỗi, AI phải tự động xem xét log lỗi và đề xuất phương án sửa chữa trong cùng một phản hồi.
- **Không tự động tạo hoặc modify files under src/pos/ (core files):**
  - Khi cần thêm tính năng hoặc thay đổi logic cho các file nằm trong thư mục src/pos/, luôn tạo các file extension hoặc plugin tương ứng trong thư mục src/extension/.
  - Chỉ sửa các file src/pos/ khi có sự đồng ý rõ ràng từ lập trình viên.
- **Quy định nghiêm ngặt về phạm vi thư mục / module được phép chỉnh sửa (Allowed Scope Rules):**
  - **TUYỆT ĐỐI KHÔNG** chỉnh sửa hoặc tạo mới các file/thư mục nằm ngoài 2 phạm vi sau:
    1. `app/code/Magestore/`
    2. `client/pos/src/extension/`
  - **Trong `app/code/Magestore/` (Magento backend/module):** CHỈ ĐƯỢC PHÉP chỉnh sửa hoặc tạo mới ở những module chứa từ `FixBug` (ví dụ: `FixBug`, `WebposFixBug`, ...) hoặc có hậu tố `Custom` (ví dụ: `WebposCustom`, `BarcodeCustom`, ...). Tuyệt đối không sửa các module Core gốc của Magestore.
  - **Trong `client/pos/src/` (WebPOS frontend):** CHỈ ĐƯỢC PHÉP thao tác trong thư mục `src/extension/`. Tuyệt đối không sửa các file core trong `src/pos/`.


