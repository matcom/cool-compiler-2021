import sys
import os
from lexer import tokenize, lexer_errors

programs_directory = sys.argv[1]
programs_files = [file for file in os.listdir(programs_directory) if file.endswith('.cl')]

for program_file in programs_files:
    input('Press enter to analyze ' + program_file)
    program_route = programs_directory+'/'+program_file
    with open(program_route, 'r') as f:
        tokens = tokenize(f.read())

    for token in tokens:
        pass
    print(lexer_errors)
