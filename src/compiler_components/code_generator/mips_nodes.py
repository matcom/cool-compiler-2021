class MipsNode:
    pass


class MipsProgramNode(MipsNode):
    def __init__(self, dotdata, dotcode):
        self.dotdata = dotdata
        self.dotcode = dotcode


# string
class MipsStringNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class MipsWordNode(MipsNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class MipsTableNode(MipsNode):
    def __init__(self , type_name,methods):
        self.type_name = type_name
        self.methods = methods


# jumps
class MipsJumpNode(MipsNode):
    def __init__(self, label):
        self.label = label


class MipsJumpAtAddressNode(MipsJumpNode):
    pass


class MipsJRNode(MipsJumpNode):
    pass


class MipsJALRNode(MipsJumpNode):
    pass


# stack
class MipsLWNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


class MipsLINode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


class MipsLANode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


class MipsSWNode(MipsNode):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest


# syscall
class MipsSyscallNode(MipsNode):
    pass


# move
class MipsMoveNode(MipsNode):
    def __init__(self, dest, src):
        self.src = src
        self.dest = dest


# arithmetic
class MipsArithmeticNode:
    def __init__(self, param1, param2, param3):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3


class MipsAddNode(MipsArithmeticNode):
    pass


class MipsAddiuNode(MipsArithmeticNode):
    pass


class MipsMinusNode(MipsArithmeticNode):
    pass


class MipsStarNode(MipsArithmeticNode):
    pass


class MipsDivNode(MipsArithmeticNode):
    pass


class MipsNEGNode(MipsNode):
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src


class MipsComparerNode(MipsNode):
    def __init__(self, param1, param2, label):
        self.param1 = param1
        self.param2 = param2
        self.label = label


class MipsBEQNode(MipsComparerNode):
    pass


class MipsBNENode(MipsComparerNode):
    pass


class MipsBLTNode(MipsComparerNode):
    pass


class MipsBLENode(MipsComparerNode):
    pass


class MipsLabelNode(MipsNode):
    def __init__(self, name):
        self.name = name


class MipsCommentNode(MipsNode):
    def __init__(self, comment):
        self.comment = '\n #' + comment + '\n'
