---
name: adam-audit-memory
description: Triggered when user runs /adam-audit-memory, /adam-healthcheck, /audit-memory or asks to audit rules, skills, token efficiency, and system health.
---

# Adam Audit Memory & System Healthcheck Workflow

Use this skill when the user triggers `/adam-audit-memory`, `/adam-healthcheck`, `/audit-memory`, or requests a comprehensive review of the AI configuration, rules, skills, and memory health.

## Objective
To inspect, detect redundancies, evaluate token efficiency, ensure rule consistency, and provide actionable optimization recommendations for the Antigravity setup.

## Audit Workflow Steps

### 1. Audit Rules & Declarative Memory (`~/.gemini/config/rules/`)
- Check all rule markdown files in `~/.gemini/config/rules/`.
- **Validation Criteria**:
  - Max line length <= 120 characters across all rule files.
  - No duplicate or contradictory instructions between rule files.
  - Clear separation between core safety rules and domain-specific knowledge.
  - Check static token footprint.

### 2. Audit Skills & Procedural Memory (`~/.gemini/config/skills/`)
- Inspect all skill directories and their `SKILL.md` definitions.
- **Validation Criteria**:
  - Valid YAML frontmatter (`name`, `description`).
  - Clear trigger conditions and actionable workflows.
  - Check whether referenced helper scripts exist and are executable.
  - Identify stale or outdated skills.

### 3. Audit Symlinks & Project Mappings
- Verify symlinks in `~/.gemini/config/` and `~/.agent/` pointing to `/mnt/projects/study-ai-antigravity-skills/`.
- Check `project-mapping.md` for project accuracy.

### 4. Audit Workspace Data Flows (if in an active project)
- Check if `docs/data-flows/README.md` or `docs/data-flows/INDEX.md` is present and up to date.

### 5. Generate System Health Report
Output a structured report in the following format:

```markdown
# 🏥 Antigravity System Health & Memory Audit Report

## 1. Bảng Tổng quan Sức khỏe Hệ thống
| Hạng mục | Trạng thái | Đánh giá & Điểm nổi bật |
| :--- | :---: | :--- |
| **Quy tắc Toàn cục (Global Rules)** | 🟢 / 🟡 / 🔴 | Đánh giá độ gọn gàng, tính nhất quán |
| **Thư viện Kỹ năng (Skills)** | 🟢 / 🟡 / 🔴 | Số lượng skill, tính hợp lệ của YAML |
| **Môi trường & Symlinks** | 🟢 / 🟡 / 🔴 | Kiểm tra liên kết thư mục |
| **Hiệu suất Token & Context** | 🟢 / 🟡 / 🔴 | Tối ưu hóa dung lượng prompt tĩnh |

## 2. Các Phát hiện & Khuyến nghị Tối ưu (Actionable Recommendations)
- **Điểm cần tối ưu 1:** [Mô tả chi tiết & cách xử lý]
- **Điểm cần tối ưu 2:** [Mô tả chi tiết & cách xử lý]
```
