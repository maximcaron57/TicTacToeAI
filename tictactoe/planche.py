from tictactoe.piece import Piece
from itertools import product

class Planche:

    def __init__(self):
        # Dictionnaire de cases. La clé est une position (ligne, colonne), et la valeur une instance de la classe Piece.
        self.cases = {}

        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()

        # On joue au TicTacToe 3x3
        self.nb_cases = 3

    def get_piece(self, position):
        if position not in self.cases.keys():
            return None

        return self.cases[position]

    def position_valide(self, position):
        return 0 <= position[0] < self.nb_cases and 0 <= position[1] < self.nb_cases

    def verifier_ligne_complete(self):
        if self.get_piece((0, 0)) is not None and self.get_piece((0, 1)) is not None and self.get_piece((0, 2)) is not None:
            if self.get_piece((0, 0)).piece == self.get_piece((0, 1)).piece and self.get_piece((0, 1)).piece == self.get_piece((0, 2)).piece:
                return True, self.get_piece((0, 0)).piece
        if self.get_piece((1, 0)) is not None and self.get_piece((1, 1)) is not None and self.get_piece((1, 2)) is not None:
            if self.get_piece((1, 0)).piece == self.get_piece((1, 1)).piece and self.get_piece((1, 1)).piece == self.get_piece((1, 2)).piece:
                return True, self.get_piece((1, 0)).piece
        if self.get_piece((2, 0)) is not None and self.get_piece((2, 1)) is not None and self.get_piece((2, 2)) is not None:
            if self.get_piece((2, 0)).piece == self.get_piece((2, 1)).piece and self.get_piece((2, 1)).piece == self.get_piece((2, 2)).piece:
                return True, self.get_piece((2, 0)).piece
        if self.get_piece((0, 0)) is not None and self.get_piece((1, 0)) is not None and self.get_piece((2, 0)) is not None:
            if self.get_piece((0, 0)).piece == self.get_piece((1, 0)).piece and self.get_piece((1, 0)).piece == self.get_piece((2, 0)).piece:
                return True, self.get_piece((0, 0)).piece
        if self.get_piece((0, 1)) is not None and self.get_piece((1, 1)) is not None and self.get_piece((2, 1)) is not None:
            if self.get_piece((0, 1)).piece == self.get_piece((1, 1)).piece and self.get_piece((1, 1)).piece == self.get_piece((2, 1)).piece:
                return True, self.get_piece((0, 1)).piece
        if self.get_piece((0, 2)) is not None and self.get_piece((1, 2)) is not None and self.get_piece((2, 2)) is not None:
            if self.get_piece((0, 2)).piece == self.get_piece((1, 2)).piece and self.get_piece((1, 2)).piece == self.get_piece((2, 2)).piece:
                return True, self.get_piece((0, 2)).piece
        if self.get_piece((0, 0)) is not None and self.get_piece((1, 1)) is not None and self.get_piece((2, 2)) is not None:
            if self.get_piece((0, 0)).piece == self.get_piece((1, 1)).piece and self.get_piece((1, 1)).piece == self.get_piece((2, 2)).piece:
                return True, self.get_piece((0, 0)).piece
        if self.get_piece((0, 2)) is not None and self.get_piece((1, 1)) is not None and self.get_piece((2, 0)) is not None:
            if self.get_piece((0, 2)).piece == self.get_piece((1, 1)).piece and self.get_piece((1, 1)).piece == self.get_piece((2, 0)).piece:
                return True, self.get_piece((0, 2)).piece
        return False, None

    def coup_est_possible(self, position):
        # S'il n'y a pas de jeton dans la case, le coup est possible
        return position not in self.cases.keys()

    def lister_coups_possibles(self):
        coups_possibles = []

        for position in list(product(range(self.nb_cases), range(self.nb_cases))):
            if self.coup_est_possible(position):
                coups_possibles.append(position)

        return coups_possibles

    def jouer_coup(self, position, piece):
        # Si le coup est possible, on effectue les changements à la planche, sinon on retourne une erreur
        if not self.coup_est_possible(position):
            return "erreur"

        self.cases[position] = Piece(piece)

        return "ok"

    def retirer_piece(self, position):
        if position in self.cases.keys():
            del self.cases[position]


    def initialiser_planche_par_default(self):
        self.cases.clear()