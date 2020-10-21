import io # For io.StringIO
import os # OS related utilities, including file management
import subprocess # Used to interface with external programs

import panflute as pf # Easier handling of Pandoc ASTs

import transcription

class Document:
    @staticmethod
    def get_ast(file_name: str) -> bytes:
        """ Open and convert the file identified by file_name into a pandoc AST. """
        ## 1. Check the file exists and is readable:
        if os.path.isfile(file_name):
            ## 2A. File exists, convert it with pandoc:
            # subprocess requires a list of arguments, so we split a string to get that.
            command = "pandoc -s -t json".split()
            command.append(file_name) # Pandoc accepts the file_name as the last argument

            ## 3. Run the pandoc command and collect its output
            result = subprocess.run(command, capture_output=True)
            ## 4. Check if the pandoc conversion was successfull. This raises an error if not.
            result.check_returncode()

            # Get the output from pandoc
            ast_json = result.stdout
            return ast_json

        else:
            # 2B. File doesn't exist, raise an error!
            raise FileNotFoundError("No such file")

    @staticmethod
    def get_doc(ast: bytes) -> pf.Doc:
        """ Loads a Pandoc AST and converts it into a usable data structure. """
        ## 1. Create necessary variables to do conversion
        # pf.load() expects a file handle to read from,
        # So we use io.StringIO to wrap the bytes returned by subprocess.
        # We also need to convert the bytes-like string to a unicode string.
        ast = str(ast, 'utf8') # Probably unsafe to assume utf-8
        with io.StringIO(ast) as ast_handle:
            ## 2. Load and parse the AST:
            doc = pf.load(ast_handle)

        return doc

    def transcribe(elem: pf.Element, doc: pf.Doc):
        """ Executed for each node in the AST.
        Delligates to the functions in the transcription module. """
        # This function walks through all nodes in the document,
        # Transcribing each depending on what type of formatting it represents.

        ## 1. Deligate transcription based on the type of the formatting
        if isinstance(elem, pf.Str): # Plain text
            ## 1A. Element is plane, unformatted text
            return transcription.plain_text(elem, doc)

    def __init__(self, file_name: str):
        """ Constructs a Document object by parsing a file into an AST. """
        ## 1. Read the file and parse it into an AST
        ast_json = Document.get_ast(file_name)
        self.ast = Document.get_doc(ast_json)
        ## 2. Transcribe the document
        self.ast.walk(Document.transcribe)

    def __repr__(self):
        """ Debug: returns a textual representation of the document. """
        repr = ""
        for elem in self.ast.content:
            repr += pf.stringify(elem)

        return repr
