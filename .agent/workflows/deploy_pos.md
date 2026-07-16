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
    -   Upload to `/var/www/html/p1062-jw/envs/jw-sc-20240115/src/app/code/Magestore/Webpos/build/apps/`.
2.  **Server Commands**:
    -   SSH into the server.
    host: internal-dev.magestore.com
    user: rong
    pass: 4HivoHVkZ4AgjjK7xCxvke3x3gFSefkf^#pHC7KgPXh7R
    -   Go to folder /var/www/html/p1062-jw/envs/jw-sc-20240115/src/
    -   Enter the Docker PHP container.
    docker compose exec php bash 
    -   Navigate to `app/code/Magestore/Webpos/build/apps`.
    -   Clean up the `pos` directory.
    rm -rf pos/*
    -   Move and extract `build.tar` into the `pos` directory.
    cp build.tar pos/
    - Go to pos directory and extract build.tar
    cd pos
    tar -xvf build.tar
3.  **Magento Update**:
    -   Run `bin/magento webpos:deploy` from the project root.

## Verification Plan

### Manual Verification
-   Access the internal dev site and verify that the POS application reflects the latest changes from the `develop` branch.
