# CẨM NANG HƯỚNG DẪN SỬ DỤNG ANTIGRAVITY AI ENGINE HIỆU QUẢ

Tài liệu này hướng dẫn quy trình 5 bước làm việc chuẩn giữa lập trình viên và Antigravity AI Engine trong các dự án Magento 2 và WebPOS để tối đa hóa hiệu suất và chất lượng code sinh ra.

---

## BƯỚC 1: Khởi tạo dự án (Initialization)

Khi bắt đầu làm việc với một dự án mới (vừa clone repo Magento/WebPOS mới về máy trạm), bước đầu tiên là thiết lập cấu hình.

* **Cách thực hiện:** Gõ phím tắt `/init-project` trong ô chat hoặc ra lệnh: *"Khởi tạo cấu hình dự án mới này giúp tôi"*.
* **Hành động của AI:**
  - Tự động tạo liên kết động (symlink) thư mục phím tắt `.agent/` từ repo gốc `/mnt/projects/study-ai-antigravity-skills/.agent` vào thư mục dự án hiện hành để dùng chung các slash command.
  - Sao chép thư mục tài liệu kiến trúc mẫu `docs/` chứa `SYSTEM.md`, `INVARIANTS.md`, `SYNC_SPEC.md` và `guide.md` vào thư mục gốc của dự án.
* **Mục tiêu:** Cung cấp đầy đủ slash command và khung tài liệu kiến trúc hệ thống chuẩn cho dự án mới.

---

## BƯỚC 2: Cập nhật ngữ cảnh dự án (Context Configuration)

AI cần nắm bắt chính xác các luật nghiệp vụ bất biến và sơ đồ hệ thống của riêng dự án này trước khi viết code để tránh sai sót.

* **Cách thực hiện:** Bạn mở các file vừa được tạo tại thư mục local của dự án:
  - `docs/SYSTEM.md`: Điền thông tin về mã dự án, tên dự án, môi trường deploy.
  - `docs/INVARIANTS.md`: Điền các ràng buộc nghiệp vụ (Ví dụ: *"Dự án này tích hợp cổng thanh toán Tyro, ID giao dịch không được trùng"*).
* **Lưu ý:** Bạn không cần viết lại kiến trúc lõi của WebPOS vì tôi đã tự động nạp nó từ thư mục kỹ năng global.

---

## BƯỚC 3: Lập kế hoạch trước khi code (Planning Phase)

Khi bạn giao một task mới (Ví dụ: *"Tạo plugin thay đổi logic tính thuế"* hoặc *"Thêm nút Cancel vào popup thanh toán"*).

* **Hành động của AI:**
  1. AI tự động đọc các file trong `docs/` để đối chiếu luật nghiệp vụ.
  2. Quét danh sách chặn core module để kiểm tra xem class cần can thiệp có thuộc module core của Magestore hay không. Nếu có, AI sẽ từ chối sửa trực tiếp và đổi sang phương án viết Plugin/Observer.
  3. Tạo file kế hoạch tại thư mục local (Ví dụ: `Plans/P1146-154_v1.0.md`) và hiển thị bảng kế hoạch `implementation_plan.md` trên màn hình chat.
* **Hành động của bạn:** Review bản kế hoạch, kiểm tra hướng đi kỹ thuật và gõ *"implement"* hoặc bấm nút **Proceed** để phê duyệt cho tôi bắt đầu viết code.

---

## BƯỚC 4: Vibe Coding & Tự động hóa (Execution Phase)

AI tiến hành viết code dựa trên các chỉ dẫn nghiệp vụ trong bộ kỹ năng global.

* **Các phím tắt hỗ trợ bạn (Slash Commands):**
  - `/magento-dev`: Dùng khi bạn cần viết code backend Magento 2 (Controller, Plugin, Cron, CLI, Observer...).
  - `/webpos-dev`: Dùng khi bạn cần tùy biến (customize) client ReactJS của WebPOS.
  - `/react-dev`: Dùng khi cần viết các React component dùng chung.
  - `/skills`: Liệt kê nhanh toàn bộ các kỹ năng lập trình có sẵn.
* **Tự động hóa bằng Script:** Đối với các tác vụ tạo Api Data Interface & Model, AI sẽ tự động gọi script `generate_data_interface.py` để sinh code tự động từ file `db_schema.xml` giúp đảm bảo chính xác 100% kiểu dữ liệu.

---

## BƯỚC 5: Kiểm tra và Commit Code (Verification & Commit)

Sau khi AI hoàn thành việc viết code và tự viết nhật ký thay đổi vào file `walkthrough.md`.

* **Hành động của bạn:** Kiểm tra, chạy thử code. Nếu đã hài lòng, bạn chỉ cần gõ yêu cầu: *"commit code"*.
* **Hành động của AI:**
  - Chạy lệnh `git status` và `git add .` để gom tất cả file chỉnh sửa.
  - Tự động tạo Git commit với message chuẩn hóa lấy từ Git branch hiện tại theo quy định tại `AGENTS.md`: 
    `{Fix/Feat} [{mã dự án} - {issue id}]: {tên ticket}`

---

## CÁC MẸO NÂNG CAO ĐỂ TỐI ƯU HÓA HIỆU SUẤT (ADVANCED TIPS)

Để nâng cao hơn nữa hiệu suất làm việc và tận dụng tối đa sức mạnh của AI, hãy áp dụng các mẹo sau:

### 1. Sử dụng `/grill-me` để chốt kế hoạch nhanh
Khi giao một task lớn phức tạp, bạn hãy gõ `/grill-me` ở cuối yêu cầu chat. AI sẽ đặt câu hỏi phỏng vấn ngắn gọn (3-5 câu hỏi trắc nghiệm) để làm rõ ý đồ thiết kế trước khi sinh file Plan, giúp tiết kiệm thời gian sửa đổi kế hoạch.

### 2. Sử dụng `/learn` để ghi nhớ bài học debug
Sau khi giải quyết xong một lỗi cấu hình khó hoặc thống nhất một cách viết code mới, hãy gõ lệnh `/learn`. AI sẽ đúc rút kinh nghiệm và cập nhật trực tiếp vào bộ kỹ năng `my-skills/` global để áp dụng tự động cho mọi dự án sau này.

### 3. Tích hợp chạy Test tự động (Automated Verification)
Khi duyệt kế hoạch viết code, bạn có thể yêu cầu AI bổ sung các script test tự động bằng command line (như `npm run test` hoặc `bin/magento dev:tests:run`). AI sẽ chạy thử và đính kèm kết quả pass/fail trực tiếp vào `walkthrough.md`.

### 4. Tạo Git Branch phụ để thử nghiệm an toàn
Đối với các tính năng có tính rủi ro cao, bạn có thể yêu cầu: *"Tạo cho tôi một branch Git phụ và thử nghiệm phương án X ở đó"*. AI sẽ tự lập nhánh mới để thử nghiệm code, giúp bảo vệ code sạch của branch chính.
