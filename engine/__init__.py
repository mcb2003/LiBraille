""" Package of modules for converting a pandoc AST into braille. """

import io # For io.StringIO
import os # OS related utilities, including file management
import subprocess # Used to interface with external programs

import panflute as pf # Easier handling of Pandoc ASTs

import transcription

def get_ast(file_name: str) -> bytes:
    """ Open and convert the file identified by file_name into a pandoc AST. """
    # Check the file exists and is readable:
    if os.path.isfile(file_name):
        # File exists, convert it with pandoc:
        # subprocess requires a list of arguments, so we split a string to get that.
        command = "pandoc -s -t json".split()
        command.append(file_name) # Pandoc accepts the file_name as the last argumentt

        # Run the pandoc command and collect its output
        result = subprocess.run(command, capture_output=True)
        # Check if the pandoc conversion was successfull. This raises an error if not.
        result.check_returncode()

        ast_json = result.stdout
        return ast_json

    else:
        # File doesn't exist, raise an error!
        raise FileNotFoundError("No such file")

def get_doc(ast: bytes) -> pf.Doc:
    """ Loads a Pandoc AST and converts it into a usable data structure. """
    # pf.load() expects a file handle to read from,
    # So we use io.StringIO to wrap the bytes returned by subprocess.
    # We also need to convert the bytes-like string to a unicode string.
    ast = str(ast, 'utf8') # Probably unsafe to assume utf-8
    with io.StringIO(ast) as ast_handle:
        # Load and parse the AST:
        doc = pf.load(ast_handle)

    return doc

def transcribe(elem: pf.Element, doc: pf.Doc):
    """ Executed for each node in the AST.
    Delligates to the functions in the transcription module. """

    if isinstance(elem, pf.Str): # Plain text
        return transcription.plain_text(elem, doc)

# The following block only runs when this module is executed directly by python,
# and not when it's imported by another module.
if __name__ == "__main__":
    from sys import argv # Allows retrieval of command-line arguments

    file_name = argv[1]
    ast = get_ast(file_name)
    # Parse the AST
    doc = get_doc(ast)
    # Transcribe the document
    doc = doc.walk(transcribe)
    # Debug: print the elements in the document:
    for elem in doc.content:
        print(pf.stringify(elem))