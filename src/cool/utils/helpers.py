import itertools
from semantic.types import Type, SelfType


def find_column(lexer, token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
    return token.lexpos - line_start


def get_type(typex: Type, current_type: Type) -> Type:
    return current_type if typex == SelfType() else typex
