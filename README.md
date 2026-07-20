# Alignement de 2 thésaurus

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Permet d'aligner 2 thésaurus en comparant le libellé des termes du thésaurus "externe" à ceux du thésaurus "interne".
Un même terme, identifié par son identifiant, peut avoir un ou plusieurs labels préférentiels ainsi qu'autant de label alternatifs que nécessaire, ou aucun.

Basé sur le script créé pour aligner le thésaurus géographique de l'IPRAUS avec ceux d'ArchiRès.

## Fonctionnement

Ce script peut utiliser plusieurs étapes pour aligner des autorités :

* [100] Match exact (`EXACT`)
* [2XX] Suite [normalisée](#normalisation) :
  * [200] Match simple (`NORMALIZED`)
  * [230] Match simple avec suppression de mots-vides (`NORMALIZED_STOP_WORDS`)
  * [261] Match simple avec suppression de mots-vides & suppression étendue de mots (`NORMALIZED_STOP_WORDS_EXTENDED`)
* [3XX] Suite [normalisée](#normalisation) avec suppression des contenus entre parenthèses :
  * [300] Match simple (`NORMALIZED_NO_PARENTHESIS`)
  * [330] Match simple avec suppression de mots-vides (`NORMALIZED_NO_PARENTHESIS_STOP_WORDS`)
  * [361] Match simple avec suppression de mots-vides & suppression étendue de mots (`NORMALIZED_NO_PARENTHESIS_STOP_WORDS_EXTENDED`)
* [4XX] Suite [fingerprint](#fingerprint) :
  * [400] Match simple (`FINGERPRINT_REORDERED`)
  * [430] Match simple avec suppression de mots-vides (`FINGERPRINT_REORDERED_STOP_WORDS`)
  * [461] Match simple avec suppression de mots-vides & suppression étendue de mots  (`FINGERPRINT_REORDERED_STOP_WORDS_EXTENDED`)

Lors de [l'exécution de l'application](#utiliser-lapplication), l'utilisateur choisit les étapes qu'il souhaite utiliser et leur ordre d'exécution.

_Note technique : toutes les étapes utilisants des suppressions étendues de mots doivent avoir un identifiant terminant en `1`_

### Normalisation

1. Passe en miniscule
1. `&` devient `et`
1. `œ` devient `oe`
1. Suppression des diacritiques
1. Remplace le bruit par des espaces : `[\x21-\x2F]|[\x3A-\x40]|[\x5B-\x60]|[\x7B-\x7F]|[\u2010-\u2015]|\.|\,|\?|\!|\;|\/|\:|\=|\[|\]|\'|\-|\(|\)|\||\"|\<|\>|\+|\°`
1. Remplace les multiples espaces par un seul espace

### Suppression de mots-vides

Supprime toutes les occurrences de chacun des [mots-vides du Sudoc](https://documentation.abes.fr/sudoc/manuels/interrogation/mots_vides/index.html#ListeMotsVidesAutresIndex) (version de fin 2023 je crois) et des opérateurs booléen de CBS (_All CBS Command_ Version 6 (2014-02-11), j'ai une copie de la page mais plus le lien original).

### Suppression étendue de mots

Supprime toutes les occurrences de chacun des termes présents dans [le fichier fourni](#fichier-attendu-pour-la-suppression-étendue-de-mots).

### Fingerprint

1. [Normalise](#normalisation)
1. Supprime les mots dupliqués
1. Réordonne les mots par ordre alphabétique

## Utiliser l'application

* Préparer [les fichiers attendus](#fichiers-de-thésaurus-attendus)
* Définir les variables d'environnement :
  * `EXTERNAL_THES_PATH` : chemin d'accès au fichier contenant le thésaurus "externe"
  * `EXTERNAL_THES_DELIMITER` : séparateur utilisé dans le fichier contenant le thésaurus "externe"
  * `EXTERNAL_THES_ID_COL` : nom de la colonne contenant l'identifiant dans le fichier contenant le thésaurus "externe"
  * `INTERNAL_THES_PATH` : chemin d'accès au fichier contenant le thésaurus "interne"
  * `INTERNAL_THES_DELIMITER` : séparateur utilisé dans le fichier contenant le thésaurus "interne"
  * `INTERNAL_THES_ID_COL` : nom de la colonne contenant l'identifiant dans le fichier contenant le thésaurus "interne"
  * `EXTENDED_WORDS_LIST` : [facultatif] chemin d'accès au fichier contenant la liste des termes à supprimer dans les étapes `_EXTENDED`
  * `OUTPUT_PATH` : chemin d'accès pour le fichier de sortie contenant toutes les formes
  * `OUTPUT_SYNTHESIS_PATH` : chemin d'accès pour le fichier de sortie qui synthètise par identifiant
* Exécuter l'application (`main.py`)

Exemple de variables d'environnement :

```
EXTERNAL_THES_PATH="C:\Path\Archires_Thesaurus_Alignement\files\A609_refined.csv"
EXTERNAL_THES_DELIMITER=";"
EXTERNAL_THES_ID_COL="authid"
INTERNAL_THES_PATH="C:\Path\Archires_Thesaurus_Alignement\files\SNG_refined.csv"
INTERNAL_THES_DELIMITER=";"
INTERNAL_THES_ID_COL="authid"
STEPS="100,200,230,261,300,330,361,400,430,461"
EXTENDED_WORDS_LIST="C:\Path\Archires_Thesaurus_Alignement\other\extended_words_geo_archires.txt"
OUTPUT_PATH="C:\Path\Archires_Thesaurus_Alignement\files\results.csv"
OUTPUT_SYNTHESIS_PATH="C:\Path\Archires_Thesaurus_Alignement\files\synthesis.csv"
```

## Fichiers de thésaurus attendus

Chaque thésaurus doit être contenu dans un fichier tabulé respectant les conditions suivantes :

* Contient au moins ces 3 colonnes :
  * Une avec l'identifiant du terme (nom personnalisable, à renseigner dans `EXTERNAL_THES_ID_COL` / `INTERNAL_THES_ID_COL`)
  * _prefLabel_ : contient un label préférentiel pour le terme avec cet identifiant
  * _altLabel_ : contient un label préférentiel pour le terme avec cet identifiant
* Le délimiteur est personnalisable (à renseigner dans `EXTERNAL_THES_DELIMITER` / `INTERNAL_THES_DELIMITER`)
* Une ligne doit contenir un identifiant, mais peut contenir un label préférentiel et / ou un label alternatif
  * Exemples : `123;Paris;Paris (France)`, `123;Paris;`, `123;;Paris (France)`, `123;;`
* Un identifiant peut apparaître sur autant de ligne que nécessaire

## Exemple de génération de fichiers de thésaurus à partir de Koha

_Note : exemple pour un export de notices d'autorités géographiques, avec le label préférentiel en `215` et le label alternatif en `415`_

* Exporter depuis Koha toutes les notices d'autorités d'un type d'autorité au format MARC (module _Catalogage_ → _Exporter_ → _Exporter les données du catalogue_)
* Dans MARCEdit, effectuer un export tabulé basé sur ce fichier selon la configuration suivante :
  * Changer le _In field delimiter_ en `###`
  * Exporter les champs : `001`, `215`, `415`
  * _Note : exporter tout le champs, pas seulement un sous-champ_
* Dans OpenRefine, importer le fichier **en pensant à renseigner _Use character `"` to enclose cells containing column separators_**
* Appliquer les opérations présentes dans le fichier [`other/OpenRefine_exemple_generation_fichier.json`](./other/OpenRefine_exemple_generation_fichier.json), ou sinon, manuellement :
    1. Colonne _215_ : _Edit cells_ → _Split multi-valued cells..._ puis choisir _by separator_ avec la valeur `###`
    1. Colonne _415_ : même opération que pour la colonne _215_
    1. Colonne _215_ : _Edit cells_ → _Transform..._ avec l'expression GREL : `value.strip().substring(2).replace(/\$[^axyz].+?(?=\$)/, "").replace(/\$./, " ").split(" ").join(" ")`
        * Supprime les espaces en début et fin, reture les indicateurs, supprime les sous champs qui ne sont pas `$a`, `$x`, `$y` ou `$z`, remplace les indicateurs de sous-champs (ex : `$a`) par un espace, retire les espaces inutiles
    1. Colonne _415_ : même opération que pour la colonne _215_
    1. Colonne _001_ : _Edit cells_ → _Fill down_
    1. Colonne _001_ : renommer en _authid_
    1. Colonne _215_ : renommer en _prefLabel_
    1. Colonne _415_ : renommer en _altLabel_
* Exporter le fichier en _Custom tabular..._ :
  * Vérifier que _Output column headers_ est coché dans l'onglet _Content_
  * Dans l'onglet _Download_, cocher _Custom separator_ et indiquer la valeur `;`
  * Vérifier que la avleur dans _Line separator_ est `\n`
  * Cocher _Always quote text_

## Fichier attendu pour la suppression étendue de mots 

* Un terme par ligne
* Les termes doivent être :
  * En minuscule
  * Sans diacritique
  * Les tirets, apostrophes et autres sont remplacés par un espace
  * Les termes peuvent être composé de plusieurs mots, mais séparés par un seul espace