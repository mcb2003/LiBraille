""" Package of modules for converting a pandoc AST into braille. """

from document import *

# This is the entry point to the transcription engine
if __name__ == "__main__":
    ## 1. Import required modules
    from sys import argv # Command-line arguments

    ## 2. Load the AST
    file_name = argv[1]
    ast = get_ast(file_name)

    ## 3. Parse the AST into a more usible data structure
    doc = get_doc(ast)

    ##  4. Transcribe the document
    doc = doc.walk(transcribe)
    # Debug: print the elements in the document:
    for elem in doc.content:
        print(pf.stringify(elem))
