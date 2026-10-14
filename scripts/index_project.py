#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from indexer.php_parser import PHPParser
from indexer.js_parser import JSParser
from indexer.markdown_writer import MarkdownWriter

def index_project_local(project_dir=None):
    """Script CLI to index Project Local Customizations (Tầng 2)."""
    if not project_dir:
        cwd = Path.cwd()
        if (cwd / "Source").exists() or (cwd / "docs").exists():
            project_dir = cwd
        else:
            project_dir = Path("/mnt/projects/p1060-graceandmarbel.co.uk")
    else:
        project_dir = Path(project_dir)

    print(f"🚀 Starting Project Local Indexing (Tầng 2) for: {project_dir}")

    output_dir = project_dir / "docs" / "data-flows"
    os.makedirs(output_dir, exist_ok=True)

    project_data = {
        'php_plugins': [],
        'php_preferences': [],
        'php_observers': [],
        'js_plugins': [],
        'js_mixins': [],
        'js_rewrites': []
    }

    # 1. Scan WebPOS Extensions in client/pos/src/extension/
    ext_dir = project_dir / "Source" / "client" / "pos" / "src" / "extension"
    if not ext_dir.exists():
        ext_dir = project_dir / "client" / "pos" / "src" / "extension"

    if ext_dir.exists():
        for root, dirs, files in os.walk(ext_dir):
            for file in files:
                if file == 'config.js' and 'etc' in root:
                    config_path = os.path.join(root, file)
                    parsed_cfg = JSParser.parse_extension_config(config_path)
                    if parsed_cfg.get('plugins'):
                        project_data['js_plugins'].extend(parsed_cfg['plugins'])
                    if parsed_cfg.get('mixins'):
                        project_data['js_mixins'].extend(parsed_cfg['mixins'])
                    if parsed_cfg.get('rewrites'):
                        project_data['js_rewrites'].extend(parsed_cfg['rewrites'])

    # 2. Scan Magento PHP FixBugs in app/code/Magestore/FixBug*
    php_fixbug_dir = project_dir / "Source" / "server" / "app" / "code" / "Magestore"
    if not php_fixbug_dir.exists():
        php_fixbug_dir = project_dir / "app" / "code" / "Magestore"

    if php_fixbug_dir.exists():
        for root, dirs, files in os.walk(php_fixbug_dir):
            if 'FixBug' in root or 'Custom' in root:
                for file in files:
                    if file == 'di.xml':
                        plugins, prefs = PHPParser.parse_di_xml(os.path.join(root, file))
                        project_data['php_plugins'].extend(plugins)
                        project_data['php_preferences'].extend(prefs)
                    elif file == 'events.xml':
                        obs = PHPParser.parse_events_xml(os.path.join(root, file))
                        project_data['php_observers'].extend(obs)

    # Write Project Local Markdown Index
    MarkdownWriter.write_project_local_index(output_dir, project_data)

    print(f"✅ Project Local Indexing Complete! Output saved to: {output_dir}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    index_project_local(target)
