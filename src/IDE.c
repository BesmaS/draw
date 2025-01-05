#include <SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

typedef struct {
    x,
    y
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


void draw_shape(SDL_Renderer* renderer, const char* shape_type, int x, int y, int x2, int y2, int r, int g, int b, int width) {
    SDL_SetRenderDrawColor(renderer, r, g, b, 255);     // couleur
    ShapeType type = get_shape_type(shape_type);        // forme

    switch (type) {
        case SHAPE_LINE:
            SDL_RenderDrawLine(renderer, x, y, x2, y2);
            break;

        case SHAPE_RECTANGLE: {
            SDL_Rect rect = {x, y, x2 - x, y2 - y};
            SDL_RenderDrawRect(renderer, &rect);
            break;
        }

        case SHAPE_OVAL: {
            int radius_x = (x2 - x) / 2;
            int radius_y = (y2 - y) / 2;
            int center_x = x + radius_x;
            int center_y = y + radius_y;
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
                SDL_RenderDrawPoint(renderer, x + w, y + w);
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

