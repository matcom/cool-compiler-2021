from typing import List

import cool.code_generation.ast_cil as cil
import cool.code_generation.ast_mips as mips
import cool.visitor.visitor as visitor
from cool.semantics.utils.scope import Context


class BaseCilToMipsVisitor:
    def __init__(self, context: Context) -> None:
        self.dotdata: List[mips.DataNode] = []
        self.dottext: List[mips.InstructionNode] = []

        self.context = context

    def register_word(self, name: str, value: str) -> mips.WordDataNode:
        data = mips.WordDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_ascii(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_instruction(self, instruction: mips.InstructionNode) -> mips.InstructionNode:
        self.dottext.append(instruction)
        return instruction
    
    def register_empty_instruction(self) -> mips.EmptyInstructionNode:
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]
    
    def register_empty_data(self):
        self.dotdata.append(mips.EmptyDataNode())

    def to_data_type(self, data_name: str, type_name: str) -> str:
        return f"type_{type_name}_{data_name}"


class CilToMipsTranslator(BaseCilToMipsVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        
        for type_node in node.dottypes:
            self.visit(type_node)

        for function_node in node.dotcode:
            self.visit(function_node)

        self.register_instruction(mips.LabelNode("main"))


        return mips.ProgramNode(self.dotdata, self.dottext)

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        size = 4 * (1 + len(node.attributes))

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name), f"type_{node.parent}" if node.parent != "null" else "0") 
        self.register_word(self.to_data_type("attributes", node.name), str(len(node.attributes)))
        self.register_ascii(self.to_data_type("name", node.name), f"\"{node.name}\"")
        
        self.register_empty_data()

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        self.register_instruction(mips.LabelNode(node.name))
        self.register_empty_instruction()


    #     for instruction in node.instructions:
    #         self.visit(instruction)
    
    # @visitor.when(cil.InstructionNode)
    # def visit(self, node: cil.InstructionNode):
    #     pass
