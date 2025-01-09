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
    def to_dict(self):
        
 #Convertit un ASTNode en un dictionnaire récursif compatible avec JSON.
        
        return {
            "type": self.node_type,
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

#Ajoute un sous-noeud 
    def add_child(self, child):
        
        self.children.append(child)
#repr pour debug
    def __repr__(self):
        
        return f"ASTNode(type={self.node_type}, value={self.value}, children={self.children})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        # Dictionnaire pour les entités initialisées
        self.declared_entities = {
            "cursor": set()  # Par exemple, les curseurs
        }
#Retourne le token courant ou 'EOF' si fin atteinte.
    def current_token(self):
    
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', 'EOF', -1, -1)  # Token spécial pour la fin
#Retourne le prochain token sans le consommer.
    def peek(self):
      
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return Token('EOF', 'EOF', -1, -1)
#Conssomme le token actuel s'il correspond au type attendu sinon lève une erreur de syntaxe
    def consume(self, expected_type):
        
        
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(
                f"Expected token type '{expected_type}' but got '{token.type}' "
                f"at line {token.line}, column {token.column}."
            )
#Vérification entité
    def check_entity_declaration(self, entity_type, entity_name, usage_context):
        
        if entity_name not in self.declared_entities.get(entity_type, set()):
            raise SyntaxError(
                f"{entity_type.capitalize()} '{entity_name}' used in '{usage_context}' "
                "has not been initialized."
            )
#Analyse du programme complet + retourne AST
    def parse_program(self):
        
        print("Parsing <program>...")
        program_node = ASTNode("program")
        while self.current_token().type != 'EOF' and not (
                self.current_token().type == 'DELIMITER' and self.current_token().value == '}'):
            instruction_node = self.parse_instruction()
            self.consume('DELIMITER')  # Consomme ';' (s'il y en a)
            program_node.add_child(instruction_node)
        return program_node


#Analyse instruction du programme et délègue son traitement au module de parsing approprié

    def parse_instruction(self):
        
        print("Parsing <instruction>...")
        token = self.current_token()

        # Vérifie si c'est une instruction d'affectation (ex: a = 7) 
        if token.type == 'IDENTIFIER' and self.peek().type == 'ASSIGN':
            return self.parse_assignment()
        # Ajout de l'instruction conditionnelle "if" 
        elif token.value == "if":
            return self.parse_condition_instruction()

        # Autres instructions existantes
        elif token.value in {"createCursor", "move", "rotate", "setColor", "setThickness"}:
            return self.parse_cursor_instruction()
        elif token.value in {"drawLine", "drawCircle", "drawSquare", "drawRectangle", "drawArc"}:
            return self.parse_drawing_instruction()
        elif token.value == "while":
            return self.parse_while_loop()
        elif token.value == "for":
            return self.parse_for_loop()
        elif token.value == "do":
            return self.parse_do_while_loop()

        
        else:
            raise SyntaxError(f"Unexpected instruction '{token.value}' at line {token.line}, column {token.column}.")
#analyse des instruction de curseur
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
        elif token.value == "setColor":
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", identifiant, token.value)
            node.add_child(ASTNode("identifiant", identifiant))  # Ajoute l'identifiant comme sous-nœud
            self.consume('DELIMITER')  # Consume ','

            # Consomme une couleur en hexadécimal
            color = self.consume('HEX_COLOR').value
            node.add_child(ASTNode("color", color))  # Ajoute la couleur comme sous-nœud

            self.consume('DELIMITER')  # Consume ')'
        elif token.value == "setThickness":
            self.consume('DELIMITER')  # Consume '('
            identifiant = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", identifiant, token.value)
            node.add_child(ASTNode("identifiant", identifiant))  # Ajoute l'identifiant comme sous-nœud
            self.consume('DELIMITER')  # Consume ','
            thickness = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("thickness", thickness))  # Ajoute l'épaisseur comme sous-nœud
            self.consume('DELIMITER')  # Consume ')'

        else:
            raise SyntaxError(f"Invalid cursor instruction '{token.value}'.")
        return node
