# Workspace Coding Rules & Guidelines

## 1. Core Principles & Communication
- **Never Edit Core Files Directly**: Always use the extensibility mechanisms of the POS framework
  (Plugins, Rewrites, Mixins, Event Observers) to customize core functionalities. For files in
  `client/pos/src`, changes are ONLY allowed within the `src/extension/` directory.
- **Communication Guidelines**:
  - Always explain briefly and concisely in Vietnamese.
  - Comment code in English. Always add comments in rewritten, plugin, or customize files explaining what was
    changed or customized compared to the original core classes/files to make it easy to review.
  - Always ask the user for clarification if any requirements or issues are not fully understood.
- **Ngôn ngữ giao tiếp:** Luôn giao tiếp bằng tiếng Việt (Vietnamese).
- **Quy định Trung thực & Không bịa đặt (Honesty & Clarification Rule):**
  Tuyệt đối không được bịa đặt thông tin, mã nguồn, hoặc kết quả kiểm thử. Luôn trả lời trung thực dựa trên
  dữ liệu/ngữ cảnh thực tế. Nếu có bất kỳ điều gì chưa hiểu rõ hoặc thiếu thông tin, BẮT BUỘC phải hỏi lại
  lập trình viên để xác nhận trước khi tiếp tục.
- **Dấu hiệu phải hỏi lại (Red Flags):** Nếu thấy bất kỳ yêu cầu nào mơ hồ, mâu thuẫn với ngữ cảnh hiện tại,
  hoặc yêu cầu thay đổi logic cốt lõi mà chưa có chỉ dẫn cụ thể, hãy chủ động hỏi lại thay vì tự phán đoán.
  - *Ví dụ mâu thuẫn:* Yêu cầu thay đổi giao diện, nhưng lại ghi đè file logic lõi (`Model`, `Controller`)
    thay vì dùng Plugin/Rewrite.
  - *Ví dụ mơ hồ:* Yêu cầu "thêm validate" mà không nêu rõ điều kiện validate là gì.
- **Quy định Thao tác Trạng thái trên MCP Jira (MCP Jira Status Transition Rule):**
  - **Mặc định:** Đối với các MCP tool liên quan đến Jira (`jira` server), AI chỉ thực thi các hành động tra cứu/đọc thông tin (Read-only như `jira_get_*`, `jira_search_*`, `jira_whoami`, ...). TUYỆT ĐỐI KHÔNG tự ý tạo, sửa nội dung, gán người hoặc xóa dữ liệu Jira.
  - **Ngoại lệ duy nhất về Chuyển Trạng Thái (Status Transition):** Khi bắt đầu làm một task, AI kiểm tra trạng thái hiện tại của issue:
    - Nếu trạng thái là **`To Do`** (hoặc `Open`, `Backlog`): AI **ĐƯỢC PHÉP tự động chuyển trạng thái task sang `In Progress` (hoặc `In Process`)** thông qua `jira_transition_issue`.
    - Nếu trạng thái **ĐANG LÀ BẤT KỲ TRẠNG THÁI NÀO KHÁC** (như `In Progress`, `In Review`, `Done`, `Resolved`, ...): **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP THAY ĐỔI TRẠNG THÁI** của issue.
---

## 2. Planning, Workflow & Proactive Actions
- **Always Create a Plan First**: Always create a plan file (e.g.
  `Plans/{ma_du_an}-{ma_issue}-{noi_dung_task_tom_tat_20_ki_tu}.md` and `implementation_plan.md` artifact)
  for the user to review. Do not start implementing code until the user explicitly reviews and approves
  the plan. Trong đó `{ma_du_an}` và `{ma_issue}` lấy từ git branch.
- **Định dạng tên file plan:** Đặt tên file plan theo định dạng:
  `{mã dự án}-{mã issue}-{nội dung task tóm tắt 20 kí tự}.md` trong đó mã dự án và mã issue lấy từ git branch.
- **Tự động hóa phỏng vấn khi lập kế hoạch (Proactive Planning):** Đối với các task phức tạp hoặc thiếu
  thông tin thiết kế, AI không cần đợi lệnh `/grill-me`. AI phải chủ động đặt 2-4 câu hỏi làm rõ các điểm nghi vấn
  ngay trong bước lập kế hoạch để thống nhất với lập trình viên trước khi bắt đầu code.
