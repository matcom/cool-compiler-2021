from cmp.cil import *

class ObjectAbortNode(InstructionNode):
    pass

class ObjectCopyNode(InstructionNode):
    pass
        
class ObjectTypeNameNode(InstructionNode):
    pass

class StringLengthNode(InstructionNode):
    pass
        
class StringConcatNode(InstructionNode):
    pass

class StringSubstringNode(InstructionNode):
    pass

class IOOutStringNode(InstructionNode):
    pass
        
class IOOutIntNode(InstructionNode):
    pass
        
class IOInStringNode(InstructionNode):
    pass
        
class IOInIntNode(InstructionNode):
    pass

class UnaryArithmeticNode(InstructionNode):
    def __init__(self, dest, value) -> None:
        self.dest = dest
        self.value = value

class GetFatherNode(InstructionNode):
    def __init__(self, dest, type) -> None:
        self.dest = dest
        self.type = type

class NotNode(UnaryArithmeticNode):
    pass

class EqualNode(ArithmeticNode):
    pass

class GreaterNode(ArithmeticNode):
    pass

class LesserNode(ArithmeticNode):
    pass

class VoidNode(InstructionNode):
    def __init__(self, dest) -> None:
        self.dest = dest