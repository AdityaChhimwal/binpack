
import sys

def analyze(ast):
    """
    Takes the parsed Abstract Syntax Tree (AST) and checks for logical errors.
    Returns the AST unchanged if everything is perfectly valid.
    """
    
    # Keep track of names we've already seen to catch duplicates
    seen_field_names = set()
    
    struct_name = ast["name"]
    fields = ast["fields"]
    
    print(f"Analyzing struct: {struct_name}...")
    
    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        
        # 1. Duplicate Detection
        if field_name in seen_field_names:
            print(f"Semantic Error: Duplicate field name '{field_name}' in struct '{struct_name}'.")
            sys.exit(1)
            
        seen_field_names.add(field_name)
        
        # 2. Type Checking (Even though the parser caught most of this, 
        # it is academically correct to enforce it here too)
        if field_type not in ["int", "string"]:
            print(f"Semantic Error: Unknown data type '{field_type}' for field '{field_name}'.")
            sys.exit(1)
            
        # 3. String Size Validation
        if field_type == "string":
            # The length must exist and be greater than 0
            if "length" not in field or field["length"] <= 0:
                print(f"Semantic Error: String array '{field_name}' must have a positive size greater than 0.")
                sys.exit(1)

    print("Semantic Analysis Passed: Logic is 100% CORRECT!\n")
    return ast

#Test
if __name__ == "__main__":
    from lexer import tokenize
    from parser import parse
    
    # Let's read the file, lex it, parse it, and then analyze it!
    with open("examples/player.pack", "r") as f:
        code = f.read()
        
    tokens = tokenize(code)
    ast = parse(tokens)
    
    # Run our new Semantic Analyzer
    validated_ast = analyze(ast)