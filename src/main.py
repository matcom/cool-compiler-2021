import sys
from tabnanny import check
from traceback import print_exception

from Tools.errors import CompilerError
from Tools.messages import UNKNOWN_FILE
from Tools.utils import get_code

from Parser.lexer import Lexer
from Parser.parser import Parser

from Semantic.collector import TypeCollector, VariableCollector
from Semantic.builder import TypeBuilder
from Semantic.checker import TypeChecker

from CIL.cil import CIL

from MIPS.mips import MIPS

def print_error(errors):
    for x in errors:
        print(x)
    if errors: exit(1)

def main(input_file, cil_file, output_file):
    try:
        text = open(input_file, 'r').read()
    except FileNotFoundError:
        print(CompilerError(UNKNOWN_FILE % input_file, 0, 0))
    
    lexer = Lexer()
    tokens = lexer.tokenize(text)
    print_error(lexer.errors)
    
    parser = Parser(lexer)
    ast = parser(text)
    print_error(parser.errors)

    collector = TypeCollector()
    collector.visit(ast)
    context = collector.context
    print_error(collector.errors)

    builder = TypeBuilder(context)
    builder.visit(ast)
    print_error(builder.errors)

    variable = VariableCollector(context)
    scope = variable.visit(ast)
    print_error(variable.errors)

    checker = TypeChecker(context)
    checker.visit(ast, scope)
    print_error(checker.errors)

    cil = CIL(context)
    cil_ast = cil.visit(ast, scope)
    #open(cil_file, 'w').write(str(cil_ast))

    mips = MIPS(context.build_inheritance_graph())
    data_code, text_code = mips.visit(cil_ast)
    open(output_file, 'w').write(get_code(text_code, data_code))

    exit(0)

if __name__=='__main__':
    cil_file = sys.argv[2]
    input_file = sys.argv[1]
    output_file = sys.argv[3]
    main(input_file, cil_file, output_file)