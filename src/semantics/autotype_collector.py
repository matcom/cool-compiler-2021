from semantics.tools import conforms, join, join_list, smart_add
import semantics.visitor as visitor
from semantics.tools import Context, ErrorType, Scope, SelfType, SemanticError, TypeBag
from parsing.ast import ArithmeticNode, AssignNode, AttrDeclarationNode, BlocksNode, BooleanNode, CaseNode, CaseOptionNode, ClassDeclarationNode, ComparerNode, ComplementNode, ConditionalNode, InstantiateNode, IntNode, IsVoidNode, LetNode, LoopNode, MethodCallNode, MethodDeclarationNode, Node, NotNode, ProgramNode, StringNode, VarDeclarationNode, VariableNode

class AutotypeCollector:
    def __init__(self, context:Context, errors):
        self.context = context
        self.current_type = None
        self.errors = errors
    
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
        expr_clone = node_expr.clone()
        if not conforms(node_expr, node_type):
            self.add_error(node, f"Type Error: In class '{self.current_type.name}' attribue '{node.id}' expression type({expr_clone.name}) does not conforms to declared type ({node_type.name}).")
            # What is made error type here!!!

        var = scope.find_variable(node.id)
        var.type = node_type

        node.inferenced_type = node_type
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex):
        scope = scopex.create_child()
        current_method = self.current_type.get_method(node.id)
        for idx, typex in zip(current_method.param_names, current_method.param_types):
            scope.define_variable(idx, typex)
        
        ret_type_decl = current_method.return_type.swap_self_type(self.current_type)
        self.visit(node.body, scope)
        ret_type_expr = node.body.inferenced_type

        ret_expr_clone = ret_type_expr.clone()
        if not conforms(ret_type_expr, ret_type_decl):
            self.add_error(node, f"Type Error: In Class \'{self.current_type.name}\' method \'{current_method.name}\' return expression type({ret_expr_clone.name}) does not conforms to declared return type ({ret_type_decl.name})")
            ret_type_expr = ErrorType()

        node.inferenced_type = ret_type_expr
        ret_type_decl.swap_self_type(self.current_type, back = True)
    
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
        
        condition_clone = condition_type.clone()
        if not conforms(condition_clone, bool_type):
            self.add_error(node, f"Type Error: If's condition type({condition_type.name}) does not conforms to Bool type.")

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
        types_visited = set()
        for option in node.options:
            child = scope.create_child()
            self.visit(option, child)
            type_list.append(option.inferenced_type)
            var_type = child.find_variable(option.id).type
            if var_type in types_visited:
                self.add_error(node, f"Semantic Error: Case Expression can't have branches with same case type({var_type.name})")
        
        joined_type = join_list(type_list)
        node.inferenced_type = joined_type
    
    @visitor.when(CaseOptionNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.type, selftype=False, autotype=False)
        except SemanticError as err:
            self.add_error(node, err)
            node_type = ErrorType()
        
        scope.define_variable(node.id, node_type)
        self.visit(node.expr, scope)
        node.inferenced_type = node.expr.inferenced_type

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        condition_type = node.condition.inferenced_type
        bool_type = self.context.get_type("Bool")
        
        condition_clone = condition_type.clone()
        if not conforms(condition_clone, bool_type):
            self.add_error(node, f"Type Error: Loop condition type({condition_type.name}) does not conforms to Bool type.")

        self.visit(node.body, scope)
        node.inferenced_type = self.context.get_type("Object")
    
    @visitor.when(LetNode)
    def visit(self, node, scope):
        child = scope.create_child()
        for var in node.var_decl_list:
            self.visit(var, child)
        self.visit(node.in_expr, child)
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
            self.add_error(node, f"Semantic Error: Variable \'{node.id}\' already defined in current scope.")
            node.defined = False
            node_type = ErrorType()
        
        if node.expr:
            self.visit(node.expr, scope)
            expr_type = node.expr.inferenced_type
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                self.add_error(node, f"Semantic Error: Variable \'{node.id}\' expression type({expr_clone.name}) does not conforms to declared type({node_type.name}).")
        
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
        node_type = var_type

        if var and var.name != 'self':
            node_expr_clone = node.expr.inferenced_type.clone()
            if not conforms(node_expr, var_type):
                self.add_error(node, f"Type Error: Cannot assign new value to variable '{node.id}'. Expression type({node_expr_clone.name}) does not conforms to declared type ({var_type.name}).")
                node_type = ErrorType()
            var.type = var_type
        elif var.name =='self':
            self.add_error(node, "Semantic Error: Cannot assign new value. Variable 'self' is Read-Only.")
            node_type = ErrorType()

        node.inferenced_type = node_type

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

            bridge_clone = bridge.clone()
            if not conforms(bridge, caller):
                self.add_error(node, f"Semantic Error: Cannot effect dispatch because expression type({bridge_clone.name}) does not conforms to caller type({caller.name}).")
                caller = ErrorType()
        
        

        methods = None
        if len(caller.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(node.id, len(node.args))
            types = [typex for _, typex in methods_by_name]
            conforms(caller, TypeBag(set(types), types))
            if len(caller.type_set):
                methods = [(t, t.get_method) for t in caller.heads]
            else:
                self.add_error(node, f"Semantic Error: There is no method \'{node.id}\' that recieves {len(node.params)} arguments in Types {caller.name}.")
                caller = ErrorType()
        elif len(caller.type_set) == 1:
            caller_type = caller.heads[0]
            try:
                methods = [(caller_type, caller_type.get_method(node.id))]
            except SemanticError:
                self.add_error(node, f"Semantic Error: There is no method \'{node.id}\' that recieves {len(node.params)} arguments in Type \'{caller.name}\'.")
                caller = ErrorType()

        if methods:
            type_set = set()
            heads = []
            for typex, method in methods:
                ret_type = method.return_type.clone()
                ret_type.swap_self_type(typex)
                type_set = smart_add(type_set, heads, ret_type)
            for i in range(len(node.args)):
                arg = node.args[i]
                self.visit(arg, scope)
                #    arg_type = arg.inferenced_type
                #    arg_clone = arg_type.clone()
                #    conforms(arg_clone, param_type)
            node.inferenced_type = TypeBag(type_set, heads)
        else:
            node.inferenced_type = ErrorType()
        node.inferenced_caller = caller
    
    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.inferenced_type
        left_clone = left_type.clone()

        self.visit(node.right, scope)
        right_type = node.right.inferenced_type
        right_clone = right_type.clone()

        int_type = self.context.get_type("Int")
        if not conforms(left_type, int_type):
            self.add_error(node.left, f"Type Error: Arithmetic Error: Left member type({left_clone.name}) does not conforms to Int type.")
        if not conforms(right_type, int_type):
            self.add_error(node.right, f"Type Error: Arithmetic Error: Right member type({right_clone.name}) does not conforms to Int type.")
        
        node.inferenced_type = int_type

    @visitor.when(ComparerNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.inferenced_type

        self.visit(node.right, scope)
        right_type = node.right.inferenced_type

        bool_type = self.context.get_type("Bool")
        left_clone = left_type.clone()
        right_clone = right_type.clone()
        if not conforms(left_clone, right_type) and not conforms(right_clone, left_type):
            self.add_error(node, f"Type Error: Left expression type({left_type.name}) does not conforms to right expression type({right_type.name})")

        node.inferenced_type = bool_type
    
    @visitor.when(VariableNode)
    def visit(self, node, scope:Scope):
        var = scope.find_variable(node.value)
        if var:
            node.defined = True
            var_type = var.type
        else:
            node.defined = False
            var_type = ErrorType()
            self.add_error(node, f"Semantic Error: Variable '{node.value}' is not defined.")
        node.inferenced_type = var_type

    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.inferenced_type
        expr_clone = expr_type.clone()
        bool_type = self.context.get_type("Bool")
        if not conforms(expr_type, bool_type):
            self.add_error(node, f"Type Error: Not's expresion type({expr_clone.name} does not conforms to Bool type")

        node.inferenced_type = bool_type
    
    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expr_type = node.expr.inferenced_type
        expr_clone = expr_type.clone()
        node_type = self.context.get_type("Int")
        
        if not conforms(expr_type, node_type):
            self.add_error(node, f"Type Error: Not's expresion type({expr_clone.name} does not conforms to Int type")
            node_type = ErrorType()
        
        node.inferenced_type = node_type
    
    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.inferenced_type = self.context.get_type("Bool")
    
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.value, selftype=False, autotype=False)
        except SemanticError as err:
            self.add_error(f"Semantic Error: Could not instantiate type '{node.value}'.")
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

    def add_error(self, node:Node, text:str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line,col), f"({line}, {col}) - " + text))