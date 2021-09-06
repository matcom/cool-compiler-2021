import ply.lex as lex


def find_column(input, lexpos):
    line_start = input.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1


class CoolLexer:


reserved = {
    'class': 'CLASS',
    'else': 'ELSE',
    'false': 'FALSE',
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
    'not': 'NOT'
    'true': 'TRUE'
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
    'BOOLEAN',
    'NOT'
]
