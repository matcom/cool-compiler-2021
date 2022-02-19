import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes

class COOL_to_CIL:
    def __init__(self, context, scope):
        self.context = context
        self.scope = scope


    @visitor.on('node')
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope=None):
        pass
    

    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self, node, scope):
        pass
    

    @visitor.when(nodes.MethDeclarationNode)
    def visit(self, node, scope):
        pass

    @visitor.when(nodes.AssignNode)
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.IfThenElseNode)
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope):
        pass
    

    @visitor.when(nodes.BlockNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.LetNode)
    def visit(self, node, scope):
        pass
            

    @visitor.when(nodes.CaseNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.NotNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.ConstantNumNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.ConstantBoolNode)
    def visit(self, node, scope):
       pass


    @visitor.when(nodes.ConstantStringNode)
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.VariableNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.InstantiateNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.IsVoidNode)
    def visit(self, node, scope):
        pass

    @visitor.when(nodes.ComplementNode)
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.PlusNode)
    def visit(self, node, scope):
        pass
    

    @visitor.when(nodes.MinusNode)
    def visit(self, node, scope):
       pass

    
    @visitor.when(nodes.StarNode)
    def visit(self, node, scope):
       pass


    @visitor.when(nodes.DivNode)
    def visit(self, node, scope):
       pass
    

    @visitor.when(nodes.LessThanNode)
    def visit(self, node, scope):
        pass

    
    @visitor.when(nodes.LessEqualNode)
    def visit(self, node, scope):
        pass
    

    @visitor.when(nodes.EqualNode)
    def visit(self, node, scope):
        pass