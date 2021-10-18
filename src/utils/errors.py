class CoolError():
    def __init__(self, error_type, text, line, column):
        self.type = type
        self.text = text
        self.line = line
        self.column = column

    def __str__(self):
        return f'({self.line, self.column}) - {self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)


class LexicographicError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('LexicograficError', text, line, column)


class SyntacticError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('SyntacticError', text, line, column)


class SemanticError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('SemanticError', text, line, column)
