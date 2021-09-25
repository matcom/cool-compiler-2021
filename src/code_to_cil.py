import visitor
import cool_cil as cil
import cool_ast as ast
from utils import MethodInfo, VarInfo

class CodeToCIL:
	def __init__(self, types):
		self.types = types
		self.dottypes = []
		self.dotdata = []
		self.dotcode = []
		self.arguments = []
		self.instructions = []
		self.local_vars = []
		self.current_type = None
		self.self_type = None
		self.current_method = ""
		self.internal_count = 0
		self.label_count = 0

	def new_label(self):
		self.label_count += 1
		return "label_{}".format(self.label_count)

	def register_primitive_types(self):
		methods = PrimitiveMethods()
		for name in ["Object", "Int", "String", "Bool", "IO"]:
			id_class = self.types.get_type(name)
			self.register_type(name, id_class)
			for n, m in id_class.methods.items():
				self.register_method(n, m.cil_name, methods.params[n], methods.cil_node[n])
				
	def register_type(self, name, type):
		attrb = []
		methods = {}
		self.build_type(type, attrb, methods)
		self.dottypes.append(Type(name, attrb, methods))
		self.dotdata.append(cil.DataNode(name, '"%s"' % name))
	
	def build_type(self, id_class, attrb, methods):
		if id_class == None:
			return
		self.build_type(id_class.inherits, attrb, methods)
		if id_class.methods:
			for name in id_class.methods:
				methods[name] = Method(id_class.methods[name].cil_name)
		if id_class.attrb:
			for name in id_class.attrb:
				attrb.append(name)

	def register_method(self, name, cil_name, params, cil_node):
		instructions = []
		self.local_vars = []
		variables = []
		arguments = []
		local = None

		for param in params:
			var = VarInfo(param)
			variables.append(var)
			arguments.append(cil.ParamNode(var))
		if name != "abort":
			local = self.register_local_var()
			variables.append(local)
		cargs = tuple(variables)
		instructions.append(cil_node(*cargs))
		if name != "abort":
			instructions.append(cil.ReturnNode(local))
		self.dotcode.append(cil.MethodNode(cil_name, arguments, self.local_vars, instructions))

	def register_local_var(self, node = None):
		var = node.var_info if node else VarInfo('internal')
		var.name = "{}_{}_{}".format(self.internal_count, self.current_method, var.name)
		self.internal_count += 1
		var.holder = len(self.local_vars)
		self.local_vars.append(cil.VarLocalNode(var))
		return var

	def register_data(self, value):
		name = "data_{}".format(len(self.dotdata))
		data = cil.DataNode(name, value)
		self.dotdata.append(data)
		return data

	def check_variance(self, node, i, j):
		type_A = self.types.get_type(node.case_list[i].variable.type)
		type_B = self.types.get_type(node.case_list[j].variable.type)
		check = self.types.check_variance(type_A, type_B)
		return 1 if check else 0
			
	@visitor.on('node')
	def visit(self, node):
		pass

	@visitor.when(ast.ProgramNode)
	def visit(self, node):
		main = ast.NewNode("Main")
		main.type_expr = self.types.get_type("Main")
		method = ast.MethodNode("entry", [], self.types.get_type("Int"), ast.DispatchInstanceNode(main, "main", []))
		method.info = MethodInfo("entry", method.type_expr, [])
		method.info.cil_name = "entry"
		self.visit(method)
		for expr in node.expr:
			self.visit(expr)
		self.register_primitive_types()
		return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

	@visitor.when(ast.ClassNode)
	def visit(self, node):
		self.current_type = node.info
		self.register_type(node.type, node.info)
		for expr in node.body:
			if type(expr) is ast.MethodNode:
				self.visit(expr)

	@visitor.when(ast.PropertyNode)
	def visit(self, node):
		return self.visit(node.decl)

	@visitor.when(ast.DeclarationNode)
	def visit(self, node):
		if node.expr == None:
			return self.register_local_var(node)
		else:
			var = self.visit(node.expr)
			if type(var) is VarInfo:
				node.var_info.name = var.name
			self.register_local_var(node)
			self.instructions.append(cil.AssignNode(node.var_info, var))
			return var
	
	@visitor.when(ast.MethodNode)
	def visit(self, node):
		self.instructions = []
		self.arguments = []
		self.local_vars = []
		self.current_method = node.info.cil_name
		self.self_type = VarInfo("self_type", self.current_type)
		args = []
		args.append(cil.ParamNode(self.self_type))

		for param in node.params:
			args.append(cil.ParamNode(param.var_info))
			param.var_info.name = "{}_{}".format(node.name, param.id)
			self.arguments.append(param.var_info)

		var = self.visit(node.body)
		cil_node = cil.EndProgram(var) if node.name == "entry" else cil.ReturnNode(var)
		self.instructions.append(cil_node)
		self.dotcode.append(cil.MethodNode(self.current_method, args, self.local_vars, self.instructions))

	@visitor.when(ast.AssignNode)
	def visit(self, node):
		var = self.visit(node.expr)
		boxing = node.type_expr.name == "Object" and (type(var) is not VarInfo or var.type.name in ["Int", "Bool"])
		if node.var_info.name in self.current_type.attrb:
			value = self.register_local_var() if boxing else var
			if boxing:
				self.instructions.append(cil.BoxingVariable(var, value))
			self.instructions.append(cil.SetAttrbNode(self.self_type, node.id, value))
			return var
		elif node.var_info in self.arguments:
			cil_node = cil.BoxingVariable(var, node.var_info) if boxing else cil.AssignNode(node.var_info, var)
			self.instructions.append(cil_node)
		else:
			if node.var_info.holder == None:
				self.register_local_var(node)
			cil_node = cil.BoxingVariable(var, node.var_info) if boxing else cil.AssignNode(node.var_info, var)
			self.instructions.append(cil_node)
		return node.var_info

	@visitor.when(ast.WhileNode)
	def visit(self, node):
		start = cil.LabelNode(self.new_label())
		loop = cil.LabelNode(self.new_label())
		end = cil.LabelNode(self.new_label())
		self.instructions.append(start)
		var_cond = self.visit(node.conditional)
		self.instructions.append(cil.GotoIfNode(var_cond, loop))
		self.instructions.append(cil.GotoNode(end))
		self.instructions.append(loop)
		self.visit(node.expr)
		self.instructions.append(cil.GotoNode(start))
		self.instructions.append(end)
		return 0
	
	@visitor.when(ast.IfNode)
	def visit(self, node):
		then = cil.LabelNode(self.new_label())
		end = cil.LabelNode(self.new_label())
		var_cond = self.visit(node.conditional)
		var = self.register_local_var()
		var.type = node.type_expr
		self.instructions.append(cil.GotoIfNode(var_cond, then))
		var_else = self.visit(node.expr_else)
		self.instructions.append(cil.AssignNode(var, var_else))
		self.instructions.append(cil.GotoNode(end))
		self.instructions.append(then)
		var_then = self.visit(node.expr_then)
		self.instructions.append(cil.AssignNode(var, var_then))
		self.instructions.append(end)
		return var

	@visitor.when(ast.LetInNode)
	def visit(self, node):
		for n in node.decl_list:
			self.visit(n)
		var = self.visit(node.expr)
		return var
	
	@visitor.when(ast.CaseNode)
	def visit(self, node):
		labels = []
		tunels = [[]]
		bases = [[]]
		ends = []
		n = len(node.case_list)
		end = cil.LabelNode(self.new_label())
		var = self.visit(node.expr)
		checkr = self.register_local_var()
		
		if type(var) is VarInfo and var.type.name == "Object":
			temp = self.register_local_var()
			self.instructions.append(cil.UnboxingVariable(var, temp))
			var = temp

		for i in range(n):
			temp = cil.LabelNode(self.new_label())
			labels.append(temp)
			for j in range(i + 1, n):
				t1 = cil.LabelNode(self.new_label())
				t2 = cil.LabelNode(self.new_label())
				tunels[len(tunels) - 1].append(t1)
				bases[len(bases) - 1].append(t2)
			bases.append([])
			tunels.append([])
			self.instructions.append(cil.CheckHierarchy(checkr, node.case_list[i].variable.type, var))
			self.instructions.append(cil.GotoIfNode(checkr, temp))
		self.instructions.append(cil.ErrorNode)
		self.instructions.append(cil.GotoNode(end))

		for i in range(0, n):
			self.instructions.append(labels[i])
			for j in range(i + 1, n):
				cond = self.check_variance(node, i, j)
				self.instructions.append(cil.GotoIfNode(cond, tunels[i][j - i - 1]))
				self.instructions.append(bases[i][j - i - 1])
			t = cil.LabelNode(self.new_label())
			ends.append(t)
			self.instructions.append(cil.GotoNode(t))

		for i in range(0, len(bases)):
			for j in range(0, len(bases[i])):
				self.instructions.append(tunels[i][j])
				self.instructions.append(cil.CheckHierarchy(checkr, node.case_list[i + j + 1].variable.type, var))
				self.instructions.append(cil.GotoIfNode(checkr, labels[i + j + 1]))
				self.instructions.append(cil.GotoNode(bases[i][j]))

		var_ret = self.register_local_var()
		for i in range(len(ends)):
			self.instructions.append(ends[i])
			e = self.visit(node.case_list[i], var)
			self.instructions.append(cil.AssignNode(var_ret, e))
			self.instructions.append(cil.GotoNode(end))

		self.instructions.append(end)
		return var_ret
	
	@visitor.when(ast.CaseItemNode)
	def visit(self, node, expr):
		var = self.visit(node.variable)
		self.instructions.append(cil.AssignNode(var, expr))
		return self.visit(node.expr)

	@visitor.when(ast.DispatchNode)
	def visit(self, node):
		instructions = []
		var_ret = self.register_local_var()
		var_ret.type = node.type_expr
		instructions.append(cil.ArgumentNode(self.self_type))
		method = node.type_method
		n = len(node.params)
		
		for i in range(n):
			var = self.visit(node.params[i])		
			if (type(var) is not VarInfo and node.type_expr.name == "Object") \
			or (method.params_types[i] == "Object" and (var.type.name in ["Int", "Bool"])):
				temp = self.register_local_var()
				temp.type = self.types.get_type(method.params_types[i])
				self.instructions.append(cil.BoxingVariable(var, temp))
				var = temp
			instructions.append(cil.ArgumentNode(var))
		self.instructions += instructions
		self.instructions.append(cil.DinamicCallNode(self.current_type.name, node.id, var_ret))
		return var_ret

	@visitor.when(ast.DispatchInstanceNode)
	def visit(self, node):
		instructions = []
		var_ret = self.register_local_var()
		var_ret.type = node.type_expr
		instructions.append(cil.ArgumentNode(self.visit(node.variable)))
		method = node.type_method
		n = len(node.params)
		for i in range(n):
			var = self.visit(node.params[i])
			if (type(var) is not VarInfo and node.type_expr.name == "Object") \
			or (method.params_types[i] == "Object" and (var.type.name in ["Int", "Bool"])):
				temp = self.register_local_var()
				temp.type = self.types.get_type(method.params_types[i])
				self.instructions.append(cil.BoxingVariable(var, temp))
				var = temp
			instructions.append(cil.ArgumentNode(var))
		self.instructions += instructions
		self.instructions.append(cil.DinamicCallNode(node.variable.type_expr.name, node.id_method, var_ret))
		return var_ret
	
	@visitor.when(ast.DispatchParentInstanceNode)
	def visit(self, node):
		instructions = []
		var_ret = self.register_local_var()
		var_ret.type = node.type_expr
		instructions.append(cil.ArgumentNode(self.visit(node.variable)))
		method = self.types.get_type(node.id_parent).methods[node.id_method]
		n = len(node.params)
		for i in range(n):
			var = self.visit(node.params[i])
			if (type(var) is not VarInfo and node.type_expr.name == "Object") \
			or (method.params_types[i] == "Object" and (var.type.name in ["Int", "Bool"])):
				temp = self.register_local_var()
				temp.type = self.types.get_type(method.params_types[i])
				self.instructions.append(cil.BoxingVariable(var, temp))
				var = temp
			instructions.append(cil.ArgumentNode(var))
		self.instructions += instructions
		self.instructions.append(cil.StaticCallNode(node.id_parent, node.id_method, var_ret))
		return var_ret
	
	@visitor.when(ast.BlockNode)
	def visit(self, node):
		var = 0
		for expr in node.expr_list:
			var = self.visit(expr)
		if type(var) is VarInfo:
			var.type = node.type_expr
		return var

	@visitor.when(ast.PlusNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.PlusNode(var, left, right))
		return var

	@visitor.when(ast.MinusNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.MinusNode(var, left, right))
		return var

	@visitor.when(ast.StarNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.StarNode(var, left, right))
		return var

	@visitor.when(ast.DivNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.DivNode(var, left, right))
		return var
	
	@visitor.when(ast.NotNode)
	def visit(self, node):
		var = self.register_local_var()
		expr = self.visit(node.expr)
		self.instructions.append(cil.NotNode(var, expr))
		return var

	@visitor.when(ast.ComplementNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		expr = self.visit(node.expr)
		self.instructions.append(cil.ComplementNode(var, expr))
		return var
	
	@visitor.when(ast.IsVoidNode)
	def visit(self, node):
		var = self.register_local_var()
		expr = self.visit(node.expr)
		if type(expr) is not VarInfo or expr.type.name in ["Int", "String", "Bool"]:
			return 0
		self.instructions.append(cil.EqualNode(var, expr, 0))
		return var
	
	@visitor.when(ast.NewNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		new_class = self.types.get_type(node.type)
		self.instructions.append(cil.AllocateNode(var, new_class))
		temp_type = self.current_type
		temp_self = self.self_type
		self.self_type = var
		id_class = new_class
		while id_class:
			self.current_type = id_class
			for name, attrb in id_class.attrb.items():
				aux = None
				if not attrb.decl.expr:
					aux = self.register_local_var()
					aux.type = attrb.decl.type
				else:
					aux = self.visit(attrb.decl.expr)
				self.instructions.append(cil.SetAttrbNode(var, name, aux))
			id_class = id_class.inherits
		self.self_type = temp_self
		self.current_type = temp_type
		return var

	@visitor.when(ast.LessThanNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.LessThanNode(var, left, right))
		return var

	@visitor.when(ast.LessEqualNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.LessEqualNode(var, left, right))
		return var

	@visitor.when(ast.EqualNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		left = self.visit(node.left)
		right = self.visit(node.right)
		self.instructions.append(cil.EqualNode(var, left, right))
		return var

	@visitor.when(ast.VariableNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.var_info.type
		if node.var_info.name in self.current_type.attrb:
			self.instructions.append(cil.GetAttrbNode(var, self.self_type, node.id))
			return var
		else:
			return node.var_info
	
	@visitor.when(ast.IntegerNode)
	def visit(self, node):
		return node.integer

	@visitor.when(ast.StringNode)
	def visit(self, node):
		var = self.register_local_var()
		var.type = node.type_expr
		data = self.register_data(node.string)
		self.instructions.append(cil.LoadNode(var, data))
		return var

	@visitor.when(ast.BooleanNode)
	def visit(self, node):
		return node.value

	@visitor.when(ast.NegationNode)
	def visit(self, node):
		expr = self.visit(node.expr)
		if not type(expr) == int:
			var = self.register_local_var()
			var.type = node.type_expr
			self.instructions.append(cil.MinusNode(var, 0, expr))
			return var
		return -expr

class Type:
    def __init__(self, name, attrb, methods):
        self.name = name
        self.attrb = attrb
        self.methods = methods
        self.position = 0

class Method:
    def __init__(self, name):
        self.name = name
        self.position = 0

class PrimitiveMethods:
	def __init__(self):
		self.cil_node = {"type_name": cil.TypeOfNode,
							"abort" : cil.AbortNode,
							"substr": cil.SubStringNode,
							"length": cil.LengthNode,
							"concat": cil.ConcatNode,
							"in_string": cil.ReadStringNode,
							"in_int": cil.ReadIntegerNode,
							"out_string": cil.PrintStringNode,
							"out_int": cil.PrintIntegerNode}
		
		self.params = {"type_name": ["self"],
						"abort" : ["self"],
						"substr": ["self", "i", "l"],
						"length": ["self"],
						"concat": ["self", "str"],
						"in_string": [],
						"in_int": [],
						"out_string": ["self"],
						"out_int": ["self"]}