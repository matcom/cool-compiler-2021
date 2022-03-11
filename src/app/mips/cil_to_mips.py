import app.shared.visitor as visitor
import app.cil.cil as cil
from app.mips import mips
from app.mips.utils import *



class CILToMIPSVisitor:
    def __init__(self):
        self._types = {}
        self._data_section = {}
        self._functions = {}
        self._actual_function = None
        self._name_func_map = {}
        self._pushed_args = 0
        self._labels_map = {}

    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)

    def register_function(self, name, function):
        self._functions[name] = function

    def init_function(self, function):
        self._actual_function = function
        self._labels_map = {}

    def finish_functions(self):
        self._actual_function = None

    def push_arg(self):
        self._pushed_args += 1

    def clean_pushed_args(self):
        self._pushed_args = 0

    def in_entry_function(self):
        return self._actual_function.label == 'main'

    def register_label(self, cil_label, mips_label):
        self._labels_map[cil_label] = mips_label

    def get_mips_label(self, label):
        return self._labels_map[label]

    @visitor.on('node')
    def collect_labels_in_func(self, node):
        pass

    @visitor.when(cil.LabelNode)
    def collect_labels_in_func(self, node):
        self.register_label(node.label, f'{self._actual_function.label}_{node.label}')


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.InstructionNode)
    def visit(self, node):
        print(type(node))

    @visitor.when(cil.ProgramNode)
    def visit(self, node:cil.ProgramNode):        
        return cil.ProgramNode.visit(node,self,mips) 

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        cil.TypeNode.visit(node,self,mips)

    @visitor.when(cil.DataNode)
    def visit(self, node):
        cil.DataNode.visit(node,self,mips)

    @visitor.when(cil.FunctionNode)
    def visit(self, node:cil.FunctionNode):
        cil.FunctionNode.visit(node,self,mips)

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        return cil.ArgNode.visit(node,self,mips)

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        return cil.StaticCallNode.visit(node,self,mips)

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        return cil.AssignNode.visit(node,self,mips)

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        return cil.AllocateNode.visit(node,self,mips)

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        return cil.ReturnNode.visit(node,self,mips)

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        return cil.LoadNode.visit(node,self,mips)

    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        return cil.PrintIntNode.visit(node,self,mips)

    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        return cil.PrintStrNode.visit(node,self,mips)

    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        return cil.TypeNameNode.visit(node,self,mips)

    @visitor.when(cil.ExitNode)
    def visit(self, node):
        return cil.ExitNode.visit(node,self,mips)

    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        return cil.GetAttribNode.visit(node,self,mips)

    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        return cil.SetAttribNode.visit(node,self,mips)

    @visitor.when(cil.CopyNode)
    def visit(self, node):
        return cil.CopyNode.visit(node,self,mips)

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        return cil.EqualNode.visit(node,self,mips)

    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        return cil.EqualStrNode.visit(node,self,mips)

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return cil.LabelNode.visit(node,self,mips)

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        return cil.GotoIfNode.visit(node,self,mips)

    @visitor.when(cil.GotoNode)
    def visit(self, node):
        return cil.GotoNode.visit(node,self,mips)

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        return cil.TypeOfNode.visit(node,self,mips)


    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        return cil.DynamicCallNode.visit(node,self,mips)


    @visitor.when(cil.ErrorNode)
    def visit(self, node):
        return cil.ErrorNode.visit(node,self,mips)

    @visitor.when(cil.NameNode)
    def visit(self, node):
        return cil.NameNode.visit(node,self,mips)

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        return cil.PlusNode.visit(node,self,mips)
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        return cil.MinusNode.visit(node,self,mips)

    @visitor.when(cil.StarNode)
    def visit(self, node):
        return cil.StarNode.visit(node,self,mips)

    @visitor.when(cil.DivNode)
    def visit(self, node):
        return cil.DivNode.visit(node,self,mips)

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        return cil.ComplementNode.visit(node,self,mips)

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        return cil.LessEqualNode.visit(node,self,mips)

    @visitor.when(cil.LessNode)
    def visit(self, node):
        return cil.LessNode.visit(node,self,mips)

    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        return cil.ReadStrNode.visit(node,self,mips)

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        return cil.LengthNode.visit(node,self,mips)

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        return cil.ReadIntNode.visit(node,self,mips)

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        return cil.ConcatNode.visit(node,self,mips)

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        return cil.SubstringNode.visit(node,self,mips)


