#!/usr/bin/env python3
"""
adam-build: Fast deterministic WebPOS Client builder & packager for Antigravity.
Builds React WebPOS client and packages it into build.tar in a single turn without log bloat.

Usage:
  python3 build_pos.py [--branch <name>] [--no-pull] [--upgrade] [--path <project_root>]
"""

import sys
import os
import subprocess
import argparse
import time
import shutil

def run_cmd(cmd, cwd=None, capture=True):
    """
    Run command and return status and output.
    """
    res = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=capture,
        text=True
    )
    return res.returncode, res.stdout, res.stderr

def format_size(bytes_size):
    """
    Format bytes to human readable string (KB, MB).
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def locate_pos_dir(base_path):
    """
    Locate WebPOS client directory containing package.json with build script.
    Checks common project structures:
    - ./Source/client/pos
    - ./client/pos
    - ./pos
    - Current directory if package.json exists
    """
    candidates = [
        os.path.join(base_path, "Source", "client", "pos"),
        os.path.join(base_path, "client", "pos"),
        os.path.join(base_path, "pos"),
        base_path
    ]
    for c in candidates:
        pkg = os.path.join(c, "package.json")
        if os.path.isfile(pkg):
            return os.path.abspath(c)
    return None

def main():
    parser = argparse.ArgumentParser(
        description="adam-build: Build WebPOS client and package build.tar in 1 turn."
    )
    parser.add_argument(
        "--branch",
        type=str,
        default=None,
        help="Optional branch to checkout and pull (overrides default 'develop')."
    )
    parser.add_argument(
        "--keep-branch",
        action="store_true",
        help="Build on current branch instead of checking out 'develop'."
    )
    parser.add_argument(
        "--no-pull",
        action="store_true",
        help="Do not pull remote changes; build from current working tree."
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Run 'npm run upgrade' before building to register extension modules."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="Project root directory path (defaults to current working directory)."
    )

    args = parser.parse_args()
    project_root = os.path.abspath(args.path)
    start_time = time.time()

    print(f"🚀 Starting WebPOS Client Build in: {project_root}")

    # 1. Determine target branch and checkout/pull
    # Default behavior: checkout and pull 'develop' unless --keep-branch or custom --branch is specified
    target_branch = args.branch if args.branch else (None if args.keep_branch else "develop")

    if target_branch:
        print(f"🌿 Switching to branch: {target_branch}...")
        code, out, err = run_cmd(f"git checkout {target_branch}", cwd=project_root)
        if code != 0:
            print(f"❌ Failed to checkout branch {target_branch}:\n{err.strip()}")
            sys.exit(1)

        if not args.no_pull:
            print(f"📡 Pulling latest changes from origin/{target_branch}...")
            code, out, err = run_cmd(f"git pull origin {target_branch}", cwd=project_root)
            if code != 0:
                print(f"⚠️ Warning: git pull returned non-zero code:\n{err.strip()}")
    elif not args.no_pull:
        # Keep branch: pull on current branch
        code, cur_branch, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=project_root)
        cur_branch = cur_branch.strip()
        if cur_branch and cur_branch != "HEAD":
            print(f"📡 Pulling latest changes on current branch ({cur_branch})...")
            code, _, err = run_cmd(f"git pull origin {cur_branch}", cwd=project_root)
            if code != 0:
                print(f"⚠️ Warning: git pull on {cur_branch} returned non-zero code:\n{err.strip()}")

    # 2. Locate client pos directory
    pos_dir = locate_pos_dir(project_root)
    if not pos_dir:
        print(f"❌ Could not find WebPOS client directory in '{project_root}'.")
        print("   Expected 'Source/client/pos' or 'client/pos' with package.json.")
        sys.exit(1)

    print(f"📁 WebPOS Directory: {pos_dir}")

    # 3. Optional: Run npm run upgrade
    if args.upgrade:
        print("⚙️ Running 'npm run upgrade' to register extensions...")
        code, out, err = run_cmd("npm run upgrade", cwd=pos_dir)
        if code != 0:
            print(f"❌ 'npm run upgrade' failed:\n{err.strip() or out.strip()}")
            sys.exit(1)

    # 4. Build client (npm run build)
    print("🔨 Compiling WebPOS client (npm run build)...")
    build_start = time.time()
    code, out, err = run_cmd("npm run build", cwd=pos_dir)
    build_duration = time.time() - build_start

    if code != 0:
        print("❌ Build failed!")
        # Print only last 25 lines of output/error to avoid token flood
        combined_err = (err.strip() or out.strip()).splitlines()
        tail_err = "\n".join(combined_err[-25:])
        print(f"--- Build Error Tail ---\n{tail_err}\n------------------------")
        sys.exit(1)

    build_dir = os.path.join(pos_dir, "build")
    if not os.path.isdir(build_dir):
        print(f"❌ Build directory '{build_dir}' not found after compile.")
        sys.exit(1)

    # 5. Compress build artifacts into build.tar (Quiet, NO -v)
    print("📦 Packaging build folder into build.tar...")
    tar_path = os.path.join(build_dir, "build.tar")
    if os.path.exists(tar_path):
        try:
            os.remove(tar_path)
        except Exception:
            pass

    # Using tar without -v for zero log bloat
    code, _, err = run_cmd("tar -cf build.tar .", cwd=build_dir)
    if code != 0 or not os.path.isfile(tar_path):
        print(f"❌ Failed to create build.tar:\n{err.strip()}")
        sys.exit(1)

    # 6. Summary Output (Clean & Minimal)
    tar_size = os.path.getsize(tar_path)
    total_time = time.time() - start_time

    print("-" * 50)
    print("🎉 WEBPOS CLIENT BUILD & PACKAGE SUCCESSFUL!")
    print(f"📦 Artifact : {tar_path}")
    print(f"📊 Size     : {format_size(tar_size)} ({tar_size:,} bytes)")
    print(f"⏱️ Duration : Build {build_duration:.1f}s | Total {total_time:.1f}s")
    print("-" * 50)

if __name__ == "__main__":
    main()
