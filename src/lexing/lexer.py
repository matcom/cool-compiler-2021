import ply.lex as lex

class Lexer:

    def __init__(self, **kwargs):
        self.tokens = []
        self.reserved = {}
        self.errors = []
        self.list_tokens = []
        self.lexer = None
        self.build()

    def build(self, **kwargs):
        self.reserved = self._reserved
        self.tokens = self._tokens + list(self._reserved.values())
        print(self.reserved)
        print(self.tokens)
        # self.lexer = lex.lex(module=self, **kwargs)
        # self.lexer.lineno = 1
        # self.lexer.linestart = 0

    @property
    def states(self):
        return (
            ('COMMENTS', 'exclusive'),
            ('STRINGS', 'exclusive')
        )

    @property
    def _reserved(self):
        return {
            'case':             'CASE',
            'class':            'CLASS',
            'else':             'ELSE',
            'esac':             'ESAC',
            'false':            'FALSE',
            'fi':               'FI',
            'if':               'IF',
            'in':               'IN',
            'inherits':         'INHERITS',
            'isvoid':           'ISVOID',
            'let':              'LET',
            'loop':             'LOOP',
            'new':              'NEW',
            'not':              'NOT',
            'of':               'OF',
            'pool':             'POOL',
            'then':             'THEN',
            'true':             'TRUE',
            'while':            'WHILE',
        }

    @property
    def _tokens(self):
        return [
            'SEMICOLON',            #  ;
            'COLON',                #  :
            'COMMA',                #  ,
            'DOT',                  #  .
            'OPAR',                 #  (
            'CPAR',                 #  )
            'OCUR',                 #  {
            'CCUR',                 #  }
            'LARROW',               #  <-
            'ARROBA',               #  @
            'RARROW',               #  =>
            'NOX',                  #  ~
            'EQUAL',                #  =
            'PLUS',                 #  +
            'MINUS',                #  -
            'STAR',                 #  *
            'DIV',                  #  /
            'LESS',                 #  <
            'LESSEQ',               #  <=
            'ID',
            'TYPE',
            'NUM',
            'STRING'
        ]
        