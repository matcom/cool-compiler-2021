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
        pass

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        pass

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        pass

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        pass 

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        pass 
    
    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode):
        pass 

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
        pass

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