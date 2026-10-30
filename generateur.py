#!/usr/bin/env python3

# Copyright (c) 2026 Apocrate-arto
# SPDX-License-Identifier: CECILL-2.1
#
# Générateur de mots de passe sécurisé pour Linux.
#
# Ce logiciel est régi par la licence CeCILL version 2.1,
# soumise au droit français.
#
# Vous pouvez utiliser, modifier et redistribuer ce logiciel
# conformément aux conditions de cette licence.
#
# Le texte intégral se trouve dans le fichier LICENSE.
# https://cecill.info/

"""Générateur de mots de passe sécurisé pour le terminal Linux."""

import argparse
import math
import os
import secrets
import string
import sys


CARACTERES_SPECIAUX = r"!@#$%&*?~-_=+^µàçù([/\])"
CARACTERES_SIMILAIRES = "0O1lI()"
LONGUEUR_MAXIMALE = 4096
NOMBRE_MAXIMAL = 100
ALEATOIRE = secrets.SystemRandom()

COULEURS_ACTIVES = sys.stdout.isatty() and "NO_COLOR" not in os.environ
COULEURS = {
    "vert": "\033[92m",
    "jaune": "\033[93m",
    "rouge": "\033[91m",
    "bleu": "\033[94m",
    "cyan": "\033[96m",
    "gras": "\033[1m",
    "fin": "\033[0m",
}


def colorer(texte, couleur):
    """Mettre le texte en couleur si le terminal le permet."""
    if not COULEURS_ACTIVES:
        return str(texte)
    return f"{COULEURS[couleur]}{texte}{COULEURS['fin']}"


def demander_entier(question, minimum, maximum, valeur_defaut):
    """Lire un nombre entier et vérifier ses limites."""
    while True:
        reponse = input(question).strip()
        if not reponse:
            return valeur_defaut
        try:
            nombre = int(reponse)
        except ValueError:
            print(colorer("Entre un nombre entier.", "rouge"))
            continue
        if minimum <= nombre <= maximum:
            return nombre
        print(colorer(f"Choisis un nombre entre {minimum} et {maximum}.", "rouge"))


def demander_oui_non(question, valeur_defaut):
    """Lire une réponse oui/non (Entrée = valeur par défaut)."""
    while True:
        reponse = input(question).strip().lower()
        if not reponse:
            return valeur_defaut
        if reponse in ("o", "oui"):
            return True
        if reponse in ("n", "non"):
            return False
        print(colorer("Réponds par o ou n.", "rouge"))


def choisir_groupes(avec_speciaux, sans_similaires):
    """Préparer les catégories de caractères autorisés."""
    groupes = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if avec_speciaux:
        groupes.append(CARACTERES_SPECIAUX)
    if sans_similaires:
        groupes = [
            "".join(caractere for caractere in groupe
                    if caractere not in CARACTERES_SIMILAIRES)
            for groupe in groupes
        ]
    return groupes


def generer_mot_de_passe(longueur, groupes):
    """Garantir au moins un caractère de chaque catégorie."""
    if longueur < len(groupes):
        raise ValueError(f"La longueur doit être d'au moins {len(groupes)}.")

    caracteres = [secrets.choice(groupe) for groupe in groupes]
    alphabet = "".join(groupes)
    caracteres.extend(
        secrets.choice(alphabet) for _ in range(longueur - len(caracteres))
    )
    ALEATOIRE.shuffle(caracteres)
    return "".join(caracteres)


def evaluer_robustesse(longueur, groupes):
    """Donner un indicateur théorique (pas un audit de sécurité)."""
    bits = longueur * math.log2(sum(map(len, groupes)))
    if bits < 50:
        return "Faible", "rouge", bits
    if bits < 80:
        return "Moyen", "jaune", bits
    if bits < 120:
        return "Fort", "vert", bits
    return "Très fort", "vert", bits


