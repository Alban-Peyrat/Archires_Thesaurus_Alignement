# -*- coding: utf-8 -*- 

# Etxernal import
import re
from unidecode import unidecode

# From FCR 2.0.1, with slight modifications versions
def prep_string(_str:str, _noise = True, _multiplespaces = True) -> str:
    """Returns a string without punctuation and/or multispaces stripped and in lower case.

    Takes as arguments :
        - _str : the string to edit
        - _noise [optional] {bool} : remove punctuation ?
        - _multispaces [optional] {bool} : remove multispaces ?
    """
    # remove noise (punctuation) if asked (by default yes)
    if _noise:
        _str = re.sub(r"[\x21-\x2F]|[\x3A-\x40]|[\x5B-\x60]|[\x7B-\x7F]|[\u2010-\u2015]|\.|\,|\?|\!|\;|\/|\:|\=|\[|\]|\'|\-|\(|\)|\||\"|\<|\>|\+|\°", " ", _str, flags=re.IGNORECASE)
    # replace multiple spaces by ine in string if requested (default yes)
    if _multiplespaces:
        _str = re.sub(r"\s+", " ", _str).strip()
    return _str.strip().lower()

def remove_extended_stop_words(txt:str) -> str:
    """Deleted every extended stop words"""
    extended_stop_word_list = ["province", "wilaya", "quartier", "cite", "gouvernat", "basilique", "region", "ile", "iles", "etat", "district", "autonome", "territoire", "prefecture", "monastere", "temple", "special", "administratif", "arrondissement", "parc", "musee", "zac", "zup", "place", "porte", "arr", "site archeologique", "principaute", "anchal", "cours eau", "land", "chateau"]
    for word in extended_stop_word_list:
        txt = txt.replace(word, " ")
    return txt
    
def delete_CBS_boolean_operators(txt:str) -> str:
    """Deletes all CBS boolean operators (AND, OR, NOT) in eevry language and return the resukt as a string
    Based on "All CBS Command" Version 6 (2014-02-11)"""
    txt = re.sub(r"\b(AND|EN|UND|ET|VE|NOT|NIET|NICHT|NON|DEGIL|SAUF|OR|OF|ORDER|OU|VEYA)\b", "", txt, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", txt)

def delete_Sudoc_empty_words(txt:str) -> str:
    """Deletes all Sudoc empty keywords (index TOUT) to simplify the query"""
    txt = re.sub(r"\b(A|BIS|DI|IL|OF|THE|AB|BY|DIE|IM|ON|THEIR|ABOUT|C|DONT|IMPR|OU|THIS|ACCORDING|CE|DR|IN|OVER|TO|ACROSS|CETTE|DU|INTO|P|UEBER|AD|CEUX|DURANT|E|PAR|UM|AGAINST|CHEZ|DURANTE|ITS|PER|UND|AINSI|CO|DURCH|J|PLUS|UNDER|AL|COMME|DURING|L|POR|UNE|ALL|COMO|E|LA|POUR|UNLESS|ALLA|CUM|ED|LAS|QU|UNTER|ALLE|D|EIN|LE|QUAE|UPON|ALS|DAL|EINE|LES|QUE|VOM|ALSO|DALL|EINEM|LEUR|R|VON|ALTRE|DALLA|EINER|LEURS|S|VOR|AM|DANS|EINES|LO|SANS|VOS|AMONG|DAS|EL|LOS|SE|VOTRE|AN|DE|EN|M|SELON|VOUS|AND|DEGLI|ES|MES|SES|W|ASI|DEL|ET|MIT|SIC|WAS|AT|DELL|F|N|SINCE|WE|ATQUE|DELLA|FOR|NACH|SIVE|WHITCH|AU|DELLE|FROM|NE|SN|WITH|AUF|DELLO|FUER|NEAR|SO|Y|AUPRES|DEM|G|NEL|SOME|ZU|AUS|DEN|GLI|NO|SOUS|ZUR|AUSSI|DEPUIS|H|NOS|ST|AUX|DER|HIS|NOTRE|SUL|AVEC|DEREN|I|NOUS|SUR|B|DES|IHRE|O|TE|BEI|DESDE|IHRER|ODER|THAT|UN)\b", "", txt, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", txt)

# not from FCR
def sort_words(txt:str) -> str:
    """Returns the string sorting all the elements"""
    return " ".join(sorted(txt.split()))

def fingerprint(txt:str, stop_words:bool=False, stop_words_extended:bool=False, no_parenthesis:bool=False) -> str:
    """Returns the string using a kind of fingerprint"""
    txt = txt.lower()
    txt = txt.replace('&', 'et')
    txt = txt.replace('œ', 'oe')
    txt = unidecode(txt)
    # If no parenthesis, remove them
    if no_parenthesis:
        # No while, we use safety net
        for index in range(0, 10):
            if "(" in txt and ")" in txt:
                txt = re.sub(r"\([^()]*\)", "", txt)
            # If regexp sub can't trigger anymore, break loop
            else:
                break
    # Remove noise + multispace + nromalise
    txt = prep_string(txt)
    # If no stop words, remove them
    if stop_words:
        txt = delete_Sudoc_empty_words(delete_CBS_boolean_operators(txt))
    # If no extended stop words, remove them
    if stop_words_extended:
        txt = remove_extended_stop_words(txt)
    # Retrigger final prep string just in case
    txt = prep_string(txt)
    return sort_words(txt)