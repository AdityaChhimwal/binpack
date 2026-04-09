#keywords SUported
KEYWORDS = {"struct", "int", "string"}

def tokenize(code):
    # We will store tokens as simple tuples: (type, value, line, column)
    tokens = []
    i = 0
    line = 1
    column = 1

    while i < len(code):
        char = code[i]

        # 1. Handle newlines for accurate row/col tracking
        if char == '\n':
            line += 1
            column = 1
            i += 1
            continue

        # 2. Ignore other whitespace (spaces, tabs)
        if char.isspace():
            column += 1
            i += 1
            continue

        # 3. Identifiers (starts with a letter)
        if char.isalpha():
            start = i
            start_col = column
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                i += 1
                column += 1
            word = code[start:i]

            if word in KEYWORDS:
                tokens.append(("KEYWORD", word, line, start_col))
            else:
                tokens.append(("IDENTIFIER", word, line, start_col))
            continue

        # 4. Numbers
        if char.isdigit():
            start = i
            start_col = column
            while i < len(code) and code[i].isdigit():
                i += 1
                column += 1
            tokens.append(("NUMBER", code[start:i], line, start_col))
            continue

        # 5. Symbols
        if char in "{}()[];":
            tokens.append(("SYMBOL", char, line, column))
            i += 1
            column += 1
            continue

        # 6. Catching errors with exact line/col location
        print(f"Lexical Error on Line {line}, Column {column}: Unexpected character '{char}'")
        import sys
        sys.exit(1)

    return tokens

#Quick Test
if __name__ == "__main__":
    with open("examples/player.pack") as f:
        code = f.read()

    tokens = tokenize(code)

    # Print out each token tuple
    for t in tokens:
        print(t)