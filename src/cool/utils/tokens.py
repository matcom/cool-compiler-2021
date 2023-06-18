from typing import Dict, List

ignored: List[str] = [' ', '\f', '\r', '\t', '\v']

reservedKeywords: Dict[str, str] = {
    'class': 'class',
    'else': 'else',
    'false': 'false',
    'fi': 'fi',
    'if': 'if',
    'in': 'in',
    'inherits': 'inherits',
    'isvoid': 'isvoid',
    'let': 'let',
    'loop': 'loop',
    'pool': 'pool',
    'then': 'then',
    'while': 'while',
    'case': 'case',
    'esac': 'esac',
    'new': 'new',
    'of': 'of',
    'not': 'not',
    'true': 'true'
}

literals: List[str] = [
    'semi',     # '; '
    'colon',    # ': '
    'comma',    # ', '
    'dot',      # '. '
    'opar',     # '( '
    'cpar',     # ') '
    'ocur',     # '{'
    'ccur',     # '} '
    'larrow',   # '<-'
    'arroba',   # '@'
    'rarrow',   # '=> '
    'nox',      # '~'
    'equal',    # '='
    'plus',     # '+'
    'minus',    # '-'
    'star',     # '\*'
    'div',      # '/ '
    'less',     # '<'
    'lesseq',   # '<='
    'id',
    'type',
    'num', 
    'string'
]

tokens = list(reservedKeywords.values()) + literals

class Token:
    def __init__(self, lex: str, type_: str, lineno: int, pos: int):
        self.lex = lex
        self.type = type_
        self.lineno = lineno
        self.pos = pos

    def __str__(self):
        return f'{self.type}: {self.lex} ({self.lineno}, {self.pos})'

    def __repr__(self):
        return str(self)