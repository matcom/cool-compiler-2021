class AST:
    def __init__(self):
        pass

    def __repr__(self):
        return str(self)


class Program(AST):
    def __init__(self, dottypes, dotdata, dotcode):
        super(Program, self).__init__()
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class Type(AST):
    def __init__(self, name):
        super(Type, self).__init__()
        self.name = name
        self.attributes = []
        self.methods = {}


class Function(AST):
    def __init__(self, name, params=[], localvars=[], instructions=[]):
        super(Function, self).__init__()
        self.name = name
        self.params = params
        self.localvars = localvars
        self.instructions = instructions


class Expr(AST):
    def __init__(self):
        super(Expr, self).__init__()


class ParamDec(Expr):
    def __init__(self, name):
        super(ParamDec, self).__init__()
        self.name = name


class LocalDec(Expr):
    def __init__(self, name):
        super(LocalDec, self).__init__()
        self.name = name


class Halt(Expr):
    def __init__(self):
        super(Halt, self).__init__()


class GetAttr(Expr):
    def __init__(self, dest, instance, attr, static_type):
        self.local_dest = dest
        self.instance = instance
        self.attr = attr
        self.static_type = static_type


class SetAttr(Expr):
    def __init__(self, instance, attr, value, static_type):
        self.instance = instance
        self.attr = attr
        self.value = value
        self.static_type = static_type


class Call(Expr):
    def __init__(self, local_dest, function, params, static_type):
        self.function = function
        self.params = params
        self.static_type = static_type
        self.local_dest = local_dest


class VCall(Expr):
    def __init__(self, local_dest, function, params, dynamic_type, instance):
        self.function = function
        self.params = params
        self.dynamic_type = dynamic_type
        self.local_dest = local_dest
        self.instance = instance


class INTEGER(Expr):
    def __init__(self, value):
        super(INTEGER, self).__init__()
        self.value = value


class STRING(Expr):
    def __init__(self, value):
        super(STRING, self).__init__()
        self.value = value


class Assign(Expr):
    def __init__(self, local_dest, right_expr):
        self.local_dest = local_dest
        self.right_expr = right_expr


class UnaryOperator(Expr):
    def __init__(self, local_dest, expr_value, op):
        self.local_dest = local_dest
        self.expr_value = expr_value
        self.op = op


class BinaryOperator(Expr):
    def __init__(self, local_dest, left, right, op):
        self.local_dest = local_dest
        self.left = left
        self.right = right
        self.op = op


class Allocate(Expr):
    def __init__(self, t, tag, dest):
        self.type = t
        self.local_dest = dest
        self.tag = tag


class TypeOf(Expr):
    def __init__(self, variable, local_dest):
        self.variable = variable
        self.local_dest = local_dest


class Param(Expr):
    def __init__(self, param, shift=0):
        self.param = param
        self.shift = shift


class Arg(Expr):
    def __init__(self, arg):
        self.arg = arg


class Case(Expr):
    def __init__(self, local_expr, first_label):
        self.local_expr = local_expr
        self.first_label = first_label


class Action(Expr):
    def __init__(self, local_expr, tag, max_tag, next_label):
        self.local_expr = local_expr
        self.tag = tag
        self.max_tag = max_tag
        self.next_label = next_label


class IfGoto(Expr):
    def __init__(self, variable, label):
        self.variable = variable
        self.label = label


class Goto(Expr):
    def __init__(self, label):
        self.label = label


class Label(Expr):
    def __init__(self, label):
        self.label = label


class Return(Expr):
    def __init__(self, value):
        self.value = value


class LoadInt(Expr):
    def __init__(self, num, dest):
        self.num = num
        self.local_dest = dest


class LoadStr(Expr):
    def __init__(self, msg, dest):
        self.msg = msg
        self.local_dest = dest


class LoadVoid(Expr):
    def __init__(self, dest):
        self.local_dest = dest


class Length(Expr):
    def __init__(self, variable, result):
        self.variable = variable
        self.result = result


class Concat(Expr):
    def __init__(self, str1, len1, str2, len2, result):
        self.str1 = str1
        self.len1 = len1
        self.str2 = str2
        self.len2 = len2
        self.result = result


class StringVar(Expr):
    def __init__(self, variable):
        self.variable = variable


class SubStr(Expr):
    def __init__(self, i, length, string, result):
        self.i = i
        self.length = length
        self.string = string
        self.result = result


class StringEquals(Expr):
    def __init__(self, s1, s2, result):
        self.s1 = s1
        self.s2 = s2
        self.result = result


class Read(Expr):
    def __init__(self, result):
        self.result = result


class ReadString(Read):
    pass


class ReadInteger(Read):
    pass


class Print(Expr):
    def __init__(self, variable):
        self.variable = variable


class PrintString(Print):
    pass


class PrintInteger(Print):
    pass


class IsVoid(Expr):
    def __init__(self, result_local, expre_value):
        self.result_local = result_local
        self.expre_value = expre_value


class Copy(Expr):
    def __init__(self, type, local_dest):
        self.type = type
        self.local_dest = local_dest

