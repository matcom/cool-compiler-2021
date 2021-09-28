import sys
from Lexer import tokenize

program_file = sys.argv[1]
with open(program_file, 'r') as f:
    tokens = tokenize(f.read())

for token in tokens:
    print(token)
