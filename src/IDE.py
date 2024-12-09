# Juste l'aspect de base IDE
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import ttkbootstrap as ttk # type: ignore
from ttkbootstrap.constants import *# type: ignore #nv
from tokenizer import tokenize # type: ignore
from parser import Parser # type: ignore

# Initialisation de la fenetre principale
compiler = ttk.Window(themename="flatly")  # Choose theme NV
compiler.title('🎨Draw++ IDE')
compiler.geometry("800x600")
file_path = ''

# Fonctions de gestion des fichiers
def set_file_path(path):
    global file_path
    file_path = path

#initialisatioon des numeros de ligne 
def update_line_number(event=None):
    line_numbers = ""
    for i in range(1, int(editor.index('end').split('.')[0])):  # Nombre de lignes dans l'editeur
        line_numbers += f"{i}\n"
    line_number_bar.config(state='normal')  # Permet d'ecrire dans le widget
    line_number_bar.delete('1.0', END)  # Supprime l'ancien contenu
    line_number_bar.insert('1.0', line_numbers)  # Ajoute les numeros de ligne
    line_number_bar.config(state='disabled')  # Empeche la modification

# Numero de ligne (barre a gauche)
line_number_bar = Text(compiler, width=4, bg="lightgrey", state='disabled')
line_number_bar.pack(side="left", fill="y")


def new_file():
    editor.delete('1.0', END)
    set_file_path('')
    compiler.title("New File - Draw++ IDE")
    update_line_number()


def open_file():
    path = askopenfilename(filetypes=[("Draw++ Files", "*.dpp"), ("All Files", "*.*")])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
        set_file_path(path)
        compiler.title(f"{path} - Draw++ IDE")


def save_file():
    if file_path == '':
        path = asksaveasfilename(defaultextension=".dpp",
                                 filetypes=[("Draw++ Files", "*.dpp"), ("All Files", "*.*")])
        if path:
            set_file_path(path)
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
    compiler.title(f"{path} - Draw++ IDE")


# Ajout de la gestion des themes
is_dark_mode = False  # Variable pour garder la trace du theme actuel

#fontion pour changer de themee
def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    
    if is_dark_mode:
        editor.config(bg="black", fg="light gray", insertbackground="light gray")
        output_display.config(bg="black", fg="white")  # Noir pour le fond, blanc pour le texte
        line_number_bar.config(bg="dim gray", fg="white")  # Gris fonce pour la barre de numeros
        compiler.config(bg="gray20")
    else:
        editor.config(bg="white", fg="black", insertbackground="black")
        output_display.config(bg="white", fg="black")
        line_number_bar.config(bg="white", fg="black")
        compiler.config(bg="SystemButtonFace")


def update_syntax_highlighting(event=None):
    """
    Tokenize the code and apply syntax highlighting.
    """
    code = editor.get("1.0", END)
    tokens = tokenize(code)
    
    # Remove previous tags
    editor.tag_remove("KEYWORD", "1.0", "end")
    editor.tag_remove("IDENTIFIER", "1.0", "end")
    editor.tag_remove("NUMBER", "1.0", "end")
    editor.tag_remove("HEX_COLOR", "1.0", "end")
    editor.tag_remove("OPERATOR", "1.0", "end")
    
    # Apply new tags based on token types
    for token in tokens:
        start_index = f"{token.line}.{token.column}"
        end_index = f"{token.line}.{token.column + len(token.value)}"
        
        if token.type == 'KEYWORD':
            editor.tag_add("KEYWORD", start_index, end_index)
        elif token.type == 'IDENTIFIER':
            editor.tag_add("IDENTIFIER", start_index, end_index)
        elif token.type == 'NUMBER':
            editor.tag_add("NUMBER", start_index, end_index)
        elif token.type == 'HEX_COLOR':
            editor.tag_add("HEX_COLOR", start_index, end_index)
        elif token.type == 'OPERATOR':
            editor.tag_add("OPERATOR", start_index, end_index)

def run():
    code = editor.get("1.0", END)
    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        parsed_output = parser.parse_program()
        output_display.delete('1.0', END)
        output_display.insert('1.0', f"Parsed Output:\n{parsed_output}")
    except SyntaxError as e:
        output_display.delete('1.0', END)
        output_display.insert('1.0', f"Syntax Error: {str(e)}")
    except Exception as e:
        output_display.delete('1.0', END)
        output_display.insert('1.0', f"Error: {str(e)}")



# Creation des menus
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_file)
file_menu.add_command(label="Exit", command=compiler.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label="Run", command=run)
menu_bar.add_cascade(label="Run", menu=run_menu)

settings_menu = Menu(menu_bar,tearoff=0)
settings_menu.add_command(label="Toggle Theme", command=toggle_theme)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

compiler.config(menu=menu_bar)


# Zones de texte
editor = Text(compiler, wrap="word", undo=True)
editor.pack(expand=True, fill='both')
editor.bind("<KeyRelease>", update_line_number)  # Met a jour apres chaque frappe


output_display = Text(compiler, height=10, bg="lightgrey", fg="black")
output_display.pack(fill="both")
# Add a status bar
status_bar = Label(compiler, text="Draw++ IDE - Ready", anchor=W, relief=SUNKEN)
status_bar.pack(side=BOTTOM, fill=X)

compiler.mainloop()
