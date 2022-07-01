import ply.lex as lex
import sys
from .error_token import ErrorToken

class MyLexer():
    def __init__(self, debug=False, lextab="lextab", optimize="False", outputdir="", debuglog=None, errorlog=None):
        self.build(
            debug=debug, lextab=lextab, optimize=optimize, outputdir=outputdir, debuglog=debuglog, errorlog=errorlog)
    
    # Build the lexer
    def build(self, **kwargs):
        self.tokens = self.get_basic_tok() + list(self.get_reserved_keywds().values()) + list(self.get_builtin_types().values())
        self.reserved = list(self.get_reserved_keywds().values()) + list(self.get_builtin_types().values())
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)

    # The tokens list
    def get_basic_tok(self):
        return [
            "INTEGER",
            "STRING",
            "BOOLEAN",
            "PLUS",
            "MINUS",
            "MULTIPLY",
            "DIVIDE",
            "EQUAL",
            "LESS",
            "LESSEQ",
            "ASSIGN",
            "NOX",
            "ID",
            "TYPE",
            "LPAREN",
            "RPAREN",
            "LBRACE",
            "RBRACE",
            "COLON",
            "SEMIC",
            "COMMA",
            "DOT",
            "ARROBA",
            "ARROW",
            "LexicographicError"
        ]

    def get_reserved_keywds(self):
        return {
            "class": "CLASS",
            "case": "CASE",
            "esac": "ESAC",
            "let": "LET",
            "in": "IN",
            "inherits": "INHERITS",
            "isvoid": "ISVOID",
            "new": "NEW",
            "if": "IF",
            "else": "ELSE",
            "then": "THEN",
            "fi": "FI",
            "while": "WHILE",
            "loop": "LOOP",
            "pool": "POOL",
            "true": "TRUE",
            "false": "FALSE",
            "not": "NOT",
            "of": "OF"
        }

    def get_builtin_types(self):
        return {
            "Object": "OBJECT_TYPE",
            "Int": "INT_TYPE",
            "String": "STRING_TYPE",
            "Bool": "BOOL_TYPE",
            "SELF_TYPE": "SELF_TYPE",
            "Main": "MAIN_TYPE",
            "IO": "IO_TYPE"
        }

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_EQUAL = r'\='
    t_LESS = r'\<'
    t_LESSEQ = r'\<\='
    t_ASSIGN = r'\<\-'
    t_NOX = r'~'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r'\:'
    t_SEMIC = r'\;'
    t_COMMA = r'\,'
    t_DOT = r'\.'
    t_ARROBA = r'\@'
    t_ARROW = r'\=\>'
    t_ignore = ' \t\r\f'
    t_ignore_LINE_COMMENT = r"\-\-[^\n]*"

    # Regular expression rules with some action code
    def t_INTEGER(self, tok):
        r"\d+"
        tok.value = int(tok.value)
        return tok

    def t_ID(self, tok):
        r"[a-z][a-zA-Z_0-9]*"
        if self.get_reserved_keywds().__contains__(str.lower(tok.value)):
            tok.value = str.lower(tok.value)
            tok.type = self.get_reserved_keywds()[str.lower(tok.value)]
        else:
            tok.type = "ID"
        return tok

    def t_TYPE(self, tok):
        r"[A-Z][a-zA-Z_0-9]*"
        if self.get_reserved_keywds().__contains__(str.lower(tok.value)):
            tok.value = str.lower(tok.value)
            tok.type = self.get_reserved_keywds()[str.lower(tok.value)]
        else:
            tok.type = "TYPE"
        return tok
    
    def t_newline(self, tok):
        r"\n+"
        tok.lexer.lineno += len(tok.value)

    states = (
        ('STRING', 'exclusive'),
        ('COMMENT', 'exclusive')
    )

    # String Matching State 
    t_STRING_ignore = ''

    def t_STRING_newline(self, tok):
        r"\n"
        tok.lexer.lineno += 1
        if not tok.lexer.backslashed:
            error = ErrorToken(f'Unterminated string constant', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
            self.errors.append(error)
            tok.lexer.pop_state()
            return error
        else:
            tok.lexer.backslashed = False

    def t_start_string_state(self, tok):
        r"\""
        tok.lexer.push_state("STRING")
        tok.lexer.backslashed = False
        tok.lexer.string = ""

    def t_STRING_end(self, tok):
        r"\""
        if not tok.lexer.backslashed:
            tok.lexer.pop_state()
            tok.value = tok.lexer.string
            tok.type = "STRING"
            return tok
        else:
            tok.lexer.string += '"'
            tok.lexer.backslashed = False
    
    def t_STRING_null(self, tok):
        r"\0"
        error = ErrorToken(f'String contains null character', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
        self.errors.append(error)

    def t_STRING_anything(self, tok):
        r"[^\n]"
        if tok.lexer.backslashed:
            if tok.value == 'b':
                tok.lexer.string += '\b'
            elif tok.value == 'n':
                tok.lexer.string += '\n'
            elif tok.value == 'f':
                tok.lexer.string += '\f'
            elif tok.value == 't':
                tok.lexer.string += '\t'
            elif tok.value == '\\':
                tok.lexer.string += '\\'
            else:
                tok.lexer.string += tok.value
            tok.lexer.backslashed = False
        else:
            if tok.value != '\\':
                tok.lexer.string += tok.value
            else:
                tok.lexer.backslashed = True

    def t_STRING_error(self, tok):
        error = ErrorToken(f'{tok.value[0]} in string constant', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
        self.errors.append(error)
        return error
    
    def t_STRING_eof(self, tok):
        error = ErrorToken(f'EOF in string constant', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
        tok.lexer.pop_state()
        self.errors.append(error)
        return error

    # Comments Multiline State
    t_COMMENT_ignore = ''

    def t_COMMENT_newline(self, tok):
        r"\n+"
        tok.lexer.lineno += len(tok.value)
    
    def t_start_comment_state(self, tok):
        r'\(\*'
        tok.lexer.push_state("COMMENT")
        tok.lexer.comment_count = 0
    
    def t_COMMENT_end(self, tok):
        r'\*\)'
        if tok.lexer.comment_count == 0:
            tok.lexer.pop_state()
        else:
            tok.lexer.comment_count -= 1

    def t_COMMENT_another(self, tok):
        r'\(\*'
        tok.lexer.comment_count += 1
    
    def t_COMMENT_error(self, tok):
        tok.lexer.skip(1)
    
    def t_COMMENT_eof(self, tok):
        error = ErrorToken(f'EOF in comment', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
        tok.lexer.pop_state()
        self.errors.append(error)
        return error

    # Error handling
    def t_error(self, tok):
        error = ErrorToken(f'ERROR "{tok.value[0]}"', tok.lineno, self.find_col(tok.lexer.lexdata,tok.lexpos))
        tok.lexer.skip(1)
        self.errors.append(error)
        return error
    
    def find_col(self, input, lexpos):
        _start = input.rfind('\n', 0, lexpos) + 1
        return (lexpos - _start) + 1

    def token(self):
        return self.lexer.token()
    
    def tokenize(self, _cool_program):
        self.lexer.input(_cool_program)
        _tokens = []
        while True:
            _tok = self.token()
            if not _tok:
                raise Exception()
            _tokens.append(_tok)
        return(_tokens)

    