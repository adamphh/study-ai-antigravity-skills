---
name: adam-plan-scaffold
description: Tự động khởi tạo tệp khung sườn kế hoạch chuẩn hóa trong thư mục Plans/ đúng định dạng {ma_du_an}-{ma_issue}-{noi_dung_20_ki_tu}.md. Sử dụng khi lập kế hoạch task mới hoặc gõ /adam-plan-scaffold.
---

# Kỹ năng Khởi Tạo Kế Hoạch Chuẩn (/adam-plan-scaffold)

Kỹ năng này tự động dựng sẵn tệp khung sườn kế hoạch đầy đủ các mục (Mục tiêu, Đối soát Data Flow, Đánh giá rủi ro, Triển khai và Kiểm thử) trong thư mục `Plans/`, giúp AI không cần tốn token "sáng tác" lại phần format văn bản mà chỉ việc điền nội dung nghiệp vụ.

---

## 🚀 Hướng Dẫn Thực Thi

```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-plan-scaffold/scripts/scaffold_plan.py <PROJECT_ID> <TASK_ID> "<TITLE_MAX_20_CHARS>" [--bug|--feature]
```

### Ví dụ:
```bash
python3 /mnt/projects/study-ai-antigravity-skills/my-skills/adam-plan-scaffold/scripts/scaffold_plan.py P1150 123 "Fix tax discount" --bug
```

Tệp được sinh ra: `Plans/P1150-123-fix-tax-discount.md`.
Sau đó AI chỉ cần mở file và điền nội dung nghiệp vụ.
