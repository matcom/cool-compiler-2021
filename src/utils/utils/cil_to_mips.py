from . import visitor
from . import ast_nodes_cil as cil
from . import ast_nodes_mips as mips


class BaseCILToMIPSVisitor:
    def __init__(self, context):
        self.dotdata = []
        self.dottext = []
        
        self.context = context

        self.current_function = None
        self.current_function_stk = []

    ## basic methods
    def register_instruction(self, instruction):
        self.dottext.append(instruction)
        return instruction

    def register_empty_instruction(self):
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]
    
    def register_empty_data(self):
        self.dotdata.append(mips.EmptyDataNode())

    def register_comment(self, comment):
        self.dottext.append(mips.CommentNode(comment))
        return self.dottext[-1]
    
    ## register basic data types
    def register_word(self, name, value):
        data = mips.WordDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_asciiz(self, name, value):
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_space(self, name, value):
        data = mips.SpaceDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_instantiation(self, size) -> mips.InstructionNode:
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        if isinstance(size, int):
            self.register_instruction(mips.AddiNode("$a0", "$zero", f"{size}"))
        if isinstance(size, str):
            self.register_instruction(mips.MoveNode("$a0", size))
        self.register_instruction(mips.SystemCallNode())

    
    
        
class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        for type_node in node.dottypes:
            self.visit(type_node)

        for function_node in node.dotcode:
            self.visit(function_node)

        for data_node in node.data:
            self.visit(data_node)
        
        return mips.ProgramNode(self.dotdata, self.dottext)
    
    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        #por cada atributo reservo una palabra
        size = 4 * (len(node.attributes) + len(node.methods))

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name), f"type_{node.parent}" if node.parent != "null" else "0")
        self.register_word(self.to_data_type("name_address", node.name), f"type_{node.name}_name_size")
        
        for method, function in node.methods:
            self.register_word(self.to_data_type(method, node.name), function)
        
        self.register_empty_data()

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        pass

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        self.current_function = node
        self.register_instruction(mips.LabelNode(node.name))

        param_names = [x.name for x in self.current_function.params]
        local_names = [x.name for x in self.current_function.local_vars]
        self.current_function_stack = ["$ra"] + param_names + local_names

        locals_size = 4 * len(self.current_function.local_vars)
        stack_size = 4 * len(self.current_function_stack)
        

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        pass 

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        self.register_comment(f"{node.dest} = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
    
    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode):
        self.register_comment(f"{node.dest} = {node.source} where {node.source} is an integer")
        self.register_instantiation(12)
        
        # puntero para node.source
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        # $t1 = type of node.source
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)"))
        # $t2 = value of node.source
        self.register_instruction(mips.LoadWordNode("$t2", "8($t0)"))
    
        # Save type of node.dest
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)"))
        # Save size of node.dest
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        # Save value of node.dest
        self.register_instruction(mips.StoreWordNode("$t2", "8($v0)"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ParentNode)
    def visit(self, node: cil.ParentNode):
        pass 

    @visitor.when(cil.ArithmeticNode)
    def visit(self, node: cil.ArithmeticNode):
        pass

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        pass

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        pass

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        pass

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        pass
    
    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        pass

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        pass
    
    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        pass
    
    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        pass
    
    @visitor.when(cil.CommentNode)
    def visit(self, node: cil.CommentNode):
        pass
    
    @visitor.when(cil.EndOfLineNode) ######
    def visit(self, node: cil.EndOfLineNode):
        pass

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        pass

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        pass

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        pass

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        pass
    
    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode):
        pass

    @visitor.when(cil.SetMethodNode)
    def visit(self, node: cil.SetMethodNode):
        pass
    
    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode):
        pass

    @visitor.when(cil.SetValueInIndexNode)
    def visit(self, node: cil.SetValueInIndexNode):
        pass

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        pass
    
    @visitor.when(cil.AllocateIntNode)
    def visit(self, node: cil.AllocateIntNode):
        pass
    
    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode):
        pass
    
    @visitor.when(cil.AllocateNullNode)
    def visit(self, node: cil.AllocateNullNode):
        pass

    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode):
        pass
    
    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        pass
    
    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        pass

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        pass

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        pass

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        pass

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        pass

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        if node.arg_index == 0:
            self.register_comment("Passing function arguments")
            ## reservando espacio para los argumentos
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"-{4 * node.total_args + 4}"))
            ## funcion de retorno (espacio)
            self.register_instruction(mips.StoreWordNode("$ra", f"{4 * (node.total_args)}($sp)"))
            self.register_empty_instruction()
        
        self.register_comment(f"Argument {node.name}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.name) +  4 * node.total_args + 4}($sp)"))
        # guardando el node.name
        self.register_instruction(mips.StoreWordNode("$t0", f"{4 * (node.total_args - node.arg_index - 1)}($sp)"))


    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        pass

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        pass

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        pass

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        pass

    @visitor.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode):
        pass

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        pass

    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        pass
    
    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        pass
    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        pass
    
    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        pass
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        pass
    
    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.PrintIntNode):
        pass
    
    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode):
        pass

    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode):
        pass
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode):
        pass
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        pass
    
    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        pass
    
    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        pass
    
    @visitor.when(cil.EmptyInstructionNode)
    def visit(self, node: cil.EmptyInstructionNode):
        pass
    
    
class MipsFormatter:
    pass