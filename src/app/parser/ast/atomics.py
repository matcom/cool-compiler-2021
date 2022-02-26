from .base import ExprNode


class AtomNode(ExprNode):
    def __init__(self, lineno, columnno, value):
        super().__init__(lineno, columnno)

        self.value = value


class IntNode(AtomNode):
    @staticmethod
    def parse(p):
        value = p.INT
        return IntNode(p.lineno, p._slice[0].columnno, value)


class StringNode(AtomNode):
    @staticmethod
    def parse(p):
        value = p.QUOTE
        return StringNode(p.lineno, p._slice[0].columnno, value)


class BoolNode(AtomNode):
    @staticmethod
    def parse(p, value):
        return BoolNode(p.lineno, p._slice[0].columnno, value)


class VarNode(AtomNode):
    @staticmethod
    def parse(p):
        return VarNode(p.lineno, p._slice[0].columnno, p.OBJECT_ID)
