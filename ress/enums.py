# -*- coding: utf-8 -*- 

# Etxernal import
from enum import Enum

class Step(Enum):
    EXACT = 0
    FINGERPRINT = 1
    FINGERPRINT_STOP_WORDS = 2
    FINGERPRINT_STOP_WORDS_EXTENDED = 3
    FINGERPRINT_NO_PARENTHESIS = 4
    FINGERPRINT_NO_PARENTHESIS_STOP_WORDS = 5
    FINGERPRINT_NO_PARENTHESIS_STOP_WORDS_EXTENDED = 6

class TSV_Headers(Enum):
    EXT_ID = "external_ID"
    EXT_NAME = "external_label"
    EXT_IS_PREF = "is_prefLabel"
    INT_ID = "matched_internal_IDs"
    INT_NAMES = "matched_internal_label@fr"
    NB_MATCH = "nb_match"
    STEP = "STEP"
    KEY_USED = "KEY_USED"