---
name: deploy pos to internal dev
description: deploy pos to internal dev
---

# deploy pos to internal dev
Khi nhận yêu cầu phát triển React, hãy làm theo các bước sau:

## Prerequisites

- Node.js (v14 or higher)
- Yarn (v1.22 or higher)
- Git
- SSH key pair

## Steps

### Local Preparation

1.  **Repository Setup**:
    -   Switch to the `develop` branch.
    -   Pull latest source code.
2.  **Build Process**:
    -   Navigate to `Source/client/pos`.
    -   Run `npm install` to ensure dependencies are up to date.
    -   Run `npm run build` to create the production build.
3.  **Artifact Creation**:
    -   Navigate to the build directory (usually `Source/client/pos/build`).
    -   Create a tarball `build.tar` containing the build files.

### Server Deployment

1.  **File Transfer**:
    -   Use `scp` to upload `build.tar` to `internal-dev.magestore.com`.
    -   Upload target path: `/var/www/html/{ProjectCode}-{ProjectName}/envs/default/src/app/code/Magestore/Webpos/build/apps/`.
2.  **Server Commands**:
    -   SSH into the server: `ssh <username>@internal-dev.magestore.com` (Sử dụng SSH key/credentials đã được cấu hình sẵn trên máy trạm của bạn).
    -   Di chuyển vào thư mục dự án: `cd /var/www/html/{ProjectCode}-{ProjectName}/envs/default/src/`
    -   Truy cập vào Docker PHP container: `docker compose exec php bash`
    -   Di chuyển vào thư mục build apps của WebPOS: `cd app/code/Magestore/Webpos/build/apps`
    -   Dọn dẹp thư mục `pos/` hiện tại: `rm -rf pos/*`
    -   Di chuyển và giải nén `build.tar` vào thư mục `pos/`:
        ```bash
        cp build.tar pos/
        cd pos
        tar -xvf build.tar
        ```
3.  **Magento Update**:
    -   Chạy lệnh deploy WebPOS từ thư mục root của Magento: `bin/magento webpos:deploy`

## Quy tắc xử lý Context (Dành cho AI)

Khi thực thi workflow này, AI **bắt buộc** phải tự động trích xuất các biến ngữ cảnh dựa vào Git branch đang active hoặc đường dẫn workspace hiện hành:
- **`{ProjectCode}`**: Mã dự án viết thường (ví dụ: `p1146`, `p1062`). Trích xuất từ tên Git branch (ví dụ: `P1146-154-...` -> `p1146`) hoặc thư mục workspace.
- **`{ProjectName}`**: Tên dự án viết thường (ví dụ: `constellationmusical-com`, `jw`). Trích xuất từ tên Git branch hoặc thư mục workspace.
- **SSH Authentication**: AI không được yêu cầu mật khẩu plaintext. AI sẽ tự động sinh lệnh kết nối sử dụng khóa SSH (SSH Key) hoặc alias cấu hình trong file `~/.ssh/config`.

## Verification Plan

### Manual Verification
-   Access the internal dev site and verify that the POS application reflects the latest changes from the `develop` branch.
