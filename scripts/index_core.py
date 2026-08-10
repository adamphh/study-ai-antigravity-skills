#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from indexer.php_parser import PHPParser
from indexer.js_parser import JSParser
from indexer.markdown_writer import MarkdownWriter

def index_shared_core():
    """Script CLI to index Shared Core (Tầng 1)."""
    skills_root = Path(__file__).parent.parent
    output_dir = skills_root / "indexes"

    print("🚀 Starting Shared Core Indexing (Tầng 1)...")

    # Scanner targets
    vendor_map = {}
    client_data = {'services': [], 'epics': [], 'indexeddb': []}

    # Search for project roots
    projects_dir = Path("/mnt/projects")
    sample_project = None
    for p in projects_dir.iterdir():
        if p.is_dir() and (p / "Source").exists():
            sample_project = p / "Source"
            break

    if not sample_project or not sample_project.exists():
        print("⚠️ Could not find active Magento/WebPOS project directory under /mnt/projects/")
        return

    print(f"📦 Scanning Core files from: {sample_project}")

    # 1. Scan PHP Server Core (app/code/Magestore/ Core & vendor/magento/ Core)
    magestore_core_dir = sample_project / "server" / "app" / "code" / "Magestore"
    if magestore_core_dir.exists():
        for root, dirs, files in os.walk(magestore_core_dir):
            # Skip FixBug and Custom modules for Tier 1
            if 'FixBug' in root or 'Custom' in root:
                continue
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    parsed = PHPParser.parse_php_file(file_path)
                    if parsed and parsed['class_name']:
                        vendor = parsed['vendor']
                        module = parsed['module']
                        if vendor not in vendor_map:
                            vendor_map[vendor] = {}
                        if module not in vendor_map[vendor]:
                            vendor_map[vendor][module] = {'classes': []}
                        vendor_map[vendor][module]['classes'].append(parsed)

    # 2. Scan WebPOS JS Client Core (client/pos/src/service/)
    pos_service_dir = sample_project / "client" / "pos" / "src" / "service"
    if pos_service_dir.exists():
        for root, dirs, files in os.walk(pos_service_dir):
            for file in files:
                if file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    parsed = JSParser.parse_js_file(file_path)
                    if parsed:
                        client_data['services'].append(parsed)

    # Write Markdown Index Files
    MarkdownWriter.write_server_core_index(output_dir, vendor_map)
    MarkdownWriter.write_client_core_index(output_dir, client_data)

    print(f"✅ Shared Core Indexing Complete! Output saved to: {output_dir}")

if __name__ == "__main__":
    index_shared_core()
