from typing import Text


class CoolError(Exception):
    def __init__(self, column: int, line: int, text: str):
        super().__init__(text)
        self.column = column
        self.line = line
        self.text = text

    @property
    def errorType(self):
        return "Cool Compiler Error"

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.errorType}: {self.text}'

    def __repr__(self):
        return str(self)
