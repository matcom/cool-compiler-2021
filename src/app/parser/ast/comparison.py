from .expressions import BinaryExprNode


class ComparisonNode(BinaryExprNode):
    pass


class LeqNode(ComparisonNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return LeqNode(p.lineno, p[0].columnno, left_expr, right_expr)


class EqNode(ComparisonNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return EqNode(p.lineno, p[0].columnno, left_expr, right_expr)


class LeNode(ComparisonNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return LeNode(p.lineno, p[0].columnno, left_expr, right_expr)
