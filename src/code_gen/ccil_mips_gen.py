from typing import Union, Dict, List
from utils import visitor
from asts import mips_ast, ccil_ast
from utils import visitor
from constants import *

WORD = 4
DOUBLE_WORD = 8
Location = Dict[str, mips_ast.MemoryIndexNode]
Types = Dict[str, str]


class CCILToMIPSGenerator:
    def __init__(self) -> None:
        self.__types_table: List[ccil_ast.Class]  # list or dict for classes???
        self.__location: Location
        self.__types: Types
        self.__current_type: str
        self.__current_function: ccil_ast.FunctionNode

    def push_stack(self, node, register: mips_ast.RegisterNode):
        stack_pointer = mips_ast.RegisterNode(node, SP)
        instructions = []
        instructions.append(
            mips_ast.Addi(node, stack_pointer, stack_pointer, -1 * WORD)
        )
        instructions.append(
            mips_ast.StoreWord(
                node, register, mips_ast.MemoryIndexNode(node, 0, stack_pointer)
            )
        )
        return instructions

    def pop_stack(self, node, register: mips_ast.RegisterNode):
        stack_pointer = mips_ast.RegisterNode(node, SP)
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node, register, mips_ast.MemoryIndexNode(node, 0, stack_pointer)
            )
        )
        instructions.append(mips_ast.Addi(node, stack_pointer, stack_pointer, WORD))
        return instructions

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ccil_ast.CCILProgram)
    def visit(self, node: ccil_ast.CCILProgram):
        self.types = node.types_section

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
        for classx in node.types_section:
            functions.extend(self.visit(classx.init_operations))
        for func in node.code_section:
            functions.extend(self.visit(func))

        return mips_ast.MIPSProgram(
            None,
            mips_ast.TextNode(node, functions),
            mips_ast.DataNode(node, types_table),
        )

    @visitor.when(ccil_ast.FunctionNode)
    def visit(self, node: ccil_ast.FunctionNode):
        instructions = []
        instructions.append(mips_ast.LabelDeclaration(node, node.id))

        frame_size = (len(node.locals)) * WORD + 12
        stack_pointer = mips_ast.RegisterNode(node, SP)
        return_address = mips_ast.RegisterNode(node, RA)
        frame_pointer = mips_ast.RegisterNode(node, FP)

        index = 0
        for param in reversed(node.locals):
            self.__location[param.id] = mips_ast.MemoryIndexNode(
                node, index, frame_pointer
            )
            index += WORD
        index = 0
        for local in node.params:
            self.__location[local.id] = mips_ast.MemoryIndexNode(
                node, -1 * index, frame_pointer
            )
            index += WORD

        instructions.append(
            mips_ast.Subu(node, stack_pointer, stack_pointer, frame_size)
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                return_address,
                mips_ast.MemoryIndexNode(node, frame_size - 2 * WORD, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                frame_pointer,
                mips_ast.MemoryIndexNode(node, frame_size - 3 * WORD, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.Addu(node, frame_pointer, frame_pointer, frame_size - WORD)
        )

        for op in node.operations:
            instructions += self.visit(op)

        ret_location = self.__location[node.ret]
        ret_register = mips_ast.RegisterNode(node, 3)
        instructions.append(mips_ast.LoadWord(node, ret_register, ret_location))

        instructions.append(
            mips_ast.LoadWord(
                node,
                return_address,
                mips_ast.MemoryIndexNode(node, frame_size - WORD, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                frame_pointer,
                mips_ast.MemoryIndexNode(node, frame_size - 3 * WORD, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.Addu(node, stack_pointer, stack_pointer, frame_size)
        )
        instructions.append(mips_ast.JumpRegister(node, return_address))

        return instructions

    @visitor.when(ccil_ast.StorageNode)
    def visit(self, node: ccil_ast.StorageNode):
        location_id = self.__location[node.id]
        instructions = []
        instructions.append(self.visit(node.operation))
        instructions.append(
            mips_ast.StoreWord(node, mips_ast.RegisterNode(node, 2), location_id)
        )
        return instructions

    @visitor.when(ccil_ast.CallOpNode)
    def visit(self, node: ccil_ast.CallOpNode):
        reg = mips_ast.RegisterNode(node, 10)
        instructions = []
        for arg in node.args:
            instructions.append(mips_ast.LoadWord(node, reg, self.__location[arg]))
            instructions.append(self.push_stack(node, reg))
        instructions.append(mips_ast.JumpAndLink(node, node.id))

        if len(node.args) > 0:
            stack_pointer = mips_ast.RegisterNode(node, SP)
            instructions.append(
                mips_ast.Addi(node, stack_pointer, stack_pointer, len(node.args) * WORD)
            )
        return instructions

    @visitor.when(ccil_ast.VCallOpNode)
    def visit(self, node: ccil_ast.VCallOpNode):
        instructions = []

        obj_location = self.__location[node.args[0]]
        obj_type = mips_ast.RegisterNode(node, T0)
        instructions.append(mips_ast.LoadWord(node, obj_type, obj_location))

        register_function = mips_ast.RegisterNode(node, T1)
        function_index = self.get_method_index(node.type, node.id)
        instructions.append(
            mips_ast.LoadWord(
                node,
                register_function,
                mips_ast.MemoryIndexNode(node, function_index, obj_type),
            )
        )
        reg_arg = mips_ast.RegisterNode(node, T2)
        instructions = []
        for arg in node.args:
            instructions.append(mips_ast.LoadWord(node, reg_arg, self.__location[arg]))
            instructions.append(self.push_stack(node, reg_arg))
        instructions.append(mips_ast.JumpAndLink(node, register_function))

        if len(node.args) > 0:
            stack_pointer = mips_ast.RegisterNode(node, SP)
            instructions.append(
                mips_ast.Addi(node, stack_pointer, stack_pointer, len(node.args) * WORD)
            )

        return instructions

    @visitor.when(ccil_ast.NewOpNode)
    def visit(self, node: ccil_ast.NewOpNode):
        instructions = []
        # TODO: SELF_TYPE
        size = self.get_attr_count(node.type_idx) + 2 * WORD
        instructions.append(
            mips_ast.LoadImmediate(
                node,
                mips_ast.RegisterNode(node, A0),
                mips_ast.Constant(node, str(size)),
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, V1), mips_ast.Constant(node, "9")
            )
        )
        instructions.append(mips_ast.Syscall(node))

        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                mips_ast.Label(node, node.type_idx),
            )
        )
        instructions.append(
            mips_ast.StoreWord(
                node,
                mips_ast.RegisterNode(node, T0),
                mips_ast.MemoryIndexNode(
                    node, mips_ast.Constant(node, "0"), mips_ast.RegisterNode(node, V0)
                ),
            )
        )
        return instructions

    @visitor.when(ccil_ast.GetAttrOpNode)
    def visit(self, node: ccil_ast.GetAttrOpNode):
        instructions = []
        attr_offset = self.get_attr_index(node.instance_type, node.attr)
        location_object = self.__location[node.instance]

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
                node, mips_ast.RegisterNode(node, T0), self.__location[node.atom.value]
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, V0),
                mips_ast.MemoryIndexNode(node, 0, mips_ast.RegisterNode(node, T0)),
            )
        )
        return instructions

    @visitor.when(ccil_ast.SumOpNode)
    def visit(self, node: ccil_ast.SumOpNode):
        instructions = []

        reg_left = mips_ast.RegisterNode(node, T3)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(node, reg_left, self.__location[node.left.value])
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(mips_ast.LoadImmediate(node, reg_left, node.left.value))

        reg_right = mips_ast.RegisterNode(node, T4)
        if isinstance(node.left, ccil_ast.IdNode):
            instructions.append(
                mips_ast.LoadWord(node, reg_right, self.__location[node.right.value])
            )
        elif isinstance(node.left, ccil_ast.ConstantNode):
            instructions.append(
                mips_ast.LoadImmediate(node, reg_right, node.right.value)
            )
        else:
            raise Exception("Invalid type of ccil node")

        reg_ret = mips_ast.RegisterNode(node, V0)
        instructions.append(mips_ast.Add(node, reg_ret, reg_left, reg_right))

        return instructions

    @visitor.when(ccil_ast.IfFalseNode)
    def visit(self, node: ccil_ast.IfFalseNode):
        instructions = []
        instructions.append(
            mips_ast.LoadWord(
                node,
                mips_ast.RegisterNode(node, T0),
                self.__location[node.eval_value.value],
            )
        )
        instructions.append(
            mips_ast.LoadImmediate(
                node, mips_ast.RegisterNode(node, 9), mips_ast.Constant(node, "0")
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
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return _method.function.id
        raise Exception("Method implementation not found")
