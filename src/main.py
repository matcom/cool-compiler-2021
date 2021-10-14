import sys
import os
from lexer import tokenize

programs_directory = sys.argv[1]
programs_files = [file for file in os.listdir(programs_directory) if file.endswith('.cl')]

for program_file in programs_files:
    input('Press enter to analyze ' + program_file)
    program_route = programs_directory + '/' + program_file
    with open(program_route, 'r', encoding='UTF-8') as f:
        tokens,errors = tokenize(f.read())

    for token in tokens:
        print(token)
    print()
    if len(errors):
        print('ERRORS:')
        for error in errors:
            print(error)
