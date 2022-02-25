class Node:
    pass


class Program(Node):
    def __init__(self):
        self.type_section = []
        self.data_section = {}
        self.code_section = []


class Type(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []


class Data(Node):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value


class Function(Node):
    def __init__(self, fun_name):
        self.fun_name = fun_name
        self.params = []
        self.local_vars = []
        self.instructions = []


class Instruction(Node):
    pass


class Assign(Instruction):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value


class Arithmetic(Instruction):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class Plus(Arithmetic):
    pass


class Minus(Arithmetic):
    pass


class Star(Arithmetic):
    pass


class Div(Arithmetic):
    pass


# Attribute Access
class GetAttr(Instruction):
    def __init__(self, dest, type_instance_address, attribute_position):
        self.dest = dest
        self.type_instance_address = type_instance_address
        self.attribute_position = attribute_position


class SetAttr(Instruction):
    def __init__(self, type_instance_address, attribute_position, value):
        self.value = value
        self.type_instance_address = type_instance_address
        self.attribute_position = attribute_position


# Array Access
class GetIndex(Instruction):
    def __init__(self, dest, direction, index):
        self.dest = dest
        self.direction = direction
        self.index = index


class SetIndex(Instruction):
    def __init__(self, value, direction, index):
        self.value = value
        self.direction = direction
        self.index = index


# Memory Manipulation
class Allocate(Instruction):
    def __init__(self, destiny, _type):
        self.destiny = destiny
        self.type = _type


class TypeOf(Instruction):
    def __init__(self, destiny, var):
        self.destiny = destiny
        self.var = var


class Array(Instruction):
    def __init__(self, name, size):
        self.name = name
        self.size = size


# Method Invocation
class Call(Instruction):
    def __init__(self, destiny, function_name):
        self.destiny = destiny
        self.function_name = function_name


class DynamicCall(Instruction):
    def __init__(self, destiny, type_name, function_name):
        self.destiny = destiny
        self.type_name = type_name
        self.func_name = function_name


class Arg(Instruction):
    def __init__(self, arg):
        self.arg = arg


# Jumps
class IfGoto(Instruction):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label


class Label(Instruction):
    def __init__(self, name):
        self.name = name


class Goto(Instruction):
    def __init__(self, label_name):
        self.label_name = label_name


# Function Return
class Return(Instruction):
    def __init__(self, value=None):
        self.value = value


# String Functions
class Load(Instruction):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class Length(Instruction):
    def __init__(self, dest, str_address):
        self.dest = dest
        self.str_address = str_address


class Concat(Instruction):
    def __init__(self, dest, head1, head2):
        self.dest = dest
        self.head1 = head1
        self.head2 = head2


class Substring(Instruction):
    def __init__(self, dest, str_addr, pos, length):
        self.dest = dest
        self.str_addr = str_addr
        self.pos = pos
        self.length = length


class Str(Instruction):
    def __init__(self, dest, numeric_value):
        self.dest = dest
        self.numeric_value = numeric_value


# IO Operations
class Read(Instruction):
    def __init__(self, dest):
        self.dest = dest


class Print(Instruction):
    def __init__(self, str_address):
        self.str_address = str_address