- **Tự động đọc Tài liệu Luồng Dữ liệu (Auto Read Data Flows):** Tại lượt tương tác đầu tiên của mỗi phiên chat
  (hoặc khi bắt đầu nghiên cứu giải pháp cho một task), AI BẮT BUỘC phải tự động kiểm tra xem trong dự án có
  thư mục `docs/data-flows/` hay không. Nếu có, AI phải chủ động xem qua danh mục `docs/data-flows/README.md`
  và đọc các file luồng dữ liệu liên quan trước khi tiến hành tra cứu mã nguồn hay lập kế hoạch.
- **Tự động kiểm tra cấu hình dự án mới (Auto-Init):** Tại lượt tương tác đầu tiên của mỗi phiên chat
  (hoặc khi bắt đầu làm việc trên một workspace mới), AI phải tự động kiểm tra xem trong thư mục gốc của dự án
  đã có thư mục `.agent` và `docs` hay chưa. Nếu chưa, AI phải chủ động thực thi hoặc đề xuất chạy skill
  `init-project` để thiết lập đầy đủ phím tắt và tài liệu mẫu cho lập trình viên mà không cần đợi yêu cầu.
- **Tự động gợi ý học hỏi (Proactive Learning):** Sau khi hoàn thành một task khó (như sửa bug cấu hình phức tạp,
  tạo giải pháp bypass lỗi hệ thống, hoặc áp dụng coding pattern mới), hoặc khi AI nhận diện mình vừa lặp lại
  một lỗi cũ (mất thẻ XML, quên copyright header, sai format commit...), AI phải tự đánh giá xem kiến thức này
  có giá trị tái sử dụng hay không. Nếu có, ngay lập tức gửi lời xin lỗi (nếu là lặp lỗi) và CHỦ ĐỘNG đề xuất
  lập trình viên chạy lệnh `/learn` để ghi nhớ quy tắc vào hệ thống mà không cần đợi nhắc nhở.
- **Bắt buộc Review Code cuối Workflow (Mandatory Code Review & Risk Analysis):** Sau khi hoàn thành việc
  triển khai mã nguồn và chạy test cho bất kỳ task nào, AI BẮT BUỘC phải tự động gọi Subagent chuyên biệt
  (`Role: Code Reviewer & Risk Analyst`) để rà soát toàn bộ các file thay đổi/tạo mới, đánh giá các rủi ro
  tiềm ẩn (Memory Leak, Race Condition, Null Pointer Safety, Edge cases) và báo cáo cho lập trình viên trước
  khi commit.

---

## 3. Allowed Scope & Coding Standards

### Scope Restrictions
- **Quy định nghiêm ngặt về phạm vi thư mục / module được phép chỉnh sửa (Allowed Scope Rules):**
  - **TUYỆT ĐỐI KHÔNG** chỉnh sửa hoặc tạo mới các file/thư mục nằm ngoài 2 phạm vi sau:
    1. `app/code/Magestore/`
    2. `client/pos/src/extension/`
  - **Trong `app/code/Magestore/` (Magento backend/module):** CHỈ ĐƯỢC PHÉP chỉnh sửa hoặc tạo mới ở những module
    chứa từ `FixBug` (ví dụ: `FixBug`, `WebposFixBug`, ...) hoặc có hậu tố `Custom` (ví dụ: `WebposCustom`,
    `BarcodeCustom`, ...). Tuyệt đối không sửa các module Core gốc của Magestore.
  - **Trong `client/pos/src/extension/` (WebPOS frontend extension):** CHỈ ĐƯỢC PHÉP tạo module mới hoặc chỉnh sửa
    các file thuộc thư mục/module có chứa từ `fix-bug` (ví dụ: `fix-bug`, `webpos-fix-bug`, ...) hoặc có hậu tố
    `custom` ở cuối (ví dụ: `custom`, `webpos-custom`, ...). Tuyệt đối không chỉnh sửa trực tiếp các file core
    trong `src/pos/` hay các extension core khác.
