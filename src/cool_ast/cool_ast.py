class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass
class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, value = None):
        self.id = idx
        self.type = typex
        self.value = value

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr = None):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, method, args, obj = None, parent = None):
        self.method = method
        self.args = args
        self.obj = obj
        self.parent = parent #propiedad necesaria para la instruccion id@parentType.prop(args)

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


#mios
class ChunkNode(ExpressionNode):
    def __init__(self, chunk):
        self.chunk = chunk
        
# class VarNode(ExpressionNode):
#     def __init__(self, idx, type, expr = None):
#         self.id = idx
#         self.type = type
#         self.value = expr

class ConditionalNode(ExpressionNode):
    def __init__(self, ifChunk, thenChunk, elseChunk):
        self.ifChunk = ifChunk
        self.thenChunk = thenChunk
        self.elseChunk = elseChunk

class WhileNode(ExpressionNode):
    def __init__(self, condition, loopChunk):
        self.condition = condition
        self.loopChunk = loopChunk

class LetInNode(ExpressionNode):
    def __init__(self, decl_list, expression):
        self.decl_list = decl_list
        self.expression = expression

class NotNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression

class IsVoidNode(ExpressionNode):
    def __init__(self, method):
        self.method = method

class ComplementNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class SwitchCaseNode(ExpressionNode):
    def __init__(self, expr, case_list):
        self.expr = expr
        self.case_list = case_list

class ConstantNumNode(AtomicNode):
    pass
class VariableNode(AtomicNode):
    pass
class InstantiateNode(AtomicNode):
    pass

#mios
class TrueNode(AtomicNode):
    pass
class FalseNode(AtomicNode):
    pass
class StringNode(AtomicNode):
    pass
class VoidNode(AtomicNode):
    pass
class AutoTypeNode(AtomicNode):
    pass

class PlusNode(BinaryNode):
    pass
class MinusNode(BinaryNode):
    pass
class StarNode(BinaryNode):
    pass
class DivNode(BinaryNode):
    pass

#mios
class LessNode(BinaryNode):
    pass
class LeqNode(BinaryNode):
    pass
class EqualNode(BinaryNode):
    pass