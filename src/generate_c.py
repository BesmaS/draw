import subprocess
from pathlib import Path
import json

# Programme C initial 
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
    "    SHAPE_UNKNOWN",
    "} ShapeType;",
    "",
    "typedef struct {",
    "int x;",
    "int y;",
    "} Cursor;",
]


c_draw_shape_func = [
    "ShapeType get_shape_type(const char* shape_type) {                  // retourne le type de forme",
    "    if (strcmp(shape_type, \"ligne\") == 0) return SHAPE_LINE;",
    "    if (strcmp(shape_type, \"rectangle\") == 0) return SHAPE_RECTANGLE;",
    "    if (strcmp(shape_type, \"oval\") == 0) return SHAPE_OVAL;",
    "    if (strcmp(shape_type, \"point\") == 0) return SHAPE_POINT;",
    "    return SHAPE_UNKNOWN;",
    "}",
    "",
    "void draw_shape(SDL_Renderer* renderer, const char* shape_type, Cursor cursor, int x2, int y2, int r, int g, int b, int width) {",
    "    SDL_SetRenderDrawColor(renderer, r, g, b, 255);     // couleur",
    "    ShapeType type = get_shape_type(shape_type);        // forme",
    "",
    "    switch (type) {",
    "        case SHAPE_LINE:",
    "            SDL_RenderDrawLine(renderer, cursor.x, cursor.y, x2, y2);",
    "            break;",
    "",
    "        case SHAPE_RECTANGLE: {",
    "            SDL_Rect rect = {cursor.x, cursor.y, x2 - cursor.x, y2 - cursor.y};",
    "            SDL_RenderDrawRect(renderer, &rect);",
    "            break;",
    "        }",
    "",
    "        case SHAPE_OVAL: {",
    "            int radius_x = (x2 - cursor.x) / 2;",
    "            int radius_y = (y2 - cursor.y) / 2;",
    "            int center_x = cursor.x + radius_x;",
    "            int center_y = cursor.y + radius_y;",
    "            for (int angle = 0; angle < 360; angle++) {",
    "                double radian = angle * (M_PI / 180.0);",
    "                int px = center_x + radius_x * cos(radian);",
    "                int py = center_y + radius_y * sin(radian);",
    "                SDL_RenderDrawPoint(renderer, px, py);",
    "            }",
    "            break;",
    "        }",
    "",
    "        case SHAPE_POINT:",
    "            for (int w = 0; w < width; ++w) {",
    "                SDL_RenderDrawPoint(renderer, cursor.x + w, cursor.y + w);",
    "            }",
    "            break;",
    "",
    "        case SHAPE_UNKNOWN:",
    "        default:",
    "            printf(\"La forme '%s' n'existe pas.\\n\", shape_type);",
    "            break;",
    "    }",
    "}",
    "",
    "// Utilisation des séquences d'echappement ANSI pour gérer le curseur",
    "",
    "void moveCursor(Cursor* cursor, int x, int y) {",
    "    cursor->x = x;",
    "    cursor->y = y;",
    "    printf(\"\\033[%d;%dH\", cursor->y, cursor->x); // Les coordonnées sont 1-indexées, 1,1 est le coin supérieur gauche, le H à la fin signifie de deplacer le curseur a une position donnée",
    "}",
    "void setCursorColor(const char* color) {",
    "    printf(\"\\033[%sm\", color);   // 30 : Noir 31 : Rouge 32 : Vert 33 : Jaune 34 : Bleu 35 : Magenta 36 : Cyan 37 : Blanc, le m actives les attributs graphique (couleur, effets etc...)",
    "}",
    "",
    "Cursor createCursor(Cursor existingCursor, int x, int y) {",
    "    if (existingCursor != NULL) {",
    "        free(existingCursor);  // Libère la mémoire si le curseur existe déjà",
    "    }",
    "    Cursor cursor = (Cursor)malloc(sizeof(Cursor));  // Alloue de la mémoire pour un nouveau curseur",
    "    cursor.x = x;",
    "    cursor.y = y;",
    "    return cursor;",
    "}",
    "",
    "void resetAttributes() {",
    "    printf(\"\\033[0m\"); // Reset la couleur et le style du curseur, 0m reset tout les attributs graphiques",
    "}",
    "",
    "void clearScreen() {",
    "    printf(\"\\033[2J\\033[H\");  // 2J: Nettoie l'écran, H: Remet le curseur au coin supérieur gauche",
    "}",
    "",
    "void hideCursor() {",
    "    printf(\"\\033[?25l\");    // 25l: Desactive l'affichage du curseur ",
    "}",
    "",
    "void showCursor() {",
    "    printf(\"\\033[?25h\");    // 25h: Active l'affichage du curseur",
    "}",
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
    "    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);",
    "    SDL_RenderClear(renderer);",
]
#Partie du code ajouté en fonction du parsed output
c_main_content = [
    
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
    "    return EXIT_SUCCESS;",
    "}"
]


