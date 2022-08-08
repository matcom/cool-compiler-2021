class CoolError(Exception):
    def __init__(self, error_type, text, line, column):
        self.type = error_type
        self.text = text
        self.line = line
        self.column = column

    def __str__(self):
        return f'{self.line, self.column} - {self.type}: {self.text}'

    def __repr__(self):
        return str(self)


class LexicographicError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('LexicographicError', text, line, column)


class SyntacticError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('SyntacticError', text, line, column)


class SemanticError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('SemanticError', text, line, column)


class TypexError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('TypeError', text, line, column)


class NamexError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('NameError', text, line, column)


class AttributexError(CoolError):
    def __init__(self, text, line, column):
        super().__init__('AttributeError', text, line, column)
