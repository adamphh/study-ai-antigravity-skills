# Git Commit & Extension Conflict Check Rules

## 1. Extension Plugin/Mixin Conflict Check Rule
- Trước khi đề xuất giải pháp hoặc tạo file kế hoạch (`implementation_plan.md`) cho bất kỳ React Component/Service nào trong WebPOS Client (`src/extension/`), AI BẮT BUỘC phải sử dụng `grep_search` kiểm tra trong thư mục `src/extension/` xem đã có extension nào khác đăng ký Plugin/Mixin/Rewrite cho cùng Class/Service/Component đó hay chưa.
- Nếu tìm thấy extension trùng lặp, AI phải báo cáo danh sách cụ thể cho lập trình viên để cùng đối soát logic, tránh xung đột hoặc đè logic lẫn nhau.

## 2. Git Commit Amend Rule
- Trước khi thực hiện `git commit`, AI phải dùng `git log -n 5` kiểm tra xem trên nhánh (branch) hiện tại đã có commit nào do AI thực hiện cho cùng mã Task/Issue này hay chưa.
- Nếu đã có commit trước đó cho task/issue hiện tại, AI BẮT BUỘC phải sử dụng `git commit --amend` (hoặc `git commit --amend --no-edit`) để gộp các thay đổi mới vào commit trước đó, đảm bảo không tạo thêm các commit rác trên lịch sử git repository.

## 3. Quy tắc Bắt buộc Chọn Nhánh Gốc Release & Merge Request (Git Base Branch & MR Target Rule)
- **Bắt buộc Rẽ Nhánh từ `release` (Mandatory Branching from `release`)**: Khi bắt đầu thực hiện bất kỳ task/issue/feature mới nào, AI BẮT BUỘC phải checkout và tạo nhánh mới từ nhánh `release` (`git checkout release && git pull origin release && git checkout -b <branch_name>`). TUYỆT ĐỐI KHÔNG ĐƯỢC tạo nhánh từ `develop` hoặc từ nhánh hiện tại (`current branch`).
- **Mục tiêu Merge Request (MR Target)**: Sau khi hoàn thành và commit mã nguồn trên nhánh task/issue, AI phải hướng dẫn hoặc đề xuất tạo Merge Request vào nhánh `develop` để tiến hành kiểm thử.
- **URL Parameter cho MR**: Khi đưa link tạo MR trên GitLab cho lập trình viên, AI BẮT BUỘC phải đính kèm thêm tham số `&merge_request%5Btarget_branch%5D=develop` vào URL để GitLab tự động chọn nhánh đích là `develop` thay vì lấy mặc định `release`.
