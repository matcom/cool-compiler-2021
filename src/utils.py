import sys
import itertools as itl
from cool_ast import DeclarationNode, PropertyNode

class TypesExist:
	def __init__(self): 	
		#methods for primitive types
		object_methods = {"type_name" : MethodInfo("type_name", "String", []), 
							"abort" : MethodInfo("abort", "Object", [])}	

		string_methods = {"length" : MethodInfo("length", "Int", []),
							"concat" : MethodInfo("concat", "String", ["String"]),
							"substr" : MethodInfo("substr", "String", ["Int", "Int"])}	

		io_methods = {"in_int" : MethodInfo("in_int", "Int", []),
					  "out_int": MethodInfo("out_int", "IO", ["Int"]),
					  "in_string" : MethodInfo("in_string", "String", []),
					  "out_string": MethodInfo("out_string", "IO", ["String"])}
		
		#primitive types declaration     
		type_object = ClassInfo("Object", None, object_methods, {"holder": PropertyNode(DeclarationNode("holder", None, None,0,0,0,0))})
		type_int = ClassInfo("Int", type_object)        
		type_string = ClassInfo("String", type_object, string_methods)
		type_bool = ClassInfo("Bool", type_object)
		type_io = ClassInfo("IO", type_object, io_methods)
		void = ClassInfo("Void")

		#dicctionary witch types
		self.types = {"Object": type_object,
					  "Int": type_int,
					  "String": type_string,
					  "Bool": type_bool,
					  "IO": type_io,
					  "Void": void
					  }
					  
	def is_defined(self, name):
		return True if name in self.types else False

	def get_type(self, name):
		return self.types[name] if self.is_defined(name) else None
	
	def get_parent_type(self, name):
		return self.types[name].inherits if self.is_defined(name) else None
		
	def set_type(self, name, methods, attrb):
		self.types[name] = ClassInfo(name, self.types["Object"], methods, attrb)
		return self.types[name]
	
	def change_inherits(self, name, inherits):
		self.types[name].inherits = self.types[inherits]
		
	def set_scope(self, name, scope):
		self.types[name].scope = scope
		
	def get_scope(self, name):
		return self.types[name].scope
	
	def check_inheritance(self, type_A, type_B):
		parents = []
		a = type_A
		b = type_B
		if a == b:
			return a
		while a.inherits != None:
			parents.append(a)
			a = a.inherits
		while b != None:
			if b in parents:
				return b
			b = b.inherits
		return self.types["Object"]
		
	def check_variance(self, type_A, type_B):
		b = type_B
		while True:
			if b == None:
				return False
			if type_A == b:
				return True
			b = b.inherits

class MethodInfo:
	def __init__(self, name, type_ret, params_types, line = 0, index = 0):
		self.name = name
		self.type_ret = type_ret
		self.params_types = params_types
		self.cil_name = ""
		self.line = line
		self.index = index
		
class ClassInfo:
	def __init__(self, name, inherits = None, methods = None, attrb = None):
		self.name = name
		self.inherits = inherits
		self.methods = methods if methods else {}
		self.attrb = attrb if attrb else {}
		self.scope = None
		self.generate_cil_names()

	def generate_cil_names(self):
		for name, method in self.methods.items():
			method.cil_name = '{}_{}'.format(self.name, name)

class VarInfo:
	def __init__(self, name, type = None):
		self.name = name
		self.type = type if type else ClassInfo("Void")
		self.holder = None

class Scope:
	def __init__(self, parent = None):
		self.parent = parent
		self.locals = []
		self.children = []
		self.index = 0 if parent == None else len(parent.locals)

	def append(self, name):
		var = VarInfo(name)
		self.locals.append(var)
		return var

	def new_scope(self):
		scope = Scope(self)
		self.children.append(scope)
		return scope

	def get_var(self, name):
		current = self
		top = len(self.locals)
		while current != None:
			var = Scope.find(name, current, top)
			if var != None:
				return var
			top = current.index
			current = current.parent
		return None

	def is_local(self, name):
		return Scope.find(name, self) != None

	@staticmethod
	def find(name, scope, top = None):
		if top == None:
			top = len(scope.locals)
		candidates = (var for var in itl.islice(scope.locals, top) if var.name == name)
		return next(candidates, None)
