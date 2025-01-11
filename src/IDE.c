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
    SHAPE_UNKNOWN
} ShapeType;

typedef struct {
int x;
int y;
} Cursor;
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


void drawArc(SDL_Renderer *renderer, int x0, int y0, int radius, double angle) {
    for (double a = 0; a <= angle; a += 0.001) {
        int x = x0 + (int)(radius * cos(a));
        int y = y0 + (int)(radius * sin(a));
        SDL_RenderDrawPoint(renderer, x, y);
    }
}

void drawCircle(SDL_Renderer *renderer, int x0, int y0, int radius) {
    for (double angle = 0; angle < 2 * M_PI; angle += 0.001) {   // on parcourt l'angle en radian
        int x = x0 + (int)(radius * cos(angle));
        int y = y0 + (int)(radius * sin(angle));
        SDL_RenderDrawPoint(renderer, x, y);
    }
}

// Utilisation des séquences d'echappement ANSI pour g�rer le curseur

void moveCursor(Cursor* cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
    printf("\033[%d;%dH", cursor->y, cursor->x); // Les coordonnées sont 1-indexées, 1,1 est le coin supérieur gauche, le H à la fin signifie de deplacer le curseur a une position donnée
}

Cursor createCursor(Cursor* existingCursor, int x, int y) {
    if (existingCursor != NULL) {
        existingCursor->x = x;
        existingCursor->y = y;
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
    Cursor cursor1 = { 1, 2 };
    moveCursor(&cursor1, 50, 50);
    
    
    
    moveCursor(&cursor1, 80, 80);
    Cursor cursor228 = { 2, 4 };
    moveCursor(&cursor1, 10, 10);
    draw_shape(renderer,"ligne",cursor1, 2, 2, 0, 255, 255, 1);
    moveCursor(&cursor1, 100, 100);
    draw_shape(renderer, "rectangle",cursor1, 21, 12, 255, 255, 255,1);
        draw_shape(renderer, "rectangle",cursor1, cursor1.x, cursor1.y, 255, 255, 255,1);
    moveCursor(&cursor1, 100, 100);
    setCursorColor("32");
    drawCircle(renderer, cursor1.x, cursor1.y, 50);
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return EXIT_SUCCESS;
}