- **Không tự động tạo hoặc modify files under src/pos/ (core files):**
  - Khi cần thêm tính năng hoặc thay đổi logic cho các file nằm trong thư mục `src/pos/`, luôn tạo các file
    extension hoặc plugin tương ứng trong thư mục `src/extension/`.
  - Chỉ sửa các file `src/pos/` khi có sự đồng ý rõ ràng từ lập trình viên.

### General Syntax & Formatting Rules
- **Quy định Độ dài Dòng Code Tối đa (Maximum Line Length Rule):** Khi sinh mã nguồn hoặc chỉnh sửa bất kỳ
  file code nào (`.php`, `.xml`, `.js`, `.css`, ...), mỗi dòng code tuyệt đối KHÔNG ĐƯỢC vượt quá 120 ký tự
  (**Bao gồm cả ký tự khoảng trắng thụt lề Indentation ở đầu dòng**). AI BẮT BUỘC phải tính tổng
  `len(indent + content)` hoặc chạy script kiểm tra tự động trước khi commit.
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
  - Dòng đầu tiên trong khối comment của mỗi hàm/phương thức phải có Description mô tả ý nghĩa công việc
    của hàm đó.
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

- **Quy định Ký tự Kết thúc Tệp (EOF Newline Rule):** Mỗi file code khi lưu BẮT BUỘC chỉ có chính xác 1 dòng
  trống / ký tự xuống dòng (1 newline) ở cuối file. Không để xảy ra lỗi thừa nhiều dòng trống ở EOF
  (`Expected 1 blank line at end of file; X found`).

---

## 4. Magento 2 Backend Guidelines
- **Quy định Tham chiếu Class trong PHP (PHP Class Reference Rule):** Khi tham chiếu tới tên Class hoặc Interface
  trong code PHP (ví dụ khi gọi ObjectManager, đăng ký DI, hoặc truyền tên class), BẮT BUỘC sử dụng cú pháp
  `::class` (ví dụ `ClassName::class` hoặc `InterfaceName::class`) thay vì truyền dạng chuỗi literal (`'ClassName'`).
- **Quy định Kiểm tra Toàn vẹn Cú pháp XML (XML Tag Match & Read-Back Validation):** Sau bất kỳ thao tác
  chỉnh sửa hoặc tạo mới file XML nào (`.xml`), AI BẮT BUỘC phải sử dụng công cụ `view_file` xem lại toàn bộ
  file vừa chỉnh sửa để kiểm định thủ công: Đảm bảo 100% các thẻ mở (ví dụ: `<type>`, `<container>`, `<item>`)
  có thẻ đóng tương ứng (`</type>`, `</container>`, `</item>`). Không để xảy ra lỗi nuốt thẻ đóng khi thực hiện
  partial replace.
- **Quy tắc Khai báo UI Component Grid trong Magento 2 (Magento 2 UI Component Grid Standards):** Khi tạo mới
  hoặc sửa cấu hình UI Component Grid (đặc biệt khi xử lý lỗi Export hoặc DataProvider), AI BẮT BUỘC phải tuân
  thủ 2 tiêu chuẩn:
  1. **Chuẩn hóa DataProvider Class**: Trong file UI Component XML, thuộc tính `<argument name="class">` của
     `dataProvider` (nằm trong `<dataSource>`) phải sử dụng class chuẩn
     `Magento\Framework\View\Element\UiComponent\DataProvider\DataProvider`.
  2. **Khai báo Data Source Collection trong `di.xml`**: Trong file `etc/di.xml`, BẮT BUỘC phải đăng ký
     mapping giữa tên `dataSource` (ví dụ `webpos_location_listing_data_source`) với Grid Resource Model
     Collection tương ứng thuộc `Magento\Framework\View\Element\UiComponent\DataProvider\CollectionFactory`.
- **Quy tắc Reindex Realtime trong Observer Magento 2 (Magento 2 Realtime Reindex Observer Rules):** Khi viết
  Observer reindex realtime (Update on Save), BẮT BUỘC sử dụng event `_commit_after` (tránh DB lock), bọc khối
  reindex trong `try-catch (\Throwable $e)` kèm ghi log lỗi (tránh rollback checkout), và kiểm tra
  `!$indexer->isScheduled()` qua `IndexerRegistry`.
