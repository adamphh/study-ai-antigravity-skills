import os
import re

class JSParser:
    """Parser for WebPOS Client JS files and extension etc/config.js configurations."""

    @staticmethod
    def parse_extension_config(config_path):
        """Parse src/extension/{ext_name}/etc/config.js for plugins, mixins, rewrites, observers."""
        if not os.path.exists(config_path):
            return {}

        try:
            with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            plugins = []
            mixins = []
            rewrites = []
            observers = []

            # Extract plugin blocks: target_service: { plugin_name: { sortOrder, around/before/after } }
            plugin_block_match = re.search(r'plugin\s*=\s*\{([\s\S]*?)\};', content) or re.search(r'plugin\s*:\s*\{([\s\S]*?)\}', content)
            if plugin_block_match:
                plugin_str = plugin_block_match.group(1)
                # Regex match target classes/services
                target_matches = re.finditer(r'([A-Za-z0-9_]+)\s*:\s*\{([\s\S]*?)\n\s*\}', plugin_str)
                for tm in target_matches:
                    target_name = tm.group(1)
                    body = tm.group(2)
                    # Find method plugins inside
                    method_matches = re.finditer(r'([A-Za-z0-9_]+)\s*:\s*\{([\s\S]*?)\}', body)
                    for mm in method_matches:
                        method_name = mm.group(1)
                        m_body = mm.group(2)
                        p_type = 'around' if 'around' in m_body else ('before' if 'before' in m_body else 'after')
                        plugins.append({
                            'target': target_name,
                            'method': method_name,
                            'type': p_type,
                            'file': config_path
                        })

            # Extract mixin blocks
            mixin_match = re.search(r'mixin\s*=\s*\{([\s\S]*?)\};', content) or re.search(r'mixin\s*:\s*\{([\s\S]*?)\}', content)
            if mixin_match:
                m_str = mixin_match.group(1)
                for tm in re.finditer(r'([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)', m_str):
                    mixins.append({
                        'target': tm.group(1),
                        'mixin': tm.group(2),
                        'file': config_path
                    })

            # Extract rewrite blocks
            rewrite_match = re.search(r'rewrite\s*=\s*\{([\s\S]*?)\};', content) or re.search(r'rewrite\s*:\s*\{([\s\S]*?)\}', content)
            if rewrite_match:
                r_str = rewrite_match.group(1)
                for tm in re.finditer(r'([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)', r_str):
                    rewrites.append({
                        'target': tm.group(1),
                        'rewrite': tm.group(2),
                        'file': config_path
                    })

            return {
                'plugins': plugins,
                'mixins': mixins,
                'rewrites': rewrites,
                'file': config_path
            }
        except Exception as e:
            return {}

    @staticmethod
    def parse_js_file(js_path):
        """Parse JS Service / Epic / Helper file to extract methods and signatures."""
        if not os.path.exists(js_path):
            return None

        try:
            with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            file_name = os.path.basename(js_path).replace('.js', '')
            methods = []

            for idx, line in enumerate(lines, 1):
                # Extract methods: methodName(arg1, arg2) { ... } or methodName: function(arg1, arg2)
                m_match = re.search(r'^\s*(?:async\s+)?([A-Za-z0-9_]+)\s*\(([^)]*)\)\s*\{', line) or \
                          re.search(r'^\s*([A-Za-z0-9_]+)\s*:\s*(?:async\s+)?function\s*\(([^)]*)\)', line)
                if m_match:
                    name = m_match.group(1)
                    if name not in ['if', 'for', 'while', 'switch', 'catch', 'constructor']:
                        params = " ".join(m_match.group(2).split())
                        methods.append({
                            'name': name,
                            'signature': f"{name}({params})",
                            'line': idx
                        })

            return {
                'file_path': js_path,
                'name': file_name,
                'methods': methods
            }
        except Exception as e:
            return None
