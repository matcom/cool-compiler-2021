class CoolpylerError(object):
    """
    Errors reported by the compiler
    """

    def __init__(self, line, column, type, msg) -> None:
        self.line = line
        self.column = column
        self.type = type
        self.msg = msg


class CompilerError(CoolpylerError):
    """
    Error reported when an anomaly in the compiler's input is detected.
    For example, if the input file doesn't exist.
    """

    def __init__(self, msg) -> None:
        CoolpylerError.__init__(self, 0, 0, "CompilerError", msg)


class LexicographicError(CoolpylerError):
    """
    Error reported by lexer
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "LexicographicError", msg)


class SyntacticError(CoolpylerError):
    """
    Error reported by parser
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "SyntacticError", msg)


class NameError(CoolpylerError):
    """
    Error reported when an identifier is referenced in a scope where it is not visible.
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "NameError", msg)


class TypeError(CoolpylerError):
    """
    Error reported when a problem with types is detected. Includes:
    - type incompatibility between `rvalue` and `lvalue`,
    - undefined operation between objects of certain types
    - referenced type is undefined
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "TypeError", msg)


class AttributeError(CoolpylerError):
    """
    Error reported when an attribute or method is referenced but undefined.
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "AttributeError", msg)


class SemanticError(CoolpylerError):
    """
    Any kind of semantic error
    """

    def __init__(self, line, column, msg) -> None:
        CoolpylerError.__init__(self, line, column, "SemanticError", msg)


class InvalidInputFileError(CompilerError):
    """
    Reported when input file is invalid.
    """

    def __init__(self, path: str) -> None:
        CompilerError.__init__(self, f"File `{path}` is not a valid file.")


class UnexpectedCharError(LexicographicError):
    """
    Reported the lexer encounters an unexpected character.
    """

    def __init__(self, line: int, column: int, char: str) -> None:
        LexicographicError.__init__(
            self, line, column, f"Unexpected character `{char}`."
        )


class UnexpectedTokenError(SyntacticError):
    """
    Reported the parser encounters an unexpected Token.
    """

    def __init__(self, line: int, column: int, token: str, expected: set) -> None:
        SyntacticError.__init__(
            self,
            line,
            column,
            f"Unexpected token `{token}`. Expected one of {expected}.",
        )


class UnexpectedEOFError(SyntacticError):
    """
    Reported the parser encounters end of file unexpectedly.
    """

    def __init__(self, expected: set) -> None:
        SyntacticError.__init__(
            self, 0, 0, f"Unexpected end of file. Expected one of {expected}."
        )
