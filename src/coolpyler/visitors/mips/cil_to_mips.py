from dis import Instruction
from random import choice

import coolpyler.ast.cil.base as cil
import coolpyler.ast.mips.base as mips
import coolpyler.utils.visitor as visitor

REGISTER_NAMES = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9"]
ARG_REGISTERS_NAMES = ["a0", "a1", "a2", "a3"]

INSTANCE_METADATA_SIZE = 4

REGISTERS = [mips.RegisterNode(name) for name in REGISTER_NAMES]
ARG_REGISTERS = [mips.RegisterNode(name) for name in ARG_REGISTERS_NAMES]
FP_REG = mips.RegisterNode("fp")
SP_REG = mips.RegisterNode("sp")
RA_REG = mips.RegisterNode("ra")
V0_REG = mips.RegisterNode("v0")
V1_REG = mips.RegisterNode("v1")
ZERO_REG = mips.RegisterNode("zero")
LOW_REG = mips.RegisterNode("low")


class MemoryManager:
    def __init__(self):
        self.registers = REGISTERS
        self.used = []
        self.saved = []

    def get_unused_register(self):
        possibles = list(set(self.registers).difference(set(self.used)))
        reg = choice(possibles)
        self.used.append(reg)
        return reg

    def clean(self):
        self.used = self.saved
        self.saved = []

    def save(self):
        self.saved = self.used.copy()


