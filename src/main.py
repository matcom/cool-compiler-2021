
from parsing.parser import COOL_Parser
from parsing.lexer import COOL_Lexer
from tours.TypeCollector import TypeCollector
from tours.TypeBuilder import TypeBuilder
from tours.TypeChecker import TypeChecker
from tours.TypeInferencer import TypeInferencer
from tours.utils import AnalizeScopeAutoTypes, AnalizeClassAutoTypes

input_file = "test.txt"
with open(input_file, 'r') as f:
    s = f.read()

lexer = COOL_Lexer()
lexer.build()

tokens = list(lexer.tokenize(s))
if lexer.errors:
    for e in lexer.errors:
        print(e)
    #exit(1)

parser = COOL_Parser()
ast, errors = parser.parse(s)
if errors:
    for e in errors:
        print(e)

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

# Infering Types
while True:
    inferencer = TypeInferencer(context, errors)
    if not inferencer.visit(ast):
        break

inferences = []
for declaration in ast.declarations:
    AnalizeClassAutoTypes(context.get_type(declaration.id), errors, inferences)
AnalizeScopeAutoTypes(scope, errors, inferences)

print("Infered Types:")
if inferences:
    for inf in inferences:
        print(inf)
else:
    print("There wasn't any variable type infered.")

# Print Errors
print("Errors:")
if errors:
    for error in errors:
        print(error)
else:
    print("There wasn't any error in the code entered.")
