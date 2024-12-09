from tokenizer import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        #"\"\"Retourne le token courant ou 'EOF' si fin atteinte.\"\"\"
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', 'EOF', -1, -1)  # Token spécial pour la fin

    def consume(self, expected_type):
        #\"\"\"
       # Consomme le token actuel s'il correspond au type attendu,
        #sinon lève une erreur de syntaxe.
        
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(
                f"Expected token type '{expected_type}' but got '{token.type}' at line {token.line}, column {token.column}."
            )

    def parse_program(self):
        
        #Analyse un programme : <program> ::= <instruction> ";" | <instruction> ";" <program>
        
        print("Parsing <program>...")
        instructions = []
        while self.current_token().type != 'EOF':
            instruction = self.parse_instruction()
            self.consume('DELIMITER')  # Consume ';'
            instructions.append(instruction)
        return {"type": "program", "instructions": instructions}

    def parse_instruction(self):
        
        #Analyse une instruction : 
       # <instruction> ::= <cursor_instruction> | <drawing_instruction> | <color_instruction> | <thickness_instruction> | <control_instruction>
       
        print("Parsing <instruction>...")
        token = self.current_token()
        if token.value in {"createCursor", "move", "rotate"}:
            return self.parse_cursor_instruction()
        elif token.value in {"drawLine", "drawCircle", "drawRectangle", "drawArc"}:
            return self.parse_drawing_instruction()
        elif token.value == "setColor":
            return self.parse_color_instruction()
        elif token.value == "setThickness":
            return self.parse_thickness_instruction()
        elif token.value in {"if", "for", "while"}:
            return self.parse_control_instruction()
        else:
            raise SyntaxError(f"Unexpected instruction '{token.value}' at line {token.line}, column {token.column}.")

    def parse_cursor_instruction(self):
        
       ## Analyse une instruction de curseur : 
        ##<cursor_instruction> ::= "createCursor" "(" <identifiant> "," <coordonnees> ")"
                                #| "move" "(" <identifiant> "," <nombre_pixels> ")"
                                #| "rotate" "(" <identifiant> "," <degres> ")"
        
        print("Parsing <cursor_instruction>...")
        token = self.consume('KEYWORD')
        if token.value == "createCursor":
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            self.consume('DELIMITER')  # Consume ','
            coordinates = self.parse_coordinates()
            self.consume('DELIMITER')  # Consume ')'
            return {"type": "createCursor", "identifiant": identifiant, "coordinates": coordinates}
        elif token.value in {"move", "rotate"}:
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            self.consume('DELIMITER')  # Consume ','
            value = self.consume('NUMBER').value
            self.consume('DELIMITER')  # Consume ')'
            return {"type": token.value, "identifiant": identifiant, "value": int(value)}
        else:
            raise SyntaxError(f"Invalid cursor instruction '{token.value}'.")

    def parse_coordinates(self):
        coord_token = self.current_token()
        if coord_token.type == 'NUMBER':
            x_value = int(self.consume('NUMBER').value)
            self.consume('DELIMITER')  # Consume ','
            y_value = int(self.consume('NUMBER').value)
            return {'x': x_value, 'y': y_value}
        else:
            raise SyntaxError(f"Expected coordinates but got '{coord_token.value}'")
