"""ILIACode, séance 1 du module NLP. Du fichier aux tokens (fichier à compléter).

Chaque fonction est une étape de la chaîne
octets -> décoder -> réparer -> normaliser -> tokeniser -> mesurer.
"""
import re
import unicodedata
from collections import Counter

import ftfy

CHIFFRES_ARABES = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
MOTIF = r'\w+|[^\w\s]'   # le cœur, à compléter à gauche par les règles de protection


def lire(chemin, regle="utf-8"):
    """Bloc Lire. Ouvre le fichier en octets puis les décode en caractères."""
    # 1. ouvrir le fichier en mode binaire "rb" et lire ses octets
    with open(chemin ,"rb") as file:
        octets=file.read()
    return octets.decode(regle)


def reparer(text):
    """Bloc Réparer. Corrige les mojibakes, laisse intact un texte sain."""
    # une ligne, ftfy.fix_text(texte, normalization=None)
    # normalization=None, car normaliser est l'étape suivante, pas celle-ci
    return ftfy.fix_text(text , normalization=None)
    


def normaliser(texte, forme="NFKC"):
    """Bloc Normaliser. Une seule écriture par caractère."""
    # 1. unicodedata.normalize(forme, texte)
    # 2. supprimer les diacritiques arabes, de \u064B à \u065F, avec re.sub
    # 3. supprimer le tatweel \u0640 avec replace
    # 4. convertir les chiffres arabes avec translate et CHIFFRES_ARABES
    raise NotImplementedError("bloc Normaliser à compléter")


def tokeniser(texte):
    """Bloc Tokeniser. Six règles, protéger d'abord, découper ensuite."""
    # 1. re.findall(MOTIF, texte) applique les règles 1 à 5
    # 2. règle 6, pour chaque token qui est un mot et contient un tiret bas,
    #    garder le token puis ajouter ses composants, token.split("_")
    raise NotImplementedError("bloc Tokeniser à compléter")


def mesurer(tokens):
    """Bloc Mesurer. Fréquence de chaque token distinct."""
    # une ligne, Counter(tokens)
    raise NotImplementedError("bloc Mesurer à compléter")


def chaine(chemin, regle="utf-8"):
    """La chaîne complète, du fichier aux tokens."""
    return tokeniser(normaliser(reparer(lire(chemin, regle))))
