import sys
import os
from lexer import tokenize
from parser import parse
from testers import parser_tester

#########################################################
# To use this script execute in terminal:               #
#   python3 main.py module_to_test test_directories     #
#                                                       #
# module_to_test can be:                                #
#   - lexer     - parser                                #
# test_directories is the dir where tests are, ex:      #
#   ../tests/lexer                                      #
#   ../tests/parser                                     #
#########################################################

# programs_directory = sys.argv[2]
programs_directory = '../tests/parser'
programs_files = [file for file in os.listdir(programs_directory) if file.endswith('.cl')]

# parser_tester(programs_directory)


for program_file in programs_files:
    input('Press enter to analyze ' + program_file)
    program_route = programs_directory + '/' + program_file

    # To test lexer
    if sys.argv[1] == 'lexer':
        with open(program_route, 'r', encoding='UTF-8') as f:
            tokens, errors = tokenize(f.read())

        # for token in tokens:
        #     print(token)
        print()
        if len(errors):
            print('ERRORS:')
            for error in errors:
                print(error)
        else:
            print('NO ERRORS')

    # To test parser
    elif sys.argv[1] == 'parser':
        with open(program_route, 'r', encoding='UTF-8') as f:
            tree, errors = parse(f.read())
            print(str(tree))

            print(errors)

    else:
        print('Invalid section to test: ' + sys.argv[1])
