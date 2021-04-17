import sys
from parsing.parser import COOL_Parser
from parsing.lexer import COOL_Lexer

input_file = sys.argv[1]
with open(input_file, 'r') as f:
    s = f.read()

lexer = COOL_Lexer()
lexer.build()
tokens = list(lexer.tokenize(s))
if lexer.errors:
    for e in lexer.errors:
        print(e)
    exit(1)

parser = COOL_Parser()
ast, errors = parser.parse(s)
if errors:
    for e in errors:
        print(e)
        exit(1)
exit(0)