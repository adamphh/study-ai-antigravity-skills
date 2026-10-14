#!/usr/bin/env python3
"""
adam-conflict-auditor: Audits potential conflicts in Magento 2 di.xml (Backend)
and WebPOS client/pos/src/extension/*/etc/config.js (Frontend).
Usage:
  python3 audit_conflict.py --target-class <CLASS_NAME_OR_COMPONENT> [--method <METHOD_NAME>]
"""

import sys
import os
import re
import xml.etree.ElementTree as ET

def audit_backend_plugins(target_class):
    conflicts = []
    # Search di.xml in app/code/Magestore/
    app_code = "app/code/Magestore"
    if not os.path.exists(app_code):
        return conflicts

    for root, _, files in os.walk(app_code):
        for f in files:
            if f == "di.xml":
                di_path = os.path.join(root, f)
                try:
                    tree = ET.parse(di_path)
                    for type_elem in tree.findall(".//type"):
                        if type_elem.get("name") == target_class:
                            for plugin_elem in type_elem.findall("plugin"):
                                conflicts.append({
                                    "source": di_path,
                                    "type": "Backend Plugin",
                                    "target": target_class,
                                    "plugin_name": plugin_elem.get("name"),
                                    "plugin_type": plugin_elem.get("type")
                                })
                except Exception:
                    pass
    return conflicts

def audit_frontend_extensions(target_component):
    conflicts = []
    ext_dir = "client/pos/src/extension"
    if not os.path.exists(ext_dir):
        return conflicts

    # Search for config.js
    for root, _, files in os.walk(ext_dir):
        for f in files:
            if f == "config.js" and "etc" in root:
                cfg_path = os.path.join(root, f)
                try:
                    with open(cfg_path, "r", encoding="utf-8", errors="replace") as file_obj:
                        content = file_obj.read()
                    if target_component in content:
                        conflicts.append({
                            "source": cfg_path,
                            "type": "Frontend Extension Registration",
                            "target": target_component,
                            "file": cfg_path
                        })
                except Exception:
                    pass
    return conflicts

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--target-class":
        print("Usage: python3 audit_conflict.py --target-class <CLASS_OR_COMPONENT_NAME>")
        sys.exit(1)

    target = sys.argv[2].strip()
    print(f"🔍 Auditing conflicts for target: {target}...")

    be_conflicts = audit_backend_plugins(target)
    fe_conflicts = audit_frontend_extensions(target)

    all_conflicts = be_conflicts + fe_conflicts

    if not all_conflicts:
        print(f"✅ NO CONFLICTS FOUND for '{target}'. You can safely create plugins/rewrites.")
        sys.exit(0)
    else:
        print(f"⚠️ POTENTIAL CONFLICTS DETECTED ({len(all_conflicts)}):")
        for idx, c in enumerate(all_conflicts, 1):
            print(f"{idx}. [{c['type']}] in {c['source']}")
            if "plugin_name" in c:
                print(f"   Plugin Name: {c['plugin_name']} -> {c['plugin_type']}")
        sys.exit(0)

if __name__ == "__main__":
    main()
