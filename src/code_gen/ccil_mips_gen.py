from typing import Union
import itertools
from asts.mips_ast import (
    DataNode,
    InstructionNode,
    JumpAndLink,
    LabelDeclaration,
    MIPSProgram,
    MemoryIndexNode,
    RegisterNode,
    TextNode,
    WordDirective,
)
from utils import visitor
from asts.ccil_ast import *


class CCILToMIPSGenerator:
    def __init__(self) -> None:
        self.types_table: List[ClassNode]
        self.location: Dict[str, Union[MemoryIndexNode, RegisterNode]]

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(CCILProgram)
    def visit(self, node: CCILProgram):
        self.types_table = node.types_section
        types_table = [self.visit(typex) for typex in node.types_section]

        # TODO: other .data section static data inicializations like strings
        functions = list(
            itertools.chain([self.visit(func) for func in node.code_section])
        )
        return MIPSProgram(None, TextNode(node, functions), DataNode(node, types_table))

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode):
        return (
            LabelDeclaration(node, node.id),
            WordDirective(node, [method.function for method in node.methods]),
        )

    @visit.when(FunctionNode)
    def visit(self, node: FunctionNode):
        label = LabelDeclaration(node, node.id)
        self.location = {}
        body: List[InstructionNode] = []

        reg_number = 4
        for param in node.params[:4]:
            register = RegisterNode(node, reg_number)
            self.location[param] = register
            reg_number += 1
        # TODO: params via stack (more than 4 parameters)

        body += [self.visit(op) for op in node.operations]
        return [label, *body]

    @visit.when(CallOpNode)
    def visit(self, node: CallOpNode):
        return JumpAndLink(node, node.id)

    def get_method_index(self, typex: str, method: str) -> int:
        for _type in self.types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return index
        return -1

    def get_class_method(self, typex: str, method: str) -> str:
        for _type in self.types_table:
            if _type.id == typex:
                for index, _method in enumerate(_type.methods):
                    if _method.id == method:
                        return _method.function
        return ""
