import sys

from ply.lex import lex

from lexing import Lexer

# from parsing import Parser
from parsing import Parser
from semantics import TypeBuilder, TypeCollector, TypeChecker
from semantics.inference import (
    AutotypeCollector,
    AutotypeInferencer,
    BackInferencer,
    SoftInferencer,
)


def run_pipeline(program_ast):

    collector = TypeCollector()
    collector.visit(program_ast)
    context = collector.context
    errors = collector.errors

    builder = TypeBuilder(context, errors)
    builder.visit(program_ast)

    soft = SoftInferencer(context)
    soft_ast = soft.visit(program_ast)

    # auto_inferencer = autotype_inferencer.AutotypeInferencer(context, errors)
    # auto_inferencer.visit(ast, scope)

    # logger = type_logger.TypeLogger(context)
    # log = logger.visit(soft_ast, soft_ast.scope)
    # print(log)
    # s = "Semantic Errors:\n"
    # s = format_errors(errors, s)
    # print(s)


input_file = "src/test.cl"


def main():

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        raise Exception("Incorrect number of arguments")

    program = open(input_file).read()

    lexer = Lexer()

    # parser = Parser(lexer)
    # ast = parser.parse(program)
    # print(ast)

    tokens = list(lexer.tokenize(program))
    # print(tokens)
    # print(lexer.errors)

    # lexer.input(program)
    # tokens = []
    # for token in lexer:
    # #     tokens.append(token)
    if lexer.errors:
        for error in lexer.errors:
            print(error)
        exit(1)

    # ast = parser.parse(program)

    # run_pipeline(ast)


main()
