class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode, idx=None):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode
        self.index = idx

    def __str__(self):
        text = '.TYPE\n\n'
        for t in self.dottypes:
            text += str(t)

        text += '\n.DATA\n\n'
        for d in self.dotdata:
            text += str(d)

        text += '\n.CODE\n\n'
        for c in self.dotcode:
            text += str(c)
        
        return text

class TypeNode(Node):
    def __init__(self, name, atributes=None, methods=None, idx=None):
        self.name = name
        self.index = idx
        self.methods = methods if methods is not None else []
        self.attributes = atributes if atributes is not None else []

    def __str__(self):
        text = f'type {self.name}{{\n'

        for attr in self.attributes:
            text += f'\tattrubte {str(attr[0])} : {str(attr[1])} ;\n'
        
        text += '\n'
        
        for meth in self.methods:
            text += f'\tmethod {str(meth[0])} : {str(meth[1])} ;\n'

        text += '} ;\n'
        return text

class DataNode(Node):
    def __init__(self, vname, value, idx=None):
        self.name = vname
        self.value = value
        self.index = idx

    def __str__(self):
        return f'{self.name} = "{self.value}" ;\n'

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, idx=None):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.index = idx

    def __str__(self):
        text = f'function {self.name}{{\n'

        for param in self.params:
            text += str(param)
        
        text += '\n'

        for local in self.localvars:
            text += str(local)
        
        text += '\n'

        for inst in self.instructions:
            text += str(inst)

        text += '}\n'
        return text

class ParamNode(Node):
    def __init__(self, name, typex, idx=None):
        self.name = name
        self.type = typex
        self.index = idx
    
    def __str__(self):
        return f'\tPARAM {self.name} ;\n'

class LocalNode(Node):
    def __init__(self, name, idx=None):
        self.name = name
        self.index = idx

    def __str__(self):
        return f'\tLOCAL {self.name} ;\n'

class InstructionNode(Node):
    def __init__(self, idx=None):
        self.in1 = None
        self.in2 = None
        self.out = None
        self.index = idx

class AssignNode(InstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source 
        
        self.in1 = source
        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = {self.source} ;\n'

class UnaryNode(InstructionNode):
    def __init__(self, dest, expr, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr

        self.in1 = expr
        self.out = dest

class NotNode(UnaryNode):
    def __str__(self) :
        return f'\t{self.dest} = NOT {self.expr} ;\n'

class LogicalNotNode(UnaryNode):
    def __str__(self) :
        return f'\t{self.dest} = ! {self.expr} ;\n'

class BinaryNode(InstructionNode):
    def __init__(self, dest, left, right, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.left = left
        self.right = right 

        self.in1 = left
        self.in2 = right
        self.out = dest

class PlusNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} + {self.right} ;\n'

class MinusNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} - {self.right} ;\n'

class StarNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} * {self.right} ;\n'

class DivNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} / {self.right} ;\n'

class LessNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} < {self.right} ;\n'

class LessEqNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} <= {self.right} ;\n'

class EqualNode(BinaryNode):
    def __str__(self) :
        return f'\t{self.dest} = {self.left} == {self.right} ;\n'

class GetAttribNode(InstructionNode):
    def __init__(self, obj, attr, typex, dest, attr_type, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.type_name = typex
        # self.attr_offset = offset
        self.dest = dest
        self.attr_type = attr_type

        self.out = dest
        self.in1 = obj

    def __str__(self) :
        return f'\t{self.dest} = GETATTR {self.obj} {self.attr} ;\n'

class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, typex, value, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        # self.attr_offset = offset
        self.value = value
        self.type_name = typex

        self.out = obj
        self.in1 = value

    def __str__(self):
        return f'\tSETATTR {self.obj} {self.attr} {self.value} ;\n'

class GetIndexNode(InstructionNode):
    pass

class SetIndexNode(InstructionNode):
    pass

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest, idx=None):
        super().__init__(idx)
        self.type = itype
        self.dest = dest

        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = ALLOCATE {self.dest} ;\n'

class ArrayNode(InstructionNode):
    pass

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.dest = dest

        self.out = dest
        self.in1 = obj

    def __str__(self):
        return f'\t{self.dest} = TYPEOF {self.obj}'

