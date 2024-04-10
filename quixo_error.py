"""Module QuixoError

Classes:
    * QuixoError - Classe d'erreur pour le jeu Quixo.
"""
class QuixoError(Exception):
    def __init__(self, message, position=None):
        super().__init__(message)
        self.position = position