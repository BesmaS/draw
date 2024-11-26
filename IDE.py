# Juste l'aspect de base IDE
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import ttkbootstrap as ttk
from ttkbootstrap.constants import *#nv

# Initialisation de la fenêtre principale
compiler = ttk.Window(themename="flatly")  # Choose theme NV
compiler.title('🎨Draw++ IDE')
compiler.geometry("800x600")
file_path = ''


# Fonctions de gestion des fichiers
def set_file_path(path):
    global file_path
    file_path = path

#initialisatioon des numéros de ligne 
def update_line_number(event=None):
    line_numbers = ""
    for i in range(1, int(editor.index('end').split('.')[0])):  # Nombre de lignes dans l'éditeur
        line_numbers += f"{i}\n"
    line_number_bar.config(state='normal')  # Permet d'écrire dans le widget
    line_number_bar.delete('1.0', END)  # Supprime l'ancien contenu
    line_number_bar.insert('1.0', line_numbers)  # Ajoute les numéros de ligne
    line_number_bar.config(state='disabled')  # Empêche la modification

# Numéro de ligne (barre à gauche)
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
        line_number_bar.config(bg="dim gray", fg="white")  # Gris foncé pour la barre de numéros
        compiler.config(bg="gray20")
    else:
        editor.config(bg="white", fg="black", insertbackground="black")
        output_display.config(bg="white", fg="black")
        line_number_bar.config(bg="white", fg="black")
        compiler.config(bg="SystemButtonFace")

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

settings_menu = Menu(menu_bar,tearoff=0)
settings_menu.add_command(label="Toggle Theme", command=toggle_theme)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

compiler.config(menu=menu_bar)


# Zones de texte
editor = Text(compiler, wrap="word", undo=True)
editor.pack(expand=True, fill='both')
editor.bind("<KeyRelease>", update_line_number)  # Met à jour après chaque frappe

output_display = Text(compiler, height=10, bg="lightgrey", fg="black")
output_display.pack(fill="both")
# Add a status bar
status_bar = Label(compiler, text="Draw++ IDE - Ready", anchor=W, relief=SUNKEN)
status_bar.pack(side=BOTTOM, fill=X)

compiler.mainloop()