class MIPSCode:
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(mips.Register)
    def visit(self, node):
        return f'${node.name}'

    @visitor.when(int)
    def visit(self, node):
        return str(node)

    @visitor.when(str)
    def visit(self, node):
        return node

    @visitor.when(mips.ProgramNode)
    def visit(self, node):
        data_section_header = "\t.data"
        static_strings = '\n'.join([self.visit(string_const)
                                    for string_const in node.data])

        names_table = f"{mips.TYPENAMES_TABLE_LABEL}:\n" + \
            "\n".join(
                [f"\t.word\t{tp.string_name_label}" for tp in node.types])
        shells_table = f"{mips.SHELLS_TABLE_LABEL}:\n" + \
            "\n".join([f"\t.word\t{tp.label}_shell" for tp in node.types])

        types = "\n\n".join([self.visit(tp) for tp in node.types])

        code = "\n".join([self.visit(func) for func in node.functions])

        auxiliar = self.register_auxiliary()
        return f'{data_section_header}\n{static_strings}\n\n{names_table}\n\n{shells_table}\n\n{types}\n\t.text\n\t.globl main\n{code}\n{auxiliar}'

    @visitor.when(mips.StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'

    @visitor.when(mips.MIPSType)
    def visit(self, node):
        methods = "\n".join(
            [f"\t.word\t {node.methods[k]}" for k in node.methods])
        dispatch_table = f"{node.label}_dispatch:\n{methods}"
        shell_begin = f"{node.label}_shell:\n\t.word\t{node.index}\n\t.word\t{node.size}\n\t.word\t{node.label}_dispatch"
        shell_attr = "\n".join(
            [f'\t.word\t{node._default_attributes.get(attr, "0")}' for attr in node.attributes])

        shell = f"{shell_begin}\n{shell_attr}\n" if shell_attr != "" else f"{shell_begin}\n"

        return f'{dispatch_table}\n\n{shell}'

    @visitor.when(mips.SyscallNode)
    def visit(self, node):
        return 'syscall'

    @visitor.when(mips.LabelRelativeLocation)
    def visit(self, node):
        return f'{node.label} + {node.offset}'

    @visitor.when(mips.RegisterRelativeLocation)
    def visit(self, node):
        return f'{node.offset}({self.visit(node.register)})'

    @visitor.when(mips.FunctionNode)
    def visit(self, node):
        
        instr = [self.visit(instruction) for instruction in node.instructions]
        # TODO la linea de abajo sobra, es necesaria mientras la traduccion del AST de CIL este incompleta
        instr2 = [inst for inst in instr if type(inst) == str]
        instructions = "\n\t".join(instr2)
        return f'{node.label}:\n\t{instructions}'

    @visitor.when(mips.AddInmediateNode)
    def visit(self, node):
        if f'addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.value)}' == 'addi $sp, $sp, 8':
            a= 5
        return f'addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.value)}'

    @visitor.when(mips.StoreWordNode)
    def visit(self, node):
        return f'sw {self.visit(node.reg)}, {self.visit(node.addr)}'

    @visitor.when(mips.LoadInmediateNode)
    def visit(self, node):
        return f'li {self.visit(node.reg)}, {self.visit(node.value)}'

    @visitor.when(mips.JumpAndLinkNode)
    def visit(self, node):
        return f'jal {node.label}'

    @visitor.when(mips.JumpRegister)
    def visit(self, node):
        return f'jr {self.visit(node.reg)}'

    @visitor.when(mips.JumpRegisterAndLinkNode)
    def visit(self, node):
        return f'jalr {self.visit(node.reg)}'

    @visitor.when(mips.LoadWordNode)
    def visit(self, node):
        return f'lw {self.visit(node.reg)}, {self.visit(node.addr)}'

    @visitor.when(mips.LoadByteNode)
    def visit(self, node):
        return f'lb {self.visit(node.reg)}, {self.visit(node.addr)}'

    @visitor.when(mips.LoadAddressNode)
    def visit(self, node):
        return f'la {self.visit(node.reg)}, {self.visit(node.label)}'

    @visitor.when(mips.MoveNode)
    def visit(self, node):
        return f'move {self.visit(node.reg1)} {self.visit(node.reg2 )}'

    @visitor.when(mips.ShiftLeftLogicalNode)
    def visit(self, node):
        return f"sll {self.visit(node.dest)} {self.visit(node.src)} {node.bits}"

    @visitor.when(mips.AddInmediateUnsignedNode)
    def visit(self, node):
        return f"addiu {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.value)}"

    @visitor.when(mips.AddUnsignedNode)
    def visit(self, node):
        return f"addu {self.visit(node.dest)} {self.visit(node.sum1)} {self.visit(node.sum2)}"

    @visitor.when(mips.LabelNode)
    def visit(self, node):
        return f"{node.name}:"

    @visitor.when(mips.BranchOnNotEqualNode)
    def visit(self, node):
        return f"bne {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"
    
    @visitor.when(mips.BranchOnEqualNode)
    def visit(self, node):
        return f"beq {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"

    @visitor.when(mips.BranchOnLessEqualNode)
    def visit(self, node):
        return f"ble {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"

    @visitor.when(mips.BranchOnLessThanNode)
    def visit(self, node):
        return f"blt {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"

    @visitor.when(mips.JumpNode)
    def visit(self, node):
        return f"j {node.label}"

    @visitor.when(mips.AddNode)
    def visit(self, node):
        return f"add {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(mips.SubNode)
    def visit(self, node):
        return f"sub {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(mips.MultiplyNode)
    def visit(self, node):
        return f"mul {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(mips.DivideNode)
    def visit(self, node):
        return f"div {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(mips.ComplementNode)
    def visit(self, node):
        return f"not {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(mips.MoveFromLowNode)
    def visit(self, node):
        return f"mflo {self.visit(node.reg)}"
    
    def register_auxiliary(self):
        return memory_operations + boolean_operations + string_operations + IO_operations    
