from ..tools import visitor

class Node:
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode, line, column):
        super().__init__(line,column)
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name
        self.attributes = {}
        self.methods = {}

class DataNode(Node):
    def __init__(self, vname, value, line, column):
        super().__init__(line, column)
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, line, column):
        super().__init__(line, column)
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.labels_count = 0

class LocalNode(Node):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.source = source

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode):
    pass

class MinusNode(ArithmeticNode):
    pass

class StarNode(ArithmeticNode):
    pass

class DivNode(ArithmeticNode):
    pass

class LessNode(ArithmeticNode):
    pass

class EqualNode(ArithmeticNode):
    pass

class EqualStringNode(ArithmeticNode):
    pass

class LessEqualNode(ArithmeticNode):
    pass

class GetAttribNode(InstructionNode):
    def __init__(self, dest, obj, attr, computed_type, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.obj = obj
        self.attr = attr
        self.computed_type = computed_type

    def __repr__(self):
        return f"{self.dest} = GETATTR {self.obj} {self.attr}"


class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, value, computed_type, line, column):
        super().__init__(line, column)
        self.obj = obj
        self.attr = attr
        self.value = value
        self.computed_type = computed_type

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest, line, column):
        super().__init__(line, column)
        self.type = itype
        self.dest = dest

class TypeOfNode(InstructionNode):
    def __init__(self, dest, obj, line, column):
        super().__init__(line, column)
        self.obj = obj
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = TYPEOF {self.obj}"


class LabelNode(InstructionNode):
    def __init__(self, label, line, column):
        super().__init__(line, column)
        self.label = label

    def __repr__(self):
        return f"LABEL {self.label}:"


class GotoNode(InstructionNode):
    def __init__(self, label, line, column):
        super().__init__(line, column)
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label}"


class GotoIfNode(InstructionNode):
    def __init__(self, condition, label, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label} if {self.condition}"

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest, line, column):
        super().__init__(line, column)
        self.function = function
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = CALL {self.function}"

class DynamicCallNode(InstructionNode):
    def __init__(self, type,  method, dest, line, column):
        super().__init__(line, column)
        self.type = type
        self.method = method
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = VCALL {self.type} {self.method}"

class ArgNode(InstructionNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

    def __repr__(self):
        return f"ARG {self.name}"


class ReturnNode(InstructionNode):
    def __init__(self, line, column, value=None):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"RETURN {self.value}"


class LoadNode(InstructionNode):
    def __init__(self, dest, msg, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.msg = msg

    def __repr__(self):
        return f"{self.dest} LOAD {self.msg}"

class LengthNode(InstructionNode):
    def __init__(self, dest, source, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.source = source

class ConcatNode(InstructionNode):
    def __init__(self, dest, prefix, suffix, length, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.prefix = prefix
        self.suffix = suffix
        self.length = length

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    def __init__(self, dest, str_value, index, length, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.str_value = str_value
        self.index = index
        self.length = length

class ToStrNode(InstructionNode):
    def __init__(self, dest, value, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.value = value

class ReadStringNode(InstructionNode):
    def __init__(self, dest, line, column):
        super().__init__(line, column)
        self.dest = dest

class ReadIntNode(InstructionNode):
    def __init__(self, dest, line, column):
        super().__init__(line, column)
        self.dest = dest

class PrintStringNode(InstructionNode):
    def __init__(self, str_addr, line, column):
        super().__init__(line, column)
        self.str_addr = str_addr

class PrintIntNode(InstructionNode):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

class ExitNode(InstructionNode):
    pass

class CopyNode(InstructionNode):
    def __init__(self, dest, value, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.value = value

class ErrorNode(InstructionNode):
    def __init__(self, data, line, column):
        super().__init__(line, column)
        self.data = data

class VoidNode(InstructionNode):
    def __str__(self):
        return 'VOID'

class NameNode(InstructionNode):
    def __init__(self, dest, value, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.value = value

class NotNode(InstructionNode):
    def __init__(self, dest, value, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.value = value

class ComplementNode(InstructionNode):
    def __init__(self, dest, value, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.value = value

class VarNode(InstructionNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

    def __str__(self):
        return f'{self.name}'

class AttributeNode(VarNode):
    def __init__(self, name, type, line, column):
        super().__init__(name, line, column)
        self.type = type

    def __str__(self):
        return f'{self.type}.{self.name}'

class ParamNode(VarNode):
    def __init__(self, name, line, column):
        super().__init__(name, line, column)

    def __str__(self):
        return f'PARAM {self.name}'