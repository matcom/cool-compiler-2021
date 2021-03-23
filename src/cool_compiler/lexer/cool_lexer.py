from typing import ClassVar
from sly import Lexer
from sly.lex import LexError
from .comment_lexer import CoolComment
from .string_lexer import CoolString

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
        ID, NUMBER,
        TWOPOINT, ARROW, OPENKEY, CLOSEKEY, ATSING, POINT, COLON, SEMICOL, LOGICAR,
        EQUAL, LESS_OR, LESS,
        COMPLEM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN,
        STRING
    }

    ignore = r' \t'
    ignore_comment = r'\(\*'
    ignore_newline = r'\n'
    ignore_line = r'--.*\n'

    CLASS   = r'class'
    INHERITS= r'inherits'

    IF      = r'if'
    THEN    = r'then'
    ELSE    = r'else'
    FI      = r'fi'

    LET     = r'let'
    IN      = r'in'


    WHILE   = r'while'
    LOOP    = r'loop'
    POOL    = r'pool'

    CASE    = r'case'
    OF      = r'of'
    ESAC    = r'esac'

    ISVOID  = r'isvoid'
    NEW     = r'new'
    NOT     = r'not'

    TRUE    = r'true'
    FALSE   = r'false'

    ID      = r'[a-zA-Z][a-zA-Z0-9_]*'
    NUMBER  = r'\d+'

    TWOPOINT= r':'
    ARROW   = r'<-'
    OPENKEY = r'{'
    CLOSEKEY= r'}'
    ATSING  = r'@'
    POINT   = r'\.'
    COLON   = r','
    SEMICOL = r';'
    LOGICAR = r'=>'

    EQUAL   = r'='
    LESS_OR = r'<='
    LESS    = r'<'
    
    COMPLEM = r'~'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    
    STRING  = r'\"'

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

    

