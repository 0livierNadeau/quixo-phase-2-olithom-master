"""Module d'API du jeu Quixo

Attributes:
    URL (str): Constante représentant le début de l'url du serveur de jeu.

Functions:
    * lister_parties - Récupérer la liste des parties reçus du serveur.
    * débuter_partie - Créer une nouvelle partie et retourne l'état de cette dernière.
    * récupérer_partie - Retrouver l'état d'une partie spécifique.
    * jouer_coup - Exécute un coup et retourne le nouvel état de jeu.
"""
import requests

parties_precedente = 'https://pax.ulaval.ca/quixo/api/h24/parties'

# Définir le délai d'attente à 5 secondes
TIMEOUT = 5

URL = "https://pax.ulaval.ca/quixo/api/h24/"


def lister_parties(idul, secret):
    """Lister les parties..

  Args:
    idul (str): idul du joueur
    secret (str): secret récupérer depuis le site de PAX

  Raises:
    PermissionError: Erreur levée lorsque le serveur retourne un code 401.
    RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
    ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

  Returns:
    list: Liste des parties reçues du serveur,
          après avoir décodé le json de sa réponse.
    """

    url = f"{URL}parties"
    reponse = requests.get(url, params={"idul": idul, "secret": secret}, timeout=TIMEOUT)

    if reponse.status_code == 200:
        return reponse.json()["parties"]
    elif reponse.status_code == 401:
        raise PermissionError("Mauvais idul ou secret.")
    elif reponse.status_code == 406:
        raise RuntimeError("Requête invalide.")
    else:
        raise ConnectionError(f"Erreur serveur ({reponse.status_code}).")


def débuter_partie(idul,  secret):
    """Débuter une partie

    Args:
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    url = f"{URL}partie"
    reponse = requests.post(url, params={"idul": idul, "secret": secret}, timeout=TIMEOUT)

    if reponse.status_code == 200:
        data = reponse.json()
        return data["id"], data["joueurs"], data["état"]
    elif reponse.status_code == 401:
        raise PermissionError("Mauvais idul ou secret.")
    elif reponse.status_code == 406:
        raise RuntimeError("Requête invalide.")
    else:
        raise ConnectionError(f"Erreur serveur ({reponse.status_code}).")


def récupérer_partie(id_partie, idul, secret):
    """Récupérer une partie

    Args:
        id_partie (str): identifiant de la partie à récupérer
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 4 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs, de l'état du plateau et du vainqueur.
    """

    url = f"{URL}partie/{id_partie}"
    reponse = requests.get(url, params={"idul": idul, "secret": secret}, timeout=TIMEOUT)

    if reponse.status_code == 200:
        data = reponse.json()
        return data["id"], data["joueurs"], data["état"], data["gagnant"]
    elif reponse.status_code == 401:
        raise PermissionError("Mauvais idul ou secret.")
    elif reponse.status_code == 406:
        raise RuntimeError("Requête invalide.")
    else:
        raise ConnectionError(f"Erreur serveur ({reponse.status_code}).")


def jouer_coup(id_partie, origine, direction, idul, secret):
    """Jouer un coup

    Args:
        id_partie (str): Identifiant de la partie.
        origine (list): La position [x, y] du bloc à déplacer.
        direction (str): La direction du déplacement du bloc.:
            'haut': Déplacement d'un bloc du bas pour l'insérer en haut.
            'bas': Déplacement d'un bloc du haut pour l'insérer en bas.
            'gauche': Déplacement d'un bloc de droite pour l'insérer à gauche,
            'droite': Déplacement d'un bloc de gauche pour l'insérer à droite,
        idul (str): idul du joueur
        secret (str): secret récupérer depuis le site de PAX

    Raises:
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
        PermissionError: Erreur levée lorsque le serveur retourne un code 401.
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        ConnectionError: Erreur levée lorsque le serveur retourne un code autre que 200, 401 ou 406

    Returns:
        tuple: Tuple de 3 éléments constitué de l'identifiant de la partie en cours,
            de la liste des joueurs et de l'état du plateau.
    """
    url = f"{URL}jouer"
    data = {"id": id_partie, "origine": origine, "direction": direction}
    reponse = requests.put(url, auth=(idul, secret), json=data, timeout=TIMEOUT)

    if reponse.status_code == 200:
        data = reponse.json()
        if data["gagnant"]:
            raise StopIteration(data["gagnant"])
        return data["id"], data["joueurs"], data["état"]
    elif reponse.status_code == 401:
        raise PermissionError("Mauvais idul ou secret.")
    elif reponse.status_code == 406:
        raise RuntimeError("Requête invalide.")
    else:
        raise ConnectionError(f"Erreur serveur ({reponse.status_code}).")