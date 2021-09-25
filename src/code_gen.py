import visitor
import cool_cil as cil

class CodeGen:
	def __init__(self):
		self.output = []
		self.arguments = []
		self.types = {}
		self.sp = 0
		self.gp = 0
		self.buffer = 0

	def write(self, text):
		if text is '\n':
			self.output.append(text)
		else:
			self.output.append(text + '\n')

	@visitor.on('node')
	def visit(self, node):
		pass

	@visitor.when(cil.DataNode)
	def visit(self, node):
		self.write('{}: .asciiz {}'.format(node.name, node.value))

	@visitor.when(cil.LabelNode)
	def visit(self, node):
		self.write('{}:'.format(node.name))

	@visitor.when(cil.GotoNode)
	def visit(self, node):
		self.write('    j {}'.format(node.label.name))

	@visitor.when(cil.GotoIfNode)
	def visit(self, node):
		if isinstance(node.conditional, int):
			self.write('    li $t0 {}'.format(node.conditional))
		elif isinstance(node.conditional, bool):
			if node.conditional:
				self.write('    li $t0, 1')
			else:
				self.write('    li $t0, 0')
		else:
			self.write('    lw $t0 {}($sp)'.format(node.conditional.holder + 4))
		self.write('    beq $t0, 1, {}'.format(node.label.name))

	@visitor.when(cil.ProgramNode)
	def visit(self, node, types):
		self.write('.data')
		for data in node.data:
			self.visit(data)
		self.write('\n')

		self.write('.text')
		self.write('    la $t0, ($gp)')
		
		for x in node.types:
			self.types[x.name] = x
			n = len(x.methods) * 4
			x.position = self.buffer
			self.buffer += 8 + n
			self.write('    la $t1, {}'.format(x.name))
			self.write('    sw $t1, 4($t0)')
			m = 0
			for name, method in x.methods.items():
				method.position = 8 + m
				m += 4
				self.write('    la $t2, {}'.format(method.name))
				self.write('    sw $t2, {}($t0)'.format(method.position))
			self.write('    add $t0, $t0, {}'.format(8 + n))

		self.write('    la $t0, ($gp)')
		self.write('    la $t2, ($gp)')
		for x in node.types:
			n = len(x.methods) * 4
			parent = types.get_parent_type(x.name)
			if parent:
				self.write('    li $t1, {}'.format(self.types[parent.name].position))
				self.write('    add $t1, $t1, $t2')   
			else:
				self.write('    li $t1, 0')
			self.write('    sw $t1, ($t0)')
			self.write('    add $t0, $t0, {}'.format(8 + n))
		self.write('    li $a0, 128')
		self.write('    li $v0, 9')
		self.write('    syscall')
		self.write('    sw $v0, {}($gp)'.format(self.buffer))

		for n in node.code:
			self.write('\n')
			self.visit(n)

		self.write('length:')
		self.write('    xor $t0, $t0, $t0') #letras
		self.write('    xor $t1, $t1, $t1') #cero
		self.write('    xor $v0, $v0, $v0') #result
		self.write('loop_length:')
		self.write('    lb $t0, ($a0)')
		self.write('    beq $t0, $t1, end_length')
		self.write('    addu $v0, $v0, 1')
		self.write('    addu $a0, $a0, 1')
		self.write('    j loop_length')
		self.write('end_length:')
		self.write('    jr $ra')

		self.write('concat:')
		self.write('    xor $t0, $t0, $t0')  # letras
		self.write('    xor $t1, $t1, $t1')  # cero
		self.write('loop_concat1:')
		self.write('    lb $t0, ($a0)')
		self.write('    beq $t0, $t1, concat2')
		self.write('    sb $t0, ($a2)')
		self.write('    add $a0, $a0, 1')
		self.write('    add $a2, $a2, 1')
		self.write('    j loop_concat1')
		self.write('    concat2:')
		self.write('loop_concat2:')
		self.write('    lb $t0, ($a1)')
		self.write('    beq $t0, $t1, end_concat')
		self.write('    sb $t0, ($a2)')
		self.write('    add $a1, $a1, 1')
		self.write('    add $a2, $a2, 1')
		self.write('    j loop_concat2')
		self.write('end_concat:')
		self.write('    sb $t1, ($a2)')
		self.write('    jr $ra')

		self.write('substring:')
		self.write('    xor $t1, $t1, $t1') #cero
		self.write('    add $a0, $a0, $a1')
		self.write('write_substring:')
		self.write('    lb $t0, ($a0)')
		self.write('    beq $a2, $t1, end_substring')
		self.write('    sb $t0, ($a3)')
		self.write('    add $a0, $a0, 1')
		self.write('    add $a3, $a3, 1')
		self.write('    subu $a2, $a2, 1')
		self.write('    j write_substring')
		self.write('end_substring:')
		self.write('    sb $t1, ($a3)')
		self.write('    jr $ra')

		self.write('check_hierarchy:')
		self.write('    la $t0, ($a0)')
		self.write('    la $t1, ($a1)')
		self.write('    xor $t2, $t2, $t2')
		self.write('    beq $t0, $t1, goodend_check_hierarchy')
		self.write('loop_check_hierarchy:')
		self.write('    lw $t1, ($t1)')
		self.write('    beq $t1, $t2, badend_check_hierarchy')
		self.write('    beq $t0, $t1, goodend_check_hierarchy')
		self.write('    j loop_check_hierarchy')
		self.write('badend_check_hierarchy:')
		self.write('    li $v0, 0')
		self.write('    jr $ra')
		self.write('goodend_check_hierarchy:')
		self.write('    li $v0, 1')
		self.write('    jr $ra')

		self.write('unboxing:')
		self.write('    lw $t0, 4($a0)')
		self.write('    beq $t0, 0, not_boxed')
		self.write('    ld $v0, ($t0)')
		self.write('    j end_unboxing')
		self.write('not_boxed:')
		self.write('    ld $v0, ($a0)')
		self.write('end_unboxing:')
		self.write('    jr $ra')

		self.write('error:')
		self.write('    break 0')

	@visitor.when(cil.MethodNode)
	def visit(self, node):
		self.sp = 0
		self.write('{}:'.format(node.name))
		sp = len(node.local_vars) * 8
		n = sp + (len(node.params) - 1) * 8
		for param in node.params:
			self.visit(param, n)
			n -= 8
		if node.params:
			self.write('\n')
		self.write('    subu $sp, $sp, {}'.format(sp))
		for vars in node.local_vars:
			self.visit(vars)
		if node.local_vars:
			self.write('\n')
		for intruction in node.intructions:
			self.visit(intruction)
		self.write('    addu $sp, $sp, {}'.format(sp))
		self.write('    jr $ra')

	@visitor.when(cil.ParamNode)
	def visit(self, node, n):
		node.name.holder = n
		
	@visitor.when(cil.VarLocalNode)
	def visit(self, node):
		node.name.holder = self.sp
		self.write('    li $t0, 0')
		self.write('    sw $t0, {}($sp)'.format(self.sp))
		self.write('    sw $t0, {}($sp)'.format(self.sp + 4))
		self.sp += 8

	@visitor.when(cil.AssignNode)
	def visit(self, node):
		if isinstance(node.source, int):
			self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
			self.write('    li $t1, {}'.format(node.source))
		elif isinstance(node.source, bool):
			self.write('    la $t0, {}($gp)'.format(self.types["Bool"].position))
			if node.source:
				self.write('    li $t1, 1')
			else:
				self.write('    li $t1, 0')
		else:
			self.write('    ld $t0, {}($sp)'.format(node.source.holder))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.GetAttrbNode)
	def visit(self, node):
		n = self.types[node.type.type.name].attrb.index(node.attrb) * 8
		self.write('    lw $t0, {}($sp)'.format(node.type.holder + 4))
		self.write('    ld $t1, {}($t0)'.format(n))
		self.write('    sd $t1, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.SetAttrbNode)
	def visit(self, node):
		n = self.types[node.type.type.name].attrb.index(node.attrb) * 8
		self.write('    lw $t0, {}($sp)'.format(node.type.holder + 4))
		if isinstance(node.value, int):
			self.write('    la $t1, {}($gp)'.format(self.types["Int"].position))
			self.write('    li $t2, {}'.format(node.value))
		elif isinstance(node.value, bool):
			self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
			if node.value:
				self.write('    li $t2, 1')
			else:
				self.write('    li $t2, 0')
		else:
			self.write('    ld $t1, {}($sp)'.format(node.value.holder))
		self.write('    sd $t1, {}($t0)'.format(n))

	@visitor.when(cil.AllocateNode)
	def visit(self, node):
		t = self.types[node.type.name]
		n = len(t.attrb) * 8
		self.write('    li $a0, {}'.format(n))
		self.write('    li $v0, 9')
		self.write('    syscall')
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))
		self.write('    la $t1, {}($gp)'.format(t.position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.LessEqualNode)
	def visit(self, node):
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		self.write('    sle $t0, $t1, $t2')
		self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.LessThanNode)
	def visit(self, node):
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))

		self.write('    slt $t0, $t1, $t2')
		self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.EqualNode)
	def visit(self, node):
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		elif isinstance(node.left, bool):
			if node.left:
				self.write('    li $t1, 1')
			else:
				self.write('    li $t1, 0')
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		elif isinstance(node.right, bool):
			if node.right:
				self.write('    li $t1, 1')
			else:
				self.write('    li $t1, 0')
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		self.write('    seq $t0, $t1, $t2')
		self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.PlusNode)
	def visit(self, node):
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		self.write('    add $t1, $t1, $t2')
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.MinusNode)
	def visit(self, node):
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		self.write('    sub $t1, $t1, $t2')
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.StarNode)
	def visit(self, node):
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		self.write('    mulo $t1, $t1, $t2')
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.DivNode)
	def visit(self, node):
		if isinstance(node.right, int):
			self.write('    li $t2, {}'.format(node.right))
		else:
			self.write('    lw $t2, {}($sp)'.format(node.right.holder + 4))
		if isinstance(node.left, int):
			self.write('    li $t1, {}'.format(node.left))
		else:
			self.write('    lw $t1, {}($sp)'.format(node.left.holder + 4))
		self.write('    div $t1, $t2')
		self.write('    mflo $t1')
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.ComplementNode)
	def visit(self, node):
		if isinstance(node.expr, int):
			self.write('    li $t0, {}'.format(node.expr))
		else:
			self.write('    lw $t0, {}($sp)'.format(node.expr.holder + 4))
		self.write('    not $t0, $t0')
		self.write('    la $t1, {}($gp)'.format(self.types["Int"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.NotNode)
	def visit(self, node):
		if isinstance(node.expr, int):
			self.write('    li $t0, {}'.format(node.expr))
		elif isinstance(node.expr, bool):
			if node.expr:
				self.write('    li $t0, 1')
			else:
				self.write('    li $t0, 0')
		else:
			self.write('    li $t0, {}'.format(node.expr.holder))
		self.write('    not $t0, $t0')
		self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.ArgumentNode)
	def visit(self, node):
		self.arguments.append(node.name)

	@visitor.when(cil.DinamicCallNode)
	def visit(self, node):
		method = self.types[node.type].methods[node.function].position
		n = len(self.arguments) * 8
		i = 8
		self.write('    lw $t2, {}($sp)'.format(self.arguments[0].holder))
		self.write('    subu $sp, $sp, {}'.format(n + 4))
		self.write('    sw $ra, {}($sp)'.format(n))
		for argument in self.arguments:
			if isinstance(argument, int):
				self.write('    li $t1, {}'.format(argument))
				self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
				self.write('    sd $t0, {}($sp)'.format(n - i))
			else:
				self.write('    ld $t0, {}($sp)'.format(n + 4 + argument.holder))
				self.write('    sd $t0, {}($sp)'.format(n - i))
			i += 8
		self.write('    lw $t0, {}($t2)'.format(method))
		self.write('    jalr $t0')
		self.write('    lw $ra, {}($sp)'.format(n))
		self.write('    addu $sp, $sp, {}'.format(n + 4))
		if isinstance(node.destiny, int):
			self.write('    sd $v0, {}($sp)'.format(node.destiny))
		else:
			self.write('    sd $v0, {}($sp)'.format(node.destiny.holder))
		self.arguments = []

	@visitor.when(cil.StaticCallNode)
	def visit(self, node):
		n = len(self.arguments) * 8
		i = 8
		self.write('    subu $sp, $sp, {}'.format(n + 4))
		self.write('    sw $ra, {}($sp)'.format(n))
		for argument in self.arguments:
			if isinstance(argument, int):
				self.write('    li $t0, {}'.format(argument))
				self.write('    la $t1, {}($gp)'.format(self.types["Int"].position))
				self.write('    sd $t0, {}($sp)'.format(n - i + 4))
			elif isinstance(argument, bool):
				if argument:
					self.write('    li $t0, 1')
				else:
					self.write('    li $t0, 0')
				self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
				self.write('    sd $t0, {}($sp)'.format(n - i + 4))
			else:
				self.write('    ld $t0, {}($sp)'.format(n + 4 + argument.holder))
				self.write('    sd $t0, {}($sp)'.format(n - i))
			i += 8
		self.write('    jal {}_{}'.format(node.type, node.function))
		self.write('    lw $ra, {}($sp)'.format(n))
		self.write('    addu $sp, $sp, {}'.format(n + 4))
		self.write('    sd $v0, {}($sp)'.format(node.destiny.holder))
		self.arguments = []

	@visitor.when(cil.CheckHierarchy)
	def visit(self, node):
		self.write('    la $a0, {}($gp)'.format(self.types[node.type_A.name].position))
		if type(node.type_B) == int:
			self.write('    la $a1, {}($gp)'.format(self.types["Int"].position))
		elif type(node.type_B) == bool:
			self.write('    la $a1, {}($gp)'.format(self.types["Bool"].position))
		else:
			self.write('    lw $a1, {}($sp)'.format(node.type_B.holder))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal check_hierarchy')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    la $t1, {}($gp)'.format(self.types["Bool"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.ReturnNode)
	def visit(self, node):
		if isinstance(node.value, int):
			self.write('    la $v0, {}($gp)'.format(self.types["Int"].position))
			self.write('    li $v1, {}'.format(node.value))
		elif isinstance(node.value, bool):
			self.write('    la $v0, {}($gp)'.format(self.types["Bool"].position))
			if node.value:
				self.write('    li $v1, 1')
			else:
				self.write('    li $v1, 0')
		else:
			self.write('    ld $v0, {}($sp)'.format(node.value.holder))

	@visitor.when(cil.EndProgram)
	def visit(self, node):
		self.write('    li $v0, 10')
		self.write('    xor $a0, $a0, $a0')
		self.write('    syscall')

#Object
	@visitor.when(cil.BoxingVariable)
	def visit(self, node):
		self.write('    li $v0, 9')
		self.write('    li $a0, 8')
		self.write('    syscall')
		self.write('    la $t0, {}($gp)'.format(self.types["Object"].position))
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder))
		if isinstance(node.variable, int):
			self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
			self.write('    li $t1, {}'.format(node.variable))
		elif isinstance(node.variable, bool):
			self.write('    la $t0, {}($gp)'.format(self.types["Bool"].position))
			if node.variable:
				self.write('    li $t1, 1')
			else:
				self.write('    li $t1, 0')
		else:
			self.write('    ld $t0, {}($sp)'.format(node.variable.holder))
		self.write('    sd $t0, ($v0)')

	@visitor.when(cil.UnboxingVariable)
	def visit(self, node):
		self.write('    la $a0, {}($sp)'.format(node.variable.holder))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal unboxing')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    sd $v0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.TypeOfNode)
	def visit(self, node):
		self.write('    lw $t1, {}($sp)'.format(node.src.holder))
		self.write('    lw $t1, 4($t1)')
		self.write('    la $t0, {}($gp)'.format(self.types["String"].position))
		self.write('    sd $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.AbortNode)
	def visit(self, node):
		self.write('    li $v0, 10')
		self.write('    xor $a0, $a0, $a0')
		self.write('    syscall')

#String
	@visitor.when(cil.LoadNode)
	def visit(self, node):
		self.write('    la $t0, {}'.format(node.msg.name))
		self.write('    la $t1, {}($gp)'.format(self.types["String"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.LengthNode)
	def visit(self, node):
		self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal length')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.ConcatNode)
	def visit(self, node):
		self.write('    lw $a0, {}($sp)'.format(node.str.holder + 4))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal length')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    la $t0, ($v0)')
		self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('    subu $sp, $sp, 8')
		self.write('    sw $ra, 4($sp)')
		self.write('    sw $t0, ($sp)')
		self.write('    jal length')
		self.write('    lw $t0, ($sp)')
		self.write('    lw $ra, 4($sp)')
		self.write('    addu $sp, $sp, 8')
		self.write('    la $a0, ($v0)')
		self.write('    addu $a0, $a0, $t0')
		self.write('    addu $a0, $a0, 1')
		self.write('    li $v0, 9')
		self.write('    syscall')
		self.write('    la $a2, ($v0)')
		self.write('    lw $a0, {}($sp)'.format(node.str.holder + 4))
		self.write('    lw $a1, {}($sp)'.format(node.src.holder + 4))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal concat')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    la $t0, {}($gp)'.format(self.types["String"].position))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder))
		self.write('    sw  $v0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.SubStringNode)
	def visit(self, node):
		self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal length')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    lw $t0, {}($sp)'.format(node.a.holder + 4))
		self.write('    blt $t0, 0, error')
		self.write('    lw $t1, {}($sp)'.format(node.b.holder + 4))
		self.write('    blt $t1, 0, error')
		self.write('    add $t0, $t0, $t1')
		self.write('    blt $v0, $t0, error')
		self.write('    li $v0, 9')
		self.write('    lw $a0, {}($sp)'.format(node.b.holder + 4))
		self.write('    add $a0, $a0, 1')
		self.write('    syscall')
		self.write('    la $a3, ($v0)')
		self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('    lw $a1, {}($sp)'.format(node.a.holder + 4))
		self.write('    lw $a2, {}($sp)'.format(node.b.holder + 4))
		self.write('    subu $sp, $sp, 4')
		self.write('    sw $ra, ($sp)')
		self.write('    jal substring')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 4')
		self.write('    la $t1, {}($gp)'.format(self.types["String"].position))
		self.write('    sw $t1, {}($sp)'.format(node.destiny.holder))
		self.write('    sw  $v0, {}($sp)'.format(node.destiny.holder + 4))

