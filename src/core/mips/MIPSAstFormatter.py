from core.tools import visitor
from core.mips.MipsAst import *

class MIPSAstFormatter:
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):

        data = f'.data\n' + '\n.word 0\n'.join(self.visit(i) for i in node.data) + '\n'

        names_table = f"{TYPES_LABEL}:\n" + "\n".join([f"\t.word\t{tp.name}" for tp in node.types])
        proto_table = f"{PROTOTYPE_LABEL}:\n" + "\n".join([f"\t.word\t{tp.label}_prototype" for tp in node.types])

        types = "\n\n\n".join([self.visit(tp) for tp in node.types])
        code = '\n\n'.join(self.visit(i) for i in node.functions) + '\n'

        mipsCode = f'{data}\n\n{names_table}\n\n{proto_table}\n\n{types}\n\n\n.text\n.globl main\n{code}\n\n'

        with open('core/mips/mips_basics.asm', 'r') as f:
            mipsCode += "".join(f.readlines())
        return mipsCode


    @visitor.when(MIPSType)
    def visit(self, node):
        methods = "\n".join([f"\t.word\t {m}" for m in node.methods])
        dispatch_table = f"{node.label}_dispatch:\n{methods}"
        proto_begin = f"{node.label}_prototype:\n\t.word\t{node.index}\n\t.word\t{node.size}\n\t.word\t{node.label}_dispatch"
        proto_attr = "\n".join([f'\t.word\t0' for attr in node.attributes])
        proto_end = f"\t.word\t-1"
        proto = f"{proto_begin}\n{proto_attr}\n{proto_end}" if proto_attr != "" else f"{proto_begin}\n{proto_end}"

        return f'{dispatch_table}\n\n{proto}'

    @visitor.when(FunctionNode)
    def visit(self, node):
        return f'{node.label}:\n\t' + \
               f'\n\t'.join(self.visit(i) for i in node.instructions)

    @visitor.when(AbsoluteNode)
    def visit(self, node):
        return f'abs {self.visit(node.rdest)} {self.visit(node.rsrc)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(AdditionNode)
    def visit(self, node):
        return f'add {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(AdditionInmediateNode)
    def visit(self, node):
        return f'addi {self.visit(node.rdest)} {self.visit(node.rsrc)} {self.visit(node.imm)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(DivideNode)
    def visit(self, node):
        return f'div {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(MultiplyNode)
    def visit(self, node):
        return f'mul {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(NegateNode)
    def visit(self, node):
        return f'neg {self.visit(node.rdest)} {self.visit(node.rsrc1)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(SubstractionNode)
    def visit(self, node):
        return f'sub {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LessNode)
    def visit(self, node):
        return f'slt {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LessInmediateNode)
    def visit(self, node):
        return f'slti {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.imm)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(EqualNode)
    def visit(self, node):
        return f'seq {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LessEqualNode)
    def visit(self, node):
        return f'sle {self.visit(node.rdest)} {self.visit(node.rsrc1)} {self.visit(node.rsrc2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(JumpNode)
    def visit(self, node):
        return f'j {self.visit(node.label)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(JumpRegisterNode)
    def visit(self, node):
        return f'jr {self.visit(node.reg)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(JalNode)
    def visit(self, node):
        return f'jal {self.visit(node.label)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(JalrNode)
    def visit(self, node):
        return f'jalr {self.visit(node.reg1)} {self.visit(node.reg2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(MoveNode)
    def visit(self, node):
        return f'move {self.visit(node.reg1)} {self.visit(node.reg2)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(StoreWordNode)
    def visit(self, node):
        return f'sw {self.visit(node.reg)} {self.visit(node.addr)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LoadInmediateNode)
    def visit(self, node):
        return f'li {self.visit(node.reg)} {self.visit(node.value)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LoadWordNode)
    def visit(self, node):
        return f'lw {self.visit(node.reg)} {self.visit(node.addr)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        return f'la {self.visit(node.reg)} {self.visit(node.label)}'

    @visitor.when(BranchOnNotEqualNode)
    def visit(self, node):
        return f'bne {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.label)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(LabelNode)
    def visit(self, node):
        return f'{self.visit(node.name)}:'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(NotNode)
    def visit(self, node):
        return f'xori {self.visit(node.dest)} {self.visit(node.src)} 1'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(ComplementNode)
    def visit(self, node):
        return f'not {self.visit(node.dest)} {self.visit(node.src)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(MoveLowNode)
    def visit(self, node):
        return f'mflo {self.visit(node.dest)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(MoveHighNode)
    def visit(self, node):
        return f'mfhi {self.visit(node.dest)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(ShiftLeftNode)
    def visit(self, node):
        return f'sll {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.bits)}'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(SyscallNode)
    def visit(self, node):
        return 'syscall'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'.ljust(50) + \
               f'#line: {node.line} column: {node.column}'

    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        return f'{node._offset}({self.visit(node._register)})'

    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        return f'{node._label}'

    @visitor.when(Register)
    def visit(self, node):
        return f'${node.name}'

    @visitor.when(int)
    def visit(self, node):
        return str(node)

    @visitor.when(str)
    def visit(self, node):
        return node