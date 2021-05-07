from .expr_nodes import ExpressionNode

class BinaryOpNode(ExpressionNode):
    def __init__(self):
        super(BinaryOpNode, self).__init__()
        pass

class UnaryOpNode(ExpressionNode):
    def __init__(self):
        super(UnaryOpNode, self).__init__()
        pass

class ArithBinOpNode(BinaryOpNode):
    def __init__(self):
        super(ArithBinOpNode, self).__init__()
        pass

class LogicBinOpNode(BinaryOpNode):
    def __init__(self):
        super(LogicBinOpNode, self).__init__()
        pass

class NotNode(UnaryOpNode):
    def __init__(self, expression, row, col):
        super(NotNode, self).__init__()
        self.expression = expression
        self.row = row
        self.col = col

class LogicNotNode(UnaryOpNode):
    def __init__(self, expression, row, col):
        super(LogicNotNode, self).__init__()
        self.expression = expression
        self.row = row
        self.col = col

class SumNode(ArithBinOpNode):
    def __init__(self, left, right, row, col):
        super(SumNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class SubNode(ArithBinOpNode):
    def __init__(self, left, right, row, col):
        super(SubNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class MultNode(ArithBinOpNode):
    def __init__(self, left, right, row, col):
        super(MultNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class DivNode(ArithBinOpNode):
    def __init__(self, left, right, row, col):
        super(DivNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class LessNode(LogicBinOpNode):
    def __init__(self, left, right, row, col):
        super(LessNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class LessEqualNode(LogicBinOpNode):
    def __init__(self, left, right, row, col):
        super(LessEqualNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col
