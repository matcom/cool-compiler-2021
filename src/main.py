import sys

from lexer import CoolLexer
from cparser import CoolParser
from semantic.visitors.typeBuilder import TypeBuilder
from semantic.visitors.typeChecker import TypeChecker
from semantic.visitors.typeCollector import TypeCollector
from semantic.visitors.varCollector import VarCollector
from code_generator.COOLToCILVisitor import COOLToCILVisitor
from code_generator.CILToMIPSVisitor import CILToMIPSVisitor


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

    varCollector = VarCollector(context, semanticErrors)
    scope = varCollector.visit(ast)

    typeChecker = TypeChecker(context, semanticErrors)
    typeChecker.visit(ast, scope)

    if semanticErrors:
        for error in semanticErrors:
            print(error)
            raise Exception()

    # Code Generation
    coolToCIL = COOLToCILVisitor(context)
    cilAST = coolToCIL.visit(ast, scope)

    cilToMIPS = CILToMIPSVisitor()
    mips_code = cilToMIPS.visit(cilAST)

    with open(_output, 'w+') as f:
        f.write(mips_code)

if __name__ == "__main__":

    in_path = '/home/cwjki/Projects/cool-compiler-2021/tests/codegen/arith.cl'
    out_path = '/home/cwjki/Projects/cool-compiler-2021/src/codeMips.mips'
    _input = sys.argv[1] if len(sys.argv) > 1 else in_path
    _output = sys.argv[2] if len(sys.argv) > 2 else out_path

    main(_input, _output)
