from core.tools import visitor
from core.mips.MipsAst import *

class MIPSAstFormatter:
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        return f'.data\n' \
               '\n'.join(self.visit(i) for i in node.data) + '\n'\
               '\n'.join(self.visit(i) for i in node.functions) + '\n'

    @visitor.when(FunctionNode)
    def visit(self, node):
        return f'{node.label}:\n\t' \
               "\n\t".join(self.visit(i) for i in node.instructions)

    @visitor.when(AbsoluteNode)
    def visit(self, node):
        pass

    @visitor.when(AdditionNode)
    def visit(self, node):
        return f'add {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(AdditionInmediateNode)
    def visit(self, node):
        pass

    @visitor.when(DivideNode)
    def visit(self, node):
        pass

    @visitor.when(MultiplyNode)
    def visit(self, node):
        pass

    @visitor.when(NegateNode)
    def visit(self, node):
        pass

    @visitor.when(SubstractionNode)
    def visit(self, node):
        pass

    @visitor.when(LessNode)
    def visit(self, node):
        pass

    @visitor.when(LessInmediateNode)
    def visit(self, node):
        pass

    @visitor.when(EqualNode)
    def visit(self, node):
        pass

    @visitor.when(LessEqualNode)
    def visit(self, node):
        pass

    @visitor.when(JumpNode)
    def visit(self, node):
        pass

    @visitor.when(JalNode)
    def visit(self, node):
        pass

    @visitor.when(MoveNode)
    def visit(self, node):
        pass

    @visitor.when(StoreWordNode)
    def visit(self, node):
        pass

    @visitor.when(LoadInmediateNode)
    def visit(self, node):
        pass

    @visitor.when(LoadWordNode)
    def visit(self, node):
        pass

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        pass

    @visitor.when(BranchOnNotEqualNode)
    def visit(self, node):
        pass

    @visitor.when(LabelNode)
    def visit(self, node):
        pass

    @visitor.when(NotNode)
    def visit(self, node):
        pass

    @visitor.when(ShiftLeftNode)
    def visit(self, node):
        pass

    @visitor.when(SyscallNode)
    def visit(self, node):
        pass

    @visitor.when(StringConst)
    def visit(self, node):
        pass

    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        pass

    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        pass