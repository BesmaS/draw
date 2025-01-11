/*#include <SDL2/SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


typedef struct {
    int x;
    int y;
    int r;
} Cursor;


typedef enum {
    SHAPE_LINE,
    SHAPE_RECTANGLE,
    SHAPE_OVAL,
    SHAPE_POINT,
    SHAPE_UNKNOWN
} ShapeType;

ShapeType get_shape_type(const char* shape_type) {                  // retourne le type de forme
    if (strcmp(shape_type, "ligne") == 0) return SHAPE_LINE;
    if (strcmp(shape_type, "rectangle") == 0) return SHAPE_RECTANGLE;
    if (strcmp(shape_type, "oval") == 0) return SHAPE_OVAL;
    if (strcmp(shape_type, "point") == 0) return SHAPE_POINT;
    return SHAPE_UNKNOWN;
}


void draw_shape(SDL_Renderer* renderer, const char* shape_type, Cursor cursor, int x2, int y2, int r, int g, int b, int width) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);     // couleur
    ShapeType type = get_shape_type(shape_type);        // forme

    switch (type) {
        case SHAPE_LINE:
            SDL_RenderDrawLine(renderer, cursor.x, cursor.y, x2, y2);
            break;

        case SHAPE_RECTANGLE: {
            SDL_Rect rect = {cursor.x, cursor.y, x2 - cursor.x, y2 - cursor.y};
            SDL_RenderDrawRect(renderer, &rect);
            break;
        }

        case SHAPE_OVAL: {
            int radius_x = (x2 - cursor.x) / 2;
            int radius_y = (y2 - cursor.y) / 2;
            int center_x = cursor.x + radius_x;
            int center_y = cursor.y + radius_y;
            for (int angle = 0; angle < 360; angle++) {
                double radian = angle * (M_PI / 180.0);
                int px = center_x + radius_x * cos(radian);
                int py = center_y + radius_y * sin(radian);
                SDL_RenderDrawPoint(renderer, px, py);
            }
            break;
        }

        case SHAPE_POINT:
            for (int w = 0; w < width; ++w) {
                SDL_RenderDrawPoint(renderer, cursor.x + w, cursor.y + w);
            }
            break;

        case SHAPE_UNKNOWN:
        default:
            printf("La forme '%s' n'existe pas.\n", shape_type);
            break;
    }
}

// Utilisation des séquences d'echappement ANSI pour gérer le curseur

void moveCursor(Cursor* cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
    printf("\033[%d;%dH", cursor->y, cursor->x); // Les coordonnées sont 1-indexées, 1,1 est le coin supérieur gauche, le H à la fin signifie de deplacer le curseur a une position donnée
}
void setCursorColor(const char* color) {
    printf("\033[%sm", color);   // 30 : Noir 31 : Rouge 32 : Vert 33 : Jaune 34 : Bleu 35 : Magenta 36 : Cyan 37 : Blanc, le m actives les attributs graphique (couleur, effets etc...)
}

Cursor createCursor(int x, int y) {
    Cursor cursor;
    cursor.x = x;
    cursor.y = y;
    return cursor;
}
//SDL drawpoint
void resetAttributes() {
    printf("\033[0m"); // Reset la couleur et le style du curseur, 0m reset tout les attributs graphiques
}

void clearScreen() {
printf("\033[2J\033[H");  // 2J: Nettoie l'écran, H: Remet le curseur au coin supérieur gauche
}

void hideCursor() {
    printf("\033[?25l");    // 25l: Desactive l'affichage du curseur 
}

void showCursor() {
    printf("\033[?25h");    // 25h: Active l'affichage du curseur
}

int main(int argc, char *argv[]) {
    // Initialisation de SDL",
        printf("Initialisation de SDL...\n");
        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            printf("Erreur d'initialisation de SDL : %s\n", SDL_GetError());
            return 1;
        }
     SDL_Window* window = SDL_CreateWindow("Test SDL", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
        if (!window) {
            printf("Erreur de création de la fenêtre : %s\n", SDL_GetError());
            SDL_Quit();
            return 1;
        }
    
        SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
        if (!renderer) {
            printf("Erreur de création du renderer : %s\n", SDL_GetError());
            SDL_DestroyWindow(window);
            SDL_Quit();
            return 1;
        }
    
        // Couleur de fond",
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        
    Cursor cursor = createCursor(0, 0);
    
    if (&cursor != NULL){
        free(&cursor);
        Cursor cursor = createCursor(5, 0);
    }
    showCursor();
    moveCursor(&cursor, 10, 10);    // Deplace le curseur vers la position 10, 10
    printf("cursor:x=%d,y=%d",cursor.x,cursor.y);
    setCursorColor("31");           // Change la couleur du curseur en rouge
    draw_shape(renderer, "ligne", cursor, 20, 20, 0, 255, 255, 150);    // Dessine une ligne verticale
    moveCursor(&cursor, 30, 30);
    draw_shape(renderer, "rectangle", cursor, 50, 50, 0, 0, 255, 400); // Dessine un rectangle  
    moveCursor(&cursor, 60, 60);
    draw_shape(renderer, "oval", cursor, 80, 80, 255, 0, 0, 100);       // Dessine un cercle
    moveCursor(&cursor, 90, 90);
    draw_shape(renderer, "point", cursor, 100, 100, 0, 255, 0, 51);    // Dessine un point
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);
    resetAttributes();
     
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}*/

#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef enum {
    SHAPE_LINE,
    SHAPE_RECTANGLE,
    SHAPE_OVAL,
    SHAPE_POINT,
    SHAPE_CIRCLE,
    SHAPE_ARC,
    SHAPE_UNKNOWN
} ShapeType;

