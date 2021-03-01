from parsing.parsing_rules import p_param
import semantics.visitor as visitor
from parsing.ast import ArithmeticNode, AssignNode, AttrDeclarationNode, BlocksNode, CaseNode, CaseOptionNode, ClassDeclarationNode, ComparerNode, ComplementNode, ConditionalNode, EqualsNode, IsVoidNode, LetNode, LoopNode, MethodCallNode, MethodDeclarationNode, Node, NotNode, ProgramNode, VarDeclarationNode, VariableNode
from semantics.tools import Context, ErrorType, Scope, TypeBag, conforms, equal, join, join_list, smart_add

class AutotypeInferencer:
    def __init__(self, context:Context, errors) -> None:
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration in node.declarations:
            self.visit(declaration, scope.next_child())
        
        scope.reset()

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id, unpacked=True)
        for feature in node.features:
            self.visit(feature, scope)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expr:
            return
        
        node_infered = node.inferenced_type
        expr_infered = node.expr.inferenced_type.clone()

        self.visit(node.expr, scope)
        new_expr_infered = node.expr.inferenced_type
        
        if equal(expr_infered, new_expr_infered):
            return
        
        new_clone_inferred = new_expr_infered.clone()
        if not conforms(new_expr_infered, node_infered):
            self.add_error(node, f"Type Error: In class '{self.current_type.name}' attribue '{node.id}' expression type({new_clone_inferred.name}) does not conforms to declared type ({node_infered.name}).")
            # What is made error type here!!!
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex:Scope):
        scope = scopex.next_child()
        
        ret_type_infered = node.body.inferenced_type.clone()
        self.visit(node.body, scope)
        new_type_infered = node.body.inferenced_type
        
        if equal(ret_type_infered, new_type_infered):
            return
        
        current_method = self.current_type.get_method(node.id)
        ret_type_decl = current_method.return_type.swap_self_type(self.current_type)
        new_clone_infered = new_type_infered.clone()

        if not conforms(new_type_infered, ret_type_decl):
            self.add_error(node, f"Type Error: In Class \'{self.current_type.name}\' method \'{current_method.name}\' return expression type({new_clone_infered.name}) does not conforms to declared return type ({ret_type_decl.name})")
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
        condition_infered = node.condition.inferenced_type.clone()
        then_infered = node.then_body.inferenced_type.clone()
        else_infered = node.else_body.inferenced_type.clone()

        self.visit(node.condition, scope)
        self.visit(node.then_body, scope)
        self.visit(node.else_body, scope)

        new_condition_infered = node.condition.inferenced_type
        new_then_infered = node.then_body.inferenced_type
        new_else_infered = node.else_body.inferenced_type

        if not equal(condition_infered, new_condition_infered):
            self.add_error(node, f"Type Error: If's condition type({new_condition_infered.name}) does not conforms to Bool type.")

        if equal(then_infered, new_then_infered) and equal(else_infered, new_else_infered):
            return
        
        joined_type = join(new_then_infered, new_else_infered)
        node.inferenced_type = joined_type

    @visitor.when(CaseNode)
    def visit(self, node, scope:Scope):
        self.visit(node.case_expr, scope)

        type_list = []
        change = False
        for option in node.options:
            child = scope.next_child()
            option_infered = option.inferenced_type.clone()
            self.visit(option, child)
            new_option_infered = option.inferenced_type
            type_list.append(new_option_infered)
            change = change or not equal(option_infered, new_option_infered)
        
        if change:
            joined_type = join_list(type_list)
            node.inferenced_type = joined_type
    
    @visitor.when(CaseOptionNode)
    def visit(self, node, scope:Scope):
        self.visit(node.expr, scope)

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        condition_infered = node.condition.inferenced_type.clone()
        self.visit(node.condition, scope)
        new_cond_infered = node.condition.inferenced_type

        if not equal(condition_infered, new_cond_infered):
            self.add_error(node, f"Type Error: Loop's condition type({new_cond_infered.name}) does not conforms to Bool type.")
        
        self.visit(node.body, scope)

    @visitor.when(LetNode)
    def visit(self, node, scope):
        child = scope.next_child()
        for var in node.var_decl_list:
            self.visit(var, child)
        self.visit(node.in_expr, child)
        node.inferenced_type = node.in_expr.inferenced_type
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope:Scope):
        if not node.expr:
            return
        
        expr_infered = node.expr.inferenced_type.clone()
        self.visit(node.expr, scope)
        new_expr_inferred = node.expr.inferenced_type

        if equal(expr_infered, new_expr_inferred):
            return
        
        node_infered = node.inferenced_type
        new_clone_infered = new_expr_inferred.clone()
        if not conforms(new_expr_inferred, node_infered):
            self.add_error(node, f"Semantic Error: Variable \'{node.id}\' expression type({new_clone_infered.name}) does not conforms to declared type({node_infered.name}).")

    @visitor.when(AssignNode)
    def visit(self, node, scope:Scope):
        if not node.defined and node.id != "self":
            return
        
        expr_infered = node.expr.inferenced_type.clone()
        self.visit(node.expr, scope)
        new_expr_infered = node.expr.inferenced_type

        if equal(expr_infered, new_expr_infered):
            return
        
        var_type = scope.find_variable(node.id).type
        new_clone_infered = new_expr_infered.clone()
        if not conforms(new_expr_infered, var_type):
            self.add_error(node, f"Type Error: Cannot assign new value to variable '{node.id}'. Expression type({new_clone_infered.name}) does not conforms to declared type ({var_type.name}).")
            var_type = ErrorType()
        
        node.inferenced_type = var_type
    
    @visitor.when(MethodCallNode)
    def visit(self, node, scope):
        caller = node.inferenced_caller
        if node.type and node.expr:
            bridge_infered = node.expr.inferenced_type.clone()
            self.visit(node.expr, scope)
            bridge = node.expr.inferenced_type
            if not equal(bridge_infered, bridge):
                bridge_clone = bridge.clone()
                if not conforms(bridge, caller):
                    self.add_error(node, f"Semantic Error: Cannot effect dispatch because expression type({bridge_clone.name}) does not conforms to caller type({caller.name}).")
                    caller = ErrorType()
        elif node.expr:
            self.visit(node.expr, scope)
            caller = node.expr.inferenced_type
        
        if len(caller.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(node.id, len(node.args))
            types = [typex for _, typex in methods_by_name]
            conforms(caller, TypeBag(set(types), types))
            if len(caller.heads) > 1:
                error = f"Semantic Error: Method \"{node.id}\" found in {len(caller.heads)} unrelated types:\n"
                error += "   -Found in: "
                error += ", ".join(typex.name for typex in caller.heads)
                self.add_error(node, error)
                caller = ErrorType()
            elif len(caller.heads) == 0:
                self.add_error(node, f"There is no method called {node.id} which takes {len(node.args)} paramters.")
                caller = ErrorType()
        
        if len(caller.heads) == 1:
            caller_type = caller.heads[0]
            method = caller_type.get_method(node.id)

            if len(node.args) != len(method.param_types):
                self.add_error(node, f"Semantic Error: Method '{node.id}' from class '{caller_type.name}' takes {len(node.args)} arguments but {method.param_types} were given.'")
                node.inferenced_type = ErrorType()
            
            decl_return_type = method.return_type.clone()
            decl_return_type.swap_self_type(caller_type)

            type_set = set()
            heads = []
            type_set = smart_add(type_set, heads, decl_return_type)
            for i in range(len(node.args)):
                arg = node.args[i]
                p_type = method.param_types[i]
                arg_infered = arg.inferenced_type.clone()
                self.visit(arg, scope)
                new_arg_infered = arg.inferenced_type
                new_clone_infered = new_arg_infered.clone()
                if not conforms(new_arg_infered, p_type):
                    self.add_error(node.arg, f"Type Error: Argument expression type ({new_clone_infered.name}) does not conforms parameter declared type({p_type.name})")
            node.inferenced_type = TypeBag(type_set, heads)
        else:
            node.inferenced_type = ErrorType()
        node.inferenced_caller = caller
    
    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        left_infered = node.left.inferenced_type#.clone()
        right_infered = node.right.inferenced_type#.clone()

        self.visit(node.left, scope)
        self.visit(node.right, scope)

        new_left = node.left.inferenced_type
        new_right = node.right.inferenced_type
        
        int_type = self.context.get_type("Int")
        if not equal(left_infered, new_left):
            left_clone = new_left.clone()
            if not conforms(left_infered, int_type):
                self.add_error(node.left, f"Type Error: Arithmetic Error: Left member type({left_clone.name}) does not conforms to Int type.")
        
        if not equal(right_infered, new_right):
            right_clone = new_left.clone()
            if not conforms(right_infered, int_type):
                self.add_error(node.right, f"Type Error: Arithmetic Error: Right member type({right_clone.name}) does not conforms to Int type.")

    @visitor.when(ComparerNode)
    def visit(self, node, scope):
        left_infered = node.left.inferenced_type#.clone()
        right_infered = node.right.inferenced_type#.clone()

        self.visit(node.left, scope)
        self.visit(node.right, scope)

        new_left = node.left.inferenced_type
        new_right = node.right.inferenced_type
        left_clone = new_left.clone()
        right_clone = new_right.clone()

        if equal(left_infered, new_left) and equal(right_infered, new_right):
            return

        if not conforms(left_clone, new_right) and not conforms(right_clone, new_left):
            self.add_error(node, f"Type Error: Left expression type({new_left.name}) does not conforms to right expression type({new_right.name})")

    @visitor.when(VariableNode)
    def visit(self, node, scope:Scope):
        if node.defined:
            node.inferenced_type = scope.find_variable(node.value).type

    @visitor.when(NotNode)
    def visit(self, node, scope):
        expr_infered = node.expr.inferenced_type#.clone()
        self.visit(node.expr, scope)
        new_expr = node.expr.inferenced_type
        expr_clone = new_expr.clone()
        bool_type = self.context.get_type("Bool")
        if equal(expr_infered, new_expr):
            return
        if not conforms(new_expr, bool_type):
            self.add_error(node.value, f"Type Error: Not's expresion type({expr_clone.name} does not conforms to Bool type")

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        expr_infered = node.expr.inferenced_type#.clone()
        self.visit(node.expr, scope)
        new_expr = node.expr.inferenced_type
        expr_clone = new_expr.clone()
        int_type = self.context.get_type("Int")
        if equal(expr_infered, new_expr):
            return
        if not conforms(new_expr, int_type):
            self.add_error(node.value, f"Type Error: Not's expresion type({expr_clone.name} does not conforms to Int type")

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
    
    def add_error(self, node:Node, text:str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line,col), f"({line}, {col}) - " + text))
    
    #todo: los .clone detras de los old_infered_types puede eliminarse, me parece q no son necesarios
    #todo: para no tener los .clone en todas las visitas en todos los casos posibles debe actualizarse el
    #todo: .inferenced_type


    #todo: Para pensar: 
    #todo: que hacer si expr_type no conforma con decl_type
    #todo: Convierto expr en error_type si se me queda vacio, si es error ahora va a ser despues
    #todo: ademas le pone ya una condicion al bolsa, en caso de que sea AUTO_TYPE
    #todo: si lo mantengo igual que puedo ganar?
    
    #todo: Es necesario agregar una propiedad Autotype a los TypeBag que indiquen quien es quien?
    
    #todo: En el caso donde Auto1 se conforma de Auto2, y Auto1, nada mas puede ser Int o Object, y el
    #todo: otro puede ser de todo, de que manera y cuando achicar Auto2.
    #todo: Una manera puede ser cuando no se hayan hecho mas cambios sobre Auto1 y Auto2

    #todo: AutoType checking for later:
    #todo: Redefined methods with params and return type are autotypes
    #todo: Check use of self types inside auto types, how does it affects, etc...
    #todo: 