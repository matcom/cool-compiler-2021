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

    def register_ascii(self, name: str, value: str) -> mips.AsciizDataNode:
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
        
        self.register_space("buffer_input", 1024)

        for function_node in node.dotcode:
            self.visit(function_node)

        return mips.ProgramNode(self.dotdata, self.dottext)

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        size = 4 * (2 + len(node.attributes))

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name),f"type_{node.parent}" if node.parent != "null" else "0")
        self.register_word(self.to_data_type("attributes", node.name), str(len(node.attributes)))
        self.register_word(self.to_data_type("name_size", node.name), str(len(node.name)))
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
                if isinstance(instruction, cil.EmptyInstruction):
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
        if node.source.isdigit():
            self.register_instruction(mips.AddiNode("$t0", "$zero", node.source))
        else:
            self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}(sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}(sp)"))

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        if node.arg_index == 0:
            self.register_comment("Passing function arguments")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"-{4 * node.total_args + 4}").set_comment("Reserving space for arguments"))
            self.register_instruction(mips.StoreWordNode("$ra", f"{4 * (node.total_args)}($sp)").set_comment("Storing return address"))
            self.register_empty_instruction()
        self.register_comment(f"Argument {node.name}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.name) +  4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.total_args - node.arg_index - 1)}($sp)").set_comment(f"Storing {node.name}"))

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        self.register_comment(f"Calling function {node.method}")
        self.register_instruction(mips.JumpAndLinkNode(node.method))
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)").set_comment(f"{node.dest} = result of {node.method}"))
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

        self.register_instruction(mips.AddiNode("$t0", "$zero", f"{node.length}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"4($v0)").set_comment("Setting length of the string in the second word of the object"))
        self.register_empty_instruction()

        for i, c in enumerate(node.string):
            ec = c.replace('\n', '\\n')
            ec = ec.replace('\t', '\\t')
            ec = ec.replace('\b', '\\b')
            ec = ec.replace('\f', '\\f')
            self.register_instruction(mips.AddiNode("$t0", "$zero",  f"{ord(c)}"))
            self.register_instruction(mips.StoreByteNode("$t1", f"{i + 8}($v0)").set_comment(f"{node.dest}[{i}] = '{ec}'"))
            self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"{i + 9}($v0)").set_comment(f"Null-terminator at the end of the string"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.value}"))

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        self.register_comment(f"{node.dest} = length of {node.str_address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "4($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9").set_comment("Subtracting 9 for the type, length, and null-terminator"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        self.register_comment(f"{node.dest} = {node.str1} + {node.str2}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str1)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.str2)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)").set_comment("$t2 = length of str1"))
        self.register_instruction(mips.LoadWordNode("$t3", "4($t1)").set_comment("$t3 = length of str2"))
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
        self.register_instruction(mips.LoadByteNode("$t7", f"0($t0)"))
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
        self.register_instruction(mips.LoadByteNode("$t7", f"0($t1)"))
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
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.start)}($sp)").set_comment("$t2 = start of the substring"))
        self.register_instruction(mips.LoadWordNode("$t3", f"{self.offset_of(node.length)}($sp)").set_comment("$t3 = length of the substring"))
        self.register_instruction(mips.AddNode("t4", "$t2", "$t3").set_comment("$t4 = start of the substring + length of the substring"))

        self.register_empty_instruction()
        self.register_instruction(mips.BgeNode("$t4", "$t1", "substring_out_of_bounds"))
        
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

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        self.register_comment(f"Get attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"Get the address of {node.instance}"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"Get the attribute '{node.attr}' from the instance"))
        self.register_instruction(mips.StoreWordNode("$t1",f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.attr}"))

    @visitor.when(cil.SetAttributeNode)
    def visit(self, node: cil.SetAttributeNode):
        self.register_comment(f"Set attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t0 = {node.instance}"))
        if node.source.isdigit():
            self.register_instruction(mips.AddiNode("$t1", "$zero", node.source).set_comment(f"$t1 {node.source}"))
            self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"Set the attribute {node.attr} of {node.instance}"))
        else:
            self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t1 = {node.source}"))
            self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        self.register_comment(f"{node.dest} = typeof {node.source} that is the first word of the object")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.AncestorNode)
    def visit(self, node: cil.AncestorNode):
        self.register_comment(f"{node.dest} = ancestor of {node.source} that is the first word of the object")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "4($t0)"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeDirectionNode)
    def visit(self, node: cil.TypeDirectionNode):
        self.register_comment(f"{node.dest} = direction of {node.name}")
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.name}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        self.register_comment(f"{node.dest} = name of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "12($t1)").set_comment(f"$t1 = length of the name of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t3", "16($t1)").set_comment(f"$t1 = name of {node.source}"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t2", "$t2", "9").set_comment(f"Setting space for the type, the size and the null byte"))
        self.register_instantiation("$t2")
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9").set_comment(f"Restoring space for the type, the size and the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t4", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t4", f"0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.MoveNode("$t4", "$v0").set_comment("$t4 = direction of the new string"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment(f"Pointer to the first character of the string in {node.source}"))
        self.register_instruction(mips.XorNode("$t5", "$t5", "$t5").set_comment("Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_start"))
        self.register_instruction(mips.BeqNode("$t5", "$t1", "while_copy_end"))
        self.register_instruction(mips.LoadByteNode("$t6", "0($t0)").set_comment("Loading the character"))
        self.register_instruction(mips.StoreByteNode("$t6", "0($t4)"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing the pointer to the new string"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment(f"Incrementing the pointer to the string in {node.source}"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_start"))
        self.register_instruction(mips.LabelNode("while_copy_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", "0($t4)").set_comment("Setting the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$t4", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new string in {node.dest}"))

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

        self.register_comment(f"Printing the string {node.str_addr}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_empty_instruction()

        self.register_comment(f"Printing the string {node.source}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        self.register_instruction(mips.LoadWordNode("$a0", "8($t0)"))
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
        self.register_instruction(mips.LoadWordNode("$t1", "buffer_input($t0)").set_comment("Loading the byte"))
        self.register_instruction(mips.BeqNode("$t1", "$zero", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_read_start"))
        self.register_instruction(mips.LabelNode("while_read_end"))
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "9").set_comment("Adding space for the type, the size and the null byte"))
        self.register_instantiation("$t0")
        self.register_instruction(mips.LoadAddressNode("$t2", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t2", "0($v0)").set_comment("Setting type in the first word of the object"))        
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$v0", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4").set_comment("Initializing counter"))
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t0", "while_copy_from_buffer_end"))
        self.register_instruction(mips.LoadWordNode("$t5", "buffer_input($t4)").set_comment("Loading the byte"))
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

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new object in {node.dest}"))

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        self.register_instruction(mips.LabelNode(node.label))
    
    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        self.register_instruction(mips.JumpNode(node.address))
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.condition)}($sp)"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "1"))
        self.register_instruction(mips.BeqNode("$t0", "$t1", node.address))

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        self.register_comment("addition operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 + $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of addition in {node.dest}"))

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        self.register_comment("Subtraction operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SubNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 - $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of subtraction in {node.dest}"))
    
    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        self.register_comment("Multiplication operation")        
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of multiplication in {node.dest}"))

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        self.register_comment("Division operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.DivNode("$t0", "$t1").set_comment("$t0 = $t0 / $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of division in {node.dest}"))
    
    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        self.register_comment("Xor operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.XorNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 ^ $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of xor in {node.dest}"))

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        self.register_comment("Equal operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.XorNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 ^ $t1"))
        self.register_instruction(mips.SeqNode("$t0", "$t0", "$zero").set_comment("$t0 = $t0 == 0"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of equal in {node.dest}"))

    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SltNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 < $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of less than in {node.dest}"))

    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SleNode("$t0", "$t0", "$t1").set_comment("$t0 = $t0 <= $t1"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Store result of less than or equal in {node.dest}"))

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