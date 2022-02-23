from operator import index
from threading import stack_size
from typing import List, Optional

import cool.code_generation.ast_cil as cil
import cool.code_generation.ast_mips as mips
import cool.visitor.visitor as visitor
from cool.semantics.utils.scope import Context


class BaseCilToMipsVisitor:
    def __init__(self, context: Context) -> None:
        self.dotdata: List[mips.DataNode] = []
        self.dottext: List[mips.InstructionNode] = []

        self.current_function: Optional[cil.FunctionNode] = None
        self.current_function_stack: List[str] = []

        self.context = context

    def register_word(self, name: str, value: str) -> mips.WordDataNode:
        data = mips.WordDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_ascii(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_instruction(
        self, instruction: mips.InstructionNode
    ) -> mips.InstructionNode:
        self.dottext.append(instruction)
        return instruction

    def register_empty_instruction(self) -> mips.EmptyInstructionNode:
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]

    def register_empty_data(self):
        self.dotdata.append(mips.EmptyDataNode())

    def register_comment(self, comment: str) -> mips.CommentNode:
        self.dottext.append(mips.CommentNode(comment))
        return self.dottext[-1]

    def to_data_type(self, data_name: str, type_name: str) -> str:
        return f"type_{type_name}_{data_name}"

    def offset_of(self, local_name: str) -> int:
        stack_size = 4 * len(self.current_function_stack)
        index = 4 * self.current_function_stack.index(local_name)
        return stack_size - index - 4


class CilToMipsTranslator(BaseCilToMipsVisitor):
    @visitor.on("node")
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
        self.register_word(
            self.to_data_type("inherits_from", node.name),
            f"type_{node.parent}" if node.parent != "null" else "0",
        )
        self.register_word(
            self.to_data_type("attributes", node.name), str(len(node.attributes))
        )
        self.register_ascii(self.to_data_type("name", node.name), f'"{node.name}"')

        self.register_empty_data()

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        self.current_function = node
        self.register_instruction(mips.LabelNode(node.name))

        param_names = [x.name for x in self.current_function.params]
        local_names = [x.name for x in self.current_function.local_vars]
        self.current_function_stack = ["$ra"] + param_names + local_names

        locals_size = 4 * len(self.current_function.local_vars)
        stack_size = 4 * len(self.current_function_stack)

        self.register_comment("Function parameters")
        self.register_comment(f"  $ra = {stack_size - 4}($sp)")
        for i, param_name in enumerate(param_names, start=2):
            self.register_comment(f"  {param_name} = {stack_size - (4 * i)}($sp)")
        self.register_empty_instruction()

        if self.current_function.local_vars:
            self.register_comment("Reserving space for local variables")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{-locals_size}"))
            self.register_empty_instruction()

        for instruction in node.instructions:
            # TODO: Remove the try/except block when the visitor is fixed
            try:
                self.visit(instruction)
            except Exception as e:
                continue
            self.register_empty_instruction()

        if self.current_function.local_vars:
            self.register_comment("Freeing space for local variables")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{locals_size}"))
            self.register_empty_instruction()

        self.register_instruction(mips.JumpRegisterNode("$ra"))
        self.register_empty_instruction()

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        self.register_comment("addition operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 + $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment("Storing result of addition"))

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        self.register_comment("Subtraction operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SubNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 - $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment("Store result of subtraction"))
    
    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        self.register_comment("Multiplication operation")        
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment("Store result of multiplication"))

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        self.register_comment("Division operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.DivNode("$t0", "$t1").set_comment("$t0 = $t0 / $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment("Store result of division"))
    
    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        self.register_comment("Xor operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.XorNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 ^ $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment("Store result of xor"))

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        offset = self.offset_of(node.value)
        self.register_comment("Loading return value in $v1")
        self.register_instruction(mips.LoadWordNode("$v1", f"{offset}($sp)"))

    def preprocess_binary_operation(self, node: cil.ArithmeticNode):
        if node.left.isdigit() and node.right.isdigit():
            self.register_instruction(mips.AddiNode("$t0", "$zero", node.left).set_comment("Save in $t0 the left operand"))
            self.register_instruction(mips.AddiNode("$t1", "$zero", node.right).set_comment("Save in $t1 the right operand"))
        elif node.left.isdigit():
            self.register_instruction(mips.AddiNode("$t0", "$zero", node.left).set_comment("Save in $t0 the left operand"))
            self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand"))
        elif node.right.isdigit():
            self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand"))
            self.register_instruction(mips.AddiNode("$t1", "$zero", node.right).set_comment("Save in $t1 the right operand"))
        else:
            self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand"))
            self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand"))