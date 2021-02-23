
class CoolError(Exception):
    def __init__(self, line, column, text):
        super().__init__(text)
        self.line = line
        self.column = column

    @property
    def error_type(self):
        return 'CoolError'

    @property
    def text(self):
        return self.args[0]

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)

class CompilerError(CoolError):
    '''
    Errores detectados con la entrada del compilador.
    '''
    WRONG_EXTENTION = 'Cool program file must end with a ".cl" extension'
    UNKNOWN_FILE = 'The file "%s" does not exist'

    @property
    def error_type(self):
        return 'CompilerError'

class LexicographicError(CoolError):
    '''
    Errores detectados por el lexer.
    '''
    UNKNOWN_TOKEN = 'ERROR "%s"\n'
    UNTERMINATED_STRING = 'Unterminated string constant\n'
    EOF_COMMENT = 'EOF in comment\n'
    EOF_STRING = 'EOF in string constant\n'
    NULL_STRING = 'String contains null character\n'

    @property
    def error_type(self):
        return 'LexicographicError'

class SyntacticError(CoolError):
    '''
    Errores detectados por el parser.
    '''
    ERROR = 'ERROR at or near "%s"'

    @property
    def error_type(self):
        return 'SyntacticError'

