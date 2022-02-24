from typing import Union, Dict, List
from utils import visitor
from asts import mips_ast, ccil_ast
from utils import visitor

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
        stack_pointer = mips_ast.RegisterNode(node, 29)
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
        stack_pointer = mips_ast.RegisterNode(node, 29)
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
        stack_pointer = mips_ast.RegisterNode(node, 29)
        return_address = mips_ast.RegisterNode(node, 31)
        frame_pointer = mips_ast.RegisterNode(node, 30)

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
                mips_ast.MemoryIndexNode(node, frame_size - 8, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.LoadWord(
                node,
                frame_pointer,
                mips_ast.MemoryIndexNode(node, frame_size - 12, stack_pointer),
            )
        )
        instructions.append(
            mips_ast.Addu(node, stack_pointer, stack_pointer, frame_size)
        )
        instructions.append(mips_ast.JumpRegister(node, return_address))

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
            stack_pointer = mips_ast.RegisterNode(node, 29)
            instructions.append(
                mips_ast.Addi(node, stack_pointer, stack_pointer, len(node.args) * WORD)
            )
        return instructions

    @visitor.when(ccil_ast.VCallOpNode)
    def visit(self, node: ccil_ast.VCallOpNode):
        instructions = []

        obj_location = self.__location[node.args[0]]
        obj_type = mips_ast.RegisterNode(node, 8)
        instructions.append(mips_ast.LoadWord(node, obj_type, obj_location))

        register_function = mips_ast.RegisterNode(node, 9)
        function_index = self.get_method_index(node.type, node.id) * WORD + DOUBLE_WORD
        instructions.append(
            mips_ast.LoadWord(
                node,
                register_function,
                mips_ast.MemoryIndexNode(node, function_index, obj_type),
            )
        )
        reg_arg = mips_ast.RegisterNode(node, 10)
        instructions = []
        for arg in node.args:
            instructions.append(mips_ast.LoadWord(node, reg_arg, self.__location[arg]))
            instructions.append(self.push_stack(node, reg_arg))
        instructions.append(mips_ast.JumpAndLink(node, register_function))

        if len(node.args) > 0:
            stack_pointer = mips_ast.RegisterNode(node, 29)
            instructions.append(
                mips_ast.Addi(node, stack_pointer, stack_pointer, len(node.args) * WORD)
            )

        return instructions

    @visitor.when(ccil_ast.StorageNode)
    def visit(self, node: ccil_ast.StorageNode):
        location_id = self.__location[node.id]
        instructions = []
        instructions.append(self.visit(node.operation))
        instructions.append(
            mips_ast.LoadWord(node, mips_ast.RegisterNode(node, 3), location_id)
        )
        return instructions

    @visitor.when(ccil_ast.SumOpNode)
    def visit(self, node: ccil_ast.SumOpNode):
        instructions = []
        reg = mips_ast.RegisterNode(node, 10)
        reg_left = mips_ast.RegisterNode(node, 11)
        reg_rigth = mips_ast.RegisterNode(node, 12)
        left_location = self.__location[node.left.value]
        right_location = self.__location[node.left.value]

        return instructions

    def get_init_function(self, typex: str):
        for _type in self.types_table:
            if _type.id == typex:
                return _type.init_operations
        raise Exception("Type's function for inicialization not found")

    def get_method_index(self, typex: str, method: str) -> int:
        for _type in self.types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return index
        raise Exception("Method implementation not found")

    def get_class_method(self, typex: str, method: str) -> str:
        for _type in self.types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return _method.function.id
        raise Exception("Method implementation not found")
