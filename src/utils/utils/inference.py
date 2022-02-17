from .semantic import Attribute, Method, Type
from .semantic import Context, Scope
from .semantic import SemanticError, ErrorType
import utils.ast_nodes as ast
import utils.visitor as visitor 
from collections import deque


def add_ext(d, node1, node2):
    try:
        d[node1].append(node2)
    except KeyError:
        d[node1] = [node2]
    if node2 not in d:
        d[node2] = []


class InferenceTypeChecker:
    def __init__(self, context: Context, errors):
        self.context: Context = context
        self.current_type: Type = None
        self.current_method: Method = None
        self.errors = errors
        self.extension = {}
        self.dfunc = {
            'attr': self.update_attr,
            'var': self.update_var,
            'param': self.update_param,
            'ret': self.update_ret,
            'base': self.update_base,
            'join': self.update_join
        }
        self.dfunc_type = {
            'attr': self.get_tuple_type_attr,
            'var': self.get_tuple_type_var,
            'param': self.get_tuple_type_param,
            'ret': self.get_tuple_type_ret,
            'base': self.get_tuple_type_base,
            'join': self.get_tuple_type_join
        }

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        if scope is None:
            scope = Scope()
        for item in node.class_list:
            self.visit(item, scope.create_child())
        #print('\n'.join([str(i) for i in self.extension.items()]))
        self.update()
        ReplaceTypes(self.context, self.errors).visit(node, scope)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, scope: Scope):
        self.current_type = self.context.get_type(node.name)
        for item in node.data:
            if isinstance(item, ast.MethodDecNode):
                self.visit(item, scope.create_child())
            elif isinstance(item, ast.AttributeDecNode):
                self.visit(item, scope)

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, scope: Scope):
        var_type = self.context.get_type(node._type)
        var_attr_info = scope.define_variable(node.name, var_type)  # scope
        tuple_var = 'var', var_attr_info
        exp = self.visit(node.expr, scope.create_child()) if node.expr is not None else None
        if node._type == "AUTO_TYPE":
            attr_type = self.context.get_type(node._type)
            attr = self.current_type.attributes[node.name]
            tuple_attr = 'attr', attr
            if exp is not None:
                add_ext(self.extension, exp, tuple_var)
                add_ext(self.extension, exp, tuple_attr)
            # si conocemos el tipo de uno, sabremos el tipo del otro
            add_ext(self.extension, tuple_attr, tuple_var)
            add_ext(self.extension, tuple_var, tuple_attr)

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.name)
        scope.define_variable('self', self.current_type)#define self
        params_name = self.current_method.param_names
        params_type = self.current_method.param_types
        for i, param_name in enumerate(params_name):
            param_type = params_type[i]
            param_var_scope = scope.define_variable(param_name, param_type)
            tuple_var = 'var', param_var_scope

            if param_type.name == "AUTO_TYPE":
                tuple_param = 'param', self.current_method, i
                add_ext(self.extension, tuple_var, tuple_param)
                add_ext(self.extension, tuple_param, tuple_var)
        body_exp = self.visit(node.expr, scope)
        if self.current_method.return_type.name == "AUTO_TYPE":
            tuple_ret = 'ret', self.current_method
            add_ext(self.extension,  body_exp, tuple_ret)

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        self.visit(node.cond, scope)
        self.visit(node.data, scope.create_child())
        return ('base', self.context.get_type("Object"))

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        for dec in node.declaration:
            id_var, type_var, expr = dec
            try:
                var_info = scope.define_variable(
                    id_var, self.context.get_type(type_var))
            except SemanticError:
                var_info = scope.define_variable(id_var, ErrorType())

            tuple_var = 'var', var_info
            expr_node = self.visit(
                expr, scope.create_child()) if expr is not None else None
            if var_info.type.name == "AUTO_TYPE":
                if expr_node is not None:
                    add_ext(self.extension, expr_node, tuple_var)
                    if expr_node[1].name == "AUTO_TYPE":
                        add_ext(self.extension, tuple_var, expr_node)
                else:
                    add_ext(self.extension, tuple_var, [])
            elif expr_node is not None and expr_node == "AUTO_TYPE":
                add_ext(self.extension, expr_node, tuple_var)

        exp_body = self.visit(node.expr, scope.create_child())
        return exp_body

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        var = scope.find_variable(node.idx)
        tuple_var = 'var', var
        expr = self.visit(node.expr, scope.create_child())

        if var is not None:  # esta definida
            if expr[0]=='join':
                exp_type = self.context.get_type('AUTO_TYPE')
            else:
                exp_type = self.dfunc_type[expr[0]](expr)
            if var.type.name == "AUTO_TYPE" and  exp_type != "AUTO_TYPE":
                add_ext(self.extension, expr, tuple_var)
            elif var.type.name != "AUTO_TYPE" and exp_type== "AUTO_TYPE":
                tuple_base = 'base', var.types
                add_ext(self.extension, tuple_base, expr)
            elif var.type.name == "AUTO_TYPE" and exp_type == "AUTO_TYPE":
                add_ext(self.extension, tuple_var, expr)
                add_ext(self.extension, expr, tuple_var)
        return expr

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        if_ = self.visit(node.if_expr,scope)

        add_ext(self.extension,('base', self.context.get_type('Bool')), if_)

        then_ = self.visit(node.then_expr,scope.create_child())
        if then_[0] == 'join':
            self.extension[then_] = []

        else_ = self.visit(node.else_expr,scope.create_child())
        if else_[0] == 'join':
            self.extension[else_] = []

        tuple_join = 'join', then_, else_
        return tuple_join
        # if then_[0]=='base' and else_[0] == 'base' :
        #     return 'base',then_[1].common_ancestor(else_[1])
        #return 'base', self.context.get_type('Object')

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, scope: Scope):
        self.visit(node.expr,scope)
        for id_,type_,exp_ in node.params:
            var_info = scope.define_variable(id_,self.context.get_type(type_))
            self.visit(exp_,scope.create_child())
        return 'base', self.context.get_type('Object')

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        final_exp = None
        current_scope = scope.create_child()

        for expr in node.expr:
            final_exp = self.visit(expr, current_scope)
        return final_exp

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, scope: Scope):
        if node.atom is None:
            node.atom = ast.VariableNode('self')
        inst = self.visit(node.atom, scope)
        type_inst = self.dfunc_type[inst[0]](inst)
        if inst[0] == 'base' and node.idx in set(m.name for m, _ in type_inst.all_methods(True)):
            method = type_inst.get_method(node.idx)

            for i, exp in enumerate(node.exprlist):
                arg = self.visit(exp, scope)
                tuple_param = 'param', method, i
                param_type = method.param_types[i]
                if arg is not None:
                    if arg[0] == 'base':
                        if param_type.name == 'AUTO_TYPE':
                            add_ext(self.extension, arg, tuple_param)
                    else:
                        if method.param_types[i].name != 'AUTO_TYPE':
                            add_ext(self.extension, tuple_param, arg)
                        else:
                            add_ext(self.extension, arg, tuple_param)
                            add_ext(self.extension, tuple_param, arg)
            if method.return_type.name == 'AUTO_TYPE':
                return 'ret', method
            ret_type = method.return_type if method.return_type != 'SELF_TYPE' else type_inst
            return 'base', ret_type

        for arg in node.exprlist:
            self.visit(arg, scope)
        return 'base', self.context.get_type('Object')

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        return self.visit_op_int(node, scope)

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        return self.visit_op_int(node, scope)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        int_type = self.context.get_type('Int')
        return self.visit_op_int(node, scope)

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode, scope: Scope):
        int_type = self.context.get_type('Int')
        return self.visit_op_int(node, scope)

    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode, scope: Scope):
        int_type = self.context.get_type('Int')
        bool_type = self.context.get_type('Bool')
        return self.visit_op_bool(node, scope)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        return self.visit_op_bool(node, scope)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        return 'base', self.context.get_type('Bool')

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        return 'base', self.context.get_type('String')

    @visitor.when(ast.NumberNode)
    def visit(self, node: ast.NumberNode, scope: Scope):
        return 'base', self.context.get_type('Int')

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        return 'base', self.context.get_type('Bool')

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, scope: Scope):
        var_info = scope.find_variable(node.lex)
        if var_info is not None:
            if var_info.type.name == 'AUTO_TYPE':
                return 'var', var_info
            else:
                return 'base', var_info.type

    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, scope: Scope):
        self.visit(node.expr, scope)
        return 'base', self.context.get_type('Int')

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, scope: Scope):
        self.visit(node.expr, scope)
        return 'base', self.context.get_type('Bool')

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, scope: Scope):
        self.visit(node.expr, scope)
        return 'base', self.context.get_type('Bool')

    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, scope: Scope):
        if node.type in self.context.types:
            return 'base', self.context.get_type(node.type)
        return 'base', self.context.get_type('Object')

    def visit_op_int(self, node: ast.BinaryNode, scope: Scope):
        left_op = self.visit(node.left, scope)
        right_op = self.visit(node.right, scope)

        if left_op[0] != 'base':
            add_ext(self.extension, ('base', self.context.get_type('Int')), left_op)

        if right_op[0] != 'base':
            add_ext(self.extension, ('base', self.context.get_type('Int')), right_op)
            
        return 'base', self.context.get_type('Int')

    def visit_op_bool(self, node: ast.BinaryNode, scope: Scope):
        left_op = self.visit(node.left, scope)
        right_op = self.visit(node.right, scope)

        if left_op[0] != 'base':
            add_ext(self.extension, ('base', self.context.get_type('Int')), left_op)

        if right_op[0] != 'base':
            add_ext(self.extension, ('base', self.context.get_type('Int')), right_op)
        
        return 'base', self.context.get_type('Bool')

    def update(self):
        q = deque(e for e in self.extension if e[0] == 'base')
        visited_base = set()
        while len(q) > 0:
            base = q.popleft()
            if base in visited_base:
                continue
            self.update_visit(base, visited_base)

        q = deque(j for j in self.extension if j[0] == 'join')
        visited_join  = set()
        while len(q) > 0:
            join = q.popleft()
            if join in visited_join:
                continue
            self.update_visit_join(join,visited_join)
            
        for t in self.extension:
            if t not in visited_base and t not in visited_join:
                self.dfunc[t[0]](t, self.context.get_type('Object'))

    def update_visit(self, base, visited):
        new_type = self.dfunc_type[base[0]](base)
        q = deque([base])
        while q:
            current = q.popleft()
            if current not in visited:
                visited.add(current)
                self.dfunc[current[0]](current, new_type)
                q.extend(self.extension[current])

    def update_visit_join(self,join,visited):
        then_type = join[1][1].type if join[1][0] == 'var' else join[1][1]
        else_type = join[2][1].type if join[2][0] == 'var' else join[2][1]
        if join[1][0] == 'join':
            then_type = self.update_visit_join(join[1],visited)
            visited.add(join[1])
        if join[2][0] == 'join':
            else_type = self.update_visit_join(join[2], visited)
            visited.add(join[2])
        join_type = then_type.common_ancestor(else_type)
        q = deque([join])
        while q:
            current = q.popleft()
            if current not in visited:
                visited.add(current)
                self.dfunc[current[0]](current,join_type)
                q.extend(self.extension[current])
        return join_type

    def update_attr(self, t, new_type):
        t[1].type = new_type

    def get_tuple_type_attr(self, t):
        return t[1].type

    def update_var(self, t, new_type):
        t[1].type = new_type

    def get_tuple_type_var(self, t):
        return t[1].type

    def update_param(self, t, new_type):
        method = t[1]
        i_param = t[2]
        method.param_types[i_param] = new_type
    
    def update_join(self,t,new_type):
        pass

    def get_tuple_type_join(self, t):
        pass

    def get_tuple_type_param(self, t):
        return t[1].params_type[t[2]]

    def update_ret(self, t, new_type):
        method = t[1]
        method.return_type = new_type

    def get_tuple_type_ret(self, t):
        return t[1].return_type

    def update_base(self, t, new_type):
        pass

    def get_tuple_type_base(self, t):
        return t[1]


