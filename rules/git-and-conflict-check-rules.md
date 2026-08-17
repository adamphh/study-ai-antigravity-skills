# Git Commit & Extension Conflict Check Rules

## 1. Extension Plugin/Mixin Conflict Check Rule
- Trước khi đề xuất giải pháp hoặc tạo file kế hoạch (`implementation_plan.md`) cho bất kỳ React Component/Service
  nào trong WebPOS Client (`src/extension/`), AI BẮT BUỘC phải sử dụng `grep_search` kiểm tra trong thư mục
  `src/extension/` xem đã có extension nào khác đăng ký Plugin/Mixin/Rewrite cho cùng Class/Service/Component đó chưa.
- Nếu tìm thấy extension trùng lặp, AI phải báo cáo danh sách cụ thể cho lập trình viên để cùng đối soát logic,
  tránh xung đột hoặc đè logic lẫn nhau.

## 2. Git Commit Amend Rule
- Trước khi thực hiện `git commit`, AI phải dùng `git log -n 5` kiểm tra xem trên nhánh (branch) hiện tại đã có
  commit nào do AI thực hiện cho cùng mã Task/Issue này hay chưa.
- Nếu đã có commit trước đó cho task/issue hiện tại, AI BẮT BUỘC phải sử dụng `git commit --amend`
  (hoặc `git commit --amend --no-edit`) để gộp các thay đổi mới vào commit trước đó, đảm bảo không tạo thêm các
  commit rác trên lịch sử git repository.

## 3. Quy tắc Vòng đời Phân nhánh Git & Xử lý Conflict (Git Branching Lifecycle & Conflict Resolution)
- **Vòng đời Phân nhánh Git Chuẩn (Git Branching & Release Lifecycle)**:
  1. **Rẽ nhánh (Branching)**: Luôn checkout và tạo nhánh `feature/fix` mới bắt đầu từ `release`
     (`git checkout release && git pull origin release && git checkout -b <branch_name>`).
     TUYỆT ĐỐI KHÔNG ĐƯỢC tạo nhánh từ `develop` hoặc từ nhánh hiện tại.
  2. **Commit mã nguồn**: Phát triển và commit code trên nhánh `feature/fix` theo đúng định dạng quy định.
  3. **Đưa code đi Test**: Tạo Merge Request vào `develop` hoặc merge `feature/fix` vào `develop` trên local để
     deploy lên môi trường test cho QA kiểm thử.
  4. **Sửa lỗi khi Test Fail**: Nếu phát sinh bug, quay về nhánh `feature/fix` để sửa tiếp và commit lại.
  5. **Bàn giao (Delivery to Release)**: Sau khi QA test PASS 100% trên `develop`, nhánh `feature/fix` mới được
     merge vào `release` để bàn giao cho khách hàng. Nhánh `release` chỉ chứa code đã hoàn thiện và kiểm thử đạt.
- **Quy tắc Tuyệt đối KHÔNG Merge `develop` vào `feature/fix` (Strict No-Develop-to-Feature Rule)**:
  - TUYỆT ĐỐI KHÔNG ĐƯỢC thực hiện `git merge develop` hoặc `git merge origin/develop` vào nhánh `feature/fix`.
  - Nhánh `develop` là nơi tích hợp code thử nghiệm của nhiều lập trình viên khác nhau. Nếu merge `develop` vào
    `feature/fix`, nhánh feature sẽ bị nhiễm code chưa hoàn thiện của các task khác, làm hỏng nhánh `release`.
- **Quy trình Xử lý Conflict khi đưa code vào `develop` (Develop Conflict Resolution Procedure)**:
  - Khi tạo Merge Request hoặc merge code vào `develop` mà bị conflict:
    1. `git checkout develop && git pull origin develop`
    2. `git merge <nhánh_feature_fix>`
    3. Xử lý các điểm conflict trực tiếp trên nhánh `develop`, giữ lại đầy đủ logic của cả 2 bên.
    4. Kiểm tra cú pháp, chạy test, sau đó `git commit` và `git push origin develop` để deploy mang đi test.
    5. BẮT BUỘC `git checkout <nhánh_feature_fix>` để quay trở lại nhánh feature sạch sẽ ban đầu.
- **URL Parameter cho MR**: Khi đưa link tạo MR trên GitLab cho lập trình viên, AI BẮT BUỘC phải đính kèm thêm
  tham số `&merge_request%5Btarget_branch%5D=develop` vào URL để GitLab tự động chọn nhánh đích là `develop`.
