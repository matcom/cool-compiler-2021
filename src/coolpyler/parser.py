from sly import Parser
from coolpyler.lexer import CoolLexer


# pyright: reportUndefinedVariable=false
# flake8: noqa


class CoolParser(Parser):
    tokens = CoolLexer.tokens

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

    @_("OBJECT_ID OPAR [ param { COMMA param } ] CPAR COLON TYPE_ID OCURLY expr CCURLY")
    def feature(self, p):
        # func_decl
        pass

    @_("OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ]")
    def feature(self, p):
        # attr_decl
        pass

    @_("OBJECT_ID COLON TYPE_ID")
    def param(self, p):
        # param
        pass

    @_("OBJECT_ID LEFT_ARROW expr")
    def expr(self, p):
        # assign
        pass

    @_("not_")
    def expr(self, p):
        pass

    @_("NOT not_")
    def not_(self, p):
        # not_
        pass

    @_("comparison")
    def not_(self, p):
        pass

    @_("comparison LEQ arithmetic")
    def comparison(self, p):
        # comparison_leq
        pass

    @_("comparison LE arithmetic")
    def comparison(self, p):
        # comparison_le
        pass

    @_("comparison EQ arithmetic")
    def comparison(self, p):
        # comparison_eq
        pass

    @_("arithmetic")
    def comparison(self, p):
        pass

    @_("arithmetic PLUS term")
    def arithmetic(self, p):
        # arithmetic_add
        pass

    @_("arithmetic MINUS term")
    def arithmetic(self, p):
        # arithmetic_sub
        pass

    @_("term")
    def arithmetic(self, p):
        pass

    @_("term STAR factor")
    def term(self, p):
        # term_mul
        pass

    @_("term SLASH factor")
    def term(self, p):
        # term_div
        pass

    @_("factor")
    def term(self, p):
        pass

    @_("ISVOID factor")
    def factor(self, p):
        # isvoid_expr
        pass

    @_("tilde")
    def factor(self, p):
        pass

    @_("TILDE tilde")
    def tilde(self, p):
        # tilde_expr
        pass

    @_("dispatch")
    def tilde(self, p):
        pass

    @_("[ dispatch DOT ] OBJECT_ID OPAR [ expr { COMMA expr } ] CPAR")
    def dispatch(self, p):
        # dispatch
        pass

    @_("static_dispatch")
    def dispatch(self, p):
        pass

    @_("static_dispatch AT TYPE_ID DOT OBJECT_ID OPAR [ expr { COMMA expr } ] CPAR")
    def static_dispatch(self, p):
        # static_dispatch
        pass

    @_("atom")
    def static_dispatch(self, p):
        pass

    @_("IF expr THEN expr ELSE expr FI")
    def atom(self, p):
        # if_expr
        pass

    @_("WHILE expr LOOP expr POOL")
    def atom(self, p):
        # while_expr
        pass

    @_(
        "LET OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ] "
        + "{ COMMA OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ] } IN expr"
    )
    def atom(self, p):
        # let_expr
        pass

    @_(
        "CASE expr OF OBJECT_ID COLON TYPE_ID RIGHT_ARROW expr SEMICOLON "
        + "{ OBJECT_ID COLON TYPE_ID RIGHT_ARROW expr SEMICOLON } ESAC"
    )
    def atom(self, p):
        # case_expr
        pass

    @_("OCURLY expr SEMICOLON { expr SEMICOLON } CCURLY")
    def atom(self, p):
        # block_expr
        pass

    @_("NEW TYPE_ID")
    def atom(self, p):
        # new_expr
        pass

    @_("OPAR expr CPAR")
    def atom(self, p):
        # parenthized_expr
        pass

    @_("OBJECT_ID")
    def atom(self, p):
        # var_expr
        pass

    @_("constant")
    def atom(self, p):
        pass

    @_("INT")
    def constant(self, p):
        # integer_atom
        pass

    @_("STRING")
    def constant(self, p):
        # string_atom
        pass

    @_("TRUE")
    def constant(self, p):
        # bool_atom
        pass

    @_("FALSE")
    def constant(self, p):
        # bool_atom
        pass
