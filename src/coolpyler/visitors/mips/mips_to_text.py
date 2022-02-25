import coolpyler.ast.mips.base as mips
import coolpyler.utils.visitor as visitor


class MIPSGenerator:
    """
    This class uses the visitor pattern to convert MIPS AST to a .mips program
    """

    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        global_main = "\t.globl main"
        text_section = "\t.text\n" + self.visit(node.text_section)
        data_section = "\t.data\n" + self.visit(node.data_section)
        return f"{global_main}\n\n{data_section}\n\n{text_section}"

    @visitor.when(mips.TextNode)
    def visit(self, node: mips.TextNode):
        return "\n".join(self.visit(instruction) for instruction in node.instructions)

    @visitor.when(mips.DataSectionNode)
    def visit(self, node: mips.DataNode):
        return "\n".join(self.visit(data) for data in node.data.values())

    @visitor.when(mips.DataNode)
    def visit(self, node: mips.DataNode):
        def visit_value(value):
            return (
                str(value)
                if isinstance(value, int) or isinstance(value, str)
                else self.visit(value)
            )

        data_value = ",".join(visit_value(value) for value in node.data)
        return f"{self.visit(node.label)}: {node.storage_type} {data_value}"

    @visitor.when(mips.RegisterNode)
    def visit(self, node: mips.RegisterNode):
        return f"${node.number}"

    @visitor.when(mips.LabelInstructionNode)
    def visit(self, node: mips.LabelInstructionNode):
        return f"{node.label}:"

    @visitor.when(mips.LabelNode)
    def visit(self, node: mips.LabelNode):
        return str(node.idx)

    @visitor.when(mips.MemoryAddressRegisterNode)
    def visit(self, node: mips.MemoryAddressRegisterNode):
        if node.index == 0:
            t = ""
        else:
            t = f"({str(node.index)})"
        return f"{t}({self.visit(node.register)})"

    @visitor.when(mips.MemoryAddressLabelNode)
    def visit(self, node: mips.MemoryAddressLabelNode):
        if node.index == 0:
            t = ""
        else:
            t = f"({str(node.index)})"
        return f"{t}{self.visit(node.address)}"

    @visitor.when(mips.MoveNode)
    def visit(self, node: mips.MoveNode):
        return f"\tmove {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.SyscallNode)
    def visit(self, node: mips.SyscallNode):
        return "\tsyscall"

    @visitor.when(mips.LoadAddressNode)
    def visit(self, node: mips.LoadAddressNode):
        return f"\tla {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.LoadWordNode)
    def visit(self, node: mips.LoadWordNode):
        return f"\tlw {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.StoreByteNode)
    def visit(self, node: mips.StoreByteNode):
        return f"\tlb {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.LoadByteNode)
    def visit(self, node: mips.LoadByteNode):
        return f"\tlb {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.LoadInmediateNode)
    def visit(self, node: mips.LoadInmediateNode):
        return f"\tli {self.visit(node.left)}, {str(node.right)}"

    @visitor.when(mips.MultNode)
    def visit(self, node: mips.MultNode):
        return f"\tmult {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.DivNode)
    def visit(self, node: mips.DivNode):
        return f"\tdiv {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.StoreWordNode)
    def visit(self, node: mips.StoreWordNode):
        return f"\tsw {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.AddNode)
    def visit(self, node: mips.AddNode):
        return f"\tadd {self.visit(node.left)},  {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(mips.SubNode)
    def visit(self, node: mips.SubNode):
        return f"\tsub {self.visit(node.left)},  {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(mips.AddiNode)
    def visit(self, node: mips.AddiNode):
        return f"\taddi {self.visit(node.left)},  {self.visit(node.middle)}, {str(node.right)}"

    @visitor.when(mips.BgtNode)
    def visit(self, node: mips.BgtNode):
        return f"\tbgt {self.visit(node.left)},  {self.visit(node.right)}, {str(node.label)}"

    @visitor.when(mips.BeqzNode)
    def visit(self, node: mips.BeqzNode):
        return f"\tbeqz {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(mips.JumpNode)
    def visit(self, node: mips.JumpNode):
        return f"\tj {self.visit(node.address)}"

    @visitor.when(mips.JumpRegisterNode)
    def visit(self, node: mips.JumpRegisterNode):
        return f"\tjr {self.visit(node.register)}"

    @visitor.when(mips.JumpAndLinkNode)
    def visit(self, node: mips.JumpAndLinkNode):
        return f"\tjal {node.address}"

    @visitor.when(mips.JumpRegisterLinkNode)
    def visit(self, node: mips.JumpRegisterLinkNode):
        return f"\tjalr {self.visit(node.register)}"
