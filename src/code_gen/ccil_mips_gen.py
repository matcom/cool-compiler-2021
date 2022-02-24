from typing import Union
from utils import visitor
from asts.mips_ast import (
    Addu,
    DataNode,
    InstructionNode,
    JumpAndLink,
    JumpRegister,
    LabelDeclaration,
    LoadWord,
    MIPSProgram,
    MemoryIndexNode,
    Move,
    RegisterNode,
    StoreWord,
    Subu,
    Label,
    TextNode,
    WordDirective,
)
from utils import visitor
from asts.ccil_ast import *

Location = Dict[str, Union[MemoryIndexNode, RegisterNode]]


class CCILToMIPSGenerator:
    def __init__(self) -> None:
        self.types_table: List[Class]  # list or dict for classes???

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(CCILProgram)
    def visit(self, node: CCILProgram, location: Location = None):
        self.types = node.types_section

        types_table = []
        for classx in node.types_section:
            word_directive = [
                Label(node, classx.id),
                Label(node, classx.init_operations.id),
            ]
            for method in classx.methods:
                word_directive.append(Label(node, method.function.id))
            types_table.append(
                (LabelDeclaration(node, classx.id), WordDirective(node, word_directive))
            )

        # TODO: other .data section static data inicializations like strings

        functions = []
        for classx in node.types_section:
            functions += self.visit(classx.init_operations, {})
        for func in node.code_section:
            functions += self.visit(func, {})

        return MIPSProgram(None, TextNode(node, functions), DataNode(node, types_table))

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, location: Location):
        label = LabelDeclaration(node, node.id)
        body: List[InstructionNode] = []

        frame_size = (len(node.params) + len(node.locals)) * 4 + 12
        stack_pointer = RegisterNode(node, 29)
        return_address = RegisterNode(node, 31)
        frame_pointer = RegisterNode(node, 30)

        index = 0
        for param in node.params:
            location[param.id] = MemoryIndexNode(node, index, frame_pointer)
            index += 4
        for local in node.params:
            location[local.id] = MemoryIndexNode(node, index, frame_pointer)
            index += 4

        body.append(Subu(node, stack_pointer, stack_pointer, frame_size))
        body.append(
            StoreWord(
                node,
                return_address,
                MemoryIndexNode(node, frame_size - 8, stack_pointer),
            )
        )
        body.append(
            StoreWord(
                node,
                frame_pointer,
                MemoryIndexNode(node, frame_size - 12, stack_pointer),
            )
        )
        body.append(Addu(node, frame_pointer, frame_pointer, frame_size - 4))

        for op in node.operations:
            body += self.visit(op, location)

        ret_location = location[node.ret]
        ret_register = RegisterNode(node, 3)
        if isinstance(ret_location, RegisterNode):
            body.append(Move(node, ret_register, ret_location))
        elif isinstance(ret_location, MemoryIndexNode):
            body.append(LoadWord(node, ret_register, ret_location))

        body.append(
            LoadWord(
                node,
                return_address,
                MemoryIndexNode(node, frame_size - 8, stack_pointer),
            )
        )
        body.append(
            LoadWord(
                node,
                frame_pointer,
                MemoryIndexNode(node, frame_size - 12, stack_pointer),
            )
        )
        body.append(Addu(node, stack_pointer, stack_pointer, frame_size))
        body.append(JumpRegister(node, return_address))

        return [label, *body]

    @visitor.when(CallOpNode)
    def visit(self, node: CallOpNode, location: Location):
        stack_pointer = RegisterNode(node, 29)
        instructions = []
        index = 4
        for arg in node.args:
            arg_location = location[arg]
            if isinstance(arg_location, RegisterNode):
                instructions.append(
                    StoreWord(node, arg_location, MemoryIndexNode(index, stack_pointer))
                )
                index += 4
        instructions.append(JumpAndLink(node, node.id))
        return instructions

    @visitor.when(VCallOpNode)
    def visit(self, node: VCallOpNode, location: Location):
        obj_location = location[node.args[0]]
        instructions = []

        # TODO use free register instead of 8
        obj_type = RegisterNode(node, 8)

        if isinstance(obj_location, RegisterNode):
            instructions.append(
                LoadWord(node, obj_type, MemoryIndexNode(node, 0, obj_location))
            )
        elif isinstance(obj_location, MemoryIndexNode):
            instructions.append(LoadWord(node, obj_type, obj_location))

        function_index = self.get_method_index(node.type, node.id) * 4 + 8

        # TODO use free register instead of 9
        register_function = RegisterNode(node, 9)

        instructions.append(
            LoadWord(
                node, register_function, MemoryIndexNode(node, function_index, obj_type)
            )
        )
        instructions.append(JumpAndLink(node, register_function))
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
