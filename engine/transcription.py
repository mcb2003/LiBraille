""" Module for functions that directly modify the AST of a document. """

# Allows tuples to be type-hinted
from typing import Tuple

import louis # Liblouis for braille
from panflute import * # Importing into the global namespace due to common use

# This constant defines the translation table for Liblouis.
# For now, it's hard-coded to UEB grade 2, which is "Universal English Braille" and is what
# The English speaking world currently uses.
LOUIS_TABLE_LIST = ['en-ueb-g2.ctb']
# This is the number of ':' characters that constitute a section break in braille
SECTION_BREAK_CHARS = 12

def typeform_length_char(text: str, typeform: str) -> Tuple[str, str]:
    """ Selects the type of typeform indicator based on how long the text is.
    Return type is a tuple in the form (stat_symbol, end_symbol). """
    if len(text) == 1:
        # Single character
        return tuple("'") # Braille dot 3
    elif len(text.split()) == 1:
        # Word
        return tuple("1") # Braille dot 2
    else:
        # Passage
        return ("7", "%s'" % typeform) # Braille dots 2356

def plain_text(elem:Element) -> Element:
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
        start = plain_text(Str("•"))
    elif isinstance(elem.parent, OrderedList):
        start = plain_text(Str(f"{elem.index+1}."))
    else:
        # Invalid situation (list items should always be children of Ordered or Bullet Lists)
        raise Exception("ListItems should only be children of OrderedList or BulletList items, found %s" % elem.parent.tag)

    ## 2. Add the prefix to the text
    para = elem.content[0] # First child of this ListItem
    para.content.insert(0, Space)
    para.content.insert(0, start)
    # Return the modified ListItem
    p = LineItem()
    [p.content.append(e) for e in para.content]
    return p

def list(elem):
    """ Transcribe entire lists of items. """
    # We convert all lists to `Lineblock`s so the line-spacing is correct in braille
    l = LineBlock()
    for e in elem.content:
        l.content.append(list_item(e))
    return l

def horizontal_rule(elem, wrap_width: int):
    # Calculate the amount of spaces to be added to center the text, clamping at 0 minimum
    # Integer division will automatically round this down if necessary
    left_pad = min(0, (wrap_width - SECTION_BREAK_CHARS) / 2)
    # Construct the result
    result = []
    for i in range(left_pad):
        result.append(Space())
    result.append(Str(":" * SECTION_BREAK_CHARS))
    # use `result` as arguments to the `Plain` constructor
    return Plain(*result)
