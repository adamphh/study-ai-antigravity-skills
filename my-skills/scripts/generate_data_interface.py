#!/usr/bin/env python3
"""
Sinh Api/Data/{Name}Interface.php + Model/{Name}.php + đoạn di.xml preference
cho 1 bảng Magento 2, dựa vào danh sách field lấy từ db_schema.xml hoặc
từ file JSON tự khai báo.

Cách dùng:

1) Đọc trực tiếp từ db_schema.xml có sẵn:
   python3 generate_data_interface.py \
       --schema-file /path/to/db_schema.xml \
       --table webpos_order_sync_queue \
       --vendor Magestore --module Webpos --name OrderSyncQueue \
       --output-dir ./output

2) Tự khai báo field qua JSON (khi chưa có db_schema.xml):
   python3 generate_data_interface.py \
       --fields-json fields.json \
       --table webpos_order_sync_queue \
       --vendor Magestore --module Webpos --name OrderSyncQueue \
       --output-dir ./output

   fields.json mẫu:
   [
     {"name": "entity_id", "xsi_type": "int", "primary": true},
     {"name": "order_id", "xsi_type": "int"},
     {"name": "status", "xsi_type": "varchar"},
     {"name": "synced_at", "xsi_type": "timestamp"}
   ]

Output: in ra 3 file - {Name}Interface.php, {Name}.php, di_xml_snippet.xml
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# Map kiểu dữ liệu XSD (db_schema.xml) -> kiểu PHP dùng cho docblock/type hint
XSD_TO_PHP = {
    "int": "int",
    "smallint": "int",
    "tinyint": "int",
    "boolean": "bool",
    "decimal": "float",
    "varchar": "string",
    "text": "string",
    "mediumtext": "string",
    "longtext": "string",
    "date": "string",
    "datetime": "string",
    "timestamp": "string",
    "blob": "string",
}


def to_studly(snake_str: str) -> str:
    """order_id -> OrderId"""
    return "".join(word.capitalize() for word in snake_str.split("_"))


def parse_fields_from_schema(schema_file: str, table_name: str):
    tree = ET.parse(schema_file)
    root = tree.getroot()
    ns = ""
    m = re.match(r"\{.*\}", root.tag)
    if m:
        ns = m.group(0)

    fields = []
    for table in root.findall(f"{ns}table"):
        if table.get("name") != table_name:
            continue
        # xác định primary key columns
        primary_cols = set()
        for constraint in table.findall(f"{ns}constraint"):
            if constraint.get("xsi:type") == "primary" or "primary" in (constraint.get("xsi:type") or ""):
                for col in constraint.findall(f"{ns}column"):
                    primary_cols.add(col.get("name"))

        for col in table.findall(f"{ns}column"):
            name = col.get("name")
            xsi_type = col.get("{http://www.w3.org/2001/XMLSchema-instance}type") or col.get("xsi:type")
            fields.append({
                "name": name,
                "xsi_type": xsi_type,
                "primary": name in primary_cols,
            })
        break
    else:
        print(f"Khong tim thay table '{table_name}' trong {schema_file}", file=sys.stderr)
        sys.exit(1)

    return fields


def parse_fields_from_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_interface(vendor, module, name, table_name, fields):
    php_type_of = lambda f: XSD_TO_PHP.get(f["xsi_type"], "string")

    const_lines = []
    method_lines = []
    for f in fields:
        const_name = f["name"].upper()
        const_lines.append(f'    public const {const_name} = \'{f["name"]}\';')

        studly = to_studly(f["name"])
        php_type = php_type_of(f)
        method_lines.append(f"""
    /**
     * @return {php_type}|null
     */
    public function get{studly}(): ?{php_type};

    /**
     * @param {php_type} ${f['name']}
     * @return $this
     */
    public function set{studly}({php_type} ${f['name']});""")

    consts = "\n".join(const_lines)
    methods = "".join(method_lines)

    return f"""<?php
declare(strict_types=1);

namespace {vendor}\\{module}\\Api\\Data;

