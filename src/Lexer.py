import ply.lex as lex
import sys

tokens = ['INTEGER',  # Non-empty strings of digits 0-9
          'ID',  # Letters, digits, and the underscore character
          'TYPE_ID',  # Begin with a capital letter
          'OBJECT_ID',  # Begin with a lower case letter
          'self', 'SELF TYPE',  # Other identifiers

          'BOOL', 'STRING'

                  'PLUS', 'MINUS', 'MULT', 'DIV', 'EQ',
          'EQ', 'LT', 'LTEQ', 'ASSIGN', 'ACTION', 'INT_COMP',
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'DOT', 'COMMA', 'COLON', 'SEMMICOLON', 'AT',
          ]

keywords = {
    # class <type> [ inherits <type> ] {
    # <feature_list>
    # };
    'class': 'CLASS',
    'inherits': 'INHERITS',

    # new <type>
    'new': 'NEW',

    # isvoid expr evaluates to true if expr is void and evaluates to false if expr is not void.
    'isvoid': 'ISVOID',

    # reads from the standard input
    'in': 'IN',

    # case <expr0> of
    # <id1> : <type1> => <expr1>;
    # . . .
    # <idn> : <typen> => <exprn>;
    # esac
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',

    # if <expr> then <expr> else <expr> fi
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',

    # while <expr> loop <expr> pool
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',

    # let <id1> : <type1> [ <- <expr1> ], ..., <idn> : <typen> [ <- <exprn> ] in <expr>
    'let': 'LET',

    'not': 'NOT'
}

tokens = tokens + list(keywords.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

t_EQ = r'\='
t_LT = r'\<'
t_LTEQ = r'\<\='
t_ASSIGN = r'\<\-'
t_ACTION = r'\=\>'
t_INT_COMP = r'\~'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'

t_AT = r'\@'


# Integers are non-empty strings of digits 0-9.
def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# Booleans are true or false
def t_BOOL(t):
    r'true|false'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False
    return t


# Type identifiers begin with a capital letter
# Object identifiers begin with a lower case letter
def t_TYPES(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'IDENTIFIER')
    if t.type == 'IDENTIFIER':
        if t.value[0].islower():
            t.type = 'OBJECT_ID'
        else:
            t.type = 'TYPE_ID'
    return t


# Identifiers are strings (other than keywords) consisting of
# letters, digits, and the underscore character
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


# \b backspace
# \t tab
# \n newline
# \f formfeed
# def t_STRING_exceptions(t):

states = (("COMMENT", 'exclusive'),)


# COMMENT TYPE 1:  “--” and the next newline (or EOF, if there is no next newline)
def t_COMMENT(t):
    r'\-\-[^\n]*'
    pass


# COMMENT TYPE 2:  enclosing text in (∗ . . . ∗)
def t_start_comment(t):
    r"\(\*"
    t.lexer.push_state("COMMENT")
    t.lexer.comment_count = 0


def t_COMMENT_start(t):
    r"\(\*"
    t.lexer.comment_count += 1


def t_COMMENT_end(t):
    r"\*\)"
    if t.lexer.comment_count == 0:
        t.lexer.pop_state()
    else:
        t.lexer.comment_count -= 1


def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT_error(t):
    t.lexer.skip(1)


# Ignore blanks, tabs, carriage return, form feed)
t_ignore = ' \t\r\f'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


if __name__ == '__main__':
    #coolc [ -o fileout ] file1.cl file2.cl ... filen.cl
    if len(sys.argv) > 1 or sys.argv[0] != 'coolc':
        print('Input Form: coolc [ -o fileout ] file1.cl file2.cl ... filen.cl')
        sys.exit(1)

    lexer = lex.lex()
    files_list = sys.argv[1:].split()
    files_count = len(files_list)
    lexer.num_count = 0

    for file in files_list:
        try:
            with open(file, 'r') as f:
                lexer.input(f.read())
        except:
            print("File not found.")
            exit(1)

        for token in lexer:
            if token is not None:
                print("Token " + "(" + str(token.value) + " " + str(token.type) + ")")
