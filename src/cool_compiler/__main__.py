import sys
from .error import CoolError
from .lexer import CoolLexer

path = ""
if len(sys.argv) > 1:
    path = sys.argv[1]


with open(path, 'r') as _file:
    text = _file.read()
    errors = CoolError(text)
    lexer = CoolLexer(errors)

    tokens = [token for token in lexer.tokenize(text)]
    if errors.any(): sys.exit(1)