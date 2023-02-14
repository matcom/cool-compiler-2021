from operator import index
from threading import stack_size
from typing import List, Optional, Union

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

    def register_asciiz(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_space(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.SpaceDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_instruction(self, instruction: mips.InstructionNode) -> mips.InstructionNode:
        self.dottext.append(instruction)
        return instruction

    def register_empty_instruction(self) -> mips.EmptyInstructionNode:
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]

    def register_instantiation(self, size: Union[int, str]) -> mips.InstructionNode:
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        if isinstance(size, int):
            self.register_instruction(mips.AddiNode("$a0", "$zero", f"{size}"))
        if isinstance(size, str):
            self.register_instruction(mips.MoveNode("$a0", size))
        self.register_instruction(mips.SystemCallNode())

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
        
        for type_node in node.dottypes: 
            self.register_word(self.to_data_type("name_size", type_node.name), str(len(type_node.name)))
            self.register_asciiz(self.to_data_type("name", type_node.name), f'"{type_node.name}"')
            self.register_empty_data()
        
        self.register_space("buffer_input", 1024)
        self.register_asciiz("debug_log", '"debug_log\\n"')

        for function_node in node.dotcode:
            self.visit(function_node)

        return mips.ProgramNode(self.dotdata, self.dottext)

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        size = 4 * (2 + len(node.attributes) + len(node.methods))

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name), f"type_{node.parent}" if node.parent != "null" else "0")
        self.register_word(self.to_data_type("name_address", node.name), f"type_{node.name}_name_size")
        for method, function in node.methods:
            self.register_word(self.to_data_type(method, node.name), function)
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

        if node.name != "main":
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
                if isinstance(instruction, (cil.EmptyInstruction, cil.CommentNode)):
                    continue
                self.visit(instruction)
                self.register_empty_instruction()
            except Exception as e:
                print(f"error {e} in {node.name} {type(instruction)}")

        if node.name != "main" and self.current_function.local_vars:
            self.register_comment("Freeing space for local variables")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{locals_size}"))
            self.register_empty_instruction()

        if node.name != "main":
            self.register_instruction(mips.JumpRegisterNode("$ra"))
        self.register_empty_instruction()

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        self.register_comment(f"{node.dest} = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode):
        self.register_comment(f"{node.dest} = {node.source} where {node.source} is an integer")
        self.register_instantiation(12)
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"Pointer to {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t0)").set_comment(f"$t2 = value of {node.source}"))
    
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)").set_comment(f"Save type of {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment(f"Save size of {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$t2", "8($v0)").set_comment(f"Save value of {node.dest}"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        if node.arg_index == 0:
            self.register_comment("Passing function arguments")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"-{4 * node.total_args + 4}").set_comment("Reserving space for arguments"))
            self.register_instruction(mips.StoreWordNode("$ra", f"{4 * (node.total_args)}($sp)").set_comment("Storing return address"))
            self.register_empty_instruction()
        self.register_comment(f"Argument {node.name}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.name) +  4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{4 * (node.total_args - node.arg_index - 1)}($sp)").set_comment(f"Storing {node.name}"))

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        self.register_comment(f"Calling function {node.method_address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.method_address) + 4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.JumpAndLinkRegisterNode("$t0"))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)").set_comment(f"{node.dest} = result of {node.method_address}"))
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}").set_comment("Freeing space for arguments"))
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        self.register_comment(f"Calling function {node.function}")
        self.register_instruction(mips.JumpAndLinkNode(node.function))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)").set_comment(f"{node.dest} = result of {node.function}"))
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}").set_comment("Freeing space for arguments"))

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        self.register_comment(f"Allocating {node.type}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.LoadWordNode("$a0", f"type_{node.type}"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.type}").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of th object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of th object"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object {node.type}"))

    @visitor.when(cil.AllocateIntNode)
    def visit(self, node: cil.AllocateIntNode):
        self.register_comment(f"Allocating Int {node.value}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t0", "type_Int").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of the object"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)").set_comment("Setting value in the third word of the object"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object Int"))

    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode):
        self.register_comment(f"Allocating Bool {node.value}")

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t0", "type_Bool").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of the object"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)").set_comment("Setting value in the third word of the object"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object Int"))

    @visitor.when(cil.AllocateStrNode)
    def visit(self, node: cil.AllocateStrNode):
        self.register_comment(f"Allocating String")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", f"{9 + node.length}").set_comment("$a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        
        self.register_instruction(mips.LoadAddressNode("$t0", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t0", f"0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t0", "$zero", f"{9 + node.length}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"4($v0)").set_comment("Setting length of the string in the second word of the object"))
        self.register_empty_instruction()

        for i, c in enumerate(node.string):
            ec = c.replace('\n', '\\n')
            ec = ec.replace('\t', '\\t')
            ec = ec.replace('\b', '\\b')
            ec = ec.replace('\f', '\\f')
            self.register_instruction(mips.AddiNode("$t0", "$zero",  f"{ord(c)}"))
            self.register_instruction(mips.StoreByteNode("$t0", f"{i + 8}($v0)").set_comment(f"{node.dest}[{i}] = '{ec}'"))
            self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"{node.length + 8}($v0)").set_comment(f"Null-terminator at the end of the string"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.value}"))

    @visitor.when(cil.AllocateNullPtrNode)
    def visit(self, node: cil.AllocateNullPtrNode):
        self.register_comment(f"Allocating NUll to {node.dest}")
        self.register_instruction(mips.StoreWordNode("$zero", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = 0"))

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        self.register_comment(f"{node.dest} = length of {node.str_address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "4($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9").set_comment("Subtracting 9 for the type, length, and null-terminator"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t1", "8($t0)"))

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        self.register_comment(f"{node.dest} = {node.str1} + {node.str2}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str1)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.str2)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)").set_comment("$t2 = length of str1"))
        self.register_instruction(mips.LoadWordNode("$t3", "4($t1)").set_comment("$t3 = length of str2"))
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))
        
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3").set_comment("$t4 = length of str1 + str2"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "9").set_comment("Adding the space for the type (4bytes), the length(4bytes) and the null-terminator(1byte)"))
        self.register_empty_instruction()

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.MoveNode("$a0", "$t4"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.AddiNode("$t4", "$t4", "-9").set_comment("Restoring $t4 = length of str1 + str2"))
        self.register_instruction(mips.AddNode("$t5", "$zero", "$v0").set_comment("$t5 = address of the new string object"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "8").set_comment("$t5 = address of the first byte of the new string"))
        self.register_empty_instruction()
        
        self.register_instruction(mips.LoadAddressNode("$t8", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t8", f"0($v0)").set_comment("Setting type in the first word of th object"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length of the string in the second word of the object"))
        self.register_empty_instruction()

        self.register_comment(f"Copying str1 to the new string")
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6").set_comment("$t6 = 0 Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_str1_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t2", "while_copy_str1_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of str1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_str1_start"))
        self.register_instruction(mips.LabelNode("while_copy_str1_end"))
        self.register_empty_instruction()

        self.register_comment(f"Copying str2 to the new string")
        self.register_instruction(mips.LabelNode("while_copy_str2_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t4", "while_copy_str2_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t1)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of str1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_str2_start"))
        self.register_instruction(mips.LabelNode("while_copy_str2_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)").set_comment("Setting the null-terminator"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.str1} + {node.str2}"))

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        self.register_comment(f"{node.dest} = {node.str_address}[{node.start}:{node.start} + {node.length}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)").set_comment("$t0 = address of the string"))
        self.register_instruction(mips.LoadWordNode("$t1", f"4($t0)").set_comment("$t1 = length of the string"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9").set_comment("$t1 = length of the string + 9"))
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.start)}($sp)").set_comment("$t2 = start of the substring"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t2)"))
        self.register_instruction(mips.LoadWordNode("$t3", f"{self.offset_of(node.length)}($sp)").set_comment("$t3 = length of the substring"))
        self.register_instruction(mips.LoadWordNode("$t3", "8($t3)"))
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3").set_comment("$t4 = start of the substring + length of the substring"))

        self.register_empty_instruction()
        self.register_instruction(mips.BgtNode("$t4", "$t1", "substring_out_of_bounds"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$t3", "9"))
        self.register_instantiation("$t3")
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))

        self.register_empty_instruction()
        self.register_instruction(mips.LoadAddressNode("$t5", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t5", f"0($v0)").set_comment("Setting type in the first word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length in the second word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("pointing to the first byte of the string"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t2").set_comment("pointing to the first byte of the substring"))
        self.register_instruction(mips.MoveNode("$t5", "$v0").set_comment("$t5 = address of the new string"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "8").set_comment("pointing to the first byte of the string"))
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6").set_comment("$t6 = 0 Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_substr_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t3", "while_copy_substr_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"0($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of the string"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_substr_start"))
        self.register_instruction(mips.LabelNode("while_copy_substr_end"))

        self.register_empty_instruction()
        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)").set_comment("Setting the null-terminator"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.str_address}[{node.start}:{node.start} + {node.length}]"))

        self.register_instruction(mips.JumpNode("substring_not_out_of_bounds"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_out_of_bounds"))
        # TODO: Throw an exception
        self.register_instruction(mips.LoadInmediateNode("$v0", "17"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "1"))
        self.register_instruction(mips.SystemCallNode())

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_not_out_of_bounds"))

    @visitor.when(cil.GetAttributeNode)
    def visit(self, node: cil.GetAttributeNode):
        node_id = hash(node)
        self.register_comment(f"Get attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"Get the address of {node.instance}"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"Get the attribute '{node.attr}' from the {node.instance}"))

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_get_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_get_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_get_attribute_{node_id}"))
        self.register_instruction(mips.StoreWordNode("$t1",f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.LabelNode(f"end_get_attribute_{node_id}"))

    @visitor.when(cil.SetAttributeNode)
    def visit(self, node: cil.SetAttributeNode):
        node_id = hash(node)
        self.register_comment(f"Set attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t0 = {node.instance}"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t1 = {node.source}"))

        self.register_instruction(mips.BeqNode("$t1", "$zero", f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_set_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_set_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_set_attribute_{node_id}"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.LabelNode(f"end_set_attribute_{node_id}"))

    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode):
        self.register_comment(f"Get method {node.method_name} of {node.type}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "12"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.method_index)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SllNode("$t1", "$t1", "2"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode):
        self.register_comment(f"initialize Array [{node.size}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.size)}($sp)").set_comment(f"$t0 = {node.size}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the size"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instantiation("$t0")
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = new Array[{node.size}]"))

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        self.register_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)").set_comment("$t1 = value in the position"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]"))

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        self.register_comment(f"array {node.instance}[4 * {node.index}] = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($t1)"))

    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode):
        self.register_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)").set_comment("$t1 = value in the position"))
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]"))
        self.register_instruction(mips.StoreWordNode("$t0", "8($t2)"))

    @visitor.when(cil.SetValueInIndexNode)
    def visit(self, node: cil.SetValueInIndexNode):
        self.register_comment(f"array {node.instance}[4 * {node.index}] = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($t1)"))

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        self.register_comment(f"{node.dest} = typeof {node.source} that is the first word of the object")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.AncestorNode)
    def visit(self, node: cil.AncestorNode):
        self.register_comment(f"{node.dest} = ancestor of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "4($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode):
        self.register_comment(f"{node.dest} = direction of {node.name}")
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.name}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        self.register_comment(f"{node.dest} = name of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t1)").set_comment(f"$t2 = direction of the type name"))
        self.register_instruction(mips.LoadAddressNode("$t3", "4($t2)").set_comment(f"$t3 = address of the name"))
        self.register_instruction(mips.LoadWordNode("$t2", "0($t2)").set_comment(f"$t2 = length of the name"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t2", "$t2", "9").set_comment(f"Setting space for the type, the size and the null byte"))
        self.register_instantiation("$t2")
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9").set_comment(f"Restoring space for the type, the size and the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t4", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t4", f"0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t4", "$v0", 0).set_comment("$t4 = direction of the new string"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.XorNode("$t5", "$t5", "$t5").set_comment("Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_name_start"))
        self.register_instruction(mips.BeqNode("$t5", "$t2", "while_copy_name_end"))
        self.register_instruction(mips.LoadByteNode("$t6", "0($t3)").set_comment("Loading the character"))
        self.register_instruction(mips.StoreByteNode("$t6", "0($t4)"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing the pointer to the new string"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment(f"Incrementing the pointer to the string in {node.source}"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_name_start"))
        self.register_instruction(mips.LabelNode("while_copy_name_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", "0($t4)").set_comment("Setting the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new string in {node.dest}"))

    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        self.register_comment(f"{node.dest} = copy of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)").set_comment(f"$t2 = length of {node.source} in bytes"))
        self.register_empty_instruction()

        self.register_comment("Allocating space for the new object")
        self.register_instantiation("$t2")
        self.register_instruction(mips.MoveNode("$t3", "$v0").set_comment("$t3 = direction of the new object"))
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()

        self.register_comment("Initializing the variable of the loop")
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("Pointer to the first character of the object"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "8").set_comment("Pointer to the first character of the object"))
        self.register_instruction(mips.AddiNode("$t2", "$2", "-8").set_comment("Decrementing in 8 the length of the object"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4").set_comment("Initializing counter"))
        self.register_empty_instruction()

        self.register_comment("Loop copying the object")
        self.register_instruction(mips.LabelNode("while_copy_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t2", "while_copy_end"))
        self.register_instruction(mips.LoadByteNode("$t5", "0($t0)").set_comment("Loading the byte"))
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)").set_comment("Storing the byte"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("Incrementing the pointer to the object"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment("Incrementing the pointer to the new object"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_start"))
        self.register_instruction(mips.LabelNode("while_copy_end"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new object in {node.dest}"))

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_addr)}($sp)").set_comment(f"$t0 = {node.str_addr}"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("Pointer to the first character of the string"))
        self.register_empty_instruction()

        self.register_comment(f"Printing the String {node.str_addr}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        self.register_comment(f"Printing the Int {node.source}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        self.register_instruction(mips.LoadWordNode("$a0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$a0", "8($a0)"))
        self.register_instruction(mips.SystemCallNode())
    
    @visitor.when(cil.PrintTypeNameNode)
    def visit(self, node: cil.PrintTypeNameNode):
        self.register_comment("Printing the type name")
        self.register_empty_instruction()
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.address)}($sp)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "12"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "4"))
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "8"))
        self.register_instruction(mips.LoadAddressNode("$a0", "buffer_input"))
        self.register_instruction(mips.LoadInmediateNode("$a1", "1024"))
        self.register_instruction(mips.SystemCallNode())


        self.register_empty_instruction()
        self.register_instruction(mips.XorNode("$t0", "$t0", "$t0").set_comment("Initializing counter"))
        self.register_instruction(mips.LabelNode("while_read_start"))
        self.register_instruction(mips.LoadByteNode("$t1", "buffer_input($t0)").set_comment("Loading the byte"))
        
        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.MoveNode("$a0", "$t1"))
        # self.register_instruction(mips.SystemCallNode())

        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.LoadInmediateNode("$a0", "0"))
        # self.register_instruction(mips.SystemCallNode())
        
        self.register_instruction(mips.AddiNode("$t2", "$zero", "10"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t2", "$zero", "13"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_read_start"))
        self.register_instruction(mips.LabelNode("while_read_end"))

        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.MoveNode("$a0", "$t0"))
        # self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "9").set_comment("Adding space for the type, the size and the null byte"))
        self.register_instantiation("$t0")
        self.register_instruction(mips.AddiNode("$t0", "$t0", "-9").set_comment("Adding space for the type, the size and the null byte"))
        self.register_instruction(mips.LoadAddressNode("$t2", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t2", "0($v0)").set_comment("Setting type in the first word of the object"))        
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting length in the second word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$v0", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4").set_comment("Initializing counter"))
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t0", "while_copy_from_buffer_end"))
        self.register_instruction(mips.LoadByteNode("$t5", "buffer_input($t4)").set_comment("Loading the byte"))
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)").set_comment("Storing the byte"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment("Imcremeenting pointer"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_end"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreByteNode("$zero", "0($t3)").set_comment("Storing the null byte"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new object in {node.dest}"))

    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "5"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v0", "8($t0)"))

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        self.register_instruction(mips.LabelNode(node.label))
    
    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        self.register_comment(f"Jumping to {node.address}")
        self.register_instruction(mips.JumpNode(node.address))
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        self.register_comment(f"If {node.condition} then goto {node.address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.condition)}($sp)").set_comment("Loading the address of the condition"))
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)").set_comment("Loading the value of the condition"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "1").set_comment("Setting the value to 1 for comparison"))
        self.register_instruction(mips.BeqNode("$t0", "$t1", node.address))

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        self.register_comment("Addition operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.AddNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 + $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        self.register_comment("Subtraction operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SubNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 - $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        self.register_comment("Multiplication operation")        
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t2 = $t0 * $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t2"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        self.register_comment("Division operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.DivNode("$t0", "$t1").set_comment("$t2 = $t0 / $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t2"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        self.register_comment("Xor operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.XorNode("$t2", "$t0", "$t1").set_comment("$t0 = $t0 ^ $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SltNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 < $t1"))
        self.postprocess_binary_int_operation(node, "Bool")
    
    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SleNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 <= $t1"))
        self.postprocess_binary_int_operation(node, "Bool")

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        self.register_comment("Equal operation")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand address"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand address"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 == $t1"))
        self.postprocess_binary_int_operation(node, "Bool")

    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.EqualAddressNode):
        self.register_comment(f"{node.dest} = EqualAddress({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))
    
    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode):
        self.register_comment(f"{node.dest} = EqualInt({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))

    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode):
        self.register_comment(f"{node.dest} = EqualStr({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "8"))

        self.register_empty_instruction()
        self.register_comment(f"By default we assume the strings are equals")
        self.register_instruction(mips.AddiNode("$t4", "$zero", "1"))
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t4", f"8($t5)"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_compare_strings_start"))
        self.register_instruction(mips.LoadByteNode("$t2", "0($t0)"))
        self.register_instruction(mips.LoadByteNode("$t3", "0($t1)"))

        self.register_instruction(mips.BeqNode("$t2", "$t3", "while_compare_strings_update"))
        
        self.register_empty_instruction()
        self.register_comment(f"The strings are no equals")
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$zero", f"8($t5)"))
        self.register_instruction(mips.JumpNode("while_compare_strings_end"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_compare_strings_update"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "1"))
        self.register_instruction(mips.BeqNode("$t2", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.BeqNode("$t3", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.JumpNode("while_compare_strings_start"))
        self.register_instruction(mips.LabelNode("while_compare_strings_end"))

    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        self.register_comment("Exit program")
        self.register_instruction(mips.LoadInmediateNode("$v0", "10"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        if node.value.isdigit():
            self.register_comment("Loading return value in $v1")
            self.register_instruction(mips.AddiNode("$v1", "$zero", f"{node.value}"))
            return
        offset = self.offset_of(node.value)
        self.register_comment("Loading return value in $v1")
        self.register_instruction(mips.LoadWordNode("$v1", f"{offset}($sp)"))

    
    def preprocess_binary_operation(self, node: cil.ArithmeticNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand address"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("Save in $t0 the left operand value"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand address"))
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)").set_comment("Save in $t1 the rigth operand value"))

    def postprocess_binary_int_operation(self, node: cil.ArithmeticNode, t: str):
        # self.register_instantiation(12)
        self.register_empty_instruction()
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"$t0 = {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)").set_comment(f"Setting value in the third word of the {t} object"))
