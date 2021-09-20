from typing import List, Tuple

from cool.error.error_tracker import ErrorTracker
from cool.error.errors import LexerCoolError
from cool.grammar import cool_grammar as cool_G
import ply.lex as lex

class Lex():
    def __init__(self, lex):
        self.lex = lex

    def set_type(self, new):
        self.type = new

    def set_row(self, new):
        self.row = new

    def set_column(self, new):
        self.column = new

    def __str__(self):
        return self.lex

    def __getitem__(self, i):
        if i == 0:
            return self.lex

        elif i == 1:
            return self.row

        elif i == 2:
            return self.column

        elif i == 3:
            return self.type

class PlyCoolToken(lex.LexToken):

    def __init__(self, lex:str, typex, line:int, column:int, is_eof=False):
        self.set_lex(lex)
        self.set_type(typex)
        self.set_position(line, column)
        self.__is_eof = is_eof
        
    @property
    def is_eof(self):
        return self.__is_eof

    def set_lex(self, lex:str):
        self.lex = Lex(lex)
        self.value = Lex(lex)

    def set_type(self, typex:str):
        self.lex.set_type(typex)
        self.value.set_type(typex)
        self.type = typex
        self.token_type = typex
        self.typex = typex

    def set_position(self, line:int, column:int):
        self.lex.set_row(line)
        self.value.set_row(line)
        self.lex.set_column(column)
        self.value.set_column(column)
        self.lineno = line
        self.line = line
        self.column = column
        self.lexpos = column

    def get_lex(self)->str:
        return self.lex

    def get_type(self)->str:
        return self.typex

    def get_position(self)->Tuple[int,int]:
        return (self.line, self.column)

    def __str__(self):
        return f"{self.lex}:{self.type} Line {self.line} Column{self.column}"

    def __repr__(self):
        return str(self)

