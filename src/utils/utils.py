import itertools
from semantic.semantic import SelfType


def find_column(text, pos):
    line_start = text.rfind('\n', 0, pos) + 1
    return (pos - line_start) + 1


class Token:
    def __init__(self, lex, token_type, row, column):
        self.lex = lex
        self.type = token_type
        self.lineno = row
        self.column = column

    def __str__(self):
        return f'{self.type}: {self.lex} ({self.lineno}, {self.column})'

    def __repr__(self):
        return str(self)


reserved = {
    'class': 'CLASS',
    'else': 'ELSE',
    'fi': 'FI',
    'if': 'IF',
    'in': 'IN',
    'inherits': 'INHERITS',
    'isvoid': 'ISVOID',
    'let': 'LET',
    'loop': 'LOOP',
    'pool': 'POOL',
    'then': 'THEN',
    'while': 'WHILE',
    'case': 'CASE',
    'esac': 'ESAC',
    'new': 'NEW',
    'of': 'OF',
    'not': 'LNOT',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens = [
    'ID',
    'TYPE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COLON',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'AT',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'EQUAL',
    'LESS',
    'LESSEQ',
    'ARROW',
    'INT',
    'STRING',
    'NOT'
] + list(reserved.values())


def path_to_objet(typex):
    path = []
    c_type = typex

    while c_type:
        path.append(c_type)

        c_type = c_type.parent

    path.reverse()
    return path


def get_common_basetype(types):
    paths = [path_to_objet(typex) for typex in types]
    tuples = zip(*paths)

    for i, t in enumerate(tuples):
        gr = itertools.groupby(t)
        if len(list(gr)) > 1:
            return paths[0][i-1]

    return paths[0][-1]


def get_type(typex, current_type):
    return current_type if typex == SelfType() else typex
