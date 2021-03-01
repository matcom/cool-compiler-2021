from sly import Parser
from coolpyler.lexer import CoolLexer


# pyright: reportUndefinedVariable=false
# flake8: noqa


class CoolParser(Parser):
    debugfile = "./parser.out"
    tokens = CoolLexer.tokens

    precedence = (
        ("left", "DOT"),
        ("left", "AT"),
        ("right", "TILDE"),
        ("right", "ISVOID"),
        ("left", "STAR", "SLASH"),
        ("left", "PLUS", "MINUS"),
        ("nonassoc", "LEQ", "LE", "EQ"),
        ("right", "NOT"),
        ("right", "LEFT_ARROW"),
    )

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

    @_("class_ SEMICOLON { class_ SEMICOLON }")
    def program(self, p):
        # program
        pass

    @_("CLASS TYPE_ID [ INHERITS TYPE_ID ] OCURLY { feature SEMICOLON } CCURLY")
    def class_(self, p):
        # class_
        pass

    @_(
        "OBJECT_ID OPAR [ formal { COMMA formal } ] CPAR COLON TYPE_ID OCURLY expr CCURLY"
    )
    def feature(self, p):
        # func_decl
        pass

    @_("OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ]")
    def feature(self, p):
        # attr_decl
        pass

    @_("OBJECT_ID COLON TYPE_ID")
    def formal(self, p):
        # param
        pass

    @_("OBJECT_ID LEFT_ARROW expr")
    def expr(self, p):
        # assign
        pass

    @_("expr AT TYPE_ID DOT OBJECT_ID OPAR [ expr { COMMA expr } ] CPAR")
    def expr(self, p):
        # static_dispatch
        pass

    @_("expr DOT OBJECT_ID OPAR [ expr { COMMA expr } ] CPAR")
    def expr(self, p):
        # dispatch
        pass

    @_("OBJECT_ID OPAR [ expr { COMMA expr } ] CPAR")
    def expr(self, p):
        # dispatch
        pass

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        # if_expr
        pass

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        # while_expr
        pass

    @_("OCURLY expr SEMICOLON { expr SEMICOLON } CCURLY")
    def expr(self, p):
        # block_expr
        pass

    @_(
        "LET OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ] "
        + "{ COMMA OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ] } IN expr"
    )
    def expr(self, p):
        # let_expr
        pass

    @_(
        "CASE expr OF OBJECT_ID COLON TYPE_ID RIGHT_ARROW expr SEMICOLON "
        + "{ OBJECT_ID COLON TYPE_ID RIGHT_ARROW expr SEMICOLON } ESAC"
    )
    def expr(self, p):
        # case_expr
        pass

    @_("NEW TYPE_ID")
    def expr(self, p):
        # new_expr
        pass

    @_("ISVOID expr")
    def expr(self, p):
        # isvoid_expr
        pass

    @_("expr PLUS expr")
    def expr(self, p):
        # arithmetic_add
        pass

    @_("expr MINUS expr")
    def expr(self, p):
        # arithmetic_sub
        pass

    @_("expr STAR expr")
    def expr(self, p):
        # term_mul
        pass

    @_("expr SLASH expr")
    def expr(self, p):
        # term_div
        pass

    @_("TILDE expr")
    def expr(self, p):
        # tilde_expr
        pass

    @_("expr LE expr")
    def expr(self, p):
        # comparison_le
        pass

    @_("expr LEQ expr")
    def expr(self, p):
        # comparison_leq
        pass

    @_("expr EQ expr")
    def expr(self, p):
        # comparison_eq
        pass

    @_("NOT expr")
    def expr(self, p):
        # not_
        pass

    @_("OPAR expr CPAR")
    def expr(self, p):
        # parenthized_expr
        pass

    @_("OBJECT_ID")
    def expr(self, p):
        # var_expr
        pass

    @_("INT")
    def expr(self, p):
        # integer_atom
        pass

    @_("STRING")
    def expr(self, p):
        # string_atom
        pass

    @_("TRUE")
    def expr(self, p):
        # bool_atom
        pass

    @_("FALSE")
    def expr(self, p):
        # bool_atom
        pass
