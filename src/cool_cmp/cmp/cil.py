from typing import Optional
import cmp.visitor as visitor


class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name, parent, name_data):
        self.name = name
        self.parent = parent
        self.name_data = name_data
        self.attributes = []
        self.methods = []
    
    def __str__(self):
        return self.name

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, labels):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.labels = labels
        
    @property
    def return_instruction(self) -> 'Optional[ReturnNode]':
        if self.instructions:
            return self.instructions[-1] if isinstance(self.instructions[-1], ReturnNode) else None
        return None
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

class GetAttribNode(InstructionNode):
    def __init__(self, source, attr, dest, attribute_index):
        self.source = source
        self.attr = attr
        self.dest = dest
        self.attribute_index = attribute_index

class SetAttribNode(InstructionNode):
    def __init__(self, source, attr, value, attribute_index):
        self.source = source
        self.attr = attr
        self.value = value
        self.attribute_index = attribute_index

class GetIndexNode(InstructionNode):
    def __init__(self, source, index, dest):
        self.source = source
        self.index = index
        self.dest = dest

class SetIndexNode(InstructionNode):
    def __init__(self, source, index, value):
        self.source = source
        self.index = index
        self.value = value

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class ArrayNode(InstructionNode):
    def __init__(self, dest, type, length) -> None:
        super().__init__()
        self.dest = dest
        self.type = type
        self.length = length

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class TypeNameNode(InstructionNode):
    def __init__(self, typex, dest) -> None:
        self.type = typex
        self.dest = dest

class LabelNode(InstructionNode):
    def __init__(self, label) -> None:
        self.label = label

class GotoNode(InstructionNode):
    def __init__(self, label) -> None:
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, condition_value, label) -> None:
        self.condition_value = condition_value
        self.label = label

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest, base_type=None):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.base_type = base_type # Needed for SELF_TYPE handling. Is the Type where the SELF_TYPE was defined

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
    def __init__(self, dest, string_var) -> None:
        self.dest = dest
        self.string_var = string_var

class ConcatNode(InstructionNode):
    def __init__(self, dest, string1, string2) -> None:
        self.dest = dest
        self.string1 = string1
        self.string2 = string2

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    def __init__(self, dest, string, index, length) -> None:
        self.dest = dest
        self.string = string
        self.index = index
        self.length = length

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class PrintIntNode(InstructionNode):
    def __init__(self, int_addr):
        self.int_addr = int_addr

class AbortNode(InstructionNode):
    pass

class CopyNode(InstructionNode):
    def __init__(self, instance, result):
        self.instance = instance
        self.result = result

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
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

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
            return f'{node.dest} = TYPEOF {node.type}'

        @visitor.when(StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.method}'

        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.name}'

        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))