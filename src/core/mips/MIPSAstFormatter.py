from core.tools import visitor
from core.mips.MipsAst import *

class MIPSAstFormatter:
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        return f'.data\n' + \
               '\n'.join(self.visit(i) for i in node.data) + '\n' + \
               '\n'.join(self.visit(i) for i in node.functions) + '\n'

    @visitor.when(FunctionNode)
    def visit(self, node):
        print([self.visit(i) for i in node.instructions])
        return f'{node.label}:\n\t' + \
               f'\n\t'.join(self.visit(i) for i in node.instructions)

    @visitor.when(AbsoluteNode)
    def visit(self, node):
        return f'abs {self.visit(node.rdest)} {self.visit(node.rsrc)}'

    @visitor.when(AdditionNode)
    def visit(self, node):
        return f'add {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(AdditionInmediateNode)
    def visit(self, node):
        return f'addi {self.visit(node.rdest)} {self.visit(node.rsrc)} {self.visit(node.imm)}'

    @visitor.when(DivideNode)
    def visit(self, node):
        return f'div {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(MultiplyNode)
    def visit(self, node):
        return f'mul {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(NegateNode)
    def visit(self, node):
        return f'neg {self.visit(node.rdest)} {self.visit(node.rsrc1)}'

    @visitor.when(SubstractionNode)
    def visit(self, node):
        return f'sub {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(LessNode)
    def visit(self, node):
        return f'slt {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(LessInmediateNode)
    def visit(self, node):
        return f'slti {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.imm)}'

    @visitor.when(EqualNode)
    def visit(self, node):
        return f'seq {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(LessEqualNode)
    def visit(self, node):
        return f'sle {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'

    @visitor.when(JumpNode)
    def visit(self, node):
        return f'j {self.visit(node.label)}'

    @visitor.when(JalNode)
    def visit(self, node):
        return f'jal {self.visit(node.label)}'

    @visitor.when(MoveNode)
    def visit(self, node):
        return f'move {self.visit(node.reg1)} {self.visit(node.reg2)}'

    @visitor.when(StoreWordNode)
    def visit(self, node):
        return f'sw {self.visit(node.reg)} {self.visit(node.addr)}'

    @visitor.when(LoadInmediateNode)
    def visit(self, node):
        return f'li {self.visit(node.reg)} {self.visit(node.value)}'

    @visitor.when(LoadWordNode)
    def visit(self, node):
        return f'lw {self.visit(node.reg)} {self.visit(node.addr)}'

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        return f'la {self.visit(node.reg)} {self.visit(node.label)}'

    @visitor.when(BranchOnNotEqualNode)
    def visit(self, node):
        return f'bne {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.label)}'

    @visitor.when(LabelNode)
    def visit(self, node):
        return f'{self.visit(node.name)}'

    @visitor.when(NotNode)
    def visit(self, node):
        return f'not {self.visit(node.dest)} {self.visit(node.src)}'

    @visitor.when(ShiftLeftNode)
    def visit(self, node):
        return f'sll {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.bits)}'

    @visitor.when(SyscallNode)
    def visit(self, node):
        return 'syscall'

    @visitor.when(StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'

    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        return f'{node._offset}({self.visit(node._register)})'

    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        return f'{node._label} + {node._offset}'

    @visitor.when(Register)
    def visit(self, node):
        return f'{node.name}'

    @visitor.when(int)
    def visit(self, node):
        return str(node)

    @visitor.when(str)
    def visit(self, node):
        return node