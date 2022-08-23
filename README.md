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

TL;DR
-----

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

> Lorsqu'on indique un code postal incomplet, tous les codes postaux qui
  commencent par cette valeur listés dans le fichier CSV
  `postcode_insee_20210923.csv` sont utilisés pour générer des mots de
  passe. Ici, tous les mots de passe seront générés avec tous les codes postaux
  du département 44.

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

Détails
-------

Par défaut, je considère qu'une bonne partie des mots de passe français
est constituée d'une **base** (no shit) à laquelle peuvent être ajoutés un
**suffixe** et/ou des **caractères spéciaux**. C'est sur ce principe que repose
Passtis, qui va générer des mots de passe qui ont les formats suivants :

```
(BASE, SUFFIX), # Bernard42
(BASE, SPECIALS), # Bernard*
(BASE, SUFFIX, SPECIALS), # Bernard42!
(BASE, SPECIALS, SUFFIX)  # Bernard@2021
```

> Les formats ne sont pas modifiables en ligne de commande mais il est possible
  de commenter ceux qui ne vous intéressent pas dans le code.


Actuellement, les bases et les suffixes sont constitués d'un certain nombre de
types d'objets, activables ou modifiables avec les arguments :

```
BASE = WORDS + MONTHS
SUFFIX = NUM + YEARS + POSTCODES + DATES
SPECIALS
```

> D'autres types d'objets sont susceptibles d'être ajoutés si je pense à
  d'autres trucs ou si on me fait des suggestions.
  
### BASE

Une base est un mot issu d'une liste prédéfinie et/ou spécifiée par
l'utilisateur.  Les listes peuvent être combinées.


* **MONTHS** est une liste prédéfinie de mois (en français), activable avec `-m`
* **WORDS** correspond à une liste de mots définis par l'utilisateur, passée via
  un fichier (`-f`) et/ou directement en argument (`-w`). Les deux options
  sont combinables. Une liste peut ne comporter qu'un seul mot.

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

Pour chaque possibilité de mot de passe généré, une base est utilisée deux fois :

1. Tel quel (`en1mot42`)
2. En version capitalisée (`En1mot42`)

Pour les mots inférieurs à 5 caractères, des versions "combinées" sont également
créées et intégrées au dictionnaire final. Ce comportement est désactivable avec
l'option `-x`.

Par exemple: `sql` et `user` produiront également des sorties `usersql` et
`sqluser`.


### SUFFIX

Les suffixes sont les ajouts faits à la base, entrecoupés ou non de
caractères spéciaux. Seul le suffixe `NUM` est activé par défaut.

* **NUM** : Séquence de chiffres de 0 à 99, de 00 à 09 et suites de chiffres :
  123, 456, 789 puis de 1234 à 123456789 et de 0123 à 012356789.
* **YEARS** : Années de 1970 à 2022, activable avec `-y`.
* **DATES** : Dates au format JJMMYY depuis le 01/01/1970 jusqu'au
  31/12/2022, activable avec `-d`.
* **POSTCODES** : Codes postaux français selon la liste de l'INSEE. Utilisable
  avec l'option `-p <code>` : tous les codes postaux commençant par la valeur
  spécifiée seront utilisés (ex: `-p 69` ajoutera tous les départements du Rhône
  en tant que suffixe, `-p 69100` n'ajoutera que le code postal 69100).

> Pour modifier les intervalles de dates, les formats ou s'il vous manque un
  format de suffixe (ex : 987654321, il est pour l'instant nécessaire de
  modifier le code directement.

### SPECIALS

Cela correspond aux caractères spéciaux. Il existe un set de caractères spéciaux
par défaut, mais vous pouvez les remplacer par les vôtres avec l'option `-s`:

```
$> python passtis.py -f dico.txt -s "!@"
```

Notes sur l'utilisation de Passtis
----------------------------------

1. **C'est meilleur avec des glaçons**, mais ça reste mauvais parce qu'il y a de
   l'anis dedans.

2. **N'oubliez pas de tester le cas login == password**. Il est conseillé
   de mettre le login dans la liste des BASES pour que ce test soit inclus dans
   le dictionnaire de mots de passe généré par Passtis.

3. **Attention, le nombre de mots de passe générés peut vite devenir très
   important**. En particulier, l'option `-d` (dates) génère énormément de
   résultats. Voici quelques indicateurs du nombre de mot de passe générés selon
   les options fournies :


   ```
   # Un seul mot, seulement deux caractères spéciaux choisis, aucune autre option
   $> python passtis.py -w pingouin -s '@!' | wc -l
   1255
   
   # Un seul mot, aucune autre option
   $> python passtis.py -w pingouin | wc -l
   5773

   # Un seul mot, utilisation des codes postaux du département 69
   $> python passtis.py -w pingouin -p69 | wc -l
   21735

   # Deux mots, ajout de la liste des mois en tant que base
   $> python passtis.py -w pingouin,lama -m | wc -l
   80822

   # Un seul mot, options date, mois et années activées
   $> python passtis.py -w pingouin -dmy | wc -l
   11682229   
   ```

Améliorations possibles
-----------------------

- [ ] Pouvoir choisir le format de la date (ex: ddmmyyyy)
- [ ] Pouvoir choisir l'intervalle de la date (par exemple, du 01012010 au 31122011)
- [ ] Choix de la taille minimum pour les combinaisons
- [ ] Pouvoir préciser une politique de mot de passe :
    - [ ] Longueur minimum
    - [ ] Présence de caractères spéciaux
