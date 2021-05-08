import ply.lex as lex

from cmp.token import Token
from cmp.errors import LexicographicError

class Lexer(object):
    def __init__(self, errors=[]):
         object.__init__(self)
         self.errors = errors
         self.build()

    #region Property
    @property
    def states(self):
        return (
            ('string', 'exclusive'),
            ('comments', 'exclusive')
        )

    @property
    def recerved(self):
        return {
            'fi'      : 'FI',
            'if'      : 'IF',
            'in'      : 'IN',
            'of'      : 'OF',
            'let'     : 'LET',
            'new'     : 'NEW',
            'not'     : 'NOT',
            'case'    : 'CASE',
            'else'    : 'ELSE',
            'loop'    : 'LOOP',
            'pool'    : 'POOL',
            'then'    : 'THEN',
            'esac'    : 'ESAC',
            'class'   : 'CLASS',
            'while'   : 'WHILE',
            'isvoid'  : 'ISVOID',
            'inherits': 'INHERITS',
        }

    @property
    def tokens(self):
        return (
            'ID'       ,
            'INT'      ,
            'TYPE'     ,
            'BOOL'     ,
            'STRING'   ,

            'AT'       ,# @
            'DOT'      ,# .
            'LESS'     ,# <
            'PLUS'     ,# +
            'STAR'     ,# *
            'EQUAL'    ,# =
            'COLON'    ,# :
            'COMMA'    ,# ,
            'MINUS'    ,# -
            'TILDE'    ,# ~
            'LDASH'    ,# <-
            'LEQUAL'   ,# <=
            'GEQUAL'   ,# =>
            'LCURLY'   ,# {
            'RCURLY'   ,# }
            'LPAREN'   ,#(
            'RPAREN'   ,# )
            'DIVIDE'   ,# /
            'SEMICOLON',# ;
        ) + tuple(self.recerved.values())
    #endregion
    
    #region regular expression rules for comments
    def t_comment(self, t):
        r'--.*'
        pass

    def t_comments(self, t):
        r'\(\*'
        t.lexer.level = 1
        t.lexer.begin('comments')

    def t_comments_open(self, t):
        r'\(\*'
        self.lexer.level += 1

    def t_comments_close(self, t):
        r'\*\)'
        self.lexer.level -= 1

        if not self.lexer.level:
            t.lexer.begin('INITIAL')
    
    def t_comments_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comments_eof(self, t):
        self.errors.append(LexicographicError.text(t.lexer.lineno, Token.find_column(t), 'EOF in comment'))
    
    def t_comments_error(self, t):
        t.lexer.skip(1)
    
    @property
    def t_comments_ignore(self):
        return ' \t'
    #endregion
    
    #region regular expression rules for string
    def t_string(self, t):
        r'"'
        t.lexer.string = ''
        t.lexer.begin_string = t.lexer.lexpos
        t.lexer.begin('string')

    def t_string_end(self, t):
        r'"'   
        t.type = "STRING"
        t.value = t.lexer.string
        t.lexpos = t.lexer.begin_string - 1
        t.value = Token(t)
        t.lexer.begin('INITIAL')
        return t
    
    #region Special character
    def t_string_backspace(self, t):
        r'\\b'
        t.lexer.string += '\b'
    
    def t_string_tab(self, t):
        r'\\t'
        t.lexer.string += '\t'

    def t_string_formfeed(self, t):
        r'\\f'
        t.lexer.string += '\f'
    
    def t_string_quotes(self, t):
        r'\\"'
        t.lexer.string += '\\"'
    
    def t_string_null(self, t):
        r'\0'
        self.errors.append(LexicographicError.text(t.lexer.lineno, Token.find_column(t), 'String contains null character'))
    
    def t_string_backslashend(self, t):
        r'\\\n'
        t.lexer.lineno += 1
    
    def t_string_backslash(self, t):
        r'(\\\\)|(\\)'
        t.lexer.string += '\\'
    #endregion

    def t_string_contline(self, t):
        r'\\n'
        t.lexer.string += '\n'

    def t_string_newline(self, t):
        r'\n'
        self.errors.append(LexicographicError.text(t.lexer.lineno, Token.find_column(t), 'Unterminated string constant'))
        t.lexer.lineno += 1
        t.lexer.begin('INITIAL')
    
    def t_string_eof(self, t):
        t.lexer.begin('INITIAL')
        self.errors.append(LexicographicError.text(t.lexer.lineno, Token.find_column(t), 'EOF in string constant'))

    def t_string_error(self, t):
        t.lexer.skip(1)
        t.lexer.string += t.value[0]

    @property
    def t_string_ignore(self):
        return ''
    #endregion

    #region regular expression rules for simple tokens
    def t_AT(self, t):
        r'@'
        t.value = Token(t)
        return t
    
    def t_DOT(self, t):
        r'\.'
        t.value = Token(t)
        return t
    
    def t_LDASH(self, t):
        r'<-'
        t.value = Token(t)
        return t
    
    def t_LEQUAL(self, t):
        r'<='
        t.value = Token(t)
        return t

    def t_LESS(self, t):
        r'<'
        t.value = Token(t)
        return t
    
    def t_PLUS(self, t):
        r'\+'
        t.value = Token(t)
        return t
    
    def t_STAR(self, t):
        r'\*'
        t.value = Token(t)
        return t
    
    def t_GEQUAL(self, t):
        r'=>'
        t.value = Token(t)
        return t
    
    def t_EQUAL(self, t):
        r'='
        t.value = Token(t)
        return t
    
    def t_COLON(self, t):
        r':'
        t.value = Token(t)
        return t
    
    def t_COMMA(self, t):
        r','
        t.value = Token(t)
        return t
    
    def t_MINUS(self, t):
        r'-'
        t.value = Token(t)
        return t
    
    def t_TILDE(self, t):
        r'~'
        t.value = Token(t)
        return t
    
    def t_LCURLY(self, t):
        r'\{'
        t.value = Token(t)
        return t
    
    def t_RCURLY(self, t):
        r'\}'
        t.value = Token(t)
        return t
    
    def t_LPAREN(self, t):
        r'\('
        t.value = Token(t)
        return t
    
    def t_RPAREN(self, t):
        r'\)'
        t.value = Token(t)
        return t
    
    def t_DIVIDE(self, t):
        r'/'
        t.value = Token(t)
        return t
    
    def t_SEMICOLON(self, t):
        r';'
        t.value = Token(t)
        return t
    #endregion
    
    #region regular expression rules with action code
    def t_ID(self, t):
        r'[a-z][a-zA-Z0-9_]*'
        
        #It's a boolean or keywords
        if t.value.lower() in ('true', 'false'):
            t.type = 'BOOL'
        else:
            t.type = self.recerved.get(t.value.lower(), 'ID')
        
        t.value = Token(t)
        return t

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z0-9_]*'

        #It's a keywords
        t.type = self.recerved.get(t.value.lower(), 'TYPE')
        t.value = Token(t)
        
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        t.value = Token(t)
        return t  
    #endregion

    #region general rules
    def t_newline(self, t):
        r'(\n|\r)+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        self.errors.append(LexicographicError.text(t.lexer.lineno, Token.find_column(t), 'ERROR "%s"'%t.value[0]))
        t.lexer.skip(1)
    
    def t_eof(self, t):
        self.lexer.begin('INITIAL')

    @property
    def t_ignore(self):
        return ' \t'
    #endregion

    #region Build and Tokenizer
    def input(self, data):
        pass

    def token(self):
        return self.lexer.token()

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenizer(self, data):
        self.lexer.input(data)
        return [token for token in self.lexer]
    #endregion