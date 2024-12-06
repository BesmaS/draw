# Juste l'aspect de base IDE
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import ttkbootstrap as ttk
from ttkbootstrap.constants import *#nv

from math import cos, sin, radians

# Initialisation de la fenêtre principale
compiler = ttk.Window(themename="flatly")  # Choose theme NV
compiler.title('🎨Draw++ IDE')
compiler.geometry("800x600")
file_path = ''

canvas = Canvas(compiler, bg="white", width=600, height=400)
canvas.pack(side="top", expand=True, fill="both")


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



def draw_shape(shape_type, x, y, **kwargs):
    color = kwargs.get('color', 'black')
    width = kwargs.get('width', 2)

    if shape_type == "line":
        x2 = kwargs.get('x2', x + 50)
        y2 = kwargs.get('y2', y)
        canvas.create_line(x, y, x2, y2, fill=color, width=width)
    elif shape_type == "rectangle":
        x2 = kwargs.get('x2', x + 50)
        y2 = kwargs.get('y2', y + 50)
        canvas.create_rectangle(x, y, x2, y2, outline=color, width=width)
    elif shape_type == "oval":  # dessine un cercle lorsque x2 et y2 sont identiques
        x2 = kwargs.get('x2', x + 50)
        y2 = kwargs.get('y2', y + 50)
        canvas.create_oval(x, y, x2, y2, outline=color, width=width)
    elif shape_type == "point":
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color, width=width)
    else:
        print(f"La forme '{shape_type}' n'existe pas.") 
        
        
cursors = [] # Liste pour stocker les curseurs



def create_cursor(x=0, y=0, visible=True, color="black", width=2):
    cursor = {
        "x": x,
        "y": y,
        "visible": visible,
        "color": color,
        "width": width
    }
    cursors.append(cursor)
    if visible:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color)
  

def move_cursor(cursor, distance):
    # Calcul de la nouvelle position
    new_x = cursor["x"] + distance * cos(radians(cursor["angle"]))
    new_y = cursor["y"] + distance * sin(radians(cursor["angle"]))
    
    canvas.create_line(cursor["x"], cursor["y"], new_x, new_y, fill="black", width=2)    # Dessine une ligne entre l'ancienne et nouvelle position
    
    cursor["x"] = new_x # Met à jour la nouvelle position du curseur
    cursor["y"] = new_y

def rotate_cursor(cursor, angle):
    cursor["angle"] = (cursor["angle"] + angle) % 360 # Met à jour l'angle du curseur

def set_cursor_visibility(index, visible):
    if 0 <= index < len(cursors):
        cursors[index]["visible"] = visible # le visibilité du curseur est mis à jour
        if visible:
            cursor = cursors[index]
            canvas.create_oval(
                cursor["x"] - 3, cursor["y"] - 3, cursor["x"] + 3, cursor["y"] + 3,     # Dessine le curseur
                fill=cursor["color"]
            )
        else:
            canvas.delete("all")  # Supprime tout du canevas 
            for cur in cursors:
                if cur["visible"]:
                    canvas.create_oval(
                        cur["x"] - 3, cur["y"] - 3, cur["x"] + 3, cur["y"] + 3,     # redessine uniquement les curseurs visibles
                        fill=cur["color"]
                    )
