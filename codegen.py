# codegen.py

def generate_code(ir):
    class_name = ir["name"]
    format_str = ir["format_string"]
    total_size = ir["total_size"]
    fields = ir["fields"]

    field_names = [f["name"] for f in fields]

    code = ""

    # Import
    code += "import struct\n\n"

    # Class
    code += f"class {class_name}:\n"
    code += f"    FORMAT = '{format_str}'\n"
    code += f"    SIZE = {total_size}\n\n"

    # Constructor
    code += f"    def __init__(self, {', '.join(field_names)}):\n"
    for name in field_names:
        code += f"        self.{name} = {name}\n"
    code += "\n"

    # pack()
    code += "    def pack(self):\n"
    code += "        return struct.pack(\n"
    code += f"            self.FORMAT,\n"

    for f in fields:
        name = f["name"]
        if f["format"].endswith("s"):
            size = f["size"]
            code += f"            self.{name}.encode('utf-8').ljust({size}, b'\\x00'),\n"
        else:
            code += f"            self.{name},\n"

    code += "        )\n\n"

    # unpack()
    code += "    @staticmethod\n"
    code += "    def unpack(data):\n"
    code += "        unpacked = struct.unpack(\n"
    code += f"            '{format_str}', data\n"
    code += "        )\n\n"

    code += f"        return {class_name}(\n"
    for i, f in enumerate(fields):
        if f["format"].endswith("s"):
            code += f"            unpacked[{i}].decode('utf-8').rstrip('\\x00'),\n"
        else:
            code += f"            unpacked[{i}],\n"
    code += "        )\n\n"

    # 🔥 NEW: serialize list of JSON objects
    code += "\n# -------- Dataset Serialization --------\n"
    code += f"def serialize_list(data_list):\n"
    code += f"    result = b''\n"
    code += f"    for item in data_list:\n"
    code += f"        obj = {class_name}(\n"

    for f in fields:
        name = f["name"]
        code += f"            item['{name}'],\n"

    code += "        )\n"
    code += "        result += obj.pack()\n"
    code += "    return result\n\n"

    return code