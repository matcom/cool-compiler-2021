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
            'OBJECTID',
            'TYPEID',
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


        def t_COMMENTMULTI(t):
            r'\(\*(.|\n)*?\*\)'
            t.lexer.lineno += t.value.count("\n")

        def t_COMMENTMULTIUNFINISHED(t):
            r'\(\*(.|\n)*'
            t.lexer.lineno += t.value.count("\n")
            msg = 'EOF in comment'
            self.add_error(LexerCoolError(msg, PlyCoolToken(t.value, t.type, t.lexer.lineno - 1, t.lexer.lexpos - 1)))

        def t_STRING(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}"'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, PlyCoolToken(t.value, t.type, line, pos)))
            return t

        def t_STRINGUNFINISHED(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}\n'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, PlyCoolToken(t.value, t.type, line, pos)))
            msg = 'Unfinished string constant'
            self.add_error(LexerCoolError(msg, PlyCoolToken(t.value, t.type, t.lexer.lineno - 1, t.lexer.lexpos - 1)))

        def t_STRINGUNFINISHEDEOF(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, PlyCoolToken(t.value, t.type, line, pos)))
            msg = 'EOF in string constant'
            self.add_error(LexerCoolError(msg, PlyCoolToken(t.value, t.type, t.lexer.lineno, t.lexer.lexpos)))

        def t_NUMBER(t):
            r'\d+'
            try:
                int(t.value)
            except ValueError:
                msg = "Integer value too large %d", t.value
                self.add_error(LexerCoolError(msg, PlyCoolToken(t.value, t.type, t.lineno, t.lexpos))) # TODO Set Token column
                t.value = 'Invalid'
            return t

        def t_OBJECTID(t):
            r'[a-z][a-zA-Z0-9_]*'
            low = t.value.lower()
            t.type = reserved.get(low,'OBJECTID')
            return t

        def t_TYPEID(t):
            r'[A-Z][a-zA-Z0-9_]*'
            low = t.value.lower()
            if low == 'true':
                t.type = 'TYPEID'

            elif low == 'false':
                t.type = 'TYPEID'

            else:
                t.type = reserved.get(low, 'TYPEID')

            return t

        def t_COMMENTSINGLE(t):
            r'(--.*)'
        

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

        for error in self.error_tracker.get_errors():
            error.token.set_position(error.token.lineno, self.find_column(program_string, error.token))
            
        return result

    def add_error(self, error:LexerCoolError):
        self.error_tracker.add_error(error)
    
    def get_errors(self)->List[LexerCoolError]:
        errors = self.error_tracker.get_errors()
        return errors
