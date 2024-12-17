import re

# Token definition
TOKEN_SPECS = [
    ('KEYWORD', r'\b(createCursor|move|rotate|drawLine|drawCircle|drawRectangle|drawArc|setColor|setThickness|if|else|for|while)\b'),  # keywords
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),        # Identifiers
    ('NUMBER', r'\b\d+(\.\d+)?\b'),         # Numbers
    ('HEX_COLOR', r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})'),  # Hex colors
    ('OPERATOR', r'==|!=|<=|>=|<|>'),       # Operators
     ('ARITHMETIC_OP', r'[+ - * /]'),          # Opérateurs arithmétiques : +, -, *, /
    ('ASSIGN', r'='),  
    ('DELIMITER', r'[(),{};]'),             # Delimiters
    ('SKIP', r'[ \t]+'),                    # Whitespace (ignored)
    ('NEWLINE', r'\n'),                     # Newline characters
    ('MISMATCH', r'.'),                     # Catch-all for unrecognized tokens
]

class Token:
    def __init__(self, value, token_type, line, column):
        self.value = value
        self.type = token_type
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}({self.value})"

def tokenize(code):
    """
    Tokenizes the provided code string into a list of Token objects.
    """
    tokens = []
    line_number = 1
    line_start = 0
    for match in re.finditer('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECS), code):
        type_ = match.lastgroup
        value = match.group()
        column = match.start() - line_start
        if type_ == 'NEWLINE':
            line_number += 1
            line_start = match.end()
        elif type_ == 'SKIP':
            continue
        elif type_ == 'MISMATCH':
            raise SyntaxError(f"Unexpected token: {value} at line {line_number}, column {column}")
        else:
            tokens.append(Token(value, type_, line_number, column))
    return tokens
