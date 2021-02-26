class LexicographicError:
    def __init__(self, line: int, col: int, char: str) -> None:
        self.line = line
        self.col = col
        self.char = char

    def __str__(self) -> str:
        return f'({self.line},{self.col}) - LexicographicError: ERROR "{self.char}"'

    def __repr__(self) -> str:
        return str(self)
  


def set_pos(token):
    token.col = token.lexer.col
    token.lexer.col += len(token.value)