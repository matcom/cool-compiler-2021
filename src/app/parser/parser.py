from sly import Parser
from app.lexer.main import CoolLexer
from app.parser.errors import ParsingError
from .ast import *


# pyright: reportUndefinedVariable=false


class CoolParser(Parser):

    tokens = CoolLexer.tokens - {"OPEN_BLOCK_COMMENT"}

    precedence = (
        ("right", "ASSIGN"),
        ("right", "NOT"),
        ("nonassoc", "LEQ", "LE", "EQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIV"),
        ("right", "ISVOID"),
        ("right", "TILDE"),
        ("left", "AT"),
        ("left", "DOT"),
    )

    def error(self, token):
        if token is None:
            self.errors.append(ParsingError.UnexpectedEof(0, 0))
        else:
            self.errors.append(
                ParsingError.UnexpectedToken(
                    token.lineno, token.columnno, f"({token.type}, {token.value})>"
                )
            )

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

    @_("_class SEMICOLON { _class SEMICOLON }")
    def program(self, p):
        return ProgramNode.parse(p)

    @_("CLASS TYPE_ID [ INHERITS TYPE_ID ] OPEN_CURLY { feature SEMICOLON } CLOSED_CURLY")
    def _class(self, p):
        return ClassNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID [ ASSIGN expr ]")
    def feature(self, p):
        return AttrDeclNode.parse(p)

    @_("OBJECT_ID OPEN_PARENTHESIS [ formal_list ] CLOSED_PARENTHESIS COLON TYPE_ID OPEN_CURLY expr CLOSED_CURLY")
    def feature(self, p):
        return MethodDeclNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID { COMMA OBJECT_ID COLON TYPE_ID }")
    def formal_list(self, p):
        return [p.OBJECT_ID0, * p.OBJECT_ID1], [p.TYPE_ID0, * p.TYPE_ID1]

    @_("OBJECT_ID ASSIGN expr")
    def expr(self, p):
        return AssignNode.parse(p)

    @_("expr AT TYPE_ID DOT OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        return StaticDispatchNode.parse(p)

    @_("expr DOT OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        return DispatchNode.parse(p, expr=p.expr)

    @_("OBJECT_ID OPEN_PARENTHESIS [ arg_list ] CLOSED_PARENTHESIS")
    def expr(self, p):
        return DispatchNode.parse(p, expr=VarNode(p.lineno, 0, "self"))

    @_("expr { COMMA expr }")
    def arg_list(self, p):
        return [p.expr0, * p.expr1]

    @_("IF expr THEN expr ELSE expr FI")
    def expr(self, p):
        return IfThenElseNode.parse(p)

    @_("WHILE expr LOOP expr POOL")
    def expr(self, p):
        return WhileNode.parse(p)

    @_("OPEN_CURLY expr SEMICOLON { expr SEMICOLON } CLOSED_CURLY")
    def expr(self, p):
        return BlockNode.parse(p)

    @_("LET let_decl { COMMA let_decl } IN expr")
    def expr(self, p):
        return LetInNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID [ ASSIGN expr ]")
    def let_decl(self, p):
        return LetDeclNode.parse(p)

    @_("CASE expr OF case SEMICOLON { case SEMICOLON } ESAC")
    def expr(self, p):
        return CaseNode.parse(p)

    @_("OBJECT_ID COLON TYPE_ID ARROW expr")
    def case(self, p):
        return CaseBranchNode.parse(p)

    @_("NEW TYPE_ID")
    def expr(self, p):
        return NewNode.parse(p)

    @_("OPEN_PARENTHESIS expr CLOSED_PARENTHESIS")
    def expr(self, p):
        return ParenthNode.parse(p)

    @_("ISVOID expr")
    def expr(self, p):
        return IsVoidNode.parse(p)

    @_("TILDE expr")
    def expr(self, p):
        return TildeNode.parse(p)

    @_("NOT expr")
    def expr(self, p):
        return NotNode.parse(p)

    @_("expr PLUS expr")
    def expr(self, p):
        return PlusNode.parse(p)

    @_("expr MINUS expr")
    def expr(self, p):
        return MinusNode.parse(p)

    @_("expr TIMES expr")
    def expr(self, p):
        return MultNode.parse(p)

    @_("expr DIV expr")
    def expr(self, p):
        return DivNode.parse(p)

    @_("expr LE expr")
    def expr(self, p):
        return LeNode.parse(p)

    @_("expr LEQ expr")
    def expr(self, p):
        return LeqNode.parse(p)

    @_("expr EQ expr")
    def expr(self, p):
        return EqNode.parse(p)

    @_("OBJECT_ID")
    def expr(self, p):
        return VarNode.parse(p)

    @_("INT")
    def expr(self, p):
        return IntNode.parse(p)

    @_("QUOTE")
    def expr(self, p):
        return StringNode.parse(p)

    @_("TRUE")
    def expr(self, p):
        return BoolNode.parse(p, p.TRUE)

    @_("FALSE")
    def expr(self, p):
        return BoolNode.parse(p, p.FALSE)