# Écriture dans le fichier C
def generate_c_code(parsed_output, depth=0):
    """
    Génère du code C basé sur une structure AST.
    Traite les instructions `createCursor`.

    :param parsed_output: Dictionnaire représentant l'AST.
    :param depth: Profondeur actuelle pour l'indentation (utilisé pour déboguer).
    """
    indent = " " * depth
    print(f"{indent}Parsed output received in generate_c_code.")
    
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
                c_main_content.append(f"Cursor {cursorId_value} = createCursor({x_value},{y_value});")
                # TODO: Générer le code C pour cette instruction
            elif node_type == "move":
                print(f"{indent}Found 'move' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                move = next((child for child in node.get("children",[]) if child.get("type") == "value"),None)
                
                cursorId_value = cursorId.get("value")
                move_value = move.get("value")
                c_main_content.append(f"moveCursor(&{cursorId_value}, {move_value}, {move_value});")
                
            elif node_type == "rotate":
                print(f"{indent}Found 'rotate' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "identifiant"), None)
                angle = next((child for child in node.get("children",[]) if child.get("type") == "value"), None)
                
                cursorId_value = cursorId.get("value")
                angle_value = angle.get("value")
                #c_main_content.append(f"rotateCursor(&{cursorId_value}, {angle_value});")

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

                c_main_content.append(f"draw_shape(renderer,\"oval\",{cursorId_value}, {x_value}, {y_value}, 255, 0, 0, 1);")
                    # draw_shape(renderer, "oval", cursor, 80, 80, 255, 0, 0, 100); 
            elif node_type == "drawLine":
                print(f"{indent}Found 'drawLine' node.")
                cursorId = next((child for child in node.get("children",[]) if child.get("type") == "cursor"), None)
                start_coordinates = node.get("children")[1]
                end_coordinates = node.get("children")[2]

                #start_x = next((child for child in start_coordinates.get("children", []) if child.get("type") == "x"), None)
                #start_y = next((child for child in start_coordinates.get("children", []) if child.get("type") == "y"), None)
                end_x = next((child for child in end_coordinates.get("children", []) if child.get("type") == "x"), None)
                end_y = next((child for child in end_coordinates.get("children", []) if child.get("type") == "y"), None)

                cursorId_value = cursorId.get("value")
                #start_x_value = start_x.get("value")
                #start_y_value = start_y.get("value")
                end_x_value = end_x.get("value")
                end_y_value = end_y.get("value")

                c_main_content.append(f"draw_shape(renderer,\"ligne\",{cursorId_value}, {end_x_value}, {end_y_value}, 0, 255, 255, 1);")
                
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

                c_main_content.append(f"draw_shape(renderer, \"rectangle\",{cursorId_value}, {width_value}, {height_value}, 255, 255, 255,1);")

            #elif node_type == "drawArc":
               

            else:
                print(f"{indent}Skipping node of type '{node_type}'.")

    else:
        raise TypeError("Expected 'parsed_output' to be a dictionary representing the AST.")

    print(c_main_content)
    complete_code = c_header + c_draw_shape_func + c_main_begin + c_main_content + c_main_end
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

#Exemple pour l'execution
parsed_output = {
    "type": "program",
    "value": None,
    "children": [
        {
            "type": "createCursor",
            "value": None,
            "children": [
                {
                    "type": "identifiant",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 1,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 2,
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "type": "move",
            "value": None,
            "children": [
                {
                    "type": "identifiant",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "value",
                    "value": 50,
                    "children": []
                }
            ]
        },
        {
            "type": "rotate",
            "value": None,
            "children": [
                {
                    "type": "identifiant",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "value",
                    "value": 90,
                    "children": []
                }
            ]
        },
        {
            "type": "drawCircle",
            "value": None,
            "children": [
                {
                    "type": "cursor",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "radius",
                    "value": 120,
                    "children": []
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 3,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 2,
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "type": "drawLine",
            "value": None,
            "children": [
                {
                    "type": "cursor",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 3,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 4,
                            "children": []
                        }
                    ]
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 2,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 2,
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "type": "drawArc",
            "value": None,
            "children": [
                {
                    "type": "cursor",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "radius",
                    "value": 3,
                    "children": []
                },
                {
                    "type": "start_angle",
                    "value": 120,
                    "children": []
                },
                {
                    "type": "end_angle",
                    "value": 80,
                    "children": []
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 2,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 2,
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "type": "drawRectangle",
            "value": None,
            "children": [
                {
                    "type": "cursor",
                    "value": "cursor1",
                    "children": []
                },
                {
                    "type": "width",
                    "value": 21,
                    "children": []
                },
                {
                    "type": "height",
                    "value": 12,
                    "children": []
                },
                {
                    "type": "coordinates",
                    "value": None,
                    "children": [
                        {
                            "type": "x",
                            "value": 2,
                            "children": []
                        },
                        {
                            "type": "y",
                            "value": 3,
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
}



generate_c_code(parsed_output)
