# ============================================================
#  Séance 2 --- Le tokeniseur appris, Byte Pair Encoding au niveau octet
#  Projet ILIACode --- Pr. Asmaa RASSIL --- ENSA Fès --- ILIA3
#  Fichier à compléter pendant la séance, une fonction par partie du TP
# ============================================================
import re
from collections import Counter

# Le marqueur de fin de mot. Il n'est pas un octet, il ne peut donc jamais
# être confondu avec un caractère du texte.
FIN = "</w>"

# Les 256 symboles de base, un par valeur d'octet. L'octet b est représenté
# par le caractère de numéro b (règle Latin-1, un caractère par octet).
BASE = [chr(b) for b in range(256)]

# Étage 1, la pré-tokenisation. Les règles 2 à 5 de la séance 1 (nombres à
# virgule, opérateurs composés, mots, signes), plus les suites de blancs
# conservées (réversibilité), les tirets bas et le camelCase. La règle 1
# (chaîne ou commentaire gardé entier) n'est pas reprise, un commentaire
# entier serait un mot de cent octets que BPE ne pourrait jamais abréger.
MOTIF = r'\d+\.\d+|!=|<=|>=|\w+|\s+|[^\w\s]'
CAMEL = r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])"


def pretokeniser(texte):
    """Pose les frontières de mots. Un identifiant est coupé sur ses tirets bas
    (gardés comme tokens) et sur ses changements de casse."""
    mots = []
    for morceau in re.findall(MOTIF, texte):
        if re.fullmatch(r"\w+", morceau):
            for partie in re.split(r"(_)", morceau):      # garde les "_"
                if partie:
                    mots.append(partie)          # partie 2 du TP, à remplacer pour couper le camelCase
        else:
            mots.append(morceau)
    return mots


def en_octets(mot):
    """Écrit un mot comme suite de symboles de base, un par octet UTF-8,
    close par le marqueur de fin de mot."""
    return [chr(b) for b in mot.encode('utf-8')]+[FIN]

def longueur(symbole):
    """Nombre de symboles de base dans un symbole, le marqueur comptant pour un."""
    return len(symbole.replace(FIN, "#"))


def hexa(symboles):
    """Affiche une suite de symboles en hexadécimal, deux chiffres par octet,
    les octets d'un même symbole étant collés, pour la lecture."""
    morceaux = []
    for s in symboles:
        coeur = s.replace(FIN, "")
        h = "".join(f"{ord(c):02X}" for c in coeur)
        morceaux.append(h + (FIN if s.endswith(FIN) else ""))
    return " ".join(m for m in morceaux if m)


def compter_paires(corpus):
    """corpus = dictionnaire {suite de symboles (tuple) : fréquence du mot}.
    Renvoie le compte de chaque paire de symboles adjacents, pondéré par la
    fréquence des mots."""
    raise NotImplementedError("partie 3 du TP")
    counts={}
    for pair in zip(corpus, corpus[1:]):
        counts[pair]=counts.get(pair,0)+1


def fusionner_mot(paire, symboles):
    """Remplace, dans une suite de symboles, chaque paire (a, b) adjacente
    par le symbole unique ab."""
    raise NotImplementedError("partie 3 du TP")


def fusionner(paire, corpus):
    """Applique la fusion à tous les mots du corpus."""
    nouveau = {}
    for symboles, freq in corpus.items():
        s = fusionner_mot(paire, symboles)
        nouveau[s] = nouveau.get(s, 0) + freq
    return nouveau


def entrainer(mots, nb_fusions):
    """Phase 1. mots = Counter {mot : fréquence}. Renvoie la liste ordonnée
    des fusions et le vocabulaire V."""
    corpus = {tuple(en_octets(mot)): freq for mot, freq in mots.items()}
    fusions = []
    for _ in range(nb_fusions):
        raise NotImplementedError("partie 3 du TP, les trois gestes de la boucle")
    vocabulaire = set(BASE) | {FIN} | {a + b for a, b in fusions}
    return fusions, vocabulaire


def table_des_rangs(fusions):
    """Associe à chaque fusion apprise son rang dans la liste, 0 pour la première."""
    return {paire: rang for rang, paire in enumerate(fusions)}


def encoder_mot(mot, rangs):
    """Phase 2. Rejoue les fusions sur un mot, la plus anciennement apprise
    (rang le plus petit) d'abord, jusqu'à ce qu'aucune ne s'applique."""
    raise NotImplementedError("partie 4 du TP")


def encoder(texte, fusions):
    """Phase 2 sur un texte entier, mot par mot."""
    rangs = table_des_rangs(fusions)
    tokens = []
    for mot in pretokeniser(texte):
        tokens.extend(encoder_mot(mot, rangs))
    return tokens


def decoder(tokens):
    """Déplie chaque token en ses octets, relit en UTF-8, retire les marqueurs."""
    raise NotImplementedError("partie 5 du TP")


def fertilite(texte, fusions):
    """Nombre moyen de tokens par mot, les blancs n'étant pas des mots."""
    raise NotImplementedError("partie 6 du TP")
    mots = [m for m in pretokeniser(texte) if not m.isspace()]
    nb_tokens = sum(len(encoder_mot(m, rangs)) for m in mots)
    return nb_tokens / len(mots)
