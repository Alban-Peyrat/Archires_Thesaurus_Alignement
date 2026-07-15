# Alignement de 2 thésaurus

Basé sur le script créé pour aligner le thésaurus géographique de l'IPRAUS avec ceux d'ArchiRès

# Aligner les thésaurus géographique de l'IPRAUS avec ceux d'ArchiRès

Procédure pour aligner le thésaurus géographique de l'IPRAUS avec les deux thésaurus géographiques utilisés dans ArchiRès.

## Formatter les données de l'IPRAUS

* Récupérer le dernier export XML du thésaurus depuis l'accueil du module de gestion → contenu du répertoire AlineaTemp → sous-répertoire `exp` → dossier `thesaurus` → fichier _Thesaurus Géographique_ avec le plus grand nombre
* Utiliser l'application `Archires_Short_Single_Exec/AR641_IPRA_thes_Geo_toCSV.py` pour générer une version TSV

## Exporter les données ArchiRès de Koha

Exécuter et enregistrer le résultats des deux requêtes SQL suivantes :

``` SQL
-- A609
SELECT authid, ExtractValue(marcxml, '//datafield[@tag="215"]/subfield[@code="a"]') AS "prefLabel@fr" from auth_header WHERE authtypecode = "A609"
```

``` SQL
-- Sujet nom géographique
SELECT authid, ExtractValue(marcxml, '//datafield[@tag="215"]/subfield[@code="a"]') AS "prefLabel@fr" from auth_header WHERE authtypecode = "SNG"
```

## Processus d'alignement

Deux procédures existent pour procéder à l'alignement :

