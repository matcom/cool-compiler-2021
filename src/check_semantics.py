import visitor
import cool_ast as ast
from errors import *
from utils import VarInfo

class CheckSemantics:
	def __init__(self, types):
		self.types = types
		self.errors = False
		self.current_type = None
		
	@visitor.on('node')
	def visit(self, node):
		pass

	@visitor.when(ast.ProgramNode)
	def visit(self, node):
		main = self.types.get_type("Main")
		if not main or not "main" in main.methods:
			self.errors = True
			print(SemanticError(0, 0, "There is no entry point. Couldnt find Main.main()"))
		for expr in node.expr:
			scope = self.types.get_scope(expr.type)
			self.visit(expr, scope)

	@visitor.when(ast.ClassNode)
	def visit(self, node, scope):
		self.current_type = node.info
		for n in node.body:
			self.visit(n, scope)
			
	@visitor.when(ast.PropertyNode)
	def visit(self, node, scope):
		expr = node.decl.expr
		if expr != None:
			self.visit(expr, scope)
			
	@visitor.when(ast.DeclarationNode)
	def visit(self, node, scope, n = ""):
		if node.id == "self":
			self.errors = True
			if n == "param":
				print(SemanticError(node.line, node.index, "'self' cannot be the name of a formal parameter.")) 
			elif n == "let":
				print(SemanticError(node.line, node.index, "'self' cannot be bound in a 'let' expression.")) 
			elif n == "case":
				print(SemanticError(node.line, node.index, "'self' cannot be bound in a 'case' expression.")) 
		else:
			if node.expr != None:
				self.visit(node.expr, scope)
			if scope.is_local(node.id) and n != "let":
				self.errors = True
				if n == "param":
					print(SemanticError(node.line, node.index, "Formal parameter a is multiply defined"))
				else:
					print(SemanticError(node.line, node.index, "Variable {} already defined.".format(node.id)))
			else:
				node.var_info = scope.append(node.id)

	@visitor.when(ast.MethodNode)
	def visit(self, node, scope):
		new_scope = scope.new_scope()
		for param in node.params:
			self.visit(param, new_scope, "param")
		self.visit(node.body, new_scope)

	@visitor.when(ast.AssignNode)
	def visit(self, node, scope):
		if node.id == "self":
			self.errors = True
			print(SemanticError(node.line, node.index2, "Cannot assign to 'self'."))
		else:		
			self.visit(node.expr, scope)
			node.var_info = scope.get_var(node.id)
			if node.var_info == None:
				node.var_info = scope.append(node.id)

	@visitor.when(ast.WhileNode)
	def visit(self, node, scope):
		new_scope = scope.new_scope()
		self.visit(node.conditional, scope)
		self.visit(node.expr, new_scope)

	@visitor.when(ast.IfNode)
	def visit(self, node, scope):
		new_scope = scope.new_scope()
		self.visit(node.conditional, scope)
		self.visit(node.expr_then, new_scope)
		self.visit(node.expr_else, new_scope)

	@visitor.when(ast.LetInNode)
	def visit(self, node, scope):
		new_scope = scope.new_scope()
		for decl in node.decl_list:
			self.visit(decl, new_scope, "let")
		self.visit(node.expr, new_scope)

	@visitor.when(ast.CaseNode)
	def visit(self, node, scope):
		self.visit(node.expr, scope)
		for case in node.case_list:
			self.visit(case, scope)

	@visitor.when(ast.CaseItemNode)
	def visit(self, node, scope):
		new_scope = scope.new_scope()
		self.visit(node.variable, new_scope, "case")
		self.visit(node.expr, new_scope)

	@visitor.when(ast.DispatchNode)
	def visit(self, node, scope):
		for param in node.params:
			self.visit(param, scope)
		
	@visitor.when(ast.DispatchInstanceNode)
	def visit(self, node, scope):
		self.visit(node.variable, scope)
		for param in node.params:
			self.visit(param, scope)
		
	@visitor.when(ast.DispatchParentInstanceNode)
	def visit(self, node, scope):
		self.visit(node.variable, scope)
		for param in node.params:
			self.visit(param, scope)
		
	@visitor.when(ast.BlockNode)
	def visit(self, node, scope):
		for expr in node.expr_list:
			self.visit(expr, scope)

	@visitor.when(ast.BinaryOperatorNode)
	def visit(self, node, scope):
		self.visit(node.left, scope)
		self.visit(node.right, scope)

	@visitor.when(ast.UnaryOperator)
	def visit(self, node, scope):
		self.visit(node.expr, scope)

	@visitor.when(ast.NotNode)
	def visit(self, node, scope):
		self.visit(node.expr, scope)

	@visitor.when(ast.ComplementNode)
	def visit(self, node, scope):
		self.visit(node.expr, scope)

	@visitor.when(ast.IsVoidNode)
	def visit(self, node, scope):
		self.visit(node.expr, scope)

	@visitor.when(ast.VariableNode)
	def visit(self, node, scope):
		if node.id != 'self':
			node.var_info = scope.get_var(node.id)
			if node.var_info == None:
				self.errors = True
				print(NameError(node.line, node.index, "Undeclared identifier {}.".format(node.id)))
		else:
			node.var_info = VarInfo("self", self.current_type)
		
	@visitor.when(ast.NegationNode)
	def visit(self, node, scope):
		self.visit(node.expr, scope)
