#include <SDL.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

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
