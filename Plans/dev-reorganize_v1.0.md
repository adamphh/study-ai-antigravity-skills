# Kế Hoạch Sắp Xếp Thư Mục Theo Khuyến Nghị Của Antigravity

Kế hoạch này đề xuất tái cấu trúc thư mục hiện tại của repository `study-ai-antigravity-skills` để đáp ứng đúng quy chuẩn lưu trữ tài liệu của Antigravity (đặc biệt là Repo Brain inputs và cấu trúc thư mục quy chuẩn).

## User Review Required

> [!IMPORTANT]
> Cần đổi tên một số tệp tài liệu hệ thống quan trọng sang dạng chữ IN HOA ở thư mục `docs/` để Antigravity AI Engine có thể tự động nhận dạng chính xác làm Repo Brain Context.

## Proposed Changes

---

### [Documentation & Brain Inputs]

#### [MODIFY] [README.md](file:///mnt/projects/study-ai-antigravity-skills/README.md)
- Cập nhật các đường dẫn tài liệu hệ thống từ chữ thường sang chữ in hoa (`docs/SYSTEM.md`, `docs/INVARIANTS.md`, `docs/SYNC_SPEC.md`).

#### [RENAME] `docs/system.md` -> [SYSTEM.md](file:///mnt/projects/study-ai-antigravity-skills/docs/SYSTEM.md)
- Đổi tên tệp kiến trúc hệ thống sang chữ IN HOA theo đúng chuẩn Repo Brain.

#### [RENAME] `docs/invariants.md` -> [INVARIANTS.md](file:///mnt/projects/study-ai-antigravity-skills/docs/INVARIANTS.md)
- Đổi tên tệp các luật không đổi sang chữ IN HOA.

#### [RENAME] `docs/sync_spec.md` -> [SYNC_SPEC.md](file:///mnt/projects/study-ai-antigravity-skills/docs/SYNC_SPEC.md)
- Đổi tên tệp spec đồng bộ dữ liệu sang chữ IN HOA.

#### [MODIFY] [guide.md](file:///mnt/projects/study-ai-antigravity-skills/docs/guide.md)
- Cập nhật lại các tham chiếu tài liệu hệ thống cho đồng bộ sang chữ in hoa.

---

### [Workflows]

#### [MODIFY] [magento-dev.md](file:///mnt/projects/study-ai-antigravity-skills/.agent/workflows/magento-dev.md)
- Sửa các đường dẫn trỏ tới skill files từ `Source/my-skills/` thành `my-skills/` vì repo này không chứa thư mục `Source` ở ngoài cùng.

#### [MODIFY] [react-dev.md](file:///mnt/projects/study-ai-antigravity-skills/.agent/workflows/react-dev.md)
- Sửa các đường dẫn trỏ tới skill files từ `Source/my-skills/` thành `my-skills/`.

#### [MODIFY] [skills.md](file:///mnt/projects/study-ai-antigravity-skills/.agent/workflows/skills.md)
- Sửa các đường dẫn trỏ tới skill files từ `Source/my-skills/` thành `my-skills/`.

#### [MODIFY] [webpos-dev.md](file:///mnt/projects/study-ai-antigravity-skills/.agent/workflows/webpos-dev.md)
- Sửa các đường dẫn trỏ tới skill files từ `Source/my-skills/` thành `my-skills/`.

---

### [Plans]

#### [NEW] [dev-reorganize_v1.0.md](file:///mnt/projects/study-ai-antigravity-skills/Plans/dev-reorganize_v1.0.md)
- Lưu trữ bản kế hoạch này trực tiếp vào thư mục `Plans/` theo đúng quy định.

#### [RENAME] `implementation_plan_pos.md` -> `Plans/deploy_pos_plan_v1.0.md`
- Di chuyển bản kế hoạch triển khai POS trước đó vào thư mục `Plans/` để quản lý tập trung và dọn dẹp thư mục gốc.

---

## Verification Plan

### Manual Verification
- Kiểm tra tính đúng đắn của các liên kết tài liệu trong `README.md`.
- Chạy thử các slash command hoặc verify sự hoạt động của các file markdown trong IDE để đảm bảo Antigravity nhận dạng tốt các files in hoa.
