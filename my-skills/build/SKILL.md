---
name: build
description: Triggered when the user runs /build or asks to checkout develop, pull latest code, build WebPOS client, and compress into build.tar.
---

# WebPOS Client Build and Package Workflow

Use this skill when the user runs `/build` or requests to package the WebPOS client for manual deployment.

## Workflow Steps

1. **Checkout develop branch & Pull latest code**:
   - Change directory to repository root
   - Run command: `git checkout develop && git pull origin develop`

2. **Build WebPOS Client**:
   - Change directory to `Source/client/pos`
   - Run command: `npm run build`

3. **Compress Build Artifact**:
   - Change directory to `Source/client/pos/build`
   - Run command: `tar -cvf build.tar .`

4. **Notify User**:
   - Verify file `Source/client/pos/build/build.tar` exists and display its absolute path and size.
   - Inform the user that the package is ready for manual deployment to the dev site.
