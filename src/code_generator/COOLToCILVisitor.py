import cil_ast as cil
from BaseCOOLToCILVisitor import *
from utils import visitor
from parser.ast import *

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))

        #self.register_instruction(cil.CallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.CallNode(result, self.to_function_name('main', 'Main'), [cil.ArgNode(instance)], 'Main'))

        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

       # self.create_built_in()

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        type_node = self.register_type(node.id)
        type_node.attributes = [attr.name for attr, _ in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]
          
        func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)


        #init
        self.current_function = self.register_function(self.init_name(node.id))
        #allocate
        instance = self.register_local('instance')
        self.register_instruction(cil.AllocateNode(node.id, instance))  

        func = self.current_function
        vtemp = self.define_internal_local()

        #init_attr
        self.current_function = self.register_function(self.init_name(node.id, attr=True))
        self.register_param(self.vself)
        if node.parent != 'Object' and node.parent != 'IO':
            self.register_instruction(cil.ArgNode(self.vself.name))
            self.register_instruction(cil.CallNode(self.init_name(node.parent, attr=True), vtemp))
        attr_declarations = (f for f in node.features if isinstance(f, AttrDeclarationNode))
        for feature in attr_declarations:
            self.visit(feature, scope)
        
        self.current_function = func
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(self.init_name(node.id, attr=True), vtemp))

        self.register_instruction(cil.ReturnNode(instance))
        self.current_function = None       
                
        self.current_type = None







