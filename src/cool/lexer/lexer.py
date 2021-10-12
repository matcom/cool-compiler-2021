from pathlib import Path
from pprint import pprint
from typing import List

import ply.lex as lex

from ..utils import Token, errors, ignored, literals, reservedKeywords, tokens


class CoolLexer:
    def __init__(self, **kwargs):
        self.reserved = reservedKeywords
        self.tokens = tokens
        self.errors = []
        self.lexer = lex.lex(self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0
 
    def updateColumn(self, t):
        t.column = t.lexpos - t.lexer.linestart + 1
        
    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive')
    )

    # Comments
    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos 

    def t_comments(self,t):
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

    t_comments_ignore = '  \t\f\r\t\v'

    def t_comments_error(self, t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        self.updateColumn(t)
        if t.lexer.level > 0:
            error_text = errors.LexicographicError.EOF_COMMENT 
            self.errors.append(errors.LexicographicError(error_text, t.lineno, t.column))
    
    # Strings
    t_strings_ignore = ''

    def t_strings(self, t):
        r'\"'
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.myString = ''
        t.lexer.backslash = False
        t.lexer.begin('strings')

    def t_strings_end(self, t):
        r'\"'
        self.updateColumn(t)

        if t.lexer.backslash : 
            t.lexer.myString += '"'
            t.lexer.backslash = False
        else:
            t.value = t.lexer.myString 
            t.type = 'string'
            t.lexer.begin('INITIAL')           
            return t

    def t_strings_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.updateColumn(t)
        
        t.lexer.linestart = t.lexer.lexpos 

        if not t.lexer.backslash:
            error_text = errors.LexicographicError.UNDETERMINED_STRING
            self.errors.append(errors.LexicographicError(error_text, t.lineno, t.column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self, t):
        r'\0'
        error_text = errors.LexicographicError.NULL_STRING
        self.updateColumn(t)
  
        self.errors.append(errors.LexicographicError(error_text, t.lineno, t.column))

    def t_strings_consume(self, t):
        r'[^\n]'

        if t.lexer.backslash :
            if t.value in ['b', 't', 'f', 'n', '\\']:
                t.lexer.myString += f'\{t.value}'
            else: 
                t.lexer.myString += t.value 

            t.lexer.backslash = False
        else:
            if t.value != '\\':
                t.lexer.myString += t.value
            else:
                t.lexer.backslash = True 

    def t_strings_error(self, t):
        pass

    def t_strings_eof(self, t):
        self.updateColumn(t)
     
        error_text = errors.LexicographicError.EOF_STRING
        self.errors.append(errors.LexicographicError(error_text, t.lineno, t.column))
    
    t_ignore = '  \t\f\r\t\v'
    
    def t_semi(self, t):
        r';'
        self.updateColumn(t)
        return t

    def t_colon(self, t):
        r':'
        self.updateColumn(t)
        return t

    def t_comma(self, t):
        r','
        self.updateColumn(t)
        return t

    def t_dot(self, t):
        r'\.'
        self.updateColumn(t)
        return t
 
    def t_opar(self, t):
        r'\('
        self.updateColumn(t)
        return t
    
    def t_cpar(self, t):
        r'\)'
        self.updateColumn(t)
        return t
    
    def t_ocur(self, t):
        r'\{'
        self.updateColumn(t)
        return t
 
    def t_ccur(self, t):
        r'\}'
        self.updateColumn(t)
        return t
 
    def t_larrow(self, t):
        r'<-'
        self.updateColumn(t)
        return t
    
    def t_arroba(self, t):
        r'@'
        self.updateColumn(t)
        return t

    def t_rarrow(self, t):
        r'=>'
        self.updateColumn(t)
        return t

    def t_nox(self, t):
        r'~'
        self.updateColumn(t)
        return t
 
    def t_equal(self, t):
        r'='
        self.updateColumn(t)
        return t
 
    def t_plus(self, t):
        r'\+'
        self.updateColumn(t)
        return t
 
    def t_of(self, t):
        r'of'
        self.updateColumn(t)
        return t
 
    def t_minus(self, t):
        r'-'
        self.updateColumn(t)
        return t
 
    def t_star(self, t):
        r'\*'
        self.updateColumn(t)
        return t
 
    def t_div(self, t):
        r'/'
        self.updateColumn(t)
        return t
   
    def t_lesseq(self, t):
        r'<='
        self.updateColumn(t)
        return t
 
    def t_less(self, t):
        r'<'
        self.updateColumn(t)
        return t
 
    def t_inherits(self, t):
        r'inherits'
        self.updateColumn(t)
        return t

    def t_type(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'type')
        self.updateColumn(t)
        return t

    # Check for reserved words:
    def t_id(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'id')
        self.updateColumn(t)
        return t

    # Get Numbers
    def t_num(self, t):
        r'\d+(\.\d+)? '
        t.value = float(t.value)
        self.updateColumn(t)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos 

    # Error handling rule
    def t_error(self, t):
        self.updateColumn(t)
        error_text = errors.LexicographicError.UNKNOWN_TOKEN % t.value[0]
        
        self.errors.append(errors.LexicographicError(error_text, t.lineno, t.column))
        #print(f'Report Error {len(self.errors)} {self.errors[0]}')
        t.lexer.skip(1)
        #t.lexer.skip(len(t.value))
    
    def tokenize(self, text: str) -> List[Token]:
        self.lexer.input(text)
        tokens: List[Token] = []

        for t in self.lexer:
            tokens.append(Token(t.type, t.value, t.lineno, t.column))
        
        return tokens

def main(text: str, output = None):
    lexer = CoolLexer()

    # print(f'Path: {input}')

    a = lexer.tokenize(text)
    
    for i in a:
        print(i)

    if lexer.errors:
        for e in lexer.errors:
            print(e)
        raise Exception()

    return lexer
    

if __name__ == '__main__':
    main()
