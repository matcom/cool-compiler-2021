### nodos del ast de MIPS ###
class Node:
    comment: str = ""

    def set_comment(self, comment: str) -> "Node":
        self.comment = comment
        return self


class ProgramNode(Node):
    def __init__(self, dotdata, dottext):
        self.dotdata = dotdata
        self.dottext = dottext


class DataNode(Node):
    data_type = ""

    def __init__(self, name, value):
        self.name = name
        self.value = value

class InstructionNode(Node):
    code: str = ""

    def __init__(self):
        pass

class EmptyDataNode(Node):
    pass

class EmptyInstructionNode(InstructionNode):
    pass


# data nodes

class WordDataNode(DataNode):
    data_type = ".word"


class SpaceDataNode(DataNode):
    data_type = ".space"


class AsciizDataNode(DataNode):
    data_type = ".asciiz"



# addr node

class OneAddressNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class TwoAddressNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ThreeAddressNode(InstructionNode):
    def __init__(self, dest, source1, source2):
        self.dest = dest
        self.source1 = source1
        self.source2 = source2


# arithmetic and logic instructions
class AddNode(ThreeAddressNode):
    code = "add"

class AddiNode(ThreeAddressNode):
    code = "addi"

class AdduNode(ThreeAddressNode):
    code = "addu"

class AddiuNode(ThreeAddressNode):
    code = "addiu"

class AndNode(ThreeAddressNode):
    code = "and"

class AndiNode(ThreeAddressNode):
    code = "andi"

class DivNode(TwoAddressNode):
    code = "div"

class DivuNode(TwoAddressNode):
    code = "divu"

class MultNode(TwoAddressNode):
    code = "mult"

class MultuNode(TwoAddressNode):
    code = "multu"

class NorNode(ThreeAddressNode):
    code = "nor"

class OrNode(ThreeAddressNode):
    code = "or"


class OriNode(ThreeAddressNode):
    code = "ori"

class SllNode(ThreeAddressNode):
    code = "sll"

class SllvNode(ThreeAddressNode):
    code = "sllv"

class SraNode(ThreeAddressNode):
    code = "sra"

class SravNode(ThreeAddressNode):
    code = "srav"

class SrlNode(ThreeAddressNode):
    code = "srl"

class SrlvNode(ThreeAddressNode):
    code = "srlv"

class SubNode(ThreeAddressNode):
    code = "sub"

class SubuNode(ThreeAddressNode):
    code = "subu"

class XorNode(ThreeAddressNode):
    code = "xor"

class XoriNode(ThreeAddressNode):
    code = "xori"

class LuiNode(TwoAddressNode):
    code = "lui"

class SltNode(ThreeAddressNode):
    code = "slt"

class SltiNode(ThreeAddressNode):
    code = "slti"

class SltuNode(ThreeAddressNode):
    code = "sltu"

class SltiuNode(ThreeAddressNode):
    code = "sltiu"

class SleNode(ThreeAddressNode):
    code = "sle"

class SeqNode(ThreeAddressNode):
    code = "seq"



# branch and jump instructions 
class BeqNode(ThreeAddressNode):
    code = "beq"

class BgtNode(ThreeAddressNode):
    code = "bgt"

class BgeNode(ThreeAddressNode):
    code = "bge"

class BgezNode(TwoAddressNode):
    code = "bgez"

class BgezalNode(TwoAddressNode):
    code = "bgezal"

class BgtzNode(TwoAddressNode):
    code = "bgtz"

class BlezNode(TwoAddressNode):
    code = "blez"

class BltzalNode(TwoAddressNode):
    code = "bltzal"

class BltzNode(TwoAddressNode):
    code = "bltz"

class BneNode(ThreeAddressNode):
    code = "bne"

class JumpNode(OneAddressNode):
    code = "j"

class JumpAndLinkNode(OneAddressNode):
    code = "jal"

class JumpAndLinkRegisterNode(OneAddressNode):
    code = "jalr"

class JumpRegisterNode(OneAddressNode):
    code = "jr"


# Memory Access and Load Instructions 

class LoadInmediateNode(TwoAddressNode):
    code = "li"

class LoadAddressNode(TwoAddressNode):
    code = "la"

class LoadByteNode(TwoAddressNode):
    code = "lb"

class LoadWordNode(TwoAddressNode):
    code = "lw"

class StoreWordNode(TwoAddressNode):
    code = "sw"

class StoreByteNode(TwoAddressNode):
    code = "sb"

class MoveNode(TwoAddressNode):
    code = "move"

class MoveFromLowNode(OneAddressNode):
    code = "mflo"

class MoveFromHighNode(OneAddressNode):
    code = "mfhi"


# end memory access and load instructions 
class SystemCallNode(InstructionNode):
    code = "syscall"

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class CommentNode(InstructionNode):
    def __init__(self, comment):
        self.comment = comment

