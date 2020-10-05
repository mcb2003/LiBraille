""" Module for functions that directly modify the AST of a document. """

import louis # Liblouis for braille
from panflute import * # Importing into the global namespace due to common use

# This constant defines the translation table for Liblouis.
# For now, it's hard-coded to UEB grade 2, which is "Universal English Braille" and is what
# The English speaking world uses now.
LOUIS_TABLE_LIST = ['en-ueb-g2.ctb']

def plain_text(elem:Element, doc: Doc) -> Element:
    """ Uses Liblouis to translate plain text into braille. """
    return Str(louis.translateString(LOUIS_TABLE_LIST, stringify(elem)))
