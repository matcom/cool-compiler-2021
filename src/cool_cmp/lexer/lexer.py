"""
Lexer usando ply
"""
from typing import List, Tuple

from cool_cmp.lexer.interface import ILexer
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared.errors import ErrorTracker
from cool_cmp.lexer.errors import LexerCoolError
import ply.lex as lex

class PlyCoolToken(lex.LexToken, ICoolToken):

    def __init__(self, lex:str, typex:str, line:int, column:int):
        self.set_lex(lex)
        self.set_type(typex)
        self.set_position(line, column)

    def set_lex(self, lex:str):
        self.lex = lex
        self.value = lex

    def set_type(self, typex:str):
        self.type = typex
        self.typex = typex

    def set_position(self, line:int, column:int):
        self.lineno = line
        self.line = line
        self.column = column
        self.lexpos = column

    def get_lex(self)->str:
        return self.lex

    def get_type(self)->str:
        return self.typex

    def get_position(self)->Tuple[int,int]:
        return (self.line, self.column)

    def __str__(self):
        return f"{self.lex}:{self.type} Line {self.line} Column{self.column}"

    def __repr__(self):
        return str(self)

class PlyLexer(ILexer):

    @staticmethod
    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def __init__(self):
        self.error_tracker = ErrorTracker() # Error tracker implementation

        reserved = {
            'if' : 'IF',
            'then' : 'THEN',
            'fi' : 'FI',
            'else' : 'ELSE',
            'case' : 'CASE',
            'of' : 'OF',
            'esac' : 'ESAC',
            'class' : 'CLASS',
            'inherits' : 'INHERITS',
            'let' : 'LET',
            'in' : 'IN',
            'while' : 'WHILE',
            'loop' : 'LOOP',
            'pool' : 'POOL',
            'new' : 'NEW',
            'isvoid' : 'ISVOID',
            'not' : 'NOT',
            'true' : 'TRUE',
            'false' : 'FALSE'
        }

        tokens = (
            'ID',
            'NUMBER',
            'PLUS',
            'MINUS',
            'STAR',
            'DIV',
            'EQ',
            'LEQ',
            'LESS',
            'NEG',
            'OPAR',
            'CPAR',
            'OCUR',
            'CCUR',
            'ASSIGN',
            'SEMI',
            'COLON',
            'SIGNALER',
            'ARROBA',
            'STRING',
            'COMMENT',
            'DOT',
            'COMMA'
        ) + tuple(reserved[x] for x in reserved.keys())


        t_STRING = r'"([^\n"\\]|(\\.)){0,1024}"'

        def t_NUMBER(t):
            r'\d+'
            try:
                int(t.value)
            except ValueError:
                msg = "Integer value too large %d", t.value
                self.add_error(LexerCoolError(msg, PlyCoolToken(t.value, t.type, t.lineno, t.lexpos))) # TODO Set Token column
                t.value = 'Invalid'
            return t

        def t_ID(t):
            r'[a-zA-Z_][a-zA-Z0-9_]*'
            low = t.value.lower()
            if (t.value[0] == 't' or t.value[0] == 'f') and (reserved.get(low) == 'TRUE' or reserved.get(low) == 'FALSE'):
                t.type = reserved.get(low)
            else:
                t.type = reserved.get(t.value,'ID')
            return t

        def t_COMMENT(t):
            r'(--.*)|(\(\*(.|\n)*\*\))'

        t_PLUS      = r'\+'
        t_MINUS     = r'-'
        t_STAR      = r'\*'
        t_DIV       = r'/'
        t_OPAR      = r'\('
        t_CPAR      = r'\)'
        t_OCUR      = r'\{'
        t_CCUR      = r'\}'
        t_EQ        = r'='
        t_ASSIGN    = r'<-'
        t_LEQ       = r'<='
        t_LESS      = r'<'
        t_NEG       = r'~'
        t_SEMI      = r';'
        t_COLON     = r':'
        t_SIGNALER  = r'=>'
        t_ARROBA    = r'@'
        t_DOT       = r'\.'
        t_COMMA     = r','

        t_ignore = " \t"

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")

        def t_error(t):
            msg = f'ERROR "{t.value[0]}"'
            self.add_error(LexerCoolError(msg, PlyCoolToken(t.value[0], t.type, t.lineno, t.lexpos))) # TODO Set Token column
            t.lexer.skip(1)

        self.lexer = lex.lex()

    def __call__(self, program_string:str):
        self.lexer.input(program_string)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append(PlyCoolToken(tok.value, tok.type, tok.lineno, self.find_column(program_string, tok)))
        return result

    def add_error(self, error:LexerCoolError):
        self.error_tracker.add_error(error)
    
    def get_errors(self)->List[LexerCoolError]:
        errors = self.error_tracker.get_errors()
        return errors
