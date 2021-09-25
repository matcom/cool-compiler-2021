class Node:
    pass

class InstructionNode(Node):
    pass

class ErrorNode(InstructionNode):
    pass

class DataNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, conditional, label):
        self.conditional = conditional
        self.label = label

class ProgramNode(Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class MethodNode(Node):
    def __init__(self, name, params, local_vars, intructions):
        self.name = name
        self.params = params
        self.local_vars = local_vars
        self.intructions = intructions

class VarLocalNode(Node):
    def __init__(self, name):
        self.name = name
		
class AssignNode(InstructionNode):
    def __init__(self, destiny, source):
        self.destiny = destiny
        self.source = source

class GetAttrbNode(InstructionNode):
	def __init__(self, destiny, type, attrb):
		self.destiny = destiny
		self.type = type
		self.attrb = attrb
        
class SetAttrbNode(InstructionNode):
    def __init__(self, type, attrb, value):
        self.type = type
        self.attrb = attrb
        self.value = value

class AllocateNode(InstructionNode):
	def __init__(self, destiny, type):
		self.destiny = destiny
		self.type = type
		self.destiny.type = type

class ArithmeticNode(InstructionNode):
	def __init__(self, destiny, left, right):
		self.destiny = destiny
		self.left = left
		self.right = right

class LessEqualNode(ArithmeticNode):
    pass

class LessThanNode(ArithmeticNode):
    pass

class EqualNode(ArithmeticNode):
    pass

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class ComplementNode(InstructionNode):
	def __init__(self, destiny, expr):
		self.destiny = destiny
		self.expr = expr

class NotNode(InstructionNode):
	def __init__(self, destiny, expr):
		self.destiny = destiny
		self.expr = expr

class ArgumentNode(InstructionNode):
    def __init__(self, name):
        self.name = name
		
class DinamicCallNode(InstructionNode):
    def __init__(self, type, function, destiny):
        self.type = type
        self.function = function
        self.destiny = destiny

class StaticCallNode(InstructionNode):
    def __init__(self, type, function, destiny):
        self.type = type
        self.function = function
        self.destiny = destiny

class CheckHierarchy(InstructionNode):
    def __init__(self, destiny, type_A, type_B):
        self.destiny = destiny
        self.type_A = type_A
        self.type_B = type_B

class ReturnNode(InstructionNode):
    def __init__(self, value = None):
        self.value = value

class EndProgram(InstructionNode):
    def __init__(self, expr):
        self.expr = expr

#Object
class BoxingVariable(InstructionNode):
    def __init__(self, variable, destiny):
        self.variable = variable
        self.destiny = destiny

class UnboxingVariable(InstructionNode):
    def __init__(self, variable, destiny):
        self.variable = variable
        self.destiny = destiny

class TypeOfNode(InstructionNode):
    def __init__(self, src, destiny):
        self.src = src
        self.destiny = destiny
	
class AbortNode(InstructionNode):
    def __init__(self, self_type):
        self.self_type = self_type
			
#String
class LoadNode(InstructionNode):
    def __init__(self, destiny, msg):
        self.destiny = destiny
        self.msg = msg

class LengthNode(InstructionNode):
    def __init__(self, src, destiny):
        self.src = src
        self.destiny = destiny

class ConcatNode(InstructionNode):
    def __init__(self, str, src, destiny):
        self.str = str
        self.src = src
        self.destiny = destiny

class SubStringNode(InstructionNode):
	def __init__(self, src, a, b, destiny):
		self.src = src
		self.a = a
		self.b = b
		self.destiny = destiny

#IO
class ReadIntegerNode(InstructionNode):
	def __init__(self, destiny):
		self.destiny = destiny

class ReadStringNode(InstructionNode):
	def __init__(self, destiny):
		self.destiny = destiny

class PrintIntegerNode(InstructionNode):
	def __init__(self, src, str_addr):
		self.src = src
		self.str_addr = str_addr

class PrintStringNode(InstructionNode):
	def __init__(self, src, str_addr):
		self.src = src
		self.str_addr = str_addr