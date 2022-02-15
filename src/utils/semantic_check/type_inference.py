import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError, ErrorType, Scope, VariableInfo

INFERENCE_ATTR_ERROR = 'Cannot infer type for attribute "%s" in class "%s".'
INFERENCE_METH_ERROR = 'Cannot infer return type for method "%s" in class "%s".'
INFERENCE_PARAMETER_ERROR = 'Cannot infer type for parameter "%s" of method "%s" in class "%s".'
INFERENCE_VARIABLE_ERROR = 'Cannot infer type for variable "%s" of method "%s" in class "%s".'

class TypeInference:
    def __init__(self, context, errors = []):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.update = True

    
    @visitor.on('node')
    def visit(self, node, scope):
        pass


    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope=None):
        for i,dec in enumerate(node.declarations):
            self.visit(dec, scope.children[i])
        
        return scope


    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)

        attrs = [feat for feat in node.features if isinstance(feat, nodes.AttrDeclarationNode)]
        i = 0
        for attr in attrs:
            if attr.expr is not None:
                attr.index = i
                i += 1
            self.visit(attr, scope)
        
        meths = [feat for feat in node.features if isinstance(feat, nodes.MethDeclarationNode)]
        for meth in meths:
            self.visit(meth, scope.children[i])
            i+=1

        for attr in attrs:
            var = scope.find_variable(attr.id)
            if var.type.name == 'AUTO_TYPE':
                var.update_type()
                if var.type.name == 'AUTO_TYPE':
                    self.errors.append(INFERENCE_ATTR_ERROR % (attr.id, self.current_type.name))
                else:
                    self.update = True
                    self.current_type.get_attribute(attr.id).type = var.type
                    attr.type = var.type.name
                    
        return


    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self, node, scope):

        if node.expr is not None:
            attr = self.current_type.get_attribute(node.id)
            var = scope.find_variable(node.id)

            type_expr = self.visit(node.expr, scope.children[node.index], attr.type)
            
            # se infiere el tipo a partir de su expresion de inicializacion
            if type_expr.name != 'AUTO_TYPE':
                var.expected_types.append(type_expr)
        return
        
    @visitor.when(nodes.MethDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        
        return_type = self.current_method.return_type

        # el tipo del body se espera que sea el tipo de return type
        body_type = self.visit(node.body, scope, self.current_type if return_type.name == 'SELF_TYPE' else return_type if return_type.name != 'AUTO_TYPE' else None)

        for i, (name, typex) in enumerate(node.params):
            var = scope.find_variable(name)
            var.expected_types = var.expected_types + self.current_method.expected_param_types[name] if name in self.current_method.expected_param_types else var.expected_types

            if var.type.name == 'AUTO_TYPE':
                var.update_type()
                if var.type.name == 'AUTO_TYPE':
                    self.errors.append(INFERENCE_PARAMETER_ERROR % (self.current_method.param_names[i], self.current_method.name, self.current_type.name))
                else:
                    self.update = True
                    self.current_method.param_types[i] = var.type
                    node.params[i][1] = var.type.name
        
        var = VariableInfo(self.current_method.name, return_type)

        # se infiere el tipo de retorno a partir del tipo del cuerpo del metodo
        if body_type.name != 'AUTO_TYPE':
            var.expected_types.append(body_type)

        var.expected_types = var.expected_types + [self.current_method.expected_return_type] if self.current_method.expected_return_type else var.expected_types

        if var.type.name == 'AUTO_TYPE':
                var.update_type()
                if var.type.name == 'AUTO_TYPE':
                    self.errors.append(INFERENCE_METH_ERROR % (self.current_method.name, self.current_type.name))
                else:
                    self.update = True
                    self.current_method.return_type = var.type
                    node.type = var.type.name

        self.current_method.expected_param_types = {}
        self.current_method.expected_return_type = None
        return


    @visitor.when(nodes.AssignNode)
    def visit(self, node, scope, expected_type = None):
        var = scope.find_variable(node.id) if scope.is_defined(node.id) else None

        # el tipo de la expresion se inifere a partir del tipo esperado de la asignacion
        type_expr = self.visit(node.expr, scope.children[0], var.type if var and var.type.name != 'AUTO_TYPE' else expected_type)

        # se infiere el tipo de la variable a partir de la expresion de asignacion
        if type_expr.name != 'AUTO_TYPE':
            var.expected_types.append(type_expr)

        return type_expr


    @visitor.when(nodes.CallNode)
    def visit(self, node, scope, expected_type = None):
        typex = None
        if node.type is not None:
            try:
                typex = self.context.get_type(node.type)
            except SemanticError:
                typex = ErrorType()
            else:
                if typex.name == 'SELF_TYPE' or typex.name == 'AUTO_TYPE':
                    typex = ErrorType()
            
        if node.obj is None:
            type_obj = self.current_type
        else:
            type_obj = self.visit(node.obj, scope, typex)
        
        type_obj = type_obj if not typex else typex

        try:
            meth = type_obj.get_method(node.id)
        except SemanticError:
            for arg in node.args:
                self.visit(node.args, scope)
            return ErrorType()
        
        for i, arg in enumerate(node.args):
            type_arg = self.visit(arg, scope, meth.param_types[i] if i < len(meth.param_types) and meth.param_types[i].name != 'AUTO_TYPE' else None)

            # el tipo esperado de los parametros se infiere a partir del tipo de los argumentos
            if i < len(meth.param_types) and type_arg.name != 'AUTO_TYPE':
                try:
                    meth.expected_param_types[meth.param_names[i]].append(type_arg)
                except KeyError:
                    meth.expected_param_types[meth.param_names[i]] = [type_arg]

        # el tipo de retorno del metodo llamado se infiere a partir del tipo esperado del llamado
        meth.expected_return_type = expected_type if expected_type and expected_type.name != 'AUTO_TYPE' else meth.expected_return_type
        
        return meth.return_type if meth.return_type.name != 'SELF_TYPE' else type_obj 


    @visitor.when(nodes.IfThenElseNode)
    def visit(self, node, scope, expected_type = None):  
        # se espera que el tipo de la expresion if sea Bool
        if_type = self.visit(node.if_expr, scope.children[0], self.context.get_type('Bool'))

        then_type = self.visit(node.then_expr, scope.children[1])
        else_type = self.visit(node.else_expr, scope.children[2])

        return then_type.join(else_type)


    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope, expected_type = None):

        # la condicion del while debe ser de tipo Bool
        self.visit(node.conditional_expr, scope, self.context.get_type('Bool'))

        self.visit(node.loop_expr, scope.children[0])

        return self.context.get_type('Object')


    @visitor.when(nodes.BlockNode)
    def visit(self, node, scope, expected_type = None):
        type_expr = ErrorType()
        for i, expr in enumerate(node.expr_list):
            # el tipo de la expresion se inifiere a partir de expected_type
            type_expr = self.visit(expr, scope.children[i]) if i != len(node.expr_list) - 1 else self.visit(expr, scope.children[i], expected_type)
        
        return type_expr


    @visitor.when(nodes.LetNode)
    def visit(self, node, scope, expected_type = None):
        # se inifiere l tipo a partir de expected_type
        body_type = self.visit(node.in_expr, scope.children[-1], expected_type)

        child_scope_index = 0
        for i, (idx, typex, id_expr) in enumerate(node.identifiers):
            if id_expr:
                var = scope.find_variable(idx)
                id_expr_type = self.visit(id_expr, scope.children[child_scope_index], var.type if var.type.name != 'AUTO_TYPE' else None)
                child_scope_index += 1

                # se inifere el tipo de un identificador a partir de su expresion de inicializacion
                if id_expr_type.name != 'AUTO_TYPE':
                    var.expected_types.append(id_expr_type)

        
        for i, (idx, typex, id_expr) in enumerate(node.identifiers):
            var = scope.find_variable(idx)
            if var.type.name == 'AUTO_TYPE':
                var.update_type()
                if var.type.name == 'AUTO_TYPE':
                    self.errors.append(INFERENCE_VARIABLE_ERROR % (var.name, self.current_method.name, self.current_type.name))
                else:
                    self.update = True
                    node.identifiers[i] = (idx, var.type.name, id_expr)


        return body_type


    @visitor.when(nodes.CaseNode)
    def visit(self, node, scope, expected_type = None):
        case_type = None

        for i, (idx, typex, expr) in enumerate(node.branches):
            type_expr = self.visit(expr, scope.children[i])
            
            case_type = case_type.join(type_expr) if case_type else type_expr

        return case_type


    @visitor.when(nodes.NotNode)
    def visit(self, node, scope, expected_type = None):
        # se el tipo de la expresion de not se infiere que sea Bool
        self.visit(node.expr, scope, self.context.get_type('Bool'))

        return self.context.get_type('Bool')


    @visitor.when(nodes.ConstantNumNode)
    def visit(self, node, scope, expected_type = None):
        return self.context.get_type('Int')


    @visitor.when(nodes.ConstantBoolNode)
    def visit(self, node, scope, expected_type = None):
        return self.context.get_type('Bool')


    @visitor.when(nodes.ConstantStringNode)
    def visit(self, node, scope, expected_type = None):
        return self.context.get_type('String')


    @visitor.when(nodes.VariableNode)
    def visit(self, node, scope, expected_type = None):
        var = scope.find_variable(node.lex)
        
        if var is not None:
            # el tipo esperado de var es expected_type
            if expected_type and expected_type != 'AUTO_TYPE':
                var.expected_types.append(expected_type)
            return var.type

        return ErrorType()


    @visitor.when(nodes.InstantiateNode)
    def visit(self, node, scope, expected_type = None):
        if node.lex in self.context.types:
            return self.context.get_type(node.lex)
        
        return ErrorType()


    @visitor.when(nodes.IsVoidNode)
    def visit(self, node, scope, expected_type = None):
        self.visit(node.lex, scope)

        return self.context.get_type('Bool')


    @visitor.when(nodes.ComplementNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expression se espera que sea Int
        self.visit(node.lex, scope, self.context.get_type('Int'))

        return self.context.get_type('Int')


    @visitor.when(nodes.PlusNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Int')


    @visitor.when(nodes.MinusNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Int')


    @visitor.when(nodes.StarNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Int')


    @visitor.when(nodes.DivNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Int')


    @visitor.when(nodes.LessThanNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Bool')


    @visitor.when(nodes.LessEqualNode)
    def visit(self, node, scope, expected_type = None):
        # el tipo de la expresiones se espera que sea Int
        self.visit(node.left, scope, self.context.get_type('Int'))
        self.visit(node.right, scope, self.context.get_type('Int'))

        return self.context.get_type('Bool')



    @visitor.when(nodes.EqualNode)
    def visit(self, node, scope, expected_type = None):
        type_left = self.visit(node.left, scope)
        # se infiere el tipo a la derecha del igual a partir del tipo izquierdo
        type_right = self.visit(node.right, scope, type_left if type_left.name != 'AUTO_TYPE' else None)

        if type_left.name == 'AUTO_TYPE':
            # se inifiere el tipo a la izquierda del igual a partir de su tipo derecho
            self.visit(node.left, scope, type_right if type_right.name != 'AUTO_TYPE' else None)

        return self.context.get_type('Bool')