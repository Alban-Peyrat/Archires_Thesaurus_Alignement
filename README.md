# Alignement de 2 thésaurus

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Permet d'aligner 2 thésaurus en comparant le libellé des termes du thésaurus "externe" à ceux du thésaurus "interne".
Un même terme, identifié par son identifiant, peut avoir un ou plusieurs labels préférentiels ainsi qu'antant de label alternatifs que nécessiare, ou aucun.

Basé sur le script créé pour aligner le thésaurus géographique de l'IPRAUS avec ceux d'ArchiRès

## Fonctionnement

Cette méthode utilise plusieurs manières d'identifier une autorité correspondante, de la plus précise à la plus large :

* [100] Match exact (`EXACT`)
* [200] Match sur fingerprint (`FINGERPRINT`)
* [230] Match sur fingerprint & suppression de mots-vides (`FINGERPRINT_STOP_WORDS`)
* [260] Match sur fingerprint & suppression de mots-vides & expressions type (province, Wilaya, etc.) (`FINGERPRINT_STOP_WORDS_EXTENDED`)
* [300] Match sur fingerprint en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS`)
* [330] Match sur fingerprint & suppression de mots-vides en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS_STOP_WORDS`)
* [360] Match sur fingerprint & suppression de mots-vides & expressions type (province, Wilaya, etc.) en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS_STOP_WORDS_EXTENDED`)
* [400] Match sur fingerprint en réordonnant les mots et supprimant les mots doubles (`FINGERPRINT_REORDERED`)
* [430] Match sur fingerprint en réordonnant les mots et supprimant les mots doubles & suppression de mots-vides en enlevant avant les contenus entre parenthèse (`FINGERPRINT_REORDERED_STOP_WORDS`)
* [460] Match sur fingerprint en réordonnant les mots et supprimant les mots doubles & suppression de mots-vides & expressions type (province, Wilaya, etc.) en enlevant avant les contenus entre parenthèse (`FINGERPRINT_REORDERED_STOP_WORDS_EXTENDED`)


## Utiliser l'application

* Préparer [les fichiers attendus](#fichiers-attendus)
* Définir les variables d'environnement :
  * `EXTERNAL_THES_PATH` : chemin d'accès au fichier contenant le thésaurus "externe"
  * `EXTERNAL_THES_DELIMITER` : séparateur utilisé dans le fichier contenant le thésaurus "externe"
  * `EXTERNAL_THES_ID_COL` : nom de la colonne contenant l'identifiant dans le fichier contenant le thésaurus "externe"
  * `INTERNAL_THES_PATH` : chemin d'accès au fichier contenant le thésaurus "interne"
  * `INTERNAL_THES_DELIMITER` : séparateur utilisé dans le fichier contenant le thésaurus "interne"
  * `INTERNAL_THES_ID_COL` : nom de la colonne contenant l'identifiant dans le fichier contenant le thésaurus "interne"
  * `OUTPUT_PATH` : chemin d'accès pour le fichier de sortie
* Exécuter l'application (`main.py`)

## Fichiers attendus

Chaque thésaurus doit être contenu dans un fichier tabulé respectant les conditions suivantes :

* Contient au moins ces 3 colonnes :
  * Une avec l'identifiant du terme (nom personnalisable, à renseigner dans `EXTERNAL_THES_ID_COL` / `INTERNAL_THES_ID_COL`)
  * _prefLabel_ : contient un label préférentiel pour le terme avec cet identifiant
  * _altLabel_ : contient un label préférentiel pour le terme avec cet identifiant
* Le délimiteur est personnalisable (à renseigner dans `EXTERNAL_THES_DELIMITER` / `INTERNAL_THES_DELIMITER`)
* Une ligne doit contenir un identifiant, mais peut contenir un label préférentiel et / ou un label alternatif
  * Exemples : `123;Paris;Paris (France)`, `123;Paris;`, `123;;Paris (France)`, `123;;`
* Un identifiant peut apparaître sur autant de ligne que nécessaire

## Exemple de génération de fichiers à partir de Koha

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
