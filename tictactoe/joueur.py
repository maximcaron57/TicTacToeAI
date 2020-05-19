class Joueur:
    def __init__(self, piece):
        self.piece = piece

class JoueurHumain(Joueur):
    def __init__(self, piece):

        super().__init__(piece)

    def obtenir_type_joueur(self):
        return "Humain"

class JoueurMachine(Joueur):
    def __init__(self, piece):

        super().__init__(piece)

    def obtenir_type_joueur(self):
        return "Machine"