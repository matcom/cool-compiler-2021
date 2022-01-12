import cil_ast as cil
from BaseCOOLToCILVisitor import *
from utils import visitor
from utils.ast import *

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

        cil_type_node = self.register_type(self.current_type)
        cil_type_node.attributes = self.current_type.get_all_attributes()
        
        if len(cil_type_node.attributes) != 0:
            constructor = FuncDeclarationNode(node.token, [], node.token, BlockNode([], node.token))
            func_declarations = [constructor]
            self.constructors.append(node.id)
            self.current_type.define_method(self.current_type.name, [], [], self.current_type, node.pos)
            scopes = [scope] + list(scope.functions.values())
        else:
            func_declarations = []
            scopes = list(scope.functions.values())

        for attr, a_type in cil_type_node.attributes:
            cil_type_node.attributes.append((attr.name, self.to_attribute_name(attr.name, a_type.name)))
            self.initialize_attr(constructor, attr, scope)
        if cil_type_node.attributes:
            constructor.body.expr_list.append(SelfNode())

        for method, mtype in self.current_type.all_methods():
            cil_type_node.methods.append((method.name, self.to_function_name(method.name, mtype.name)))

        func_declarations += [f for f in node.features if isinstance(f, FuncDeclarationNode)] 
        for feature, child_scope in zip(func_declarations, scopes):
            self.visit(feature, child_scope)

        self.current_type = None

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):        
        self.current_method = self.current_type.get_method(node.id)
        cil_name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(cil_name)

        self.register_param('self', self.current_type.name)
        for param_name, param_type in node.params:
            self.register_param(param_name, param_type.value)
        
        ret_value = self.visit(node.body, scope)
        if not isinstance(ret_value, str):
            result = self.define_internal_local()
            self.register_instruction(cil.AssignNode(result, ret_value))
            self.register_instruction(cil.ReturnNode(result))
        else:
            self.register_instruction(cil.ReturnNode(ret_value))   

        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(cil.SetAttrNode(self.vself.name, node.id, scope.ret_expr, self.current_type))
        elif node.type in self.value_types:
            local_value = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, local_value))
            self.register_instruction(cil.SetAttrNode(self.vself.name, node.id, local_value, self.current_type))

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            attributes_names = [attr.name for attr, attr_type in self.current_type.get_all_attributes()]
            self.register_instruction(cil.SetAttrNode('self', var_info.name, self.current_type.name, value))
        else:
            local_name = self.to_variable_name(var_info.name)
            self.register_instruction(cil.AssignNode(local_name, value))
        return value, typex

    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        pass