typedef struct {
    int r;
    int g;
    int b;
} Color;

typedef struct {
    int x;
    int y;
    int radius;
    Color color;
} Cursor;

ShapeType get_shape_type(const char* shape_type) {                  // retourne le type de forme
    if (strcmp(shape_type, "ligne") == 0) return SHAPE_LINE;
    if (strcmp(shape_type, "rectangle") == 0) return SHAPE_RECTANGLE;
    if (strcmp(shape_type, "oval") == 0) return SHAPE_OVAL;
    if (strcmp(shape_type, "point") == 0) return SHAPE_POINT;
    if (strcmp(shape_type, "circle") == 0) return SHAPE_CIRCLE;
    if (strcmp(shape_type, "arc") == 0) return SHAPE_ARC;
    return SHAPE_UNKNOWN;
}

void draw_shape(SDL_Renderer* renderer, const char* shape_type, Cursor cursor, int x2, int y2,int z) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, 255);     // couleur
    printf("couleur : %d %d %d\n", cursor.color.r, cursor.color.g, cursor.color.b);
    ShapeType type = get_shape_type(shape_type);        // forme

    switch (type) {
        case SHAPE_LINE:
            SDL_RenderDrawLine(renderer, cursor.x, cursor.y, x2, y2);
            break;

        case SHAPE_RECTANGLE: 
            int height = x2;
            int width = y2;
            SDL_Rect rect = {cursor.x, cursor.y, x2 - cursor.x, y2 - cursor.y};
            SDL_RenderDrawRect(renderer, &rect);
            break;
        

        case SHAPE_OVAL: 
            int radius_x = (x2 - cursor.x) / 2;
            int radius_y = (y2 - cursor.y) / 2;
            int center_x = cursor.x + radius_x;
            int center_y = cursor.y + radius_y;
            for (int angle = 0; angle < 360; angle++) {
                double radian = angle * (M_PI / 180.0);
                int px = center_x + radius_x * cos(radian);
                int py = center_y + radius_y * sin(radian);
                SDL_RenderDrawPoint(renderer, px, py);
            }
            break;
        case SHAPE_CIRCLE:
            int radius = z;
            for (double angle = 0; angle < 2 * M_PI; angle += 0.001) {   // on parcourt l'angle en radian
                int x = x2 + (int)(radius * cos(angle));
                int y = y2 + (int)(radius * sin(angle));
                SDL_RenderDrawPoint(renderer, x, y);
            }
            break;
        case SHAPE_POINT:
            for (int w = 0; w < width; ++w) {
                SDL_RenderDrawPoint(renderer, cursor.x + w, cursor.y + w);
            }
            break;
        case SHAPE_ARC:
            int angle = x2;
            for (double a = 0; a <= angle; a += 0.001) {
                int x = cursor.x + (int)(radius * cos(a));
                int y = cursor.y + (int)(radius * sin(a));
                SDL_RenderDrawPoint(renderer, x, y);
            }

            break;
        case SHAPE_UNKNOWN:
        default:
            printf("La forme '%s' n'existe pas.\n", shape_type);
            break;
    }
}

void setCursorColor(Cursor* cursor, int r, int g, int b) {
    cursor->color.r = r;
    cursor->color.g = g;
    cursor->color.b = b;
}

void rotateCursor(Cursor* cursor, int angle) {
    cursor->radius =  angle;
}

void moveCursor(Cursor* cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
}

Cursor createCursor(Cursor* existingCursor, int x, int y, int r, int g, int b) {
    if (existingCursor != NULL) {
        existingCursor->x = x;
        existingCursor->y = y;
        existingCursor->color.r = r;
        existingCursor->color.g = g;
        existingCursor->color.b = b;
        return *existingCursor;  // Retourne le curseur modifié
    } else {
        Cursor newCursor;
        newCursor.x = x;
        newCursor.y = y;
        return newCursor;  // Retourne un nouveau curseur
    }
}

int main(int argc, char *argv[]) {
    // Initialisation de SDL
    printf("Initialisation de SDL...\n");
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("Erreur d'initialisation de SDL : %s\n", SDL_GetError());
        return 1;
    }
    SDL_Window* window = SDL_CreateWindow("Test SDL", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur de création de la fenêtre : %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Erreur de création du renderer : %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    //Exemples
    Cursor cursor1 = { 1, 2, 0,255,255,255 };
    moveCursor(&cursor1, 50, 50);
    
    
    
    moveCursor(&cursor1, 80, 80);
    Cursor cursor228 = { 2, 4 };
    moveCursor(&cursor1, 10, 10);
    draw_shape(renderer,"ligne",cursor1, 2, 2, 1);
    moveCursor(&cursor1, 100, 100);
    setCursorColor(&cursor1, 255, 200, 0);
    draw_shape(renderer, "rectangle",cursor1, 21, 12, 1);
    setCursorColor(&cursor1, 5, 0, 100);
    moveCursor(&cursor1, 500, 400);
    draw_shape(renderer, "rectangle",cursor1, 100, 25, 1);
    setCursorColor(&cursor1, 255, 0, 0);
   
    moveCursor(&cursor1, 200, 400);
    draw_shape(renderer, "circle",cursor1, 500, 500,10);
    draw_shape(renderer, "oval",cursor1, 1, 1,1);
    moveCursor(&cursor1, 400, 77);
     draw_shape(renderer, "arc",cursor1, 77, 1,1);
    //draw_shape(renderer, "circle",cursor1, 50,1);
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return EXIT_SUCCESS;
}
