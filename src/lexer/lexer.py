import ply.lex as lex
from utils.errors import _LexicographicError
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
]
_tokens += list(reserved.values())
def find_all(s):
    b = [] 
    a = s.find('a')
    while a != -1:
        b.append(a)
        a = s.find('a', a + 1)
    return b

def find_last(text, row, col):
    first = text.find("\n")
    temp_text = text
    add_col= first
    add_row = 0
    loop = True
    while loop:
        if first > 0:
            if temp_text[first-1] == "\\":
                temp_text = temp_text[first+1: ]
                add_col = first
                first = temp_text.find("\n")
                add_row += 1
                loop = True
            else:
                loop = False
                if first + 1 == len(temp_text):
                    eof = True
                else:
                    eof = False
        else:
            # cuando no hay newline
            if first == -1:
                add_col = len(temp_text) + 1
                eof = True
            # cuando hay newline pero al inicio :)
            else:
                add_col = 0
                eof = False
            break
                
    if add_row == 0:
        add_col += col
    add_row += row
    return (add_row, add_col, eof)

class CoolLexer:
    tokens = _tokens
    states = (
        ('chunkComment', 'exclusive'),
        ('string', 'exclusive')
    )
    col = 0
    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.col = 0

    # Compute column.
    #   input is the input text string
    #   token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1  #parentesis?

    t_ignore_space = r'[ ]+'
    # def t_space(self,t):
    #     r'[ ]+'
    #     pass

    # t_ignore_lineComment = r'--.*'
    # preguntarle a andy como no hacer esto con la precedencia...
    def t_ignore_lineComment(self, t):
        r'--.*'
        pass

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
            self.errors.append(_LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), 'EOF in comment'))
            # print(_LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), 'EOF in comment'))
        return None

    # t_assignArrow = r'<\-'
    def t_assignArrow(self, t):
        r'<\-'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_rArrow = r'=>'
    def t_rArrow(self, t):
        r'=>'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_leq = r'<='
    def t_leq(self, t):
        r'<='
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_semi = r';'
    def t_semi(self, t):
        r';'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_colon = r':'
    def t_colon(self, t):
        r':'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_comma = r','
    def t_comma(self, t):
        r','
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_dot = r'\.'
    def t_dot(self, t):
        r'\.'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_opar = r'\('
    def t_opar(self, t):
        r'\('
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_cpar = r'\)'
    def t_cpar(self, t):
        r'\)'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_ocur = r'\{'
    def t_ocur(self, t):
        r'\{'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_ccur = r'\}'
    def t_ccur(self, t):
        r'\}'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_plus = r'\+'
    def t_plus(self,t):
        r'\+'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_minus = r'\-'
    def t_minus(self,t):
        r'\-'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    
    # t_star = r'\*'
    def t_star(self,t):
        r'\*'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_div = r'/'
    def t_div(self,t):
        r'/'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_equal = r'='
    def t_equal(self,t):
        r'='
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_lneq = r'<'
    def t_lneq(self, t):
        r'<'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    # t_complement = r'\~'
    def t_complement(self, t):
        r'\~'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    def t_string(self, t):
        r'\"'
        t.lexer.begin('string')
        pass

    def t_string_string(self, t):
        r"([^\n]|(?<!\\)(\\\\)*?\\\n)*?(?<!\\)(\\\\)*?\""
        col = self.find_column(t.lexer.lexdata,t)+1
        row = t.lineno
        errors = []
        for c in t.value[1:]:
            if c =='\x00':
                errors.append(_LexicographicError % (row, col, f'String contains null character'))
            if c == '\n':
                t.lexer.lineno += 1
                col = 0
            col += 1
        t.lexer.begin('INITIAL')
        if len(errors) != 0:
            self.errors += errors
        else:
            t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4) -1
            t.value = '"'+t.value
            return t
    # t_string = r"\"([^\x00\n]|(?<!\\)(\\\\)*?\\\n)*?(?<!\\)(\\\\)*?\""
    # t_string = r'\"[^\"]*\"'

    def t_string_error(self, t):
        a = self.find_column(t.lexer.lexdata,t)
        row, col, eof = find_last(t.value, t.lexer.lineno, self.find_column(t.lexer.lexdata,t))
        if eof:
            self.errors.append(_LexicographicError % (row, col, f'EOF in string constant'))
            # print(LexicographicError % (row, col, f'EOF in string constant'))
            t.lexer.skip(len(t.value))
        else:
            self.errors.append(_LexicographicError % (row, col, f'Unterminated string constant'))
            # print(LexicographicError % (row, col, f'Unterminated string constant'))
            t.lexer.skip(1)
        
        t.lexer.begin('INITIAL')
        
    # t_arroba = r'@'
    def t_arroba(self, t):
        r'@'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_ignore_tab = r'\t+'
    def t_tab(self, t):
        r'\t+'
        self.col += 4*len(t.value)
        # t.lexer.skip(len(t.value))
        
    def t_type(self, t):
        r'[A-Z][a-zA-Z0-9_]*'
        lex =  t.value.lower()
        if lex in reserved:
            t.type = reserved[lex]
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_id(self, t):
        r'[a-z][a-zA-Z0-9_]*'
        if t.value.lower() in reserved:
            t.type = reserved[t.value.lower()]
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_eof(self, t):
        a = 0
    
    # Error handling rule
    def t_error(self,t):
        # errores del string
        # if t.value[0] == '"':
        #     row, col, eof = find_last(t.value, t.lexer.lineno, self.find_column(t.lexer.lexdata,t))
        #     if eof:
        #         self.errors.append(LexicographicError % (row, col, f'EOF in string constant'))
        #         t.lexer.skip(len(t.value))
        #     else:
        #         self.errors.append(LexicographicError % (row, col, f'Unterminated string constant'))
        # else:
        self.errors.append(_LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), f'ERROR "{t.value[0]}"'))
        # print(LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), f'ERROR "{t.value[0]}"'))
        t.lexer.skip(1)

    def t_chunkComment_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.errors = []
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