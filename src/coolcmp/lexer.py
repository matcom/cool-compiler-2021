from ply import lex
from ply.lex import TOKEN

import errors as err


class Lexer:
    """
    Cool Lexer.
    """
    def __init__(self, build_lexer=False, debug=False):
        self.lexer = None
        self.errors = []

        if build_lexer:
            self.lexer = lex.lex(module=self, debug=True)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    states = (
        ('STR', 'exclusive'),
        ('COMM', 'exclusive')
    )

    reserved = {
        'class': 'CLASS',
        'inherits': 'INHERITS',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'fi': 'FI',
        'while': 'WHILE',
        'loop': 'LOOP',
        'pool': 'POOL',
        'case': 'CASE',
        'of': 'OF',
        'esac': 'ESAC',
        'let': 'LET',
        'new': 'NEW',
        'isvoid': 'ISVOID',
        'not': 'NOT',
        'in': 'IN',
    }

    tokens = [
        # Identifiers
        'TYPE', 'ID',

        # Built-in types
        'INT', 'STRING', 'BOOL',

        # Special Notation
        'PLUS', 'MINUS', 'STAR', 'DIV', 'LESS', 'LEQ', 'EQ', 'COMP',
        'COLON', 'SEMI', 'COMMA', 'DOT', 'ASSIGN', 'ARROW', 'AT',
        'OPAR', 'CPAR', 'OCCUR', 'CCUR'

    ] + list(reserved.values())

    # Tokens defined as strings go after defined in functions.
    # This order is not relevant, they are ordered by length (longer first).
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_STAR = r'\*'
    t_DIV = r'\/'
    t_LESS = r'\<'
    t_LEQ = r'\<\='
    t_EQ = r'\='
    t_COMP = r'\~'
    t_COLON = r'\:'
    t_SEMI = r'\;'
    t_COMMA = r'\,'
    t_DOT = r'\.'
    t_ASSIGN = r'\<\-'
    t_ARROW = r'\=\>'
    t_AT = r'\@'
    t_OPAR = r'\('
    t_CPAR = r'\)'
    t_OCCUR = r'\{'
    t_CCUR = r'\}'

    t_ignore = ' \t\f\r'
    t_ignore_comment = r'\-\-[^\n]*'

    # #########################
    # ##### INITIAL state #####
    # #########################

    # match types
    @TOKEN(r'[A-Z]\w*')
    def t_TYPE(self, t: lex.LexToken) -> lex.LexToken:
        if t.value[0] in ('t', 'f') and t.value.lower() in ('true', 'false'):
            t.type = 'BOOL'
        else:
            t.type = self.reserved.get(t.value.lower(), 'TYPE')

        return t

    # match ids
    @TOKEN(r'[a-z]\w*')
    def t_ID(self, t: lex.LexToken) -> lex.LexToken:
        if t.value[0] in ('t', 'f') and t.value.lower() in ('true', 'false'):
            t.type = 'BOOL'
        else:
            t.type = self.reserved.get(t.value.lower(), 'ID')

        return t

    # match integers
    @TOKEN(r'\d+')
    def t_INT(self, t: lex.LexToken) -> lex.LexToken:
        t.value = int(t.value)

        return t

    # also defined for COMM state, newline tracker
    @TOKEN(r'\n+')
    def t_INITIAL_COMM_newline(self, t: lex.LexToken):
        t.lexer.lineno += len(t.value)

    # in case of error
    def t_error(self, t: lex.LexToken):
        t.lexer.skip(1)

        line, col = t.lexer.lineno, self.find_column(t.lexer.lexdata, t)
        self.errors.append(err.LEX_ERROR % (line, col, t.value[0]))

    # #####################
    # ##### STR state #####
    # #####################

    t_STR_ignore = ''

    @TOKEN(r'"')
    def t_begin_STR(self, t: lex.LexToken):
        t.lexer.string_start = t.lexer.lexpos - 1
        t.lexer.push_state('STR')

    @TOKEN(r'"')
    def t_STR_end(self, t: lex.LexToken) -> lex.LexToken:
        t.value = t.lexer.lexdata[t.lexer.string_start: t.lexer.lexpos]
        t.type = 'STRING'
        t.lexer.pop_state()

        return t

    @TOKEN(r'\n+')
    def t_STR_newline(self, t: lex.LexToken):
        line, col = t.lexer.lineno, self.find_column(t.lexer.lexdata, t)
        self.errors.append(err.UNT_STR % (line, col))

        t.lexer.lineno += len(t.value)
        t.lexer.pop_state()

    @TOKEN(r'\\(.|\n)')
    def t_STR_escaped(self, t: lex.LexToken):
        lookahead = t.value[1]

        if lookahead == '\n':
            t.lexer.lineno += 1
        elif lookahead == '0':  # TODO: Not detecting null caracter in sting3.cl
            line, col = t.lexer.lineno, self.find_column(t.lexer.lexdata, t)
            self.errors.append(err.NULL_STR % (line, col + 1))

    @TOKEN(r'[^"\n\\\0]+')
    def t_STR_char(self, t: lex.LexToken):
        pass

    def t_STR_error(self, t: lex.LexToken):
        t.lexer.skip(1)

    def t_STR_eof(self, t: lex.LexToken):
        line, col = t.lexer.lineno, self.find_column(t.lexer.lexdata, t)
        self.errors.append(err.EOF_STR % (line, col))

    # ######################
    # ##### COMM state #####
    # ######################

    t_COMM_ignore = ''

    @TOKEN(r'\(\*')
    def t_begin_COMM(self, t: lex.LexToken):
        t.lexer.comment_start = t.lexer.lexpos
        t.lexer.level = 1
        t.lexer.push_state('COMM')

    @TOKEN(r'\(\*')
    def t_COMM_new(self, t: lex.LexToken):
        t.lexer.level += 1

    @TOKEN(r'\*\)')
    def t_COMM_end(self, t: lex.LexToken):
        t.lexer.level -= 1

        if t.lexer.level == 0:
            t.lexer.pop_state()

    def t_COMM_error(self, token):
        token.lexer.skip(1)

    def t_COMM_eof(self, t: lex.LexToken):
        line, col = t.lexer.lineno, self.find_column(t.lexer.lexdata, t)
        self.errors.append(err.EOF_COMM % (line, col))

    # #####################
    # not lexical functions
    # #####################

    def find_column(self, input_text: str, token: lex.LexToken) -> int:
        """
        Used for compute column in case of error.
        """
        line_start = input_text.rfind('\n', 0, token.lexpos) + 1

        return (token.lexpos - line_start) + 1

    def input(self, cool_source_code):
        if self.lexer is None:
            raise Exception('You must call first build method.')

        self.lexer.input(cool_source_code)

    def __iter__(self):
        for token in self.lexer:
            yield token

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print('Usage: python3 lexer.py program.cl')
        exit()
    elif not sys.argv[1].endswith('.cl'):
        print('COOl source code files must end with .cl extension.')
        print('Usage: python3 lexer.py program.cl')
        exit()

    cool_program = open(sys.argv[1], encoding='utf8').read()
    # lexer = Lexer(build_lexer=True, debug=True)
    lexer = Lexer()
    lexer.build(debug=False)
    lexer.input(cool_program)

    tokens = [(t.value, t.type) for t in lexer]
    # print(tokens)

    for i in range(10):
        try:
            print(lexer.errors[i])
        except IndexError:
            break

    print(len(lexer.errors))
