# Quy định Ưu tiên Định vị và Tìm kiếm Dự án / Workspace

1. **Ưu tiên Tìm kiếm tuyệt đối tại `/mnt/projects`**:
   - Khi người dùng yêu cầu mở dự án, tìm workspace, bắt đầu task hoặc tìm kiếm mã nguồn:
     AI **BẮT BUỘC** ưu tiên tìm kiếm và kiểm tra trong thư mục `/mnt/projects/` đầu tiên
     (ví dụ: `/mnt/projects/<ma_du_an>-*`, `/mnt/projects/study-ai-antigravity-skills`, ...).
   - Nếu đã tìm thấy workspace/dự án trong `/mnt/projects/`: **TUYỆT ĐỐI DỪNG LẠI**, không
     được tiếp tục tìm kiếm hoặc quét các thư mục con trong `/home/*` (như `/home/bss/*`).

2. **Quy định về phạm vi quét thư mục**:
   - Nghiêm cấm mọi hành vi tự ý quét toàn bộ thư mục `/home/bss` khi chưa kiểm tra `/mnt/projects`.
   - Chỉ khi nào tìm kiếm trong `/mnt/projects` không thấy kết quả VÀ có chỉ định cụ thể từ
     người dùng thì mới mở rộng phạm vi tìm kiếm.