* [Procédure Heavy](#procédure-heavy-application-dédiée), plus précise et utilisant une application python dédiée
* [Procédure Light](#procédure-light-openrefine), moins précise mais plus accessible, utilisant OpenRefine

### Procédure Heavy (application dédiée)

Cette méthode utilise plusieurs manières d'identifier une autorité correspondante, de la plus précise à la plus large :

1. Match exact (`EXACT`)
2. Match sur fingerprint (`FINGERPRINT`)
3. Match sur fingerprint & suppression de mots-vides (`FINGERPRINT_STOP_WORDS`)
4. Match sur fingerprint & suppression de mots-vides & expressions type (province, Wilaya, etc.) (`FINGERPRINT_STOP_WORDS_EXTENDED`)
5. Match sur fingerprint en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS`)
6. Match sur fingerprint & suppression de mots-vides en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS_STOP_WORDS`)
7. Match sur fingerprint & suppression de mots-vides & expressions type (province, Wilaya, etc.) en enlevant avant les contenus entre parenthèse (`FINGERPRINT_NO_PARENTHESIS_STOP_WORDS_EXTENDED`)

#### Utiliser l'application

Utiliser **deux fois** l'application `Archires_Short_Single_Exec/AR643_compare_thes_geo.py`, pour les A609 et pour les SNG :

* Définir les variables d'environnement :
  * `AR643_EXTERNAL_THES_GEO_PATH` : chemin d'accès au fichier des données de l'IPRAUS formatté au début de cette procédure
  * `AR643_EXTERNAL_THES_GEO_DELIMITER` : `\t`
  * `AR643_EXTERNAL_THES_GEO_ID_COL` : `identifier`
  * `AR643_INTERNAL_THES_GEO_PATH` : chemin d'accès au fichier exporté de Koha pour la A609 / SNG (selon le thésaurus en cours de traitement)
  * `AR643_INTERNAL_THES_GEO_DELIMITER` : `;`
  * `AR643_INTERNAL_THES_GEO_ID_COL` : `authid`
  * `AR643_OUTPUT_PATH` : chemin d'accès pour le fichier de sortie
* Exécuter l'application

#### Fusionner les fichiers avec OpenRefine

_Note : export des opérations à la fin de la liste à puces_

* Lancer OpenRefine
* Créer un projet pour chacun des 2 fichiers (appelés `alignement archires A609` & `alignement archires SNG`)
* Dans le fichier `alignement archires A609`, renommer les colonnes suivantes :
  * `matched_internal_IDs` : `A609_matched_IDs`
  * `matched_internal_prefLabel@fr` : `A609_matched_prefLabel@fr`
  * `nb_match` : `A609_nb_match`
  * `STEP` : `A609_STEP`
  * `KEY_USED` : `A609_KEY_USED`
* Créer les colonnes suivantes basées sur la colonne `external_ID` :
  * `SNG_matched_IDs` avec l'expression GREL : `cell.cross("alignement archires SNG", "external_ID").cells["matched_internal_IDs"].value[0]`
  * `SNG_matched_prefLabel@fr` avec l'expression GREL : `cell.cross("alignement archires SNG", "external_ID").cells["matched_internal_prefLabel@fr"].value[0]`
  * `SNG_nb_match` avec l'expression GREL : `cell.cross("alignement archires SNG", "external_ID").cells["nb_match"].value[0]`
  * `SNG_STEP` avec l'expression GREL : `cell.cross("alignement archires SNG", "external_ID").cells["STEP"].value[0]`
  * `SNG_KEY_USED` avec l'expression GREL : `cell.cross("alignement archires SNG", "external_ID").cells["KEY_USED"].value[0]`
* Réordonner les colonnes pour afficher toutes les colonnes `SNG` après celles de l'A609, dans le même ordre

``` JSON
[
  {
    "op": "core/column-rename",
    "oldColumnName": "matched_internal_IDs",
    "newColumnName": "A609_matched_IDs",
    "description": "Renommer la colonne matched_internal_IDs} en A609_matched_IDs"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "matched_internal_prefLabel@fr",
    "newColumnName": "A609_matched_prefLabel@fr",
    "description": "Renommer la colonne matched_internal_prefLabel@fr} en A609_matched_prefLabel@fr"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "nb_match",
    "newColumnName": "A609_nb_match",
    "description": "Renommer la colonne nb_match} en A609_nb_match"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "STEP",
    "newColumnName": "A609_STEP",
    "description": "Renommer la colonne STEP} en A609_STEP"
  },
  {
    "op": "core/column-rename",
    "oldColumnName": "KEY_USED",
    "newColumnName": "A609_KEY_USED",
    "description": "Renommer la colonne KEY_USED} en A609_KEY_USED"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "external_ID",
    "expression": "grel:cell.cross(\"alignement archires SNG\", \"external_ID\").cells[\"matched_internal_IDs\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_matched_IDs",
    "columnInsertIndex": 1,
    "description": "Créer la colonne SNG_matched_IDs à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "external_ID",
    "expression": "grel:cell.cross(\"alignement archires SNG\", \"external_ID\").cells[\"matched_internal_prefLabel@fr\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_matched_prefLabel@fr",
    "columnInsertIndex": 1,
    "description": "Créer la colonne SNG_matched_prefLabel@fr à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "external_ID",
    "expression": "grel:cell.cross(\"alignement archires SNG\", \"external_ID\").cells[\"nb_match\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_nb_match",
    "columnInsertIndex": 1,
    "description": "Créer la colonne SNG_nb_match à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "external_ID",
    "expression": "grel:cell.cross(\"alignement archires SNG\", \"external_ID\").cells[\"STEP\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_STEP",
    "columnInsertIndex": 1,
    "description": "Créer la colonne SNG_STEP à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "external_ID",
    "expression": "grel:cell.cross(\"alignement archires SNG\", \"external_ID\").cells[\"KEY_USED\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_KEY_USED",
    "columnInsertIndex": 1,
    "description": "Créer la colonne SNG_KEY_USED à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-reorder",
    "columnNames": [
      "external_ID",
      "external_prefLabel@fr",
      "A609_matched_IDs",
      "A609_matched_prefLabel@fr",
      "A609_nb_match",
      "A609_STEP",
      "A609_KEY_USED",
      "SNG_matched_IDs",
      "SNG_matched_prefLabel@fr",
      "SNG_nb_match",
      "SNG_STEP",
      "SNG_KEY_USED"
    ],
    "description": "Reordonner les colonnes"
  }
]
```

### Procédure Light (OpenRefine)

Cette méthode est plus facile à appliquer, mais n'utilise pas une procédure de d'alignement graduée.

* Lancer OpenRefine
* Créer un projet pour chacun des 3 fichiers (appeler ceux d'ArchiRès `archires A609` & `archires SNG`)
* Dans chaque projet, créer une colonne `fingerprint` basée sur le `prefLabel@fr` avec l'expression GREL : `value.fingerprint()` :

``` JSON
[
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "prefLabel@fr",
    "expression": "grel:value.fingerprint()",
    "onError": "set-to-blank",
    "newColumnName": "fingerprint",
    "columnInsertIndex": 2,
    "description": "Créer la colonne fingerprint à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  }
]
```

* Dans le projet basé sur le thésaurus de l'IPRAUS, créer les colonnes suivantes basées sur la colonne `fingerprint` :
  * _Note : un export de ces 4 opérations est diponibles à la fin de la liste à puces_
  * `A609_nb_match` avec l'expression GREL : `length(cell.cross("archires A609", "fingerprint").cells["authid"].value)`
  * `A609_koha_authid` : `cell.cross("archires A609", "fingerprint").cells["authid"].value[0]`
  * `SNG_nb_match` avec l'expression GREL : `length(cell.cross("archires SNG", "fingerprint").cells["authid"].value)`
  * `SNG_koha_authid` : `cell.cross("archires SNG", "fingerprint").cells["authid"].value[0]`
* Puis réordonner les colonnes pour afficher d'abord le nombre de matchs puis l'ID qui a matché

``` JSON
[
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "fingerprint",
    "expression": "grel:length(cell.cross(\"archires A609\", \"fingerprint\").cells[\"authid\"].value)",
    "onError": "set-to-blank",
    "newColumnName": "A609_nb_match",
    "columnInsertIndex": 3,
    "description": "Créer la colonne A609_nb_match à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "fingerprint",
    "expression": "grel:cell.cross(\"archires A609\", \"fingerprint\").cells[\"authid\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "A609_koha_authid",
    "columnInsertIndex": 3,
    "description": "Créer la colonne A609_koha_authid à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "fingerprint",
    "expression": "grel:length(cell.cross(\"archires SNG\", \"fingerprint\").cells[\"authid\"].value)",
    "onError": "set-to-blank",
    "newColumnName": "SNG_nb_match",
    "columnInsertIndex": 3,
    "description": "Créer la colonne SNG_nb_match à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-addition",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "baseColumnName": "fingerprint",
    "expression": "grel:cell.cross(\"archires SNG\", \"fingerprint\").cells[\"authid\"].value[0]",
    "onError": "set-to-blank",
    "newColumnName": "SNG_koha_authid",
    "columnInsertIndex": 3,
    "description": "Créer la colonne SNG_koha_authid à lindex {1} sur la base de la colonne {2} à laide de lexpression {3}"
  },
  {
    "op": "core/column-reorder",
    "columnNames": [
      "identifier",
      "prefLabel@fr",
      "fingerprint",
      "A609_nb_match",
      "A609_koha_authid",
      "SNG_nb_match",
      "SNG_koha_authid",
      "broader@fr",
      "broader@ID",
      "scopeNote@fr",
      "altLabel@fr",
      "altLabel@en",
      "narrower@fr",
      "narrower@ID",
      "NB_OCCURRENCES"
    ],
    "description": "Reordonner les colonnes"
  }
]
```

## Ajout du nombre d'utilisations

* Extraire du fichier original de notices l'identifiant du thésaurus toutes les lignes qui sont des mots-clefs géographiques
* Faire un tableau croisé dynamique dans Excel avec en ligne l'identifiant et en valeur le nombre d'utilisation
* Exporter les données
* Dans OpenRefine, importer els données
* Importer dans le fichier final le nombre d'utilisations