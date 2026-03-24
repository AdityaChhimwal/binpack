
def parse(tokens):
    current = 0  # Keeps track of where we are in the token list

    # Helper function to look at the current token without moving forward
    def peek():
        if current < len(tokens):
            return tokens[current]
        return None

    # Helper function to grab the current token and move to the next one
    def advance():
        nonlocal current
        token = peek()
        current += 1
        return token

    # The magic function: Checks if the next token matches what we expect
    def expect(expected_type, expected_value=None):
        token = advance()
        if not token:
            print("Syntax Error: Unexpected end of file. Did you forget a '}'?")
            import sys
            sys.exit(1)
            
        t_type, t_value, line, col = token
        
        # If the type or value doesn't match, crash and report exactly where!
        if t_type != expected_type or (expected_value and t_value != expected_value):
            expected_msg = expected_value if expected_value else expected_type
            print(f"Syntax Error on Line {line}, Column {col}: Expected '{expected_msg}', but got '{t_value}'")
            import sys
            sys.exit(1)
            
        return token

    
    # 1. We expect the file to start with 'struct'
    expect("KEYWORD", "struct")
    
    # 2. Next should be the name of the struct (an identifier)
    _, struct_name, _, _ = expect("IDENTIFIER")
    
    # 3. Next should be '{'
    expect("SYMBOL", "{")
    
    fields = []
    
    # 4. Loop to parse all the fields inside the struct until we see '}'
    while peek() and not (peek()[0] == "SYMBOL" and peek()[1] == "}"):
        
        # Get the field type (should be 'int' or 'string')
        type_token = advance()
        t_type, t_value, line, col = type_token
        
        if t_type != "KEYWORD":
            print(f"Syntax Error on Line {line}, Column {col}: Expected type 'int' or 'string', got '{t_value}'")
            import sys
            sys.exit(1)
            
        field_info = {"type": t_value}
        
        # If it's a string, we expect an array size like [20]
        if t_value == "string":
            expect("SYMBOL", "[")
            _, size_val, _, _ = expect("NUMBER")
            field_info["length"] = int(size_val)
            expect("SYMBOL", "]")
            
        # Get the actual name of the variable (e.g., 'health')
        _, field_name, _, _ = expect("IDENTIFIER")
        field_info["name"] = field_name
        
        # Every line must end with a semicolon ';'
        expect("SYMBOL", ";")
        
        # Add this field to our list
        fields.append(field_info)
        
    # 5. Finally, we expect the closing bracket '}'
    expect("SYMBOL", "}")
    
    # Return our neat and organized Symbol Table!
    return {
        "name": struct_name,
        "fields": fields
    }

# --- Quick Test ---
if __name__ == "__main__":
    # Import the lexer we just built!
    from lexer import tokenize
    
    with open("examples/player.pack", "r") as f:
        code = f.read()
        
    tokens = tokenize(code)
    symbol_table = parse(tokens)
    
    # Print the result nicely
    import json
    print("--- Symbol Table (AST) ---")
    print(json.dumps(symbol_table, indent=4))