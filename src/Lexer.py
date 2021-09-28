import ply.lex as lex
import sys

tokens = ['INTEGER',  # Non-empty strings of digits 0-9
          'ID',  # Letters, digits, and the underscore character
          'TYPE_ID',  # Begin with a capital letter
          'OBJECT_ID',  # Begin with a lower case letter
          'self', 'SELF_TYPE',  # Other identifiers

          'BOOL', 'STRING',
          'COMMENT',
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

states = (("STRING", "exclusive"), ("COMMENT", 'exclusive'),)


# Integers are non-empty strings of digits 0-9.
def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
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


# Booleans are true=True or false=False
def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


# Strings are enclosed in double quotes "..."
t_STRING_ignore = ''


# A string start with " caracter
def t_STRING_start(t):
    r'\"'
    t.lexer.push_state("STRING")  # Changes the lexing state and saves old on stack
    t.lexer.string_backslashed = False
    t.lexer.stringbuf = ""  # start string with no chart


# A non-escaped newline character may not appear in a string. Example:
# "This \
# is OK"

# "This is not
# OK"
def t_STRING_newline(t):
    r"\n"
    t.lexer.lineno += 1
    if not t.lexer.string_backslashed:
        print("A non-escaped newline character may not appear in a string")
        t.lexer.skip(1)
    else:
        t.lexer.string_backslashed = False


# Within a string, a sequence ‘\c’ denotes the character ‘c’, with the exception of the following:
# \b backspace
# \t tab
# \f formfeed
# \\ backsalached caracter
# \n newline
# A string may not contain EOF
# A string may not contain the null
def t_STRING_no_newline(t):
    r"[^\n]"
    if not t.lexer.string_backslashed:  # if the previosur chat is not '\'
        if t.value == '\\':
            t.lexer.string_backslashed = True  # backsalached caracter
        else:
            t.lexer.stringbuf += t.value  # no backsalached caracter situation
    else:
        t.lexer.string_backslashed = False
        if t.value == 0:  # A string may not contain the null (character \0). Check for EOF??
            print('A string may not contain the null')
            t.lexer.skip(1)
        elif t.value == 'b':  # \b backspace
            t.lexer.stringbuf = '\b'
        elif t.value == 't':  # \t tab
            t.lexer.stringbuf = '\t'
        elif t.value == 'f':  # \f formfeed
            t.lexer.stringbuf = '\f'
        elif t.value == '\\':  # \\ backsalached caracter
            t.lexer.stringbuf = '\\'
        else:
            t.lexer.stringbuf += t.value


# A string ends with " caracter
def t_STRING_end(t):
    r"\""
    if t.lexer.string_backslashed:
        t.lexer.stringbuf += '"'
        t.lexer.string_backslashed = False
    else:
        t.lexer.pop_state()
        t.value = t.lexer.stringbuf
        return t


# String Error handling
def t_STRING_error(t):
    print("Illegal string character '%s'" % t.value[0])
    t.lexer.skip(1)


# Exist two forms of comments in Cool:
# Type1: Any characters between two dashes “--” and the next newline (or EOF, if there is no next newline)
# Type2: Enclosing text in (∗ . . . ∗)
t_COMMENT_ignore = ''


# COMMENT TYPE 1:  “--” and the next newline (or EOF, if there is no next newline)
def t_COMMENT(t):
    r'\-\-[^\n]*'
    pass


# COMMENT TYPE 2:  enclosing text in (∗ . . . ∗)
def t_start_comment(t):
    r"\(\*"
    t.lexer.push_state("COMMENT")  # Changes the lexing state and saves old on stack
    t.lexer.comment_count = 0


# A comment start with " (* "
def t_COMMENT_start(t):
    r"\(\*"
    t.lexer.comment_count += 1


# A comment can has as many lines as it wants.. until the end comment " *) "
def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A comment finish with " *) "
def t_COMMENT_end(t):
    r"\*\)"
    if t.lexer.comment_count == 0:
        t.lexer.pop_state()
    else:
        t.lexer.comment_count -= 1


# Comment Error handling
def t_COMMENT_error(t):
    t.lexer.skip(1)


# Ignore blanks, tabs, carriage return, form feed
t_ignore = ' \t\r\f'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# if __name__ == '__main__':
#     # coolc [ -o fileout ] file1.cl file2.cl ... filen.cl
#     if len(sys.argv) > 1 or sys.argv[0] != 'coolc':
#         print('Input Form: coolc [ -o fileout ] file1.cl file2.cl ... filen.cl')
#         sys.exit(1)
#
#     lexer = lex.lex()
#     files_list = sys.argv[1:].split()
#     files_count = len(files_list)
#     lexer.num_count = 0
#
#     for file in files_list:
#         try:
#             with open(file, 'r') as f:
#                 lexer.input(f.read())
#         except:
#             print("File not found.")
#             exit(1)
#
#         for token in lexer:
#             if token is not None:
#                 print("Token " + "(" + str(token.value) + " " + str(token.type) + ")")

def tokenize(text):
    lexer = lex.lex()
    lexer.input(text)
    return lexer
