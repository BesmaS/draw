# Juste l'aspect de base IDE
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename


# Initialisation de la fenêtre principale
compiler = Tk()
compiler.title('🎨Draw++ IDE')
file_path = ''


# Fonctions de gestion des fichiers
def set_file_path(path):
    global file_path
    file_path = path


def new_file():
    editor.delete('1.0', END)
    set_file_path('')
    compiler.title("New File - Draw++ IDE")


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


# Fonction pour exécuter le code (placeholder) revoir qd grammaire ok
def run():
    output_display.delete('1.0', END)
    output_display.insert('1.0', "Execution of Draw++ code will go here.")


# Création des menus
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

compiler.config(menu=menu_bar)

# Zones de texte
editor = Text(compiler, wrap="word", undo=True)
editor.pack(expand=True, fill='both')

output_display = Text(compiler, height=10, bg="lightgrey", fg="black")
output_display.pack(fill="both")

compiler.mainloop()
