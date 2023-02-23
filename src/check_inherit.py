import visitor
import cool_ast as ast
from errors import *

class CheckInherintance1:
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
		if node.inherits:
			if not self.types.is_defined(node.inherits):
				self.errors = True
				print(TypeError(node.line, node.index2, "Class {} inherits from an undefined class {}.".format(node.type, node.inherits)))
			else:
				parent = self.types.get_type(node.inherits)
				p = parent
				#Check cycles
				while p != None:
					if p.name == node.type:
						self.errors = True
						print(SemanticError(node.line, node.index2, "Class {}, or an ancestor of {}, is involved in an inheritance cycle.".format(node.type, node.type)))
						return
					p = p.inherits
				self.types.change_inherits(node.type, node.inherits)

class CheckInherintance2:
	def __init__(self):
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
		for n in node.body:
			self.visit(n, node.info)
				
	@visitor.when(ast.PropertyNode)
	def visit(self, node, info):
		self.visit(node.decl, info)
	
	#Check attribute inherited
	@visitor.when(ast.DeclarationNode)
	def visit(self, node, info):
		parent = info.inherits
		while parent != None:
			if node.id in parent.attrb.keys():
				aux = parent.attrb[node.id]
				if node.type == aux.decl.type:
					self.errors = True
					print(SemanticError(node.line, node.index, "Attribute {} is an attribute of an inherited class.".format(node.id)))
					break
			parent = parent.inherits
		
	#Check overloads methods
	@visitor.when(ast.MethodNode)
	def visit(self, node, info):
		parent = info.inherits
		while parent != None:
			if node.name in parent.methods.keys():
				aux = parent.methods[node.name]
				if node.type_ret != aux.type_ret:
					self.errors = True
					print(SemanticError(node.line, node.index2, "In redefined method {}, return type {} is different from original return type {}.".format(node.name, node.type_ret, aux.type_ret)))
					break
				elif len(node.params) != len(aux.params_types):
						self.errors = True
						print(SemanticError(node.line, node.index, "Incompatible number of formal parameters in redefined method {}.".format(node.name)))
						break						
				else:
					params = aux.params_types
					i = -1
					for param in node.params:
						i += 1 
						if param.type != params[i]:
							self.errors = True
							print(SemanticError(param.line, param.index, "In redefined method {}, parameter type {} is different from original type {}.".format(node.name, param.type, params[i])))
							return
			parent = parent.inherits