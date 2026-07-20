# -*- coding: utf-8 -*- 

# Etxernal import
from typing import List, Dict
# Internal import
from ress.enums import Step
from ress.func_string_manip import fingerprint

class Term(object):
    # def __init__(self, id:str, pref_label:str): #original
    def __init__(self, id:str, label:str, extended_words:List[str]):
        self.id = id
        # self.pref_label = pref_label #original
        self.label = label
        self.forms:Dict[Step, str] = {}
        self.forms[Step.EXACT] = self.label
        self.forms[Step.NORMALIZED] = fingerprint(self.label)
        self.forms[Step.NORMALIZED_STOP_WORDS] = fingerprint(self.label, stop_words=True)
        self.forms[Step.NORMALIZED_STOP_WORDS_EXTENDED] = fingerprint(self.label, stop_words=True, stop_words_extended=extended_words)
        self.forms[Step.NORMALIZED_NO_PARENTHESIS] = fingerprint(self.label, no_parenthesis=True)
        self.forms[Step.NORMALIZED_NO_PARENTHESIS_STOP_WORDS] = fingerprint(self.label, stop_words=True, no_parenthesis=True)
        self.forms[Step.NORMALIZED_NO_PARENTHESIS_STOP_WORDS_EXTENDED] = fingerprint(self.label, stop_words=True, stop_words_extended=extended_words, no_parenthesis=True)
        self.forms[Step.FINGERPRINT] = fingerprint(self.label, reorder=True)
        self.forms[Step.FINGERPRINT_STOP_WORDS] = fingerprint(self.label, stop_words=True, reorder=True)
        self.forms[Step.FINGERPRINT_STOP_WORDS_EXTENDED] = fingerprint(self.label, stop_words=True, stop_words_extended=extended_words, reorder=True)

class Metaterm(object):
    def __init__(self, id:str):
        self.id = id
        self.pref_labels:List[Term] = []
        self.alt_labels:List[Term] = []
    
    def get_label(self, is_pref:bool=True) -> str:
        """Returns all pref labels as a string"""
        separator = " $$$ "
        if is_pref:
            return separator.join([term.label for term in self.pref_labels])
        return separator.join([term.label for term in self.alt_labels])