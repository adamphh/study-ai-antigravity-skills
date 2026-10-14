#!/usr/bin/env python3
"""
adam-plan-scaffold: Generates standardized Plan markdown file in Plans/ directory.
Usage:
  python3 scaffold_plan.py <PROJECT_ID> <TASK_ID> "<TITLE_MAX_20_CHARS>"
"""

import sys
import os
import re
import datetime

PLAN_TEMPLATE = """# Kế hoạch Thực Hiện: {project_id}-{task_id} - {title}

- **Mã Task**: {project_id}-{task_id}
- **Loại Task**: {task_type}
- **Ngày lập**: {today}
- **Trạng thái**: Chờ duyệt (Pending Approval)

---

## 1. Mục Tiêu & Nghiệp Vụ Cần Xử Lý
- **Vấn đề hiện tại**: <Mô tả lỗi hoặc nghiệp vụ cần thực hiện>
- **Kết quả mong muốn**: <Mô tả hành vi đúng sau khi hoàn thành>

---

## 2. Đối Soát Data Flow & Xung Đột (Conflict Audit)
- **Data Flow liên quan**: `docs/data-flows/<domain>/...`
- **Phạm vi tác động (Scope)**:
  - Backend: `app/code/Magestore/*FixBug*` hoặc `*Custom*`
  - Frontend: `client/pos/src/extension/*fix-bug*` hoặc `*custom*`
- **Kết quả kiểm tra xung đột**: <Đã kiểm tra qua adam-conflict-auditor: Không có xung đột / Có xung đột...>

---

## 3. Đánh Giá Mức Độ Rủi Ro (Risk Assessment)
- [ ] **Thanh toán (Payment / Terminal)**: Có / Không
- [ ] **Tồn kho & Đơn hàng (MSI / Stock Deduction)**: Có / Không
- [ ] **Đồng bộ ngoại tuyến & CSDL (IndexedDB / Realtime Reindex)**: Có / Không
- [ ] **Core API Override**: Có / Không

*(Nếu có bất kỳ mục nào là "Có" -> Bắt buộc gọi Subagent Review tại Bước 9)*

---

## 4. Các Bước Triển Khai Chi Tiết (Implementation Steps)
1. **Bước 1**: <Chi tiết bước 1>
2. **Bước 2**: <Chi tiết bước 2>
3. **Bước 3**: <Chi tiết bước 3>

---

## 5. Kế Hoạch Kiểm Thử (Verification Plan)
### A. Kiểm thử Tự Động (Automated Tests)
- Chạy unit test / integration test: `<câu lệnh test>`

### B. Kiểm thử Thủ Công (Manual Testing)
1. Bước 1: ...
2. Bước 2: ...
"""

def slugify(text, max_len=20):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text[:max_len].rstrip('-')

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 scaffold_plan.py <PROJECT_ID> <TASK_ID> <TITLE_MAX_20_CHARS> [--bug|--feature]")
        sys.exit(1)

    project_id = sys.argv[1].upper()
    task_id = sys.argv[2]
    title = sys.argv[3]
    task_type = "Bug Fix" if "--bug" in sys.argv else "Feature / Improvement"

    slug = slugify(title, 20)
    file_name = f"{project_id}-{task_id}-{slug}.md"
    os.makedirs("Plans", exist_ok=True)
    file_path = os.path.join("Plans", file_name)

    content = PLAN_TEMPLATE.format(
        project_id=project_id,
        task_id=task_id,
        title=title,
        task_type=task_type,
        today=datetime.date.today().isoformat()
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Scaffolded Plan created at: {file_path}")

if __name__ == "__main__":
    main()
