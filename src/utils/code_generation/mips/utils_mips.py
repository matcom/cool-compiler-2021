from collections import defaultdict
import cmp.visitor as visitor
from utils.code_generation.cil.AST_CIL import cil_ast as cil
from utils.code_generation.mips.AST_MIPS import mips_ast as mips
from utils.code_generation.mips.AST_MIPS import mips_ast as nodes
from utils.code_generation.mips.AST_MIPS import *
from random import choice


def push_register(reg):
    move_stack = nodes.AddInmediateNode(SP_REG, SP_REG, -4)
    save_location = RegisterRelativeLocation(SP_REG, 0)
    save_register = nodes.StoreWordNode(reg, save_location)
    return [move_stack, save_register]


def pop_register(reg):
    load_value = nodes.LoadWordNode(reg, RegisterRelativeLocation(SP_REG, 0))
    move_stack = nodes.AddInmediateNode(SP_REG, SP_REG, 4)
    return [load_value, move_stack]


def alloc_memory(size):
    instructions = []
    instructions.append(nodes.LoadInmediateNode(V0_REG, 9))
    instructions.append(nodes.LoadInmediateNode(ARG_REGISTERS[0], size))
    instructions.append(nodes.SyscallNode())
    return instructions


def exit_program():
    instructions = []
    instructions.append(nodes.LoadInmediateNode(V0_REG, 10))
    instructions.append(nodes.SyscallNode())
    return instructions


def create_object(reg1, reg2):
    instructions = []

    instructions.append(nodes.ShiftLeftLogicalNode(reg1, reg1, 2))
    instructions.append(nodes.LoadAddressNode(reg2, "proto_table"))
    instructions.append(nodes.AddUnsignedNode(reg2, reg2, reg1))
    instructions.append(nodes.LoadWordNode(
        reg2, RegisterRelativeLocation(reg2, 0)))
    instructions.append(nodes.LoadWordNode(
        ARG_REGISTERS[0], RegisterRelativeLocation(reg2, 4)))
    instructions.append(nodes.ShiftLeftLogicalNode(
        ARG_REGISTERS[0], ARG_REGISTERS[0], 2))
    instructions.append(nodes.JumpAndLinkNode("malloc"))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[2], ARG_REGISTERS[0]))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[0], reg2))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[1], V0_REG))
    instructions.append(nodes.JumpAndLinkNode("copy"))

    return instructions


def copy_object(reg1, reg2):
    instructions = []

    instructions.append(nodes.LoadWordNode(
        ARG_REGISTERS[0], RegisterRelativeLocation(reg1, 4)))
    instructions.append(nodes.ShiftLeftLogicalNode(
        ARG_REGISTERS[0], ARG_REGISTERS[0], 2))
    instructions.append(nodes.JumpAndLinkNode("malloc"))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[2], ARG_REGISTERS[0]))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[0], reg1))
    instructions.append(nodes.MoveNode(ARG_REGISTERS[1], V0_REG))
    instructions.append(nodes.JumpAndLinkNode("copy"))

    return instructions


class MemoryManager:
    def __init__(self, registers, function_for_assign):
        self.registers = registers
        self.func = function_for_assign

    def get_reg_for_var(self, var):
        index = self.func(var)
        if index == -1:
            return None
        return self.registers[index]

    def get_reg_unusued(self, used=[]):
        possibles = list(set(self.registers).difference(set(used)))
        return choice(possibles)


class LabelGenerator:
    def __init__(self):
        self.data_count = 0
        self.type_count = 0
        self.code_count = 0

    def generate_type_label(self):
        self.type_count += 1
        return f'type_{self.type_count}'

    def generate_data_label(self):
        self.data_count += 1
        return f'data_{self.data_count}'

    def generate_code_label(self):
        self.code_count += 1
        return f'L_{self.code_count}'


class UsedRegisterFinder:
    def __init__(self):
        self.used_registers = set()

    def get_used_registers(self, instructions):
        self.used_registers = set()

        for inst in instructions:
            self.visit(inst)
        self.used_registers = set.difference(
            self.used_registers, set([SP_REG, Register('fp'), V0_REG]))
        return [reg for reg in self.used_registers]

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(mips.LoadInmediateNode)
    def visit(self, node):
        self.used_registers.add(node.reg)

    @visitor.when(mips.LoadAddressNode)
    def visit(self, node):
        self.used_registers.add(node.reg)

    @visitor.when(mips.AddInmediateNode)
    def visit(self, node):
        self.used_registers.add(node.dest)

    @visitor.when(mips.MoveNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)

    @visitor.when(mips.LoadWordNode)
    def visit(self, node):
        self.used_registers.add(node.reg)

    @visitor.when(mips.JumpAndLinkNode)
    def visit(self, node):
        self.used_registers.add(RA_REG)

    @visitor.when(mips.JumpRegisterAndLinkNode)
    def visit(self, node):
        self.used_registers.add(RA_REG)

    @visitor.when(mips.AddUnsignedNode)
    def visit(self, node):
        self.used_registers.add(node.dest)

    @visitor.when(mips.ShiftLeftLogicalNode)
    def visit(self, node):
        self.used_registers.add(node.dest)

    @visitor.when(mips.AddNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)

    @visitor.when(mips.SubNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)

    @visitor.when(mips.MultiplyNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)

    @visitor.when(mips.ComplementNode)
    def visit(self, node):
        self.used_registers.add(node.reg1)

    @visitor.when(mips.MoveFromLowNode)
    def visit(self, node):
        self.used_registers.add(node.reg)


