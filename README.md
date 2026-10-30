# Générateur de mots de passe Linux

Générateur de mots de passe aléatoires et sécurisés
pour Linux, développé en Python 3.

Interface et documentation en français.

## Fonctionnalités

- Génération de plusieurs mots de passe
- Longueur personnalisable
- Caractères spéciaux facultatifs
- Exclusion des caractères similaires
- Indicateur de robustesse
- Menu interactif avec couleurs
- Utilisation en ligne de commande
- Aucune dépendance Python externe

## Prérequis

- Linux
- Python 3

## Installation

Télécharger le fichier `generateur.py`, puis exécuter :

```bash
chmod +x generateur.py
```

## Utilisation

Menu interactif :

```bash
./generateur.py
```

Générer 3 mots de passe de 20 caractères avec symboles ASCII classiques :

```bash
./generateur.py -n 3 -l 20 --avec-speciaux
```

Générer 3 mots de passe de 20 caractères avec symboles classiques et étendus :

```bash
./generateur.py -n 3 -l 20 --avec-speciaux --avec-etendus
```

Exclure les caractères similaires :

```bash
./generateur.py -n 3 -l 20 --avec-speciaux --sans-similaires
```

Afficher l'aide :

```bash
./generateur.py --help
```

## Sécurité

Le programme utilise la bibliothèque Python `secrets`
pour générer des mots de passe aléatoires.

L'indicateur de robustesse est une estimation
théorique et non une garantie de sécurité.

Les mots de passe sont affichés dans le terminal,
mais ne sont pas enregistrés par le programme.

## Licence

Ce projet est distribué sous licence CeCILL 2.1.

Consultez le fichier LICENSE.

Site officiel : https://cecill.info/

## Auteur

Apocrate-arto

https://github.com/Apocrate-arto
