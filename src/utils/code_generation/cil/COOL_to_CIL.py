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

        temp_f = self.current_function
        vtemp = self.define_internal_local()

        self.current_function = self.register_function(self.init_name(node.id, attr=True))
        self.register_param(self.vself)
        if node.parent != 'Object' and node.parent != 'IO':
            self.register_instruction(nodes_cil.ArgNode(self.vself.name))
            self.register_instruction(nodes_cil.StaticCallNode(self.init_name(node.parent, attr=True), vtemp))
        attr_declarations = (f for f in node.features if isinstance(f, nodes.AttrDeclarationNode))
        for feature in attr_declarations:
            self.visit(feature, scope)
        
        self.current_function = temp_f
        self.register_instruction(nodes_cil.ArgNode(instance))
        self.register_instruction(nodes_cil.StaticCallNode(self.init_name(node.id, attr=True), vtemp))
        self.register_instruction(nodes_cil.ReturnNode(instance))
        self.current_function = None
        self.current_type = None


    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self, node, scope):
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(nodes_cil.SetAttrNode(self.vself.name, node.id, scope._return, self.current_type))
        elif node.type in ['String', 'Int', 'Bool']:
            vtemp = self.define_internal_local()
            self.register_instruction(nodes_cil.AllocateNode(node.type, vtemp))
            self.register_instruction(nodes_cil.SetAttrNode(self.vself.name, node.id, vtemp, self.current_type))
    

    @visitor.when(nodes.MethDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, self.current_type.name))
        
        self.register_param(self.vself)
        for param_name, _ in node.params:
            self.register_param(VariableInfo(param_name, None))
        
        scope._return = None
        self.visit(node.body, scope)

        if scope._return is None:
            self.register_instruction(nodes_cil.ReturnNode(''))
        elif self.current_function.id == 'entry':
            self.register_instruction(nodes_cil.ReturnNode(0))
        else:
            self.register_instruction(nodes_cil.ReturnNode(scope._return))
        
        self.current_method = None


    @visitor.when(nodes.AssignNode)
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.IfThenElseNode)
    def visit(self, node, scope):
        vresult = self.register_local(VariableInfo('if_then_else_value', None))
        vcondition = self.define_internal_local()

        then_label_node = self.register_label('then_label')
        else_label_node = self.register_label('else_label')
        continue_label_node = self.register_label('continue_label')

        self.visit(node.if_expr, scope)
        self.register_instruction(nodes_cil.GetAttrNode(vcondition, scope._return, 'value', 'Bool'))
        self.register_instruction(nodes_cil.IfGotoNode(vcondition, then_label_node.label))
        
        self.register_instruction(nodes_cil.GotoNode(else_label_node.label))
        
        self.register_instruction(then_label_node)
        self.visit(node.then_expr, scope)
        self.register_instruction(nodes_cil.AssignNode(vresult, scope._return))
        self.register_instruction(nodes_cil.GotoNode(continue_label_node.label))
        
        self.register_instruction(else_label_node)
        self.visit(node.else_expr, scope)
        self.register_instruction(nodes_cil.AssignNode(vresult, scope._return))

        self.register_instruction(continue_label_node)
        scope._return = vresult


    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope):
        vcondition = self.define_internal_local()
        while_label_node = self.register_label('while_label')
        loop_label_node = self.register_label('loop_label')
        pool_label_node = self.register_label('pool_label')
        
        self.register_instruction(while_label_node)
        self.visit(node.conditional_expr, scope)
        self.register_instruction(nodes_cil.GetAttrNode(vcondition, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(nodes_cil.IfGotoNode(vcondition, loop_label_node.label))
        
        self.register_instruction(nodes_cil.GotoNode(pool_label_node.label))
        self.register_instruction(loop_label_node)
        self.visit(node.loop_expr, scope)
        
        self.register_instruction(nodes_cil.GotoNode(while_label_node.label))
        self.register_instruction(pool_label_node)

        scope.ret_expr = nodes_cil.VoidNode()
    

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