from .semantic import SemanticError
from .semantic import Type
from .semantic import VoidType, ErrorType
from .semantic import Context, Scope 
from utils import ast_nodes as ast
from utils import visitor

class TypeCollector(object):
    def __init__(self, context: Context, errors):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        self_type = self.context.create_type('SELF_TYPE')
        object_type = self.context.create_type('Object')
        int_type = self.context.create_type('Int')
        bool_type = self.context.create_type('Bool')
        str_type = self.context.create_type('String')
        io_type = self.context.create_type('IO')
        self.context.create_type('AUTO_TYPE')
        # setting parent
        io_type.set_parent(object_type)
        str_type.set_parent(object_type)
        int_type.set_parent(object_type)
        bool_type.set_parent(object_type)
        # defining methods
        object_type.define_method('abort', [], [], object_type)
        object_type.define_method('get_type', [], [], str_type)
        object_type.define_method('copy', [], [], object_type)
        str_type.define_method('length', [], [], int_type)
        str_type.define_method('concat', ['str'], [str_type], str_type)
        str_type.define_method('substr', ['pos', 'len'], [int_type, int_type], str_type)
        io_type.define_method('out_string', ['i'], [str_type], io_type)
        io_type.define_method('out_int', ['i'], [int_type], io_type)
        io_type.define_method('in_string', [], [], str_type)
        io_type.define_method('in_int', [], [], int_type)

        for item in node.class_list:
            self.visit(item)
 
    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode):
        try:
            self.context.create_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)


class TypeBuilder:
    def __init__(self, context: Context, errors):
        self.context: Context = context
        self.current_type: Type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        for item in node.class_list:
            self.visit(item)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode):
        self.current_type = self.context.get_type(node.name)
       
        if node.parent is not None:
            if node.parent in ['Int', 'Bool', 'String', 'SELF_TYPE']:
                self.errors.append('La clase \'{node.name}\' no puede heredar de \'{node.parent}\'')
            try:
                self.current_type.set_parent(self.context.get_type(node.parent))
            except SemanticError as e:
                self.errors.append(e.text)
                
        else:
            obj = self.context.get_type('Object')
            self.current_type.set_parent(obj)
        
        for item in node.data:
            self.visit(item)

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode):
        params_name = []
        params_type = []
        for param in node.params:
            name = param.name
            type_ = param.type
            params_name.append(name)
            
            try:
                t = self.context.get_type(type_)
                params_type.append(t)
            except SemanticError as e:
                self.errors.append(e.text)
                params_type.append(ErrorType())
        try:
            result_type = self.context.get_type(node.type)
        except SemanticError as e:
            result_type = ErrorType()
            self.errors.append(e.text)
        self.current_type.define_method(node.name, params_name, params_type, result_type)


    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode):
        try:
            type_ = self.context.get_type(node._type)
            self.current_type.define_attribute(node.name, type_)
        except SemanticError as e:
            self.errors.append(e.text)
            self.current_type.define_attribute(node.name, ErrorType())


