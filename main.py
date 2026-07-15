# -*- coding: utf-8 -*- 

# Etxernal import
import os
from dotenv import load_dotenv
import csv
from typing import List, Dict

# Internal imports
from ress.enums import TSV_Headers, Step
from ress.class_thesaurus import Thesaurus
from ress.class_terms import Term

# To do :
# - user should be able to chose wich steps they want
# - maybe : 1 CSV file with only 1 lien per metaterm ID

# ----------------- Load configs -----------------
load_dotenv()
# -------- Load thesaurus --------
external_thes = Thesaurus(os.getenv("EXTERNAL_THES_PATH"), os.getenv("EXTERNAL_THES_DELIMITER"), os.getenv("EXTERNAL_THES_ID_COL"))
print(f"External thesaurus is loaded : {external_thes.nb_metaterms} terms")
internal_thes = Thesaurus(os.getenv("INTERNAL_THES_PATH"), os.getenv("INTERNAL_THES_DELIMITER"), os.getenv("INTERNAL_THES_ID_COL"))
print(f"Internal thesaurus is loaded : {internal_thes.nb_metaterms} terms")

# ----------------- Func def -----------------
def match_term(term:Term, is_pref:bool=True) -> dict:
    output = {
        TSV_Headers.EXT_ID.value:term.id,
        TSV_Headers.EXT_NAME.value:term.label,
        TSV_Headers.EXT_IS_PREF.value:is_pref,
        TSV_Headers.INT_ID.value:[],
        TSV_Headers.INT_NAMES.value:[],
        TSV_Headers.NB_MATCH.value:None,
        TSV_Headers.STEP.value:None,
        TSV_Headers.KEY_USED.value:None,
    }
    # Try to match once
    for step in Step:
        matched_ids = internal_thes.get_terms_id_by_form(term.forms[step], step)
        # If match, add it to output and break from loop
        if matched_ids:
            output[TSV_Headers.INT_ID.value] = matched_ids
            for matched_id in matched_ids:
                matched_term = internal_thes.get_metaterm_by_id(matched_id)
                if matched_term:
                    output[TSV_Headers.INT_NAMES.value].append(matched_term.get_pref_label())
            output[TSV_Headers.NB_MATCH.value] = len(matched_ids)
            output[TSV_Headers.STEP.value] = step.name
            output[TSV_Headers.KEY_USED.value] = term.forms[step]
            break
    # Join lists
    output[TSV_Headers.INT_ID.value] = "|".join(output[TSV_Headers.INT_ID.value])
    output[TSV_Headers.INT_NAMES.value] = "|".join(output[TSV_Headers.INT_NAMES.value])

    # Return the dict ready for output
    return output

# ----------------- Main -----------------
output_list:List[Dict] = []

print("Starting term matching")
# For each term, look for matchign terms # Old one
# For each meta term, look for each term on the other side if there are matching terms
for index, id in enumerate(external_thes.term_index):
    # Give user info on progression
    if index % 1000 == 0:
        print(f"Starting term {index}")
    metaterm = external_thes.term_index[id]
    # Loop through each term inside this meta terme
    for term in metaterm.pref_labels:
        output_list.append(match_term(term, is_pref=True))
    for term in metaterm.alt_labels:
        output_list.append(match_term(term, is_pref=False))
    
# CSV output
with open(os.getenv("OUTPUT_PATH"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, [val.value for val in TSV_Headers], delimiter="\t")
    writer.writeheader()
    for output in output_list:
        writer.writerow(output)
    
