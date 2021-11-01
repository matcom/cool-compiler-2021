import itertools
from ..semantic.types import Type, SelfType
from typing import List
from .errors import SemanticError, TypesError


def find_column(lexer, token):
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
    return token.lexpos - line_start


def get_type(typex: Type, current_type: Type) -> Type:
    return current_type if typex == SelfType() else typex


def path_to_objet(_type):
    path = []
    c_type = _type

    while c_type:
        path.append(c_type)
        c_type = c_type.parent

    path.reverse()

    return path


def get_common_base_type(types):
    paths = [path_to_objet(_type) for _type in types]
    tuples = zip(*paths)

    for i, t in enumerate(tuples):
        gr = itertools.groupby(t)
        if len(list(gr)) > 1:
            return paths[0][i - 1]

    return paths[0][-1]
