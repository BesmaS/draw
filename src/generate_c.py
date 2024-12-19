# generate_c.py
import subprocess
from parser import ASTNode



def generate_c_code(node, indent=0):
    code = ""
    indent_str = " " * indent

    if node.node_type == 'program':
        code += "#include <SDL2/SDL.h>\n\n"
        code += "int main(int argc, char* argv[]) {\n"
        code += f"{indent_str}if (SDL_Init(SDL_INIT_VIDEO) != 0) {{\n"
        code += f"{indent_str}    printf(\"SDL_Init Error: %s\\n\", SDL_GetError());\n"
        code += f"{indent_str}    return 1;\n"
        code += f"{indent_str}}}\n"
        code += f"{indent_str}SDL_Window *win = SDL_CreateWindow(\"Hello SDL\", 100, 100, 640, 480, SDL_WINDOW_SHOWN);\n"
        code += f"{indent_str}if (win == NULL) {{\n"
        code += f"{indent_str}    printf(\"SDL_CreateWindow Error: %s\\n\", SDL_GetError());\n"
        code += f"{indent_str}    SDL_Quit();\n"
        code += f"{indent_str}    return 1;\n"
        code += f"{indent_str}}}\n"
        code += f"{indent_str}SDL_Renderer *ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);\n"
        code += f"{indent_str}if (ren == NULL) {{\n"
        code += f"{indent_str}    SDL_DestroyWindow(win);\n"
        code += f"{indent_str}    printf(\"SDL_CreateRenderer Error: %s\\n\", SDL_GetError());\n"
        code += f"{indent_str}    SDL_Quit();\n"
        code += f"{indent_str}    return 1;\n"
        code += f"{indent_str}}}\n"



        for child in node.children:
            code += generate_c_code(child, indent + 4)
        code += f"{indent_str}SDL_SetRenderDrawColor(ren, 255, 255, 255, 255);\n"
        code += f"{indent_str}SDL_RenderClear(ren);\n"
        code += f"{indent_str}SDL_SetRenderDrawColor(ren, 255, 0, 0, 255);\n"
        code += f"{indent_str}SDL_RenderFillRect(ren, &cursor2);\n"
        code += f"{indent_str}SDL_RenderPresent(ren);\n"
        code += f"{indent_str}SDL_Delay(5000);\n"
        code += f"{indent_str}SDL_DestroyRenderer(ren);\n"
        code += f"{indent_str}SDL_DestroyWindow(win);\n"
        code += f"{indent_str}SDL_Quit();\n"
        code += f"{indent_str}return 0;\n"
        code += "}\n"
    elif node.node_type == 'createCursor':
        identifiant = node.children[0].value
        x = node.children[1].children[0].value
        y = node.children[1].children[1].value
        code += f"{indent_str}SDL_Rect {identifiant} = {{ {x}, {y}, 50, 50 }};\n"
    elif node.node_type == 'if':
        condition = generate_c_code(node.children[0])
        then_block = generate_c_code(node.children[1], indent + 4)
        else_block = generate_c_code(node.children[2], indent + 4)
        code += f"{indent_str}if ({condition}) {{\n{then_block}{indent_str}}} else {{\n{else_block}{indent_str}}}\n"
    elif node.node_type == 'comparison':
        left = generate_c_code(node.children[0])
        right = generate_c_code(node.children[1])
        code += f"{left} {node.value} {right}"
    elif node.node_type == 'assignment':
        variable = node.value
        value = generate_c_code(node.children[0])
        code += f"{indent_str}int {variable} = {value};\n"
    elif node.node_type == 'variable':
        code += node.value
    elif node.node_type == 'number':
        code += str(node.value)

    return code

def save_c_code_to_file(c_code, filename):
    with open(filename, 'w') as file:
        file.write(c_code)

def compile_and_run_c_code(filename):
    # Compile the C code
    compile_command = f"gcc -o output {filename} -lSDL2"
    compile_process = subprocess.run(compile_command, shell=True, check=True)
    
    # Run the compiled executable
    run_command = "./output"
    run_process = subprocess.run(run_command, shell=True, check=True)