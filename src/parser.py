from tokenizer import Token

# Classe représentant un nœud dans l'AST
class ASTNode:
    def __init__(self, node_type, value=None):
        """
        Initialise un nœud d'AST.
        :param node_type: Type du nœud (par exemple, "createCursor", "move", etc.).
        :param value: Valeur du nœud, si applicable (par exemple, un identifiant ou un nombre).
        """
        self.node_type = node_type
        self.value = value
        self.children = []  # Sous-nœuds de l'AST

    def add_child(self, child):
        """Ajoute un sous-nœud à ce nœud."""
        self.children.append(child)

    def __repr__(self):
        """Représentation en texte pour déboguer."""
        return f"ASTNode(type={self.node_type}, value={self.value}, children={self.children})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        # Dictionnaire pour les entités initialisées
        self.declared_entities = {
            "cursor": set()  # Par exemple, les curseurs
        }

    def current_token(self):
        """Retourne le token courant ou 'EOF' si fin atteinte."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', 'EOF', -1, -1)  # Token spécial pour la fin

    def peek(self):
        """Retourne le prochain token sans le consommer."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return Token('EOF', 'EOF', -1, -1)

    def consume(self, expected_type):
        """
        Consomme le token actuel s'il correspond au type attendu,
        sinon lève une erreur de syntaxe.
        """
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(
                f"Expected token type '{expected_type}' but got '{token.type}' "
                f"at line {token.line}, column {token.column}."
            )

    def check_entity_declaration(self, entity_type, entity_name, usage_context):
        """
        Vérifie si une entité a été déclarée.
        :param entity_type: Type de l'entité (par exemple, "cursor").
        :param entity_name: Nom de l'entité (par exemple, "cursor1").
        :param usage_context: Contexte où l'entité est utilisée (par exemple, "move").
        """
        if entity_name not in self.declared_entities.get(entity_type, set()):
            raise SyntaxError(
                f"{entity_type.capitalize()} '{entity_name}' used in '{usage_context}' "
                "has not been initialized."
            )

    def parse_program(self):
        """Analyse un programme complet et retourne un AST."""
        print("Parsing <program>...")
        program_node = ASTNode("program")
        while self.current_token().type != 'EOF':
            instruction_node = self.parse_instruction()
            self.consume('DELIMITER')  # Consume ';'
            program_node.add_child(instruction_node)
        return program_node

    def parse_instruction(self):
        """Analyse une instruction et crée un nœud dans l'AST."""
        print("Parsing <instruction>...")
        token = self.current_token()

        # Vérifie si c'est une instruction d'affectation (ex: a = 7)
        if token.type == 'IDENTIFIER' and self.peek().type == 'ASSIGN':
            return self.parse_assignment()
        # Ajout de l'instruction conditionnelle "if"
        elif token.value == "if":
            return self.parse_condition_instruction()


        # Autres instructions existantes
        elif token.value in {"createCursor", "move", "rotate"}:
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
        """Analyse une instruction de curseur et crée un nœud AST."""
        print("Parsing <cursor_instruction>...")
        token = self.consume('KEYWORD')
        node = ASTNode(token.value)  # Crée un nœud pour l'instruction

        if token.value == "createCursor":
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            node.add_child(ASTNode("identifiant", identifiant))  # Ajoute l'identifiant comme sous-nœud
            self.consume('DELIMITER')  # Consume ',' 
            coordinates = self.parse_coordinates()
            node.add_child(coordinates)  # Ajoute les coordonnées comme sous-nœud
            self.consume('DELIMITER')  # Consume ')'
            self.declared_entities["cursor"].add(identifiant)  # Enregistre le curseur déclaré
        elif token.value in {"move", "rotate"}:
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", identifiant, token.value)
            node.add_child(ASTNode("identifiant", identifiant))  # Ajoute l'identifiant comme sous-nœud
            self.consume('DELIMITER')  # Consume ',' 
            value = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("value", value))  # Ajoute la valeur comme sous-nœud
            self.consume('DELIMITER')  # Consume ')'
        else:
            raise SyntaxError(f"Invalid cursor instruction '{token.value}'.")
        
        return node

    def parse_coordinates(self):
        """Analyse les coordonnées et crée un nœud AST."""
        print("Parsing <coordinates>...")
        coord_node = ASTNode("coordinates")
        x_value = int(self.consume('NUMBER').value)
        coord_node.add_child(ASTNode("x", x_value))
        self.consume('DELIMITER')  # Consume ',' 
        y_value = int(self.consume('NUMBER').value)
        coord_node.add_child(ASTNode("y", y_value))
        return coord_node

    def parse_condition_instruction(self):
        """Analyse une instruction conditionnelle 'if'."""
        print("Parsing <if_instruction>...")
        self.consume('KEYWORD')  # Consomme 'if'
        self.consume('DELIMITER')  # Consomme '('
        condition_node = self.parse_expression()  # Analyse l'expression conditionnelle
        self.consume('DELIMITER')  # Consomme ')'
        self.consume('DELIMITER')  # Consomme '{'
        program_node = self.parse_program()  # Analyse le programme dans le bloc 'if'
        self.consume('DELIMITER')  # Consomme '}'

        # Vérification de la présence d'un bloc 'else' optionnel
        else_node = None
        if self.current_token().value == "else":
            self.consume('KEYWORD')  # Consomme 'else'
            self.consume('DELIMITER')  # Consomme '{'
            else_program_node = self.parse_program()  # Programme dans le bloc 'else'
            self.consume('DELIMITER')  # Consomme '}'
            else_node = ASTNode("else", None)
            else_node.add_child(else_program_node)

        # Créer le nœud conditionnel
        if else_node:
            node = ASTNode("if", None)
            node.add_child(condition_node)
            node.add_child(program_node)
            node.add_child(else_node)
        else:
            node = ASTNode("if", None)
            node.add_child(condition_node)
            node.add_child(program_node)

        return node

    def parse_assignment(self):
        """Analyse une instruction d'affectation de variable."""
        identifiant = self.consume('IDENTIFIER').value
        self.consume('ASSIGN')  # Consomme '='
        assignment_node = ASTNode("assignment", identifiant)

        # Analyse l'expression affectée
        expression_node = self.parse_expression()
        assignment_node.add_child(expression_node)
        return assignment_node

    

    def parse_expression(self):
        """
        Analyse une expression arithmétique avec gestion des priorités et des parenthèses.
        """
        left = self.parse_term()  # Analyse un premier terme

        while self.current_token().type == 'ARITHMETIC_OP' and self.current_token().value in {"+", "-"}:
            operator = self.consume('ARITHMETIC_OP').value  # Consomme '+' ou '-'
            right = self.parse_term()
            operation_node = ASTNode("operation", operator)
            operation_node.add_child(left)
            operation_node.add_child(right)
            left = operation_node

        return left

    def parse_term(self):
        """
        Analyse un terme, qui peut inclure des multiplications/divisions ou des parenthèses.
        """
        left = self.parse_factor()  # Analyse un facteur

        while self.current_token().type == 'ARITHMETIC_OP' and self.current_token().value in {"*", "/"}:
            operator = self.consume('ARITHMETIC_OP').value  # Consomme '*' ou '/'
            right = self.parse_factor()
            operation_node = ASTNode("operation", operator)
            operation_node.add_child(left)
            operation_node.add_child(right)
            left = operation_node

        return left

    def parse_factor(self):
        """
        Analyse un facteur, qui peut être un nombre, une variable ou une expression entre parenthèses.
        """
        token = self.current_token()

        if token.type == 'NUMBER':  # Si c'est un nombre
            value = int(self.consume('NUMBER').value)
            return ASTNode("number", value)

        elif token.type == 'IDENTIFIER':  # Si c'est une variable
            value = self.consume('IDENTIFIER').value
            return ASTNode("variable", value)

        elif token.type == 'DELIMITER' and token.value == "(":  # Si c'est une parenthèse ouvrante
            self.consume('DELIMITER')  # Consomme '('
            expression = self.parse_expression()  # Analyse récursive
            if self.current_token().type == 'DELIMITER' and self.current_token().value == ")":
                self.consume('DELIMITER')  # Consomme ')'
                return expression
            else:
                raise SyntaxError("Missing closing parenthesis.")

        else:
            raise SyntaxError(f"Unexpected token in factor: {token.value}")
            
            
           