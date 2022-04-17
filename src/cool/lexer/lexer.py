import ply.lex as lex
from cool.utils.Errors import LexerErrors
from cool.utils.LexerTokens import Tokens

class Lexer:
    def __init__(self,text,**kwargs) -> None:
        self.tokens = Tokens.tokens
        self.reserved = Tokens.reserved
        self.lexer = lex.lex(module=self, **kwargs)
        self.errors = []
        self.text = text

    def get_column(self, token):
        start_line = self.text.rfind('\n', 0, token.lexpos) + 1
        c = (token.lexpos - start_line) + 1 
        token.column = c

     # Declare the state
    states = (
    ('comments','exclusive'),
    ('STRING','exclusive')
    )

    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos 
    
    # Match the first (*. Enter comments state.
    def t_comments(self,t):
        r'\(\*'
        t.lexer.level = 1                          
        t.lexer.begin('comments')

    def t_comments_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)              
    
    # Rules for the comments state
    def t_comments_open(self,t):     
        r'\(\*'
        t.lexer.level +=1                
    
    def t_comments_close(self,t):
        r'\*\)'
        t.lexer.level -=1

        if t.lexer.level == 0:
            t.lexer.begin('INITIAL')

    def t_comments_error(self,t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        self.get_column(t)
        if t.lexer.level > 0:
            text = LexerErrors.LexerErrors.EOF_COMMENT
            self.errors.append(LexerErrors.LexerErrors(t.column,t.lineno,text))

    t_comments_ignore = '  \t\f\r\t\v'

    def t_STRING(self,t):
        r'\"'
        t.lexer.found_backslash = False          
        t.lexer.result = ''       
        self.get_column(t)      
        t.lexer.begin('STRING')   

    def t_STRING_close(self,t):
        r'\"'
        self.get_column(t)      
        
        if t.lexer.found_backslash:
            t.lexer.found_backslash = False
            t.lexer.result += t.value
        else:
            t.type = 'STRING'
            t.value = t.lexer.result 
            t.lexer.begin('INITIAL')     
            return t                 
    
    def t_STRING_error(self,t):
        pass

    t_STRING_ignore = ''

    def t_STRING_eof(self,t):
        r'\$'
        self.get_column(t)
        text = LexerErrors.LexerErrors.EOF_STRING
        self.errors.append(LexerErrors.LexerErrors(t.column,t.lineno,text))

    def t_STRING_null(self,t):
        r'\0'
        self.get_column(t)
        text = LexerErrors.LexerErrors.NULL_STRING
        self.errors.append(LexerErrors.LexerErrors(t.column,t.lineno,text))

    def t_STRING_newline(self, t):
        r'\n+'
        self.get_column(t)
        t.lexer.lineno += len(t.value)

        if not t.lexer.found_backslash:
            text = LexerErrors.LexerErrors.UNTERMINATED_STRING
            self.errors.append(LexerErrors.LexerErrors(t.column,t.lineno,text))
            t.lexer.begin('INITIAL')
    
    def t_STRING_take(self,t):
        r'[^\n]'

        if t.lexer.found_backslash:
            if t.value in ['b','t','n','f']:
                t.lexer.result += f'\{t.value}'
            else:
                t.lexer.result += t.value
            t.lexer.found_backslash = False

        else:
            if t.value == '\\':
                t.lexer.found_backslash = True
            else:
                t.lexer.result += t.value


    def t_SEMI(self,t):
        r';'
        self.get_column(t)
        return t

    def t_COLON(self,t):
        r':'
        self.get_column(t)
        return t

    def t_COMMA(self,t):
        r','
        self.get_column(t)
        return t

    def t_DOT(self,t):
        r'\.'
        self.get_column(t)
        return t

    def t_OPAR(self,t):
        r'\('
        self.get_column(t)
        return t

    def t_CPAR(self,t):
        r'\)'
        self.get_column(t)
        return t

    def t_OCUR(self,t):
        r'\{'
        self.get_column(t)
        return t

    def t_CCUR(self,t):
        r'\}'
        self.get_column(t)
        return t

    def t_LARROW(self,t):
        r'<-'
        self.get_column(t)
        return t

    def t_ARROBA(self,t):
        r'@'
        self.get_column(t)
        return t

    def t_RARROW(self,t):
        r'=>'
        self.get_column(t)
        return t

    def t_NOX(self,t):
        r'~'
        self.get_column(t)
        return t

    def t_EQUAL(self,t):
        r'='
        self.get_column(t)
        return t

    def t_PLUS(self,t):
        r'\+'
        self.get_column(t)
        return t

    def t_MINUS(self,t):
        r'-'
        self.get_column(t)
        return t
    
    def t_STAR(self,t):
        r'\*'
        self.get_column(t)
        return t
    
    def t_DIV(self,t):
        r'/'
        self.get_column(t)
        return t

    def t_LESSEQ(self,t):
        r'<='
        self.get_column(t)
        return t
        
    def t_LESS(self,t):
        r'<'
        self.get_column(t)
        return t

    def t_inherits(self, t):
        r'inherits'
        self.get_column(t)
        return t

    def t_TYPE(self,t):
        r'[A-Z][a-zA-Z_0-9]*'
        v = str.lower(t.value)
        if v in self.reserved:
            t.type = self.reserved[v]
            t.value = v
        else:
            t.type = 'TYPE'
        self.get_column(t)
        return t


    def t_ID(self,t):
        r'[a-z][a-zA-Z_0-9]*'

        v = str.lower(t.value)
        if v in self.reserved:    
            t.type = self.reserved[v]
            t.value = v
        else:
            t.type = 'ID'

        self.get_column(t)
        return t


    def t_NUMBER(self,t):
        r'\d+(\.\d+)?'
        self.get_column(t)
        t.value = float(t.value)    
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    t_ignore= '  \t\f\r\t\v'

    # Error handling rule
    def t_error(self,t):
        text = f'ERROR "{t.value[0]}"'
        self.get_column(t)
        self.errors.append(LexerErrors.LexerErrors(t.column,t.lineno,text))
        t.lexer.skip(1)

    def tokenize(self):
        self.lexer.input(self.text)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(Tokens.Token(tok.lineno,tok.column,tok.type,tok.value))
            
        return tokens

def main(input:str):
    mylexer = Lexer(input)
    return mylexer