#Analyse instruction de dessin
    def parse_drawing_instruction(self):
        
        print("Parsing <drawing_instruction>...")
        token = self.consume('KEYWORD')
        node = ASTNode(token.value)  # Crée un nœud pour l'instruction de dessin

        if token.value == "drawCircle":
            self.consume('DELIMITER')  # Consomme '('
            cursor_id = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", cursor_id, token.value)
            node.add_child(ASTNode("cursor", cursor_id))  # Ajoute le curseur comme sous-nœud
            self.consume('DELIMITER')  # Consomme ','

            # Rayon du cercle
            radius = int(self.consume('NUMBER').value)  
            node.add_child(ASTNode("radius", radius))  

            self.consume('DELIMITER')  # Consomme ','

            coordinates = self.parse_coordinates()
            node.add_child(coordinates)  # Ajoute les coordonnées comme sous-nœud
            self.consume('DELIMITER')  # Consume ')'

        elif token.value == "drawLine":
            self.consume('DELIMITER')  # Consomme '('
            cursor_id = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", cursor_id, token.value)
            node.add_child(ASTNode("cursor", cursor_id))  # Ajoute le curseur comme sous-nœud
            self.consume('DELIMITER')  # Consomme ','

            # Première coordonnée (x1, y1)
            coordinates = self.parse_coordinates()
            node.add_child(coordinates) 
            self.consume('DELIMITER')  # Consomme ','

            # Deuxième coordonnée (x2, y2)
            coordinates = self.parse_coordinates()
            node.add_child(coordinates)  
            self.consume('DELIMITER')  # Consomme ')'

        elif token.value == "drawSquare":
            self.consume('DELIMITER')  # Consomme '('
            cursor_id = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", cursor_id, token.value)
            node.add_child(ASTNode("cursor", cursor_id))  # Ajoute le curseur comme sous-nœud
            self.consume('DELIMITER')  # Consomme ','

            # Taille du côté
            side_length = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("side_length", side_length)) 

            self.consume('DELIMITER')  # Consomme ','

            # Coordonnées
            coordinates = self.parse_coordinates()
            node.add_child(coordinates)  
            self.consume('DELIMITER')  # Consomme ')'
    
        elif token.value == "drawArc":
            self.consume('DELIMITER')  # Consomme '('
            cursor_id = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", cursor_id, token.value)
            node.add_child(ASTNode("cursor", cursor_id))  # Ajoute le curseur comme sous-nœud
            self.consume('DELIMITER')  # Consomme ','

            # Rayon
            radius = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("radius", radius))  

            self.consume('DELIMITER')  # Consomme ','

            # Angle de départ
            start_angle = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("start_angle", start_angle))  

            self.consume('DELIMITER')  # Consomme ','

            # Angle de fin
            end_angle = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("end_angle", end_angle))  
            self.consume('DELIMITER')  # Consomme ','
            
            # Centre de l'arc
             # Coordonnées
            coordinates = self.parse_coordinates()
            node.add_child(coordinates) 
            self.consume('DELIMITER')  # Consomme ')'
             
             
        elif token.value == "drawRectangle":
            self.consume('DELIMITER')  # Consomme '('
            cursor_id = self.consume('IDENTIFIER').value
            self.check_entity_declaration("cursor", cursor_id, token.value)
            node.add_child(ASTNode("cursor", cursor_id))  # Ajoute le curseur comme sous-nœud
            self.consume('DELIMITER')  # Consomme ','

            # Largeur
            width = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("width", width))  

            self.consume('DELIMITER')  # Consomme ','

            # Hauteur
            height = int(self.consume('NUMBER').value)
            node.add_child(ASTNode("height", height))  

            self.consume('DELIMITER')  # Consomme ','

            # Coordonnées
            coordinates = self.parse_coordinates()
            node.add_child(coordinates)  # Ajoute les coordonnées comme sous-nœud
            self.consume('DELIMITER')  # Consomme ')'
            
               

        else:
            raise SyntaxError(f"Invalid drawing instruction '{token.value}'.")

        return node

#Analyse les coordonnées 
    def parse_coordinates(self):
       
        print("Parsing <coordinates>...")
        coord_node = ASTNode("coordinates")
        x_value = int(self.consume('NUMBER').value)
        coord_node.add_child(ASTNode("x", x_value))
        self.consume('DELIMITER')  # Consume ','
        y_value = int(self.consume('NUMBER').value)
        coord_node.add_child(ASTNode("y", y_value))
        return coord_node
        #Analyse une boucle while
    def parse_while_loop(self):
        
        print("Parsing <while_loop>...")
        self.consume('KEYWORD')  # Consomme 'while'
        self.consume('DELIMITER')  # Consomme '('
        condition_node = self.parse_expression()  # Analyse l'expression conditionnelle
        self.consume('DELIMITER')  # Consomme ')'
        self.consume('DELIMITER')  # Consomme '{'
        program_node = self.parse_program()  # Analyse le programme dans le bloc de la boucle
        self.consume('DELIMITER')  # Consomme '}'

        # Créer le nœud pour la boucle while
        loop_node = ASTNode("while", None)
        loop_node.add_child(condition_node)
        loop_node.add_child(program_node)

        return loop_node
#Analyse une boucle for (faut qur je revienne dessus pb incrementation bouhhh
    def parse_for_loop(self):
      
        print("Parsing <for_loop>...")
        self.consume('KEYWORD')  # Consomme 'for'
        self.consume('DELIMITER')  # Consomme '('
        
        # Partie initialisation (expression d'affectation)
        init_node = self.parse_assignment()

        self.consume('DELIMITER')  # Consomme ';'
        
        # Condition de la boucle
        condition_node = self.parse_expression()

        self.consume('DELIMITER')  # Consomme ';'
        
        # Partie incrémentation (expression) c'est ici je penses
        increment_node = self.parse_expression()

        self.consume('DELIMITER')  # Consomme ')'
        self.consume('DELIMITER')  # Consomme '{'
        
        # Bloc des instructions de la boucle
        program_node = self.parse_program()
        self.consume('DELIMITER')  # Consomme '}'

        # Créer le nœud pour la boucle for
        loop_node = ASTNode("for", None)
        loop_node.add_child(init_node)
        loop_node.add_child(condition_node)
        loop_node.add_child(increment_node)
        loop_node.add_child(program_node)

        return loop_node
