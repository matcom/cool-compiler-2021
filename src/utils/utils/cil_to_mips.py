from utils import visitor
from utils import ast_nodes_cil as cil


class CILToMIPSVisitor:
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(cil.TypeNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.DataNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.FunctionNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ParamNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node, scope):
        pass 

    @visitor.when(cil.AssignNode)
    def visit(self, node, scope):
        pass 

    @visitor.when(cil.ArithmeticNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.PlusNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.MinusNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.StarNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.DivNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.GetAttribNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.SetAttribNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.GetIndexNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.SetIndexNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.AllocateNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ArrayNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(cil.TypeOfNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(cil.LabelNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.GotoNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.GotoIfNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.StaticCallNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ArgNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ReturnNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.LoadNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.LengthNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ConcatNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.PrefixNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.SubstringNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ToStrNode)
    def visit(self, node, scope):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(cil.PrintNode)
    def visit(self, node, scope):
        pass

