import ply.lex as lex

from Tools.messages import *
from Tools.tokens import Token
from Tools.errors import LexicographicError, SyntaticError

class Lexer:
    def __init__(self, **kwargs):
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0

    def update_column(self, t):
        t.column = t.lexpos - t.lexer.linestart + 1
        
    @property    
    def states(self): 
        return (('comments', 'exclusive'),('strings', 'exclusive'))

    @property
    def reserved(self):
        return {
            'class': 'class', 'else': 'else', 'false': 'false', 'fi': 'fi',
            'if': 'if', 'in': 'in', 'inherits': 'inherits', 'isvoid': 'isvoid', 
            'let': 'let', 'loop': 'loop', 'pool': 'pool', 'then': 'then', 
            'while': 'while', 'case': 'case', 'esac': 'esac', 'new': 'new', 
            'of': 'of', 'not': 'not', 'true': 'true'
        }

    @property
    def tokens(self):
        return (
            'semi', 'colon', 'comma', 'dot', 'opar', 'cpar', 'ocur', 'ccur', 'larrow', 'arroba',
            'rarrow', 'nox', 'equal', 'plus', 'minus', 'star', 'div', 'less', 'lesseq', 'id',
            'type', 'num', 'string') + tuple(self.reserved.values())
    
    #########################################################################
    ##                         Rules for comment                           ##
    #########################################################################

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
        self.update_column(t)
        if t.lexer.level > 0:
            self.errors.append(LexicographicError('EOF in comment' , t.lineno, t.column))
    
    #########################################################################
    ##                        Rules for string                             ##
    #########################################################################
    
    t_strings_ignore = ''

    def t_strings(self, t):
        r'\"'
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.myString = ''
        t.lexer.backslash = False
        t.lexer.begin('strings')

    def t_strings_end(self, t):
        r'\"'
        self.update_column(t)

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
        self.update_column(t)
        
        t.lexer.linestart = t.lexer.lexpos 

        if not t.lexer.backslash:
            self.errors.append(LexicographicError('Undeterminated string constant', t.lineno, t.column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self, t):
        r'\0'
        self.update_column(t)
  
        self.errors.append(LexicographicError('String contains null character', t.lineno, t.column))

    def t_strings_consume(self, t):
        r'[^\n]'
        if t.lexer.backslash :
            if t.value == 'b':
                t.lexer.myString += '\b' 
            elif t.value == 't':
                t.lexer.myString += '\t'      
            elif t.value == 'f':
                t.lexer.myString += '\f'   
            elif t.value == 'n':
                t.lexer.myString += '\n'     
            elif t.value == '\\':
                t.lexer.myString += '\\'
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
        self.update_column(t)
     
        self.errors.append(LexicographicError('EOF in string constant', t.lineno, t.column))
    
    #########################################################################
    ##                      Rules for simple tokens                        ##
    #########################################################################

    def t_semi(self, t):
        r';'
        self.update_column(t)
        return t

    def t_colon(self, t):
        r':'
        self.update_column(t)
        return t

    def t_comma(self, t):
        r','
        self.update_column(t)
        return t

    def t_dot(self, t):
        r'\.'
        self.update_column(t)
        return t
 
    def t_opar(self, t):
        r'\('
        self.update_column(t)
        return t
    
    def t_cpar(self, t):
        r'\)'
        self.update_column(t)
        return t
    
    def t_ocur(self, t):
        r'\{'
        self.update_column(t)
        return t
 
    def t_ccur(self, t):
        r'\}'
        self.update_column(t)
        return t
 
    def t_larrow(self, t):
        r'<-'
        self.update_column(t)
        return t
    
    def t_arroba(self, t):
        r'@'
        self.update_column(t)
        return t

    def t_rarrow(self, t):
        r'=>'
        self.update_column(t)
        return t

    def t_nox(self, t):
        r'~'
        self.update_column(t)
        return t
 
    def t_equal(self, t):
        r'='
        self.update_column(t)
        return t
 
    def t_plus(self, t):
        r'\+'
        self.update_column(t)
        return t
 
    def t_of(self, t):
        r'of'
        self.update_column(t)
        return t
 
    def t_minus(self, t):
        r'-'
        self.update_column(t)
        return t
 
    def t_star(self, t):
        r'\*'
        self.update_column(t)
        return t
 
    def t_div(self, t):
        r'/'
        self.update_column(t)
        return t
   
    def t_lesseq(self, t):
        r'<='
        self.update_column(t)
        return t
 
    def t_less(self, t):
        r'<'
        self.update_column(t)
        return t
 
    def t_inherits(self, t):
        r'inherits'
        self.update_column(t)
        return t

    def t_type(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'type')
        self.update_column(t)
        return t

    #########################################################################
    ##                      Rules for action code                          ##
    #########################################################################
    
    def t_id(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'id')
        self.update_column(t)
        return t

    def t_num(self, t):
        r'\d+(\.\d+)? '
        t.value = float(t.value)
        self.update_column(t)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos 

    def t_error(self, t):
        self.update_column(t)
        self.errors.append(LexicographicError(f'ERROR "{t.value[0]}"', t.lineno, t.column))
        t.lexer.skip(1)

    @property
    def t_ignore(self): 
        return '  \t\f\r\t\v'
    
    #########################################################################
    ##                            Tokenizer                                ##
    #########################################################################

    def tokenize(self, text: str):
        self.lexer.input(text)
        tokens = [Token(token.type, token.value, token.lineno, token.column) for token in self.lexer]
        self.lexer.lineno = 1
        self.lexer.linestart = 0
        if len(tokens) == 0:
            self.errors.append(SyntaticError('ERROR at or near "EOF"' , 0, 0))
        return tokens