class LabelNode(InstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label

    def __str__(self):
        return f'\tLABEL {self.label} ;\n'

class GotoNode(InstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label
    
    def __str__(self):
        return f'\tGOTO {self.label} ;\n'

class GotoIfNode(InstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond

    def __str__(self):
        return f'\tIF {self.cond} GOTO {self.label} ;\n'

class GotoIfFalseNode(InstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.in1 = cond

    def __str__(self):
        return f'\tIF {self.cond} GOTO {self.label} ;\n'

class StaticCallNode(InstructionNode):
    def __init__(self, xtype, function, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.function = function
        self.dest = dest
        self.args = args
        self.return_type = return_type
        
        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = CALL {self.function} ;\n'

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, obj, method, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.method = method
        self.dest = dest
        self.args = args
        self.return_type = return_type
        self.obj = obj

        self.out = dest
        self.in1 = obj
    
    def __str__(self):
        return f'\t{self.dest} = VCALL {self.obj} {self.method} ;\n'

class ArgNode(InstructionNode):
    def __init__(self, name, idx=None):
        super().__init__(idx)
        self.dest = name

        self.out = name

    def __str__(self):
        return f'\tARG {self.dest} ;\n'

class ReturnNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.out = value
    
    def __str__(self):
        return f'\tRETURN {self.value} ;\n'

class LoadNode(InstructionNode):
    def __init__(self, dest, msg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.msg = msg

        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = LOAD {self.msg} ;\n'

class LengthNode(InstructionNode):
    def __init__(self, dest, arg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg = arg

        self.out = dest
        self.in1 = arg

    def __str__(self):
        return f'\t{self.dest} = LENGTH {self.arg} ;\n'

class ConcatNode(InstructionNode):
    def __init__(self, dest, arg1, arg2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg1 = arg1
        self.arg2 = arg2

        self.out = dest
        self.in1 = arg1
        self.in2 = arg2

    def __str__(self):
        return f'\t{self.dest} = CONCAT {self.arg1} {self.arg2} ;\n'

class PrefixNode(InstructionNode):
    def __init__(self, dest, word, n, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.word = word
        self.n = n

        self.out = dest
        self.in1 = word
        self.in2 = n
    
    def __str__(self):
        return f'\t{self.dest} = PREFIX {self.word} {self.n} ;\n'

class SubstringNode(InstructionNode):
    def __init__(self, dest, word, begin, end, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.begin = begin
        self.word = word
        self.end = end

        self.out = dest
        self.in1 = begin
        self.in2 = end

    def __str__(self):
        return f'\t{self.dest} = SUBSTR {self.word} {self.begin} {self.end} ;\n'

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.ivalue = ivalue

        self.out = dest
        self.in1 = ivalue

    def __str__(self):
        return f'\t{self.dest} = TOSTR {self.ivalue} ;\n'

class OutStringNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

    def __str__(self):
        return f'\tOUT String {self.value} ;\n'

class OutIntNode(InstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.in1 = value

    def __str__(self):
        return f'\tOUT Int {self.value} ;\n'

class ReadStringNode(InstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = READ String ;\n'

class ReadIntNode(InstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest

        self.out = dest
    
    def __str__(self):
        return f'\t{self.dest} = READ Int ;\n'

class ExitNode(InstructionNode):
    def __init__(self, classx, value=0, idx=None):
        super().__init__(idx)
        self.classx = classx        # instance of the method that called the class
        self.value = value

        self.in1 = value
        self.in2 = classx

    def __str__(self):
        return f'\tEXIT {self.classx} {self.value} ;\n'

class CopyNode(InstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source

        self.out = dest
        self.in1 = source
    
    def __str__(self):
        return f'\t{self.dest} = COPY {self.source} ;\n'

class ConformsNode(InstructionNode):
    "Checks if the type of expr conforms to type2"
    def __init__(self, dest, expr, type2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr
        self.type = type2

        self.out = dest
        self.in1 = expr    # is a string, so is always a variable

    def __str__(self):
        return f'\t{self.dest} = CONFORMTO {self.expr} {self.type} ;\n'
        
class VoidConstantNode(InstructionNode):
    def __init__(self, obj, idx=None):
        super().__init__(idx)
        self.obj = obj

        self.out = obj

    def __str__(self):
        return f'\t{self.obj}'

class ErrorNode(InstructionNode):
    "Generic class to report errors in mips"
    def __init__(self, typex, idx=None):
        super().__init__(idx)
        self.type = typex

    def __str__(self):
        return f'\tERROR {self.type} ;\n'

class BoxingNode(InstructionNode):
    def __init__(self, dest, type_name, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.type = type_name

        self.out = dest

    def __str__(self):
        return f'\t{self.dest} = BOX {self.type} ;\n'
