import os
from sly import Parser
from coolpyler.lexer import CoolLexer
from coolpyler.errors import UnexpectedEOFError, UnexpectedTokenError
from coolpyler.ast.cool.basic import (
    CoolAssignNode,
    CoolAttrDeclNode,
    CoolBlockNode,
    CoolBoolNode,
    CoolCaseNode,
    CoolCaseOfNode,
    CoolClassNode,
    CoolDispatchNode,
    CoolDivNode,
    CoolEqNode,
    CoolFormalNode,
    CoolFuncDeclNode,
    CoolIfThenElseNode,
    CoolIntNode,
    CoolIsVoidNode,
    CoolLeNode,
    CoolLeqNode,
    CoolLetDeclNode,
    CoolLetInNode,
    CoolMinusNode,
    CoolMultNode,
    CoolNewNode,
    CoolNotNode,
    CoolParenthNode,
    CoolPlusNode,
    CoolProgramNode,
    CoolStaticDispatchNode,
    CoolStringNode,
    CoolTildeNode,
    CoolVarNode,
    CoolWhileNode,
)

# pyright: reportUndefinedVariable=false
# flake8: noqa

DEBUG = False


class CoolLogger(object):
    def __init__(self, f=None):
        if f is None:
            f = open(os.devnull, "w")
        self.f = open(f, "w") if isinstance(f, str) else f

    def debug(self, msg, *args, **kwargs):
        self.f.write((msg % args) + "\n")

    info = debug

    def warning(self, msg, *args, **kwargs):
        self.f.write("WARNING: " + (msg % args) + "\n")

    def error(self, msg, *args, **kwargs):
        self.f.write("ERROR: " + (msg % args) + "\n")

    critical = debug


class CoolParser(Parser):
    log = CoolLogger("parser.log" if DEBUG else None)
    debugfile = "parser.out" if DEBUG else None

    tokens = CoolLexer.tokens - {"INLINE_COMMENT", "OCOMMENT"}

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
        # ("right", "IN"),
    )

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

    @_("cool_class SEMICOLON { cool_class SEMICOLON }")
    def program(self, p):
        classes = [p.cool_class0] + p.cool_class1
        return CoolProgramNode(classes)

    @_("CLASS TYPE_ID [ INHERITS TYPE_ID ] OCURLY { feature SEMICOLON } CCURLY")
    def cool_class(self, p):
        name, parent, features = p.TYPE_ID0, p.TYPE_ID1, p.feature
        return CoolClassNode(name, features, parent=parent)

    @_("OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ]")
    def feature(self, p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CoolAttrDeclNode(id, type, expr)

    @_("OBJECT_ID OPAR [ formal_list ] CPAR COLON TYPE_ID OCURLY expr CCURLY")
    def feature(self, p):
        id = p.OBJECT_ID
        params = p.formal_list if p.formal_list is not None else []
        type, body = p.TYPE_ID, p.expr
        return CoolFuncDeclNode(id, params, type, body)

    @_("formal { COMMA formal }")
    def formal_list(self, p):
        return [p.formal0] + p.formal1

    @_("OBJECT_ID COLON TYPE_ID")
    def formal(self, p):
        id, type = p.OBJECT_ID, p.TYPE_ID
        return CoolFormalNode(id, type)

    @_("OBJECT_ID LEFT_ARROW expr")
    def expr(self, p):
        id, expr = p.OBJECT_ID, p.expr
        return CoolAssignNode(id, expr)

    @_("expr AT TYPE_ID DOT OBJECT_ID OPAR [ arg_list ] CPAR")
    def expr(self, p):
        expr, type, id = p.expr, p.TYPE_ID, p.OBJECT_ID
        args = p.arg_list if p.arg_list is not None else []
        return CoolStaticDispatchNode(expr, type, id, args)

    @_("expr DOT OBJECT_ID OPAR [ arg_list ] CPAR")
    def expr(self, p):
        expr, id = p.expr, p.OBJECT_ID
        args = p.arg_list if p.arg_list is not None else []
        return CoolDispatchNode(id, args, expr=expr)

    @_("OBJECT_ID OPAR [ arg_list ] CPAR")
    def expr(self, p):
        id = p.OBJECT_ID
        args = p.arg_list if p.arg_list is not None else []
        return CoolDispatchNode(id, args)

    @_("expr { COMMA expr }")
    def arg_list(self, p):
        return [p.expr0] + p.expr1

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        cond, then_expr, else_expr = p.expr0, p.expr1, p.expr2
        return CoolIfThenElseNode(cond, then_expr, else_expr)

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        cond, body = p.expr0, p.expr1
        return CoolWhileNode(cond, body)

    @_("OCURLY expr SEMICOLON { expr SEMICOLON } CCURLY")
    def expr(self, p):
        expr_list = [p.expr0] + p.expr1
        return CoolBlockNode(expr_list)

    @_("LET let_decl { COMMA let_decl } IN expr")
    def expr(self, p):
        decl_list = [p.let_decl0] + p.let_decl1
        expr = p.expr
        return CoolLetInNode(decl_list, expr)

    @_("OBJECT_ID COLON TYPE_ID [ LEFT_ARROW expr ]")
    def let_decl(self, p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CoolLetDeclNode(id, type, expr=expr)

    @_("CASE expr OF case SEMICOLON { case SEMICOLON } ESAC")
    def expr(self, p):
        expr = p.expr
        case_list = [p.case0] + p.case1
        return CoolCaseOfNode(expr, case_list)

    @_("OBJECT_ID COLON TYPE_ID RIGHT_ARROW expr")
    def case(self, p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CoolCaseNode(id, type, expr)

    @_("NEW TYPE_ID")
    def expr(self, p):
        type = p.TYPE_ID
        return CoolNewNode(type)

    @_("OPAR expr CPAR")
    def expr(self, p):
        expr = p.expr
        return CoolParenthNode(expr)

    @_("ISVOID expr")
    def expr(self, p):
        expr = p.expr
        return CoolIsVoidNode(expr)

    @_("TILDE expr")
    def expr(self, p):
        expr = p.expr
        return CoolTildeNode(expr)

    @_("NOT expr")
    def expr(self, p):
        expr = p.expr
        return CoolNotNode(expr)

    @_("expr PLUS expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolPlusNode(left_expr, right_expr)

    @_("expr MINUS expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolMinusNode(left_expr, right_expr)

    @_("expr STAR expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolMultNode(left_expr, right_expr)

    @_("expr SLASH expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolDivNode(left_expr, right_expr)

    @_("expr LE expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolLeNode(left_expr, right_expr)

    @_("expr LEQ expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolLeqNode(left_expr, right_expr)

    @_("expr EQ expr")
    def expr(self, p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolEqNode(left_expr, right_expr)

    @_("OBJECT_ID")
    def expr(self, p):
        return CoolVarNode(p.OBJECT_ID)

    @_("INT")
    def expr(self, p):
        value = p.INT
        return CoolIntNode(value)

    @_("STRING")
    def expr(self, p):
        value = p.STRING
        return CoolStringNode(value)

    @_("TRUE")
    def expr(self, p):
        value = p.TRUE
        return CoolBoolNode(value)

    @_("FALSE")
    def expr(self, p):
        value = p.FALSE
        return CoolBoolNode(value)

    # error rules
    # TODO: parser recovery and resynchronization with error rules

    def error(self, token):
        if token is None:
            self.errors.append(UnexpectedEOFError())
        else:
            self.errors.append(
                UnexpectedTokenError(
                    token.lineno, token.columnno, f"({token.type}, {token.value})>"
                )
            )
