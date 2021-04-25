<<<<<<< HEAD
=======
from os import close, error
from semantics.inference.hard_inferencer import HardInferencer
from debbuging.type_logger import TypeLogger
>>>>>>> 55759b8cb59c5d6caf6a83058531f096817f19e0
import sys

from lexing import Lexer
from parsing import Parser
from semantics import TypeBuilder, TypeCollector
from semantics.inference import (
    SoftInferencer,
    HardInferencer,
    BackInferencer,
)


def format_errors(errors, s=""):
    # errors.sort(key=lambda x: x[0])
    for error in errors:
        s += error[1] + "\n"
    return s[:]


def run_pipeline(program_ast):

    collector = TypeCollector()
    collector.visit(program_ast)
    context = collector.context
    errors = collector.errors

    builder = TypeBuilder(context)
    builder.visit(program_ast)
    errors += builder.errors

    soft = SoftInferencer(context)
    soft_ast = soft.visit(program_ast)
    errors += soft.errors

    hard = HardInferencer(context)
    hard_ast = hard.visit(soft_ast)
    errors += hard.errors

    logger = TypeLogger(context)
    log = logger.visit(hard_ast, hard_ast.scope)
    print(log)
    if len(errors) > 0:
        for error in errors:
            print(error[1])
        # s = format_errors(errors)
        # print(s)
        exit(1)
    # print(s)


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]  # + " " + sys.argv[2] + " " + sys.argv[3]
    else:
        input_file = "src/test.cl"
    #   raise Exception("Incorrect number of arguments")

    program_file = open(input_file)
    program = program_file.read()
    program_file.close()

    lexer = Lexer()
    tokens = list(lexer.tokenize(program))
    if lexer.errors:
        for error in lexer.errors:
            print(error)
        exit(1)

    parser = Parser(Lexer())
    ast = parser.parse(program)
    if parser.errors:
        for error in parser.errors:
            print(error)
        exit(1)

    run_pipeline(ast)


main()