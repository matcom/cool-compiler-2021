import cmp.visitor as visitor


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []


class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions


class ParamNode(Node):
    def __init__(self, name):
        self.name = name


class LocalNode(Node):
    def __init__(self, name):
        self.name = name


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ArithmeticNode(InstructionNode):
    def __init__(
        self,
        dest,
        left,
        right,
    ):
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


class LessEqualNode(ArithmeticNode):
    pass


class EqualNode(ArithmeticNode):
    pass


class UnaryNode(InstructionNode):
    def __init__(self, dest, expr):
        self.dest = dest
        self.expr = expr


class NotNode(UnaryNode):
    pass


class IntComplementNode(UnaryNode):
    def __init__(self, dest, source):
        self.source = source
        self.dest = dest


class GetAttribNode(InstructionNode):
    def __init__(self, dest, instance, attr, typex):
        self.dest = dest
        self.instance = instance
        self.attr = attr
        self.type = typex


class SetAttribNode(InstructionNode):
    def __init__(self, instance, attr, value, typex):
        self.instance = instance
        self.value = value
        self.attr = attr
        self.type = typex


class ArrayNode(InstructionNode):
    pass


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class GotoIfNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, instance_type, method_index, dest):
        self.instance_type = instance_type
        self.method_index = method_index
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ConcatNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    def __init__(self, dest, source, idx, length):
        self.dest = dest
        self.source = source
        self.id = idx
        self.length = length


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class RuntimeErrorNode(InstructionNode):
    def __init__(self, signal):
        self.signal = signal


class CopyNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class PrintStrNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class PrintIntNode(InstructionNode):
    def __init__(self, int_addr):
        self.int_addr = int_addr


class TypeNameNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class DefaultValueNode(InstructionNode):
    def __init__(self, dest, typex):
        self.dest = dest
        self.type = typex


class IsVoidNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
        
class ExitNode(InstructionNode):
    def __init__(self):
        pass
        


class PrintVisitor(object):
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        dottypes = "\n".join(self.visit(t) for t in node.dottypes)
        dotdata = "\n".join(self.visit(t) for t in node.dotdata)
        dotcode = "\n".join(self.visit(t) for t in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @visitor.when(TypeNode)
    def visit(self, node):
        attributes = "\n\t".join(f"attribute {x}" for x in node.attributes)
        methods = "\n\t".join(f"method {x}: {y}" for x, y in node.methods)

        return f"type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}"

    @visitor.when(FunctionNode)
    def visit(self, node):
        params = "\n\t".join(self.visit(x) for x in node.params)
        localvars = "\n\t".join(self.visit(x) for x in node.localvars)
        instructions = "\n\t".join(self.visit(x) for x in node.instructions)

        return f"function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}"

    @visitor.when(DataNode)
    def visit(self, node):
        return f'{node.name} = "{node.value}"'

    @visitor.when(ParamNode)
    def visit(self, node):
        return f"PARAM {node.name}"

    @visitor.when(LocalNode)
    def visit(self, node):
        return f"LOCAL {node.name}"

    @visitor.when(AssignNode)
    def visit(self, node):
        return f"{node.dest} <- {node.source}"

    @visitor.when(PlusNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} + {node.right}"

    @visitor.when(MinusNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} - {node.right}"

    @visitor.when(StarNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} * {node.right}"

    @visitor.when(DivNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} / {node.right}"

    @visitor.when(LessNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} < {node.right}"

    @visitor.when(LessEqualNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} <= {node.right}"

    @visitor.when(EqualNode)
    def visit(self, node):
        return f"{node.dest} = {node.left} == {node.right}"

    @visitor.when(NotNode)
    def visit(self, node):
        return f"{node.dest} = NOT {node.expr}"

    @visitor.when(IntComplementNode)
    def visit(self, node):
        return f"{node.dest} = ~ {node.expr}"

    @visitor.when(LabelNode)
    def visit(self, node):
        return f"LABEL {node.name}"

    @visitor.when(GotoNode)
    def visit(self, node):
        return f"GOTO {node.label}"

    @visitor.when(GotoIfNode)
    def visit(self, node):
        return f"IF {node.condition} GOTO {node.label}"

    @visitor.when(AllocateNode)
    def visit(self, node):
        return f"{node.dest} = ALLOCATE {node.type}"

    @visitor.when(SetAttribNode)
    def visit(self, node):
        return f" SETATTR {node.type} {node.attr} {node.value}"

    @visitor.when(GetAttribNode)
    def visit(self, node):
        return f" {node.dest} = GETATTR {node.type} {node.attr}"

    @visitor.when(TypeOfNode)
    def visit(self, node):
        return f"{node.dest} = TYPEOF {node.obj}"

    @visitor.when(StaticCallNode)
    def visit(self, node):
        return f"{node.dest} = CALL {node.function}"

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        return f"{node.dest} = VCALL {node.instance_type} {node.method_index}"

    @visitor.when(ArgNode)
    def visit(self, node):
        return f"ARG {node.name}"

    @visitor.when(ReturnNode)
    def visit(self, node):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(RuntimeErrorNode)
    def visit(self, node):
        return f"ABORT {node.signal}"

    @visitor.when(CopyNode)
    def visit(self, node):
        return f"{node.dest} = COPY {node.source}"

    @visitor.when(TypeNameNode)
    def visit(self, node):
        return f"{node.dest} = TYPE_NAME {node.source}"

    @visitor.when(ToStrNode)
    def visit(self, node):
        return f"{node.dest} = STR {node.ivalue}"

    @visitor.when(ReadNode)
    def visit(self, node):
        return f"{node.dest} = READ"

    @visitor.when(PrintStrNode)
    def visit(self, node):
        return f"PRINT STR{node.str_addr}"

    @visitor.when(PrintIntNode)
    def visit(self, node):
        return f"PRINT INT {node.int_addr}"

    @visitor.when(LengthNode)
    def visit(self, node):
        return f"{node.dest} = LENGTH {node.source}"

    @visitor.when(LoadNode)
    def visit(self, node):
        return f"{node.dest} = LOAD {node.msg.name}"

    @visitor.when(ConcatNode)
    def visit(self, node):
        return f"{node.dest} = CONCAT {node.left} {node.right}"

    @visitor.when(SubstringNode)
    def visit(self, node):
        return f"{node.dest} = SUBSTRING {node.source} {node.id} {node.length}"

    @visitor.when(DefaultValueNode)
    def visit(self, node):
        return f"{node.dest} = DEFAULT {node.type}"

    @visitor.when(IsVoidNode)
    def visit(self, node):
        return f"{node.dest} = ISVOID {node.value}"

    @visitor.when(ExitNode)
    def visit(self, node):
        return f"EXIT"
# printer = PrintVisitor()
# return lambda ast: printer.visit(ast)
