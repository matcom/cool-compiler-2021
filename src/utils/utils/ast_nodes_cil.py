import utils.visitor as visitor


class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name, parent=None):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = parent if parent is not None else "null"

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
    def __init__(self, name, type="Object"):
        self.name = name
        self.type = type

class InstructionNode(Node):
    pass

class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class ParentNode(InstructionNode):
    def __init__(self, dest, source):
        self.source = source
        self.dest = dest

#######################
##### ARITHMETICS #####
#######################

class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(ArithmeticNode): #
    pass

class MinusNode(ArithmeticNode): #
    pass

class StarNode(ArithmeticNode): #
    pass

class DivNode(ArithmeticNode): #
    pass

class EqualNode(ArithmeticNode): #
    pass

class XorNode(ArithmeticNode): #
    pass

class LessEqualNode(ArithmeticNode): #
    pass

class LessThanNode(ArithmeticNode): #
    pass

class CommentNode(Node):
    def __init__(self, comment: str):
        self.comment = '# ' + comment
        
class EndOfLineNode(Node):
    def __init__(self):
        self.text = '\n'


class GetAttribNode(InstructionNode): #
    def __init__(self, dest, instance, attr, attr_index):
        self.dest = dest
        self.instance = instance
        self.attr = attr
        self.attr_index = attr_index


class SetAttribNode(InstructionNode):
    def __init__(self, instance, attr, source, attrindex):
        self.instance: str = instance
        self.attr: str = attr
        self.source: str = source
        self.attr_index: int = attrindex

class GetIndexNode(InstructionNode):
    def __init__(self, dest, instance, index):
        self.dest = dest
        self.instance = instance
        self.index = index

class SetIndexNode(InstructionNode):
    def __init__(self, instance, index, source):
        self.instance = instance
        self.index = index
        self.source = source

class GetMethodNode(InstructionNode):
    def __init__(self, dest, instance, methodindex, methodname, type):
        self.dest = dest
        self.instance = instance
        self.method_index = methodindex
        self.method_name = methodname
        self.type = type

class SetMethodNode(InstructionNode):
    def __init__(self, dest, instance, attr, attrindex):
        self.dest = dest
        self.instance = instance
        self.attr = attr
        self.attr_index = attrindex 

class GetValueInIndexNode(InstructionNode):
    def __init__(self, dest, instance, index):
        self.dest = dest
        self.instance = instance
        self.index = index

class SetValueInIndexNode(InstructionNode):
    def __init__(self, instance, index, source):
        self.instance = instance
        self.index = index
        self.source = source

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest
        
class AllocateIntNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
        
class AllocateStringNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
        
    @property
    def string(self):
        stopvalues = [
            ('\\n', '\n'), 
            ('\\t', '\t'), 
            ('\\f', '\f'), 
            ('\\b', '\b')
        ]
        s = self.value
        for old, new in stopvalues:
            s = s.replace(old, new)
        return s[1:-1]
    
    @property
    def length(self):
        stopvalues = ['\\n', '\\t', '\\b', '\\f']
        lenvalue = 0
        for item in stopvalues:
            lenvalue += self.value.count(item)
        return len(self.value)  - lenvalue -  2
    

class AllocateBoolNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
        
class AllocateBuildInNode(InstructionNode):
    def __init__(self, dest, value, typename):
        self.dest = dest
        self.value = value
        self.typename = typename ## int or bool
       

class AllocateNullNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class ArrayNode(InstructionNode): #
    def __init__(self, dest, size):
        self.dest = dest
        self.size = size

class TypeOfNode(InstructionNode): #
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label
        
class GotoNode(InstructionNode):
    def __init__(self, addr):
        self.addr = addr
        
class GotoIfNode(InstructionNode):
    def __init__(self, cond, addr):
        self.condition = cond
        self.address = addr

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest, argscount):
        self.function = function
        self.dest = dest
        self.total_args = argscount

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest, argscount):
        self.type = xtype
        self.method_addr = method
        self.dest = dest
        self.total_args = argscount

class ArgNode(InstructionNode):
    def __init__(self, name, arg_index, total_args):
        self.name = name
        self.arg_index = arg_index
        self.total_args = total_args

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class LengthNode(InstructionNode):
    def __init__(self, dest, str_address):
        self.dest = dest
        self.str_address = str_address

class ConcatNode(InstructionNode):
    def __init__(self, dest, s1, s2):
        self.dest = dest
        self.str1 = s1
        self.str2 = s2

class PrefixNode(InstructionNode):
    pass

class SubstringNode(InstructionNode):
    pass

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue

class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr

class AllocateNullNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

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
