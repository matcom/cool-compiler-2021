from . import lexing_rules
from ply import lex

lexer = lex.lex(module=lexing_rules)
# Set starting col
lexer.col = 1
lexer.errors = []