/**
 * Interface cho entity {name} (bang: {table_name})
 */
interface {name}Interface
{{
{consts}
{methods}
}}
"""


def generate_model(vendor, module, name, table_name, fields):
    php_type_of = lambda f: XSD_TO_PHP.get(f["xsi_type"], "string")

    method_lines = []
    for f in fields:
        const_name = f["name"].upper()
        studly = to_studly(f["name"])
        php_type = php_type_of(f)
        method_lines.append(f"""
    /**
     * @inheritDoc
     */
    public function get{studly}(): ?{php_type}
    {{
        $value = $this->getData(self::{const_name});
        return $value === null ? null : ({php_type})$value;
    }}

    /**
     * @inheritDoc
     */
    public function set{studly}({php_type} ${f['name']})
    {{
        return $this->setData(self::{const_name}, ${f['name']});
    }}""")

    methods = "".join(method_lines)

    return f"""<?php
declare(strict_types=1);

namespace {vendor}\\{module}\\Model;

use Magento\\Framework\\Model\\AbstractModel;
use {vendor}\\{module}\\Api\\Data\\{name}Interface;
use {vendor}\\{module}\\Model\\ResourceModel\\{name} as {name}ResourceModel;

/**
 * Model cho entity {name} (bang: {table_name})
 */
class {name} extends AbstractModel implements {name}Interface
{{
    /**
     * @inheritDoc
     */
    protected function _construct(): void
    {{
        $this->_init({name}ResourceModel::class);
    }}
{methods}
}}
"""


def generate_di_snippet(vendor, module, name):
    return f"""<!-- Them doan nay vao trong the <config> cua etc/di.xml -->
<preference for="{vendor}\\{module}\\Api\\Data\\{name}Interface"
            type="{vendor}\\{module}\\Model\\{name}"/>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--schema-file", help="Duong dan toi db_schema.xml co san")
    parser.add_argument("--fields-json", help="Duong dan toi file JSON khai bao field thu cong")
    parser.add_argument("--table", required=True, help="Ten bang can sinh (dung khi doc tu db_schema.xml)")
    parser.add_argument("--vendor", required=True, help="Ten Vendor, VD: Magestore")
    parser.add_argument("--module", required=True, help="Ten Module, VD: Webpos")
    parser.add_argument("--name", required=True, help="Ten entity/class, VD: OrderSyncQueue")
    parser.add_argument("--output-dir", default=".", help="Thu muc luu file output")

    args = parser.parse_args()

    if not args.schema_file and not args.fields_json:
        print("Can truyen --schema-file hoac --fields-json", file=sys.stderr)
        sys.exit(1)

    if args.schema_file:
        fields = parse_fields_from_schema(args.schema_file, args.table)
    else:
        fields = parse_fields_from_json(args.fields_json)

    os.makedirs(args.output_dir, exist_ok=True)

    interface_code = generate_interface(args.vendor, args.module, args.name, args.table, fields)
    model_code = generate_model(args.vendor, args.module, args.name, args.table, fields)
    di_snippet = generate_di_snippet(args.vendor, args.module, args.name)

    interface_path = os.path.join(args.output_dir, f"{args.name}Interface.php")
    model_path = os.path.join(args.output_dir, f"{args.name}.php")
    di_path = os.path.join(args.output_dir, "di_xml_snippet.xml")

    with open(interface_path, "w", encoding="utf-8") as f:
        f.write(interface_code)
    with open(model_path, "w", encoding="utf-8") as f:
        f.write(model_code)
    with open(di_path, "w", encoding="utf-8") as f:
        f.write(di_snippet)

    print(f"Da sinh: {interface_path}")
    print(f"Da sinh: {model_path}")
    print(f"Da sinh: {di_path}")
    print("\nLuu y: kiem tra lai kieu du lieu PHP (int/string/float) co dung voi")
    print("nghiep vu thuc te khong, va bo sung ResourceModel/Collection neu chua co.")


if __name__ == "__main__":
    main()
