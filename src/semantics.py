import visitor
import cool_ast as ast
from utils import TypesExist, MethodInfo, Scope
from check_inherit import CheckInherintance1, CheckInherintance2
from check_semantics import CheckSemantics
from check_types import CheckTypes
from errors import *

class SemanticsAndTypes:
	def __init__(self, tree):
		self.tree = tree
		self.types = TypesExist()
	
	def check(self):
		ct = CreateTypes(self.types)
		ct.visit(self.tree)
		if ct.errors:
			return False
		ci = CheckInherintance1(ct.types)
		ci.visit(self.tree)
		if ci.errors:
			return False
		ci2 = CheckInherintance2()
		ci2.visit(self.tree)
		if ci2.errors:
			return False
		crs = CreateScopes(ci.types)
		crs.visit(self.tree)
		cs = CheckSemantics(crs.types)
		cs.visit(self.tree)
		if cs.errors:
			return False
		cts = CheckTypes(ci.types)
		cts.visit(self.tree)
		self.types = cts.types
		return not cts.errors

class CreateTypes:
	def __init__(self, types):
		self.types = types
		self.errors = False
	
	@visitor.on('node')
	def visit(self, node):
		pass

	@visitor.when(ast.ProgramNode)
	def visit(self, node):
		for expr in node.expr:
			self.visit(expr)

	@visitor.when(ast.ClassNode)
	def visit(self, node):
		if node.type in ["Int", "String", "Bool", "IO", "Object"]:
			self.errors = True
			print(SemanticError(node.line, node.index, "Redefinition of basic class {}.".format(node.type)))
		elif self.types.is_defined(node.type):
			self.errors = True
			print(SemanticError(node.line, node.index-2, "Classes may not be redefined"))
		elif node.inherits in ["Int", "String", "Bool"]:
			self.errors = True
			print(SemanticError(node.line, node.index2, "Class {} cannot inherit class {}.".format(node.type, node.inherits)))
		attrb = {}
		methods = {}
		for n in node.body:
			if type(n) is ast.PropertyNode:
				if n.decl.id == "self":
					self.errors = True
					print(SemanticError(n.line, n.index, "'self' cannot be the name of an attribute."))
				elif n.decl.id in attrb:
					self.errors = True
					print(SemanticError(n.line, n.index, "Property {} already defined in type {}".format(n.decl.id, node.type)))
				else:
					attrb[n.decl.id] = n
			else:
				params = []
				for p in n.params:
					params.append(p.type)
				if n.name in methods:
					self.errors = True
					print(SemanticError(n.line, n.index, "Method {} already defined in type {}".format(n.name, node.type)))
				else:
					method = MethodInfo(n.name, n.type_ret, params, n.line, n.index)
					methods[n.name] = method
					n.info = method
		node.info = self.types.set_type(node.type, methods, attrb)
		
class CreateScopes:
	def __init__(self, types):
		self.types = types
	
	@visitor.on('node')
	def visit(self, node):
		pass

	@visitor.when(ast.ProgramNode)
	def visit(self, node):
		n = len(node.expr)
		while n > 0:
			for expr in node.expr:
				scope = self.types.get_scope(expr.type)
				if scope == None:
					if expr.inherits in ["IO", "Object"] or expr.inherits == None:
						self.visit(expr, Scope())
						n -= 1
					else:
						inherits_scope = self.types.get_scope(expr.inherits)
						if inherits_scope != None:
							self.visit(expr, inherits_scope.new_scope())
							n -= 1

	@visitor.when(ast.ClassNode)
	def visit(self, node, scope):
		for n in node.body:
			if type(n) is ast.PropertyNode:
				self.visit(n, scope)
		self.types.set_scope(node.type, scope)
		
	@visitor.when(ast.PropertyNode)
	def visit(self, node, scope):
		self.visit(node.decl, scope)

	@visitor.when(ast.DeclarationNode)
	def visit(self, node, scope):
		if scope.get_var(node.id) == None:
			node.var_info = scope.append(node.id)
			node.var_info.type = self.types.get_type(node.type)