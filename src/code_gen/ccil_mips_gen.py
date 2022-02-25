from typing import Tuple, Union, Dict, List
from utils import visitor
from asts import mips_ast, ccil_ast
from utils import visitor
from .constants import *

WORD = 4
DOUBLE_WORD = 8
Location = Dict[Tuple[str, str], mips_ast.MemoryIndexNode]


class CCILToMIPSGenerator:
    def __init__(self) -> None:
        self.__types_table: List[ccil_ast.Class] = []  # list or dict for classes???
        self.__location: Location = {}
        self.__current_function: ccil_ast.FunctionNode

    def push_stack(self, node, register: mips_ast.RegisterNode):
        stack_pointer = mips_ast.RegisterNode(node, SP)
        instructions = []
        instructions.append(
            mips_ast.Addi(
                node,
                stack_pointer,
                stack_pointer,
                mips_ast.Constant(node, -1 * DOUBLE_WORD),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                register,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), stack_pointer
                ),
            )
        )
        return instructions

    def pop_stack(self, node, register: mips_ast.RegisterNode):
        stack_pointer = mips_ast.RegisterNode(node, SP)
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                register,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), stack_pointer
                ),
            )
        )
        instructions.append(
            mips_ast.Addi(
                node, stack_pointer, stack_pointer, mips_ast.Constant(node, DOUBLE_WORD)
            )
        )
        return instructions

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ccil_ast.CCILProgram)
    def visit(self, node: ccil_ast.CCILProgram):
        self.__types_table = node.types_section
        types_table = []
        for classx in node.types_section:
            word_directive = [
                mips_ast.Label(node, classx.id),
                mips_ast.Label(node, classx.init_operations.id),
            ]
            for method in classx.methods:
                word_directive.append(mips_ast.Label(node, method.function.id))
            types_table.append(
                (
                    mips_ast.LabelDeclaration(node, classx.id),
                    mips_ast.WordDirective(node, word_directive),
                )
            )

        # TODO: other .data section static data inicializations like strings

        functions = []
        functions.extend(self.visit(node.entry_func))
        functions.extend(
            [self.visit(func) for func in node.code_section if func.id == "main"][0]
        )

        for classx in node.types_section:
            functions.extend(self.visit(classx.init_operations))
        for func in node.code_section:
            if func.id != "main":
                functions.extend(self.visit(func))

        return mips_ast.MIPSProgram(
            None,
            mips_ast.TextNode(node, functions),
            mips_ast.DataNode(node, types_table),
        )

    @visitor.when(ccil_ast.FunctionNode)
    def visit(self, node: ccil_ast.FunctionNode):
        self.__current_function = node
        instructions = []
        instructions.append(mips_ast.LabelDeclaration(node, node.id))

        frame_size = (len(node.locals)) * DOUBLE_WORD + 2 * DOUBLE_WORD
        stack_pointer = mips_ast.RegisterNode(node, SP)
        return_address = mips_ast.RegisterNode(node, RA)
        frame_pointer = mips_ast.RegisterNode(node, FP)

        index = 0
        for param in reversed(node.locals):
            self.set_relative_location(
                param.id,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, -1 * index), frame_pointer
                ),
            )
            index += DOUBLE_WORD
        index = DOUBLE_WORD
        for local in node.params:
            self.set_relative_location(
                local.id,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, index), frame_pointer
                ),
            )
            index += DOUBLE_WORD

        instructions.append(
            mips_ast.Subu(
                node, stack_pointer, stack_pointer, mips_ast.Constant(node, frame_size)
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                return_address,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, frame_size - DOUBLE_WORD),
                    stack_pointer,
                ),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                frame_pointer,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, frame_size - 2 * DOUBLE_WORD),
                    stack_pointer,
                ),
            )
        )
        instructions.append(
            mips_ast.Addu(
                node,
                frame_pointer,
                stack_pointer,
                mips_ast.Constant(node, frame_size - DOUBLE_WORD),
            )
        )

        for op in node.operations:
            instructions.extend(self.visit(op))

        ret_location = self.get_relative_location(node.ret)
        ret_register = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.LoadWord(node, ret_register, ret_location))

        instructions.append(
            mips_ast.LoadWord(
                node,
                return_address,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, frame_size - DOUBLE_WORD),
                    stack_pointer,
                ),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                frame_pointer,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, frame_size - 2 * DOUBLE_WORD),
                    stack_pointer,
                ),
            )
        )
        instructions.append(
            mips_ast.Addu(
                node, stack_pointer, stack_pointer, mips_ast.Constant(node, frame_size)
            )
        )
        if node.id == "main":
            instructions.append(
                mips_ast.LoadImmediate(
                    node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 10)
                )
            )
            instructions.append(mips_ast.Syscall(node))
        else:
            instructions.append(mips_ast.JumpRegister(node, return_address))

        return instructions

    @visitor.when(ccil_ast.StorageNode)
    def visit(self, node: ccil_ast.StorageNode):
        location_id = self.get_relative_location(node.id)
        instructions = []
        instructions.extend(self.visit(node.operation))
        instructions.append(
            mips_ast.StoreWord(node, mips_ast.RegisterNode(node, V0), location_id)
        )
        return instructions

    @visitor.when(ccil_ast.IntNode)
    def visit(self, node: ccil_ast.IntNode):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node,
                mips_ast.RegisterNode(node, V0),
                mips_ast.Constant(node, node.value),
            )
        )
        return instructions

    @visitor.when(ccil_ast.CallOpNode)
    def visit(self, node: ccil_ast.CallOpNode):
        reg = mips_ast.RegisterNode(node, T0)
        instructions = []
        for arg in node.args:
            instructions.append(
                mips_ast.LoadWord(node, reg, self.get_relative_location(arg.value))
            )
            instructions.extend(self.push_stack(node, reg))
        instructions.append(mips_ast.JumpAndLink(node, mips_ast.Label(node, node.id)))

        if len(node.args) > 0:
            stack_pointer = mips_ast.RegisterNode(node, SP)
            instructions.append(
                mips_ast.Addi(
                    node,
                    stack_pointer,
                    stack_pointer,
                    mips_ast.Constant(node, len(node.args) * WORD),
                )
            )
        return instructions

    @visitor.when(ccil_ast.VCallOpNode)
    def visit(self, node: ccil_ast.VCallOpNode):
        instructions = []

        obj_location = self.get_relative_location(node.args[0].value)
        obj_type = mips_ast.RegisterNode(node, T0)
        instructions.append(mips_ast.LoadWord(node, obj_type, obj_location))

        register_function = mips_ast.RegisterNode(node, T1)
        function_index = self.get_method_index(node.type, node.id)
        instructions.append(
            mips_ast.LoadWord(
                node,
                register_function,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, function_index), obj_type
                ),
            )
        )
        reg_arg = mips_ast.RegisterNode(node, T2)
        instructions = []
        for arg in node.args:
            instructions.append(
                mips_ast.LoadWord(node, reg_arg, self.get_relative_location(arg.value))
            )
            instructions.extend(self.push_stack(node, reg_arg))
        instructions.append(mips_ast.JumpAndLink(node, register_function))

        if len(node.args) > 0:
            stack_pointer = mips_ast.RegisterNode(node, SP)
            instructions.append(
                mips_ast.Addi(
                    node,
                    stack_pointer,
                    stack_pointer,
                    mips_ast.Constant(node, len(node.args) * DOUBLE_WORD),
                )
            )

        return instructions

    @visitor.when(ccil_ast.NewOpNode)
    def visit(self, node: ccil_ast.NewOpNode):
        instructions = []

        # TODO: SELF_TYPE
        if node.type == "SELF_TYPE":
            return []
        size = self.get_attr_count(node.type) + WORD
        instructions.append(
            mips_ast.LoadImmediate(
                node,
                mips_ast.RegisterNode(node, A0),
                mips_ast.Constant(node, size),
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V1), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))

        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                mips_ast.Label(node, node.type),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T0),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        return instructions

    @visitor.when(ccil_ast.GetAttrOpNode)
    def visit(self, node: ccil_ast.GetAttrOpNode):
        instructions = []
        attr_offset = self.get_attr_index(node.instance_type, node.attr)
        location_object = self.get_relative_location(node.instance)

        instructions.append(
            mips_ast.LoadWord(node, mips_ast.RegisterNode(node, T0), location_object)
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, V0),
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, str(attr_offset)),
                    mips_ast.RegisterNode(node, T0),
                ),
            )
        )

        return instructions

    @visitor.when(ccil_ast.GetTypeOpNode)
    def visit(self, node: ccil_ast.GetTypeOpNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                self.get_relative_location(node.atom.value),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, V0),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), mips_ast.RegisterNode(node, T0)
                ),
            )
        )
        return instructions

    @visitor.when(ccil_ast.SetAttrOpNode)
    def visit(self, node: ccil_ast.SetAttrOpNode):
        instructions = []

        attr_offset = self.get_attr_index(node.instance_type, node.attr)
        object_location = self.get_relative_location(node.instance)

        instructions.append(
            mips_ast.LoadWord(node, mips_ast.RegisterNode(node, T0), object_location)
        )

        reg_new_value = mips_ast.RegisterNode(node, T1)
        if isinstance(node.new_value, ccil_ast.IntNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_new_value, mips_ast.Constant(node, node.new_value.value)
                )
            )
        elif isinstance(node.new_value, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    reg_new_value,
                    self.get_relative_location(node.new_value.value),
                )
            )
        instructions.append(
            mips_ast.StoreWord(
                node,
                reg_new_value,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, attr_offset),
                    mips_ast.RegisterNode(node, T0),
                ),
            )
        )
        return instructions

    @visitor.when(ccil_ast.SumOpNode)
    def visit(self, node: ccil_ast.SumOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Add(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.MinusOpNode)
    def visit(self, node: ccil_ast.MinusOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Sub(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.MultOpNode)
    def visit(self, node: ccil_ast.MultOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Multiply(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.DivOpNode)
    def visit(self, node: ccil_ast.DivOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Div(node, reg_left, reg_right))
        instructions.append(
            # mips_ast.Move(node, reg_ret, mips_ast.RegisterNode(node, "lo"))
            mips_ast.MoveFromLo(node, reg_ret)
        )
        return instructions

    @visitor.when(ccil_ast.LessOpNode)
    def visit(self, node: ccil_ast.LessOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Less(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.LessOrEqualOpNode)
    def visit(self, node: ccil_ast.LessOrEqualOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.LessOrEqual(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.EqualIntNode)
    def visit(self, node: ccil_ast.EqualIntNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self.get_relative_location(node.left.value)
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_left, mips_ast.Constant(node, node.left.value)
                )
            )

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self.get_relative_location(node.right.value)
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg_right, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Equal(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.NotOpNode)
    def visit(self, node: ccil_ast.NotOpNode):
        instructions = []

        reg = mips_ast.RegisterNode(node, V0)
        if isinstance(node.atom, ccil_ast.IntNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg, mips_ast.Constant(node, node.atom.value)
                )
            )
        elif isinstance(node.atom, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg, self.get_relative_location(node.atom.value)
                )
            )
        instructions.append(mips_ast.Not(node, reg, reg))

        return instructions

    @visitor.when(ccil_ast.NegOpNode)
    def visit(self, node: ccil_ast.NegOpNode):
        instructions = []

        reg = mips_ast.RegisterNode(node, V0)
        if isinstance(node.atom, ccil_ast.IntNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, reg, mips_ast.Constant(node, node.atom.value)
                )
            )
        elif isinstance(node.atom, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg, self.get_relative_location(node.atom.value)
                )
            )
        instructions.append(mips_ast.Xori(node, reg, reg, mips_ast.Constant(node, "1")))

        return instructions

    @visitor.when(ccil_ast.LoadOpNode)
    def visit(self, node: ccil_ast.LoadOpNode):
        instructions = []

        return instructions

    @visitor.when(ccil_ast.IfFalseNode)
    def visit(self, node: ccil_ast.IfFalseNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                self.get_relative_location(node.eval_value.value),
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, 9), mips_ast.Constant(node, 0)
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node,
                mips_ast.RegisterNode(node, 9),
                mips_ast.RegisterNode(node, T0),
                mips_ast.Label(node, node.target.id),
            )
        )
        return instructions

    @visitor.when(ccil_ast.GoToNode)
    def visit(self, node: ccil_ast.GoToNode):
        instructions = []
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, node.target.id)))
        return instructions

    @visitor.when(ccil_ast.LabelNode)
    def visit(self, node: ccil_ast.LabelNode):
        instructions = []
        instructions.append(mips_ast.LabelDeclaration(node, node.id))
        return instructions

    @visitor.when(ccil_ast.PrintIntNode)
    def visit(self, node: ccil_ast.PrintIntNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, A0),
                self.get_relative_location(node.id),
            )
        )

        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 1)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        return instructions

    @visitor.when(ccil_ast.PrintStrNode)
    def visit(self, node: ccil_ast.PrintStrNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, A0),
                self.get_relative_location(node.id),
            )
        )

        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 4)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        return instructions

    @visitor.when(ccil_ast.ReadIntNode)
    def visit(self, node: ccil_ast.ReadIntNode):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 5)
            )
        )
        return instructions

    def get_attr_index(self, typex: str, attr: str):
        for _type in self.__types_table:
            if _type.id == typex:
                for index, _attr in enumerate(_type.attributes):
                    if _attr.id == attr:
                        return index + WORD
        raise Exception(f"Attribute {attr} not found in type {typex}")

    def get_attr_count(self, typex: str):
        for _type in self.__types_table:
            if _type.id == typex:
                return len(_type.attributes)
        raise Exception("Type declaration not found")

    def get_init_function(self, typex: str):
        for _type in self.__types_table:
            if _type.id == typex:
                return _type.init_operations
        raise Exception("Type's function for inicialization not found")

    def get_method_index(self, typex: str, method: str) -> int:
        for _type in self.__types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return index * WORD + DOUBLE_WORD
        raise Exception("Method implementation not found")

    def get_class_method(self, typex: str, method: str) -> str:
        for _type in self.__types_table:
            if _type.id == typex:
                for _method in _type.methods:
                    if _method.id == method:
                        return _method.function.id
        raise Exception("Method implementation not found")

    def get_relative_location(self, id: str):
        return self.__location[self.__current_function.id, id]

    def set_relative_location(self, id: str, memory: mips_ast.MemoryIndexNode):
        self.__location[self.__current_function.id, id] = memory
