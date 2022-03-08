from itertools import chain
import sys
import type_collector
import type_builder
import type_checker
from lexer_cool import Lexer
from parser_cool import Parser
from translate_cool_cil import COOLToCILVisitor
from translate_cil_mips import CILToMIPSVisitor
from utils.utils import display_errors
import ast_cool_hierarchy as ast
import ast_cool_h_extender as to_ast
from match_cool_class import CoolMatch

if not len(sys.argv) > 1:
    exit(1)

lexer = Lexer(CoolMatch(), to_ast.TOKEN_TYPE)
astsum = {
    k: v
    for k, v in chain.from_iterable([to_ast.__dict__.items(), ast.__dict__.items()])
}
parser = Parser(astsum, to_ast.TOKEN_TYPE)

input_file = sys.argv[1]
with open(input_file, encoding="utf-8") as file:
    cool_program_code = file.read()

# Lexer
tokens, errors = lexer(cool_program_code)
for token in tokens:
    pass
display_errors(errors)

# Parser
cool_ast, errors = parser(tokens)
display_errors(errors)

# Semantic
collector = type_collector.TypeCollector(errors)
collector.visit(cool_ast)
context = collector.context
builder = type_builder.TypeBuilder(context, errors)
builder.visit(cool_ast)
checker = type_checker.TypeChecker(context, errors)
checker.visit(cool_ast)
display_errors(errors)

# Code generation
cool_to_cil = COOLToCILVisitor(context)
cil_ast = cool_to_cil.visit(cool_ast)
cil_to_mips = CILToMIPSVisitor()
mips_code = cil_to_mips.visit(cil_ast)

with open(f"{sys.argv[1][:-3]}.mips", "w") as f:
    f.write(f"{mips_code}")
