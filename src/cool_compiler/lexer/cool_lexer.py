from typing import ClassVar
from sly import Lexer
from sly.lex import LexError
from .comment_lexer import CoolComment

class CoolLexer(Lexer):
    tokens = {
        CLASS,IF,
        ID,NUMBER,
        PLUS,MINUS,TIMES,DIVIDE,
        ASSIGN,LPAREN,RPAREN,
    }

    ignore = r' \t'
    ignore_comment = r'\(\*'
    ignore_newline = r'\n+'

    CLASS   = r'class'
    IF      = f'if'
    ID      = r'[a-zA-Z][a-zA-Z0-9]*'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LPAREN  = r'\('
    RPAREN  = r'\)'

    def ignore_newline(self,token):
        self.lineno += 1

    def ignore_comment(self,token):
        lexer = CoolComment()
        text = self.text[self.index-2:]
        pos, line = lexer.comment_analizer(text)
        self.index += pos
        self.lineno += line
        #text = token.value[2:]
        #print(text)
        #copen = '(*'
        #cclse = '*)'
        #s = 1
        # mas (* que *)
        #for i in range(len(text)):
        #    if s == 0:
        #        text = text[i+1:]
        #        break
        #    if copen == text[ i:i+2 ]: s = s + 1
        #    if cclse == text[ i:i+2 ]: s = s - 1
        
        # mas *) que (*
        #pos = 0
        #for i  in range(len(text)):
        #    if copen == text[ i:i+2 ]: break
        #    if cclse == text[ i:i+2 ]: 
        #        s = s - 1
        #        pos = i+2

        #self.index -= len(text[pos:]
            

    def NUMBER(self, token):
        token.value = int(token.value)
        return token


    

if __name__ == '__main__':
    data = '''
                (* (* (* *) *) *) a *) e*) eeeee (* a*)
           '''
    lexer = CoolLexer()
    for tok in lexer.tokenize(data):
        print(tok)