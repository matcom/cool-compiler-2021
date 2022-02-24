from sly import Lexer
from .comment_lexer import CoolComment
from .string_lexer import CoolString
import re

class CoolLexer(Lexer):
    def __init__(self, error=None) -> None:
        super().__init__()
        self.cool_error = error

    tokens = {
        CLASS, INHERITS,
        IF, THEN, ELSE, FI,
        LET, IN,
        WHILE, LOOP, POOL,
        CASE, OF, ESAC,
        ISVOID, NEW, NOT,
        TRUE, FALSE,
        ID, NUMBER, TYPE,
        ARROW, LOGICAR, LESS_OR, 
        STRING
    }

    literals = {
        '{','}', '@', '.', ',', ';',
        '=', '<', '~', '+', '-',
        '*', '/', '(', ')', ':',
    }
    
    ignore = r' '
    ignore_tab = r'\t'
    ignore_comment = r'\(\*'
    ignore_newline = r'\n'
    ignore_line = r'--.*\n'

    keyword = [ "class", 'inherits',
                'if', 'then', 'else', 'fi',
                'let', 'in',
                'while', 'loop', 'pool',
                'case', 'of' , 'esac',
                'isvoid', 'new', 'not',
                'true','false'
    ]
 
    ID      = r'[a-zA-Z][a-zA-Z0-9_]*'
    NUMBER  = r'\d+'
    ARROW   = r'<-'
    LOGICAR = r'=>'
    LESS_OR = r'<='
    STRING  = r'\"'

    def ID(self, token):
        if token.value.lower() in self.keyword:
            token.type = token.value.upper()
        elif not token.value[0].islower():
            token.type = "TYPE"
        
        return  token

    def ignore_line(self, token):
        self.lineno += 1

    def ignore_newline(self,token):
        self.lineno += 1

    def ignore_comment(self,token):
        lexer = CoolComment(self)
        _bool, pos, line = lexer.comment_analizer()
        self.lineno += line
        
        if _bool:
            self.index = len(self.text)
            self.cool_error(self.lineno, self.index)
            self.cool_error.add_lexical("EOF in comment")
        
        else: self.index += pos
      
    def STRING(self, token):
        lexer = CoolString(self)
        result, pos, line = lexer.string_analizer()
        self.lineno += line
        token.value = result

        if pos == 0:
            self.index = len(self.text)
            self.cool_error(self.lineno, self.index)
            self.cool_error.add_lexical("EOF in string constant")

        else : 
            self.index += pos
            
        return token

    def NUMBER(self, token):
        token.value = int(token.value)
        return token

    def error(self, token):
        self.cool_error(token.lineno, token.index)
        self.cool_error.add_lexical(f'Unknown character {token.value[0]}')
        self.index += 1

    

