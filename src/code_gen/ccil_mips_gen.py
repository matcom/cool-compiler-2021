from typing import Union
from asts.mips_ast import (
    Addu,
    DataNode,
    InstructionNode,
    JumpAndLink,
    LabelDeclaration,
    LoadWord,
    MIPSProgram,
    MemoryIndexNode,
    RegisterNode,
    StoreWord,
    Subu,
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
            word_directive = [Label(node, classx.id)]
            for method in classx.methods:
                word_directive.append(method.function.id)
            types_table.append(
                LabelDeclaration(node, classx.id), WordDirective(node, word_directive)
            )

        # TODO: other .data section static data inicializations like strings

        functions = []
        for func in node.code_section:
            functions += self.visit(func, {})

        return MIPSProgram(None, TextNode(node, functions), DataNode(node, types_table))

    @visit.when(FunctionNode)
    def visit(self, node: FunctionNode, location: Location):
        label = LabelDeclaration(node, node.id)
        body: List[InstructionNode] = []

        frame_size = len(node.params) * 4 + 12
        stack_pointer = RegisterNode(node, 29)
        return_address = RegisterNode(node, 31)
        frame_pointer = RegisterNode(node, 30)

        index = 0
        for param in node.params:
            location[param.id] = MemoryIndexNode(node, index, frame_pointer)
            index += 4

        body.append(Subu(node, stack_pointer, stack_pointer, frame_size))
        body.append(
            StoreWord(node, return_address, MemoryIndexNode(node, stack_pointer, 20))
        )
        body.append(
            StoreWord(node, frame_pointer, MemoryIndexNode(node, stack_pointer, 16))
        )
        body.append(Addu(node, frame_pointer, frame_pointer, frame_size - 4))

        for op in node.operations:
            body += self.visit(op, location)

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

        function_index = self.get_method_index(node.type, node.id)

        # TODO use free register instead of 9
        register_function = RegisterNode(node, 9)

        instructions.append(
            LoadWord(
                node, register_function, MemoryIndexNode(node, function_index, obj_type)
            )
        )
        instructions.append(JumpAndLink(node, register_function))

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
