from typing import List


class Node:
    comment: str = ""

    def set_comment(self, comment: str) -> "Node":
        self.comment = comment
        return self


class ProgramNode(Node):
    def __init__(self, dotdata: List["DataNode"], dottext: List["InstructionNode"]):
        self.dotdata: List[DataNode] = dotdata
        self.dottext: List[InstructionNode] = dottext


class DataNode(Node):
    data_type: str = ""

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class EmptyDataNode(Node):
    pass


class WordDataNode(DataNode):
    data_type = ".word"


class SpaceDataNode(DataNode):
    data_type = ".space"


class AsciizDataNode(DataNode):
    data_type = ".asciiz"


class InstructionNode(Node):
    code: str = ""

    def __init__(self):
        pass


class OneAddressInstructionNode(InstructionNode):
    def __init__(self, dest: str):
        self.dest: str = dest


class TwoAddressIntructionNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.dest: str = dest
        self.source: str = source


class ThreeAddressIntructionNode(InstructionNode):
    def __init__(self, dest: str, source1: str, source2: str):
        self.dest: str = dest
        self.source1: str = source1
        self.source2: str = source2


#####################################
# Arithmetic and Logic Instructions #
#####################################
class AddNode(ThreeAddressIntructionNode):
    code = "add"


class AddiNode(ThreeAddressIntructionNode):
    code = "addi"


class AdduNode(ThreeAddressIntructionNode):
    code = "addu"


class AddiuNode(ThreeAddressIntructionNode):
    code = "addiu"


class AndNode(ThreeAddressIntructionNode):
    code = "and"


class AndiNode(ThreeAddressIntructionNode):
    code = "andi"


class DivNode(TwoAddressIntructionNode):
    code = "div"


class DivuNode(TwoAddressIntructionNode):
    code = "divu"


class MultNode(TwoAddressIntructionNode):
    code = "mult"


class MultuNode(TwoAddressIntructionNode):
    code = "multu"


class NorNode(ThreeAddressIntructionNode):
    code = "nor"


class OrNode(ThreeAddressIntructionNode):
    code = "or"


class OriNode(ThreeAddressIntructionNode):
    code = "ori"


class SllNode(ThreeAddressIntructionNode):
    code = "sll"


class SllvNode(ThreeAddressIntructionNode):
    code = "sllv"


class SraNode(ThreeAddressIntructionNode):
    code = "sra"


class SravNode(ThreeAddressIntructionNode):
    code = "srav"


class SrlNode(ThreeAddressIntructionNode):
    code = "srl"


class SrlvNode(ThreeAddressIntructionNode):
    code = "srlv"


class SubNode(ThreeAddressIntructionNode):
    code = "sub"


class SubuNode(ThreeAddressIntructionNode):
    code = "subu"


class XorNode(ThreeAddressIntructionNode):
    code = "xor"


class XoriNode(ThreeAddressIntructionNode):
    code = "xori"


class LuiNode(TwoAddressIntructionNode):
    code = "lui"


class SltNode(ThreeAddressIntructionNode):
    code = "slt"


class SltiNode(ThreeAddressIntructionNode):
    code = "slti"


class SltuNode(ThreeAddressIntructionNode):
    code = "sltu"


class SltiuNode(ThreeAddressIntructionNode):
    code = "sltiu"


class SleNode(ThreeAddressIntructionNode):
    code = "sle"


class SeqNode(ThreeAddressIntructionNode):
    code = "seq"

#########################################
# End Arithmetic and Logic Instructions #
#########################################

################################
# Branch and Jump Instructions #
################################


class BeqNode(ThreeAddressIntructionNode):
    code = "beq"


class BgtNode(ThreeAddressIntructionNode):
    code = "bgt"


class BgeNode(ThreeAddressIntructionNode):
    code = "bge"


class BgezNode(TwoAddressIntructionNode):
    code = "bgez"


class BgezalNode(TwoAddressIntructionNode):
    code = "bgezal"


class BgtzNode(TwoAddressIntructionNode):
    code = "bgtz"


class BlezNode(TwoAddressIntructionNode):
    code = "blez"


class BltzalNode(TwoAddressIntructionNode):
    code = "bltzal"


class BltzNode(TwoAddressIntructionNode):
    code = "bltz"


class BneNode(ThreeAddressIntructionNode):
    code = "bne"


class JumpNode(OneAddressInstructionNode):
    code = "j"


class JumpAndLinkNode(OneAddressInstructionNode):
    code = "jal"


class JumpAndLinkRegisterNode(OneAddressInstructionNode):
    code = "jalr"


class JumpRegisterNode(OneAddressInstructionNode):
    code = "jr"


####################################
# End Branch and Jump Instructions #
####################################


#######################################
# Memory Access and Load Instructions #
#######################################


class LoadInmediateNode(TwoAddressIntructionNode):
    code = "li"


class LoadAddressNode(TwoAddressIntructionNode):
    code = "la"


class LoadByteNode(TwoAddressIntructionNode):
    code = "lb"


class LoadWordNode(TwoAddressIntructionNode):
    code = "lw"


class StoreWordNode(TwoAddressIntructionNode):
    code = "sw"


class StoreByteNode(TwoAddressIntructionNode):
    code = "sb"


class MoveNode(TwoAddressIntructionNode):
    code = "move"


class MoveFromLowNode(OneAddressInstructionNode):
    code = "mflo"


class MoveFromHighNode(OneAddressInstructionNode):
    code = "mfhi"


###########################################
# End Memory Access and Load Instructions #
###########################################

class SystemCallNode(InstructionNode):
    code = "syscall"


class LabelNode(InstructionNode):
    def __init__(self, name: str):
        self.name: str = name


class CommentNode(InstructionNode):
    def __init__(self, comment: str):
        self.comment: str = comment

class EmptyInstructionNode(InstructionNode):
    pass