class PlyLexer():

    @staticmethod
    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def __init__(self):
        self.error_tracker = ErrorTracker() # Error tracker implementation

        reserved = {
            'if' : 'IF',
            'then' : 'THEN',
            'fi' : 'FI',
            'else' : 'ELSE',
            'case' : 'CASE',
            'of' : 'OF',
            'esac' : 'ESAC',
            'class' : 'CLASS',
            'inherits' : 'INHERITS',
            'let' : 'LET',
            'in' : 'IN',
            'while' : 'WHILE',
            'loop' : 'LOOP',
            'pool' : 'POOL',
            'new' : 'NEW',
            'isvoid' : 'ISVOID',
            'not' : 'NOT',
            'true' : 'TRUE',
            'false' : 'FALSE'
        }

        tokens = (
            'OBJECTID',
            'TYPEID',
            'NUMBER',
            'PLUS',
            'MINUS',
            'STAR',
            'DIV',
            'EQ',
            'LEQ',
            'LESS',
            'NEG',
            'OPAR',
            'CPAR',
            'OCUR',
            'CCUR',
            'ASSIGN',
            'SEMI',
            'COLON',
            'SIGNALER',
            'ARROBA',
            'STRING',
            'COMMENT',
            'DOT',
            'COMMA'
        ) + tuple(reserved[x] for x in reserved.keys())

        
        self.terminals = {
            'IF'            : cool_G.ifx,
            'THEN'          : cool_G.then,
            'ELSE'          : cool_G.elsex,
            'FI'            : cool_G.if_r,
            'WHILE'         : cool_G.whilex,
            'LOOP'          : cool_G.loop,
            'POOL'          : cool_G.loop_r,
            'OCUR'          : cool_G.ocur,
            'CCUR'          : cool_G.ccur,
            'COLON'         : cool_G.colon,
            'SEMI'          : cool_G.semi,
            'COMMA'         : cool_G.comma,
            'DOT'           : cool_G.dot,
            'OPAR'          : cool_G.opar,
            'CPAR'          : cool_G.cpar,
            'PLUS'          : cool_G.plus,
            'MINUS'         : cool_G.minus,
            'DIV'           : cool_G.div,
            'STAR'          : cool_G.star,
            'NOT'           : cool_G.notx,
            'NEG'           : cool_G.roof,
            'LESS'          : cool_G.less,
            'LEQ'           : cool_G.less_eq,
            # 'GREAT'         : cool_G.greater,
            # 'GEQ'           : cool_G.greater_eq,
            'EQ'            : cool_G.equal,
            'LET'           : cool_G.let,
            'IN'            : cool_G.inx,
            'CASE'          : cool_G.case,
            'OF'            : cool_G.of,
            'ESAC'          : cool_G.case_r,
            'SIGNALER'      : cool_G.arrow,
            'ASSIGN'        : cool_G.assign,
            'TRUE'          : cool_G.true,
            'FALSE'         : cool_G.false,
            'NUMBER'        : cool_G.num,
            'STRING'        : cool_G.string,
            'CLASS'         : cool_G.classx,
            'INHERITS'      : cool_G.inherits,
            'NEW'           : cool_G.new,
            'ISVOID'        : cool_G.isvoid,
            'OBJECTID'      : cool_G.idx,
            'TYPEID'        : cool_G.typex,
            'ARROBA'        : cool_G.at,
            'COMMENT'       : cool_G.comment_open,
            'COMMENT'       : cool_G.comment_close}

        # def t_COMMENTMULTI(t):
        #     r'\(\*(.|\n)*?\*\)'
        #     t.lexer.lineno += t.value.count("\n")

        # def t_COMMENTMULTIUNFINISHED(t):
        #     r'\(\*(.|\n)*'
        #     t.lexer.lineno += t.value.count("\n")
        #     msg = 'EOF in comment'
        #     self.add_error(LexerCoolError(msg, token = PlyCoolToken(t.value, t.type, t.lexer.lineno - 1, t.lexer.lexpos - 1)))

        def t_STRING(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}"'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, token = PlyCoolToken(t.value, t.type, line, pos)))
            return t

        def t_STRINGUNFINISHED(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}\n'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, token = PlyCoolToken(t.value, t.type, line, pos)))
            msg = 'Unterminated string constant'
            self.add_error(LexerCoolError(msg, token = PlyCoolToken(t.value, t.type, t.lexer.lineno - 1, t.lexer.lexpos - 1)))

        def t_STRINGUNFINISHEDEOF(t):
            r'"([^\r\n"\\]|(\\\n)|(\\.)){0,1024}'
            t.lexer.lineno += t.value.count("\n")
            null_ch = 'String contains null character'
            for i in range(len(t.value)):
                if t.value[i] == '\x00':
                    pos = t.lexer.lexpos - (len(t.value) - i)
                    line = t.lexer.lineno - t.value[:i].count("\n")
                    self.add_error(LexerCoolError(null_ch, token = PlyCoolToken(t.value, t.type, line, pos)))
            msg = 'EOF in string constant'
            self.add_error(LexerCoolError(msg, token = PlyCoolToken(t.value, t.type, t.lexer.lineno, t.lexer.lexpos)))

        def t_NUMBER(t):
            r'\d+'
            try:
                int(t.value)
            except ValueError:
                msg = "Integer value too large %d", t.value
                self.add_error(LexerCoolError(msg, token = PlyCoolToken(t.value, t.type, t.lineno, t.lexpos))) # TODO Set Token column
                t.value = 'Invalid'
            return t

        def t_OBJECTID(t):
            r'[a-z][a-zA-Z0-9_]*'
            low = t.value.lower()
            t.type = reserved.get(low,'OBJECTID')
            return t

        def t_TYPEID(t):
            r'[A-Z][a-zA-Z0-9_]*'
            low = t.value.lower()
            if low == 'true':
                t.type = 'TYPEID'

            elif low == 'false':
                t.type = 'TYPEID'

            else:
                t.type = reserved.get(low, 'TYPEID')

            return t

        def t_COMMENTSINGLE(t):
            r'(--.*)'
        

        t_PLUS      = r'\+'
        t_MINUS     = r'-'
        t_STAR      = r'\*'
        t_DIV       = r'/'
        t_OPAR      = r'\('
        t_CPAR      = r'\)'
        t_OCUR      = r'\{'
        t_CCUR      = r'\}'
        t_EQ        = r'='
        t_ASSIGN    = r'<-'
        t_LEQ       = r'<='
        t_LESS      = r'<'
        t_NEG       = r'~'
        t_SEMI      = r';'
        t_COLON     = r':'
        t_SIGNALER  = r'=>'
        t_ARROBA    = r'@'
        t_DOT       = r'\.'
        t_COMMA     = r','

        t_ignore = " \t"

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += t.value.count("\n")

        def t_error(t):
            msg = f'ERROR "{t.value[0]}"'
            self.add_error(LexerCoolError(msg, token = PlyCoolToken(t.value[0], t.type, t.lineno, t.lexpos))) # TODO Set Token column
            t.lexer.skip(1)

        self.lexer = lex.lex()

    def __call__(self, program_string:str):
        self.error_tracker = ErrorTracker()
        count = 0
        lines = 0
        passes = 0
        semi_clean_string = []
        for i in range(len(program_string)):
            if passes > 0:
                passes -= 1
            elif program_string[i] == '(' and i + 1 < len(program_string) and program_string[i + 1] == '*':
                count += 1
                semi_clean_string.append(' ')
                semi_clean_string.append(' ')
                if i + 2 < len(program_string) and program_string[i + 2] == ')':
                    semi_clean_string.append(' ')
                    passes = 2
                
                else:
                    passes = 1

            elif program_string[i] == '*' and i + 1 < len(program_string) and program_string[i + 1] == ')' and count > 0:
                count -= 1
                semi_clean_string.append(' ')
                semi_clean_string.append(' ')
                passes = 1

            elif count > 0 and program_string[i] != '\n':
                semi_clean_string.append(' ')

            elif program_string[i] == '\n':
                semi_clean_string.append(program_string[i])
                lines += 1

            else:
                semi_clean_string.append(program_string[i])

        clean = ''.join(semi_clean_string)
        # print(clean)
        # print(len(clean))
        # print(len(program_string))
        self.lexer.input(clean)
        result = []
        base_line = -1
        while True:
            tok = self.lexer.token()
            # if base_line < 0:
            #     base_line = tok.lineno - 1

            if not tok:
                break
            result.append(PlyCoolToken(tok.value, tok.type, tok.lineno, self.find_column(program_string, tok)))

        if count > 0:
            self.add_error(LexerCoolError('EOF in comment', token = PlyCoolToken('', '', lines + 1, len(program_string))))

        for error in self.error_tracker.get_errors():
            error.token.set_position(error.token.lineno, self.find_column(program_string, error.token))

        for token in result:
            token.set_type(self.terminals[token.token_type])

        result.append(PlyCoolToken('EOF', cool_G.G.EOF, lines + 1, len(program_string), True))
        result[-1].set_position(result[-1].line, self.find_column(program_string, result[-1]))

        return result

    def add_error(self, error:LexerCoolError):
        self.error_tracker.add_error(error)
    
    def get_errors(self)->List[LexerCoolError]:
        errors = self.error_tracker.get_errors()
        return errors
