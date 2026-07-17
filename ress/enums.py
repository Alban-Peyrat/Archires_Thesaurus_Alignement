# -*- coding: utf-8 -*- 

# Etxernal import
from enum import Enum

class Step(Enum):
    EXACT = 100
    FINGERPRINT = 200
    FINGERPRINT_STOP_WORDS = 230
    FINGERPRINT_STOP_WORDS_EXTENDED = 260
    FINGERPRINT_NO_PARENTHESIS = 300
    FINGERPRINT_NO_PARENTHESIS_STOP_WORDS = 330
    FINGERPRINT_NO_PARENTHESIS_STOP_WORDS_EXTENDED = 360
    # FINGERPRINT_REORDERED = 400
    # FINGERPRINT_REORDERED_STOP_WORDS = 430
    # FINGERPRINT_REORDERED_STOP_WORDS_EXTENDED = 460

class TSV_Headers(Enum):
    EXT_ID = "external_ID"
    EXT_NAME = "external_label"
    EXT_IS_PREF = "is_prefLabel"
    INT_ID = "matched_internal_IDs"
    INT_NAMES = "matched_internal_label"
    NB_MATCH = "nb_match"
    STEP = "STEP"
    KEY_USED = "KEY_USED"

class TSV_Synthesis_Headers(Enum):
    EXT_ID = "external_ID"
    EXT_PREFLABEL = "external_prefLabel"
    EXT_ALTLABEL = "external_altLabel"
    INT_ID = "matched_internal_IDs"
    INT_PREFLABEL = "matched_internal_prefLabels"
    INT_ALTLABEL = "matched_internal_altLabels"
    NB_MATCH = "nb_match"
    STEP = "Most precise Step"