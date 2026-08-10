import os
import datetime

class MarkdownWriter:
    """Formatter and writer for generating modular Markdown index files."""

    @staticmethod
    def get_header(title, scope=""):
        now_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        return f"""<!-- INDEX_METADATA
generated_at: {now_str}
target_scope: {scope}
-->

# {title}

> File chỉ mục được tạo tự động bởi Antigravity Script Indexer. Không sửa thủ công.

---
"""

    @staticmethod
    def format_file_link(file_path, line=None, label=None):
        file_path_clean = str(file_path).replace('\\', '/')
        if label is None:
            label = os.path.basename(file_path_clean)
        if line:
            return f"[`{label}#L{line}`](file://{file_path_clean}#L{line})"
        return f"[`{label}`](file://{file_path_clean})"

    @staticmethod
    def write_server_core_index(output_dir, vendor_map):
        """Write Server Core Index (Tầng 1) grouped by Vendor."""
        server_dir = os.path.join(output_dir, "server", "vendor")
        os.makedirs(server_dir, exist_ok=True)

        for vendor_name, modules in vendor_map.items():
            vendor_slug = vendor_name.lower()
            v_dir = os.path.join(server_dir, vendor_slug)
            os.makedirs(v_dir, exist_ok=True)

            md_content = MarkdownWriter.get_header(f"Vendor Core Index: {vendor_name}", scope=f"vendor/{vendor_name}")

            for mod_name, mod_data in modules.items():
                md_content += f"\n## Module: `{vendor_name}_{mod_name}`\n\n"
                md_content += "| Class / Interface | Methods & Signatures | Location |\n"
                md_content += "| :--- | :--- | :--- |\n"

                for cls_info in mod_data.get('classes', []):
                    cls_name = cls_info['full_class'] or cls_info['class_name']
                    methods_str = "<br/>".join([f"`{m['signature']}`" for m in cls_info['methods'][:5]])
                    if len(cls_info['methods']) > 5:
                        methods_str += f"<br/>*(+{len(cls_info['methods']) - 5} more)*"
                    link = MarkdownWriter.format_file_link(cls_info['file_path'])
                    md_content += f"| `{cls_name}` | {methods_str or 'N/A'} | {link} |\n"

            out_file = os.path.join(v_dir, "overview.md")
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(md_content)

    @staticmethod
    def write_client_core_index(output_dir, client_data):
        """Write Client Core Index (Tầng 1) for WebPOS JS."""
        client_dir = os.path.join(output_dir, "client", "webpos-core")
        os.makedirs(client_dir, exist_ok=True)

        # Services Index
        md_content = MarkdownWriter.get_header("WebPOS Client Core Services", scope="client/pos/src/service/")
        md_content += "| Service Name | Methods & Signatures | File Location |\n"
        md_content += "| :--- | :--- | :--- |\n"
        for srv in client_data.get('services', []):
            methods_str = "<br/>".join([f"`{m['signature']}`" for m in srv['methods'][:5]])
            link = MarkdownWriter.format_file_link(srv['file_path'])
            md_content += f"| `{srv['name']}` | {methods_str or 'N/A'} | {link} |\n"

        with open(os.path.join(client_dir, "core-services.md"), 'w', encoding='utf-8') as f:
            f.write(md_content)

    @staticmethod
    def write_project_local_index(output_dir, project_data):
        """Write Project Local Index (Tầng 2) for custom extensions/fixbugs."""
        server_local = os.path.join(output_dir, "server", "project-custom")
        client_local = os.path.join(output_dir, "client", "project-extensions")
        os.makedirs(server_local, exist_ok=True)
        os.makedirs(client_local, exist_ok=True)

        # Write Router INDEX.md
        router_content = MarkdownWriter.get_header("Project Local Index Router", scope="project-local")
        router_content += """
## 🖥️ Server FixBugs & Customizations
- 🛠️ **PHP Server Customizations**: [`magestore-fixbug.md`](file://""" + os.path.abspath(os.path.join(server_local, "magestore-fixbug.md")).replace('\\', '/') + """)

## 📱 WebPOS Client Extensions
- 🎨 **JS Extension Plugins**: [`extension-plugins.md`](file://""" + os.path.abspath(os.path.join(client_local, "extension-plugins.md")).replace('\\', '/') + """)
"""
        with open(os.path.join(output_dir, "INDEX.md"), 'w', encoding='utf-8') as f:
            f.write(router_content)

        # Write Client Extension Plugins
        c_content = MarkdownWriter.get_header("WebPOS Client Extension Plugins Matrix", scope="client/pos/src/extension/")
        c_content += "| Target Service / Component | Method | Type | Extension File |\n"
        c_content += "| :--- | :--- | :--- | :--- |\n"

        for p in project_data.get('js_plugins', []):
            link = MarkdownWriter.format_file_link(p['file'])
            c_content += f"| `{p['target']}` | `{p['method']}` | `{p['type']}` | {link} |\n"

        with open(os.path.join(client_local, "extension-plugins.md"), 'w', encoding='utf-8') as f:
            f.write(c_content)
