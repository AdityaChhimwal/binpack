from lexer import tokenize
from parser import parse
from semantic import analyze
from intermediate import generate_ir
from optimizer import optimize
from codegen import generate_code


def compile_code(code):
    try:
        tokens = tokenize(code)
    except Exception as e:
        return {"error": str(e), "phase": "Lexical"}

    try:
        ast = parse(tokens)
    except Exception as e:
        return {"error": str(e), "phase": "Syntax"}

    try:
        validated_ast = analyze(ast)
    except Exception as e:
        return {"error": str(e), "phase": "Semantic"}

    try:
        ir = generate_ir(validated_ast)
    except Exception as e:
        return {"error": str(e), "phase": "IR"}

    try:
        optimized_ir = optimize(ir)
    except Exception as e:
        return {"error": str(e), "phase": "Optimization"}

    try:
        generated_code = generate_code(optimized_ir)
    except Exception as e:
        return {"error": str(e), "phase": "CodeGen"}

    return {
        "ir": optimized_ir,
        "code": generated_code
    }