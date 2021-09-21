
class Node:
    def __init__(self,row=None,column=None):
        self.row = row
        self.column = column

class ProgramNode(Node):
    def __init__(self, declarations,row=None,column=None):
        super().__init__(row,column)
        self.declarations = declarations
    
    def __iter__(self):
        for x in self.declarations:
            yield from x

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.parent = parent[0] if parent else 'Object'
        self.parent_row = parent[1] if parent else -1
        self.parent_column = parent[2] if parent else -1
        self.features = features
    
    def __iter__(self):
        yield self
        for x in self.features:
            yield from x

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.params = params
        self.type = return_type[0]
        self.type_row = return_type[1]
        self.type_column = return_type[2]
        self.body = body
    
    def __iter__(self):
        yield self
        yield from self.params
        yield from self.body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class ParamNode(DeclarationNode):
    def __init__(self, idx, typex, row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex

    def __iter__(self):
        yield self

class SpecialNode(ExpressionNode):
    def __init__(self, func,row=None,column=None):
        super().__init__(row,column)
        self.func = func

    def __iter__(self):
        yield self

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args,at_type,row=None,column=None):
        super().__init__(row,column)
        self.obj = obj
        self.id = idx
        self.args = args
        self.at = at_type

    def __iter__(self):
        yield from self.obj
        for x in self.args:
            yield from x
        yield self

class BlockNode(ExpressionNode):
    def __init__(self, expr_list,row=None,column=None):
        super().__init__(row,column)
        self.expr_list = expr_list

    def __iter__(self):
        yield self
        for x in self.expr_list:
            yield from x

class ConditionalNode(ExpressionNode):
    def __init__(self, condition,then_expr,else_expr,row=None,column=None):
        super().__init__(row,column)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def get_return_type(self,current_type):
        else_type = self.else_expr.type
        then_type = self.then_expr.type
        return else_type.join(then_type,current_type)

    def __iter__(self):
        yield self
        for x in [self.condition,self.then_expr,self.else_expr]:
            yield from x

class CheckNode(ExpressionNode):
    def __init__(self, idx, typex, expr,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        yield from self.expr

class LetNode(ExpressionNode):
    def __init__(self, dec_var_list, expr,row=None,column=None):
        super().__init__(row,column)
        self.params = dec_var_list
        self.expr = expr

    def __iter__(self):
        yield self
        for x in self.params:
            yield from x


class CaseNode(ExpressionNode):
    def __init__(self, expr, check_list,row=None,column=None):
        super().__init__(row,column)
        self.expr = expr
        self.params = check_list

    def __iter__(self):
        yield self
        yield from expr
        for x in self.params:
            yield from x

class WhileNode(ExpressionNode):
    def __init__(self, condition, expr,row=None,column=None):
        super().__init__(row,column)
        self.condition = condition
        self.expr = expr

    def __iter__(self):
        yield self
        yield from expr
        for x in self.params:
            yield from x

class AtomicNode(ExpressionNode):
    def __init__(self, lex,row=None,column=None):
        super().__init__(row,column)
        self.lex = lex

    def __iter__(self):
        yield self

class UnaryNode(ExpressionNode):
    def __init__(self, member,row=None,column=None):
        super().__init__(row,column)
        self.member = member

    def __iter__(self):
        yield self
        yield self.member

class BinaryNode(ExpressionNode):
    def __init__(self, left, right,row=None,column=None):
        super().__init__(row,column)
        self.left = left
        self.right = right

    def __iter__(self):
        yield self
        yield self.left
        yield self.right

class StringNode(AtomicNode):
    pass

class BoolNode(AtomicNode):
    pass
        
class ConstantNumNode(AtomicNode):
    pass

class VoidNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class InstantiateNode(AtomicNode):
    
    def __init__(self, type, row=None,column=None):
        super().__init__(type[0], row, column)
        self.type_row = type[1]
        self.type_column = type[2]

class NotNode(UnaryNode):
    pass

class RoofNode(UnaryNode):
    pass

class IsVoidNode(UnaryNode):
    pass

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class GreaterNode(BinaryNode):
    pass

class GreaterEqualNode(BinaryNode):
    pass

class LesserNode(BinaryNode):
    pass

class LesserEqualNode(BinaryNode):
    pass