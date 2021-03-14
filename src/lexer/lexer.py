import ply.lex as lex
from utils.errors import LexicographicError
reserved = {
    'class' : 'class',
    'new' : 'new',
    'while' : 'while',
    'if' : 'if',
    'then' : 'then',
    'else' : 'else',
    'fi' : 'fi',
    'not' : 'not',
    'loop' : 'loop',
    'pool' : 'pool',
    'let' : 'let',
    'in' : 'in',
    'case' : 'case',
    'of' : 'of',
    'esac' : 'esac',
    'inherits' : 'inherits',
    'isvoid' : 'isvoid',
    'true' : 'true',
    'false' : 'false'
}
_tokens = [
    'space',
    'lineComment',
    'chunkComment',
    'number',
    'semi',
    'colon',
    'comma',
    'dot',
    'opar',
    'cpar',
    'ocur',
    'ccur',
    'plus',
    'minus',
    'star',
    'div',
    'equal',
    'lneq',
    'leq',
    'complement',
    'assignArrow',
    'rArrow',
    'string',
    'arroba',
    'tab',
    'newline',
    'type',
    'id'
    #ress
]
_tokens += list(reserved.values())

class CoolLexer:
    tokens = _tokens
    states = (
        ('chunkComment', 'exclusive'),
        ('string', 'inclusive')
    )

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Compute column.
    #   input is the input text string
    #   token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1  #parentesis?

    t_ignore_space = r'[ ]+'

    t_ignore_lineComment = r'--.*'

    # t_ignore_chunkComment = r'\(\*[^$]*\*\)'

    def t_chunkComment(self, t):
        r'\(\*'
        t.lexer.code_start = t.lexer.lexpos - 2
        t.lexer.level = 1
        t.lexer.begin('chunkComment')
        pass

    def t_chunkComment_initComment(self, t):
        r'\(\*'
        t.lexer.level += 1
        pass

    def t_chunkComment_endComment(self, t):
        r'\*\)'
        t.lexer.level += -1
        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.code_start : t.lexer.lexpos]
            t.type = 'chunkComment'
            # t.lexer.lineno += t.value.count('\n')
            t.lexer.begin('INITIAL')
        if t.lexer.level < 0:
            print(f'( {t.lexer.lineno}')
        pass

    def t_chunkComment_comment(self, t):
        r'.|\n'
        if t.value == '\n':
            t.lexer.lineno+=len(t.value)
        pass

    def t_chunkComment_eof(self, t):
        if t.lexer.level > 0:
            print(LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), 'EOF in comment'))
        return None

    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_semi = r';'

    t_colon = r':'

    t_comma = r','

    t_dot = r'\.'

    t_opar = r'\('
    t_cpar = r'\)'

    t_ocur = r'\{'
    t_ccur = r'\}'

    t_plus = r'\+'
    t_minus = r'\-'
    t_star = r'\*'
    t_div = r'/'

    t_equal = r'='
    t_lneq = r'<'
    t_leq = r'<='

    t_complement = r'\~'

    t_assignArrow = r'<\-'

    t_rArrow = r'=>'

    def t_string(self, t):
        r'\"'
        t.lexer.begin('string')
        pass

    def t_string_string(self, t):
        r'[^\"]*\"'
        t.lexer.begin('INITIAL')
        return t

    def t_string_error(self, t):
        print(f'ERROR tokenizando un string en {t.lexer.lineno}')
        t.lexer.skip(1)

    t_arroba = r'@'

    t_ignore_tab = r'\t+'

    # t_newline = r'\n+'

    def t_type(self, t):
        r'[A-Z][a-zA-Z0-9_]*'
        lex =  t.value.lower()
        if lex in reserved:
            # if lex in ('true', 'false'):
            #     t.type = 'type'
            # else:
            t.type = reserved[lex]
        return t

    def t_id(self, t):
        r'[a-z_][a-zA-Z0-9_]*'
        if t.value.lower() in reserved:
            t.type = reserved[t.value.lower()]
        return t

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_chunkComment_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)
        self.tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.tokens.append(tok)
        
        return self.tokens