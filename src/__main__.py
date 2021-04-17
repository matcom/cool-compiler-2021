import sys

from lexing import lexer
from parsing import parser
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

    # if len(sys.argv) > 1:
    #     input_file = sys.argv[1]
    # else:
    #     raise Exception("Incorrect number of arguments")

    program = open(input_file).read()
    lexer.input(program)
    tokens = []
    for token in lexer:
        tokens.append(token)
    if lexer.errors:
        print(lexer.errors[0])
        exit(1)

    # ast = parser.parse(program)

    # run_pipeline(ast)


main()
