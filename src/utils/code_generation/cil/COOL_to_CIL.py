import cmp.visitor as visitor
from cmp.semantic import VariableInfo
from utils.ast.AST_Nodes import ast_nodes as nodes
from utils.code_generation.cil.AST_CIL import cil_ast as nodes_cil
from utils.code_generation.cil.Base_COOL_to_CIL import BaseCOOLToCIL

class COOLtoCIL(BaseCOOLToCIL):
    def __init__(self, context):
        BaseCOOLToCIL.__init__(self, context)


    @visitor.on('node')
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope=None):
        self.current_function = self.register_function('entry')
        result = self.define_internal_local()
        instance = self.register_local(VariableInfo('instance', None))
        self.register_instruction(nodes_cil.StaticCallNode(self.init_name('Main'), instance))
        self.register_instruction(nodes_cil.ArgNode(instance))
        self.register_instruction(nodes_cil.StaticCallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(nodes_cil.ReturnNode(0))
       
        self.register_data('Aborting... in class ')
        self.register_built_in()
        self.current_function = None
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return nodes_cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    

    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        
        type_node = self.register_type(node.id)
        type_node.attributes = [attr.name for attr, _ in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]

        func_declarations = (f for f in node.features if isinstance(f, nodes.MethDeclarationNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)

        self.current_function = self.register_function(self.init_name(node.id))
        
        instance = self.register_local(VariableInfo('instance', None))
        self.register_instruction(nodes_cil.AllocateNode(node.id, instance))  

        func = self.current_function
        vtemp = self.define_internal_local()

        self.current_function = self.register_function(self.init_name(node.id, attr=True))
        self.register_param(self.vself)
        if node.parent != 'Object' and node.parent != 'IO':
            self.register_instruction(nodes_cil.ArgNode(self.vself.name))
            self.register_instruction(nodes_cil.StaticCallNode(self.init_name(node.parent, attr=True), vtemp))
        attr_declarations = (f for f in node.features if isinstance(f, nodes.AttrDeclarationNode))
        for feature in attr_declarations:
            self.visit(feature, scope)
        
        self.current_function = func
        self.register_instruction(nodes_cil.ArgNode(instance))
        self.register_instruction(nodes_cil.StaticCallNode(self.init_name(node.id, attr=True), vtemp))

        self.register_instruction(nodes_cil.ReturnNode(instance))
        self.current_function = None
                
        self.current_type = None

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