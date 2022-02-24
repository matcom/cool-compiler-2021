from ply import lex

from utils.errors import LexicographicError
from utils.utils import Token, tokens, reserved


class CoolLexer:

    states = (
        ('comments', 'exclusive'),
        ('strings', 'exclusive')
    )

    def __init__(self, **kwargs):
        self.errors = []
        self.reserved = reserved
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.lineno = 1
        self.lexer.linestart = 0
        self.text = None

    # Comments

    def t_comment(self, t):
        r'--.*($|\n)'
        t.lexer.lineno += 1
        t.lexer.linestart = t.lexer.lexpos

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

    def t_comments_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos

    def t_comments_error(self, t):
        t.lexer.skip(1)

    def t_comments_eof(self, t):
        self.compute_column(t)
        if t.lexer.level > 0:
            self.errors.append(LexicographicError(
                "EOF in comment", t.lineno, t.column))

    t_comments_ignore = '  \t\f\r\t\v'

    # Strings
    t_strings_ignore = ''

    def t_strings(self, t):
        r'\"'
        t.lexer.string_start = t.lexer.lexpos
        t.lexer.string = ''
        t.lexer.backslash = False
        t.lexer.begin('strings')

    def t_strings_end(self, t):
        r'\"'
        self.compute_column(t)

        if t.lexer.backslash:
            t.lexer.string += '"'
            t.lexer.backslash = False
        else:
            t.value = t.lexer.string
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
            return t

    def t_strings_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.compute_column(t)

        t.lexer.linestart = t.lexer.lexpos

        if not t.lexer.backslash:
            self.errors.append(LexicographicError(
                'Undeterminated string constant', t.lineno, t.column))
            t.lexer.begin('INITIAL')

    def t_strings_nill(self, t):
        r'\0'
        self.compute_column(t)
        self.errors.append(LexicographicError(
            'Null caracter in string', t.lineno, t.column))

    def t_strings_consume(self, t):
        r'[^\n]'

        if t.lexer.backslash:
            if t.value == 'b':
                t.lexer.string += '\b'
            elif t.value == 't':
                t.lexer.string += '\t'
            if t.value == 'f':
                t.lexer.string += '\f'
            elif t.value == 'n':
                t.lexer.string += '\n'
            elif t.value == '\\':
                t.lexer.string += '\\'
            else:
                t.lexer.string += t.value

            t.lexer.backslash = False
        else:
            if t.value != '\\':
                t.lexer.string += t.value
            else:
                t.lexer.backslash = True

    def t_strings_error(self, t):
        pass

    def t_strings_eof(self, t):
        self.compute_column(t)
        self.errors.append(LexicographicError(
            'EOF in string constant', t.lineno, t.column))

    t_ignore = '  \t\f\r\t\v'

    def compute_column(self, t):
        t.column = t.lexpos - t.lexer.linestart + 1

    def t_LPAREN(self, t):
        r'\('
        self.compute_column(t)
        return t

    def t_RPAREN(self, t):
        r'\)'
        self.compute_column(t)
        return t

    def t_LBRACE(self, t):
        r'\{'
        self.compute_column(t)
        return t

    def t_RBRACE(self, t):
        r'\}'
        self.compute_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.compute_column(t)
        return t

    def t_SEMICOLON(self, t):
        r';'
        self.compute_column(t)
        return t

    def t_COMMA(self, t):
        r','
        self.compute_column(t)
        return t

    def t_DOT(self, t):
        r'\.'
        self.compute_column(t)
        return t

    def t_AT(self, t):
        r'@'
        self.compute_column(t)
        return t

    def t_ASSIGN(self, t):
        r'<-'
        self.compute_column(t)
        return t

    def t_PLUS(self, t):
        r'\+'
        self.compute_column(t)
        return t

    def t_MINUS(self, t):
        r'-'
        self.compute_column(t)
        return t

    def t_STAR(self, t):
        r'\*'
        self.compute_column(t)
        return t

    def t_DIV(self, t):
        r'/'
        self.compute_column(t)
        return t

    def t_ARROW(self, t):
        r'=>'
        self.compute_column(t)
        return t

    def t_EQUAL(self, t):
        r'='
        self.compute_column(t)
        return t

    def t_LESSEQ(self, t):
        r'<='
        self.compute_column(t)
        return t

    def t_LESS(self, t):
        r'<'
        self.compute_column(t)
        return t

    def t_NOT(self, t):
        r'~'
        self.compute_column(t)
        return t

    def t_INT(self, t):
        r'\d+'
        t.value = int(t.value)
        self.compute_column(t)
        return t

    def t_ID(self, t):
        r'[a-z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        self.compute_column(t)
        return t

    def t_TYPE(self, t):
        r'[A-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'TYPE')
        self.compute_column(t)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.lexer.linestart = t.lexer.lexpos

    def t_error(self, t):
        self.compute_column(t)
        self.errors.append(LexicographicError(
            f'ERROR \"{t.value[0]}\"', t.lineno, t.column))
        t.lexer.skip(1)

    def tokenize(self, text):
        self.text = text
        self.lexer.input(text)
        tokens = []
        for token in self.lexer:
            tokens.append(Token(token.value, token.type,
                                token.lineno, token.column))
        self.lexer.lineno = 1
        self.lexer.linestart = 0
        return tokens

    def run(self, text):
        tokens = self.tokenize(text)
        if self.errors:
            for error in self.errors:
                print(error)
            raise Exception()

        return tokens
