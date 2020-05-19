from tkinter import messagebox

class ErreurExceptionCoup(Exception):
    # On redéfinit le constructeur de la classe Exception pour générer un messagebox
    # quand on lance l'erreur de type ErreurExceptionCoup, en prenant en paramètre le
    # message d'erreur.
    def __init__(self, message):
        super().__init__(message)
        self.popup = messagebox.showerror("Erreur", message)
    pass
