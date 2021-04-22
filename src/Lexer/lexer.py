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
            ('comments' , 'exclusive'),
        )
    
    @property
    def recerved(self):
        return {
            'class' : 'CLASS',
            'inherits': 'INHERITS',
            'true': 'TRUE',
            'false': 'FALSE',
            'not': 'NOT',
        }
    
    @property
    def tokens(self):
        return (
            'AT',         # @
            'DOT',        # .
            'LESS',       # <
            'PLUS',       # +
            'STAR',       # *
            'EQUAL',      # =
            'COLON',      # :
            'COMMA',      # ,
            'MINUS',      # -
            'LDASH',      # <-
            'LEQUAL',     # <=
            'GEQUAL',     # =>
            'LCURLY',     # {
            'RCURLY',     # }
            'LPAREN',     # (
            'RPAREN',     # )
            'DIVIDE',     # /
            'GREATER',    # >
            'SEMICOLON',  # ;
            'ID',
            'INT',
            'TYPE',
            'STRING',
        )+ tuple(self.recerved.values())
   #endregion
   
   #region Regular expression rules for simple tokens
    t_AT = r'@'
    t_DOT = r'\.'
    t_LESS = r'<'
    t_PLUS = r'\+'
    t_STAR = r'\*'
    t_EQUAL = r'='
    t_COLON = r':'
    t_COMMA = r','
    t_MINUS = r'-'
    t_LDASH = r'<-'
    t_LEQUAL = r'<='
    t_GEQUAL = r'=>'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_DIVIDE = r'/'
    t_GREATER = r'>'
    t_SEMICOLON = r';'

    t_TYPE = r'[A-Z_][a-zA-Z0-9_]*'
   #endregion

   #region Regular expression rule for comments
    def t_COMMENTS(self, t):
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
        t.lexer.skip(1)

    def t_comments_error(self, t):
        t.lexer.skip(1)
    
    t_comments_ignore = ' \t'
   #endregion
   
   #region Regular expression rule with some action code
    
    def t_ID(self, t):
        r'[a-z_][a-zA-Z0-9_]*'
        t.type = self.recerved.get(t.value, 'ID')
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
   #endregion

   #region  General rules
    def t_newline(self, t):
        r'\n+'
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
        line_start = t.lexer.lexdata.rfind('\n', 0, t.lexer.lexpos) + 1
        return (t.lexer.lexpos - line_start) + 1 
