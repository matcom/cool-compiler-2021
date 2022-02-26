import sys
import os
import ast_cool_print
import type_collector
import type_builder
import type_checker
import translate_cool_cil
from lexer import tokenize
from parser import parse
from testers import test_parser

#################################################################################
# To use this script execute in terminal:                                       #
#   python3 main_sandbox.py execute_mode module_to_execute program_directory    #
#                                                                               #
# execute_mode is to use the tester or just run the program(s), ex:             #
#   - test      - run                                                           #
# module_to_execute can be:                                                     #
#   - lexer     - parser     - semantic                                         #
# program_directory is the dir where program(s) is(are), ex:                    #
#   ../tests/lexer                                                              #
#   ../tests/parser                                                             #
#################################################################################

execute_mode = sys.argv[1]
module_to_execute = sys.argv[2]
program_directory = sys.argv[3]

# TEST
if execute_mode == "test":
    if module_to_execute == "parser":
        test_parser(program_directory)
    else:
        raise Exception("Not implemented Test Mode for %s" % module_to_execute)

# RUN
programs_files = [
    file for file in os.listdir(program_directory) if file.endswith("conditional3.cl")
]
for program_file in programs_files:
    input("Press enter to analyze " + program_file)
    program_route = program_directory + "/" + program_file

    # To run lexer
    if module_to_execute == "lexer":
        with open(program_route, "r", encoding="UTF-8") as f:
            tokens, errors = tokenize(f.read())

        for token in tokens:
            print(token)
        print()
        if len(errors):
            print("ERRORS:")
            for error in errors:
                print(error)

    # To run parser
    elif module_to_execute == "parser":
        with open(program_route, "r", encoding="UTF-8") as f:
            ast, errors = parse(f.read())
            if len(errors):
                print(errors)
            else:
                # print ast
                formatter = ast_cool_print.FormatVisitor()
                tree = formatter.visit(ast)
                print(str(tree))

    # To run semantic
    elif module_to_execute == "semantic":
        with open(program_route, "r", encoding="UTF-8") as f:
            # program_route = program_route[: len(program_route) - 3] + "_error.txt"
            # with open(program_route, "r", encoding="UTF-8") as f1:
            #     print(f1.read())
            ast, errors = parse(f.read())
            if len(errors):
                print(errors)
                continue

            collector = type_collector.TypeCollector(errors)
            collector.visit(ast)

            context = collector.context
            builder = type_builder.TypeBuilder(context, errors)
            builder.visit(ast)

            checker = type_checker.TypeChecker(context, errors)
            scope = checker.visit(ast)

            translate = translate_cool_cil.TranslateCool2Cil(context)
            tree = translate.visit(ast)
            print('jasdwqe')

    else:
        print("Invalid section to execute: " + module_to_execute)
