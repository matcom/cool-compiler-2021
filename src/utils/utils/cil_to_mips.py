from . import visitor
from . import ast_nodes_cil as cil


class BaseCILToMIPSVisitor:
    def __init__(self, context):
        self.dotdata = []
        self.dottext = []
        self.context = context

        # self.current_type = None
        # self.current_method = None
        # self.current_function = None

    
        
class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode, scope):
        for type_node in node.dottypes:
            self.visit(type_node)

        for function_node in node.dotcode:
            self.visit(function_node)

        for data_node in node.data:
            self.visit(data_node)
        
        return #mips.programNode o el string del programa de mips???
    
    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode, scope):
        #por cada atributo reservo una palabra
        pass

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode, scope):
        pass

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode, scope):
        pass

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode, scope):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode, scope):
        pass 

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode, scope):
        pass 
    
    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode, scope):
        pass 

    @visitor.when(cil.ParentNode)
    def visit(self, node: cil.ParentNode, scope):
        pass 

    @visitor.when(cil.ArithmeticNode)
    def visit(self, node: cil.ArithmeticNode, scope):
        pass

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode, scope):
        pass

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode, scope):
        pass

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode, scope):
        pass

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode, scope):
        pass
    
    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode, scope):
        pass

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode, scope):
        pass
    
    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode, scope):
        pass
    
    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode, scope):
        pass
    
    @visitor.when(cil.CommentNode)
    def visit(self, node: cil.CommentNode, scope):
        pass
    
    @visitor.when(cil.EndOfLineNode) ######
    def visit(self, node: cil.EndOfLineNode, scope):
        pass

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode, scope):
        pass

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode, scope):
        pass

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode, scope):
        pass

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode, scope):
        pass
    
    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode, scope):
        pass

    @visitor.when(cil.SetMethodNode)
    def visit(self, node: cil.SetMethodNode, scope):
        pass
    
    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode, scope):
        pass

    @visitor.when(cil.SetValueInIndexNode)
    def visit(self, node: cil.SetValueInIndexNode, scope):
        pass

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode, scope):
        pass
    
    @visitor.when(cil.AllocateIntNode)
    def visit(self, node: cil.AllocateIntNode, scope):
        pass
    
    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode, scope):
        pass
    
    @visitor.when(cil.AllocateNullNode)
    def visit(self, node: cil.AllocateNullNode, scope):
        pass

    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode, scope):
        pass
    
    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode, scope):
        pass
    
    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode, scope):
        pass

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode, scope):
        pass

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode, scope):
        pass

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode, scope):
        pass

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode, scope):
        pass

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode, scope):
        pass

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode, scope):
        pass

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode, scope):
        pass

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode, scope):
        pass

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode, scope):
        pass

    @visitor.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode, scope):
        pass

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode, scope):
        pass

    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode, scope):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode, scope):
        pass
    
    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode, scope):
        pass
    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode, scope):
        pass
    
    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode, scope):
        pass
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.PrintIntNode, scope):
        pass
    
    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode, scope):
        pass

    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode, scope):
        pass
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode, scope):
        pass
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode, scope):
        pass
    
    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode, scope):
        pass
    
    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode, scope):
        pass
    
    @visitor.when(cil.EmptyInstructionNode)
    def visit(self, node: cil.EmptyInstructionNode, scope):
        pass