class LexicographicError:
    def __init__(self, line: int, col: int, message: str) -> None:
        self.line = line
        self.col = col
        self.message = message

    def __str__(self) -> str:
        return f'({self.line},{self.col}) - LexicographicError: ERROR "{self.message}"'

    def __repr__(self) -> str:
        return str(self)
  