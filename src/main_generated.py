from itertools import chain
from typing import Union, List, Tuple
import sys
import type_collector
import type_builder
import type_checker
from lexer_cool import Lexer
from parser_cool import Parser
from generated_utils.token_class import Match
from main_regex import RegexCompilator, RegexExpr
from translate_cool_cil import COOLToCILVisitor
from translate_cil_mips import CILToMIPSVisitor
from utils.utils import display_errors
import ast_cool_hierarchy as ast
import ast_cool_h_extender as to_ast

if not len(sys.argv) > 1:
    exit(1)


class CoolMatch(Match):
    def __init__(self):
        self.match_ = dict()
        self.compiled: Union[List[Tuple[str, RegexExpr]], None] = None
        self.reg_comp = RegexCompilator()

    def add_matcher(self, to_add):
        if not self.compiled:
            self.match_[to_add[0]] = to_add[1:]

    def initialize(self):
        if self.compiled is None:
            self.compiled = []
            for name, matcher in self.match_.items():
                regex = matcher[0]
                pattern = self.reg_comp.compile(regex)
                self.compiled.append((name, pattern))

    def match(self, match, pos):
        matched_expr = ""
        matched_str = None
        matched_bool = False
        for str_, expr in self.compiled:
            match_, bool_match_ = expr.match(match, pos)
            if len(match_) > len(matched_expr) or (
                    len(match_) == len(matched_expr) and not matched_bool and bool_match_):
                matched_str = str_
                matched_expr = match_
                matched_bool = bool_match_

        matched_extra = (False, [])
        if matched_bool:
            matched_extra = self.match_[matched_str][1] if self.match_[matched_str][1] else matched_extra
        return (matched_str, matched_expr, matched_extra, matched_bool)


lexer = Lexer(CoolMatch(), to_ast.TOKEN_TYPE)
astsum = {k: v for k, v in chain.from_iterable([to_ast.__dict__.items(), ast.__dict__.items()])}
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

with open(f'{sys.argv[1][:-3]}.mips', 'w') as f:
    f.write(f'{mips_code}')
