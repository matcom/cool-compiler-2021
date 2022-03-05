from sly import Parser
from coolpyler.lexer.main import CoolLexer
from coolpyler.errors import UnexpectedEOFError, UnexpectedTokenError
from coolpyler.ast_nodes.main import (
    CoolAssignNode,
    CoolAttrDeclNode,
    CoolBlockNode,
    CoolBoolNode,
    CoolCaseBranchNode,
    CoolCaseNode,
    CoolClassNode,
    CoolDispatchNode,
    CoolEqNode,
    CoolMethodDeclNode,
    CoolIfThenElseNode,
    CoolIntNode,
    CoolIsVoidNode,
    CoolLeNode,
    CoolLeqNode,
    CoolLetDeclNode,
    CoolLetInNode,
    CoolMinusNode,
    CoolDivNode,
    CoolMultNode,
    CoolPlusNode,
    CoolNewNode,
    CoolNotNode,
    CoolParenthNode,
    CoolProgramNode,
    CoolStaticDispatchNode,
    CoolStringNode,
    CoolTildeNode,
    CoolVarNode,
    CoolWhileNode,
)

# pyright: reportUndefinedVariable=false
# flake8: noqa

DEBUG = True


class CoolParser(Parser):
    debugfile = "parser.out" if DEBUG else None

    tokens = CoolLexer.tokens - {"OPEN_BLOCK_COMMENT"}

    precedence = (
        ("right", "ASSIGN"),
        ("right", "NOT"),
        ("nonassoc", "LEQ", "LE", "EQ"),
        ("left", "TIMES", "DIV"),
        ("left", "PLUS", "MINUS"),
        ("right", "ISVOID"),
        ("right", "TILDE"),
        ("left", "AT"),
        ("left", "DOT"),
    )

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

    @_("cool_class SEMICOLON { cool_class SEMICOLON }")
    def program(self, p):
        # print(p.cool_class1)
        return CoolProgramNode.parse(p)

    @_("CLASS TYPE_ID [ INHERITS TYPE_ID ] OPEN_CURLY { feature SEMICOLON } CLOSED_CURLY")
    def cool_class(self, p):
        # print(p.lineno, p.index)
        return CoolClassNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID [ ASSIGN expr ]")
    def feature(self, p):
        return CoolAttrDeclNode.parse(p)

    @_("OBJECT_ID OPEN_PARENTHESIS [ formal_list ] CLOSED_PARENTHESIS COLON TYPE_ID OPEN_CURLY expr CLOSED_CURLY")
    def feature(self, p):
        return CoolMethodDeclNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID { COMMA OBJECT_ID COLON TYPE_ID }")
    def formal_list(self, p):
        return [p.OBJECT_ID0, * p.OBJECT_ID1], [p.TYPE_ID0, * p.TYPE_ID1]

    @_("OBJECT_ID ASSIGN expr")
    def expr(self, p):
        return CoolAssignNode.parse(p)

    @_("expr AT TYPE_ID DOT OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        return CoolStaticDispatchNode.parse(p)

    @_("expr DOT OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        return CoolDispatchNode.parse(p, expr=p.expr)

    @_("OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        # print("Dispatch", p.lineno, p.index)
        return CoolDispatchNode.parse(p, expr=CoolVarNode(p.lineno, 0, "self"))

    @_("expr { COMMA expr }")
    def arg_list(self, p):
        return [p.expr0, * p.expr1]

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        return CoolIfThenElseNode.parse(p)

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        return CoolWhileNode.parse(p)

    @_("OPEN_CURLY expr SEMICOLON { expr SEMICOLON } CLOSED_CURLY")
    def expr(self, p):
        return CoolBlockNode.parse(p)

    @_("LET let_decl { COMMA let_decl } IN expr")
    def expr(self, p):
        return CoolLetInNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID [ ASSIGN expr ]")
    def let_decl(self, p):
        return CoolLetDeclNode.parse(p)

    @_("CASE expr OF case SEMICOLON { case SEMICOLON } ESAC")
    def expr(self, p):
        return CoolCaseNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID ARROW expr")
    def case(self, p):
        return CoolCaseBranchNode.parse(p)

    @_("NEW TYPE_ID")
    def expr(self, p):
        return CoolNewNode.parse(p)

    @_("OPEN_PARENTHESIS expr CLOSED_PARENTHESIS")
    def expr(self, p):
        return CoolParenthNode.parse(p)

    @_("ISVOID expr")
    def expr(self, p):
        return CoolIsVoidNode.parse(p)

    @_("TILDE expr")
    def expr(self, p):
        return CoolTildeNode.parse(p)

    @_("NOT expr")
    def expr(self, p):
        return CoolNotNode.parse(p)

    @_("expr PLUS expr")
    def expr(self, p):
        return CoolPlusNode.parse(p)

    @_("expr MINUS expr")
    def expr(self, p):
        return CoolMinusNode.parse(p)

    @_("expr TIMES expr")
    def expr(self, p):
        return CoolMultNode.parse(p)

    @_("expr DIV expr")
    def expr(self, p):
        return CoolDivNode.parse(p)

    @_("expr LE expr")
    def expr(self, p):
        return CoolLeNode.parse(p)

    @_("expr LEQ expr")
    def expr(self, p):
        return CoolLeqNode.parse(p)

    @_("expr EQ expr")
    def expr(self, p):
        return CoolEqNode.parse(p)

    @_("OBJECT_ID")
    def expr(self, p):
        # print('OBJECT_ID', p.lineno, p.index)
        return CoolVarNode.parse(p)

    @_("INT")
    def expr(self, p):
        # print("Int", p.lineno, p.index)
        return CoolIntNode.parse(p)

    @_("QUOTE")
    def expr(self, p):
        return CoolStringNode.parse(p)

    @_("TRUE")
    def expr(self, p):
        # print("TRUE", p.lineno, p.index)
        return CoolBoolNode.parse(p, p.TRUE)

    @_("FALSE")
    def expr(self, p):
        # print("False", p.lineno, p.index)
        return CoolBoolNode.parse(p, p.FALSE)

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
