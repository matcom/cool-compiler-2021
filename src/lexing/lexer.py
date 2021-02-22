import ply.lex as lex
from utils.utils import Token
# from utils.errors import LexicographicError

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
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0

    def tokenizer(self, code):
        self.lexer.input(code)
        tokens = []

        for token in self.lexer:
            self.list_tokens.append(token)
            tokens.append(Token(token.lineno, token.column, token.type, token.value))
        
        self.lexer.lineno = 1
        self.lexer.linestart = 0
        return tokens

    def find_column(self, lexer, token):
        line_start = lexer.lexdata.rfind('\n', 0, token.lexpos)
        return (token.lexpos - line_start)

    def update_column(self, token):
        token.column = token.lexpos - token.lexer.linestart + 1

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

    # region COMMENTS STATE rules

    def t_comment(self, token):
        r'--.*($|\n)'
        token.lexer.lineno += 1
        token.lexer.linestart = token.lexer.lexpos

    def t_COMMENTS(self, token):
        r'\(\*'
        token.lexer.level = 1
        token.lexer.begin('COMMENTS')
    
    def t_COMMENTS_open(self, token):
        r'\(\*'
        token.lexer.level += 1
        
    def t_COMMENTS_close(self, token):
        r'\*\)'
        token.lexer.level -= 1

        if token.lexer.level == 0:
            token.lexer.begin('INITIAL')

    def t_COMMENTS_newline(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)
        token.lexer.linestart = token.lexer.lexpos

    t_COMMENTS_ignore = '  \t\f\r\t\v'

    def t_COMMENTS_error(self, token):
        token.lexer.skip(1)

    def t_COMMENTS_eof(self, token):
        self.update_column(token)
        if token.lexer.level > 0:
            error_text = LexicographicError.EOF_COMMENT
            line = token.lineno
            column = token.column
            self.errors.append(LexicographicError(line, column, error_text))

    # endregion

    # region STRINGS STATE rules

    t_STRINGS_ignore = ''

    def t_STRINGS(self, token):
        r'\"'
        token.lexer.str_start = token.lexer.lexpos
        token.lexer.myString = ''
        token.lexer.backslash = False
        token.lexer.begin('STRINGS')

    def t_STRINGS_end(self, token):
        r'\"'
        self.update_column(token)

        if token.lexer.backslash:
            token.lexer.myString += '"'
            token.lexer.backslash = False
        else:
            token.value = token.lexer.myString
            token.type = 'STRING'
            token.lexer.begin('INITIAL')
            return token

    def t_STRINGS_newline(self, token):
        r'\n'
        token.lexer.lineno += 1
        self.update_column(token)
        token.lexer.linestart = token.lexer.lexpos

        if not token.lexer.backslash:
            error_text = LexicographicError.UNTERMINATED_STRING
            line = token.lineno
            column = token.column
            self.errors.append(LexicographicError(line, column, error_text))
            token.lexer.begin('INITIAL')

    def t_STRINGS_nill(self, token):
        r'\0'
        self.update_column(token)
        error_text = LexicographicError.NULL_STRING
        line = token.lineno
        column = token.column
        self.errors.append(LexicographicError(line, column, error_text))

    def t_STRINGS_consume(self, token):
        r'[^\n]'
        if token.lexer.backslash:
            if token.value == 'b':
                token.lexer.myString += '\b'
            elif token.value == 't':
                token.lexer.myString += '\t'
            elif token.value == 'f':
                token.lexer.myString += '\f'
            elif token.value == 'n':
                token.lexer.myString += '\n'
            elif token.value == '\\':
                token.lexer.myString += '\\'
            else:
                token.lexer.myString += token.value
            token.lexer.backslash = False
        else:
            if token.value != '\\':
                token.lexer.myString += token.value
            else:
                token.lexer.backslash = True

    def t_STRINGS_error(self, token):
        pass

    def t_STRINGS_eof(self, token):
        self.update_column(token)
        error_text = LexicographicError.EOF_STRING
        line = token.lineno
        column = token.column
        self.errors.append(LexicographicError(line, column, error_text))

    # endregion

    # region REGULAR EXPRESSIONS rules

    t_ignore = '  \t\f\r\t\v'
    
    def t_SEMICOLON(self, token):
        r';'
        self.update_column(token)
        return token

    def t_COLON(self, token):
        r':'
        self.update_column(token)
        return token

    def t_COMMA(self, token):
        r','
        self.update_column(token)
        return token

    def t_DOT(self, token):
        r'\.'
        self.update_column(token)
        return token
 
    def t_OPAR(self, token):
        r'\('
        self.update_column(token)
        return token
    
    def t_CPAR(self, token):
        r'\)'
        self.update_column(token)
        return token
    
    def t_OCUR(self, token):
        r'\{'
        self.update_column(token)
        return token
 
    def t_CCUR(self, token):
        r'\}'
        self.update_column(token)
        return token
 
    def t_LARROW(self, token):
        r'<-'
        self.update_column(token)
        return token
    
    def t_ARROBA(self, token):
        r'@'
        self.update_column(token)
        return token

    def t_RARROW(self, token):
        r'=>'
        self.update_column(token)
        return token

    def t_NOX(self, token):
        r'~'
        self.update_column(token)
        return token
 
    def t_EQUAL(self, token):
        r'='
        self.update_column(token)
        return token
 
    def t_PLUS(self, token):
        r'\+'
        self.update_column(token)
        return token
 
    def t_OF(self, token):
        r'of'
        self.update_column(token)
        return token
 
    def t_MINUS(self, token):
        r'-'
        self.update_column(token)
        return token
 
    def t_STAR(self, token):
        r'\*'
        self.update_column(token)
        return token
 
    def t_DIV(self, token):
        r'/'
        self.update_column(token)
        return token
   
    def t_LESSEQ(self, token):
        r'<='
        self.update_column(token)
        return token
 
    def t_LESS(self, token):
        r'<'
        self.update_column(token)
        return token

    def t_INHERITS(self, token):
        r'inherits'
        self.update_column(token)
        return token

    def t_TYPE(self, token):
        r'[A-Z][a-zA-Z_0-9]*'
        self.update_column(token)
        token.type = self.reserved.get(token.value.lower(), 'TYPE')
        return token

    def t_ID(self, token):
        r'[a-z][a-zA-Z_0-9]*'
        self.update_column(token)
        token.type = self.reserved.get(token.value.lower(), 'ID')
        return token

    def t_NUM(self, token):
        r'\d+(\.\d+)? '
        self.update_column(token)
        token.value = (token.value)
        return token

    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)
        token.lexer.linestart = token.lexer.lexpos 

    def t_error(self, token):
        self.update_column(token)
        error_text = LexicographicError.UNKNOWN_TOKEN % token.value[0]
        line = token.lineno
        column = token.column
        self.errors.append(LexicographicError(line, column, error_text))
        token.lexer.skip(1)

    # endregion
