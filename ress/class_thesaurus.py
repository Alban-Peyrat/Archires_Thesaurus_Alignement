# -*- coding: utf-8 -*- 

# Etxernal import
from typing import List, Dict
import csv
# Internal import
from ress.enums import Step
from ress.class_terms import Metaterm, Term

class Thesaurus(object):
    def __init__(self, file_path:str, delimiter:str, id_col_name:str):
        self.file_path:str = file_path
        self.delimiter:str = delimiter
        # Makes sure that escaped strigns are not escaped
        if "\\" in self.delimiter:
            self.delimiter = self.delimiter.encode("latin-1", "backslashreplace").decode("unicode-escape")
        self.id_col_name:str = id_col_name
        # self.term_index:dict[str, Term] = {} # orignal one
        self.term_index:dict[str, Metaterm] = {}
        self.indexes:Dict[Step, Dict[str, List[str]]] = {}
        for step in Step:
            self.indexes[step] = {}
        # read data from the file
        with open(self.file_path, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f, delimiter=self.delimiter)
            for row in csv_reader:
                self.add_term(row[self.id_col_name], row["prefLabel@fr"], row["altLabel@fr"])
                # term = Term(row[self.id_col_name], row["prefLabel@fr"])
                # # Add the term to the ID-Term index
                # self.term_index[term.id] = term
        # Add each form to its index
        for id in list(self.term_index.keys()):
            for pref_label_term in self.term_index[id].pref_labels:
                self.__add_label_to_specific_indexes(pref_label_term)
            for alt_label_term in self.term_index[id].alt_labels:
                self.__add_label_to_specific_indexes(alt_label_term)

    def __add_label_to_specific_indexes(self, term:Term):
        for step in term.forms:
            temp_index:Dict[str, List[str]] = self.indexes[step]
            temp_form = term.forms[step]
            # if term is not in the index, create it
            if temp_form not in temp_index:
                temp_index[temp_form] = []
            # If this erm ID is not already associated with this term, add if
            if term.id not in temp_index[temp_form]:
                temp_index[temp_form].append(term.id)

    def add_term(self, id:str, pref_label:str, alt_label:str):
        """Adds a term to the index"""
        # Check if a metaterm already exists with this ID
        if not id in self.term_index:
            self.term_index[id] = Metaterm(id)
        
        # Adds the labels to the metaterm list if the label is not empty
        if pref_label != "":
            self.term_index[id].pref_labels.append(Term(id, pref_label))
        if alt_label != "":
            self.term_index[id].alt_labels.append(Term(id, alt_label))

    @property
    def nb_metaterms(self):
        return len(list(self.term_index.keys()))

    # Passer ça en meta term et voir comment a foncitonen avec l'autre
    def get_metaterm_by_id(self, id:str) -> Metaterm|None:
        if id in self.term_index:
            return self.term_index[id]
        return None
    
    def get_terms_id_by_form(self, form:str, step:Step) -> List[str]|None:
        if form in self.indexes[step]:
            return self.indexes[step][form]
        return None