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
        self.saved = self.used


class CilToMIPS:
    def __init__(self):
        self.data_section = dict()
        self.types = dict()
        self.memory_manager = MemoryManager()
        self.pushed_args = 0
        self.locals = []
        self.params = []

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
            node.name, ".word", [mips.LabelNode(method.name) for method in node.methods]
        )

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        instructions = []

        locals_save = self.locals
        self.locals = []

        self.memory_manager.save()
        old_fp = self.memory_manager.get_unused_register()
        instructions.append(mips.MoveNode(old_fp, FP_REG))
        instructions.append(mips.MoveNode(FP_REG, SP_REG))

        instructions.append(mips.LabelInstructionNode(node.name))
        self.memory_manager.clean()

        for i in range(len(node.params)):
            param = node.params[i]
            self.params.append(param.name)
            self.memory_manager.save()
            reg = self.memory_manager.get_unused_register()

            instructions.append(mips.LoadInmediateNode(reg, param.name))
            instructions.append(
                mips.StoreWordNode(reg, mips.MemoryAddressRegisterNode(SP_REG, i * 4))
            )

            self.memory_manager.clean()

        locals_size = len(node.localvars) * 4

        for local in node.localvars:
            instructions.extend(self.visit(local))

        # instructions.append(mips.AddiNode(SP_REG, SP_REG, -locals_size))

        for instruction in node.instructions:
            instructions.extend(self.visit(instruction))

        instructions.append(mips.AddiNode(SP_REG, SP_REG, locals_size))

        if node.name == "main":
            instructions.extend(self.exit_program())
        else:
            instructions.append(mips.JumpRegisterNode(RA_REG))

        instructions.append(mips.MoveNode(FP_REG, old_fp))
        self.locals = locals_save
        return instructions

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        self.data_section[node.name] = mips.DataNode(
            mips.LabelNode(node.name), ".asciiz", [node.value]
        )

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        self.memory_manager.save()
        reg = self.memory_manager.get_unused_register()

        self.locals.append(node.name)
        instructions = []

        instructions.append(mips.LoadInmediateNode(reg, node.name))
        instructions.append(
            mips.StoreWordNode(reg, mips.MemoryAddressRegisterNode(SP_REG, 0))
        )
        instructions.append(mips.AddiNode(SP_REG, SP_REG, -4))

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        pass

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        pass

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        pass

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        pass

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        pass

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        pass

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        pass

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        pass

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        instructions = []
        dest_index = self.locals[node.dest].index()
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        typ = self.types[node.type]
        reserved_bytes = (len(typ.attributes) + 1) * 4

        instructions.append(mips.LoadInmediateNode(V0_REG, 9))
        instructions.append(mips.LoadInmediateNode(ARG_REGISTERS[0], reserved_bytes))
        instructions.append(mips.SyscallNode())

        instructions.append(
            mips.StoreWordNode(
                ARG_REGISTERS[0],
                mips.MemoryAddressRegisterNode(
                    FP_REG, len(self.params) * 4 + dest_index * 4
                ),
            )
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        obj_index = self.locals[node.obj].index()
        dest_index = self.locals[node.dest].index()

        self.memory_manager.save()
        reg = self.memory_manager.get_unused_register()

        instructions = []

        instructions.append(
            mips.LoadWordNode(
                reg,
                mips.MemoryAddressRegisterNode(
                    FP_REG, len(self.params) * 4 + obj_index * 4
                ),
            )
        )
        instructions.append(
            mips.StoreWordNode(
                reg,
                mips.MemoryAddressRegisterNode(
                    FP_REG, len(self.params) * 4 + dest_index * 4
                ),
            )
        )

        self.memory_manager.clean()

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        pass

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        pass

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        pass

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
        local_index = self.locals[node.type].index()

        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()
        reg2 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(
                    FP_REG, len(self.params) * 4 + local_index * 4
                ),
            )
        )

        instructions.append(
            mips.LoadWordNode(reg2, mips.MemoryAddressRegisterNode(reg1, node.method))
        )

        instructions.append(mips.JumpRegisterLinkNode(reg2))

        instructions.append(mips.AddiNode(SP_REG, SP_REG, self.pushed_args * 4))
        self.clean_pushed_args()

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        instructions = []
        local_index = self.locals[node.name].index()
        self.memory_manager.save()
        reg1 = self.memory_manager.get_unused_register()

        instructions.append(
            mips.LoadWordNode(
                reg1,
                mips.MemoryAddressRegisterNode(
                    FP_REG, len(self.params) * 4 + local_index * 4
                ),
            )
        )

        instructions.append(
            mips.StoreWordNode(
                ARG_REGISTERS[0], mips.MemoryAddressRegisterNode(SP_REG, 0),
            )
        )

        self.memory_manager.clean()
        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        pass

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        pass

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        pass

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        pass

    @visitor.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode):
        pass

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        pass

    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        pass

    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        pass

    def exit_program(self):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 10))
        instructions.append(mips.SyscallNode())
        return instructions
