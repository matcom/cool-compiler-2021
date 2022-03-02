import sys
from parsing.parser import COOL_Parser
from parsing.lexer import COOL_Lexer
from semantics.TypeCollector import TypeCollector
from semantics.TypeBuilder import TypeBuilder
from semantics.TypeChecker import TypeChecker
from codegen.generate_ast import CIL
from codegen.cil_codegen import CILCodegen
from codegen.spim_scope import MIPSScopeBuilder
from codegen.spim_visitor import MIPSCodegen
input_file = sys.argv[1]
with open(input_file, 'r') as f:
    s = f.read()

lexer = COOL_Lexer()
lexer.input(s)
a = list(lexer.output)
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
checker.visit(ast)

if errors:
    for e in errors:
        print(e)
        exit(1)
        
cil_generator = CIL(context)
cil = cil_generator.visit(ast)
#print(cil)
cil_codegen = CILCodegen()
code = cil_codegen.visit(cil)


mips_scope_builder = MIPSScopeBuilder()
scope = mips_scope_builder.visit(cil)
#print(scope)
mips_codegen = MIPSCodegen(scope)
mips_codegen.visit(cil, None)
#print(mips_codegen.code)
with open(f'{input_file[:-3]}.mips', 'w') as f:
    f.write(mips_codegen.code)
with open(f'{input_file[:-3]}.cil', 'w') as f:
    f.write(code)
exit(0)
