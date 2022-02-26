from .expressions import BinaryExprNode


class ArithmeticNode(BinaryExprNode):
    pass


class PlusNode(ArithmeticNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return PlusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class MinusNode(ArithmeticNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return MinusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class MultNode(ArithmeticNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return MultNode(p.lineno, p[0].columnno, left_expr, right_expr)


class DivNode(ArithmeticNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return DivNode(p.lineno, p[0].columnno, left_expr, right_expr)
