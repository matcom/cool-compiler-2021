class Node:
	pass

class ProgramNode(Node):
	def __init__(self, expr):
		self.expr = expr

class ExpressionNode(Node):
	def __init__(self):
		self.type_expr = None
		
class AtomicNode(ExpressionNode):
    pass

class ClassNode(AtomicNode):
	def __init__(self, type, inherits, body, line = 0, index = 0, index2 = 0):
		AtomicNode.__init__(self)
		self.type = type
		self.inherits = inherits
		self.body = body
		self.info = None
		self.line = line
		self.index = index
		self.index2 = index2

class PropertyNode(AtomicNode):
	def __init__(self, decl, line = 0, index = 0):
		AtomicNode.__init__(self)
		self.decl = decl	
		self.line = line
		self.index = index

class UtilNode(Node):
    pass

class DeclarationNode(UtilNode):
	def __init__(self, id, type, expr, line, index, index2=0, index3=0):
		UtilNode.__init__(self)
		self.id = id
		self.type = type
		self.expr = expr
		self.line = line
		self.index = index
		self.index2 = index2
		self.index3 = index3
		self.var_info = None
		
class MethodNode(AtomicNode):
	def __init__(self, id, params, type_ret, body, line=0, index=0, index2=0):
		AtomicNode.__init__(self)
		self.name = id
		self.params = params
		self.type_ret = type_ret
		self.body = body
		self.line = line
		self.index = index
		self.index2 = index2
		self.info = None
		
class AssignNode(AtomicNode):
	def __init__(self, id, expr, line, index=0, index2=0):
		AtomicNode.__init__(self)
		self.id = id
		self.expr = expr
		self.line = line
		self.index = index
		self.index2 = index2
		self.var_info = None
		
class WhileNode(AtomicNode):
	def __init__(self, conditional, expr, line, index, index2=0):
		AtomicNode.__init__(self)
		self.conditional = conditional
		self.expr = expr
		self.line = line
		self.index = index
		self.index2 = index2
		
class IfNode(AtomicNode):
	def __init__(self, conditional, expr_then, expr_else, line, index=0):
		AtomicNode.__init__(self)
		self.conditional = conditional
		self.expr_then = expr_then
		self.expr_else = expr_else
		self.line = line
		self.index = index
		
class LetInNode(AtomicNode):
	def __init__(self, decl_list, expr, line, index):
		AtomicNode.__init__(self)
		self.decl_list = decl_list
		self.expr = expr
		self.line = line
		self.index = index

class CaseNode(AtomicNode):
	def __init__(self, expr, case_list, line, index):
		AtomicNode.__init__(self)
		self.expr = expr
		self.case_list = case_list
		self.line = line
		self.index = index
		
class CaseItemNode(AtomicNode):
	def __init__(self, variable, expr, line, index, index2=0):
		AtomicNode.__init__(self)
		self.variable = variable
		self.expr = expr
		self.line = line
		self.index = index
		self.index2 = index2
		
class DispatchNode(AtomicNode):
	def __init__(self, id, params, line, index):
		AtomicNode.__init__(self)
		self.id = id
		self.params = params
		self.line = line
		self.index = index
		self.type_method = None
		
class DispatchInstanceNode(ExpressionNode):
	def __init__(self, variable, id_method, params, line=0, index=0, index2=0):
		ExpressionNode.__init__(self)
		self.variable = variable
		self.id_method = id_method
		self.params = params
		self.line = line
		self.index = index
		self.index2 = index2
		self.type_method = None

class DispatchParentInstanceNode(ExpressionNode):
	def __init__(self, variable, id_parent, id_method, params, line, index, index2=0, index3=0):
		ExpressionNode.__init__(self)
		self.variable = variable
		self.id_parent = id_parent
		self.id_method = id_method
		self.params = params
		self.line = line
		self.index = index
		self.index2 = index2
		self.index3 = index3
		
class BlockNode(AtomicNode):
	def __init__(self, expr_list, line, index):
		AtomicNode.__init__(self)
		self.expr_list = expr_list
		self.line = line
		self.index = index
		
class BinaryOperatorNode(ExpressionNode):
	def __init__(self, left, right, line, index, index2=0):
		ExpressionNode.__init__(self)
		self.left = left
		self.right = right
		self.line = line
		self.index = index
		self.index2 = index2
		
class PlusNode(BinaryOperatorNode):
    pass

class MinusNode(BinaryOperatorNode):
    pass

class StarNode(BinaryOperatorNode):
    pass

class DivNode(BinaryOperatorNode):
    pass

class UnaryOperator(ExpressionNode):
	def __init__(self, expr, line, index, index2=0):
		ExpressionNode.__init__(self)
		self.expr = expr
		self.line = line
		self.index = index
		self.index2 = index2

class NotNode(UnaryOperator):
    pass
	
class ComplementNode(UnaryOperator):
    pass
	
class IsVoidNode(AtomicNode):
	def __init__(self, expr, line, index):
		AtomicNode.__init__(self)
		self.expr = expr
		self.line = line
		self.index = index
		
class NewNode(AtomicNode):
	def __init__(self, type, line=0, index=0, index2=0):
		AtomicNode.__init__(self)
		self.type = type
		self.line = line
		self.index = index
		self.index2 = index2
		
class LessThanNode(BinaryOperatorNode):
    pass

class LessEqualNode(BinaryOperatorNode):
    pass

class EqualNode(BinaryOperatorNode):
    pass
	
class VariableNode(AtomicNode):
	def __init__(self, id, line, index):
		AtomicNode.__init__(self)
		self.id = id
		self.line = line
		self.index = index
		self.var_info = None

class IntegerNode(AtomicNode):
	def __init__(self, integer, line, index):
		AtomicNode.__init__(self)
		self.integer = integer
		self.line = line
		self.index = index
		
class StringNode(AtomicNode):
	def __init__(self, string, line, index):
		AtomicNode.__init__(self)
		self.string = str(string)
		self.line = line
		self.index = index

class BooleanNode(ExpressionNode):
	def __init__(self, value, line, index):
		ExpressionNode.__init__(self)
		self.value = True if value == "true" else False
		self.line = line
		self.index = index
		
