import subprocess
import os
import time
# Étape 1 : Programme C stocké dans une liste
c_header = [
    "#include <SDL2/SDL.h>",
    "#include <stdio.h>",
    "#include <stdlib.h>",
    "#include <string.h>",
    "#include <math.h>",
    "",
    "typedef enum {",
    "    SHAPE_LINE,",
    "    SHAPE_RECTANGLE,",
    "    SHAPE_OVAL,",
    "    SHAPE_POINT,",
    "    SHAPE_CIRCLE,",
    "    SHAPE_ARC,",
    "    SHAPE_UNKNOWN",
    "} ShapeType;",
    "",
    "typedef struct {",
    "int r;",
    "int g;",
    "int b;"
    "} Color;"
    "",
    "typedef struct {",
    "int x;",
    "int y;",
    "int radius;",
    "int t;",
    "Color color;",
    "} Cursor;",
    "",
]


c_draw_shape_func = [
    "ShapeType get_shape_type(const char* shape_type) {                  // retourne le type de forme",
    "    if (strcmp(shape_type, \"ligne\") == 0) return SHAPE_LINE;",
    "    if (strcmp(shape_type, \"rectangle\") == 0) return SHAPE_RECTANGLE;",
    "    if (strcmp(shape_type, \"oval\") == 0) return SHAPE_OVAL;",
    "    if (strcmp(shape_type, \"point\") == 0) return SHAPE_POINT;",
    "    if (strcmp(shape_type, \"arc\") == 0) return SHAPE_ARC;",
    "    if (strcmp(shape_type, \"circle\") == 0) return SHAPE_CIRCLE;",
    "    return SHAPE_UNKNOWN;",
    "}",
    "",
   "void draw_shape(SDL_Renderer* renderer, const char* shape_type, Cursor cursor, int x2, int y2, int z) {",
    "    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, 255);",
    "    int t = cursor.t;",
    "    ShapeType type = get_shape_type(shape_type);",
    "    double theta = cursor.radius * (M_PI / 180.0);",
    "    switch (type) {",
    "        case SHAPE_LINE:",
    "            for (int i = 0; i < t; i++) {",
    "                int x1_rot = cursor.x + (cursor.x + i - cursor.x) * cos(theta) - (cursor.y + i - cursor.y) * sin(theta);",
    "                int y1_rot = cursor.y + (cursor.x + i - cursor.x) * sin(theta) + (cursor.y + i - cursor.y) * cos(theta);",
    "                int x2_rot = cursor.x + (x2 + i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);",
    "                int y2_rot = cursor.y + (x2 + i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);",
    "                SDL_RenderDrawLine(renderer, x1_rot, y1_rot, x2_rot, y2_rot);",
    "            }",
    "            break;",
    "        case SHAPE_RECTANGLE: {",
    "            for (int i = 0; i < t; i++) {",
    "                SDL_Point points[4];",
    "                points[0].x = cursor.x + (cursor.x - i - cursor.x) * cos(theta) - (cursor.y - i - cursor.y) * sin(theta);",
    "                points[0].y = cursor.y + (cursor.x - i - cursor.x) * sin(theta) + (cursor.y - i - cursor.y) * cos(theta);",
    "                points[1].x = cursor.x + (x2 + i - cursor.x) * cos(theta) - (cursor.y - i - cursor.y) * sin(theta);",
    "                points[1].y = cursor.y + (x2 + i - cursor.x) * sin(theta) + (cursor.y - i - cursor.y) * cos(theta);",
    "                points[2].x = cursor.x + (x2 + i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);",
    "                points[2].y = cursor.y + (x2 + i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);",
    "                points[3].x = cursor.x + (cursor.x - i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);",
    "                points[3].y = cursor.y + (cursor.x - i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);",
    "                SDL_RenderDrawLine(renderer, points[0].x, points[0].y, points[1].x, points[1].y);",
    "                SDL_RenderDrawLine(renderer, points[1].x, points[1].y, points[2].x, points[2].y);",
    "                SDL_RenderDrawLine(renderer, points[2].x, points[2].y, points[3].x, points[3].y);",
    "                SDL_RenderDrawLine(renderer, points[3].x, points[3].y, points[0].x, points[0].y);",
    "            }",
    "            break;",
    "        }",
    "        case SHAPE_OVAL: {",
    "            int radius_x = (x2 - cursor.x) / 2;",
    "            int radius_y = (y2 - cursor.y) / 2;",
    "            int center_x = cursor.x + radius_x;",
    "            int center_y = cursor.y + radius_y;",
    "            double angle = M_PI;",
    "            for (int i = 0; i < t; i++) {",
    "                for (int angle = 0; angle < 360; angle++) {",
    "                    double radian = angle * (M_PI / 180.0);",
    "                    int px = center_x + (radius_x + i) * cos(radian);",
    "                    int py = center_y + (radius_y + i) * sin(radian);",
    "                    int px_rot = cursor.x + (px - cursor.x) * cos(theta) - (py - cursor.y) * sin(theta);",
    "                    int py_rot = cursor.y + (px - cursor.x) * sin(theta) + (py - cursor.y) * cos(theta);",
    "                    SDL_RenderDrawPoint(renderer, px_rot, py_rot);",
    "                }",
    "            }",
    "            break;",
    "        }",
    "        case SHAPE_CIRCLE: {",
    "            int radius = z;",
    "            for (int i = 0; i < t; i++) {",
    "                for (double a = 0; a < 2 * M_PI; a += 0.001) {",
    "                    int x = x2 + (int)((radius + i) * cos(a));",
    "                    int y = y2 + (int)((radius + i) * sin(a));",
    "                    int x_rot = cursor.x + (x - cursor.x) * cos(theta) - (y - cursor.y) * sin(theta);",
    "                    int y_rot = cursor.y + (x - cursor.x) * sin(theta) + (y - cursor.y) * cos(theta);",
    "                    SDL_RenderDrawPoint(renderer, x_rot, y_rot);",
    "                }",
    "            }",
    "            break;",
    "        }",
    "        case SHAPE_ARC: {",
    "            int radius = z;",
    "            double angle = M_PI;",
    "            for (int i = 0; i < t; i++) {",
    "                for (double a = 0; a <= angle; a += 0.001) {",
    "                    int x = x2 + (int)((radius + i) * cos(a));",
    "                    int y = y2 + (int)((radius + i) * sin(a));",
    "                    int x_rot = cursor.x + (x - cursor.x) * cos(theta) - (y - cursor.y) * sin(theta);",
    "                    int y_rot = cursor.y + (x - cursor.x) * sin(theta) + (y - cursor.y) * cos(theta);",
    "                    SDL_RenderDrawPoint(renderer, x_rot, y_rot);",
    "                }",
    "            }",
    "            break;",
    "        }",
    "        case SHAPE_UNKNOWN:",
    "        default:",
    "            printf(\"La forme '%s' n'existe pas.\\n\", shape_type);",
    "            break;",
    "    }",
    "}"
    "",
    "// Utilisation des séquences d'echappement ANSI pour gérer le curseur",
    "",
    "void moveCursor(Cursor* cursor, int x, int y) {",
    "    cursor->x = x;",
    "    cursor->y = y;",
    "}",
    "",
    "void rotateCursor(Cursor* cursor, int angle) {",
    "   cursor->radius =  angle;",
    "}",
    "",
    "void setCursorColor(Cursor* cursor, int r, int g, int b) {",
    "   cursor->color.r = r;",
    "   cursor->color.g = g;",
    "   cursor->color.b = b;",
    "}",
    "void setThickness(Cursor* cursor, int t) {",
    "cursor->t = t;",
    "}",
    "",
     "Cursor createCursor(Cursor* existingCursor, int x, int y) {",
    "    if (existingCursor != NULL) {",
    "        existingCursor->x = x;",
    "        existingCursor->y = y;",
    "        //Couleur par défaut",
    "",        
    "        return *existingCursor;  // Retourne le curseur modifié",
    "    } else {",
    "        Cursor newCursor;",
    "        newCursor.x = x;",
    "        newCursor.y = y;",
    "        setCursorColor(&newCursor, 0, 0, 0);",
    "        return newCursor;  // Retourne un nouveau curseur",
    "    }",
    "}"
    "",
]