class ReplaceTypes:
    def __init__(self, context: Context, errors):
        self.context: Context = context
        self.current_type: Type = None
        self.current_method: Method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        for i, c in enumerate(node.class_list):
            self.visit(c, scope.children[i])
        return scope

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, scope: Scope):
        self.current_type = self.context.get_type(node.name)
        i_attr = 0
        i_method = 0
        for item in node.data:
            if isinstance(item, ast.MethodDecNode):
                self.visit(item, scope.children[i_attr])
                i_attr += 1
            elif isinstance(item, ast.AttributeDecNode):
                if item.expr is not None:
                    item.index = i_attr
                    i_attr += 1
                self.visit(item, scope)

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, scope: Scope):
        attr_type = self.context.get_type(node._type)
        attr_info = scope.find_variable(node.name)
        if node.expr is not None:
            self.visit(node.expr, scope.children[node.index])
        if attr_type.name == "AUTO_TYPE":
            if attr_info.type.name == "AUTO_TYPE":
                node._type = 'Object'
                # self.errors.append('InferenceError:No se pudo inferir el tipo')
            else:
                node._type = attr_info.type.name

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.name)
        for i, param in enumerate(node.params):
            var_info = scope.find_variable(param.name)
            if var_info is not None:
                if var_info.type.name == "AUTO_TYPE":
                    node.type = 'Object'
                    #self.errors.append('InferenceError:No se pudo inferir el tipo')
                else:
                    node.params[i] = ast.ParamNode(param.name, var_info.type.name)
        self.visit(node.expr, scope)

        if node.type == "AUTO_TYPE":
            if self.current_method.return_type.name == "AUTO_TYPE":
                node.type = 'Object'
                #self.errors.append('InferenceError:No se pudo inferir el tipo')
            else:
                node.type = self.current_method.return_type.name

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        self.visit(node.cond, scope)
        self.visit(node.data, scope.children[0])

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        i_child = 0
        for i, dec in enumerate(node.declaration):
            id_var, type_var, expr = dec
            var_info = scope.find_variable(id_var)
            if expr is not None:
                self.visit(expr, scope.children[i_child])
                i_child += 1
            if type_var == "AUTO_TYPE":
                if var_info.type.name == "AUTO_TYPE":
                    node.declaration[i] = (id_var, 'Object', expr)
                    # self.errors.append('InferenceError:No se pudo inferir el tipo')
                node.declaration[i] = (id_var, var_info.type.name, expr)
        self.visit(node.expr, scope.children[i_child])

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        self.visit(node.expr, scope.children[0])

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, scope: Scope):
        self.visit(node.atom, scope)
        for expr in node.exprlist:
            self.visit(expr, scope)

    @visitor.when(ast.BinaryNode)
    def visit(self, node: ast.BinaryNode, scope: Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)

    @visitor.when(ast.UnaryNode)
    def visit(self, node: ast.UnaryNode, scope: Scope):
        self.visit(node.expr, scope)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        current_scope = scope.children[0]
        for expr in node.expr:
            self.visit(expr, current_scope)

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        self.visit(node.if_expr,scope)
        self.visit(node.then_expr,scope.children[0])
        self.visit(node.else_expr,scope.children[1])

        
