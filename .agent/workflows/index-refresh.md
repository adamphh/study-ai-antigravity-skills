---
description: Làm mới bộ chỉ mục mã nguồn (Refresh Indexer) cho Shared Core hoặc Dự án hiện tại
---

# Slash Command: /index-refresh

Workflow này tự động thực thi làm mới bộ chỉ mục mã nguồn 2 Tầng.

## Cú pháp sử dụng trong Chat:
- `/index-refresh` hoặc `/index-refresh all`: Làm mới toàn bộ cả Tầng 1 (Shared Core) và Tầng 2 (Project hiện tại).
- `/index-refresh core`: Chỉ làm mới Tầng 1 (Shared Core Index dùng chung).
- `/index-refresh project`: Chỉ làm mới Tầng 2 (Project Local Index dự án hiện tại).

---

## Hướng dẫn thực thi tự động cho Agent:

1. Xác định tham số `target` từ câu lệnh của người dùng:
   - Nếu không nhập tham số hoặc nhập `all`: Thực thi cả **Bước A** và **Bước B**.
   - Nếu nhập `core`: Chỉ thực thi **Bước A**.
   - Nếu nhập `project`: Chỉ thực thi **Bước B**.

2. **Bước A (Làm mới Shared Core Index)**:
   Chạy lệnh terminal:
   ```bash
   python3 /mnt/projects/study-ai-antigravity-skills/scripts/index_core.py
   ```

3. **Bước B (Làm mới Project Local Index)**:
   Chạy lệnh terminal:
   ```bash
   python3 /mnt/projects/study-ai-antigravity-skills/scripts/index_project.py
   ```

4. Báo cáo ngắn gọn kết quả thời gian và đường dẫn file index đã làm mới cho người dùng.
