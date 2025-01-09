#Parcourt l'AST pour collecter toutes les entités déclarées pour curseurs et varaibles
def collect_declared_entities(ast):
  
    declared_entities = {"cursor": set(), "variables": {}}  
    for node in ast.children:
        if node.node_type == "createCursor":
            identifiant_node = next((child for child in node.children if child.node_type == "identifiant"), None)
            if not identifiant_node:
                raise SyntaxError("Missing identifier in createCursor.")
            identifiant = identifiant_node.value
            declared_entities["cursor"].add(identifiant)
            print(f"Declared cursor: {identifiant}")

        elif node.node_type == "assignment":
            identifiant = node.value  
            declared_entities["variables"][identifiant] = None 

    return declared_entities

#  Évalue une expression arithmétique ou de comparaison
def evaluate_expression(node, declared_variables):
    
    if node.node_type == "number":
        return node.value

    elif node.node_type == "variable":
        if node.value not in declared_variables or declared_variables[node.value] is None:
            raise SyntaxError(f"Variable '{node.value}' used before initialization.")
        return declared_variables[node.value]
 # Gestion de l'incrémentation
    elif node.node_type == "increment":  
        variable_name = node.value

        if variable_name not in declared_variables or declared_variables[variable_name] is None:
            raise SyntaxError(f"Variable '{variable_name}' used before initialization.")

        if node.children[0].node_type == "postfix":
            # Post-fixé (i++): retourne l'ancienne valeur, puis incrémente
            old_value = declared_variables[variable_name]
            declared_variables[variable_name] += 1
            return old_value
        elif node.children[0].node_type == "prefix":
            # Pré-fixé (++i): incrémente, puis retourne la nouvelle valeur
            declared_variables[variable_name] += 1
            return declared_variables[variable_name]
    elif node.node_type == "operation":
        left = evaluate_expression(node.children[0], declared_variables)
        right = evaluate_expression(node.children[1], declared_variables)

        if node.value == "+":
            return left + right
        elif node.value == "-":
            return left - right
        elif node.value == "*":
            return left * right
        elif node.value == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero.")
            return left / right
# Gestion des comparateurs
    elif node.node_type == "comparison":  
        left = evaluate_expression(node.children[0], declared_variables)
        right = evaluate_expression(node.children[1], declared_variables)

        if node.value == "==":
            return left == right
        elif node.value == "!=":
            return left != right
        elif node.value == "<":
            return left < right
        elif node.value == ">":
            return left > right
        elif node.value == "<=":
            return left <= right
        elif node.value == ">=":
            return left >= right

    else:
        raise SyntaxError(f"Unknown expression node: {node.node_type}")

#Valide les propriétés assignées aux curseurs (couleur, épaisseur).
def validate_cursor_properties(ast):
    
    for node in ast.children:
        if node.node_type == "setColor":
            identifiant = next(child for child in node.children if child.node_type == "identifiant").value
            color = next(child for child in node.children if child.node_type == "color").value
            
            # Pas de validation du format ici, car HEX_COLOR est déjà validé par notre tokenizer
            print(f"Cursor '{identifiant}' assigned color '{color}'.")

        elif node.node_type == "setThickness":
            identifiant = next(child for child in node.children if child.node_type == "identifiant").value
            thickness = next(child for child in node.children if child.node_type == "thickness").value
            
            # Validation de l'épaisseur
            if thickness <= 0:
                raise SyntaxError(f"Thickness '{thickness}' for cursor '{identifiant}' must be positive.")
            print(f"Cursor '{identifiant}' assigned thickness '{thickness}'.")
#vérifie que toutes les coordonnées des curseurs (x, y) sont comprises entre 0 et 100.
def validate_cursor_coordinates(ast):
    
    for node in ast.children:
        if node.node_type == "createCursor":
            # Récupérer les coordonnées
            coordinates = next((child for child in node.children if child.node_type == "coordinates"), None)
            if not coordinates:
                raise SyntaxError("Missing coordinates in createCursor.")
            x = next((child for child in coordinates.children if child.node_type == "x"), None)
            y = next((child for child in coordinates.children if child.node_type == "y"), None)
            if x is None or y is None:
                raise SyntaxError("Both x and y coordinates must be specified in createCursor.")
            if not (0 <= x.value <= 100):
                raise SyntaxError(f"Invalid x-coordinate {x.value} in createCursor. Must be between 0 and 9.")
            if not (0 <= y.value <= 100):
                raise SyntaxError(f"Invalid y-coordinate {y.value} in createCursor. Must be between 0 and 9.")
            print(f"Cursor coordinates validated: x={x.value}, y={y.value}.")

#Valide que toutes les entités (variables, curseurs) sont correctement initialisées et gère les affectations.
def validate_entity_initialization(ast, declared_entities):
    
    for node in ast.children:
        if node.node_type == "assignment":
            variable = node.value 
            expression = node.children[0]  
            declared_entities["variables"][variable] = evaluate_expression(expression, declared_entities["variables"])
            print(f"Variable '{variable}' assigned value: {declared_entities['variables'][variable]}")

#Applique nos validations nécessaires semantique 
def validate_program(ast):
    
    declared_entities = collect_declared_entities(ast)

    validate_cursor_coordinates(ast)

    validate_entity_initialization(ast, declared_entities)
    
    validate_cursor_properties(ast)

    
