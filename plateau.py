"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""
from copy import deepcopy

from quixo_error import QuixoError


class Plateau:
    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.plateau = self.construire_plateau(deepcopy(plateau))


    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Déplacer le code de votre fonction formater_plateau ici et ajuster le en conséquence.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        lignes = []
        for ligne in self.plateau:
            lignes.append("| ".join(ligne))
        return "\n".join(lignes)

    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du pion sur le plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        return self.plateau[y - 1][x - 1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du pion sur le plateau.
            value (str): La valeur à insérer à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: La valeur donnée doit être "X", "O" ou " ".
        """
        x, y = position
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        if valeur not in ("X", "O", " "):
            raise QuixoError("La valeur donnée doit être 'X', 'O' ou ' '.")
        self.plateau[y - 1][x - 1] = valeur

    def construire_plateau(self, plateau):
        """Construit un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Le plateau doit être une liste de 5 listes de 5 éléments.
            QuixoError: Les éléments du plateau doivent être "X", "O" ou " ".
        """
        if plateau is None:
            return [[" " for _ in range(5)] for _ in range(5)]

        if not isinstance(plateau, list) or len(plateau) != 5:
            raise QuixoError("Le plateau doit être une liste de 5 listes de 5 éléments.")
        for ligne in plateau:
            if not isinstance(ligne, list) or len(ligne) != 5:
                raise QuixoError("Le plateau doit être une liste de 5 listes de 5 éléments.")
            for element in ligne:
                if element not in ("X", "O", " "):
                    raise QuixoError("Les éléments du plateau doivent être 'X', 'O' ou ' '.")

        return plateau

    def insertion(self, pion, origine, direction):
        """Insère un pion dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la direction donnée.

        À noter que la validation des positions sont faites dans
        les méthodes __setitem__ et __getitem__. Vous devez donc en faire usage dans
        les diverses méthodes d'insertion pour vous assurez que les positions sont valides.

        Args:
            pion (str): La valeur du pion à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du pion à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".
            QuixoError: Le pion à insérer doit être "X" ou "O".
        """
        if not isinstance(pion, str) or pion not in ("X", "O"):
            raise QuixoError("Le pion à insérer doit être 'X' ou 'O'.")

        if not isinstance(direction, str) or direction not in ("haut", "bas", "gauche", "droite"):
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        if direction == "haut":
            self.insertion_par_le_haut(pion, origine)
        elif direction == "bas":
            self.insertion_par_le_bas(pion, origine)
        elif direction == "gauche":
            self.insertion_par_la_gauche(pion, origine)
        else:
            self.insertion_par_la_droite(pion, origine)

    def insertion_par_le_bas(self, pion, origine):
        """Insère un pion dans le plateau en direction du bas

        Args:
            pion (str): La valeur du pion à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du pion à insérer.
        """
        x, y = origine
        self[x, y] = pion
        for i in range(y - 1, -1, -1):
            self[x, i + 1] = self[x, i]
        self[x, 0] = " "

    def insertion_par_le_haut(self, pion, origine):
        """Insère un pion dans le plateau en direction du haut

        Args:
            pion (str): La valeur du pion à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du pion à insérer.
        """
        x, y = origine
        self[x, y] = pion
        for i in range(y + 1, 5):
            self[x, i - 1] = self[x, i]
        self[x, 4] = " "


    def insertion_par_la_gauche(self, pion, origine):
        """Insère un pion dans le plateau en direction de la gauche

        Args:
            pion (str): La valeur du pion à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du pion à insérer.
        """
        x, y = origine
        self[x, y] = pion
        for i in range(x - 1, -1, -1):
            self[i + 1, y] = self[i, y]
        self[0, y] = " "

    def insertion_par_la_droite(self, pion, origine):
        """Insère un pion dans le plateau en direction de la droite

        Args:
            pion (str): La valeur du pion à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du pion à insérer.
        """
        x, y = origine
        self[x, y] = pion
        for i in range(x + 1, 5):
            self[i - 1, y] = self[i, y]
        self[4, y] = " "
