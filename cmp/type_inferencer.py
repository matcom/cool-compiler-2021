import cmp.visitor as visitor
from cmp.semantic import SemanticError, ErrorType, SelfType, AutoType, LCA
from cmp.ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from cmp.ast import AssignNode, CallNode, CaseNode, BlockNode, LoopNode, ConditionalNode, LetNode
from cmp.ast import ArithmeticNode, ComparisonNode, EqualNode
from cmp.ast import VoidNode, NotNode, NegNode
from cmp.ast import ConstantNumNode, ConstantStringNode, ConstantBoolNode, VariableNode, InstantiateNode


TYPE_CONFORMANCE = 'Type "%s" can not conform to type "%s"'
AUTOTYPE_ERROR = 'Incorrect use of AUTO_TYPE'

class TypeInferencer:
    def __init__(self, context, manager, errors=[]):
        self.context = context
        self.errors = errors
        self.manager = manager
        
        self.current_type = None
        self.current_method = None
        self.scope_children_id = 0

        # built-in types
        self.obj_type = self.context.get_type('Object')
        self.int_type = self.context.get_type('Int')
        self.bool_type = self.context.get_type('Bool')
        self.string_type = self.context.get_type('String')

    @visitor.on('node')
    def visit(self, node, scope, types=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope, types=None):
        if types is None:
            types = []

        change = self.manager.count > 0
        while change:
            change = False

            for declaration, child_scope in zip(node.declarations, scope.children):
                self.scope_children_id = 0
                self.visit(declaration, child_scope, types)

            change = self.manager.infer_all()

        self.manager.infer_object(self.obj_type)
        for declaration, child_scope in zip(node.declarations, scope.children):
                self.scope_children_id = 0
                self.visit(declaration, child_scope, types)
            
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, types):
        self.current_type = self.context.get_type(node.id)
            
        for feature, child_scope in zip(node.features, scope.children):
            self.scope_children_id = 0
            self.visit(feature, child_scope, types)
     
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope, types):
        var_attr = scope.find_variable(node.id)
        attr_type = var_attr.type
        idx = var_attr.idx
        
        if isinstance(attr_type, AutoType):
            inf_type =  self.manager.infered_type[idx]
            if inf_type is not None:
                if isinstance(inf_type, ErrorType):
                    self.errors.append(AUTOTYPE_ERROR)
                else:
                    node.type = inf_type.name
                    self.current_type.update_attr(node.id, inf_type)
                scope.update_variable(node.id, inf_type)
                attr_type = inf_type

        conforms_to_types = []
        if isinstance(attr_type, AutoType):
            conforms_to_types.extend(self.manager.conforms_to[idx])
        else:
            conforms_to_types.append(attr_type)

        if node.expr is not None:
            _, computed_types = self.visit(node.expr, scope, conforms_to_types)
            if isinstance(attr_type, AutoType):
                self.manager.upd_conformed_by(node.idx, computed_types)
            
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope, types):
        self.current_method = self.current_type.get_method(node.id)

        method_params = []
        for i, t in enumerate(self.current_method.param_types):
            idx = self.current_method.param_idx[i]
            name = self.current_method.param_names[i]
            if isinstance(t, AutoType):
                inf_type =  self.manager.infered_type[idx]
                if inf_type is not None:
                    if isinstance(inf_type, ErrorType):
                        self.errors.append(AUTOTYPE_ERROR)
                    else:
                        node.params[i] = (node.params[i][0], inf_type.name)
                        self.current_type.update_method_param(name, inf_type, i)
                    scope.update_variable(name, inf_type)
                    t = inf_type
            method_params.append(t)

        rtype = self.current_method.return_type
        idx = self.current_method.ridx
        if isinstance(rtype, AutoType):
            inf_type =  self.manager.infered_type[idx]
            if inf_type is not None:
                if isinstance(inf_type, ErrorType):
                    self.errors.append(AUTOTYPE_ERROR)
                else:
                    node.type = inf_type.name
                    self.current_type.update_method_rtype(self.current_method.name, inf_type)
                rtype = inf_type

        # checking overwriting
        try:
            method = self.current_type.parent.get_method(node.id)    
        
            for i, t in enumerate(method_params):
                if not isinstance(method.param_types[i], AutoType) and isinstance(t, AutoType):
                    self.manager.auto_to_type(self.current_method.param_idx[i], method.param_types[i])
                    self.manager.type_to_auto(self.current_method.param_idx[i], method.param_types[i])

            if isinstance(rtype, AutoType) and not isinstance(method.return_type, AutoType):
                self.manager.auto_to_type(idx, method.return_type)
                self.manager.type_to_auto(idx, method.return_type)
        except SemanticError:
            pass
        
        # checking return type in computed types of the expression
        conforms_to_types = []
        if isinstance(rtype, AutoType):
            conforms_to_types.extend(self.manager.conforms_to[idx])
        else:
            conforms_to_types.append(rtype)
        _, computed_types = self.visit(node.body, scope, conforms_to_types)
        if isinstance(rtype, AutoType):
            self.manager.upd_conformed_by(self.current_method.ridx, computed_types)
              
    @visitor.when(AssignNode)
    def visit(self, node, scope, types):
        var = scope.find_variable(node.id)
        # obtaining defined variable
        if isinstance(var.type, AutoType):
            inf_type =  self.manager.infered_type[var.idx]
            if inf_type is not None:    
                scope.update_variable(var.name, inf_type)
                var.type = inf_type
        
        conforms_to_types = []
        if isinstance(var.type, AutoType):
            conforms_to_types.extend(self.manager.conforms_to[var.idx])
        else:
            conforms_to_types.append(var.type)
        conforms_to_types.extend(types)

        scope_index = self.scope_children_id
        self.scope_children_id = 0
        
        typex, computed_types = self.visit(node.expr, scope.children[scope_index], conforms_to_types)
        if isinstance(var.type, AutoType):
            self.manager.upd_conformed_by(var.idx, computed_types)

        self.scope_children_id = scope_index + 1
        return typex, computed_types
        
    @visitor.when(CallNode)
    def visit(self, node, scope, types):
        # Check cast type
        cast_type = None
        if node.type is not None:
            try:
                cast_type = self.context.get_type(node.type)
                if isinstance(cast_type, AutoType):
                    cast_type = None
                elif isinstance(cast_type, SelfType):
                    cast_type = SelfType(self.current_type)
            except SemanticError:
                pass
 
        conforms_to_types = [] if cast_type is None else [cast_type]
        # Check object
        obj_type, computed_types = self.visit(node.obj, scope, conforms_to_types)

        if cast_type is None:
            cast_type = obj_type

        # if the obj that is calling the function is autotype, let it pass
        if isinstance(cast_type, AutoType):
            return cast_type, []
        
        # Check this function is defined for cast_type
        try:
            method = cast_type.get_method(node.id)
            if not len(node.args) == len(method.param_types):
                return ErrorType(), []
            for i, arg in enumerate(node.args):
                arg_type = method.param_types[i]
                if isinstance(arg_type, AutoType):
                    inf_type =  self.manager.infered_type[method.param_idx[i]]
                    if inf_type is not None:
                        arg_type = inf_type

                conforms_to_types = []
                if isinstance(arg_type, AutoType):
                    conforms_to_types.extend(self.manager.conforms_to[method.param_idx[i]])
                else:
                    conforms_to_types.append(arg_type)
                _, computed_types = self.visit(arg, scope, conforms_to_types)
                if isinstance(arg_type, AutoType):
                    self.manager.upd_conformed_by(method.param_idx[i], computed_types)
            
            # check return_type
            computed_types = []
            rtype = method.return_type
            if isinstance(rtype, SelfType):
                rtype = obj_type
            
            if isinstance(rtype, AutoType):
                self.manager.upd_conforms_to(method.ridx, types)
                computed_types.extend(self.manager.conformed_by[method.ridx])
            else:
                computed_types.append(rtype)

            return rtype, computed_types

        except SemanticError:
            return ErrorType(), []
        
    @visitor.when(CaseNode)
    def visit(self, node, scope, types):
        # check expression
        self.visit(node.expr, scope, set())

        scope_index = self.scope_children_id
        nscope = scope.children[scope_index]

        # check branches
        expr_types = []
        for i, (branch, child_scope) in enumerate(zip(node.branch_list, nscope.children)):
            branch_name, branch_type, expr =  branch
            if isinstance(branch_type, AutoType):
                inf_type =  self.manager.infered_type[node.branch_idx[i]]
                if inf_type is not None:
                    if isinstance(inf_type, ErrorType):
                        self.errors.append(AUTOTYPE_ERROR)
                    else:
                        node.branch_list[i][1] = inf_type.name
                    scope.update_variable(branch_name, inf_type)

            self.scope_children_id = 0

            _, computed_types = self.visit(expr, child_scope, types)
            expr_types.extend(computed_types)

        self.scope_children_id = scope_index + 1
        return LCA(expr_types), expr_types
    
    @visitor.when(BlockNode)
    def visit(self, node, scope, types):
        scope_index = self.scope_children_id
        nscope = scope.children[scope_index]
        self.scope_children_id = 0

        # Check expressions but last one
        sz = len(node.expr_list) - 1
        for expr in node.expr_list[:sz]:
            self.visit(expr, nscope, [])

        # Check last expression
        typex, computed_types = self.visit(node.expr_list[-1], nscope, types)

        # return the type of the last expression of the list
        self.scope_children_id = scope_index
        return typex, computed_types

    @visitor.when(LoopNode)
    def visit(self, node, scope, types):
        scope_index = self.scope_children_id
        nscope = scope.children[scope_index]
        self.scope_children_id = 0

        # checking condition: it must conform to bool
        self.visit(node.condition, nscope, [self.bool_type])

        # checking body
        self.visit(node.body, nscope, [])

        self.scope_children_id = scope_index
        return self.obj_type, [self.obj_type]

    @visitor.when(ConditionalNode)
    def visit(self, node, scope, types):
        # check condition conforms to bool
        self.visit(node.condition, scope, [self.bool_type])
        
        branch_types = []

        scope_index = self.scope_children_id
        self.scope_children_id = 0
        _, then_types = self.visit(node.then_body, scope.children[scope_index], types)
        scope_index += 1
        self.scope_children_id = 0
        _, else_types = self.visit(node.else_body, scope.children[scope_index], types)

        branch_types.extend(then_types)
        branch_types.extend(else_types)

        self.scope_children_id = scope_index + 1
        return LCA(branch_types), branch_types

    @visitor.when(LetNode)
    def visit(self, node, scope, types):
        scope_index = self.scope_children_id
        nscope = scope.children[scope_index]
        self.scope_children_id = 0

        for i, item in enumerate(node.id_list):
            temp_scope_index = self.scope_children_id
            new_scope = nscope.children[temp_scope_index]
            self.scope_children_id = 0

            var_name, _, expr = item               
            var = new_scope.find_variable(var_name)

            if isinstance(var.type, AutoType):
                inf_type =  self.manager.infered_type[node.idx_list[i]]
                if inf_type is not None:
                    if isinstance(inf_type, ErrorType):
                        self.errors.append(AUTOTYPE_ERROR)
                    else:
                        node.id_list[i] = (var_name, inf_type.name, expr)
                    new_scope.update_variable(var_name, inf_type)
                    var.type = inf_type
            
            conforms_to_types = []
            if isinstance(var.type, AutoType):
                conforms_to_types.extend(self.manager.conforms_to[node.idx_list[i]])
            else:
                conforms_to_types.append(var.type)
            
            if expr is not None:
                _, computed_types = self.visit(expr, new_scope, conforms_to_types)
                if isinstance(var.type, AutoType):
                    self.manager.upd_conformed_by(node.idx_list[i], computed_types)

            nscope = new_scope

        expr_type, computed_types = self.visit(node.body, nscope, types)
        self.scope_children_id = scope_index + 1
        return expr_type, computed_types

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope, types):
        self.check_expr(node, scope)

        # Check int type conforms to all the types in types
        self.check_conformance(types, self.int_type)

        return self.int_type, [self.int_type]

    @visitor.when(ComparisonNode)
    def visit(self, node, scope, types):
        self.check_expr(node, scope)

        # Check bool type conforms to all the types in types
        self.check_conformance(types, self.bool_type)

        return self.bool_type, [self.bool_type]

    @visitor.when(EqualNode)
    def visit(self, node, scope, types):
        left, _ = self.visit(node.left, scope, [])
        right, _ = self.visit(node.right, scope, [])

        fixed_types = [self.int_type, self.bool_type, self.string_type]
        def check_equal(typex):
            if not isinstance(typex, AutoType) and not isinstance(typex, ErrorType):
                for t in fixed_types:
                    if typex.conforms_to(t):
                        return True
            return False

        if check_equal(left):
            self.visit(node.right, scope, [left])
        elif check_equal(right):
            self.visit(node.left, scope, [right])
        
        self.check_conformance(types, self.bool_type)
        
        return self.bool_type, [self.bool_type]

    @visitor.when(VoidNode)
    def visit(self, node, scope, types):
        self.visit(node.expr, scope, [])
        self.check_conformance(types, self.bool_type)

        return self.bool_type, [self.bool_type]

    @visitor.when(NotNode)
    def visit(self, node, scope, types):
        self.visit(node.expr, scope, [self.bool_type])
        self.check_conformance(types, self.bool_type)
        
        return self.bool_type, [self.bool_type]

    @visitor.when(NegNode)
    def visit(self, node, scope, types):
        self.visit(node.expr, scope, [self.int_type])
        self.check_conformance(types, self.int_type)
        
        return self.int_type, [self.int_type]

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope, types):
        self.check_conformance(types, self.int_type)
        return self.int_type, [self.int_type]

    @visitor.when(ConstantBoolNode)
    def visit(self, node, scope, types):
        self.check_conformance(types, self.bool_type)
        return self.bool_type, [self.bool_type]

    @visitor.when(ConstantStringNode)
    def visit(self, node, scope, types):
        self.check_conformance(types, self.string_type)
        return self.string_type, [self.string_type]

    @visitor.when(VariableNode)
    def visit(self, node, scope, types):
        var = scope.find_variable(node.lex)
        if isinstance(var.type, AutoType):
            inf_type =  self.manager.infered_type[var.idx]
            if inf_type is not None:  
                scope.update_variable(var.name, inf_type)
                var.type = inf_type
        
        conformed_by = []
        if isinstance(var.type, AutoType):
            self.manager.upd_conforms_to(var.idx, types)
            conformed_by.extend(self.manager.conformed_by[var.idx])
        else:
            self.check_conformance(types, var.type)
            conformed_by.append(var.type)

        return var.type, conformed_by
 
    @visitor.when(InstantiateNode)
    def visit(self, node, scope, types):
        try:
            typex = self.context.get_type(node.lex)
            if isinstance(typex, SelfType):
                typex = SelfType(self.current_type)
        except SemanticError:
            typex = ErrorType()

        self.check_conformance(types, typex)
        
        return typex, [typex]


    
    def check_expr(self, node, scope):
        self.visit(node.left, scope, [self.int_type])
        self.visit(node.right, scope, [self.int_type])

    def check_conformance(self, types, typex):
        for item in types:
            if not typex.conforms_to(item):
                self.errors.append(TYPE_CONFORMANCE %(typex.name, item.name))
