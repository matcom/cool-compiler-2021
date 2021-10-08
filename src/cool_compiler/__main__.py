import sys
from .error import CoolError
from .lexer import CoolLexer
from .parser import CoolParser
from .semantic import *
from .types import CoolTypeBuildInManager

path = ""
if len(sys.argv) > 1:
    path = sys.argv[1]


with open(path, 'r') as _file:
    text = _file.read()
    errors = CoolError(text)
    lexer = CoolLexer(errors)
    CoolTypeBuildInManager()
    parser = CoolParser(CoolFactory(errors), errors)

    
    tokens = [token for token in lexer.tokenize(text)]
    if errors.any(): sys.exit(1)

    ast = parser.parse(iter(tokens))
    if errors.any(): sys.exit(1)

    visitorList = [ CreateType ]
 
    for visitorClass in visitorList:
        ast = visitorClass(errors).visit(ast)
        if errors.any(): sys.exit(1)



    