class RegistersAllocator:
    def __init__(self):
        self.mark = False

    def get_registers_for_variables(self, instructions, params, n):
        self.numbered_instructions(instructions)
        basic_blocks = self.divide_basics_blocks(instructions)
        flow_graph = RegistersAllocator.create_flow_graph(basic_blocks)
        gk, io = self.liveness_analysis((basic_blocks, flow_graph), params)
        interference = RegistersAllocator.interference_compute(gk, io)
        return RegistersAllocator.assign_registers(interference, n)

    def divide_basics_blocks(self, instructions):
        self.mark = True
        for instruction in instructions:
            self.mark_leaders(instruction)

        blocks = []

        for instruction in instructions:
            if instruction.leader:
                blocks.append([instruction])
            else:
                blocks[-1].append(instruction)

        return blocks

    def liveness_analysis(self, graph, params):
        blocks, ady_list = graph

        instructions = []
        for block in blocks:
            instructions.extend(block)
        instructions_total = len(instructions)

        suc = [0 for _ in range(instructions_total)]
        for block_index, block in enumerate(blocks):
            for ins_index, instruction in enumerate(block):
                if ins_index == len(block) - 1:
                    ady = [i for i in range(len(blocks))
                           if ady_list[block_index][i] == 1]
                    suc[instruction.number] = [
                        blocks[b][0].number for b in ady]
                else:
                    suc[instruction.number] = [block[ins_index + 1].number]

        gk = [self.gen_kill(inst) for inst in instructions]
        io = RegistersAllocator.out_in_compute(suc, gk)
        gk = [([], [param.id for param in params])] + gk
        io = [([], io[0][0])] + io

        return gk, io

    @staticmethod
    def interference_compute(gk, in_out):
        neigs = {}
        for g, k in gk:
            for v in g:
                neigs[v] = set()
            for v in k:
                neigs[v] = set()

        for i, (_, k) in enumerate(gk):
            for v in k:
                neigs[v].update(in_out[i][1])

        for k, v in neigs.items():
            for n in v:
                neigs[n].add(k)

        for k, v in neigs.items():
            neigs[k] = list(v.difference([k]))

        return neigs

    @staticmethod
    def assign_registers(interference_graph, n):
        stack = []
        var_registers = defaultdict(lambda: -1)
        nodes = set(interference_graph.keys())

        def myLen(l):
            count = 0
            for v in l:
                if v in nodes:
                    count += 1
            return count

        while nodes:
            to_remove = None
            for node in nodes:
                if myLen(interference_graph[node]) < n:
                    stack.append((node, interference_graph[node]))
                    to_remove = node
                    break

            if to_remove:
                nodes.remove(to_remove)
            else:
                selection = choice(list(nodes))
                stack.append((selection, interference_graph[selection]))
                nodes.remove(selection)

        while stack:
            node, ady = stack.pop()
            regs = set(range(n))
            for neig in ady:
                reg = var_registers[neig]
                if reg != -1:
                    try:
                        regs.remove(reg)
                    except:
                        pass
            if regs:
                var_registers[node] = min(regs)
            else:
                var_registers[node] = -1

        return var_registers

    @staticmethod
    def out_in_compute(suc, gk):
        n_instructions = len(gk)
        in_out = [[set(), set()] for _ in range(n_instructions)]
        next_in_out = [[set(), set()] for _ in range(n_instructions)]

        def add(set1, set2):
            return not set2.issubset(set1)

        changed = True
        while changed:
            changed = False
            for i in range(n_instructions)[::-1]:
                for i_suc in suc[i]:
                    if i_suc < i:
                        changed |= add(next_in_out[i][1], in_out[i_suc][0])
                        next_in_out[i][1] = next_in_out[i][1].union(
                            in_out[i_suc][0])
                    else:
                        changed |= add(
                            next_in_out[i][1], next_in_out[i_suc][0])
                        next_in_out[i][1] = next_in_out[i][1].union(
                            next_in_out[i_suc][0])

                g_i = set(gk[i][0])
                k_i = set(gk[i][1])
                new = g_i.union(next_in_out[i][1].difference(k_i))
                changed |= add(next_in_out[i][0], new)
                next_in_out[i][0] = next_in_out[i][0].union(new)

            in_out = next_in_out

        return in_out

    @staticmethod
    def create_flow_graph(blocks):
        graph = [[-1 for _ in range(len(blocks))] for _ in range(len(blocks))]
        labels = {b[0].label: i for i, b in enumerate(
            blocks) if isinstance(b[0], cil.LabelNode)}

        for i, block in enumerate(blocks):
            if isinstance(block[-1], cil.GotoNode):
                graph[i][labels[block[-1].label]] = 1
            elif isinstance(block[-1], cil.IfGotoNode):
                graph[i][labels[block[-1].label]] = 1
                graph[i][i + 1] = 1 if i + 1 < len(blocks) else -1
            elif i != len(blocks) - 1:
                graph[i][i + 1] = 1

        return graph

    @staticmethod
    def numbered_instructions(instructions):
        for i, instr in enumerate(instructions):
            instr.number = i

    @visitor.on('instruction')
    def gen_kill(self, instruction):
        pass

    @visitor.when(cil.ArgNode)
    def gen_kill(self, instruction):
        if isinstance(instruction.id, int):
            return ([], [])
        return ([instruction.id], [])

    @visitor.when(cil.StaticCallNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.AssignNode)
    def gen_kill(self, instruction):
        gen = []
        if isinstance(instruction.right, str):
            if not instruction.right.isnumeric():
                gen = [instruction.right]
        return (gen, [instruction.left])

    @visitor.when(cil.AllocateNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.ReturnNode)
    def gen_kill(self, instruction):
        gen = [instruction.id] if isinstance(instruction.id, str) else []
        return (gen, [])

    @visitor.when(cil.LoadNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.PrintIntNode)
    def gen_kill(self, instruction):
        return ([instruction.value], [])

    @visitor.when(cil.PrintStrNode)
    def gen_kill(self, instruction):
        return ([instruction.value], [])

    @visitor.when(cil.TypeNameNode)
    def gen_kill(self, instruction):
        return ([instruction.type], [instruction.dest])

    @visitor.when(cil.AbortNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.when(cil.GetAttrNode)
    def gen_kill(self, instruction):
        return ([instruction.id], [instruction.dest])

    @visitor.when(cil.SetAttrNode)
    def gen_kill(self, instruction):
        gen = [instruction.id]
        if not isinstance(instruction.value, int):
            gen.append(instruction.value)
        return (gen, [])

    @visitor.when(cil.CopyNode)
    def gen_kill(self, instruction):
        return ([instruction.copy], [instruction.dest])

    @visitor.when(cil.ArithmeticNode)
    def gen_kill(self, instruction):
        gen = [x for x in [instruction.op_l,
                           instruction.op_r] if isinstance(x, str)]
        return (gen, [instruction.dest])

    @visitor.when(cil.IfGotoNode)
    def gen_kill(self, instruction):
        return ([instruction.if_cond], [])

    @visitor.when(cil.GotoNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.when(cil.TypeOfNode)
    def gen_kill(self, instruction):
        return ([instruction.id], [instruction.dest])

    @visitor.when(cil.DynamicCallNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.NameNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.ComplementNode)
    def gen_kill(self, instruction):
        gen = [instruction.id] if isinstance(instruction.id, str) else []
        return (gen, [instruction.dest])

    @visitor.when(cil.ReadStrNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.LengthNode)
    def gen_kill(self, instruction):
        return ([instruction.id], [instruction.dest])

    @visitor.when(cil.ReadIntNode)
    def gen_kill(self, instruction):
        return ([], [instruction.dest])

    @visitor.when(cil.ConcatNode)
    def gen_kill(self, instruction):
        return ([instruction.s1, instruction.s2], [instruction.dest])

    @visitor.when(cil.SubstringNode)
    def gen_kill(self, instruction):
        gen = [instruction.s]
        if isinstance(instruction.i, str):
            gen.append(instruction.i)
        if isinstance(instruction.length, str):
            gen.append(instruction.length)

        return (gen, [instruction.dest])

    @visitor.when(cil.LabelNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.when(cil.ErrorNode)
    def gen_kill(self, instruction):
        return ([], [])

    @visitor.on('instruction')
    def mark_leaders(self, instruction):
        pass

    @visitor.when(cil.LabelNode)
    def mark_leaders(self, instruction):
        instruction.leader = True
        self.mark = False

    @visitor.when(cil.GotoNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = True

    @visitor.when(cil.IfGotoNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = True

    @visitor.when(cil.InstructionNode)
    def mark_leaders(self, instruction):
        instruction.leader = self.mark
        self.mark = False


class MIPSType:
    def __init__(self, label, name_addr, attributes, methods, index, default=[]):
        self._label = label
        self._name = name_addr
        self._attributes = attributes
        self._default_attributes = dict(default)
        self._methods = methods
        self._index = index

    @property
    def size(self):
        return len(self.attributes) + 4

    @property
    def label(self):
        return self._label

    @property
    def string_name_label(self):
        return self._name

    @property
    def methods(self):
        return self._methods

    @property
    def attributes(self):
        return self._attributes

    @property
    def index(self):
        return self._index