import ply.lex as lex
from utils.errors import *

class CoolLexer:

    def __init__(self, **kwargs):
        self.errors = []
        self.lexer = lex.lex(modele=self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0 

    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive')
    )

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
        'not': 'NOT',
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
        'NOT'
    ] + list(reserved.values())

    # Comments
    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos

    def t_comments(self, t):
        r'\(\*'
        t.lexer.level = 1
        t.lexer.begin('comments')

    def t_comments_open(self, t):
        r'\(\*'
        t.lexer.level += 1
 
    def t_comments_close(self, t):
        r'\*\)'
        t.lexer.level -= 1
        if t.lexer.level == 0:
            t.lexer.begin('INITIAL')
    
    def t_comments_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos

    def t_comments_error(self, t):
        t.lexer.skip(1)
    
    def t_comments_eof(self, t):
        line = t.lexer.lineno
        column = self.find_column(t)
        add_lexer_error(line, column, "EOF in comment")

    t_comments_ignore = '  \t\f\r\v'
    
    # Strings 
    t_strings_ignore = ''

    def t_strings(self, t):
        r'\"'
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string = ''
        t.lexer.backslash = False
        t.lexer.begin('string')

    def t_strings_end(self, t):
        r'\"'
        self.add_row_column(t)

        if  t.lexer.backslash:
            t.lexer.string += '"'
            t.lexer.backslash = False
        else:
            t.value = t.lexer.string
            t.type = 'string'
            t.lexer.begin('INITIAL')
            return t
        
    def t_strings_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.add_row_column(t)

        t.lexer.linestart = t.lexer.lexpos

        if not t.lexer.backslash:
            add_lexer_error(t.row, t.column, 'Undeterminated string constant')
            t.lexer.begin('INITIAL')

    def t_strings_nill(self, t):
        r'\0'
        self.add_row_column(t)
        add_lexer_error(t.row, t.column, 'Null caracter in string')

    def t_strings_consume(self, t):
        r'[^\n]'

        if t.lexer.backslash:
            if t.value == 'b':
                t.lexer.string += '\b'
            elif t.value == 't':
                t.lexer.string += '\t'
            if t.value == 'f':
                t.lexer.string += '\f'
            elif t.value == 'n':
                t.lexer.string += '\n'
            elif t.value == '\\':
                t.lexer.string += '\\'
            else:
                t.lexer.string += t.value

            t.backslash = FALSE
        else:
            if t.value != '\\':
                t.lexer.string += t.value
            else:
                t.lexer.backslash = True

    def t_strings_eof(self, t):
        self.add_row_column(t)
        add_lexer_error(t.row, r.column, 'EOF in string constant')

    def find_column(self, t):
        line_start = self.text.rfind('\n', 0, t.lexpos) + 1
        return (t.lexpos - line_start) + 1

    def add_row_column(self, t):
        t.row = t.lexer.lineno
        t.column = self.find_column(t)

    t_ignore = '  \t\f\r\t\v'

    def t_LPAREN(self, t):
        r'\('
        self.add_row_column(t)
        return t

    def t_RPAREN(self, t):
        r'\)'
        self.add_row_column(t)
        return t

    def t_LBRACE(self, t):
        r'\{'
        self.add_row_column(t)
        return t

    def t_RPAREN(self, t):
        r'\}'
        self.add_row_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.add_row_column(t)
        return t

    def t_SEMICOLON(self, t):
        r';'
        self.add_row_column(t)
        return t

    def t_COMMA(self, t):
        r','
        self.add_line_column(t)
        return t

    def t_DOT(self, t):
        r'\.'
        self.add_row_column(t)
        return t

    def t_AT(self, t):
        r'@'
        self.add_row_column(t)
        return t

    def t_ASSIGN(self, t):
        r'<-'
        self.add_row_column(t)
        return t

    def t_PLUS(self, t):
        r'\+'
        self.add_row_column(t)
        return t

    def t_MINUS(self, t):
        r'-'
        self.add_row_column(t)
        return t

    def t_STAR(self, t):
        r'\*'
        self.add_row_column(t)
        return t

    def t_DIV(self, t):
        r'/'
        self.add_row_column(t)
        return t

    def t_EQUAL(self, t):
        r'='
        self.add_row_column(t)
        return t

    def t_LESS(self, t):
        r'<'
        self.add_row_column(t)
        return t

    def t_LESSEQ(self, t):
        r'<='
        self.add_row_column(t)
        return t

    def t_ARROW(self, t):
        r'=>'
        self.add_row_column(t)
        return t

    def t_NOT(self, t):
        r'~'
        self.add_row_column(t)
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        self.add_row_column(t)
        return t

    def t_ID(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        self.add_row_column(t)
        return t

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'TYPE')
        self.add_row_column(t)
        return t

    def t_newline(self, t):
        

    





