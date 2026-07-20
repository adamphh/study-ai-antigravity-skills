# Kế Hoạch Bổ Sung Kỹ Năng Khởi Tạo Dự Án (Init Project)

Kế hoạch này thực hiện việc bổ sung kỹ năng `init-project` vào bộ kỹ năng local `my-skills/` và đăng ký nó vào tệp chỉ mục chính để AI có thể tự động hóa việc khởi tạo cấu hình dự án mới cho lập trình viên.

## User Review Required

> [!IMPORTANT]
> Sẽ tạo mới thư mục kỹ năng [my-skills/init-project/](file:///mnt/projects/study-ai-antigravity-skills/my-skills/init-project/) và tệp [SKILL.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/init-project/SKILL.md) hướng dẫn AI tự động symlink `.agent/` và copy `docs/` template khi nhận lệnh khởi tạo dự án.

## Proposed Changes

---

### [New Skills]

#### [NEW] [SKILL.md (init-project)](file:///mnt/projects/study-ai-antigravity-skills/my-skills/init-project/SKILL.md)
- Tạo tệp đặc tả kỹ năng `init-project` hướng dẫn AI chạy lệnh shell `ln -s` và `cp -r` để khởi tạo dự án mới.

---

### [Indexes]

#### [MODIFY] [SKILL.md (Root index)](file:///mnt/projects/study-ai-antigravity-skills/my-skills/SKILL.md)
- Bổ sung liên kết dẫn tới kỹ năng mới [init-project/SKILL.md](file:///mnt/projects/study-ai-antigravity-skills/my-skills/init-project/SKILL.md) vào danh sách kỹ năng chính.

---

## Verification Plan

### Manual Verification
- Kiểm tra tính đúng đắn của tệp `my-skills/init-project/SKILL.md` mới tạo.
- Xác thực liên kết đến kỹ năng mới trong tệp chỉ mục chính `my-skills/SKILL.md`.
