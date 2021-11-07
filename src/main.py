import sys
from testers import test_parser, test_lexer

################################################
#   To use this script execute in terminal:    #
#     python3 main.py module_to_test           #
#                                              #
#   module_to_test can be:                     #
#     - lexer     - parser                     #
################################################

tester = sys.argv[1]

if tester == 'parser':
    test_parser()
elif tester == 'lexer':
    test_lexer()


# programs_directory = sys.argv[2]
# programs_files = [file for file in os.listdir(programs_directory) if file.endswith('.cl')]

# for program_file in programs_files:
#     input('Press enter to analyze ' + program_file)
#     program_route = programs_directory + '/' + program_file
#
#     # To test lexer
#     if sys.argv[1] == 'lexer':
#         with open(program_route, 'r', encoding='UTF-8') as f:
#             tokens, errors = tokenize(f.read())
#
#         for token in tokens:
#             print(token)
#         print()
#         if len(errors):
#             print('ERRORS:')
#             for error in errors:
#                 print(error)
#
#     # To test parser
#     if sys.argv[1] == 'parser':
#         with open(program_route, 'r', encoding='UTF-8') as f:
#             tree, errors = parse(f.read())
#             print(str(tree))
#
#             print(errors)
#
#     else:
#         print('Invalid section to test: ' + sys.argv[1])
