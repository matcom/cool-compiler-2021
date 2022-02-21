import sys
from parsing.parser import COOL_Parser
from parsing.lexer import COOL_Lexer
from tours.TypeCollector import TypeCollector
from tours.TypeBuilder import TypeBuilder
from tours.TypeChecker import TypeChecker


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

# Collecting Types
collector = TypeCollector()
collector.visit(ast)
context = collector.context
errors = collector.errors

# Building Types
builder = TypeBuilder(context, errors)
builder.visit(ast)

# Checking Types
checker = TypeChecker(context, errors)
scope = checker.visit(ast)

if errors:
    for e in errors:
        print(e)
        exit(1)

exit(0)