class CilToMIPS:
    def __init__(self):
        self.data_section = dict()
        self.types = dict()
        self.memory_manager = MemoryManager()
        self.pushed_args = 0
        self.locals = []
        self.locals_save = []
        self.params = []
        self.fp_save = None
        self.loop_count = 0
        self.exit_count = 0

    def get_loop_count(self):
        self.loop_count += 1
        return self.loop_count

    def get_exit_count(self):
        self.exit_count += 1
        return self.exit_count

    def search_mem(self, id: str):
        try:
            index = self.locals.index(id)
            return -index * 4
        except ValueError:
            index = self.params.index(id)
            return index * 4

    def load_value_to_reg(self, reg, id: str):
        instructions = []
        if id.isdigit():
            instructions.append(mips.LoadInmediateNode(reg, int(id)))
        elif id == "true" or id == "false":
            instructions.append(mips.LoadInmediateNode(reg, id))
        else:
            obj1_dir = self.search_mem(id)
            instructions.append(
                mips.StoreWordNode(
                    reg, mips.MemoryAddressRegisterNode(FP_REG, obj1_dir)
                )
            )
        return instructions

    def push_arg(self):
        self.pushed_args += 1

    def clean_pushed_args(self):
        self.pushed_args = 0

    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        text_section = []
        for data in node.dotdata:
            _ = self.visit(data)

        for ty in node.dottypes:
            _ = self.visit(ty)

        for function in node.dotcode:
            instructions = self.visit(function)
            text_section.extend(instructions)

        return mips.ProgramNode(
            mips.TextNode(text_section), mips.DataSectionNode(self.data_section)
        )

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        self.types[node.name] = mips.TypeNode(node.name, node.attributes, node.methods)

        self.data_section[node.name] = mips.DataNode(
            mips.LabelNode(node.name),
            ".word",
            [mips.LabelNode(f"{method}") for method in node.methods],
        )

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        instructions = []

        self.locals_save = self.locals
        self.locals = []

        instructions.append(mips.LabelInstructionNode(node.name))

        self.memory_manager.save()
        self.fp_save = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(self.fp_save, FP_REG))
        instructions.append(mips.MoveNode(FP_REG, SP_REG))

        for i in range(len(node.params)):
            param = node.params[i]
            self.params.append(param.name)
            self.memory_manager.save()
            reg = self.memory_manager.get_unused_register()

            instructions.append(mips.LoadAddressNode(reg, (mips.LabelNode(param.name))))
            instructions.append(
                mips.StoreWordNode(reg, mips.MemoryAddressRegisterNode(SP_REG, i * 4))
            )

            self.memory_manager.clean()

        for local in node.localvars:
            instructions.extend(self.visit(local))

        # instructions.append(mips.AddiNode(SP_REG, SP_REG, -locals_size))

        for instruction in node.instructions:
            instructions.extend(self.visit(instruction))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        self.data_section[node.name] = mips.DataNode(
            mips.LabelNode(node.name), ".asciiz", [node.value]
        )

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        self.memory_manager.save()
        instructions = []
        # reg = self.memory_manager.get_unused_register()

        # self.params.append(node.name)

        # instructions.append(mips.LoadInmediateNode(reg, node.name))
        # instructions.append(
        #     mips.StoreWordNode(
        #         reg, mips.MemoryAddressRegisterNode(FP_REG, len(self.params) * 4)
        #     )
        # )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        self.memory_manager.save()
        instructions = []
        reg = self.memory_manager.get_unused_register()

        self.locals.append(node.name)

        instructions.append(mips.LoadAddressNode(reg, (mips.LabelNode(node.name))))
        instructions.append(
            mips.StoreWordNode(reg, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -4))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()

        instructions.extend(self.load_value_to_reg(reg1, node.left))
        instructions.extend(self.load_value_to_reg(reg2, node.right))

        instructions.append(mips.AddNode(reg3, reg1, reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, dest_dir),)
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()

        instructions.extend(self.load_value_to_reg(reg1, node.left))
        instructions.extend(self.load_value_to_reg(reg2, node.right))

        instructions.append(mips.SubNode(reg3, reg1, reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, dest_dir),)
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions.extend(self.load_value_to_reg(reg1, node.left))
        instructions.extend(self.load_value_to_reg(reg2, node.right))

        instructions.append(mips.MultNode(reg1, reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                LOW_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )  # TODO: HI_REG ???

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions.extend(self.load_value_to_reg(reg1, node.left))
        instructions.extend(self.load_value_to_reg(reg2, node.right))

        instructions.append(mips.DivNode(reg1, reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                LOW_REG, mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )  # TODO: HI_REG ???

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instance_dir = self.search_mem(node.instance)
        instructions.append(
            mips.LoadWordNode(
                reg1, mips.MemoryAddressRegisterNode(FP_REG, instance_dir)
            )
        )
        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressLabelNode(reg1, node.attr * 4))
        )
        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        source_dir = self.search_mem(node.source)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir))
        )
        instance_dir = self.search_mem(node.instance)
        instructions.append(
            mips.LoadWordNode(
                reg2, mips.MemoryAddressRegisterNode(FP_REG, instance_dir)
            )
        )
        instructions.append(
            mips.StoreWordNode(
                reg1, mips.MemoryAddressRegisterNode(reg2, node.attr * 4)
            )
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        instructions = []
        self.memory_manager.save()

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        instructions = []
        self.memory_manager.save()

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        instructions = []
        self.memory_manager.save()

        typ = self.types[node.type]
        reserved_bytes = (len(typ.attributes) + 1) * 4

        instructions.append(mips.LoadInmediateNode(V0_REG, 9))
        instructions.append(mips.LoadInmediateNode(ARG_REGISTERS[0], reserved_bytes))
        instructions.append(mips.SyscallNode())

        reg1 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadAddressNode(
                reg1, mips.MemoryAddressLabelNode(mips.LabelNode(node.type), 0)
            )
        )
        instructions.append(
            mips.StoreWordNode(
                reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS_NAMES[0], 0)
            )
        )
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 4))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(
                ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(FP_REG, dest_dir),
            )
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions = []

        obj_dir = self.search_mem(node.obj)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, obj_dir),)
        )

        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(reg1, -4))
        )

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir),)
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        return [mips.LabelInstructionNode(node.name)]

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):

        return [mips.JumpNode(node.label)]

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        instructions = []
        self.memory_manager.save()

        cond_dir = self.search_mem(node.cond)
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions.append(mips.LoadInmediateNode(reg1, 0))
        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, cond_dir))
        )
        instructions.append(mips.BgtNode(reg1, reg2, node.label))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        instructions = []

        instructions.append(mips.JumpAndLinkNode(node.function))

        instructions.append(mips.AddiNode(SP_REG, SP_REG, self.pushed_args * 4))
        self.clean_pushed_args()

        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        instructions = []

        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        local_dir = self.search_mem(node.type)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, local_dir),)
        )

        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(reg1, node.method))
        )

        instructions.append(mips.JumpRegisterLinkNode(reg2))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        instructions.append(mips.AddiNode(SP_REG, SP_REG, self.pushed_args * 4))
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        local_dir = self.search_mem(node.name)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, local_dir))
        )

        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, 4))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()

        value_dir = self.search_mem(node.value)
        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, value_dir))
        )

        locals_size = len(node.localvars) * 4
        instructions.append(mips.AddiNode(SP_REG, SP_REG, locals_size))

        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )

        instructions.append(mips.MoveNode(FP_REG, self.fp_save))
        self.locals = self.locals_save

        instructions.append(mips.JumpRegisterNode(RA_REG))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        instructions = []
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        if isinstance(node.msg, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.msg))
        else:
            instructions.append(mips.LoadAddressNode(reg1, node.msg))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        loop = f"loop{self.get_loop_count}"
        exit = f"exit{self.get_exit_count}"

        string_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadAddressNode(
                ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(FP_REG, string_dir)
            )
        )

        instructions.append(mips.LoadInmediateNode(reg1, 0))

        instructions.append(mips.LabelInstructionNode(mips.LabelNode(loop)))
        instructions.append(
            mips.LoadByteNode(reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0))
        )
        instructions.append(mips.BeqzNode(reg2, mips.LabelNode(exit)))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(reg1, reg1, 1))
        instructions.append(mips.JumpNode(mips.LabelNode(loop)))
        instructions.append(mips.LabelInstructionNode(mips.LabelNode(exit)))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        instructions = []
        self.memory_manager.save()

        loop1 = f"loop{self.get_loop_count}"
        exit1 = f"exit{self.get_exit_count}"
        loop2 = f"loop{self.get_loop_count}"
        exit2 = f"exit{self.get_exit_count}"

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        lenght_dir = self.search_mem(node.dest_lenght)
        instructions.append(
            mips.LoadWordNode, mips.MemoryAddressRegisterNode(FP_REG, lenght_dir)
        )
        instructions.append(mips.LoadInmediateNode(V0_REG, 9))
        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg1))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.LoadAddressNode(
                reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )

        string1_dir = self.search_mem(node.string1)
        instructions.append(
            mips.LoadAddressNode(
                ARG_REGISTERS[1], mips.MemoryAddressRegisterNode(FP_REG, string1_dir)
            )
        )
        string2_dir = self.search_mem(node.string2)
        instructions.append(
            mips.LoadAddressNode(
                ARG_REGISTERS[2], mips.MemoryAddressRegisterNode(FP_REG, string2_dir)
            )
        )

        instructions.append(mips.LabelInstructionNode(mips.LabelNode(loop1)))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[1], 0))
        )
        instructions.append(
            mips.StoreByteNode(
                reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )
        instructions.append(mips.BeqzNode(ARG_REGISTERS[1], mips.LabelNode(exit1)))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[1], ARG_REGISTERS[1], 1))
        instructions.append(mips.JumpNode(mips.LabelNode(loop1)))
        instructions.append(mips.LabelInstructionNode(mips.LabelNode(exit1)))

        instructions.append(mips.LabelInstructionNode(mips.LabelNode(loop2)))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[2], 0))
        )
        instructions.append(
            mips.StoreByteNode(
                reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )
        instructions.append(mips.BeqzNode(ARG_REGISTERS[2], mips.LabelNode(exit2)))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[2], ARG_REGISTERS[2], 1))
        instructions.append(mips.JumpNode(mips.LabelNode(loop2)))
        instructions.append(mips.LabelInstructionNode(mips.LabelNode(exit2)))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode):
        instructions = []
        self.memory_manager.save()

        loop = f"loop{self.get_loop_count}"
        exit = f"exit{self.get_exit_count}"

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()

        lenght_dir = self.search_mem(node.n)
        instructions.append(
            mips.LoadWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, lenght_dir))
        )
        instructions.append(mips.LoadInmediateNode(V0_REG, 9))
        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg1))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.LoadAddressNode(
                reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )

        string_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadAddressNode(
                ARG_REGISTERS[1], mips.MemoryAddressRegisterNode(FP_REG, string_dir)
            )
        )

        instructions.append(mips.LabelInstructionNode(mips.LabelNode(loop)))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[1], 0))
        )
        instructions.append(
            mips.StoreByteNode(
                reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )
        instructions.append(mips.BeqzNode(reg3, mips.LabelNode(exit)))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[1], ARG_REGISTERS[1], 1))
        instructions.append(mips.AddiNode(reg3, reg3, 1))
        instructions.append(mips.JumpNode(mips.LabelNode(loop)))
        instructions.append(mips.LabelInstructionNode(mips.LabelNode(exit)))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        instructions = []
        self.memory_manager.save()

        loop = f"loop{self.get_loop_count}"
        exit = f"exit{self.get_exit_count}"

        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()
        reg3 = self.memory_manager.get_unused_register()
        reg4 = self.memory_manager.get_unused_register()

        lenght_dir = self.search_mem(node.n)
        instructions.append(
            mips.LoadWordNode(reg3, mips.MemoryAddressRegisterNode(FP_REG, lenght_dir))
        )

        lenght_index = self.search_mem(node.index)
        instructions.append(
            mips.LoadWordNode(
                reg4, mips.MemoryAddressRegisterNode(FP_REG, lenght_index)
            )
        )

        instructions.append(mips.LoadInmediateNode(V0_REG, 9))
        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg1))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.LoadAddressNode(
                reg2, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )

        string_dir = self.search_mem(node.string)
        instructions.append(
            mips.LoadAddressNode(
                ARG_REGISTERS[1], mips.MemoryAddressRegisterNode(FP_REG, string_dir)
            )
        )
        instructions.append(mips.AddNode(ARG_REGISTERS[1], ARG_REGISTERS[1], reg3))

        instructions.append(mips.LabelInstructionNode(mips.LabelNode(loop)))
        instructions.append(
            mips.LoadByteNode(reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[1], 0))
        )
        instructions.append(
            mips.StoreByteNode(
                reg1, mips.MemoryAddressRegisterNode(ARG_REGISTERS[0], 0)
            )
        )
        instructions.append(mips.BeqzNode(reg3, mips.LabelNode(exit)))
        instructions.append(mips.AddiNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 1))
        instructions.append(mips.AddiNode(ARG_REGISTERS[1], ARG_REGISTERS[1], 1))
        instructions.append(mips.AddiNode(reg3, reg3, 1))
        instructions.append(mips.JumpNode(mips.LabelNode(loop)))
        instructions.append(mips.LabelInstructionNode(mips.LabelNode(exit)))

        dest_dir = self.search_mem(node.dest)
        instructions.append(
            mips.StoreWordNode(reg2, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        instructions = []
        self.memory_manager.save()

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        instructions = []
        self.memory_manager.save()

        dest_dir = self.search_mem(node.dest)

        if node.is_string:
            n = 5
        else:
            n = 8

        instructions.append(mips.LoadInmediateNode(V0_REG, n))
        instructions.append(mips.SyscallNode())
        instructions.append(
            mips.StoreWordNode(
                ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(FP_REG, dest_dir)
            )
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        instructions = []
        self.memory_manager.save()

        str_dir = self.search_mem(node.str_addr)

        if node.is_string:
            n = 4
        else:
            n = 1

        instructions.append(mips.LoadInmediateNode(V0_REG, n))
        instructions.append(
            mips.LoadWordNode(
                ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(FP_REG, str_dir)
            )
        )
        instructions.append(mips.SyscallNode())

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        instructions = []
        self.memory_manager.save()

        reg1 = self.memory_manager.get_unused_register
        source_dir = self.search_mem(node.source)
        dest_dir = self.search_mem(node.dest)

        instructions.append(
            mips.LoadWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, source_dir))
        )
        instructions.append(
            mips.StoreWordNode(reg1, mips.MemoryAddressRegisterNode(FP_REG, dest_dir))
        )

        self.memory_manager.clean()
        return instructions

    def exit_program(self):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 10))
        instructions.append(mips.SyscallNode())
        return instructions
