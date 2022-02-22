class Node:
    pass


class Program(Node):
    def __init__(self):
        self.type_section = []
        self.data_section = {}  # data[string] = tag
        self.code_section = []


class Type(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = {}


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
    def __init__(self, dest, _type, source):
        self.dest = dest
        self.type = _type
        self.source = source


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


class GetAttr(Instruction):
    def __init__(self, dest, instance, attribute):
        self.dest = dest
        self.instance = instance  # local con la direccion en memoria
        self.attribute = attribute  # indice del atributo(contando los heredados)


class SetAttr(Instruction):
    def __init__(self, instance, attribute, src):
        self.instance = instance  # local con la direccion en memoria
        self.attribute = attribute  # indice del atributo
        self.value = src


class GetIndex(Instruction):
    def __init__(self, destiny, direction, index):
        self.destiny = destiny
        self.direction = direction
        self.index = index


class SetIndex(Instruction):
    def __init__(self, value, direction, index):
        self.value = value
        self.direction = direction
        self.index = index


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
    def __init__(self, arg_info):
        self.arg_info = arg_info


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


class Return(Instruction):
    def __init__(self, value=None):
        self.value = value


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


class ToStr(Instruction):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class Copy(Instruction):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class GetParent(Instruction):
    def __init__(self, dest, instance, array, length):
        self.dest = dest
        self.instance = instance  # local con la direccion en memoria
        self.array_name = array  # indice del atributo(contando los heredados)
        self.length = length

    def to_string(self):
        return "{} = GETPARENT {} {}".format(self.dest, self.instance, self.array_name)


class ReadStr(Instruction):
    def __init__(self, dest):
        self.dest = dest

    def to_string(self):
        return "{} = READ".format(self.dest)


class ReadInt(Instruction):
    def __init__(self, dest):
        self.dest = dest

    def to_string(self):
        return "{} = READ".format(self.dest)


class PrintStr(Instruction):
    def __init__(self, str_addr):
        self.str_addr = str_addr

    def to_string(self):
        return "PRINT {}".format(self.str_addr)


class PrintInt(Instruction):
    def __init__(self, value):
        self.value = value

    def to_string(self):
        return "PRINT {}".format(self.value)


class EndProgram(Instruction):
    def __init__(self):
        pass

    def to_string(self):
        return "PROGRAM END WITH ERROR"


class IsVoid(Instruction):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj


class LowerThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.dest = dest
        self.left = left_expr
        self.right = right_expr

    def to_string(self):
        return "{} <- {} < {}".format(self.dest, self.left, self.right)


class LowerEqualThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.dest = dest
        self.left = left_expr
        self.right = right_expr

    def to_string(self):
        return "{} <- {} <= {}".format(self.dest, self.left, self.right)


class EqualThan(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.dest = dest
        self.left = left_expr
        self.right = right_expr

    def to_string(self):
        return "{} <- {} == {}".format(self.dest, self.left, self.right)


class Exit(Instruction):
    def __init__(self):
        pass

    def to_string(self):
        return "Exit"


class EqualStrThanStr(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.dest = dest
        self.left = left_expr
        self.right = right_expr

    def to_string(self):
        return "{} <- {} == {}".format(self.dest, self.left, self.right)
