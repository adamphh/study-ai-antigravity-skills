import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

class PHPParser:
    """Parser for Magento 2 PHP files and XML configuration files (di.xml, events.xml)."""

    @staticmethod
    def detect_vendor_module(path_str):
        """Detect vendor and module name from file path."""
        path_str = path_str.replace('\\', '/')
        if 'app/code/' in path_str:
            parts = path_str.split('app/code/')[1].split('/')
            if len(parts) >= 2:
                return parts[0], parts[1]
        elif 'vendor/' in path_str:
            parts = path_str.split('vendor/')[1].split('/')
            if len(parts) >= 2:
                return parts[0], parts[1]
        return 'Unknown', 'Unknown'

    @staticmethod
    def parse_di_xml(xml_path):
        """Parse di.xml for plugins, preferences, and virtualTypes."""
        plugins = []
        preferences = []
        if not os.path.exists(xml_path):
            return plugins, preferences

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract preferences
            for pref in root.findall('.//preference'):
                for_cls = pref.attrib.get('for')
                type_cls = pref.attrib.get('type')
                if for_cls and type_cls:
                    preferences.append({
                        'for': for_cls,
                        'type': type_cls,
                        'file': xml_path
                    })

            # Extract plugins
            for type_tag in root.findall('.//type'):
                target_cls = type_tag.attrib.get('name')
                for plugin_tag in type_tag.findall('plugin'):
                    plugin_name = plugin_tag.attrib.get('name')
                    plugin_type = plugin_tag.attrib.get('type')
                    sort_order = plugin_tag.attrib.get('sortOrder', '10')
                    disabled = plugin_tag.attrib.get('disabled', 'false')
                    if target_cls and plugin_type:
                        plugins.append({
                            'target_class': target_cls,
                            'plugin_name': plugin_name,
                            'plugin_class': plugin_type,
                            'sort_order': sort_order,
                            'disabled': disabled,
                            'file': xml_path
                        })

            # Extract type-level plugins
            for plugin_tag in root.findall('.//plugin'):
                target_cls = plugin_tag.attrib.get('for') or plugin_tag.parent.attrib.get('name') if hasattr(plugin_tag, 'parent') else None
                plugin_name = plugin_tag.attrib.get('name')
                plugin_type = plugin_tag.attrib.get('type')
                if target_cls and plugin_type and not any(p['plugin_name'] == plugin_name for p in plugins):
                    plugins.append({
                        'target_class': target_cls,
                        'plugin_name': plugin_name,
                        'plugin_class': plugin_type,
                        'sort_order': plugin_tag.attrib.get('sortOrder', '10'),
                        'disabled': plugin_tag.attrib.get('disabled', 'false'),
                        'file': xml_path
                    })

        except Exception as e:
            pass

        return plugins, preferences

    @staticmethod
    def parse_events_xml(xml_path):
        """Parse events.xml for observers."""
        observers = []
        if not os.path.exists(xml_path):
            return observers

        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            for event_tag in root.findall('.//event'):
                event_name = event_tag.attrib.get('name')
                for obs_tag in event_tag.findall('observer'):
                    obs_name = obs_tag.attrib.get('name')
                    obs_cls = obs_tag.attrib.get('instance')
                    disabled = obs_tag.attrib.get('disabled', 'false')
                    if event_name and obs_cls:
                        observers.append({
                            'event_name': event_name,
                            'observer_name': obs_name,
                            'observer_class': obs_cls,
                            'disabled': disabled,
                            'file': xml_path
                        })
        except Exception as e:
            pass

        return observers

    @staticmethod
    def parse_php_file(php_path):
        """Parse PHP file to extract class name, namespace, and method signatures."""
        if not os.path.exists(php_path):
            return None

        try:
            with open(php_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            namespace = ""
            class_name = ""
            methods = []

            for idx, line in enumerate(lines, 1):
                # Extract namespace
                ns_match = re.search(r'^\s*namespace\s+([^;]+);', line)
                if ns_match:
                    namespace = ns_match.group(1).strip()

                # Extract class or interface name
                cls_match = re.search(r'^\s*(?:final\s+|abstract\s+)?(?:class|interface|trait)\s+([A-Za-z0-9_]+)', line)
                if cls_match:
                    class_name = cls_match.group(1).strip()

                # Extract method signatures
                method_match = re.search(r'^\s*(public|protected|private)\s+(?:static\s+)?function\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)', line)
                if method_match:
                    visibility = method_match.group(1)
                    method_name = method_match.group(2)
                    params = method_match.group(3).strip()
                    # Clean params
                    params_clean = " ".join(params.split())
                    methods.append({
                        'name': method_name,
                        'visibility': visibility,
                        'signature': f"{method_name}({params_clean})",
                        'line': idx
                    })

            full_class = f"{namespace}\\{class_name}" if namespace and class_name else class_name
            vendor, module = PHPParser.detect_vendor_module(php_path)

            return {
                'file_path': php_path,
                'namespace': namespace,
                'class_name': class_name,
                'full_class': full_class,
                'vendor': vendor,
                'module': module,
                'methods': methods
            }
        except Exception as e:
            return None
