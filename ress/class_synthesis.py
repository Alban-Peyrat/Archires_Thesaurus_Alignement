# -*- coding: utf-8 -*- 

# Etxernal import
from typing import List, Dict
# Internal import
from ress.enums import Step, TSV_Synthesis_Headers
from ress.func_enums import step_for_output

class Synthesis_Metaterm(object):
    def __init__(self, id:str, pref_label:str, alt_label:str):
        self.id = id
        self.pref_label = pref_label
        self.alt_label = alt_label
        self.matched_ids = []
        self.matched_pref_labels = []
        self.matched_alt_labels = []
        self.matched_steps = []
    
    def add_metaterm_match(self, matched_id:str, matched_pref_label:str, matched_alt_label:str, step:Step):
        """Adds the term only if it did not already match"""
        if matched_id not in self.matched_ids:
            self.matched_ids.append(matched_id)
            self.matched_pref_labels.append(matched_pref_label)
            self.matched_alt_labels.append(matched_alt_label)
            self.matched_steps.append(step)
    
    @property
    def nb_match(self) -> int:
        """Returns the number of match"""
        return len(self.matched_ids)
    
    @property
    def highest_step(self) -> Step:
        """Returns the highest step"""
        if len(self.matched_steps) == 0:
            return None
        dedupe = set(self.matched_steps)
        return min(dedupe, key=lambda step: step.value)
    
    def CSV_output(self):
        """Returns as a dict for CSV output"""
        output = {
            TSV_Synthesis_Headers.EXT_ID.value:self.id,
            TSV_Synthesis_Headers.EXT_PREFLABEL.value:self.pref_label,
            TSV_Synthesis_Headers.EXT_ALTLABEL.value:self.alt_label,
            TSV_Synthesis_Headers.INT_ID.value:"|".join(self.matched_ids),
            TSV_Synthesis_Headers.INT_PREFLABEL.value:"|".join(self.matched_pref_labels),
            TSV_Synthesis_Headers.INT_ALTLABEL.value:"|".join(self.matched_alt_labels),
            TSV_Synthesis_Headers.NB_MATCH.value:self.nb_match,
            TSV_Synthesis_Headers.STEP.value:None
        }
        if self.highest_step != None:
            output[TSV_Synthesis_Headers.STEP.value] = step_for_output(self.highest_step)
        return output