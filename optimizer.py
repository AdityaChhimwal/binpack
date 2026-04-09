def optimize(ir):
    total_size = 0

    for field in ir["fields"]:
        total_size += field["size"]

    ir["total_size"] = total_size

    return ir


#Test
if __name__ == "__main__":
    from lexer import tokenize
    from parser import parse
    from semantic import analyze
    from intermediate import generate_ir

    with open("examples/player.pack") as f:
        code = f.read()

    tokens = tokenize(code)
    ast = parse(tokens)
    validated_ast = analyze(ast)
    ir = generate_ir(validated_ast)

    optimized_ir = optimize(ir)

    import json
    print("--- Optimized IR ---")
    print(json.dumps(optimized_ir, indent=4))