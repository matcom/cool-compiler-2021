from .ast_nodes import AST

class ExpressionNode(AST):
    def __init__(self):
        super(ExpressionNode, self).__init__()
        self.expr_type = None

class DynamicCallNode(ExpressionNode):
    def __init__(self, obj, method, args, row , col):
        super(DynamicCallNode, self).__init__()
        self.obj = obj
        self.method = method
        self.args = args
        self.row = row
        self.col = col

class StaticCallNode(ExpressionNode):
    def __init__(self, obj, static_type, method, args, row, col):
        super(StaticCallNode, self).__init__()
        self.obj = obj
        self.static_type = static_type
        self.method = method
        self.args = args
        self.row = row
        self.col = col

class AssignNode(ExpressionNode):
    def __init__(self, name, expression, row, col):
        super(AssignNode, self).__init__()
        self.name = name
        self.expression = expression
        self.row = row
        self.col = col

class IfNode(ExpressionNode):
    def __init__(self, predicate, then_expr, else_expr, row, col):
        super(IfNode, self).__init__()
        self.predicate = predicate
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.row = row
        self.col = col

class WhileNode(ExpressionNode):
    def __init__(self, predicate, expression, row, col):
        super(WhileNode, self).__init__()
        self.predicate = predicate
        self.expression = expression
        self.row = row
        self.col = col

class BlockNode(ExpressionNode):
    def __init__(self, expr_list, row , col):
        super(BlockNode, self).__init__()
        self.expr_list = expr_list

class LetNode(ExpressionNode):
    def __init__(self, init_list, body, row, col):
        super(LetNode, self).__init__()
        self.init_list = init_list
        self.body = body
        self.row = row
        self.col = col

class CaseNode(ExpressionNode):
    def __init__(self, expression, act_list, row, col):
        super(CaseNode, self).__init__()
        self.expression = expression
        self.act_list = act_list
        self.row = row
        self.col = col

class NewNode(ExpressionNode):
    def __init__(self, new_type, row, col):
        super(NewNode, self).__init__()
        self.new_type = new_type
        self.row = row
        self.col = col

class IsVoidNode(ExpressionNode):
    def __init__(self, expression, row, col):
        super(IsVoidNode, self).__init__()
        self.expression = expression
        self.row = row
        self.col = col

class IdNode(ExpressionNode):
    def __init__(self, name, row, col):
        super(IdNode, self).__init__()
        self.name = name

class EqualsNode(ExpressionNode):
    def __init__(self, left, right, row, col):
        super(EqualsNode, self).__init__()
        self.left = left
        self.right = right
        self.row = row
        self.col = col

class IntegerNode(ExpressionNode):
    def __init__(self, value, row, col):
        super(IntegerNode, self).__init__()
        self.value = value
        self.row = row
        self.col = col

class StringNode(ExpressionNode):
    def __init__(self, value, row, col):
        super(StringNode, self).__init__()
        self.value = value
        self.row = row
        self.col = col

class BooleanNode(ExpressionNode):
    def __init__(self, value, row, col):
        super(BooleanNode, self).__init__()
        self.value = value
        self.row = row
        self.col = col
