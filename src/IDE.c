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
    int t; 
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

void draw_shape(SDL_Renderer* renderer, const char* shape_type, Cursor cursor, int x2, int y2, int z) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, 255);     // couleur
    int t = cursor.t;        // épaisseur
    ShapeType type = get_shape_type(shape_type);        // forme
    double theta = cursor.radius * (M_PI / 180.0); // Convertir l'angle du curseur en radians
    switch (type) {
        case SHAPE_LINE:
            for (int i = 0; i < t; i++) {
                // Points originaux de la ligne
                int x1_rot = cursor.x + (cursor.x + i - cursor.x) * cos(theta) - (cursor.y + i - cursor.y) * sin(theta);
                int y1_rot = cursor.y + (cursor.x + i - cursor.x) * sin(theta) + (cursor.y + i - cursor.y) * cos(theta);
                int x2_rot = cursor.x + (x2 + i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);
                int y2_rot = cursor.y + (x2 + i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);
                SDL_RenderDrawLine(renderer, x1_rot, y1_rot, x2_rot, y2_rot);
            }
            break;

        case SHAPE_RECTANGLE: {
            for (int i = 0; i < t; i++) {
                // Calcul des 4 sommets du rectangle
                SDL_Point points[4];
                points[0].x = cursor.x + (cursor.x - i - cursor.x) * cos(theta) - (cursor.y - i - cursor.y) * sin(theta);
                points[0].y = cursor.y + (cursor.x - i - cursor.x) * sin(theta) + (cursor.y - i - cursor.y) * cos(theta);

                points[1].x = cursor.x + (x2 + i - cursor.x) * cos(theta) - (cursor.y - i - cursor.y) * sin(theta);
                points[1].y = cursor.y + (x2 + i - cursor.x) * sin(theta) + (cursor.y - i - cursor.y) * cos(theta);

                points[2].x = cursor.x + (x2 + i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);
                points[2].y = cursor.y + (x2 + i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);

                points[3].x = cursor.x + (cursor.x - i - cursor.x) * cos(theta) - (y2 + i - cursor.y) * sin(theta);
                points[3].y = cursor.y + (cursor.x - i - cursor.x) * sin(theta) + (y2 + i - cursor.y) * cos(theta);

                // Dessiner le rectangle
                SDL_RenderDrawLine(renderer, points[0].x, points[0].y, points[1].x, points[1].y);
                SDL_RenderDrawLine(renderer, points[1].x, points[1].y, points[2].x, points[2].y);
                SDL_RenderDrawLine(renderer, points[2].x, points[2].y, points[3].x, points[3].y);
                SDL_RenderDrawLine(renderer, points[3].x, points[3].y, points[0].x, points[0].y);
            }
            break;
        }

        case SHAPE_OVAL: {
            int radius_x = (x2 - cursor.x) / 2;
            int radius_y = (y2 - cursor.y) / 2;
            int center_x = cursor.x + radius_x;
            int center_y = cursor.y + radius_y;
            double angle = M_PI;
            for (int i = 0; i < t; i++) {
                for (int angle = 0; angle < 360; angle++) {
                    double radian = angle * (M_PI / 180.0);
                    int px = center_x + (radius_x + i) * cos(radian);
                    int py = center_y + (radius_y + i) * sin(radian);

                    // Appliquer la rotation au point
                    int px_rot = cursor.x + (px - cursor.x) * cos(theta) - (py - cursor.y) * sin(theta);
                    int py_rot = cursor.y + (px - cursor.x) * sin(theta) + (py - cursor.y) * cos(theta);

                    SDL_RenderDrawPoint(renderer, px_rot, py_rot);
                }
            }
            break;
        }

        case SHAPE_CIRCLE: {
            int radius = z;
           
            for (int i = 0; i < t; i++) {
                for (double a = 0; a < 2 * M_PI; a += 0.001) {
                    int x = x2 + (int)((radius + i) * cos(a));
                    int y = y2 + (int)((radius + i) * sin(a));

                    // Appliquer la rotation au point
                    int x_rot = cursor.x + (x - cursor.x) * cos(theta) - (y - cursor.y) * sin(theta);
                    int y_rot = cursor.y + (x - cursor.x) * sin(theta) + (y - cursor.y) * cos(theta);

                    SDL_RenderDrawPoint(renderer, x_rot, y_rot);
                }
            }
            break;
        }

        case SHAPE_ARC: {
            int radius = z;
            double angle = M_PI;
            for (int i = 0; i < t; i++) {
                for (double a = 0; a <= angle; a += 0.001) {
                    int x = x2 + (int)((radius + i) * cos(a));
                    int y = y2 + (int)((radius + i) * sin(a));

                    // Appliquer la rotation au point
                    int x_rot = cursor.x + (x - cursor.x) * cos(theta) - (y - cursor.y) * sin(theta);
                    int y_rot = cursor.y + (x - cursor.x) * sin(theta) + (y - cursor.y) * cos(theta);

                    SDL_RenderDrawPoint(renderer, x_rot, y_rot);
                }
            }
            break;
        }

        case SHAPE_UNKNOWN:
        default:
            printf("La forme '%s' n'existe pas.\n", shape_type);
            break;
    }
}

Cursor setCursorColor(Cursor* cursor, int r, int g, int b) {
    cursor->color.r = r;
    cursor->color.g = g;
    cursor->color.b = b;
    return *cursor;
}

void rotateCursor(Cursor* cursor, int angle) {
    cursor->radius =  angle;
}

void moveCursor(Cursor* cursor, int x, int y) {
    cursor->x = x;
    cursor->y = y;
}
void setThickness(Cursor* cursor, int t) {
    cursor->t = t;
}
Cursor createCursor(Cursor* existingCursor, int x, int y, int r, int g, int b, int t) {
    if (existingCursor != NULL) {
        existingCursor->x = x;
        existingCursor->y = y;
        existingCursor->color.r = r;
        existingCursor->color.g = g;
        existingCursor->color.b = b;
        existingCursor->t = t;
        return *existingCursor;  // Retourne le curseur modifié
    } else {
        Cursor newCursor;
        newCursor.x = x;
        newCursor.y = y;
        newCursor.t = t;
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
    Cursor cursor1 = { 1, 2, 0, 1, { 0, 0, 0 }};
    moveCursor(&cursor1, 100, 100);
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
    draw_shape(renderer, "arc",cursor1, cursor1.x, cursor1.y, 100);
    moveCursor(&cursor1, 200, 250);
    //rotateCursor(&cursor1,90);
    cursor1 = setCursorColor(&cursor1, 0, 0, 255);
    draw_shape(renderer, "circle",cursor1, cursor1.x, cursor1.y, 100);
    cursor1 = setCursorColor(&cursor1, 255, 0, 0);
    setThickness(&cursor1, 5);
    moveCursor(&cursor1, 500, 350);
    draw_shape(renderer, "rectangle",cursor1, cursor1.x+200, cursor1.y +50, 100);
    rotateCursor(&cursor1,90);
    setThickness(&cursor1, 10);
    draw_shape(renderer, "ligne",cursor1, cursor1.x+200, cursor1.y +50, 100);
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return EXIT_SUCCESS;
}
