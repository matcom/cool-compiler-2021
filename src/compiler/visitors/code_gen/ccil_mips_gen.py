from typing import Dict, List, Tuple

from asts import ccil_ast, mips_ast
from visitors.utils import visitor

from .constants import *

WORD = 4
DOUBLE_WORD = 8
Location = Dict[Tuple[str, str], mips_ast.MemoryIndexNode]


class CCILToMIPSGenerator:
    """
    This class transform CCIL AST to MIPS AST using visitor pattern
    """

    def __init__(self) -> None:
        self.__id = 0
        self.__types_table: List[ccil_ast.Class] = []
        self.__location: Location = {}
        self.__current_function: ccil_ast.FunctionNode
        self.buffer_size = 1000

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ccil_ast.CCILProgram)
    def visit(self, node: ccil_ast.CCILProgram):
        self.__types_table = node.types_section

        data = []
        types_table = []
        for classx in node.types_section:
            word_directive = [
                mips_ast.Label(node, classx.id),
                mips_ast.Label(node, classx.init_operations.id),
                mips_ast.Label(node, f"class_{classx.id}"),
                mips_ast.Label(node, self._get_attr_count(classx.id)),
            ]
            for method in classx.methods:
                word_directive.append(mips_ast.Label(node, method.function.id))
            types_table.append(
                (
                    mips_ast.LabelDeclaration(node, classx.id),
                    mips_ast.WordDirective(node, word_directive),
                )
            )
        data.extend(types_table)
        for d in node.data_section:
            data.append(
                (
                    mips_ast.LabelDeclaration(node, d.id),
                    mips_ast.AsciizDirective(node, [mips_ast.Label(node, d.value)]),
                )
            )
        data.append(
            (
                mips_ast.LabelDeclaration(node, "buffer"),
                mips_ast.SpaceDirective(
                    node, [mips_ast.Constant(node, self.buffer_size)]
                ),
            )
        )

        functions = []
        functions.extend(self.visit(node.entry_func))

        for classx in node.types_section:
            functions.extend(self.visit(classx.init_operations))
        for func in node.code_section:
            functions.extend(self.visit(func))

        return mips_ast.MIPSProgram(
            None,
            mips_ast.TextNode(node, functions),
            mips_ast.DataNode(node, data),
        )

    @visitor.when(ccil_ast.FunctionNode)
    def visit(self, node: ccil_ast.FunctionNode):
        self.__current_function = node
        instructions = []
        instructions.append(mips_ast.LabelDeclaration(node, node.id))

        frame_size = len(node.locals) * DOUBLE_WORD
        stack_pointer = mips_ast.RegisterNode(node, SP)
        return_address = mips_ast.RegisterNode(node, RA)
        frame_pointer = mips_ast.RegisterNode(node, FP)

        for index, local in enumerate(node.locals):
            self._set_relative_location(
                local.id,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(
                        node, -1 * (len(node.locals) + 2 - index) * DOUBLE_WORD
                    ),
                    frame_pointer,
                ),
            )
        for index, param in enumerate(node.params):
            self._set_relative_location(
                param.id,
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(
                        node, ((len(node.params) - 1) - index) * DOUBLE_WORD
                    ),
                    frame_pointer,
                ),
            )

        instructions.extend(self._push_stack(node, return_address))
        instructions.extend(self._push_stack(node, frame_pointer))
        instructions.append(
            mips_ast.Addi(
                node, frame_pointer, stack_pointer, mips_ast.Constant(node, 16)
            )
        )
        instructions.append(
            mips_ast.Addi(
                node,
                stack_pointer,
                stack_pointer,
                mips_ast.Constant(node, -1 * frame_size),
            )
        )

        for op in node.operations:
            instructions.extend(self.visit(op))
        ret_location = self._get_relative_location(node.ret)
        ret_register = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.LoadWord(node, ret_register, ret_location))

        instructions.append(
            mips_ast.Addi(
                node, stack_pointer, stack_pointer, mips_ast.Constant(node, frame_size)
            )
        )
        instructions.extend(self._pop_stack(node, frame_pointer))
        instructions.extend(self._pop_stack(node, return_address))

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
        location_id = self._get_relative_location(node.id)
        instructions = []
        instructions.extend(self.visit(node.operation))
        instructions.append(
            mips_ast.StoreWord(node, mips_ast.RegisterNode(node, V0), location_id)
        )
        return instructions

    @visitor.when(ccil_ast.IdNode)
    def visit(self, node: ccil_ast.IdNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, V0),
                self._get_relative_location(node.value),
            )
        )
        return instructions

    @visitor.when(ccil_ast.BoolNode)
    def visit(self, node: ccil_ast.BoolNode):
        instructions = []

        t7 = mips_ast.RegisterNode(node, T7)
        instructions.append(
            mips_ast.LoadImmediate(node, t7, mips_ast.Constant(node, node.value))
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.IntNode)
    def visit(self, node: ccil_ast.IntNode):
        instructions = []

        t7 = mips_ast.RegisterNode(node, T7)
        instructions.append(
            mips_ast.LoadImmediate(node, t7, mips_ast.Constant(node, node.value))
        )
        instructions.extend(self._set_new_int(node))
        return instructions

    @visitor.when(ccil_ast.CallOpNode)
    def visit(self, node: ccil_ast.CallOpNode):
        reg = mips_ast.RegisterNode(node, T0)
        instructions = []
        for arg in node.args:
            instructions.append(
                mips_ast.LoadWord(node, reg, self._get_relative_location(arg.value))
            )
            instructions.extend(self._push_stack(node, reg))
        instructions.append(mips_ast.JumpAndLink(node, mips_ast.Label(node, node.id)))

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

    @visitor.when(ccil_ast.VCallOpNode)
    def visit(self, node: ccil_ast.VCallOpNode):
        instructions = []

        obj_location = self._get_relative_location(node.args[0].value)
        reg_obj = mips_ast.RegisterNode(node, T0)
        instructions.append(mips_ast.LoadWord(node, reg_obj, obj_location))

        obj_type = mips_ast.RegisterNode(node, T1)
        instructions.append(
            mips_ast.LoadWord(
                node,
                obj_type,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), reg_obj),
            )
        )
        register_function = mips_ast.RegisterNode(node, T2)
        function_index = self._get_method_index(node.type, node.id)
        instructions.append(
            mips_ast.LoadWord(
                node,
                register_function,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, function_index), obj_type
                ),
            )
        )
        reg_arg = mips_ast.RegisterNode(node, T3)
        for arg in node.args:
            instructions.append(
                mips_ast.LoadWord(node, reg_arg, self._get_relative_location(arg.value))
            )
            instructions.extend(self._push_stack(node, reg_arg))
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

        if node.type == "SELF_TYPE":
            object_location = self._get_relative_location(
                self.__current_function.params[0].id
            )
            object_type = mips_ast.RegisterNode(node, T1)
            attr_count = mips_ast.RegisterNode(node, T3)
            object = mips_ast.RegisterNode(node, T4)
            instructions.append(mips_ast.LoadWord(node, object, object_location))
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    object_type,
                    mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), object),
                )
            )
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    attr_count,
                    mips_ast.MemoryIndexNode(
                        node, mips_ast.Constant(node, 3 * WORD), object_type
                    ),
                )
            )
            instructions.append(
                mips_ast.Addi(node, attr_count, attr_count, mips_ast.Constant(node, 1))
            )
            instructions.append(
                mips_ast.Multiply(
                    node, attr_count, attr_count, mips_ast.Constant(node, WORD)
                )
            )
            instructions.append(
                mips_ast.Move(node, mips_ast.RegisterNode(node, A0), attr_count)
            )
        else:
            size = self._get_attr_count(node.type) * WORD + WORD
            instructions.append(
                mips_ast.LoadImmediate(
                    node,
                    mips_ast.RegisterNode(node, A0),
                    mips_ast.Constant(node, size),
                )
            )

        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))

        if node.type == "SELF_TYPE":
            instructions.append(
                mips_ast.Move(
                    node,
                    mips_ast.RegisterNode(node, T0),
                    mips_ast.RegisterNode(node, T1),
                )
            )
        else:
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

        # Initialize attibutes
        init_function = mips_ast.RegisterNode(node, T2)
        instructions.append(
            mips_ast.LoadWord(
                node,
                init_function,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, T0)
                ),
            )
        )

        instructions.extend(self._push_stack(node, mips_ast.RegisterNode(node, V0)))
        instructions.append(mips_ast.JumpAndLink(node, init_function))
        instructions.extend(self._pop_stack(node, mips_ast.RegisterNode(node, V0)))

        return instructions

    @visitor.when(ccil_ast.GetAttrOpNode)
    def visit(self, node: ccil_ast.GetAttrOpNode):
        instructions = []
        attr_offset = self._get_attr_index(node.instance_type, node.attr)
        location_object = self._get_relative_location(node.instance)

        instructions.append(
            mips_ast.LoadWord(node, mips_ast.RegisterNode(node, T0), location_object)
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, V0),
                mips_ast.MemoryIndexNode(
                    node,
                    mips_ast.Constant(node, attr_offset),
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
                self._get_relative_location(node.atom.value),
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

        attr_offset = self._get_attr_index(node.instance_type, node.attr)
        object_location = self._get_relative_location(node.instance)

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
                    self._get_relative_location(node.new_value.value),
                )
            )
        # NOTE: Fix: instances should not be of type str
        elif isinstance(node.new_value, str):
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    reg_new_value,
                    self._get_relative_location(node.new_value),
                )
            )
        else:
            raise Exception(f"Invalid type of ccil node: {type(node.new_value)}")

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
        instructions.extend(self._get_operands_value(node))

        instructions.append(
            mips_ast.Add(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )

        instructions.extend(self._set_new_int(node))

        return instructions

    @visitor.when(ccil_ast.MinusOpNode)
    def visit(self, node: ccil_ast.MinusOpNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.Sub(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_int(node))

        return instructions

    @visitor.when(ccil_ast.MultOpNode)
    def visit(self, node: ccil_ast.MultOpNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.Multiply(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_int(node))

        return instructions

    @visitor.when(ccil_ast.DivOpNode)
    def visit(self, node: ccil_ast.DivOpNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.Div(
                node, mips_ast.RegisterNode(node, T5), mips_ast.RegisterNode(node, T6)
            )
        )
        instructions.append(mips_ast.MoveFromLo(node, mips_ast.RegisterNode(node, T7)))
        instructions.extend(self._set_new_int(node))
        return instructions

    @visitor.when(ccil_ast.LessOpNode)
    def visit(self, node: ccil_ast.LessOpNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.Less(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.LessOrEqualOpNode)
    def visit(self, node: ccil_ast.LessOrEqualOpNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.LessOrEqual(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_bool(node))
        return instructions

    @visitor.when(ccil_ast.EqualIntNode)
    def visit(self, node: ccil_ast.EqualIntNode):
        instructions = []

        instructions.extend(self._get_operands_value(node))
        instructions.append(
            mips_ast.Equal(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.EqualAddrNode)
    def visit(self, node: ccil_ast.EqualAddrNode):
        instructions = []

        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T5),
                self._get_relative_location(node.left.value),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T6),
                self._get_relative_location(node.right.value),
            )
        )
        instructions.append(
            mips_ast.Equal(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, T6),
            )
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.IsVoidOpNode)
    def visit(self, node: ccil_ast.IsVoidOpNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T5),
                self._get_relative_location(node.atom.value),
            )
        )

        instructions.append(
            mips_ast.Equal(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.RegisterNode(node, T5),
                mips_ast.RegisterNode(node, ZERO),
            )
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.NegOpNode)
    def visit(self, node: ccil_ast.NotOpNode):
        instructions = []

        value = mips_ast.RegisterNode(node, T7)
        if isinstance(node.atom, ccil_ast.IntNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, value, mips_ast.Constant(node, node.atom.value)
                )
            )
        elif isinstance(node.atom, ccil_ast.IdNode):
            object = mips_ast.RegisterNode(node, T0)
            instructions.append(
                mips_ast.LoadWord(
                    node, object, self._get_relative_location(node.atom.value)
                )
            )
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    value,
                    mips_ast.MemoryIndexNode(
                        node, mips_ast.Constant(node, WORD), object
                    ),
                )
            )
        instructions.append(mips_ast.Not(node, value, value))
        instructions.append(
            mips_ast.Addi(node, value, value, mips_ast.Constant(node, 1))
        )
        instructions.extend(self._set_new_int(node))

        return instructions

    @visitor.when(ccil_ast.NotOpNode)
    def visit(self, node: ccil_ast.NotOpNode):
        instructions = []

        value = mips_ast.RegisterNode(node, T7)
        if isinstance(node.atom, ccil_ast.IntNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, value, mips_ast.Constant(node, node.atom.value)
                )
            )
        elif isinstance(node.atom, ccil_ast.IdNode):
            object = mips_ast.RegisterNode(node, T0)
            instructions.append(
                mips_ast.LoadWord(
                    node, object, self._get_relative_location(node.atom.value)
                )
            )
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    value,
                    mips_ast.MemoryIndexNode(
                        node, mips_ast.Constant(node, WORD), object
                    ),
                )
            )
        instructions.append(
            mips_ast.Xori(node, value, value, mips_ast.Constant(node, "1"))
        )
        instructions.extend(self._set_new_bool(node))

        return instructions

    @visitor.when(ccil_ast.LoadOpNode)
    def visit(self, node: ccil_ast.LoadOpNode):
        instructions = []
        instructions.append(
            mips_ast.LoadAddress(
                node, mips_ast.RegisterNode(node, T7), mips_ast.Label(node, node.target)
            )
        )
        instructions.extend(self._set_new_string(node))

        return instructions

    @visitor.when(ccil_ast.IfFalseNode)
    def visit(self, node: ccil_ast.IfFalseNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                self._get_relative_location(node.eval_value.value),
            )
        )

        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T1),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, T0)
                ),
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node,
                mips_ast.RegisterNode(node, T1),
                mips_ast.RegisterNode(node, ZERO),
                mips_ast.Label(node, node.target.id),
            )
        )
        return instructions

    @visitor.when(ccil_ast.IfNode)
    def visit(self, node: ccil_ast.IfFalseNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                self._get_relative_location(node.eval_value.value),
            )
        )

        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T1),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, T0)
                ),
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, T2), mips_ast.Constant(node, 1)
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node,
                mips_ast.RegisterNode(node, T1),
                mips_ast.RegisterNode(node, T2),
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
        a0 = mips_ast.RegisterNode(node, A0)
        instructions.append(
            mips_ast.LoadWord(
                node,
                a0,
                self._get_relative_location(node.id),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                a0,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), a0),
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
        a0 = mips_ast.RegisterNode(node, A0)
        instructions.append(
            mips_ast.LoadWord(
                node,
                a0,
                self._get_relative_location(node.id),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                a0,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), a0),
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
        instructions.append(mips_ast.Syscall(node))
        instructions.append(
            mips_ast.Move(
                node, mips_ast.RegisterNode(node, T7), mips_ast.RegisterNode(node, V0)
            )
        )
        instructions.extend(self._set_new_int(node))
        return instructions

    @visitor.when(ccil_ast.Abort)
    def visit(self, node: ccil_ast.Abort):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 10)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        return instructions

    @visitor.when(ccil_ast.LengthOpNode)
    def visit(self, node: ccil_ast.LengthOpNode):
        instructions = []
        count = mips_ast.RegisterNode(node, T7)
        instructions.append(
            mips_ast.LoadImmediate(node, count, mips_ast.Constant(node, 0))
        )
        string = mips_ast.RegisterNode(node, T1)
        instructions.append(
            mips_ast.LoadWord(node, string, self._get_relative_location(node.target))
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                string,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), string),
            )
        )

        loop = self._generate_unique_label()
        instructions.append(mips_ast.LabelDeclaration(node, loop))

        char = mips_ast.RegisterNode(node, T2)
        instructions.append(
            mips_ast.LoadByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), string),
            )
        )
        zero = mips_ast.RegisterNode(node, ZERO)
        exit = self._generate_unique_label()
        instructions.append(
            mips_ast.BranchOnEqual(node, char, zero, mips_ast.Label(node, exit))
        )
        instructions.append(
            mips_ast.Addi(node, string, string, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(node, count, count, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop)))
        instructions.append(mips_ast.LabelDeclaration(node, exit))
        instructions.extend(self._set_new_int(node))
        return instructions

    @visitor.when(ccil_ast.EqualStrNode)
    def visit(self, node: ccil_ast.EqualStrNode):
        instructions = []
        left_string = mips_ast.RegisterNode(node, T0)
        right_string = mips_ast.RegisterNode(node, T1)

        instructions.append(
            mips_ast.LoadWord(
                node, left_string, self._get_relative_location(node.left.value)
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                left_string,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), left_string
                ),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node, right_string, self._get_relative_location(node.right.value)
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                right_string,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), right_string
                ),
            )
        )

        left_char = mips_ast.RegisterNode(node, T2)
        right_char = mips_ast.RegisterNode(node, T3)
        loop = self._generate_unique_label()
        instructions.append(mips_ast.LabelDeclaration(node, loop))
        instructions.append(
            mips_ast.LoadByte(
                node,
                left_char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), left_string),
            )
        )
        instructions.append(
            mips_ast.LoadByte(
                node,
                right_char,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), right_string
                ),
            )
        )

        equals_end = self._generate_unique_label()
        not_equals_end = self._generate_unique_label()

        zero = mips_ast.RegisterNode(node, ZERO)
        instructions.append(
            mips_ast.BranchOnNotEqual(
                node, left_char, right_char, mips_ast.Label(node, not_equals_end)
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node, left_char, zero, mips_ast.Label(node, equals_end)
            )
        )

        instructions.append(
            mips_ast.Addi(node, left_string, left_string, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(node, right_string, right_string, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop)))

        end = self._generate_unique_label()
        result = mips_ast.RegisterNode(node, T7)
        instructions.append(mips_ast.LabelDeclaration(node, equals_end))
        instructions.append(
            mips_ast.LoadImmediate(node, result, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, end)))
        instructions.append(mips_ast.LabelDeclaration(node, not_equals_end))
        instructions.append(
            mips_ast.LoadImmediate(node, result, mips_ast.Constant(node, 0))
        )
        instructions.append(mips_ast.LabelDeclaration(node, end))
        instructions.extend(self._set_new_bool(node))
        return instructions

    @visitor.when(ccil_ast.ConcatOpNode)
    def visit(self, node: ccil_ast.ConcatOpNode):
        instructions = []
        string_a = mips_ast.RegisterNode(node, T0)
        string_b = mips_ast.RegisterNode(node, T1)

        len_a = mips_ast.RegisterNode(node, T4)
        len_b = mips_ast.RegisterNode(node, T3)

        instructions.append(
            mips_ast.LoadWord(node, string_a, self._get_relative_location(node.source))
        )
        instructions.extend(self._push_stack(node, string_a))
        instructions.append(mips_ast.JumpAndLink(node, mips_ast.Label(node, "length")))
        instructions.extend(self._pop_stack(node, string_a))
        instructions.append(mips_ast.Move(node, len_a, mips_ast.RegisterNode(node, V0)))

        instructions.append(
            mips_ast.LoadWord(node, string_b, self._get_relative_location(node.target))
        )
        instructions.extend(self._push_stack(node, string_b))
        instructions.append(mips_ast.JumpAndLink(node, mips_ast.Label(node, "length")))
        instructions.extend(self._pop_stack(node, string_b))

        instructions.append(mips_ast.Move(node, len_b, mips_ast.RegisterNode(node, V0)))

        instructions.append(
            mips_ast.LoadWord(
                node,
                len_b,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), len_b),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                len_a,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), len_a),
            )
        )

        instructions.append(
            mips_ast.Add(node, mips_ast.RegisterNode(node, A0), len_a, len_b)
        )
        instructions.append(
            mips_ast.Addi(
                node,
                mips_ast.RegisterNode(node, A0),
                mips_ast.RegisterNode(node, A0),
                mips_ast.Constant(node, 1),
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))

        concat_string = mips_ast.RegisterNode(node, V0)
        concat_char = mips_ast.RegisterNode(node, T6)
        char = mips_ast.RegisterNode(node, T5)
        instructions.append(mips_ast.Move(node, concat_char, concat_string))

        instructions.append(
            mips_ast.LoadWord(
                node,
                string_b,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), string_b),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                string_a,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), string_a),
            )
        )

        loop_string_a = self._generate_unique_label()
        end_loop_string_a = self._generate_unique_label()
        instructions.append(mips_ast.LabelDeclaration(node, loop_string_a))
        instructions.append(
            mips_ast.LoadByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), string_a),
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node,
                char,
                mips_ast.RegisterNode(node, ZERO),
                mips_ast.Label(node, end_loop_string_a),
            )
        )
        instructions.append(
            mips_ast.StoreByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), concat_char),
            )
        )
        instructions.append(
            mips_ast.Addi(node, string_a, string_a, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(node, concat_char, concat_char, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop_string_a)))
        instructions.append(mips_ast.LabelDeclaration(node, end_loop_string_a))

        loop_string_b = self._generate_unique_label()
        end_loop_string_b = self._generate_unique_label()
        instructions.append(mips_ast.LabelDeclaration(node, loop_string_b))
        instructions.append(
            mips_ast.LoadByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), string_b),
            )
        )
        instructions.append(
            mips_ast.BranchOnEqual(
                node,
                char,
                mips_ast.RegisterNode(node, ZERO),
                mips_ast.Label(node, end_loop_string_b),
            )
        )
        instructions.append(
            mips_ast.StoreByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), concat_char),
            )
        )
        instructions.append(
            mips_ast.Addi(node, string_b, string_b, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(node, concat_char, concat_char, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop_string_b)))
        instructions.append(mips_ast.LabelDeclaration(node, end_loop_string_b))

        instructions.append(
            mips_ast.StoreByte(
                node,
                mips_ast.RegisterNode(node, ZERO),
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), concat_char),
            )
        )
        instructions.append(
            mips_ast.Move(
                node, mips_ast.RegisterNode(node, T7), mips_ast.RegisterNode(node, V0)
            )
        )
        instructions.extend(self._set_new_string(node))

        return instructions

    @visitor.when(ccil_ast.SubstringOpNode)
    def visit(self, node: ccil_ast.SubstringOpNode):
        instructions = []
        substring = mips_ast.RegisterNode(node, V0)
        substring_length = mips_ast.RegisterNode(node, A0)
        instructions.append(
            mips_ast.LoadWord(
                node, substring_length, self._get_relative_location(node.length.value)
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                substring_length,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), substring_length
                ),
            )
        )
        instructions.append(
            mips_ast.Addi(
                node, substring_length, substring_length, mips_ast.Constant(node, 1)
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(node, substring, mips_ast.Constant(node, 9))
        )
        instructions.append(mips_ast.Syscall(node))

        char_string = mips_ast.RegisterNode(node, T0)
        char_substring = mips_ast.RegisterNode(node, T1)
        char = mips_ast.RegisterNode(node, T2)
        start = mips_ast.RegisterNode(node, T3)

        loop = self._generate_unique_label()
        end = self._generate_unique_label()

        instructions.append(mips_ast.Move(node, char_substring, substring))

        instructions.append(
            mips_ast.LoadWord(
                node, char_string, self._get_relative_location(node.target.value)
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                char_string,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), char_string
                ),
            )
        )

        instructions.append(
            mips_ast.LoadWord(
                node, start, self._get_relative_location(node.start.value)
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                start,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), start),
            )
        )
        instructions.append(mips_ast.Add(node, char_string, char_string, start))
        instructions.append(
            mips_ast.Addi(
                node, substring_length, substring_length, mips_ast.Constant(node, -1)
            )
        )
        instructions.append(mips_ast.LabelDeclaration(node, loop))

        zero = mips_ast.RegisterNode(node, ZERO)
        instructions.append(
            mips_ast.BranchOnEqual(
                node, substring_length, zero, mips_ast.Label(node, end)
            )
        )
        instructions.append(
            mips_ast.LoadByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), char_string),
            )
        )
        instructions.append(
            mips_ast.StoreByte(
                node,
                char,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), char_substring
                ),
            )
        )
        instructions.append(
            mips_ast.Addi(node, char_string, char_string, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(
                node, char_substring, char_substring, mips_ast.Constant(node, 1)
            )
        )
        instructions.append(
            mips_ast.Addi(
                node, substring_length, substring_length, mips_ast.Constant(node, -1)
            )
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop)))
        instructions.append(mips_ast.LabelDeclaration(node, end))
        instructions.append(
            mips_ast.StoreByte(
                node,
                zero,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), char_substring
                ),
            )
        )
        instructions.append(
            mips_ast.Move(
                node, mips_ast.RegisterNode(node, T7), mips_ast.RegisterNode(node, V0)
            )
        )
        instructions.extend(self._set_new_string(node))
        return instructions

    @visitor.when(ccil_ast.TypeNameOpNode)
    def visit(self, node: ccil_ast.TypeNameOpNode):
        instructions = []
        result = mips_ast.RegisterNode(node, T7)

        object = mips_ast.RegisterNode(node, T0)
        instructions.append(
            mips_ast.LoadWord(node, object, self._get_relative_location(node.target))
        )
        object_type = mips_ast.RegisterNode(node, T1)

        instructions.append(
            mips_ast.LoadWord(
                node,
                object_type,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), object),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                result,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, DOUBLE_WORD), object_type
                ),
            )
        )
        instructions.extend(self._set_new_string(node))
        return instructions

    @visitor.when(ccil_ast.ShallowCopyOpNode)
    def visit(self, node: ccil_ast.ShallowCopyOpNode):
        instructions = []
        object = mips_ast.RegisterNode(node, T0)
        object_type = mips_ast.RegisterNode(node, T1)
        attr_total = mips_ast.RegisterNode(node, T2)

        instructions.append(
            mips_ast.LoadWord(node, object, self._get_relative_location(node.source))
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                object_type,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), object),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                attr_total,
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 3 * WORD), object_type
                ),
            )
        )
        instructions.append(
            mips_ast.Addi(node, attr_total, attr_total, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Multiply(
                node, attr_total, attr_total, mips_ast.Constant(node, WORD)
            )
        )
        instructions.append(
            mips_ast.Move(node, mips_ast.RegisterNode(node, A0), attr_total)
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))

        object_copy = mips_ast.RegisterNode(node, T3)
        section = mips_ast.RegisterNode(node, T4)
        zero = mips_ast.RegisterNode(node, ZERO)
        loop = self._generate_unique_label()
        end = self._generate_unique_label()

        instructions.append(
            mips_ast.Move(node, object_copy, mips_ast.RegisterNode(node, V0))
        )

        instructions.append(mips_ast.LabelDeclaration(node, loop))
        instructions.append(
            mips_ast.BranchOnEqual(node, attr_total, zero, mips_ast.Label(node, end))
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                section,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), object),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                section,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), object_copy),
            )
        )
        instructions.append(
            mips_ast.Addi(node, object, object, mips_ast.Constant(node, WORD))
        )
        instructions.append(
            mips_ast.Addi(node, object_copy, object_copy, mips_ast.Constant(node, WORD))
        )
        instructions.append(
            mips_ast.Addi(
                node, attr_total, attr_total, mips_ast.Constant(node, -1 * WORD)
            )
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop)))

        instructions.append(mips_ast.LabelDeclaration(node, end))

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, V0),
                self._get_relative_location(node.dest),
            )
        )
        return instructions

    @visitor.when(ccil_ast.ReadStrNode)
    def visit(self, node: ccil_ast.ReadStrNode):
        instructions = []

        a0 = mips_ast.RegisterNode(node, A0)
        a1 = mips_ast.RegisterNode(node, A1)
        v0 = mips_ast.RegisterNode(node, V0)
        t7 = mips_ast.RegisterNode(node, T7)
        instructions.append(
            mips_ast.LoadAddress(node, a0, mips_ast.Label(node, "buffer"))
        )
        instructions.append(
            mips_ast.LoadImmediate(node, a1, mips_ast.Constant(node, self.buffer_size))
        )
        instructions.append(
            mips_ast.LoadImmediate(node, v0, mips_ast.Constant(node, 8))
        )
        instructions.append(mips_ast.Syscall(node))
        instructions.append(
            mips_ast.LoadAddress(node, t7, mips_ast.Label(node, "buffer"))
        )
        instructions.extend(self._set_new_string(node))

        instructions.extend(self._push_stack(node, v0))
        instructions.append(mips_ast.JumpAndLink(node, mips_ast.Label(node, "length")))
        instructions.extend(self._pop_stack(node, a0))

        instructions.append(
            mips_ast.LoadWord(
                node,
                a0,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, WORD), v0),
            )
        )
        instructions.append(mips_ast.Addi(node, a0, a0, mips_ast.Constant(node, 1)))

        loop = self._generate_unique_label()
        end = self._generate_unique_label()
        zero = mips_ast.RegisterNode(node, ZERO)
        char = mips_ast.RegisterNode(node, T0)
        string = mips_ast.RegisterNode(node, T1)
        buffer_string = mips_ast.RegisterNode(node, T2)
        buffer_char = mips_ast.RegisterNode(node, T3)
        string_char = mips_ast.RegisterNode(node, T4)

        instructions.append(
            mips_ast.LoadImmediate(node, v0, mips_ast.Constant(node, 9))
        )
        instructions.append(mips_ast.Syscall(node))

        instructions.append(mips_ast.Move(node, string, v0))
        instructions.append(
            mips_ast.LoadAddress(node, buffer_string, mips_ast.Label(node, "buffer"))
        )
        instructions.append(mips_ast.Move(node, buffer_char, buffer_string))
        instructions.append(mips_ast.Move(node, string_char, string))

        instructions.append(mips_ast.LabelDeclaration(node, loop))
        instructions.append(
            mips_ast.LoadByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), buffer_char),
            )
        )
        instructions.append(
            mips_ast.StoreByte(
                node,
                char,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), string_char),
            )
        )
        new_line = mips_ast.RegisterNode(node, T9)
        instructions.append(
            mips_ast.LoadImmediate(node, new_line, mips_ast.Constant(node, 10))
        )
        instructions.append(
            mips_ast.BranchOnEqual(node, char, new_line, mips_ast.Label(node, end))
        )
        instructions.append(
            mips_ast.BranchOnEqual(node, char, zero, mips_ast.Label(node, end))
        )

        instructions.append(
            mips_ast.Addi(node, buffer_char, buffer_char, mips_ast.Constant(node, 1))
        )
        instructions.append(
            mips_ast.Addi(node, string_char, string_char, mips_ast.Constant(node, 1))
        )
        instructions.append(mips_ast.Jump(node, mips_ast.Label(node, loop)))
        instructions.append(mips_ast.LabelDeclaration(node, end))

        instructions.append(
            mips_ast.StoreByte(
                node,
                zero,
                mips_ast.MemoryIndexNode(node, mips_ast.Constant(node, 0), string_char),
            )
        )

        instructions.append(mips_ast.Move(node, t7, string))
        instructions.extend(self._set_new_string(node))

        return instructions

    def _get_attr_index(self, typex: str, attr: str):
        for _type in self.__types_table:
            if _type.id == typex:
                for index, _attr in enumerate(_type.attributes):
                    if _attr.id == attr:
                        return index * WORD + WORD
        raise Exception(f"Attribute {attr} not found in type {typex}")

    def _get_attr_count(self, typex: str):
        for _type in self.__types_table:
            if _type.id == typex:
                return len(_type.attributes)
        raise Exception(f"Type declaration not found: {typex}")

    def _get_init_function(self, typex: str):
        for _type in self.__types_table:
            if _type.id == typex:
                return _type.init_operations
        raise Exception(f"Type's function for inicialization not found: {typex}")

    def _get_method_index(self, typex: str, method: str) -> int:
        for _type in self.__types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return index * WORD + WORD + WORD + DOUBLE_WORD

        raise Exception(f"Method implementation not found:{typex} {method}")

    def _get_class_method(self, typex: str, method: str) -> str:
        for _type in self.__types_table:
            if _type.id == typex:
                for _method in _type.methods:
                    if _method.id == method:
                        return _method.function.id
        raise Exception(f"Method implementation not found")

    def _get_relative_location(self, id: str):
        return self.__location[self.__current_function.id, id]

    def _set_relative_location(self, id: str, memory: mips_ast.MemoryIndexNode):
        self.__location[self.__current_function.id, id] = memory

    def _generate_unique_label(self):
        self.__id += 1
        return f"label_{self.__id}"

    def _push_stack(self, node, register: mips_ast.RegisterNode):
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

    def _pop_stack(self, node, register: mips_ast.RegisterNode):
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

    def _get_operands_value(self, node):

        instructions = []

        left_value = mips_ast.RegisterNode(node, T5)
        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_left, self._get_relative_location(node.left.value)
                )
            )
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    left_value,
                    mips_ast.MemoryIndexNode(
                        node, mips_ast.Constant(node, WORD), reg_left
                    ),
                )
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, left_value, mips_ast.Constant(node, node.left.value)
                )
            )

        right_value = mips_ast.RegisterNode(node, T6)
        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.right, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(
                    node, reg_right, self._get_relative_location(node.right.value)
                )
            )
            instructions.append(
                mips_ast.LoadWord(
                    node,
                    right_value,
                    mips_ast.MemoryIndexNode(
                        node, mips_ast.Constant(node, WORD), reg_right
                    ),
                )
            )
        elif isinstance(node.right, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(
                    node, right_value, mips_ast.Constant(node, node.right.value)
                )
            )
        else:
            raise Exception("Invalid type of ccil node")
        return instructions

    def _set_new_int(self, node):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, A0), mips_ast.Constant(node, 2 * WORD)
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        instructions.append(
            mips_ast.LoadAddress(
                node, mips_ast.RegisterNode(node, T8), mips_ast.Label(node, "Int")
            )
        )

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T8),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), mips_ast.RegisterNode(node, V0)
                ),
            )
        )

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        return instructions

    def _set_new_bool(self, node):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, A0), mips_ast.Constant(node, 2 * WORD)
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        instructions.append(
            mips_ast.LoadAddress(
                node, mips_ast.RegisterNode(node, T8), mips_ast.Label(node, "Bool")
            )
        )

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T8),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), mips_ast.RegisterNode(node, V0)
                ),
            )
        )

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        return instructions

    def _set_new_string(self, node):
        instructions = []
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, A0), mips_ast.Constant(node, 2 * WORD)
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V0), mips_ast.Constant(node, 9)
            )
        )
        instructions.append(mips_ast.Syscall(node))
        instructions.append(
            mips_ast.LoadAddress(
                node, mips_ast.RegisterNode(node, T8), mips_ast.Label(node, "String")
            )
        )

        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T8),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, 0), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T7),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, WORD), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        return instructions
