from tictactoe.planche import Planche
from tictactoe.joueur import JoueurHumain, JoueurMachine
from tictactoe.exceptions import ErreurExceptionCoup
from math import inf as infini
from os import system, name

class Partie:
    def __init__(self):
        self.planche = Planche()

        self.piece_joueur_courant = "X"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []

        self.initialiser_joueurs()

    def initialiser_joueurs(self):
        self.joueur_x = self.creer_joueur('X')
        self.joueur_o = self.creer_joueur('O')
        self.joueur_courant = self.joueur_x

    def creer_joueur(self, piece):
        if piece.lower() == "O":
            return JoueurMachine("O")
        else:
            return JoueurHumain("X")

    def obtenir_piece_joueur_adverse(self):
        if self.piece_joueur_courant == "X":
            return "O"
        return "X"

    def valider_position_coup(self, position_coup):
        # On lance une exception pour tout type de situation qui empêche un joueur
        # de jouer un coup.
        valide = True
        erreur = ""

        if not self.planche.position_valide(position_coup):
            erreur = "Position coup invalide: la position entrée est à l'extérieur de la planche de jeu.\n"
            raise ErreurExceptionCoup(erreur)
        elif self.planche.get_piece(position_coup) is not None:
            erreur = "Position coup invalide: une pièce se trouve déjà à cette position.\n"
            raise ErreurExceptionCoup(erreur)
        return valide, erreur

    def tour(self, position):
        # On joue le tour présent en vérifiant s'il termine la partie.
        # Sinon, on valide le coup et on procède au changement de couleur si tout est dans l'ordre.
        # On vérifie finalement si un coup peut être joué dans le tour suivant.
        self.coups_possibles = self.planche.lister_coups_possibles()

        if not self.valider_position_coup(position)[0]:
            return
        self.planche.jouer_coup(position, self.piece_joueur_courant)
        if self.partie_terminee():
            return

    # On vérifie si dans un état donné de la planche, O gagne (une ligne complète de O dans l'état), X gagne (une
    # ligne complète de X dans l'état)ou le match est nul
    def obtenir_valeur_heuristique(self, etat_planche):
        ligne_complete = etat_planche.verifier_ligne_complete()

        if ligne_complete[0] and ligne_complete[1] == "O":
            score = + 1
        elif ligne_complete[0] and ligne_complete[1] == "X":
            score = -1
        else:
            score = 0
        return score

    def minimax(self, etat_planche, piece, profondeur, scores, profondeur_initiale):

        # On intialise avec le pire score pour O qui est MAX, X qui est MIN
        if piece == "O":
            optimal = [None, -infini]
        else:
            optimal = [None, +infini]

        # Si on est au bout de l'arbre ou si la partie est gagnée par un joueur, on retourne le score
        if profondeur == 0 or etat_planche.verifier_ligne_complete()[0]:
            score = self.obtenir_valeur_heuristique(etat_planche)
            return [None, score]

        # On parcour l'arbre récursivement, en faisant alterner les pièces pour respecter MAX = O et MIN = X
        for position in etat_planche.lister_coups_possibles():
            # Lorsqu'on joue un coup, la quantité de coups possibles baisse, ce qui nous fait descendre dans l'arbre
            # des états possibles
            etat_planche.jouer_coup(position, piece)

            # Le tour change
            if piece == "O":
                prochaine_piece = "X"
            else:
                prochaine_piece = "O"

            # Obtention du score d'une position en faisant le trajet récursif
            score = self.minimax(etat_planche, prochaine_piece, profondeur - 1, scores, profondeur_initiale)

            # On replace la position dans le score qui nous est retournée, puisqu'on a None dans score[0] à ce point
            # La position qu'on sauvegarde se retrouve dans la profondeur la plus haute en terme de hauteur verticale
            # dans l'arbre
            score[0] = position

            # On retire la pièce de notre état de planche (qui est en fait une copie), pour pouvoir continuer la
            # recherche à partir de la profondeur initiale.
            etat_planche.retirer_piece(position)

            if piece == "O": # Valeur MAX O
                if score[1] > optimal[1]:
                    optimal = score
                    # On sauvegarde les positions de la plus haute profondeur, pour pouvoir faire un affichage des
                    # candidats possibles. On conserve seulement les meilleurs quandidats rencontrés dans notre
                    # recherche, c'est-à-dire les positions aux valeurs heuristiques les plus grandes. On ne conserve
                    # ni une position à une valeur égale, ni une position à une valeur moindre.
                    if profondeur == profondeur_initiale:
                        scores[score[0]] = score[1], profondeur
            else: # Valeur MIN X
                if score[1] < optimal[1]:
                    optimal = score
                    if profondeur == profondeur_initiale:
                        scores[score[0]] = score[1], profondeur
        return optimal

    def afficher_section_arbre(self, scores, valeur_minimax):
        self.clear()
        # Premier élément du dictionnaire, pour obtenir la profondeur
        profondeur = list(scores.items())[0][1][1]
        s = " À la profondeur " + str(profondeur) + ", la position qui optimise MAX (pièce O) est " + str(valeur_minimax[0]) + " avec la valeur heuristique " + str(
            valeur_minimax[1]) + ".\n"
        s += "  +-0-+-1-+-2-+\n"
        for i in range(0, self.planche.nb_cases):
            s += str(i) + " | "
            for j in range(0, self.planche.nb_cases):
                if (i, j) in self.planche.cases:
                    s += str(self.planche.cases[(i, j)].piece) + " | "
                elif (i, j) in scores:
                    if scores[(i, j)][0] == -1:
                        s += str(scores[(i, j)][0]) + "| "
                    else:
                        s += str(scores[(i, j)][0]) + " | "
                else:
                    s += "  | "
            s += str(i)
            if i != self.planche.nb_cases - 1:
                s += "\n  +---+---+---+\n"

        s += "\n  +-0-+-1-+-2-+\n"
        print(s)

    def clear(self):
        # for windows
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def verifier_prochain_tour(self):
        # On vérifie si un coup peut être joué dans ce tour, si oui on retourne,
        # sinon on passe le tour.
        self.coups_possibles = self.planche.lister_coups_possibles()

    def passer_tour(self):
        # On passe le tour et on met l'attribut de vérification du tour_precedent à vrai.
        # L'exception est lancée et affiche l'erreur au joueur avec une description.
        self.tour_precedent_passe = True
        self.changer_piece()
        self.coups_possibles = self.planche.lister_coups_possibles()

        if len(self.coups_possibles) == 0:
            self.deux_tours_passes = True
            return
        joueur_adverse = self.obtenir_piece_joueur_adverse()
        raise ErreurExceptionCoup("Le joueur " + joueur_adverse + " ne peut pas jouer avec l'état actuel de la planche,"
                                                           " il doit donc passer son tour.\n")

    def changer_piece(self):
        if self.joueur_courant.piece == "X":
            self.joueur_courant = self.joueur_o
            self.piece_joueur_courant = "O"
        else:
            self.joueur_courant = self.joueur_x
            self.piece_joueur_courant = "X"

    def partie_terminee(self):
        # S'il y a 64 pièces sur la planche ou que deux tours sont passés, la partie est terminée.
        if len(self.planche.cases.keys()) > 8 or self.planche.verifier_ligne_complete()[0] is True:
            return True
        return False

    def determiner_gagnant(self):
        x = self.compter_pieces()[0]
        o = self.compter_pieces()[1]

        if(self.planche.verifier_ligne_complete()[0] is False):
            return("Match nul.", "nul")

        if x > o:
            return("Le gagnant est X en " + str(x+o) + " tours.","X")
        else:
            return("Le gagnant est O en " + str(x+o) + " tours.", "O")

    def compter_pieces(self):
        x = 0
        o = 0
        for coords in self.planche.cases:
            if self.planche.cases[coords].piece == "X":
                x += 1
            else:
                o += 1

        return x, o