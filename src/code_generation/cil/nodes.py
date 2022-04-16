from utils.constants import *

class CILNode:
    pass

class CILFunctionNode(CILNode):
    def __init__(self, fname, params, local_variables, instructions, idx=None):
        self.name = fname
        self.params = params
        self.local_variables = local_variables
        self.instructions = instructions
        self.index = idx

class CILParamNode(CILNode):
    def __init__(self, name, typex, idx=None):
        self.name = name
        self.type = typex
        self.index = idx

class CILLocalNode(CILNode):
    def __init__(self, name, idx=None):
        self.name = name
        self.index = idx

class CILInstructionNode(CILNode):
    def __init__(self, idx=None):
        self.input1 = None
        self.input2 = None
        self.output = None
        self.index = idx

class CILAssignNode(CILInstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source 
        
        self.input1 = source
        self.output = dest

class CLIUnaryNode(CILInstructionNode):
    def __init__(self, dest, expr, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr

        self.input1 = expr
        self.output = dest

class CILNotNode(CLIUnaryNode):
    pass

class CILLogicalNotNode(CLIUnaryNode):
    pass

class CILBinaryNode(CILInstructionNode):
    def __init__(self, dest, left, right, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.left = left
        self.right = right 

        self.input1 = left
        self.input2 = right
        self.output = dest

class CILPlusNode(CILBinaryNode):
    pass

class CILMinusNode(CILBinaryNode):
    pass

class CILStarNode(CILBinaryNode):
    pass

class CILDivNode(CILBinaryNode):
    pass

class CILLessNode(CILBinaryNode):
    pass

class CILLessEqNode(CILBinaryNode):
    pass

class CILEqualNode(CILBinaryNode):
    pass

class CILGetAttribNode(CILInstructionNode):
    def __init__(self, obj, attr, typex, dest, attr_type, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.type_name = typex
        self.dest = dest
        self.attr_type = attr_type

        self.output = dest
        self.input1 = obj

class CILSetAttribNode(CILInstructionNode):
    def __init__(self, obj, attr, typex, value, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.attr = attr
        self.value = value
        self.type_name = typex

        self.output = obj
        self.input1 = value

class CILGetIndexNode(CILInstructionNode):
    pass

class CILSetIndexNode(CILInstructionNode):
    pass

class CILAllocateNode(CILInstructionNode):
    def __init__(self, itype, dest, idx=None):
        super().__init__(idx)
        self.type = itype
        self.dest = dest

        self.output = dest

class CILArrayNode(CILInstructionNode):
    pass

class CILTypeOfNode(CILInstructionNode):
    def __init__(self, obj, dest, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.dest = dest

        self.output = dest
        self.input1 = obj

class CILLabelNode(CILInstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label

class CILGotoNode(CILInstructionNode):
    def __init__(self, label, idx=None):
        super().__init__(idx)
        self.label = label

class CILGotoIfNode(CILInstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.input1 = cond

class CILGotoIfFalseNode(CILInstructionNode):
    def __init__(self, cond, label, idx=None):
        super().__init__(idx)
        self.cond = cond
        self.label = label

        self.input1 = cond

class CILStaticCallNode(CILInstructionNode):
    def __init__(self, xtype, function, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.function = function
        self.dest = dest
        self.args = args
        self.return_type = return_type
        
        self.output = dest

class CILDynamicCallNode(CILInstructionNode):
    def __init__(self, xtype, obj, method, dest, args, return_type, idx=None):
        super().__init__(idx)
        self.type = xtype
        self.method = method
        self.dest = dest
        self.args = args
        self.return_type = return_type
        self.obj = obj

        self.output = dest
        self.input1 = obj

class CILArgNode(CILInstructionNode):
    def __init__(self, name, idx=None):
        super().__init__(idx)
        self.dest = name

        self.output = name

class CILReturnNode(CILInstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.output = value

class CILConformsNode(CILInstructionNode):
    def __init__(self, dest, expr, type2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.expr = expr
        self.type = type2

        self.output = dest
        self.input1 = expr
        
class CILVoidConstantNode(CILInstructionNode):
    def __init__(self, obj, idx=None):
        super().__init__(idx)
        self.obj = obj
        self.output = obj

class CILErrorNode(CILInstructionNode):
    def __init__(self, typex, idx=None):
        super().__init__(idx)
        self.type = typex
class CILLoadNode(CILInstructionNode):
    def __init__(self, dest, msg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.msg = msg

        self.output = dest

class CILLengthNode(CILInstructionNode):
    def __init__(self, dest, arg, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg = arg

        self.output = dest
        self.input1 = arg

class CILConcatNode(CILInstructionNode):
    def __init__(self, dest, arg1, arg2, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.arg1 = arg1
        self.arg2 = arg2

        self.output = dest
        self.input1 = arg1
        self.input2 = arg2

class CILPrefixNode(CILInstructionNode):
    def __init__(self, dest, word, n, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.word = word
        self.n = n

        self.output = dest
        self.input1 = word
        self.input2 = n
class CILProgramNode(CILNode):
    def __init__(self, info: dict, idx=None):
        self.cil_types = info[TYPE]
        self.cil_data = info[DATA]
        self.cil_code = info[CODE]
        self.index = idx

class CILTypeNode(CILNode):
    def __init__(self, name, atributes=None, methods=None, idx=None):
        self.name = name
        self.attributes = atributes if atributes is not None else []
        self.methods = methods if methods is not None else []
        self.index = idx

class CILDataNode(CILNode):
    def __init__(self, vname, value, idx=None):
        self.name = vname
        self.value = value
        self.index = idx

class CILSubstringNode(CILInstructionNode):
    def __init__(self, dest, word, begin, end, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.begin = begin
        self.word = word
        self.end = end

        self.output = dest
        self.input1 = begin
        self.input2 = end

class CILToStrNode(CILInstructionNode):
    def __init__(self, dest, ivalue, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.ivalue = ivalue
        self.output = dest
        self.input1 = ivalue

class CILOutStringNode(CILInstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value

        self.input1 = value

class CILOutIntNode(CILInstructionNode):
    def __init__(self, value, idx=None):
        super().__init__(idx)
        self.value = value
        self.input1 = value

class CILReadStringNode(CILInstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.output = dest

class CILReadIntNode(CILInstructionNode):
    def __init__(self, dest, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.output = dest

class CILExitNode(CILInstructionNode):
    def __init__(self, classx, value=0, idx=None):
        super().__init__(idx)
        self.classx = classx
        self.value = value

        self.input1 = value
        self.input2 = classx

class CILCopyNode(CILInstructionNode):
    def __init__(self, dest, source, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.source = source

        self.output = dest
        self.input1 = source

class CILBoxingNode(CILInstructionNode):
    def __init__(self, dest, type_name, idx=None):
        super().__init__(idx)
        self.dest = dest
        self.type = type_name

        self.output = dest