- **Quy định Truy xuất Extension Attributes trong Magento 2 (Magento 2 Extension Attributes Standard):**
  Các class Extension Interface (như `ProductExtensionInterface`, `ItemExtensionInterface`, ...) được Magento
  sinh tự động từ `\Magento\Framework\Api\AbstractSimpleObject`, **KHÔNG kế thừa** từ
  `\Magento\Framework\DataObject`. Tuyệt đối KHÔNG gọi `getData()` hoặc `setData()` trên đối tượng extension
  attributes. BẮT BUỘC sử dụng getter/setter chuẩn dạng camelCase được sinh tự động theo khai báo attribute
  (ví dụ `getWorkStation()`, `setWorkStation($val)`) hoặc kiểm tra `method_exists()` trước khi gọi.
- **Quy định Không để Khối Catch Rỗng (No Empty Catch Block Rule):** Trong các khối `try ... catch (\Exception $e)`,
  TUYỆT ĐỐI KHÔNG để khối `catch` rỗng không có câu lệnh xử lý (gây lỗi PHPCS `Empty CATCH statement detected`).
  Phải ghi log lỗi qua `$this->logger->error(...)` hoặc có câu lệnh gán biến fallback (ví dụ `$result = null;`).
- **Quy định Đối soát Tồn tại Namespace Class/Interface trong Magento 2 (Magento 2 Class/Interface Verification Rule):**
  Trước khi khai báo `use <Namespace>\<ClassName>;` hoặc inject Class / Interface trong code PHP, AI BẮT BUỘC phải
  dùng `grep_search` hoặc `find_by_name` kiểm tra sự tồn tại thực tế của tệp Class/Interface đó trong codebase
  (bao gồm đường dẫn thư mục và chuỗi namespace chính xác). TUYỆT ĐỐI KHÔNG tự phán đoán hoặc suy diễn namespace
  (ví dụ: `Magestore\Webpos\Api\Location\LocationRepositoryInterface` có chứa sub-namespace `Location\`, không được
  tự ý viết tắt thành `Magestore\Webpos\Api\LocationRepositoryInterface`). Subagent Code Reviewer khi rà soát mã
  nguồn cũng BẮT BUỘC phải kiểm tra chéo các `use` import mới trong diff để đảm bảo namespace tồn tại 100%.
- **Quy định Tương thích Ngược Constructor trong Magento 2 (Magento 2 Constructor Backward Compatibility Rule):**
  Khi bổ sung bất kỳ Dependency mới nào vào phương thức `__construct()` của một Class / Service / Resolver đã tồn tại:
  1. **BẮT BUỘC** đặt tham số mới ở cuối danh sách tham số dưới dạng nullable: `?TypeInterface $param = null`.
  2. **BẮT BUỘC** gán giá trị fallback bên trong thân constructor thông qua `ObjectManager`:
     `$this->param = $param ?: \Magento\Framework\App\ObjectManager::getInstance()->get(TypeInterface::class);`
  Quy tắc này đảm bảo 100% không làm gãy các module khác đang extends class đó hoặc khởi tạo qua `parent::__construct()`
  với danh sách tham số cũ.

- **Quy định Logging cho các tác vụ quan trọng (Critical Task Logging Rule):**
  Trong các tiến trình nghiệp vụ quan trọng (đặc biệt là thanh toán, tồn kho, đồng bộ dữ liệu), BẮT BUỘC phải
  thêm các dòng log (`logger->info` hoặc `logger->error`) ghi lại các điểm mốc (checkpoint) và các dữ liệu
  đầu vào/đầu ra quan trọng. Việc này giúp đội ngũ hỗ trợ kỹ thuật truy vết nhanh lỗi khi có khiếu nại từ người dùng.
- **Quy định Kiểm tra Phân quyền (Permission Check Rule):**
  Khi phát triển các API hoặc Controller mới (ví dụ `Adminhtml` hoặc `Rest API`), AI BẮT BUỘC phải khai báo
  đúng các ACL (Access Control List) trong file `acl.xml` và thực hiện kiểm tra `_isAllowed()` hoặc check quyền
  hệ thống trước khi thực hiện bất kỳ thao tác thay đổi dữ liệu nào.

---

## 5. WebPOS Client Extension Guidelines

### Module Creation & Customization Patterns
- **Creating a New Module in Extension**:
  - Create a directory: `src/extension/<module_name>/`.
  - Create a configuration file: `src/extension/<module_name>/etc/config.js` extending `ModuleConfigAbstract`.
  - Enable & Register: Run `npm run upgrade` in the `client/pos` directory. This script automatically enables
    the module in `modules.json`, updates `src/extension/config.js` imports, and merges any custom dependencies
    from the extension's local `package.json`.
- **Rewrite Mechanism**:
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
- **Plugins (Before, Around, After)**:
  - Register plugins in the `plugin` block of `etc/config.js` to modify arguments, wrap execution, or alter
    return values of specific methods.
- **Mixins**:
  - Inject new methods or static functions into core classes via `mixin` registration in `etc/config.js`.
- **Event Observers**:
  - Subscribe to custom events using `listen` from `event-bus` or dispatch new ones with `fire`.
- **Layout Customization Mechanism**:
  - Inject or customize UI elements in screens/pages by declaring them in the `layout` block of `etc/config.js`.
  - Layout configurations correspond to the layout hooks defined in core components via
    `layout('[block]')('[hook]')()(this)`.
  - Layout plugins can be plain text, React components, or functions that receive the parent component instance
    as an argument.

### WebPOS Extension Code Rules
- **Quy định Export JS trong WebPOS Extension (Tránh lỗi ESLint):** Khi viết các file plugin/helper/service
  JS trong WebPOS client, tuyệt đối KHÔNG `export default` trực tiếp object vô danh (`export default { ... }`).
  Bắt buộc khai báo gán vào hằng số/biến có tên trước khi `export default` (ví dụ: `const PluginName = { ... };
  export default PluginName;`) để đảm bảo tuân thủ ESLint rule `import/no-anonymous-default-export`.
- **Quy định Nạp Dependency trong WebPOS JS Extension (WebPOS Extension Require Standard):** Khi viết các file
  plugin/rewrite/mixin/observer JS trong WebPOS client (`src/extension/`), ngoại trừ React, tất cả các
  Service/Helper/Constant hoặc Component tham chiếu từ core BẮT BUỘC phải nạp bằng cú pháp `require("...").default`
  bên trong thân từng phương thức (in-function require) để tránh lỗi undefined dependency.
- **Quy định Đối soát Tên Hàm khi Rewrite WebPOS Component (WebPOS Component Rewrite Method Check Rule):** Trước
  khi tạo phương thức rewrite cho bất kỳ React Component nào trong WebPOS client, AI BẮT BUỘC phải dùng
  `view_file` hoặc `grep_search` kiểm tra trực tiếp mã nguồn class gốc trong `src/view/` để xác định chính xác
  tên phương thức gốc (ví dụ `getTemplateDetailItem` thay vì tự phán đoán) đảm bảo logic rewrite được thực thi.
- **Quy định Kiểm Tra Plugin Trùng Lặp trong WebPOS Extension (Plugin Conflict Check Rule):** Trước khi tạo plugin
  cho bất kỳ phương thức/component nào trong WebPOS client (`src/extension/`), AI BẮT BUỘC phải dùng `grep_search`
  kiểm tra trong `src/extension/` xem đã có extension nào khác đăng ký plugin cho cùng component/method đó hay
  chưa. Nếu có, AI phải ngay lập tức thông báo danh sách extension trùng lặp cho lập trình viên và cùng đối soát
  logic để tránh bị đè hoặc xung đột logic giữa các plugin.
- **Quy định Tính Tồn Kho Khả Dụng trong WebPOS Client (WebPOS Client Available Qty Rule):** Khi kiểm tra
  tồn kho sản phẩm trong giỏ hàng (`quote`) để quyết định khả năng giao hàng (Shipment/Ship All Items),
  BẮT BUỘC sử dụng giá trị nhỏ nhất giữa Salable Qty và Location Qty:
  `availableQty = Math.min(productStockService.getSalableQty(product), productStockService.getQtyInLocation(product))`.
  Không được chỉ kiểm tra đơn lẻ `qtyInLocation` hay `qty_backordered`.
- **Quy tắc Xử lý Xung đột Đồng bộ khi Server Reindex (WebPOS Reindexing Sync Race Condition Rule):** Khi đồng
  bộ đối soát dữ liệu (ví dụ Catalog Rules) giữa POS và Server, để tránh việc xóa sạch dữ liệu IndexedDB local
  trong lúc server reindex (bảng giá tạm trống, API trả về `[]`), bắt buộc kết hợp cả hai giải pháp:
  1. **Server-side (Magento Plugin):** Viết plugin cho API lấy ID. Nếu kết quả trống nhưng thực tế vẫn có
     rules active trong bảng cấu hình gốc (`catalogrule`), bắt buộc ném `LocalizedException` để báo lỗi về client.
  2. **Client-side (POS Rewrite):** Bọc phương thức gọi lấy ID trong khối `try-catch`. Khi bắt được lỗi từ
     server (Exception), ghi log cảnh báo và gán mảng ID cần xóa về rỗng `[]` để bảo toàn dữ liệu local IndexedDB.

---

## 6. Testing, Verification & CodeRunner
- **Bắt buộc viết và chạy Automation Test khi sinh code (Mandatory Automated Testing):** Khi sinh mã nguồn
  cho bất kỳ tính năng mới hoặc chỉnh sửa logic nào, AI BẮT BUỘC phải thiết kế và viết kèm theo bộ kiểm thử
  tự động (Automation Test - như Unit Test, Integration Test phù hợp cho frontend/backend). Sau khi hoàn thành,
  AI phải tự động xác định câu lệnh và thực thi các bộ test này, kiểm tra kết quả pass/fail thực tế và đính kèm
  chi tiết trực tiếp vào tệp `walkthrough.md` trước khi bàn giao cho lập trình viên kiểm thử thủ công.
- **Tích hợp với CodeRunner - Tự động kiểm tra tính đúng đắn của code:**
  - Sau khi hoàn thành việc sinh hoặc chỉnh sửa mã nguồn, AI phải chủ động gọi CodeRunner để biên dịch (compile)
    và chạy Unit Test (nếu có thể). 
  - Kết quả thực thi (Pass/Fail và log lỗi) từ CodeRunner phải được đính kèm trực tiếp vào `walkthrough.md`
    như một bằng chứng xác thực cho chất lượng code trước khi bàn giao.
  - Nếu CodeRunner báo lỗi, AI phải tự động xem xét log lỗi và đề xuất phương án sửa chữa trong cùng một phản hồi.
- **Quy định Tự Động Dọn Dẹp File Test Tạm Thời Trước Khi Commit (Temporary Test File Cleanup Rule):** Các tệp
  Unit Test / Automation Test được tạo ra CHỈ dùng để biên dịch và kiểm thử tính đúng đắn của code tại thời điểm
  vừa sinh/sửa mã nguồn. Sau khi chạy test thành công và ghi nhận kết quả vào `walkthrough.md`, AI BẮT BUỘC
  phải tự động xóa (remove) toàn bộ tệp test tạm thời đó TRƯỚC KHI thực hiện lệnh `git commit` để tránh đẩy
  tệp test lên repository làm phát sinh cảnh báo/lỗi CI linter.

---

## 7. Git Commit & Branching Workflow Guidelines
1. **Vòng đời Phân nhánh Git Chuẩn (Git Branching & Release Lifecycle)**:
   - **Rẽ nhánh (Branching)**: Luôn luôn tạo branch mới bắt đầu (break branch) từ nhánh `release`
     (hoặc `origin/release`), TUYỆT ĐỐI KHÔNG break branch từ nhánh `develop`.
   - **Commit mã nguồn**: Phát triển và commit code trên nhánh `feature/fix` theo đúng định dạng quy định.
   - **Đưa code đi Test**: Tạo Merge Request vào `develop` hoặc merge `feature/fix` vào `develop` trên local
     để deploy lên môi trường test cho QA kiểm thử.
   - **Sửa lỗi khi Test Fail**: Nếu phát sinh bug, quay về nhánh `feature/fix` để sửa tiếp và commit lại.
   - **Bàn giao (Delivery to Release)**: Sau khi QA test PASS 100% trên `develop`, nhánh `feature/fix` mới được
     merge vào `release` để bàn giao cho khách hàng. Nhánh `release` chỉ chứa code đã hoàn thiện và kiểm thử đạt.
2. **Quy tắc Tuyệt đối KHÔNG Merge `develop` vào `feature/fix` (Strict No-Develop-to-Feature Rule)**:
   - TUYỆT ĐỐI KHÔNG ĐƯỢC thực hiện `git merge develop` hoặc `git merge origin/develop` vào nhánh `feature/fix`.
   - Nhánh `develop` là nơi tích hợp code thử nghiệm của nhiều lập trình viên khác nhau. Nếu merge `develop` vào
     `feature/fix`, nhánh feature sẽ bị nhiễm code chưa hoàn thiện của các task khác, làm hỏng nhánh `release`.
3. **Quy trình Xử lý Conflict khi đưa code vào `develop` (Develop Conflict Resolution Procedure)**:
   - Khi tạo Merge Request hoặc merge code vào `develop` mà bị conflict:
     1. `git checkout develop && git pull origin develop`
     2. `git merge <nhánh_feature_fix>`
     3. Xử lý các điểm conflict trực tiếp trên nhánh `develop`, giữ lại đầy đủ logic của cả 2 bên.
     4. Kiểm tra cú pháp, chạy test, sau đó `git commit` và `git push origin develop` để deploy mang đi test.
     5. BẮT BUỘC `git checkout <nhánh_feature_fix>` để quay trở lại nhánh feature sạch sẽ ban đầu.
4. **Commit Message Format**:
   - Use the format: `{Fix/Feat} [{mã dự án} - {issue id}]: {ticket ID hoặc user story name}`
     - `{Fix/Feat}`: Use `Fix` for bugs, `Feat` for user stories / features.
     - `{mã dự án}`: Project code (e.g. `P1115` at the start of branch).
     - `{issue id}`: Issue ID (e.g. `391` after project code in branch).
     - `{ticket ID hoặc user story name}`: Ticket ID hoặc user story name
       (e.g. `[US09] Customize Tyro payment popup layout and cancellation flow`).
     - Example: `Feat [P1115 - 391]: [US09] Customize Tyro payment popup layout and cancellation flow`.
5. **Review Changes Before Committing**:
   - Always run `git status` and `git diff` to review code modifications.
   - Do not stage or commit temporary build outputs, configs, or dependencies.
6. **Commit Scope**:
   - Only commit files within the defined implementation plan.

---

## 8. Workspace & Project Search Priority
1. **Ưu tiên Tìm kiếm tuyệt đối tại `/mnt/projects`**:
   - Khi người dùng yêu cầu mở dự án, tìm workspace, bắt đầu task hoặc tìm kiếm mã nguồn:
     AI **BẮT BUỘC** ưu tiên tìm kiếm và kiểm tra trong thư mục `/mnt/projects/` đầu tiên
     (ví dụ: `/mnt/projects/<ma_du_an>-*`, `/mnt/projects/study-ai-antigravity-skills`, ...).
   - Nếu đã tìm thấy workspace/dự án trong `/mnt/projects/`: **TUYỆT ĐỐI DỪNG LẠI**, không
     được tiếp tục tìm kiếm hoặc quét các thư mục con trong `/home/*` (như `/home/bss/*`).
2. **Quy định về phạm vi quét thư mục**:
   - Nghiêm cấm mọi hành vi tự ý quét toàn bộ thư mục `/home/bss` khi chưa kiểm tra `/mnt/projects`.
   - Chỉ khi nào tìm kiếm trong `/mnt/projects` không thấy kết quả VÀ có chỉ định cụ thể từ
     người dùng thì mới mở rộng phạm vi tìm kiếm.