#IO
	@visitor.when(cil.ReadIntegerNode)
	def visit(self, node):
		self.write('    li $v0, 5')
		self.write('    syscall')
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))
		self.write('    la $t0, {}($gp)'.format(self.types["Int"].position))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder))

	@visitor.when(cil.ReadStringNode)
	def visit(self, node):
		self.write('    lw $a0, {}($gp)'.format(self.buffer))
		self.write('    li $a1, 128')
		self.write('    li $v0, 8')
		self.write('    syscall')
		self.write('    subu $sp, $sp, 8')
		self.write('    sw $ra, 4($sp)')
		self.write('    sw $a0, ($sp)')
		self.write('    jal length')
		self.write('    lw $a0, ($sp)')
		self.write('    lw $ra, 4($sp)')
		self.write('    addu $sp, $sp, 8')
		self.write('    la $t0, ($a0)')
		self.write('    la $t1, ($v0)')
		self.write('    la $a0, ($v0)')
		self.write('    li $v0, 9')
		self.write('    syscall')
		self.write('    la $a0, ($t0)')
		self.write('    li $a1, 0')
		self.write('    la $a2, ($t1)')
		self.write('    la $a3, ($v0)')
		self.write('    subu $sp, $sp, 8')
		self.write('    sw $ra, ($sp)')
		self.write('    jal substring')
		self.write('    lw $ra, ($sp)')
		self.write('    addu $sp, $sp, 8')
		self.write('    la $t0, {}($gp)'.format(self.types["String"].position))
		self.write('    sw $t0, {}($sp)'.format(node.destiny.holder))
		self.write('    sw $v0, {}($sp)'.format(node.destiny.holder + 4))

	@visitor.when(cil.PrintIntegerNode)
	def visit(self, node):
		self.write('    li $v0, 1')
		if isinstance(node.src, int):
			self.write('    li $a0, {}'.format(node.src))
		else:
			self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('syscall')
		self.write('    ld $v0, {}($sp)'.format(node.str_addr.holder))

	@visitor.when(cil.PrintStringNode)
	def visit(self, node):
		self.write('    li $v0, 4')
		self.write('    lw $a0, {}($sp)'.format(node.src.holder + 4))
		self.write('syscall')
		self.write('    ld $v0, {}($sp)'.format(node.str_addr.holder))

	@visitor.when(cil.ErrorNode)
	def visit(self, node):
		self.write('    j error')
