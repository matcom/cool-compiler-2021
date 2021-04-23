import ply.lex as lex

class Lexer(object):
    
    def __init__(self, errors):
        object.__init__(self)
        self.errors = errors
        self.build()
   
   #region Property
    @property
    def states(self):
        return (
            ('string', 'exclusive'),
            ('comments' , 'exclusive'),
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
            'GREATER'  ,# >
            'SEMICOLON',# ;
        ) + tuple(self.recerved.values())
   #endregion
   
   #region Regular expression rules for simple tokens
    t_AT        = r'@'
    t_DOT       = r'\.'
    t_LESS      = r'<'
    t_PLUS      = r'\+'
    t_STAR      = r'\*'
    t_EQUAL     = r'='
    t_COLON     = r':'
    t_COMMA     = r','
    t_MINUS     = r'-'
    t_TILDE     = r'~'
    t_LDASH     = r'<-'
    t_LEQUAL    = r'<='
    t_GEQUAL    = r'=>'
    t_LCURLY    = r'\{'
    t_RCURLY    = r'\}'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_DIVIDE    = r'/'
    t_GREATER   = r'>'
    t_SEMICOLON = r';'
   #endregion

   #region Regular expression rule for comments
    def t_comment(self, t):
        r'--.*'

    def t_comments(self, t):
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
    
    def t_comments_nexline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comments_eof(self, t):
        self.errors.append('(%s, %s) - LexicographicError: EOF in comment'%(t.lexer.lineno, Lexer.find_column(t)))

    def t_comments_error(self, t):
        t.lexer.skip(1)
    
    t_comments_ignore = ' \t'
   #endregion
   
   #region Regular expression rule for string
    def t_string(self, t):
        r'"'
        t.lexer.string = ''
        t.lexer.begin('string')

    def t_string_end(self, t):
        r'"'
        t.type = "STRING"
        t.value = t.lexer.string
        t.lexer.begin('INITIAL')
        return t
    
    def t_string_newline(self, t):
        r'\n'
        self.errors.append('(%s, %s) - LexicographicError: Unterminated string constant'%(t.lexer.lineno, Lexer.find_column(t)))
        t.lexer.begin('INITIAL')
        t.lexer.lineno += 1

    def t_string_eof(self, t):
        t.lexer.begin('INITIAL')
        self.errors.append('(%s, %s) - LexicographicError: EOF in string constant'%(t.lexer.lineno, Lexer.find_column(t)))

    def t_string_error(self, t):
        t.lexer.skip(1)
        t.lexer.string += t.value[0]
    
    #Special character
    def t_string_backspace(self, t):
        r'\\b'
        t.lexer.string += '\b'
    def t_string_tab(self, t):
        r'\\t'
        t.lexer.string += '\t'
    def t_string__newline(self, t):
        r'\\n'
        t.lexer.string += '\n'
    def t_string_formfeed(self, t):
        r'\\f'
        t.lexer.string += '\f'
    def t_string_quotes(self, t):
        r'\\"'
        t.lexer.string += '\\"'
    def t_string_null(self, t):
        r'\0'
        self.errors.append('(%s, %s) - LexicographicError: String contains null character'%(t.lexer.lineno, Lexer.find_column(t)-1))
    def t_string_backslashend(self, t):
        r'\\\n'
        t.lexer.lineno += 1
    def t_string_backslash(self, t):
        r'(\\\\)|(\\)'
        t.lexer.string += '\\'
         
    t_string_ignore = ''
   #endregion
   
   #region Regular expression rule with some action code  
    def t_ID(self, t):
        r'[a-z][a-zA-Z0-9_]*'
        if t.value.lower() in ('true', 'false'):
            t.type = 'BOOL'
        else:
            t.type = self.recerved.get(t.value, 'ID')
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t  

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z0-9_]*' 
        return t
   #endregion

   #region  General rules
    def t_newline(self, t):
        r'(\n|\f|\r|\v|\t)+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        self.errors.append('(%s, %s) - LexicographicError: ERROR "%s"'%(t.lexer.lineno, Lexer.find_column(t), t.value[0]))
        t.lexer.skip(1)
    
    t_ignore = ' \t'
   #endregion
    
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    def Tokenizer(self, data):
        self.lexer.input(data)
        return [token for token in self.lexer]
    
    @staticmethod
    def find_column(t):
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexer.lexpos - int(t.value=='\n')) + 1
        return (t.lexer.lexpos - line_start) + 1 - int(t.value=='\n') 