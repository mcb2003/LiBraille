""" Module for functions that directly modify the AST of a document. """

# Allows tuples to be type-hinted
from typing import Tuple

import louis # Liblouis for braille
from panflute import * # Importing into the global namespace due to common use

# This constant defines the translation table for Liblouis.
# For now, it's hard-coded to UEB grade 2, which is "Universal English Braille" and is what
# The English speaking world uses now.
LOUIS_TABLE_LIST = ['en-ueb-g2.ctb']

def typeform_length_char(text: str, typeform: str) -> Tuple[str, str]:
    """ Selects the type of typeform indicator based on how long the text is.
    Return type is a tuple in the form (start_symbol, end_symbol). """
    if len(text) == 1:
        # Single character
        return tuple("'") # Braille dot 3
    elif len(text.split()) == 1:
        # Word
        return tuple("1") # Braille dot 2
    else:
        # Passage
        return ("7", "%s'" % typeform) # Braille dots 2356

def plain_text(elem:Element, doc: Doc) -> Element:
    """ Uses Liblouis to translate plain text into braille. """
    return Str(louis.translateString(LOUIS_TABLE_LIST, stringify(elem)))
