from ..Tools import visitor

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
        self.labels_count = 0

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
    def __init__(self, dest, left, right):
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
    def __init__(self, dest, obj, attr, computed_type):
        self.dest = dest
        self.obj = obj
        self.attr = attr
        self.computed_type = computed_type

    def __repr__(self):
        return f"{self.dest} = GETATTR {self.obj} {self.attr}"


class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, value, computed_type):
        self.obj = obj
        self.attr = attr
        self.value = value
        self.computed_type = computed_type

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class TypeOfNode(InstructionNode):
    def __init__(self, dest, obj):
        self.obj = obj
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = TYPEOF {self.obj}"


class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"LABEL {self.label}:"


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label}"


class GotoIfNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label} if {self.condition}"

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = CALL {self.function}"

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = VCALL {self.type} {self.method}"

class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ARG {self.name}"


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f"RETURN {self.value}"


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

    def __repr__(self):
        return f"{self.dest} LOAD {self.msg}"

class LengthNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ConcatNode(InstructionNode):
    def __init__(self, dest, prefix, suffix, length):
        self.dest = dest
        self.prefix = prefix
        self.suffix = suffix
        self.length = length

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    def __init__(self, dest, str_value, index, length):
        self.dest = dest
        self.str_value = str_value
        self.index = index
        self.length = length

class ToStrNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintStringNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class PrintIntNode(InstructionNode):
    def __init__(self, value):
        self.value = value

class ExitNode(InstructionNode):
    pass

class CopyNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class ErrorNode(InstructionNode):
    def __init__(self, data):
        self.data = data

class VoidNode(InstructionNode):
    pass

class NameNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class NotNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class ComplementNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}' for x in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\t{methods}\n}}'

        @visitor.when(DataNode)
        def visit(self, node):
            return f'DATA "{node.value}"'

        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node):
            return f'{node.dest} = {node.source}'

        @visitor.when(PlusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} + {node.right}'

        @visitor.when(MinusNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} - {node.right}'

        @visitor.when(StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} * {node.right}'

        @visitor.when(DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} / {node.right}'

        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.obj}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method.lex}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

        @visitor.when(LoadNode)
        def visit(self, node):
            return f'{node.dest} = LOAD {self.visit(node.msg)}'

        @visitor.when(PrintStringNode)
        def visit(self, node: PrintStringNode):
            return f'PRINTSTRING {node.str_addr}'

        @visitor.when(PrintIntNode)
        def visit(self, node: PrintIntNode):
            return f'PRINTINT {node.value}'

        @visitor.when(ExitNode)
        def visit(self, node: ExitNode):
            return f'EXIT'

        @visitor.when(CopyNode)
        def visit(self, node):
            return f'{node.dest} = COPY {node.value}'

        @visitor.when(GetAttribNode)
        def visit(self, node: GetAttribNode):
            return f'{node.dest} = GETATTRIB {node.obj}.{node.attr} {node.computed_type}'

        @visitor.when(ErrorNode)
        def visit(self, node: ErrorNode):
            return f'ERROR {self.visit(node.data)}'

        @visitor.when(ReadNode)
        def visit(self, node: ReadNode):
            return f'{node.dest} = READ'

        @visitor.when(SetAttribNode)
        def visit(self, node: SetAttribNode):
            return f'SETATTR {node.obj}.{node.attr}: {node.computed_type} = {node.value}'

        @visitor.when(LessNode)
        def visit(self, node: LessNode):
            return f'{node.dest} = {node.left} < {node.right}'

        @visitor.when(GotoIfNode)
        def visit(self, node: GotoIfNode):
            return f'GOTOIF {node.condition} {node.label}'

        @visitor.when(GotoNode)
        def visit(self, node: GotoNode):
            return f'GOTO {node.label}'

        @visitor.when(LabelNode)
        def visit(self, node: LabelNode):
            return f'LABEL {node.label}'

        @visitor.when(SubstringNode)
        def visit(self, node: SubstringNode):
            return f'{node.dest} = SUBSTRING {node.str_value}[{node.index}:{node.index + node.length}]'

        @visitor.when(ConcatNode)
        def visit(self, node: ConcatNode):
            return f'{node.dest} = CONCAT {node.prefix} + {node.suffix}'

        @visitor.when(LengthNode)
        def visit(self, node: LengthNode):
            return f'{node.dest} = {node.source}.lenght'

        @visitor.when(EqualNode)
        def visit(self, node: EqualNode):
            return f'{node.dest} = {node.left} == {node.right}'

        @visitor.when(NameNode)
        def visit(self, node: NameNode):
            return f'{node.dest} = NAME {node.value}'

        @visitor.when(EqualStringNode)
        def visit(self, node: EqualStringNode):
            return f'{node.dest} = {node.left} == {node.right}'

        @visitor.when(ComplementNode)
        def visit(self, node: ComplementNode):
            return f'{node.dest} = ~{node.value}'

        @visitor.when(LessEqualNode)
        def visit(self, node: LessEqualNode):
            return f'{node.dest} = {node.left} <= {node.right}'

        @visitor.when(GetIndexNode)
        def visit(self, node: GetIndexNode):
            return f'GETINDEXNODE'

        @visitor.when(SetIndexNode)
        def visit(self, node: SetIndexNode):
            return f'SETINDEXNODE'

        @visitor.when(PrefixNode)
        def visit(self, node: PrefixNode):
            return f'PREFFIXNODE'

        @visitor.when(ToStrNode)
        def visit(self, node: ToStrNode):
            return f'{node.dest} = str({node.value})'

        @visitor.when(VoidNode)
        def visit(self, node: VoidNode):
            return 'VOID'

        @visitor.when(NotNode)
        def visit(self, node: NotNode):
            return f'{node.dest} = NOT {node.value}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))