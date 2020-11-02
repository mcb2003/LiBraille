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

def bold(elem: Strong):
    """ Return the text with the correct surrounding typeforms. """
    # "~" is the braille symbol for bold
    length_symbols = typeform_length_char(stringify(elem), "~")
    elems = [Str("~" + length_symbols[0]), elem]
    try:
        # We might not have an end symbol
        elems.append(Str(length_symbols[1]))
    except IndexError:
        pass
    return elems

def italic(elem: Emph):
    """ Return the text with the correct surrounding typeforms. """
    # "_" is the braille symbol for italic
    length_symbols = typeform_length_char(stringify(elem), "_")
    elems = [Str("_" + length_symbols[0]), elem]
    try:
        # We might not have an end symbol
        elems.append(Str(length_symbols[1]))
    except IndexError:
        pass
    return elems

def underline(elem: Span):
    """ Return the text with the correct surrounding typeforms. """
    # "." is the braille symbol for italic
    length_symbols = typeform_length_char(stringify(elem), ".")
    elems = [Str("." + length_symbols[0]), elem]
    try:
        # We might not have an end symbol
        elems.append(Str(length_symbols[1]))
    except IndexError:
        pass
    return elems

def list_item(elem: ListItem):
    """ Transcribe items of bulletted and ordered lists. """
    ## 1. Determine type of list and create appropriate prefix
    if isinstance(elem.parent, BulletList):
        start = Str("_4") # Braille bullet point "⠸⠲"
    elif isinstance(elem.parent, OrderedList):
        start = Str(str(elem.index + 1) + ".")
    else:
        # Invalid situation (list items should always be children of Ordered or Bullet Lists)
        raise Exception("ListItems should only be children of OrderedList or BulletList items, found %s" % elem.parent.tag)

    ## 2. Add the prefix to the text
    para = elem.content[0]
    # Add the bullet or number to the start of the text
    para.content.insert(0, Space)
    para.content.insert(0, start)
    return elem
