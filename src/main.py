from ast import parse
import sys

from lexer import CoolLexer
from cparser import CoolParser
from src.semantic.visitors.typeBuilder import TypeBuilder
from src.semantic.visitors.typeChecker import TypeChecker
from src.semantic.visitors.typeCollector import TypeCollector
from src.semantic.visitors.varCollector import VarCollector


def main(_input, _output):

    with open(_input) as file:
        text = file.read()

    # Lexer
    lexer = CoolLexer()
    tokens = lexer.run(text)

    # Parser
    parser = CoolParser(lexer)
    ast = parser.parse(text)
    if parser.errors:
        parser.print_error()
        raise Exception()

    # Semantic
    semanticErrors = []
    typeCollector = TypeCollector(semanticErrors)
    typeCollector.visit(ast)
    context = typeCollector.context
    typeBuilder = TypeBuilder(context, semanticErrors)
    typeBuilder.visit(ast)
    typeInferer = VarCollector(context, semanticErrors)
    scope = typeInferer.visit(ast)
    typeChecker = TypeChecker(context, semanticErrors)
    typeChecker.visit(ast, scope)
    if semanticErrors:
        for error in semanticErrors:
            print(semanticErrors)
            raise Exception()

    # Code Generation


    # ast, errors, context, scope = SemanticAn
if __name__ == "__main__":

    path = '/home/cwjki/Projects/cool-compiler-2021/tests/parser/case2.cl'
    _input = sys.argv[1] if len(sys.argv) > 1 else path
    _output = sys.argv[2] if len(sys.argv) > 2 else None

    main(_input, _output)

    # input_ = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/lexer/iis4.cl'
    # main(input_)