class TypeChecker:
    def __init__(self, context: Context, errors):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        if scope is None:
            scope = Scope()
        for item in node.class_list:
            self.visit(item, scope.create_child())

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, scope: Scope):
        try:
            self.current_type = self.context.get_type(node.name)
        except SemanticError as e:
            self.errors.append(e.text)
        for item in node.data:
            self.visit(item, scope.create_child())
    
    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, scope: Scope):
        if node.name == 'self':
            self.errors.append('El nombre del atributo no puede ser \'self\'')

        attr_type = self.current_type if node._type == 'SELF_TYPE' else self.context.get_type(node._type)

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                self.errors.append(f'El tipo de la variable {node.name} no puede ser {expr_type}')

        scope.define_variable(node.name, attr_type)
    
    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.name)

        scope.define_variable('self', self.current_type)

        for item in node.params:
            param_name, param_type = item.name, self.context.get_type(item.type)
            if not scope.is_local_variable(param_name):
                if param_type.name == 'SELF_TYPE':
                    self.errors.append('El tipo \'SELF_TYPE\' es invalido')
                    scope.define_variable(param_name, ErrorType())
                else:
                    scope.define_variable(
                        param_name, self.context.get_type(param_type.name))
            else:
                self.errors.append(f'La variable {param_name} ya esta definida en el metodo {self.current_method.name}')

        return_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type

        expr_type = self.visit(node.expr, scope)

        if not expr_type.conforms_to(return_type):
            self.errors.append(f'El tipo esperado seria {return_type.name} y no {expr_type.name}')

    # expresiones
    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        cond_type = self.visit(node.cond, scope)
        cond_exp_type = self.context.get_type('Bool')

        if cond_type != cond_exp_type:
            self.errors.append(f'La condicional del \'while\' debe ser de tipo Bool, no puede ser de tipo {cond_type}')

        return self.context.get_type('Object')

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        sc = scope.create_child()
        for id_, type_, exp in node.declaration:
            if exp is not None:
                return_type = self.visit(exp, sc)
                if return_type != type_:
                    self.errors.append(f'La declaración {id_} debería ser de tipo {type_}')
                    scope.define_variable(id_, ErrorType())
                else:
                    scope.define_variable(id_, type_)
            else: 
                scope.define_variable(id_, type_)
        
        return self.visit(node.expr, sc)

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ is not None:
            scope.define_variable(node.idx, type_)
        else:
            self.errors.append(f'El tipo asignado a {node.idx} es incorrecto')
            scope.define_variable(node.idx, ErrorType())

    @visitor.when(ast.ParenthesisNode)
    def visit(self, node: ast.ParenthesisNode, scope: Scope):
        return self.visit(node.expr, scope)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        type_ = ErrorType()
        sc = scope.create_child()
        if not node.expr:
            self.errors.append('Los bloques deben contener al menos una expresión.')
        for expr in node.expr:
            type_ = self.visit(expr, sc)    
        return type_

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, scope: Scope):

        if node.atom is None:
            node.atom = ast.VariableNode('self')
        
        obj_type = self.visit(node.atom, scope)

        if node.type is not None:
            try:
                parent_type = self.context.get_type(node.type)
            except SemanticError as e:
                parent_type = ErrorType()
                self.errors.append(e.text)

            if not obj_type.conforms_to(parent_type):
                self.errors.append(f'El tipo {parent_type.name} no es ancestro de {obj_type.name}')
        else:
            parent_type = obj_type

        try:
            method = parent_type.get_method(node.idx)
        except SemanticError as e:
            self.errors.append(e.text)
            for arg in node.exprlist:
                self.visit(arg, scope)
            return ErrorType()

        if len(node.exprlist) != len(method.param_names):
            self.errors.append(f'El metodo {method.name} ya ha sido definido en {obj_type.name} con diferente signatura')

        for i, arg in enumerate(node.exprlist):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(method.param_types[i]):
                self.errors.append(f'no de puede convertir a {arg_type.name} en { method.param_types[i].name}')

        return method.return_type if method.return_type.name != 'SELF_TYPE' else parent_type

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        if_type = self.visit(node.if_expr, scope)
        if if_type != self.context.get_type('Bool'):
            self.errors.append('La condicion del \'if\' tiene que ser de tipo booleano')

        self.visit(node.then_expr, scope.create_child())
        self.visit(node.else_expr, scope.create_child())
        
    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, scope: Scope):
        try:
            current_type = self.current_type if node.type == 'SELF_TYPE' else self.context.get_type(node.type) 
        except SemanticError as e:
            self.errors.append(e.text)
            current_type = ErrorType()
        return current_type

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, scope: Scope):
        self.visit(node.expr, scope)
        return self.context.get_type('Bool')

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, scope: Scope):
        return_type = ErrorType()
        if node.expr:
            return_type = self.visit(node.expr, scope)
        else:
            self.errors.append('La expresión del \'case\' no puede ser nula.')

        sc = scope.create_child()
        for id_, type_, expr in node.params:
            if type_ == 'SELF_TYPE':
                current_type = self.current_type
            else:
                try:
                    current_type = self.context.get_type(type_) 
                except SemanticError as e:
                    current_type = ErrorType()
            if scope.is_local_variable(id_):
                self.errors.append(f'La variable \'{id_}\' ya ha sido definida.')
            else:
                sc.define_variable(id_, current_type)
                
            if expr is not None:
                self.visit(expr, sc)
        
        return return_type
        

    # variable
    @visitor.when(ast.ParamNode)
    def visit(self, node: ast.ParamNode, scope: Scope):
        scope.define_variable(node.name, node.type)

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, scope: Scope):
        var_ = scope.find_variable(node.lex)
        if var_ is None:
            self.errors.append(f'La variable {node.lex} no ha sido definida definida')
            return ErrorType()
        return var_.type

    # operaciones aritmeticas
    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append('La operación \'Suma\' debe ser efectuada entre valores enteros')  
            return ErrorType()      
 
    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append('La operación \'Resta\' debe ser efectuada entre valores enteros')  
            return ErrorType()      

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append('La operación \'Multiplicación\' debe ser efectuada entre valores enteros')  
            return ErrorType()      

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append('La operación \'Divición\' debe ser efectuada entre valores enteros')  
            return ErrorType()      


    # operaciones logicas
    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        bool_type = self.context.get_type('Bool')

        if right == bool_type and left == bool_type:
            return bool_type
        else:
            self.errors.append('La operación \'Menor que\' debe ser efectuada entre valores booleanos')  
            return ErrorType()      

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        bool_type = self.context.get_type('Bool')

        if right == bool_type and left == bool_type:
            return bool_type
        else:
            self.errors.append('La operación \'Menor o igual que\' debe ser efectuada entre valores booleanos')  
            return ErrorType()      

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        self.visit(node.right, scope)
        self.visit(node.left, scope)
        return self.context.get_type('Bool')     


    # operaciones unarias
    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type('Int'):
            return type_
        else:
            self.errors.append('La operación \'Complemento\' esperaba un entero')
            return ErrorType()

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type('Bool'):
            return type_
        else:
            self.errors.append('La operación \'Negación\' esperaba un booleano')
            return ErrorType()


    # operaciones atomicas
    @visitor.when(ast.NumberNode)
    def visit(self, node: ast.NumberNode, scope: Scope):
        return self.context.get_type('Int')

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        return self.context.get_type('Bool')

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        return self.context.get_type('String')

      

        
