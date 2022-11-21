import sys
from .error import CoolError
from .lexer import CoolLexer
from .parser import CoolParser
from .codegen import CoolToCIL, MipsGenerate
from .semantic import *
from .types import CoolTypeBuildInManager

path = ""
if len(sys.argv) > 1:
    path = sys.argv[1]

#path = "test.cl"

with open(path, 'r') as _file:
    text = _file.read()
    _file.close()
    errors = CoolError(text)
    lexer = CoolLexer(errors)
    type_manager = CoolTypeBuildInManager()
    type_manager.all_inherence_of_object()
    parser = CoolParser(CoolFactory(errors), errors)
   
    tokens = [token for token in lexer.tokenize(text)]
    if errors.any(): sys.exit(1)

    ast = parser.parse(iter(tokens))
    if errors.any(): sys.exit(1)

    visitorList = [ CreateType, SemanticChecking, CoolToCIL , MipsGenerate ]
 
    for visitorClass in visitorList:
        ast  = visitorClass(errors).visit(ast)
        if errors.any(): sys.exit(1)
        
with open(path.replace('.cl', '.mips'), '+w') as _file:    
    _file.write(str(ast))
    _file.close()
