from Lexer.tokens import COOL_Tokens
from Lexer.errors_types import *
import ply.lex as lex
import sys

class COOL_Lexer:

    def __init__(self):
        self.t = COOL_Tokens()
        self.tokens = self.t.tokens
        self.errors = False
        self.states = [('STRING', 'exclusive'), ('COMMENT', 'exclusive')]
        self.linelastpos = [-1]
        self.lexer = lex.lex(module = self)

    #===============================================================================================================================================

    # SIMPLE TOKENS
    t_LPAREN =    r'\('  # (
    t_RPAREN =    r'\)'  # )
    t_LBRACE =    r'\{'  # {
    t_RBRACE =    r'\}'  # }
    t_COLON =     r'\:'  # :
    t_COMMA =     r'\,'  # ,
    t_DOT =       r'\.'  # .
    t_SEMICOLON = r'\;'  # ;
    t_AT =        r'\@'  # @
    t_MULTIPLY =  r'\*'  # *
    t_DIVIDE =    r'\/'  # /
    t_PLUS =      r'\+'  # +
    t_MINUS =     r'\-'  # -
    t_INT_COMP =  r'~'  # ~
    t_LT =        r'\<'  # <
    t_EQ =        r'\='  # =
    t_LTEQ =      r'\<\='  # <=
    t_ASSIGN =    r'\<\-'  # <-
    t_ARROW =     r'\=\>'  # =>

    def t_BOOL_TYPE(self, t):
        r'(true|false)'
        t.value = True if t == "true" else False
        t.type = "BOOLEAN"
        return t
    
    def t_INT_TYPE(self, t):
        r'\d+'
        t.value = int(t.value)
        t.type = "INTEGER"
        return t

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        if t.value.lower() in list(self.t.cool_keywords.keys()):
            t.value = t.value.lower()
            t.type = self.t.cool_keywords[t.value]
            return t
        t.type = 'TYPE'
        return t

    def t_ID(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.t.cool_keywords.get(t.value.lower(), 'ID')
        return t

    t_ignore = ' \t\r\f'

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.linelastpos.append(t.lexpos)

    def t_error(self, t):
        """
        Error Handling and Reporting Rule.
        """
        sys.stdout.write(f'({t.lineno}, {t.lexpos - self.linelastpos[len(self.linelastpos)-1]}) - {LXERR} "{t.value[0]}"\n')
        self.errors = True
        t.lexer.skip(1)
    
    #===============================================================================================================================================
    # THE STRING STATE
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def t_begin_STRING(self, t):
        r'"'
        t.lexer.begin("STRING")
        t.lexer.string_backslashed = False
        t.lexer.stringbuf = ""

    def t_STRING_newline(self, t):
        r'\n'
        t.lexer.lineno += 1

        if not t.lexer.string_backslashed:
            sys.stdout.write(f'({t.lineno}, {t.lexpos - self.linelastpos[len(self.linelastpos)-1]}) - {LXUSC}\n')
            self.errors = True
            t.lexer.begin("INITIAL")
        else:
            t.lexer.string_backslashed = False
        self.linelastpos.append(t.lexpos)

    def t_STRING_end(self, t):
        r'"'
        if not t.lexer.string_backslashed:
            t.lexer.begin("INITIAL")
            t.value = t.lexer.stringbuf
            t.type = "STRING"
            return t
        else:
            t.lexer.stringbuf += '"'
            t.lexer.string_backslashed = False

    def t_STRING_anything(self, t):
        r'[^\n\x00]'
        if t.lexer.string_backslashed:
            if t.value in ['b', 't', 'n', 'f', '\\']:
                t.lexer.stringbuf += '\\'
            t.lexer.stringbuf += t.value
            t.lexer.string_backslashed = False
        else:
            if t.value != '\\':
                t.lexer.stringbuf += t.value
            else:
                t.lexer.string_backslashed = True

    t_STRING_ignore = ''

    def t_STRING_error(self, t):
        sys.stdout.write(f'({t.lineno}, {t.lexpos - self.linelastpos[len(self.linelastpos)-1]}) - {LXSCN}\n')
        self.errors = True
        t.lexer.skip(1)
    
    def t_STRING_eof(self, t):
        sys.stdout.write(f'({t.lineno}, {t.lexer.lexlen - self.linelastpos[len(self.linelastpos)-1]}) - {LXESC}\n')
        self.errors = True
    
    #===============================================================================================================================================
    # THE COMMENT STATE
    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def t_begin_COMMENT(self, t):
        r'\(\*'
        t.lexer.begin("COMMENT")
        t.lexer.comment_count = 1

    def t_COMMENT_startanother(self, t):
        r'\(\*'
        t.lexer.comment_count += 1

    def t_COMMENT_end(self, t):
        r'\*\)'
        if t.lexer.comment_count == 1:
            t.lexer.begin("INITIAL")
        else:
            t.lexer.comment_count -= 1
    
    t_ignore_SINGLE_LINE_COMMENT = r"\-\-[^\n]*"
    t_COMMENT_ignore = ''

    def t_COMMENT_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.linelastpos.append(t.lexpos)
    
    def t_COMMENT_error(self, t):
        t.lexer.skip(1)
    
    def t_COMMENT_eof(self, t):
        sys.stdout.write(f'({t.lineno}, {t.lexer.lexlen - self.linelastpos[len(self.linelastpos)-1]}) - {LXEIC}\n')
        self.errors = True

    #===============================================================================================================================================