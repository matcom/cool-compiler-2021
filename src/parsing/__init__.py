from ply import yacc
from . import parsing_rules

parser = yacc.yacc(module=parsing_rules)
