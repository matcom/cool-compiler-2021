from ply import lex
from ply.lex import TOKEN


import coolcmp.errors as err
from coolcmp.utils import find_column

states = (
    ('STR', 'exclusive'),
    ('COMM', 'exclusive')
)

reserved = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'let': 'LET',
    'new': 'NEW',
    'isvoid': 'ISVOID',
    'not': 'NOT',
    'in': 'IN',
}

tokens = [
    # Identifiers
    'TYPE', 'ID',

    # Built-in types
    'INT', 'STRING', 'BOOL',

    # Special Notation
    'PLUS', 'MINUS', 'STAR', 'DIV', 'LESS', 'LEQ', 'EQ', 'COMP',
    'COLON', 'SEMI', 'COMMA', 'DOT', 'ASSIGN', 'ARROW', 'AT',
    'OPAR', 'CPAR', 'OCUR', 'CCUR'

] + list(reserved.values())

# Tokens defined as strings go after defined in functions.
# This order is not relevant, they are ordered by length (longer first).
t_PLUS = r'\+'
t_MINUS = r'\-'
t_STAR = r'\*'
t_DIV = r'\/'
t_LESS = r'\<'
t_LEQ = r'\<\='
t_EQ = r'\='
t_COMP = r'\~'
t_COLON = r'\:'
t_SEMI = r'\;'
t_COMMA = r'\,'
t_DOT = r'\.'
t_ASSIGN = r'\<\-'
t_ARROW = r'\=\>'
t_AT = r'\@'
t_OPAR = r'\('
t_CPAR = r'\)'
t_OCUR = r'\{'
t_CCUR = r'\}'

t_ignore = ' \t\f\r'
t_ignore_comment = r'\-\-[^\n]*'


# #########################
# ##### INITIAL state #####
# #########################

# match types
@TOKEN(r'[A-Z]\w*')
def t_TYPE(t: lex.LexToken) -> lex.LexToken:
    if t.value[0] in ('t', 'f') and t.value.lower() in ('true', 'false'):
        t.type = 'BOOL'
    else:
        t.type = reserved.get(t.value.lower(), 'TYPE')

    return t


# match ids
@TOKEN(r'[a-z]\w*')
def t_ID(t: lex.LexToken) -> lex.LexToken:
    if t.value[0] in ('t', 'f') and t.value.lower() in ('true', 'false'):
        t.type = 'BOOL'
    else:
        t.type = reserved.get(t.value.lower(), 'ID')

    return t


# match integers
@TOKEN(r'\d+')
def t_INT(t: lex.LexToken) -> lex.LexToken:
    t.value = int(t.value)

    return t


# also defined for COMM state, newline tracker
@TOKEN(r'\n+')
def t_INITIAL_COMM_newline(t: lex.LexToken):
    t.lexer.lineno += len(t.value)


# in case of error
def t_error(t: lex.LexToken):
    t.lexer.skip(1)

    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.LEX_ERROR % (line, col, t.value[0]))


# #####################
# ##### STR state #####
# #####################

t_STR_ignore = ''


@TOKEN(r'"')
def t_begin_STR(t: lex.LexToken):
    t.lexer.string_start = t.lexer.lexpos - 1
    t.lexer.push_state('STR')


@TOKEN(r'"')
def t_STR_end(t: lex.LexToken) -> lex.LexToken:
    t.value = t.lexer.lexdata[t.lexer.string_start: t.lexer.lexpos]
    t.type = 'STRING'
    t.lexer.pop_state()

    return t


@TOKEN(r'\n+')
def t_STR_newline(t: lex.LexToken):
    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.UNT_STR % (line, col))

    t.lexer.lineno += len(t.value)
    t.lexer.pop_state()


@TOKEN(r'\\(.|\n)')
def t_STR_escaped(t: lex.LexToken):
    lookahead = t.value[1]

    if lookahead == '\n':
        t.lexer.lineno += 1


@TOKEN(r'\x00')
def t_STR_null(t: lex.LexToken):
    t.lexer.skip(1)
    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.NULL_STR % (line, col))


@TOKEN(r'[^"\n\\\x00]+')
def t_STR_char(t: lex.LexToken):
    pass


def t_STR_error(t: lex.LexToken):
    t.lexer.skip(1)
    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.EOF_STR % (line, col))


def t_STR_eof(t: lex.LexToken):
    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.EOF_STR % (line, col))


# ######################
# ##### COMM state #####
# ######################

t_COMM_ignore = ''


@TOKEN(r'\(\*')
def t_begin_COMM(t: lex.LexToken):
    t.lexer.comment_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.push_state('COMM')


@TOKEN(r'\(\*')
def t_COMM_new(t: lex.LexToken):
    t.lexer.level += 1


@TOKEN(r'\*\)')
def t_COMM_end(t: lex.LexToken):
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.lexer.pop_state()


def t_COMM_error(token):
    token.lexer.skip(1)


def t_COMM_eof(t: lex.LexToken):
    line, col = t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)
    errors.append(err.EOF_COMM % (line, col))


errors = []
lexer = lex.lex()
