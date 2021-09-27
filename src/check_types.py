import visitor
import cool_ast as ast
from errors import *

class CheckTypes:
	def __init__(self, types):
		self.class_type = None
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
		node.type_expr = self.types.get_type(node.type)
		self.class_type = node.type_expr
		if not node.type_expr:
			self.errors = True
			print(TypeError(node.line, node.index, "Type {} is not defined".format(node.type)))
		for expr in node.body:
			self.visit(expr)
		return node.type_expr

	@visitor.when(ast.PropertyNode)
	def visit(self, node):
		node.type_expr = self.visit(node.decl, "attrb")
		return node.type_expr

	@visitor.when(ast.DeclarationNode)
	def visit(self, node, n):
		aux = self.types.get_type(node.type)
		if aux == None:	
			self.errors = True
			if n == "param":
				print(TypeError(node.line, node.index2, "Class {} of formal parameter {} is undefined.".format(node.type, node.id)))
			elif n == "let":
				print(TypeError(node.line, node.index2, "Class {} of let-bound identifier {} is undefined.".format(node.type, node.id)))
			elif n == "attrb":
				print(TypeError(node.line, node.index2, "Class {} of attribute {} is undefined.".format(node.type, node.id)))
			elif n == "case":
				print(TypeError(node.line, node.index2, "Class {} of case branch is undefined.".format(node.type)))
		else:
			if node.expr != None:
				expr = self.visit(node.expr)
				if not self.types.check_variance(aux, expr):
					self.errors = True
					print(TypeError(node.expr.line, node.expr.index, "Inferred type {} of initialization of attribute {} does not conform to declared type {}.".format(expr.name, node.id, node.type)))
		node.type = node.var_info.type = aux
		return node.type

	@visitor.when(ast.MethodNode)
	def visit(self, node):
		for param in node.params:
			self.visit(param, "param")
		if not self.types.is_defined(node.type_ret):
			self.errors = True
			print(TypeError(node.line, node.index2, "Undefined return type {} in method {}.".format(node.type_ret, node.name)))#OH
		node.type_expr = self.visit(node.body)
		ret = self.types.get_type(node.type_ret)
		variance = self.types.check_variance(ret, node.type_expr)
		if not variance:
			self.errors = True
			print(TypeError(node.body.line, node.body.index, "Inferred return type {} of method {} does not conform to declared return type {}.".format(node.type_expr.name, node.name, node.type_ret)))
		return node.type_expr

	@visitor.when(ast.AssignNode)
	def visit(self, node):
		expr = self.visit(node.expr)
		if node.var_info.type != self.types.get_type("Void"):
			variance = self.types.check_variance(node.var_info.type, expr)
			if not variance:
				self.errors = True
				print(TypeError(node.line, node.index2, "Type mistmatch with variable {}".format(node.var_info.name)))
		node.type_expr = node.var_info.type = expr
		return node.type_expr

	@visitor.when(ast.WhileNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Object")
		self.visit(node.expr)
		expr = self.visit(node.conditional)
		if expr != self.types.get_type("Bool"):
			self.errors = True
			print(TypeError(node.line, node.index2, "Loop condition does not have type Bool"))
		return node.type_expr

	@visitor.when(ast.IfNode)
	def visit(self, node):
		expr = self.visit(node.conditional)
		if expr != self.types.get_type("Bool"):
			self.errors = True 
			print(TypeError(node.conditional.line, node.conditional.index, "Predicate of 'if' does not have type Bool."))
		then_expr = self.visit(node.expr_then)
		else_expr = self.visit(node.expr_else)
		node.type_expr = self.types.check_inheritance(then_expr, else_expr)
		return node.type_expr

	@visitor.when(ast.LetInNode)
	def visit(self, node):
		for n in node.decl_list:
			self.visit(n, "let")
		node.type_expr = self.visit(node.expr)
		return node.type_expr

	@visitor.when(ast.CaseNode)
	def visit(self, node):
		self.visit(node.expr)
		aux = self.visit(node.case_list[0], [])
		list = [node.case_list[0].variable.type]
		for i in range(1, len(node.case_list)):
			expr = self.visit(node.case_list[i], list)		
			aux = self.types.check_inheritance(expr, aux)
			list.append(node.case_list[i].variable.type)
		node.type_expr = aux
		return node.type_expr

	@visitor.when(ast.CaseItemNode)
	def visit(self, node, list):
		self.visit(node.variable, "case")
		if node.variable.type in list:
			self.errors = True
			print(SemanticError(node.line, node.index2, "Duplicate branch {} in case statement.".format(node.variable.type.name)))
		aux = self.visit(node.expr)
		if aux == None:
			self.errors = True
			print(SemanticError(node.line, node.index2, "The expresion is None"))
		else:
			node.type_expr = aux
		return node.type_expr

	@visitor.when(ast.DispatchNode)
	def visit(self, node):
		method = None
		id_class = self.class_type
		while not method and id_class:
			for n, m in id_class.methods.items():
				if n == node.id:
					method = m
					break
			id_class = id_class.inherits
		if not method:
			self.errors = True 
			print(AttributeError(node.line, node.index, "Dispatch to undefined method {}.".format(node.id)))
			return self.types.get_type("Void")
		elif len(method.params_types) != len(node.params):
			self.errors = True
			print(SemanticError(node.line, node.index, "Method {} called with wrong number of arguments".format(node.id)))
		else:
			for i in range(len(node.params)):
				aux = self.types.get_type(method.params_types[i])
				expr = self.visit(node.params[i])
				if not self.types.check_variance(aux, expr):
					self.errors = True 
					print(TypeError(node.params[i].line, node.params[i].index, "In call of method {}, type {} of parameter number {} does not conform to declared type {}.".format(node.id, expr.name, i, aux.name)))
			node.type_expr = self.types.get_type(method.type_ret)
			node.type_method = method
		return node.type_expr

	@visitor.when(ast.DispatchInstanceNode)
	def visit(self, node):
		type_var = self.visit(node.variable)
		method = None
		id_class = type_var
		while not method and id_class:
			for n, m in id_class.methods.items():
				if n == node.id_method:
					method = m
					break
			id_class = id_class.inherits
		node.type_method = method
		if not method:
			self.errors = True
			print(AttributeError(node.line, node.index2, "Class {} doesnt contains method {}.".format(type_var.name, node.id_method)))
			return self.types.get_type("Void")
		else:
			if len(method.params_types) != len(node.params):
				self.errors = True
				print(SemanticError(node.line, node.index2, "Method {} called with wrong number of arguments".format(node.id_method)))
			else:
				for i in range(0, len(node.params)):
					aux = self.types.get_type(method.params_types[i])
					expr = self.visit(node.params[i])
					if not self.types.check_variance(aux, expr):
						self.errors = True
						print(TypeError(node.params[i].line, node.params[i].index, "In call of method {}, type {} of parameter number {} does not conform to declared type {}.".format(node.id_method, expr.name, i, aux.name)))
			node.type_expr = self.types.get_type(method.type_ret)
		return node.type_expr

	@visitor.when(ast.DispatchParentInstanceNode)
	def visit(self, node):
		type_var = self.visit(node.variable)
		id_class = type_var
		id_parent = self.types.get_type(node.id_parent)
		method = None
		if not id_parent:
			self.errors = True
			print(TypeError(node.line, node.index3, "Type {} is not defined".format(node.id_parent)))
		while not method and id_class:
			if id_class == id_parent:
				for n, m in id_class.methods.items():
					if n == node.id_method:
						method = m
						break
				if not method:
					self.errors = True
					print(AttributeError(node.line, node.index2, "Parent class {} doesnt have a definition for method {}".format(node.id_parent, node.id_method)))
					return self.types.get_type(method.type_ret)
				break
			id_class = id_class.inherits
		if not id_class:
			self.errors = True
			print(TypeError(node.line, node.index, "Expression type {} does not conform to declared static dispatch type {}. ".format(type_var.name, node.id_parent)))
			return self.types.get_type("Void")
		else:
			if len(method.params_types) != len(node.params):
				self.errors = True
				print(SemanticError(node.line, node.index2, "Method {} called with wrong number of arguments".format(node.id_method)))
			else:
				for i in range(0, len(node.params)):
					aux = self.types.get_type(method.params_types[i])
					expr = self.visit(node.params[i])
					if not self.types.check_variance(aux, expr):
						self.errors = True
						print(TypeError(node.params[i].line, node.params[i].index, "In call of method {}, type {} of parameter {} does not conform to declared type {}.".format(node.id_method, expr.name, i, aux.name)))
			node.type_expr = self.types.get_type(method.type_ret)
		return node.type_expr

	@visitor.when(ast.BlockNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Void")
		for expr in node.expr_list:
			node.type_expr = self.visit(expr)
		return node.type_expr

	@visitor.when(ast.PlusNode)
	def visit(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		type_int = self.types.get_type("Int")
		if left != type_int or right != type_int:
			self.errors = True
			print(TypeError(node.line, node.index2, "non-Int arguments: {} + {}".format(left.name, right.name)))
		node.type_expr = type_int
		return node.type_expr

	@visitor.when(ast.MinusNode)
	def visit(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		type_int = self.types.get_type("Int")
		if left != type_int or right != type_int:
			self.errors = True 
			print(TypeError(node.line, node.index2, "non-Int arguments: {} - {}".format(left.name, right.name)))
		node.type_expr = type_int
		return node.type_expr

	@visitor.when(ast.StarNode)
	def visit(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		type_int = self.types.get_type("Int")
		if left != type_int or right != type_int:
			self.errors = True
			print(TypeError(node.line, node.index2, "non-Int arguments: {} * {}".format(left.name, right.name)))
		node.type_expr = type_int
		return node.type_expr

	@visitor.when(ast.DivNode)
	def visit(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		type_int = self.types.get_type("Int")
		if left != type_int or right != type_int:
			self.errors = True 
			print(TypeError(node.line, node.index2, "non-Int arguments: {} / {}".format(left.name, right.name)))
		node.type_expr = type_int
		return node.type_expr

	@visitor.when(ast.NotNode)
	def visit(self, node):
		expr = self.visit(node.expr)
		if expr != self.types.get_type("Bool"):
			self.errors = True
			print(TypeError(node.line, node.index2, "Argument of 'not' has type {} instead of Bool.".format(expr.name)))
		node.type_expr = self.types.get_type("Bool")
		return node.type_expr

	@visitor.when(ast.ComplementNode)
	def visit(self, node):
		expr = self.visit(node.expr)
		type_int = self.types.get_type("Int")
		if expr != type_int:
			self.errors = True
			print(TypeError(node.line, node.index2, "Argument of '~' has type {} instead of Int.".format(expr.name)))
		node.type_expr = type_int
		return node.type_expr

	@visitor.when(ast.IsVoidNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Bool")
		return node.type_expr

	@visitor.when(ast.NewNode)
	def visit(self, node):
		node.type_expr = self.types.get_type(node.type)
		if not node.type_expr:
			self.errors = True
			print(TypeError(node.line, node.index2, "'new' used with undefined class {}.".format(node.type)))
		return node.type_expr

	@visitor.when(ast.LessThanNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Bool")
		left = self.visit(node.left)
		right = self.visit(node.right)
		if left == right == self.types.get_type("Int"):
			return node.type_expr
		self.errors = True
		print(TypeError(node.line, node.index2, "non-Int arguments: {} < {}".format(left.name, right.name)))
		return node.type_expr

	@visitor.when(ast.LessEqualNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Bool")
		left = self.visit(node.left)
		right = self.visit(node.right)
		if left == right == self.types.get_type("Int"):
			return node.type_expr
		self.errors = True
		print(TypeError(node.line, node.index2, "non-Int arguments: {} <= {}".format(left.name, right.name)))
		return node.type_expr

	@visitor.when(ast.EqualNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Bool")
		left = self.visit(node.left)
		right = self.visit(node.right)
		static = ["Int", "Bool", "String"]
		if (left.name in static or right.name in static) and left != right:
			self.errors = True
			print(TypeError(node.line, node.index2, "Illegal comparison with a basic type."))
		return node.type_expr

	@visitor.when(ast.VariableNode)
	def visit(self, node):
		if node.id == "self":
			node.type_expr = self.class_type
		else:
			node.type_expr = node.var_info.type
		return node.type_expr

	@visitor.when(ast.IntegerNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Int")
		return node.type_expr

	@visitor.when(ast.StringNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("String")
		return node.type_expr

	@visitor.when(ast.BooleanNode)
	def visit(self, node):
		node.type_expr = self.types.get_type("Bool")
		return node.type_expr