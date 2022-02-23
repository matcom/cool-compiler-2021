class CilNode:
    pass


class CilProgramNode(CilNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class CilTypeNode(CilNode):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []


class CilDataNode(CilNode):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class CilFunctionNode(CilNode):
    def __init__(self, fname, params, localvars, instructions, labels):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.labels = labels


class CilParamNode(CilNode):
    def __init__(self, name):
        self.name = name


class CilLocalNode(CilNode):
    def __init__(self, name):
        self.name = name


class CilInstructionNode(CilNode):
    pass


class CilAssignNode(CilInstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class CilArithmeticNode(CilInstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class CilComplementNode(CilInstructionNode):
    def __init__(self, expression, dest):
        self.expression = expression
        self.dest = dest


class CilPlusNode(CilArithmeticNode):
    pass


class CilMinusNode(CilArithmeticNode):
    pass


class CilStarNode(CilArithmeticNode):
    pass


class CilDivNode(CilArithmeticNode):
    pass


class CilLessNode(CilInstructionNode):
    def __init__(self, result, left, right, labelTrue, labelEnd):
        self.result = result
        self.left = left
        self.right = right
        self.labelTrue = labelTrue
        self.labelEnd = labelEnd


class CilLessEqualNode(CilArithmeticNode):
    def __init__(self, result, left, right, labelTrue, labelEnd):
        self.result = result
        self.left = left
        self.right =right
        self.labelTrue = labelTrue
        self.labelEnd = labelEnd


class CilGetAttribNode(CilInstructionNode):
    def __init__(self, ins,att,dest):
        self.ins = ins
        self.att = att
        self.dest = dest


class CilSetAttribNode(CilInstructionNode):
     def __init__(self, ins,att, value):
        self.ins = ins
        self.att = att

        self.value = value


class CilGetIndexNode(CilInstructionNode):
    pass


class CilSetIndexNode(InstructionNode):
    pass


class CilAllocateNode(CilInstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest


class CilJumpNode(CilInstructionNode):
    def __init__(self, method, dest):
        self.method = method
        self.dest = dest


class CilArrayNode(CilInstructionNode):
    pass


class CilTypeOfNode(CilInstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class CilIsVoidNode(CilInstructionNode):
    def __init__(self, obj, dest, label):
        self.obj = obj
        self.dest = dest
        self.label = label


class CilCaseOption(CilInstructionNode):
    def __init__(self, expression, label, typex):
        self.expression = expression
        self.label = label
        self.typex = typex


class CilLabelNode(CilInstructionNode):
    def __init__(self, name):
        self.name = name


class CilGotoNode(CilInstructionNode):
    def __init__(self, name):
        self.name = name


class CilGotoIfNode(CilInstructionNode):
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition


class CilStaticCallNode(CilInstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class CilDynamicCallNode(CilInstructionNode):
    def __init__(self, xtype, method, dest,ins):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.ins = ins


class CilArgsNode(CilInstructionNode):
    def __init__(self, names):
        self.names = names


class CilReturnNode(CilInstructionNode):
    def __init__(self, value=None):
        self.value = value


class CilLoadNode(CilInstructionNode):
    def __init__(self, dest, msg, desp=0):
        self.dest = dest
        self.msg = msg
        self.desp = desp


class CilLoadAddressNode(CilLoadNode):
    pass


class CilLoadIntNode(CilInstructionNode):
    def __init__(self, dest, msg, desp):
        self.dest = dest
        self.msg = msg
        self.desp = desp


class CilLengthNode(CilInstructionNode):
    pass


class CilConcatNode(CilInstructionNode):
    pass


class CilPrefixNode(CilInstructionNode):
    pass


class CilSubstringNode(CilInstructionNode):
    pass


class CilStringComparer(CilInstructionNode):
    def __init__(self, result, left, right):
        self.result = result
        self.left = left
        self.right = right


class CilToStrNode(CilInstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class CilReadNode(CilInstructionNode):
    def __init__(self, dest):
        self.dest = dest


class CilPrintNode(CilInstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr
