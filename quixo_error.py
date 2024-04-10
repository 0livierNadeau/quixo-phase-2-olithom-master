"""Module QuixoError

Classes:
    * QuixoError - Classe d'erreur pour le jeu Quixo.
"""
class QuixoError(Exception):
    def __init__(self, message, position=None):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self):
        if self.position is None:
            return self.message
        else:
            return f"{self.message} (position: {self.position})"