class CoolpylerError(object):
    """
    Errors reported by the compiler
    """

    def __init__(self, line, column, type, msg) -> None:
        self.line = line
        self.column = column
        self.type = type
        self.msg = msg

    def __str__(self) -> str:
        return f"({self.line}, {self.column}) - {self.type}: {self.msg}"


# Compiler errors {{{


class CompilerError(CoolpylerError):
    """
    Error reported when an anomaly in the compiler's input is detected.
    For example, if the input file doesn't exist.
    """

    def __init__(self, msg) -> None:
        CoolpylerError.__init__(self, 0, 0, "CompilerError", msg)


class InvalidInputFileError(CompilerError):
    """
    Reported when input file is invalid.
    """

    def __init__(self, path: str) -> None:
        CompilerError.__init__(self, f"File `{path}` is not a valid file.")


# }}}


# Lexicographic errors {{{


class LexicographicError(CoolpylerError):
    """
    Error reported by lexer
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "LexicographicError", msg)


class UnexpectedCharError(LexicographicError):
    """
    Reported the lexer encounters an unexpected character.
    """

    def __init__(self, line: int, column: int, char: str) -> None:
        LexicographicError.__init__(self, line, column, f"Unexpected `{char}`.")


# }}}

# Syntactic errors {{{


class SyntacticError(CoolpylerError):
    """
    Error reported by parser
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolpylerError.__init__(self, line, column, "SyntacticError", msg)


class UnexpectedTokenError(SyntacticError):
    """
    Reported the parser encounters an unexpected Token.
    """

    def __init__(self, line: int, column: int, token: str) -> None:
        SyntacticError.__init__(
            self,
            line,
            column,
            f"Unexpected token `{token}`.",
        )


class UnexpectedEOFError(SyntacticError):
    """
    Reported the parser encounters end of file unexpectedly.
    """

    def __init__(self) -> None:
        SyntacticError.__init__(self, 0, 0, "Unexpected EOF.")


# }}}


# Semantic errors {{{


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


class IncompatibleTypesError(SemanticError):
    def __init__(self, line, column, type_a, type_b) -> None:
        SemanticError.__init__(
            self, line, column, f"Cannot convert {type_a} into {type_b}."
        )


class InvalidOperationError(SemanticError):
    def __init__(self, line, column, type_a, type_b) -> None:
        SemanticError.__init__(
            self, line, column, f"invalid operation {type_a} between {type_b}."
        )


class InvalidComparissonError(SemanticError):
    def __init__(self, line, column, type_a, type_b) -> None:
        SemanticError.__init__(
            self, line, column, f"invalid comparisson {type_a} between {type_b}."
        )


class IsReadOnlyError(SemanticError):
    def __init__(self, line, column, name) -> None:
        SemanticError.__init__(
            self, line, column, f"{name} is read only."
        )


class NotConformsError(SemanticError):
    def __init__(self, line, column, type_a, type_b) -> None:
        SemanticError.__init__(
            self, line, column, f"type {type_a} does not conforms {type_b}."
        )


class WrongArgsCountError(SemanticError):
    def __init__(self, line, column, method, n1, n2) -> None:
        SemanticError.__init__(
            self, line, column, f"Method {method} takes {n1} but {n2} were given."
        )


class WrongSignatureError(SemanticError):
    def __init__(self, line, column, method) -> None:
        SemanticError.__init__(
            self,
            line,
            column,
            f"Method {method} already defined with a different signature.",
        )


class VariableNotDefinedError(SemanticError):
    def __init__(self, line, column, variable) -> None:
        SemanticError.__init__(
            self,
            line,
            column,
            f"Variable {variable} not defined.",
        )


# }}}


# {{{


class InternalError(object):
    """
    Internal compiler errors
    """
    def __init__(self, message, context):
        self.message = message
        self.context = context


# }}}
