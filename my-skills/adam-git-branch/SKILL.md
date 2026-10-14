---
name: adam-git-branch
description: Tự động kiểm tra working tree, fetch origin/release và tạo nhánh fix/ hoặc feature/ chuẩn xác theo định dạng chỉ trong 1 lệnh duy nhất. Sử dụng khi bắt đầu task hoặc gõ /adam-git-branch.
---

# Kỹ năng Chuẩn Bị Git Branch (/adam-git-branch)

Kỹ năng này tự động hóa toàn bộ thao tác kiểm tra working tree, đồng bộ nhánh `origin/release` và rẽ nhánh mới (`fix/...` hoặc `feature/...`) với tên chuẩn kebab-case $\le 30$ ký tự chỉ trong **1 lệnh terminal duy nhất (1 turn)** thay vì 3-4 lệnh, tiết kiệm token tối đa.

---

## 🚀 Hướng Dẫn Thực Thi

```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-git-branch/scripts/prepare_branch.py <TASK_KEY> "<TASK_SUMMARY>" [--bug|--feature]
```

### Ví dụ:
- Bug: `python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-git-branch/scripts/prepare_branch.py P1150-123 "Fix tax calculation in checkout" --bug`
- Feature: `python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-git-branch/scripts/prepare_branch.py P1150-124 "Add terminal payment method" --feature`

### Kết quả:
Tự động rẽ nhánh: `fix/P1150-123-fix-tax-calculation-in-checkout` từ `origin/release`.
