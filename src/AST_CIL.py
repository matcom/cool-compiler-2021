class Node:
    pass

class Program(Node):
    def __init__(self):
        self.type_section = []
        self.data_section = {} #data[string] = tag
        self.code_section = []

class Type(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = {}
    def to_string(self):
        return "type {} \n attributes {}\n methods {}\n".format(self.name, self.attributes, self.methods)

class Data(Node):
    def __init__(self, vname, value):
        self.vname = vname
        self.value = value




class Function(Node):
    def __init__(self, fname):
        self.fname = fname
        self.params = []
        self.localvars = []
        self.instructions = []

class Instruction(Node):
    pass

class Assign(Instruction):
    def __init__(self, dest, _type, source):
        self.dest = dest
        self.type = _type
        self.source = source
    def to_string(self):
        return "{} <- {}".format(self.dest, self.source)

class Arithmetic(Instruction):
    pass

class Plus(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} + {}".format(self.dest, self.left, self.right)

class Minus(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} - {}".format(self.dest, self.left, self.right)

class Star(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} * {}".format(self.dest, self.left, self.right)
    
class Div(Arithmetic):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right
    def to_string(self):
        return "{} = {} / {}".format(self.dest, self.left, self.right)

class GetAttrib(Instruction):
    def __init__(self, dest, instance, attribute):
        self.dest = dest
        self.instance = instance    #local con la direccion en memoria
        self.attribute = attribute  #indice del atributo(contando los heredados)
    def to_string(self):
        return "{} = GETATTR {} {}".format(self.dest, self.instance, self.attribute)

class SetAttrib(Instruction):
    def __init__(self, instance, attribute, src):
        self.instance = instance    #local con la direccion en memoria
        self.attribute = attribute  #indice del atributo
        self.value = src
    def to_string(self):
        return "SETATTR {} {} {}".format(self.instance, self.attribute, self.value)

class Allocate(Instruction):
    def __init__(self, dest, ttype):
        self.dest = dest
        self.ttype = ttype

    def to_string(self):
        return "{} = ALLOCATE {}".format(self.dest, self.ttype)

class Array(Instruction):
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

class TypeOf(Instruction):
    def __init__(self, dest, var):
        self.dest = dest
        self.var = var
    def to_string(self):
        return "{} = TYPEOF {}".format(self.dest, self.var)

class Label(Instruction):
    def __init__(self, name):
        self.name = name
    
    def to_string(self):
        return "LABEL {}".format(self.name)

class Goto(Instruction):
    def __init__(self, name):
        self.name = name    
    
    def to_string(self):
        return "GOTO {}".format(self.name)

class GotoIf(Instruction):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label
    def to_string(self):
        return "IF {} GOTO {}".format(self.condition, self.label)

class Call(Instruction):
    def __init__(self, dest, func):
        self.dest = dest
        self.func = func

    def to_string(self):
        return "{} = CALL {}".format(self.dest, self.func)

class Dynamic_Call(Instruction):
    def __init__(self, dest, ttype, func, left):
        self.dest = dest
        self.ttype = ttype
        self.func = func
        self.left = left
    def to_string(self):
        return "{} = VCALL {} {}".format(self.dest, self.ttype, self.func)

class Arg(Instruction):
    def __init__(self, vinfo):
        self.vinfo = vinfo
    def to_string(self):
        return "ARG {}".format(self.vinfo)

class Return(Instruction):
    def __init__(self, value=None):
        self.value = value

    def to_string(self):
        return "RETURN {}".format(self.value)

class Load(Instruction):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg
    def to_string(self):
        return "{} = LOAD {}".format(self.dest, self.msg)

class Length(Instruction):
    def __init__(self, dest, str_addr):
        self.dest = dest
        self.str_addr = str_addr
    def to_string(self):
        return "{} = LENGTH {}".format(self.dest, self.str_addr)

class Concat(Instruction):
    def __init__(self, dest, head, tail):
        self.dest = dest
        self.head = head
        self.tail = tail
    
    def to_string(self):
        return "{} = CONCAT {} {}".format(self.dest, self.head, self.tail)

class Prefix(Instruction):
    def __init__(self, dest, str_addr, pos):
        self.dest = dest
        self.str_addr = str_addr
        self.pos = pos

class Substring(Instruction):
    def __init__(self, dest, str_addr, pos, length):
        self.dest = dest
        self.str_addr = str_addr
        self.pos = pos
        self.length = length
    def to_string(self):
        return "{} = Substring {} {} {}".format(self.dest, self.str_addr, self.pos, self.length)

class ToStr(Instruction):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

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
        return 'Exit'

class EqualStrThanStr(Instruction):
    def __init__(self, dest, left_expr, right_expr):
        self.dest = dest
        self.left = left_expr
        self.right = right_expr
    def to_string(self):
        return "{} <- {} == {}".format(self.dest, self.left, self.right)