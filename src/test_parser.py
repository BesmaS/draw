try:
    from tokenizer import tokenize
except ImportError as e:
    print(f"Error importing tokenizer: {e}")
    exit()

try:
    from parser import Parser
except ImportError as e:
    print(f"Error importing parser: {e}")
    exit()

# Exemple de code à analyserry:
    from tokenizer import tokenize
except ImportError as e:
    print(f"Error importing tokenizer: {e}")
    exit()
code = """
createCursor (cursor1,x100,y200);
move(cursor1, 50);
rotate(cursor1, 90);
"""

print("Tokenizing code...\n")
try:
    # Tokenisation
    tokens = tokenize(code)
    print("Tokens generated:")
    for token in tokens:
        print(token)
except SyntaxError as e:
    print(f"Lexer error: {e}")
    exit()

print("\nParsing tokens...\n")
try:
    # Parsing
    parser = Parser(tokens)
    result = parser.parse_program()
    print("Parsing result:")
    print(result)
except SyntaxError as e:
    print(f"Parser error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
