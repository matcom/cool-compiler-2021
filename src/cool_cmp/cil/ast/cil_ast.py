from cmp.cil import *

################################################################################
# META INSTRUCTIONS

class IntAbortNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class IntTypeNameNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)

class BoolAbortNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)
        
class BoolTypeNameNode(InstructionNode):
    def __init__(self,row,column,comment=None):
        super().__init__(row,column,comment)


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

class InitInstance(InstructionNode): # TODO Add to META MIPS Section
    def __init__(self, source, instance_type, row, column, comment=None)-> None:
        super().__init__(row, column, comment)
        self.source = source
        self.instance_type = instance_type


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
    pass

class EqualNode(ArithmeticNode):
    pass


class GreaterNode(ArithmeticNode):
    pass


class LesserNode(ArithmeticNode):
    pass

class ObjEqualNode(ArithmeticNode): # TODO Add to CIL Section
    def __init__(self, dest, left, right, row=None, column=None, comment=None, value_compare=None) -> None:
        super().__init__(dest, left, right, row, column, comment=comment)
        if value_compare is None:
            raise ValueError("value_compare must be initialized to True or False")
        self.value_compare = value_compare

################################################################################

