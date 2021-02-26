from semantics.tools import conforms, join, join_list, smart_add
import semantics.visitor as visitor
from semantics.tools import Context, ErrorType, Scope, SelfType, SemanticError, TypeBag
from parsing.ast import ArithmeticNode, AssignNode, AttrDeclarationNode, BlocksNode, BooleanNode, CaseNode, CaseOptionNode, ClassDeclarationNode, ComparerNode, ComplementNode, ConditionalNode, InstantiateNode, IntNode, IsVoidNode, LetNode, LoopNode, MethodCallNode, MethodDeclarationNode, NotNode, ProgramNode, StringNode, VarDeclarationNode, VariableNode

class AutotypeCollector:
    def __init__(self, context:Context):
        self.context = context
        self.current_type = None
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode) -> Scope:
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id, unpacked=True)
        scope.define_variable("self", TypeBag({self.current_type}))
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)
        
        for feature in node.features:
            self.visit(feature, scope)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        node_type = self.current_type.get_attribute(node.id).type.swap_self_type(self.current_type)
        if not node.expr:
            node.inferenced_type = node_type
            return
        
        self.visit(node.expr, scope)
        node_expr = node.expr.inferenced_type
        conforms(node_expr, node_type)

        var = scope.find_variable(node.id)
        var.type = node_type

        node.inferenced_type = node_type
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex):
        scope = scopex.create_child()
        current_method = self.current_type.get_method(node.id)
        for idx, typex in zip(current_method.param_names, current_method.param_types):
            scope.define_variable(idx, typex)
        
        self.visit(node.body, scope)
        ret_type_decl = current_method.return_type.swap_self_type(self.current_type)
        ret_type_expr = node.body.inferenced_type
        conforms(ret_type_expr, ret_type_decl)
        node.body.inferenced_type = ret_type_expr

        node.inferenced_type = ret_type_decl.clone()
        ret_type_decl.swap_types(SelfType(), self.current_type)
    
    @visitor.when(BlocksNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            self.visit(expr, scope)
        node.inferenced_type = node.expr_list[-1].inferenced_type
    
    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        condition_type = node.condition.inferenced_type
        bool_type = self.context.get_type("Bool")
        conforms(condition_type, bool_type)

        self.visit(node.then_body, scope)
        then_type = node.then_body.inferenced_type
        self.visit(node.else_body, scope)
        else_type = node.else_body.inferenced_type

        joined_type = join(then_type, else_type)
        node.inferenced_type = joined_type
    
    @visitor.when(CaseNode)
    def visit(self, node, scope:Scope):
        self.visit(node.case_expr, scope)

        type_list = []
        for var in node.options:
            child = scope.create_child()
            self.visit(var, child)
            type_list.append(var.inferenced_type)
        
        joined_type = join_list(type_list)
        node.inferenced_type = joined_type
    
    @visitor.when(CaseOptionNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type, selftype=False, autotype=False)
        except SemanticError as err:
            node_type = ErrorType()
        
        scope.define_variable(node.id, node_type)
        self.visit(node.expr, scope)
        node.inferenced_type = node.expr.inferenced_type

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        condition_type = node.condition.inferenced_type
        bool_type = self.context.get_type("Bool")
        conforms(condition_type, bool_type)

        self.visit(node.body, scope)
        node.inferenced_type = self.context.get_type("Object")
    
    @visitor.when(LetNode)
    def visit(self, node, scope):
        child = scope.create_child()
        for var in node.var_decl_list:
            self.visit(var, child)
        self.visit(node.in_expr, scope)
        node.inferenced_type = node.in_expr.inferenced_type
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type).swap_self_type(self.current_type)
        except SemanticError as err:
            node_type = ErrorType()
        
        if not scope.is_local(node.id):
            scope.define_variable(node.id, node_type)
            node.defined = True
        else:
            #add error
            node.defined = False
        
        if node.expr:
            self.visit(node.expr, scope)
            expr_type = node.expr.inferenced_type
            conforms(expr_type, node_type)
            node.expr.inferenced_type = expr_type
        
        node.inferenced_type = node_type

    @visitor.when(AssignNode)
    def visit(self, node, scope:Scope):
        var = scope.find_variable(node.id)
        if not var:
            var_type = ErrorType()
            node.defined = False
        else:
            var_type = var.type.swap_self_type(self.current_type)
            node.defined = True
        
        self.visit(node.expr, scope)
        node_expr = node.expr.inferenced_type

        if var and var.name != 'self':
            conforms(node_expr, var_type)
            var.type = var_type
        node.inferenced_type = var_type

    @visitor.when(MethodCallNode)
    def visit(self, node, scope):
        if node.expr == None:
            caller = TypeBag({self.current_type})
        elif node.type == None:
            self.visit(node.expr, scope)
            caller = node.expr.inferenced_type
        else:
            self.visit(node.expr, scope)
            bridge = node.expr.inferenced_type
            caller = self.context.get_type(node.type, selftype=False, autotype=False)
            conforms(bridge, caller)
        
        methods = None
        if len(caller.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(node.id, len(node.args))
            types = [typex for _, typex in methods_by_name]
            conforms(caller, TypeBag(set(types)))
            if len(caller.type_set):
                methods = [(t, t.get_method) for t in caller.heads]
            else:
                pass #Add Error
        elif len(caller.type_set) == 1:
            caller_type = caller.heads[0]
            try:
                methods = [(caller_type, caller_type.get_method(node.id))]
            except SemanticError:
                pass #Add Error
        
        if methods:
            type_set = set()
            heads = []
            for typex, method in methods:
                ret_type = method.return_type.clone()
                ret_type.swap_self_type(typex)
                smart_add(type_set, heads, ret_type)
                for i in range(len(node.args)):
                    arg, param_type = node.args[i], method.param_types[i]
                    self.visit(arg, scope)
                    arg_type = arg.inferenced_type
                    conforms(arg_type, param_type)
            node.inferenced_type = TypeBag(type_set, heads)
        else:
            node.inferenced_type = ErrorType()
    
    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.inferenced_type

        self.visit(node.right, scope)
        right_type = node.right.inferenced_type

        int_type = self.context.get_type("Int")
        conforms(left_type, int_type)
        conforms(right_type, int_type)
        node.inferenced_type = int_type

    @visitor.when(ComparerNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.inferenced_type

        self.visit(node.right, scope)
        right_type = node.right.inferenced_type

        conforms(left_type, right_type)
        conforms(right_type, left_type)
        node.inferenced_type = self.context.get_type("Bool")
    
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        var = scope.find_variable(node.value)
        if var:
            node.defined = True
            var_type = var.type
        else:
            node.defined = False
            var_type = ErrorType()
        node.inferenced_type = var_type

    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.inferenced_type
        bool_type = self.context.get_type("Bool")
        conforms(expr_type, bool_type)

        node.inferenced_type = bool_type
    
    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.inferenced_type
        int_type = self.context.get_type("int")
        conforms(expr_type, int_type)

        node.inferenced_type = int_type
    
    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.inferenced_type = self.context.get_type("Bool")
    
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.value, selftype=False, autotype=False)
        except SemanticError as err:
            node_type = ErrorType()
        node.inferenced_type = node_type

    @visitor.when(IntNode)
    def visit(self, node, scope):
        node.inferenced_type = self.context.get_type("Int")
    
    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.inferenced_type = self.context.get_type("String")
    
    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        node.inferenced_type = self.context.get_type("Bool")



# todo: Revisar los auto types que me hace falta y que no
# todo: completar de manera acorde el autotype collector
# todo: Annadir error en VarDeclarationNode
# todo: Annadir error en MethodCallNode (2)
# todo: annadir error en INsyantiate Node
# todo: Cambiar self.error a que cada error tengo la tupla de localizacion, asi permite organizar los errores
