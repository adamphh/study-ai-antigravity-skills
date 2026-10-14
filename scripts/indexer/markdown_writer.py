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
                md_content += "| Class / Interface | Methods, Signatures & Line Numbers | Location |\n"
                md_content += "| :--- | :--- | :--- |\n"

                for cls_info in mod_data.get('classes', []):
                    cls_name = cls_info['full_class'] or cls_info['class_name']
                    methods_str = "<br/>".join([f"`{m['signature']}` (#L{m['line']})" for m in cls_info['methods'][:10]])
                    if len(cls_info['methods']) > 10:
                        methods_str += f"<br/>*(+{len(cls_info['methods']) - 10} more)*"
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
        md_content += "| Service Name | Methods, Signatures & Line Numbers | File Location |\n"
        md_content += "| :--- | :--- | :--- |\n"
        for srv in client_data.get('services', []):
            methods_str = "<br/>".join([f"`{m['signature']}` (#L{m['line']})" for m in srv['methods'][:10]])
            if len(srv['methods']) > 10:
                methods_str += f"<br/>*(+{len(srv['methods']) - 10} more)*"
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

        # 1. Write Router INDEX.md (using relative links)
        router_content = MarkdownWriter.get_header("Project Local Index Router", scope="project-local")
        router_content += """## 🖥️ Server FixBugs & Customizations
- 🛠️ **PHP Server Customizations**: [`magestore-fixbug.md`](server/project-custom/magestore-fixbug.md)

## 📱 WebPOS Client Extensions
- 🎨 **JS Extension Plugins**: [`extension-plugins.md`](client/project-extensions/extension-plugins.md)
"""
        with open(os.path.join(output_dir, "INDEX.md"), 'w', encoding='utf-8') as f:
            f.write(router_content)

        # 2. Write Server FixBugs Index (magestore-fixbug.md)
        s_content = MarkdownWriter.get_header("Magento 2 PHP Server Customizations & FixBugs", scope="app/code/Magestore/")
        
        s_content += "## 🔌 DI Plugins\n\n"
        if project_data.get('php_plugins'):
            s_content += "| Target Class | Plugin Name | Plugin Class | Sort Order | File |\n"
            s_content += "| :--- | :--- | :--- | :--- | :--- |\n"
            for p in project_data['php_plugins']:
                link = MarkdownWriter.format_file_link(p['file'])
                s_content += f"| `{p['target_class']}` | `{p['plugin_name']}` | `{p['plugin_class']}` | `{p['sort_order']}` | {link} |\n"
        else:
            s_content += "*No PHP DI plugins found.*\n"

        s_content += "\n## 🔄 DI Preferences (Rewrites)\n\n"
        if project_data.get('php_preferences'):
            s_content += "| For (Original Interface/Class) | Type (Rewrite Class) | File |\n"
            s_content += "| :--- | :--- | :--- |\n"
            for pref in project_data['php_preferences']:
                link = MarkdownWriter.format_file_link(pref['file'])
                s_content += f"| `{pref['for']}` | `{pref['type']}` | {link} |\n"
        else:
            s_content += "*No PHP preferences found.*\n"

        s_content += "\n## 📡 Event Observers\n\n"
        if project_data.get('php_observers'):
            s_content += "| Event Name | Observer Name | Observer Class | File |\n"
            s_content += "| :--- | :--- | :--- | :--- |\n"
            for obs in project_data['php_observers']:
                link = MarkdownWriter.format_file_link(obs['file'])
                s_content += f"| `{obs['event_name']}` | `{obs['observer_name']}` | `{obs['observer_class']}` | {link} |\n"
        else:
            s_content += "*No PHP observers found.*\n"

        with open(os.path.join(server_local, "magestore-fixbug.md"), 'w', encoding='utf-8') as f:
            f.write(s_content)

        # 3. Write Client Extension Plugins (extension-plugins.md)
        c_content = MarkdownWriter.get_header("WebPOS Client Extension Plugins Matrix", scope="client/pos/src/extension/")
        c_content += "## 🔌 Extension Plugins\n\n"
        if project_data.get('js_plugins'):
            c_content += "| Target Component / Service | Method / Plugin | Type | Config File |\n"
            c_content += "| :--- | :--- | :--- | :--- |\n"
            for p in project_data['js_plugins']:
                link = MarkdownWriter.format_file_link(p['file'])
                c_content += f"| `{p['target']}` | `{p['method']}` | `{p['type']}` | {link} |\n"
        else:
            c_content += "*No JS extension plugins registered.*\n"

        if project_data.get('js_mixins'):
            c_content += "\n## 🔀 Extension Mixins\n\n"
            c_content += "| Target | Mixin | Config File |\n"
            c_content += "| :--- | :--- | :--- |\n"
            for m in project_data['js_mixins']:
                link = MarkdownWriter.format_file_link(m['file'])
                c_content += f"| `{m['target']}` | `{m['mixin']}` | {link} |\n"

        if project_data.get('js_rewrites'):
            c_content += "\n## ✏️ Extension Rewrites\n\n"
            c_content += "| Target | Rewrite | Config File |\n"
            c_content += "| :--- | :--- | :--- |\n"
            for r in project_data['js_rewrites']:
                link = MarkdownWriter.format_file_link(r['file'])
                c_content += f"| `{r['target']}` | `{r['rewrite']}` | {link} |\n"

        with open(os.path.join(client_local, "extension-plugins.md"), 'w', encoding='utf-8') as f:
            f.write(c_content)
