<programme> ::= <instruction> ";"
              | <instruction> ";" <programme>

<instruction> ::= <curseur_instruction>
                | <dessin_instruction>
                | <couleur_instruction>
                | <épaisseur_instruction>
                | <controle_instruction>

<curseur_instruction> ::= "createCursor" "(" <identifiant> "," <coordonnees> ")"
                        | "move" "(" <identifiant> "," <nombre_pixels> ")"
                        | "rotate" "(" <identifiant> "," <degres> ")"

<dessin_instruction> ::= "drawLine" "(" <coordonnees> "," <coordonnees> ")"
                       | "drawCircle" "(" <coordonnees> "," <rayon> ")"
                       | "drawRectangle" "(" <coordonnees> "," <largeur> "," <hauteur> ")"
                       | "drawArc" "(" <coordonnees> "," <rayon> "," <angle> ")"
                       
<couleur_instruction> ::= "setColor" "(" <identifiant> "," <couleur> ")"
<épaisseur_instruction> ::= "setThickness" "(" <identifiant> "," <épaisseur> ")"
<controle_instruction> ::= <condition_instruction> 
                         | <boucle_instruction>

<condition_instruction> ::= "if" "(" <expression> ")" "{" <programme> "}" ["else" "{" <programme> "}"]

<boucle_instruction> ::= "for" "(" <initialisation> ";" <condition> ";" <incrementation> ")" "{" <programme> "}"
                       | "while" "(" <expression> ")" "{" <programme> "}"
<expression> ::= <variable> <operateur> <valeur>

<initialisation> ::= <variable> "=" <valeur>
<incrementation> ::= <variable> "++" | <variable> "--"

<coordonnees> ::= "x" <nombre> "," "y" <nombre>
<rayon> ::= <nombre>
<largeur> ::= <nombre>
<hauteur> ::= <nombre>
<angle> ::= <nombre>
<nombre_pixels> ::= <nombre>
<degres> ::= <nombre>

<couleur> ::= "#" <hexadecimal>    (* couleur en hexadécimal *)
<épaisseur> ::= <nombre>

<variable> ::= <identifiant>
<valeur> ::= <nombre> | <variable>
<operateur> ::= "==" | "!=" | "<" | ">" | "<=" | ">="
