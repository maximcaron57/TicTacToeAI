class Piece:

    def __init__(self, piece):
        self.piece = piece

    def est_o(self):
        return self.piece == "O"

    def est_x(self):
        return self.piece == "X"

    def echange_piece(self):
        self.piece = "X" if self.est_o() else "O"

    def __repr__(self):
        if self.est_x():
            return "\u274C"
        else:
            return "\u25EF"
