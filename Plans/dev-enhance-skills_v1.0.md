# Kế Hoạch Tích Hợp Và Nâng Cấp Local Skills (my-skills)

Kế hoạch này chi tiết hóa việc sao chép các tệp cấu hình nâng cao, kịch bản tự động hóa (scripts), danh sách chặn core modules từ Global Skills (`.gemini/config`) sang Local Skills (`my-skills`) để sử dụng hoàn toàn tại Workspace.

## User Review Required

> [!IMPORTANT]
> - Cần sao chép script Python `generate_data_interface.py` vào thư mục local để AI có thể tự chạy script sinh Model/Data Interface tự động.
> - Cần cập nhật tệp chỉ mục chính [SKILL.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/SKILL.md) vốn đang bị bỏ trống.

## Proposed Changes

---

### [Scripts & Automation]

#### [NEW] [generate_data_interface.py](file:///mnt/projects/study-ai-antigravity-skills/my-skills/scripts/generate_data_interface.py)
- Sao chép script Python tự động hóa sinh Data Interface & Model từ Global.

---

### [References & Safe-Guards]

#### [NEW] [protected-modules.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/protected-modules.md)
- Danh sách chặn và các quy định bảo vệ core module của Magestore/Webpos không cho phép sửa trực tiếp.

#### [NEW] [data-interface-model.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/data-interface-model.md)
- Hướng dẫn AI cách sử dụng script tự động hóa sinh Data Interface & Model.

#### [NEW] [data-patch.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/data-patch.md)
- Hướng dẫn viết Data Patch chuẩn cho Magento 2.4.x.

#### [NEW] [preference-virtualtype.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/preference-virtualtype.md)
- Hướng dẫn phân biệt và cấu hình Preference vs Virtual Type trong `di.xml`.

#### [NEW] [code-review.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/code-review.md)
- Quy chuẩn và checklist kiểm tra code/diff trước khi hợp nhất (merge).

#### [NEW] [debugging.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/references/debugging.md)
- Quy trình phân tích stack trace và gỡ lỗi (debug) Magento.

---

### [Indexes]

#### [MODIFY] [SKILL.md (Magento 2 index)](file:///mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/SKILL.md)
- Thêm phần "Kỹ năng nâng cao & Tài liệu tham chiếu" và liên kết tới các tài liệu mới trong thư mục `my-skills/references/`.
- Thêm quy chuẩn bắt buộc: kiểm tra danh sách module được bảo vệ trong `my-skills/references/protected-modules.md` trước khi sửa code.

#### [MODIFY] [SKILL.md (Root index)](file:///mnt/projects/study-ai-antigravity-skills/my-skills/SKILL.md)
- Điền đầy đủ thông tin metadata (name, description) và viết tài liệu hướng dẫn chỉ mục dẫn tới các bộ kỹ năng con (Magento 2, ReactJS, WebPOS).

---

## Verification Plan

### Manual Verification
- Kiểm tra tính hoạt động của các liên kết mới trong [SKILL.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/magento2-skills/SKILL.md).
- Thực thi thử script Python `my-skills/scripts/generate_data_interface.py --help` để đảm bảo script có thể chạy bình thường trong môi trường local.
