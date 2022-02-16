class CoolCompilerError(object):
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


# Compiler errors


class CompilerError(CoolCompilerError):
    """
    Error reported when an anomaly in the compiler's input is detected.
    For example, if the input file doesn't exist.
    """

    def __init__(self, msg) -> None:
        CoolCompilerError.__init__(self, 0, 0, "CompilerError", msg)


class InvalidInputFileError(CompilerError):
    """
    Reported when input file is invalid.
    """

    def __init__(self, path: str) -> None:
        CompilerError.__init__(self, f"File `{path}` is not a valid file.")


# Lexicographic errors


class LexicographicError(CoolCompilerError):
    """
    Error reported by lexer
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolCompilerError.__init__(self, line, column, "LexicographicError", msg)


class UnexpectedCharError(LexicographicError):
    """
    Reported the lexer encounters an unexpected character.
    """

    def __init__(self, line: int, column: int, char: str) -> None:
        LexicographicError.__init__(self, line, column, f"Unexpected `{char}`.")


# Syntactic errors


class SyntacticError(CoolCompilerError):
    """
    Error reported by parser
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolCompilerError.__init__(self, line, column, "SyntacticError", msg)


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


# Semantic errors


class NameError(CoolCompilerError):
    """
    Error reported when an identifier is referenced in a scope where it is not visible.
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolCompilerError.__init__(self, line, column, "NameError", msg)


class TypeError(CoolCompilerError):
    """
    Error reported when a problem with types is detected. Includes:
    - type incompatibility between `rvalue` and `lvalue`,
    - undefined operation between objects of certain types
    - referenced type is undefined
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolCompilerError.__init__(self, line, column, "TypeError", msg)


class AttributeError(CoolCompilerError):
    """
    Error reported when an attribute or method is referenced but undefined.
    """

    def __init__(self, line: int, column: int, msg: str) -> None:
        CoolCompilerError.__init__(self, line, column, "AttributeError", msg)


class SemanticError(CoolCompilerError):
    """
    Any kind of semantic error
    """

    def __init__(self, line, column, msg) -> None:
        CoolCompilerError.__init__(self, line, column, "SemanticError", msg)


class IncompatibleTypesError(SemanticError):
    def __init__(self, line, column, type_a, type_b) -> None:
        SemanticError.__init__(
            self, line, column, f"Cannot convert {type_a} into {type_b}."
        )


class WrongSignatureError(SemanticError):
    def __init__(self, line, column, method) -> None:
        SemanticError.__init__(
            self,
            line,
            column,
            f"Method {method} already defined with a different signature.",
        )


# ----------------------------------------------
class Error(Exception):
    "Base class for exceptions"
    pass


class tokenizer_error(Error):
    "raised when tokenizer got unespected sequences of characters"

    def __init__(self, text, line):
        Error.__init__(
            self,
            f"Got {text} while analizing line {line}",
        )


class parsing_table_error(Error):
    "raised when T[X,t] possess more than one production"

    def __init__(self, production1, production2, invalid_sentence):
        Error.__init__(
            self,
            f"conflict betweeen {production1}  and {production2}, invalid sentence: {invalid_sentence}",
        )


class shift_reduce_error(Error):
    "raised when goto or action table in shift reduce parsers possess more than one production"

    def __init__(self, action1, action2, grammar, key=None):
        if action1[0] == action2[0] == "REDUCE":
            conflict = "Reduce-Reduce"
        else:
            conflict = "Shift-Reduce"

        Error.__init__(
            self,
            f"When analizing {key}, {conflict} conflict!!! betweeen {action1}  and {action2}. Grammar given is not {grammar}",
        )


class invalid_sentence_error(Error):
    "raised when w is not in G"

    def __init__(
        self,
        w,
        pos,
        actual_token,
        expected_token=None,
        message="",
        output=None,
        operations=None,
    ):
        if expected_token != None:
            Error.__init__(
                self,
                f"Invalid sentence {w}. Expected {expected_token} at position {pos} but received {actual_token} instead. {message}",
            )
        else:
            Error.__init__(
                self,
                f"Unexpected token {actual_token} at position {pos}. Invalid sentence {w}. {message}. Secuencia de derivaciones: {output}. Operaciones: {operations}",
            )


class non_regular_production_error(Error):
    def __init__(self, production):
        Error.__init__(
            self,
            f"production {production} most be of the form: A -> a, A -> e or A -> aX",
        )
