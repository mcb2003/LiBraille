""" Package of modules for converting a pandoc AST into braille. """

from document import *

# This is the entry point to the transcription engine
if __name__ == "__main__":
    ## 1. Import required modules
    from sys import argv # Command-line arguments

    ## 2. Create an instance of the Document class.
    #  This will automatically transcribe the document as well
    file_name = argv[1]
    doc = Document(file_name)
    ## 3. Debug: Print out a textual representation of the document
    print(doc)
