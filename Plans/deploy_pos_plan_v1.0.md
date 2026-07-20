# Deployment of POS to Internal Dev

This plan outlines the steps to build the POS application locally and deploy it to the internal development server.

## Proposed Changes

No code changes are proposed. This is a deployment task.

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
    -   Enter the Docker PHP container.
    -   Navigate to `app/code/Magestore/Webpos/build/apps`.
    -   Clean up the `pos` directory.
    -   Move and extract `build.tar` into the `pos` directory.
3.  **Magento Update**:
    -   Run `bin/magento webpos:deploy` from the project root.

## Verification Plan

### Manual Verification
-   Access the internal dev site and verify that the POS application reflects the latest changes from the `develop` branch.
