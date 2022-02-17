from cmp.cil import *






################################################################################
# META INSTRUCTIONS

class ObjectAbortNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

class ObjectCopyNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class ObjectTypeNameNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

class StringLengthNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class StringConcatNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

class StringSubstringNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

class IOOutStringNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class IOOutIntNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class IOInStringNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class IOInIntNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

################################################################################







################################################################################
# OTHER INSTRUCTIONS

class GetFatherNode(InstructionNode):
    def __init__(self, dest, variable,row, column, comment=None)-> None:
        super().__init__(row, column, comment)
        self.dest = dest
        self.variable = variable


class VoidNode(InstructionNode):
    def __init__(self, dest, row, column, comment=None)-> None:
        super().__init__(row, column, comment)
        self.dest = dest

################################################################################







################################################################################
# ARITHMETIC INSTRUCTIONS

class UnaryArithmeticNode(InstructionNode):
    def __init__(self, dest, value, row, column, comment=None)-> None:
        super().__init__(row, column, comment)
        self.dest = dest
        self.value = value

class NotNode(UnaryArithmeticNode):
    def __init__(self, row, column, comment=None)-> None:
        super().__init__(row, column, comment)

class EqualNode(ArithmeticNode):
    def __init__(self, row, column, comment=None)-> None:
        super().__init__(row, column, comment)

class GreaterNode(ArithmeticNode):
    def __init__(self, row, column, comment=None)-> None:
        super().__init__(row, column, comment)

class LesserNode(ArithmeticNode):
    def __init__(self, row, column, comment=None)-> None:
        super().__init__(row, column, comment)

################################################################################


