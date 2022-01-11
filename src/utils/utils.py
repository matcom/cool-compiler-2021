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
    'not': 'LNOT'
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
    'NOT',
    'BOOL'
] + list(reserved.values())
