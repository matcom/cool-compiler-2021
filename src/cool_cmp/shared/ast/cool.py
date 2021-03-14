"""
Cool AST nodes
"""
from cool_cmp.shared.ast import Node
from typing import List


class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, features:List[DeclarationNode], parent=None,row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.parent = parent if parent else 'Object'
        self.features = features
    
    def __iter__(self):
        yield self
        for x in self.features:
            yield from x

class ProgramNode(Node):
    def __init__(self, declarations:List[ClassDeclarationNode],row:int=None,column:int=None):
        super().__init__(row,column)
        self.declarations = declarations
    
    def __iter__(self):
        for x in self.declarations:
            yield from x


class ParamNode(DeclarationNode):
    def __init__(self, idx:str, typex:str, row:int=None,column:int=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex

    def __iter__(self):
        yield self

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx:int, params:List[ParamNode], return_type:str, body:ExpressionNode, row:int=None,column:int=None):
        super().__init__(row,column)
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
    
    def __iter__(self):
        yield self
        yield from self.params
        yield from self.body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx:str, typex:str, expr:ExpressionNode=None,row:int=None,column:int=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class SpecialNode(ExpressionNode):
    def __init__(self, func,row=None,column=None):
        super().__init__(row,column)
        self.func = func

    def __iter__(self):
        yield self

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx:str, typex:str, expr:ExpressionNode, row=None, column=None):
        super().__init__(row, column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class AssignNode(ExpressionNode):
    def __init__(self, idx:str, expr:ExpressionNode, row=None,column=None):
        super().__init__(row,column)
        self.id = idx
        self.expr = expr

    def __iter__(self):
        yield self
        if self.expr:
            yield from self.expr

class CallNode(ExpressionNode):
    def __init__(self, obj:ExpressionNode, idx:str, args:List[ExpressionNode], at_type:str, row:int = None, column:int = None):
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
    def __init__(self, expr_list:List[ExpressionNode],row=None,column=None):
        super().__init__(row,column)
        self.expr_list = expr_list

    def __iter__(self):
        yield self
        for x in self.expr_list:
            yield from x

class ConditionalNode(ExpressionNode):
    def __init__(self, condition:ExpressionNode, then_expr:ExpressionNode, else_expr:ExpressionNode, row:int=None,column:int=None):
        super().__init__(row,column)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def __iter__(self):
        yield self
        for x in [self.condition, self.then_expr, self.else_expr]:
            yield from x

class CheckNode(ExpressionNode):
    def __init__(self, idx:str, typex:str, expr:ExpressionNode, row:int=None, column:int=None):
        super().__init__(row,column)
        self.id = idx
        self.type = typex
        self.expr = expr

    def __iter__(self):
        yield self
        yield from self.expr

class LetNode(ExpressionNode):
    def __init__(self, dec_var_list:List[VarDeclarationNode], expr:ExpressionNode, row:int=None,column:int=None):
        super().__init__(row,column)
        self.params = dec_var_list
        self.expr = expr

    def __iter__(self):
        yield self
        for x in self.params:
            yield from x


class CaseNode(ExpressionNode):
    def __init__(self, expr:ExpressionNode, check_list:List[CheckNode], row:int=None,column:int=None):
        super().__init__(row,column)
        self.expr = expr
        self.params = check_list

    def __iter__(self):
        yield self
        yield from self.expr
        for x in self.params:
            yield from x

class WhileNode(ExpressionNode):
    def __init__(self, condition:ExpressionNode, expr:ExpressionNode, row:int=None, column:int=None):
        super().__init__(row,column)
        self.condition = condition
        self.expr = expr

    def __iter__(self):
        yield self
        yield self.condition
        yield self.expr

class AtomicNode(ExpressionNode):
    def __init__(self, lex:str, row:int=None,column:int=None):
        super().__init__(row,column)
        self.lex = lex

    def __iter__(self):
        yield self

class UnaryNode(ExpressionNode):
    def __init__(self, member:ExpressionNode, row:int=None,column:int=None):
        super().__init__(row,column)
        self.member = member

    def __iter__(self):
        yield self
        yield self.member

class BinaryNode(ExpressionNode):
    def __init__(self, left:ExpressionNode, right:ExpressionNode, row:int=None,column:int=None):
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
    pass

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