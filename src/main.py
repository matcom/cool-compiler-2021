import sys

from lexer import CoolLexer
from cparser import CoolParser
from semantic.visitors.typeBuilder import TypeBuilder
from semantic.visitors.typeChecker import TypeChecker
from semantic.visitors.typeCollector import TypeCollector
from semantic.visitors.varCollector import VarCollector
# from code_generator.COOLToCILVisitor import COOLToCILVisitor
from utils.errors import SemanticError


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
    # print("TYPE COLLECTOR")
    # if semanticErrors:
    #     for error in semanticErrors:
    #         print(error)

    context = typeCollector.context
    typeBuilder = TypeBuilder(context, semanticErrors)
    typeBuilder.visit(ast)

    # print("CONTEXT")
    # print(context)
    # print("TYPE Builder")
    # if semanticErrors:
    #     for error in semanticErrors:
    #         print(error)

    varCollector = VarCollector(context, semanticErrors)
    scope = varCollector.visit(ast)
    # print("Var Collector")
    # if semanticErrors:
    #     for error in semanticErrors:
    #         print(error)
    
    typeChecker = TypeChecker(context, semanticErrors)
    typeChecker.visit(ast, scope)
    if semanticErrors:
        for error in semanticErrors:
            print(error)
            raise Exception()

    # Code Generation

    # coolToCIL = COOLToCILVisitor(context)
    # cilAST = coolToCIL.visit(ast, scope)


    # ast, errors, context, scope = SemanticAn
if __name__ == "__main__":

    path = '/mnt/c/Users/Liviton/Desktop/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/semantic/arithmetic1.cl'
    _input = sys.argv[1] if len(sys.argv) > 1 else path
    _output = sys.argv[2] if len(sys.argv) > 2 else None

    main(_input, _output)

    # input_ = '/mnt/d/UH/4to Año/EVEA/Complementos de Compilacion/cool-compiler/cool-compiler-2021/tests/lexer/iis4.cl'
    # main(input_)