def afficher_resultats(nombre, longueur, avec_speciaux,
                       sans_similaires):
    """Générer et afficher les mots de passe et leur robustesse."""

    groupes = choisir_groupes(avec_speciaux, sans_similaires)
    minimum = len(groupes)

    if not minimum <= longueur <= LONGUEUR_MAXIMALE:
        raise ValueError(
            f"La longueur doit être comprise entre {minimum} "
            f"et {LONGUEUR_MAXIMALE}."
        )

    if not 1 <= nombre <= NOMBRE_MAXIMAL:
        raise ValueError(
            f"Le nombre doit être entre 1 et {NOMBRE_MAXIMAL}."
        )

    niveau, couleur, bits = evaluer_robustesse(
        longueur, groupes
    )

    deja_generes = set()

    print("\n" + colorer(
        "═══ MOTS DE PASSE GÉNÉRÉS ═══", "cyan"
    ))

    for index in range(1, nombre + 1):

        while True:
            mot_de_passe = generer_mot_de_passe(
                longueur, groupes
            )

            if mot_de_passe not in deja_generes:
                break

        deja_generes.add(mot_de_passe)

        print(
            f"{index:>3}. {mot_de_passe}  "
            f"[{colorer(niveau, couleur)}]"
        )

    print(
        f"\nRobustesse indicative : {niveau} "
        f"(environ {bits:.0f} bits théoriques)."
    )

    print()


def menu_interactif():
    """Afficher un menu coloré qui permet de relancer plusieurs générations."""
    while True:
        print(colorer("\n╔═══════════════════════════════════════╗", "cyan"))
        print(colorer("║    GÉNÉRATEUR DE MOTS DE PASSE        ║", "cyan"))
        print(colorer("╚═══════════════════════════════════════╝", "cyan"))
        print("  1. Générer des mots de passe")
        print("  2. Quitter")
        choix = input("\nTon choix [1] : ").strip() or "1"
        if choix == "2":
            print(colorer("Au revoir !", "bleu"))
            return
        if choix != "1":
            print(colorer("Choix inconnu : tape 1 ou 2.", "rouge"))
            continue

        nombre = demander_entier(
            "Combien de mots de passe ? [1] : ", 1, NOMBRE_MAXIMAL, 1
        )
        avec_speciaux = demander_oui_non(
            "Inclure les caractères spéciaux ? (o/n) [o] : ", True
        )
        sans_similaires = demander_oui_non(
            "Exclure 0, O, 1, l et I ? (o/n) [o] : ", True
        )
        longueur = demander_entier(
            f"Longueur (minimum {4 if avec_speciaux else 3}) [20] : ",
            4 if avec_speciaux else 3, LONGUEUR_MAXIMALE, 20
        )
        afficher_resultats(nombre, longueur, avec_speciaux,
                           sans_similaires)


def principal():
    global COULEURS_ACTIVES

    analyseur = argparse.ArgumentParser(
        description="Générateur sécurisé de mots de passe pour Linux"
    )
    analyseur.add_argument(
        "-l", "--longueur", type=int, default=20,
        help="longueur du mot de passe (20 par défaut)"
    )
    analyseur.add_argument(
        "-n", "--nombre", type=int, default=1,
        help="nombre de mots de passe (1 par défaut, maximum 100)"
    )
    choix_speciaux = analyseur.add_mutually_exclusive_group()
    choix_speciaux.add_argument(
        "--avec-speciaux", action="store_true",
        help="autoriser les caractères spéciaux"
    )
    choix_speciaux.add_argument(
        "--sans-speciaux", action="store_true",
        help="ne pas utiliser de caractères spéciaux (défaut)"
    )
    analyseur.add_argument(
        "--sans-similaires", action="store_true",
        help="exclure les caractères 0, O, 1, l et I"
    )
    analyseur.add_argument(
        "--sans-couleurs", action="store_true",
        help="désactiver les couleurs dans le terminal"
    )
    arguments = analyseur.parse_args()
    if arguments.sans_couleurs:
        COULEURS_ACTIVES = False

    if len(sys.argv) == 1:
        try:
            menu_interactif()
        except (KeyboardInterrupt, EOFError):
            print("\nInterruption : fermeture du programme.")
        return

    try:
        afficher_resultats(
            arguments.nombre,
            arguments.longueur,
            arguments.avec_speciaux,
            arguments.sans_similaires,
        )
    except ValueError as erreur:
        analyseur.error(str(erreur))


if __name__ == "__main__":
    principal()