c_main_begin = [
     "int main(int argc, char *argv[]) {",
    "    // Initialisation de SDL",
    "    printf(\"Initialisation de SDL...\\n\");",
    "    if (SDL_Init(SDL_INIT_VIDEO) != 0) {",
    "        printf(\"Erreur d'initialisation de SDL : %s\\n\", SDL_GetError());",
    "        return 1;",
    "    }",
    "    SDL_Window* window = SDL_CreateWindow(\"Test SDL\", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);",
    "    if (!window) {",
    "        printf(\"Erreur de création de la fenêtre : %s\\n\", SDL_GetError());",
    "        SDL_Quit();",
    "        return 1;",
    "    }",
    "    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);",
    "    if (!renderer) {",
    "        printf(\"Erreur de création du renderer : %s\\n\", SDL_GetError());",
    "        SDL_DestroyWindow(window);",
    "        SDL_Quit();",
    "        return 1;",
    "    }",
    "    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);",
    "    SDL_RenderClear(renderer);",
]

c_main_end = [
    "    SDL_RenderPresent(renderer);",
    "",
    "    SDL_Delay(5000);",
    "",
    "    SDL_DestroyRenderer(renderer);",
    "    SDL_DestroyWindow(window);",
    "    SDL_Quit();",
    "",
    "    return 0;",
    "}"
]

