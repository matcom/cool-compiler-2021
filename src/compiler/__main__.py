from visitors.code_gen.ccil_gen import CCILGenerator
from visitors.code_gen.ccil_mips_gen import CCILToMIPSGenerator
from visitors.code_gen.mips_gen import MIPSGenerator
from visitors.ast_print.type_logger import TypeLogger
import sys

from lexing import Lexer
from parsing import Parser
from visitors.semantics import TypeBuilder, TypeCollector
from visitors.semantics.inference import (
    SoftInferencer,
    HardInferencer,
    BackInferencer,
    TypesInferencer,
)


def format_errors(errors, s=""):
    for error in errors:
        s += error[1] + "\n"
    return s[:]


def semantics_pipeline(program_ast):

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

    if len(errors) > 0:
        s = format_errors(errors)
        print(s)
        exit(1)

    change = True
    back = BackInferencer(context)

    back_ast, change = back.visit(hard_ast)
    while change:
        back_ast, change = back.visit(back_ast)

    types = TypesInferencer(context)
    types_ast = types.visit(back_ast)
    errors += types.errors

    logger = TypeLogger(context)
    log = logger.visit(back_ast, back_ast.scope)
    print(log)

    if len(errors) > 0:
        s = format_errors(errors)
        print(s)
        exit(1)

    return types_ast


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]  # + " " + sys.argv[2] + " " + sys.argv[3]
    else:
        input_file = "../tests/normal/abort1.cl"
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

    type_ast = semantics_pipeline(ast)
    ccil_gen = CCILGenerator()
    ccil_ast = ccil_gen.visit(type_ast)

    ccil_mips_gen = CCILToMIPSGenerator()
    mips_ast = ccil_mips_gen.visit(ccil_ast)

    mips_gen = MIPSGenerator()
    mips_code = mips_gen.visit(mips_ast)

    out_file = input_file.split(".")[0]
    path_to_file = f"{out_file}.mips"
    # path_to_file = "output.asm"
    with open(path_to_file, "w") as f:
        f.write(mips_code)


main()
