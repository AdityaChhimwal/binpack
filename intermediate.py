def generate_ir(ast):
    ir = {
        "name": ast["name"],
        "fields": [],
        "format_string": "<"  # little-endian
    }

    for field in ast["fields"]:
        field_name = field["name"]
        field_type = field["type"]

        if field_type == "int":
            ir["fields"].append({
                "name": field_name,
                "format": "i",
                "size": 4
            })
            ir["format_string"] += "i"

        elif field_type == "string":
            length = field["length"]
            ir["fields"].append({
                "name": field_name,
                "format": f"{length}s",
                "size": length
            })
            ir["format_string"] += f"{length}s"

    return ir


# Test 
if __name__ == "__main__":
    from lexer import tokenize
    from parser import parse
    from semantic import analyze

    with open("examples/player.pack") as f:
        code = f.read()

    tokens = tokenize(code)
    ast = parse(tokens)
    validated_ast = analyze(ast)

    ir = generate_ir(validated_ast)

    import json
    print("--- IR ---")
    print(json.dumps(ir, indent=4))