def HexToRGB(hex):
    hex = hex.lstrip('#')
    
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)   
    b = int(hex[4:6], 16)
    
    return r, g, b

global c_main_content
c_main_content = []
# Étape 2 : Écrire le fichier C
def get_instruction(parsed_output, depth=4):
    """
    Génère du code C basé sur une structure AST.
    Traite les instructions `createCursor`.

    :param parsed_output: Dictionnaire représentant l'AST.
    :param depth: Profondeur actuelle pour l'indentation (utilisé pour déboguer).
    """
    #print('parsed_output in generate c', parsed_output)
    indent = " " * depth
    print(f"{indent}Parsed output received in generate_c_code.")
    created_variable = set() # Stocker les curseurs créés
    if isinstance(parsed_output, dict):
        print(f"{indent}Processing root node.")
        # Parcourir les enfants de la racine
        children = parsed_output.get("children", [])
        for node in children:
            node_type = node.get("type")
            
            # Traiter les nœuds "createCursor"
            if node_type == "createCursor":
                print(f"{indent}Found 'createCursor' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                # Extraire le nœud "coordinates"
                coordinates = next((child for child in node.get("children", []) if child.get("type") == "coordinates"), None)
                
                # Extraire les coordonnées x et y
                x = next((child for child in coordinates.get("children", []) if child.get("type") == "x"), None)
                y = next((child for child in coordinates.get("children", []) if child.get("type") == "y"), None)
                
                # Récupérer les valeurs
                cursorId_value = cursorId.get("value")
                x_value = x.get("value")
                y_value = y.get("value")
                
                # Afficher les coordonnées validées
                print(f"{indent}Cursor id={cursorId_value} coordinates: x={x_value}, y={y_value}.")
                # Vérifiez si le curseur existe déjà
                if cursorId_value in created_variable:
                    print(f"{indent}Cursor '{cursorId_value}' already exists. Updating its values.")
                    c_main_content.append(f"moveCursor(&{cursorId_value}, {x_value}, {y_value});")
                else:
                    print(f"{indent}Creating new cursor '{cursorId_value}'.")
                    created_variable.add(cursorId_value)
                    c_main_content.append(f"Cursor {cursorId_value} = {{ {x_value}, {y_value}, 0, 1, {{0, 0, 0}} }};")
                    
            elif node_type == "move":
                print(f"{indent}Found 'move' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                move = next((child for child in node.get("children",[]) if child.get("type") == "value"),None)
                
                cursorId_value = cursorId.get("value")
                move_value = move.get("value")
                c_main_content.append(f"moveCursor(&{cursorId_value}, {move_value}, {move_value});")
            elif node_type == "setColor":
                print(f"{indent}Found 'setColor' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                HexColor = next((child for child in node.get("children",[]) if child.get("type") == "color"),None)

                cursorId_value = cursorId.get("value")  
                r,g,b = HexToRGB(HexColor.get("value"))                
                c_main_content.append(f"setCursorColor(&{cursorId_value}, {r}, {g},{b});")
            elif node_type == "setThickness":
                print(f"{indent}Found 'setThickness' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                thickness = next((child for child in node.get("children",[]) if child.get("type") == "thickness"),None)

                cursorId_value = cursorId.get("value")
                thickness_value = thickness.get("value")
                c_main_content.append(f"setThickness(&{cursorId_value}, {thickness_value});")
            elif node_type == "rotate":
                print(f"{indent}Found 'rotate' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                angle = next((child for child in node.get("children",[]) if child.get("type") == "value"), None)
                
                cursorId_value = cursorId.get("value")
                angle_value = angle.get("value")
                c_main_content.append(f"rotateCursor(&{cursorId_value}, {angle_value});")

            elif node_type == "drawCircle":
                print(f"{indent}Found 'drawCircle' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                radius = next((child for child in node.get("children",[]) if child.get("type") == "radius"), None)
                coordinates = next((child for child in node.get("children",[]) if child.get("type") == "coordinates"), None)
                
                x = next((child for child in coordinates.get("children", []) if child.get("type") == "x"), None)
                y = next((child for child in coordinates.get("children", []) if child.get("type") == "y"), None)

                cursorId_value = cursorId.get("value")
                radius_value = radius.get("value")
                x_value = x.get("value")
                y_value = y.get("value")

                c_main_content.append(f"draw_shape(renderer,\"circle\",{cursorId_value}, {x_value}, {y_value}, {radius_value});")

            elif node_type == "drawOval":
                print(f"{indent}Found 'drawCircle' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                radius = next((child for child in node.get("children",[]) if child.get("type") == "radius"), None)
                coordinates = next((child for child in node.get("children",[]) if child.get("type") == "coordinates"), None)
                
                x = next((child for child in coordinates.get("children", []) if child.get("type") == "x"), None)
                y = next((child for child in coordinates.get("children", []) if child.get("type") == "y"), None)

                cursorId_value = cursorId.get("value")
                radius_value = radius.get("value")
                x_value = x.get("value")
                y_value = y.get("value")

                c_main_content.append(f"draw_shape(renderer,\"oval\",{cursorId_value}, {x_value}, {y_value}, 1, 1, 1);")
                          
            elif node_type == "drawLine":
                print(f"{indent}Found 'drawLine' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                coordinates = node.get("children")[2]

                x = next((child for child in coordinates.get("children", []) if child.get("type") == "x"), None)
                y = next((child for child in coordinates.get("children", []) if child.get("type") == "y"), None)

                cursorId_value = cursorId.get("value")
                
                x_value = x.get("value")
                y_value = y.get("value")

                c_main_content.append(f"draw_shape(renderer,\"ligne\",{cursorId_value}, {x_value}, {y_value}, 1);")
                
            elif node_type == "drawRectangle":
                print(f"{indent}Found 'drawRectangle' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                width = next((child for child in node.get("children",[]) if child.get("type") == "width"), None)
                height = next((child for child in node.get("children",[]) if child.get("type") == "height"), None)
                coordinates = next((child for child in node.get("children",[]) if child.get("type") == "coordinates"), None)

                x = next((child for child in coordinates.get("children", []) if child.get("type") == "x"), None)
                y = next((child for child in coordinates.get("children", []) if child.get("type") == "y"), None)

                cursorId_value = cursorId.get("value")
                width_value = width.get("value")
                height_value = height.get("value")
                x_value = x.get("value")
                y_value = y.get("value")

                c_main_content.append(f"draw_shape(renderer, \"rectangle\",{cursorId_value}, {height_value}, {width_value}, 1);")

            elif node_type == "drawArc":
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                radius = next((child for child in node.get("children",[]) if child.get("type") == "radius"), None)
                angle = next((child for child in node.get("children",[]) if child.get("type") == "start_angle"), None)

                cursorId_value = cursorId.get("value")
                radius_value = radius.get("value")
                angle_value = angle.get("value")

                c_main_content.append(f"draw_shape(renderer,\"arc\",{cursorId_value}, {radius_value}, {angle_value}, 1);")
                #draw_shape(renderer, "arc",cursor1, 10, 5,1);
            elif node_type == "assignment":
                assignmentId_value = node.get("value") 
                assignment_type = next((child for child in node.get("children", []) if child.get("type") == "number"), None)
                if assignment_type:
                    assignment_value = assignment_type.get("value")
                    if assignmentId_value in created_variable:
                        print(f"{indent}Variable '{assignmentId_value}' already exists. Updating its value.")
                        c_main_content.append(f"{assignmentId_value} = {assignment_value};")
                    else:
                        c_main_content.append(f"int {assignmentId_value} = {assignment_value};")
                        created_variable.add(assignmentId_value) 
            elif node_type == "if":
                # Générer le code pour la condition
                comparaison = next((child for child in node.get("children", []) if child.get("type") == "comparison"), None)
                if comparaison:
                    operator = comparaison.get("value")
                    left = comparaison.get("children", [])[0]
                    right = comparaison.get("children", [])[1]

                    left_value = left.get("value") 
                    right_value = right.get("value") 

                    # Ajouter la condition "if" au contenu
                    c_main_content.append(f"if ({left_value} {operator} {right_value}) {{")
                    print(f"Condition: if ({left_value} {operator} {right_value})")
                else:
                    # Si aucune comparaison, afficher un message d'erreur pour le debug
                    print("Erreur : aucune comparaison trouvée dans le bloc if.")

                # Vérifier si un bloc "else" est présent
                elsecdt = next((child for child in node.get("children", []) if child.get("type") == "else"), None)

                # Générer le code pour le bloc "program" associé au "if"
                program_node = next((child for child in node.get("children", []) if child.get("type") == "program"), None)
                if program_node:
                    get_instruction(program_node)

                # Si pas de bloc "else", fermer le bloc "if"
                if not elsecdt:
                    c_main_content.append("}")  # Fermer le bloc "if"

                # Gérer le bloc "else" s'il est présent
                if elsecdt:
                    c_main_content.append("} else {")  # Ajouter la déclaration "else"
                    # Générer le code pour le programme du bloc "else"
                    else_program_node = next((child for child in elsecdt.get("children", []) if child.get("type") == "program"), None)
                    if else_program_node:
                        get_instruction(else_program_node)
                    c_main_content.append("}")  # Fermer le bloc "else"


            elif node_type == "while":
                print(f"{indent}Found 'while' node.")
                comparaison = next((child for child in node.get("children", []) if child.get("type") == "comparison"), None)
                if comparaison:
                    operator = comparaison.get("value")
                    left = comparaison.get("children", [])[0]
                    right = comparaison.get("children", [])[1]

                    left_value = left.get("value") 
                    right_value = right.get("value") 
                    
                    c_main_content.append(f"while ({left_value} {operator} {right_value}) {{")
                    program_node = next((child for child in node.get("children", []) if child.get("type") == "program"), None)
                    if program_node:
                        get_instruction(program_node)
                    c_main_content.append("}")

            else:
                print(f"{indent}Skipping node of type '{node_type}'.")

    else:
        raise TypeError("Expected 'parsed_output' to be a dictionary representing the AST.")

def generate_c_code(parsed_output):
    c_main_content.clear()
    get_instruction(parsed_output)
    complete_code = c_header + c_draw_shape_func + c_main_begin + c_main_content + c_main_end
    print(f"c_main_content: {c_main_content}")
    filename = "Output.c"
    with open(filename, "w") as file:
        file.write("\n".join(complete_code))

    print(f"Code C écrit dans le fichier : {filename}")

    # Étape 3 : Compiler le fichier C sur Windows
    compile_command = f"gcc {filename} -o output -I include -L lib -lmingw32 -lSDL2main -lSDL2"
    try:
        subprocess.run(compile_command, shell=True, check=True)
        print("Compilation réussie.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compilation : {e}")
        exit(1)

    # Étape 4 : Exécuter le programme compilé sur Windows
    run_command = "output.exe"  
    try:
        result = subprocess.run(run_command, shell=True, check=True, capture_output=True, text=True)
        print("Exécution réussie.")
        print("Sortie du programme :")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution : {e}")
        print(e.stderr)
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Fichier {filename} supprimé après délai.")
        else:
            print(f"Fichier {filename} introuvable pour suppression.")
    except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")
