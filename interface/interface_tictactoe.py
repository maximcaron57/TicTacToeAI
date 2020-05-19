from tkinter import Tk, Canvas, Label, NSEW, messagebox
from tictactoe.partie import Partie
from tictactoe.exceptions import ErreurExceptionCoup
import copy

class CanvasBoard(Canvas):
    """Classe héritant d'un Canvas, et affichant un board qui se redimensionne automatiquement lorsque
    la fenêtre est étirée.

    """

    def __init__(self, parent, n_pixels_par_case):
        self.partie = Partie()

        # Nombre de lignes et de colonnes.
        self.n_lignes = 3
        self.n_colonnes = 3

        # Coordonnées des lignes et des colonnes.
        self.chiffres_rangees = [0, 1, 2]
        self.chiffres_colonnes = [0, 1, 2]

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces du jeu.
        self.pieces = self.partie.planche.cases

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def dessiner_cases(self):
        # On dessine les cases

        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                couleur = "green"

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

    def dessiner_pieces(self):
        # Pour tout paire position, pièce:

        for position, piece in self.pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.

            coordonnee_y = (self.n_pixels_par_case * position[1]) + self.n_pixels_par_case // 2
            coordonnee_x = (self.n_pixels_par_case * position[0]) + self.n_pixels_par_case // 2
            self.create_text(coordonnee_y, coordonnee_x, text=piece,
                             font=('Deja Vu', self.n_pixels_par_case // 2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un board
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.rafraichir_board('case')

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.rafraichir_board('piece')

    def rafraichir_board(self, element):
        self.delete(element)
        if element == 'piece':
            self.dessiner_pieces()
        else:
            self.dessiner_cases()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("TicTacToe")

        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_board = CanvasBoard(self, 120)
        self.canvas_board.grid(sticky=NSEW)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()
        self.messages['foreground'] = 'black'
        if (self.canvas_board.partie.piece_joueur_courant == 'X'):
            self.messages['text'] = "Tour du joueur X."
        else:
            self.messages['text'] = "Tour du joueur O."

        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_board.bind('<Button-1>', self.selectionner)

        self.position = self.selectionner

    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_board.n_pixels_par_case
        colonne = event.x // self.canvas_board.n_pixels_par_case
        position = (int(ligne), int(colonne))

        # On joue le coup en passant en paramètre la position cliquée.
        # Le tour du joueur actif est affiché en bas de la fenêtre.
        try:
            self.jouer(position)
            if self.canvas_board.partie.piece_joueur_courant == 'X':
                self.messages['text'] = "Tour du joueur X."
            else:
                self.messages['text'] = "Tour du joueur O."

        # Dans le cas d'une exception, on affiche un popup avec l'erreur.
        except ErreurExceptionCoup as err:
            err.popup

        # Peu importe ce qui arrive, on rafraîchit les pièces sur le board
        finally:
            self.canvas_board.rafraichir_board('piece')

    def jouer(self, position):
        # On passe la position à la classe partie, qui contient la logique du jeu TicTacToe.
        # On ajuste par la suite le canvas selon les changements apportés au board, et si
        # la partie est terminée à ce moment, on détermine le gagnant et on vérifie si l'utilisateur
        # veut recommencer.
        self.canvas_board.partie.tour(position)
        self.canvas_board.rafraichir_board('piece')

        # Tour de la machine
        if not self.canvas_board.partie.partie_terminee():
            # On crée une copie de la planche pour pouvoir la passer comme valeur, et non par référence.
            etat_planche = copy.deepcopy(self.canvas_board.partie.planche)
            profondeur = len(self.canvas_board.partie.planche.lister_coups_possibles())
            # Servira à sauver les positions candidates
            scores = dict()
            valeur_minimax = self.canvas_board.partie.minimax(etat_planche, "O", profondeur, scores, profondeur)

            # Affichage de la section de l'arbre sous forme de planche dans la console
            self.canvas_board.partie.afficher_section_arbre(scores, valeur_minimax)
            self.canvas_board.partie.planche.jouer_coup(valeur_minimax[0], "O")
            self.canvas_board.rafraichir_board('piece')

        if self.canvas_board.partie.partie_terminee():
            self.messages['text'] = self.canvas_board.partie.determiner_gagnant()[0]
            messagebox.showinfo("Partie terminée", self.canvas_board.partie.determiner_gagnant()[0])
            self.recommencer_partie()

    def recommencer_partie(self):
        # Demande à l'utilisateur s'il veut recommencer une partie,
        # si oui on détruit l'instance de fenêtre actuelle pour en créer une nouvelle,
        # sinon on quitte le programme.

        if messagebox.askyesno("Recommencer", "Désirez-vous lancer une nouvelle partie?"):
            self.destroy()
            f = Fenetre()
            f.mainloop()
            return
        else:
            self.destroy()
            exit()
