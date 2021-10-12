Passtis
=======

This is a password dictionary generator for France, based on the format and
content I usually encounter during pentests in that particular country. Passtis
supports only common formats and remains a basic tool for those who don't want
to read the docs of complete and powerful dictionary generators.

> As this should be used mostly by french-speaking people, the rest of this
  README is in french (sorry :)).

Introduction
------------

Passtis permet de générer des dictionnaires de mots de passe selon des formats
récurrents en France, avec un contenu par défaut ou personnalisable, pour ceux
qui ont la flemme de faire des règles pour de meilleurs outils.

Pourquoi ? Après de nombreux tests d'intrusion internes, on se rend compte que :

* certains formats reviennent tout le temps et c'est ceux-là qu'on veut
  retrouver dans les dictionnaires de mots de passe qu'on génère pour faire du
  bruteforce ;

* les formats et sets de règles par défaut ou accessibles facilement sont très
  biens, mais pas exactement comme on voudrait ;

* on n'a pas le temps d'en faire des comme on voudrait sur le moment, et après
  on oublie (jusqu'au prochain).

Alors je pourrais m'embêter à faire un milliardième set de règles pour un outil,
mais je préfère faire un milliardième outil qui fait ce que je lui demande (et
surtout, comme je lui demande).

Usage
-----

```
$> python passtis.py -h
usage: passtis.py [-h] [-w words] [-f file] [-p postcode (69|69100)]
                  [-s specialchars] [-m] [-d] [-y] [-xc]

French password dictionary builder

optional arguments:
  -h, --help            show this help message and exit
  -w word(s), --words word(s)
                        Comma-separated word(s) to use
  -f file, --file file  File containing a list of words
  -p postcode (69|69100), --postcode postcode (69|69100)
                        Postcode to use (can also be "42,73")
  -s specialchars, --special specialchars
                        Special chars to use (can be empty string)
  -m, --month           Use months as base (in french)
  -d, --date            Use dates as suffix with format ddmmyy
  -y, --year            Use years as suffix with format yyyy
  -x, --nocombo        Do not build combined words with short words
```

### TL;DR

Pour utiliser Passtis de manière efficace:

1. Lors d'un test dans l'entreprise "superlama" située à Aubenas (07200), sur le
hash de l'administrateur système dont le fils s'appelle Killian et est né à
Saint-Etienne (42000):

```
python passtis.py -w "superlama,killian" -p07200,42000
```

2. Lors d'un test dans l'entreprise "dupoulet" située en Loire-Atlantique (44),
pour faire du bruteforce sur tous les comptes du domaine sans politique de
verrouillage (sans compter le test login = mot de passe) :

```
python passtis.py -w "dupoulet" -p44 -dmy
```

### Détails

Par défaut, je considère qu'une bonne grosse partie des mots de passe français
est constitué d'une **base** (no shit) à laquelle peuvent être ajoutées un
**suffixe** et/ou des **caractères spéciaux**. C'est sur ce principe que se base
Passtis, qui va générer des mots de passe qui ont les formats suivants :

```
(BASE, SUFFIX), # Bernard42
(BASE, SPECIALS), # Bernard*
(BASE, SUFFIX, SPECIALS), # Bernard42!
(BASE, SPECIALS, SUFFIX)  # Bernard@2021
```

Actuellement, les bases et les suffixes sont constitués d'un certain nombre de
types d'objets, activables ou modifiables avec les arguments :

```
BASE = WORDS + MONTHS
SUFFIX = NUM + YEARS + POSTCODES + DATES
```

Chaque base sera utilisée tel quel + en version capitalisée (ex: `En1mot`)

> D'autres types d'objets sont susceptibles d'être ajoutés si je pense à
  d'autres trucs ou si on me fait des suggestions.

#### Bases personnalisées

`WORDS` correspond à la liste des mots que vous aurez spécifiés manuellement ou
en donnant un fichier de mots.

```
$> python passtis.py -w en1mot,mot,en2mots,momots!
[...]
$> python passtis.py -f dico.txt
[...]
$> cat dico.txt
en1mot
mot
en2mots
momots!
```

Pour les mots inférieurs à 5 caractères, des versions "combinées" sont également
créées et intégrées au dictionnaire final. Ce comportement est désactivable avec
l'option `-x`.

Par exemple: `sql` et `user` produiront également des sorties `usersql` et
`sqluser`.

#### Bases prédéfinies

Vous pouvez utiliser des listes de mots prédéfinifies. Pour l'instant, l'option
`-m` permet d'utiliser également les mois comme base de mot de passe (`MONTHS`).
Ces listes peuvent être combinées avec les options `-w` et `-f`

#### Suffixes

Les suffixes sont les ajouts faits à cette base, entrecoupés ou non de
caractères spéciaux. Tous les sont désactivés par défaut à part `NUM` qui
consiste en une séquence de chiffres de 0 à 99, de 00 à 09 ainsi que des suites
type 123, 456, 789 puis de 1234 à 123456789 et de 0123 à 012356789.

> S'il vous manque un format de suffixe (ex : 987654321, vous pouvez l'ajouter
  en tant que mot (BASE) ou vous pouvez modifier le code directement :p

#### Caractères spéciaux

Finalement, il existe un set de caractères spéciaux par défaut, mais vous pouvez
les remplacer par les vôtres avec l'option `-s`:

```
$> python passtis.py -f dico.txt -s "!@"
```

Améliorations possibles
-----------------------

- [ ] Pouvoir choisir le format de la date (ex: ddmmyyyy)
- [ ] Pouvoir choisir l'intervalle de la date (par exemple, du 01012010 au 31122011)
- [ ] Choix de la taille minimum pour les combinaisons
- [ ] Pouvoir préciser une politique de mot de passe :
    - [ ] Longueur minimum
    - [ ] Présence de caractères spéciaux