#Analyse une boucle do while
    def parse_do_while_loop(self):
     
        print("Parsing <do_while_loop>...")
        self.consume('KEYWORD')  # Consomme 'do'
        self.consume('DELIMITER')  # Consomme '{'
        
        # Bloc des instructions de la boucle
        program_node = self.parse_program()
        self.consume('DELIMITER')  # Consomme '}'
        
        self.consume('KEYWORD')  # Consomme 'while'
        self.consume('DELIMITER')  # Consomme '('
        
        # Condition de la boucle
        condition_node = self.parse_expression()
        
        self.consume('DELIMITER')  # Consomme ')'
        
        # Créer le nœud pour la boucle do while
        loop_node = ASTNode("do_while", None)
        loop_node.add_child(program_node)
        loop_node.add_child(condition_node)

        return loop_node
    #Analyse instruction conditionelle
    def parse_condition_instruction(self):
        
        print("Parsing <if_instruction>...")
        self.consume('KEYWORD')  # Consomme 'if'
        self.consume('DELIMITER')  
        condition_node = self.parse_expression()  # Analyse l'expression conditionnelle
        self.consume('DELIMITER')  
        self.consume('DELIMITER')  
        program_node = self.parse_program()  # Analyse le programme dans le bloc 'if'

        
        self.consume('DELIMITER') 

        # Vérification de la présence d'un bloc 'else' optionnel
        else_node = None
        if self.current_token().value == "else":
            self.consume('KEYWORD')  # Consomme 'else'
            self.consume('DELIMITER')  
            else_program_node = self.parse_program()  # Programme dans le bloc 'else'
            self.consume('DELIMITER')  
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
#Analyse affectation de variable
    def parse_assignment(self):
      
        identifiant = self.consume('IDENTIFIER').value
        self.consume('ASSIGN')  # Consomme '='
        assignment_node = ASTNode("assignment", identifiant)

        # Analyse l'expression affectée
        expression_node = self.parse_expression()
        assignment_node.add_child(expression_node)
        return assignment_node
#Analyse une expression qui peut inclure des comparateurs et des opérateurs arithmétiques
    def parse_expression(self):
        
        # Analyse un premier terme
        left = self.parse_term()

        # Gestion des comparateurs (==, !=, <, >, <=, >=)
        # Vérifie si c'est un opérateur de comparaison
        while self.current_token().type == 'OPERATOR':
        # Consomme l'opérateur      
            operator = self.consume('OPERATOR').value 
         # Analyse le terme à droite 
            right = self.parse_term() 
            comparison_node = ASTNode("comparison", operator)
            comparison_node.add_child(left)
            comparison_node.add_child(right)
           # Le résultat devient le nouveau "left"

            left = comparison_node  
        # Gestion des opérateurs arithmétiques (+, -)
        while self.current_token().type == 'ARITHMETIC_OP' and self.current_token().value in {"+", "-"}:
            operator = self.consume('ARITHMETIC_OP').value  # Consomme '+' ou '-'
            right = self.parse_term()
            operation_node = ASTNode("operation", operator)
            operation_node.add_child(left)
            operation_node.add_child(right)
            left = operation_node  
        return left
#Analyse un terme, qui peut inclure des multiplications/divisions ou des parenthèses.
    def parse_term(self):
# Analyse un facteur
        left = self.parse_factor()  

        while self.current_token().type == 'ARITHMETIC_OP' and self.current_token().value in {"*", "/"}:
            # Consomme '*' ou '/'
            operator = self.consume('ARITHMETIC_OP').value 
            right = self.parse_factor()
            operation_node = ASTNode("operation", operator)
            operation_node.add_child(left)
            operation_node.add_child(right)
            left = operation_node

        return left
#Analyse un facteur, qui peut être un nombre, une variable ou une expression entre parenthèses.

    def parse_factor(self):
        
        token = self.current_token()
# Si c'est un nombre
        if token.type == 'NUMBER':  
            value = int(self.consume('NUMBER').value)
            return ASTNode("number", value)

        elif token.type == 'IDENTIFIER':  # Si c'est une variable
            value = self.consume('IDENTIFIER').value
            return ASTNode("variable", value)
        # Si c'est une parenthèse ouvrante
        elif token.type == 'DELIMITER' and token.value == "(":  
            self.consume('DELIMITER')  
            # Analyse récursive
            expression = self.parse_expression()  
            if self.current_token().type == 'DELIMITER' and self.current_token().value == ")":
                self.consume('DELIMITER')  
                return expression
            else:
                raise SyntaxError("Missing closing parenthesis.")

        else:
            raise SyntaxError(f"Unexpected token in factor: {token.value}")