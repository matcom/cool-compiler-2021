
class Error:
    def __init__(self, line = None, column = None, text = ''):
        self.line = line
        self.column = column
        self.text = text
    def __str__(self):
        raise NotImplementedError()
    def __repr__(self):
        raise NotImplementedError()

class CompilerError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'CompilerError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'CompilerError: {self.text}'

class LexicographicError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'LexicographicError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'LexicographicError: {self.text}'

class SyntacticError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'SyntacticError: ERROR at or near {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'SyntacticError: ERROR at or near {self.text}'

class SemanticError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'SemanticError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'SemanticError: {self.text}'

class TypeError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'TypeError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'TypeError: {self.text}'

class NameError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'NameError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'NameError: {self.text}'

class AttributeError(Error):
    def __str__(self):
        return f'{self.line, self.column} - ' \
               f'AttributeError: {self.text}'
    def __repr__(self):
        return f'{self.line, self.column} - ' \
               f'AttributeError: {self.text}'