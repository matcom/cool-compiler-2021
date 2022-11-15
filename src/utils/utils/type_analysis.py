from signal import raise_signal
from .semantic import SemanticError
from .semantic import Type
from .semantic import VoidType, ErrorType
from .semantic import Context, Scope 
from utils import ast_nodes as ast
from utils import visitor

class TypeCollector(object):
    def __init__(self, context: Context, errors, program):
        self.context = context
        self.errors = errors
        self.program = program
    
    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2


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
        # object_type.define_method('get_type', [], [], str_type)
        object_type.define_method('type_name', [], [], str_type)
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
        except SemanticError:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Invalid redefinition of class "{node.name}"')


class TypeBuilder:
    def __init__(self, context: Context, errors, program):
        self.context: Context = context
        self.current_type: Type = None
        self.errors = errors
        self.program = program
    
    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

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
                line, lexpos = node.parent_pos
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Class "{node.name}" cannot inherits from "{node.parent}"')
            
            try:
                parent_type = self.current_type.set_parent(self.context.get_type(node.parent))
            except SemanticError:
                line, lexpos = node.parent_pos
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Parent type for class "{node.name}" is an undefined type "{node.parent}"')

            # try:
            #     self.current_type.set_parent(parent_type)
            # except SemanticError:
            #     self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Parent type is already set for "{node.name}"')   
        else:
            # obj = self.context.get_type('Object')
            # self.current_type.set_parent(obj)

            try:
                self.current_type.set_parent(self.context.get_type("Object"))
            except SemanticError:
                if node.name not in ["Int","String","Bool","IO","Object","SELF_TYPE"]:
                    self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Parent type is already set for "{node.name}"') 
        
        # for item in node.data:
        #      self.visit(item)

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
        except SemanticError:
            pass
            # self.errors.append(
                # f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) \
                #     - SemanticError: Method "{self.name}" already defined in \
                #         {self.current_type.name}')
            # self.errors.append(e.text)
            # self.current_type.define_attribute(node.name, ErrorType())


class TypeBuilderFeature:
    def __init__(self, context: Context, errors, program):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.program = program
    
    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

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

        for data in node.data:
            self.visit(data)

        self.current_type = self.context.get_type(node.name)
        
    
    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode):
        line, lexpos = node.type_pos
        try:
            attr_type = self.context.get_type(node._type)
        except SemanticError:
            attr_type = ErrorType()
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Undefined type "{node._type}" for attribute "{node.name}" in class "{self.current_type.name}"')

        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticError:
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Attribute "{node.name}" is already defined in "{self.current_type.name}".')
    
    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode):
        param_names = []
        param_types = []

        # (name, typex)
        for i, param in enumerate(node.params):
            name = param.name
            typex = param.type
            param_names.append(name)
            try:
                param_types.append(self.context.get_type(typex))
            except SemanticError:
                param_types.append(ErrorType())
                line, lexpos = node.p_types_pos[i]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Undefined param type "{typex}" in method "{node.name}", in class "{self.current_type.name}"')
        try:
            return_type = self.context.get_type(node.type)
        except SemanticError:
            return_type = ErrorType()
            line, lexpos = node.r_types_pos
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Undefined return type "{node.type}" in method "{node.name}", in class "{self.current_type.name}"')
        try:
            self.current_type.define_method(node.name, param_names, param_types, return_type)
        except SemanticError:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Method "{node.name}" already defined in {self.current_type.name}')

class TypeChecker:
    def __init__(self, context: Context, errors, program):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.program = program
    
    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

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
        self.current_type = self.context.get_type(node.name)
        
        attributes = [att for att in node.data if isinstance(att, ast.AttributeDecNode)]
        methods = [meth for meth in node.data if isinstance(meth, ast.MethodDecNode)]
        
        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for item in attributes:
            self.visit(item, scope)
        
        for item in methods:
            self.visit(item, scope.create_child())
    
    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, scope: Scope):
        if node.name == 'self':
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Cannot set "self" as attribute of a class.')
        try:
            attr_type = self.current_type if node._type == 'SELF_TYPE' else self.context.get_type(node._type)
        except SemanticError: attr_type = ErrorType()
        
        scope.define_variable('self', self.current_type)
        self.current_attribute = self.current_type.get_attribute(node.name)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if expr_type is not None and not expr_type.conforms_to(attr_type):
                self.errors.append(f'({node.expr_pos[0]}, {node.expr_pos[1]}) - TypeError: Cannot convert "{expr_type.name}" into "{attr_type.name}".')
        scope.define_variable(node.name, attr_type)
    
    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.name)

        scope.define_variable('self', self.current_type)

        for item in node.params:
            param_name, param_type = item.name, self.context.get_type(item.type)
            if not scope.is_local_variable(param_name):
                if param_type.name == 'SELF_TYPE':
                    self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: "SELF_TYPE" cannot be a static type of a parameter.')
                    scope.define_variable(param_name, ErrorType())
                else:
                    scope.define_variable(
                        param_name, self.context.get_type(param_type.name))
            else:
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Variable "{param_name}" is already defined in method "{self.current_method.name}".')

        return_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type

        expr_type = self.visit(node.expr, scope)

        if expr_type is not None and not expr_type.conforms_to(return_type):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{return_type.name}".')

    # expresiones
    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        cond_type = self.visit(node.cond, scope)
        cond_exp_type = self.context.get_type('Bool')

        if cond_type != cond_exp_type:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{cond_type.name}" into "Bool".')

        return self.context.get_type('Object')

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        for pos, (id_, type_, exp) in enumerate(node.declaration):
            if id_ == 'self':
                l, lp = node.dec_names_pos[pos]
                self.errors.append(f'({l}, {lp}) - SemanticError: "self" cannot be bound in a "let" expression')
                continue
            try:
                if type_ != "SELF_TYPE": 
                    var_type = self.context.get_type(type_)
                else: 
                    var_type = self.current_type
                
            except SemanticError:
                line, lexpos = node.dec_types_pos[pos]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Type "{type_}" is not defined')
                var_type = ErrorType()
            scope.define_variable(id_, var_type)
            
            expr_type = None
            if exp is not None:
                expr_type = self.visit(exp, scope.create_child())
            if expr_type is not None and not expr_type.conforms_to(var_type):
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{var_type.name}".')
            
            # if exp is not None:
            #     return_type = self.visit(exp, sc)
            #     if return_type != type_:
            #         self.errors.append(f'La declaración {id_} debería ser de tipo {type_}')
            #         scope.define_variable(id_, ErrorType())
            #     else:
            #         scope.define_variable(id_, type_)
            # else: 
            #     scope.define_variable(id_, type_)
        
        sc = scope.create_child()
        return self.visit(node.expr, sc)

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        var_type = scope.find_variable(node.idx)
        if var_type is None:
            self.error.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - NameError: Variable "{self.idx}" is not defined in "{self.current_method.name}".')
        else:
            if var_type.name == "self":
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Variable "self" is read-only.')

            type_ = self.visit(node.expr, scope.create_child())
        
            if not type_.conforms_to(var_type.type):
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{type_.name}" into "{var_type.type.name}".')
            # if type_ is not None:
            #     scope.define_variable(node.idx, type_)
            # else:
            #     self.errors.append(f'El tipo asignado a {node.idx} es incorrecto')
            #     scope.define_variable(node.idx, ErrorType())
        return type_

    @visitor.when(ast.ParenthesisNode)
    def visit(self, node: ast.ParenthesisNode, scope: Scope):
        return self.visit(node.expr, scope)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        type_ = ErrorType()
        # sc = scope.create_child()
        # if not node.expr:
        #     self.errors.append('Los bloques deben contener al menos una expresión.')
        for expr in node.expr:
            type_ = self.visit(expr, scope)    
        return type_

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, scope: Scope):

        if node.atom is None:
            node.atom = ast.VariableNode('self')
        
        obj_type = self.visit(node.atom, scope)

        if node.type is not None:
            try:
                parent_type = self.context.get_type(node.type)
            except SemanticError:
                parent_type = ErrorType()
                line, lexpos = node.type_position
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)})\
                     - TypeError: Type "{node.type}" is not defined')

            if not obj_type.conforms_to(parent_type):
                line, lexpos = node.type_position
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)})\
                     - TypeError: Class "{obj_type.name}" has no an ancestor \
                         class "{parent_type.name}".')
        else:
            parent_type = obj_type

        try:
            method = parent_type.get_method(node.idx)
        except SemanticError:
            line, lexpos = node.id_position
            self.errors.append(
                f'({line}, {self.get_tokencolumn(self.program, lexpos)})\
                     - AttributeError: Dispatch undefined method "{node.idx}"\
                          from type {obj_type.name}')
            for arg in node.exprlist:
                self.visit(arg, scope)
            return ErrorType()

        if len(node.exprlist) != len(method.param_names):
            line, lexpos = node.id_position
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Method "{method.name}" of type "{obj_type.name}" called with wrong number of arguments. Expected {len(node.exprlist)} instead of {len(method.param_names)}')

        else:
            for i, arg in enumerate(node.exprlist):
                arg_type = self.visit(arg, scope)
                if not arg_type.conforms_to(method.param_types[i]):
                    line, lexpos = node.exprlist_positions[i]
                    self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Cannot convert "{arg_type.name}" into "{method.param_types[i].name}".')

        return method.return_type if method.return_type.name != 'SELF_TYPE' else parent_type

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        if_type = self.visit(node.if_expr, scope)
        if if_type != self.context.get_type('Bool'):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{if_type.name}" into "Bool".')

        then_ = self.visit(node.then_expr, scope.create_child())
        else_ = self.visit(node.else_expr, scope.create_child())

        return then_.join(else_)
        
    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, scope: Scope):
        try:
            current_type = self.current_type if node.type == 'SELF_TYPE' else self.context.get_type(node.type) 
        except SemanticError as e:
            line, lexpos = node.type_position
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Using "new" expresion with undefined type "{node.type}"')
            return ErrorType()
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
        t = []
        v = []
        for pos, (id_, type_, expr) in enumerate(node.params):
            sc = scope.create_child()
            try:
                if type_ != 'SELF_TYPE':
                    t_ = self.context.get_type(type_)
                    sc.define_variable(id_, t_)
                else:
                    line, lexpos = node.cases_positions[pos]
                    type_
                    self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: "{type_}" cannot be a static type of a case branch.')
            except SemanticError:
                sc.define_variable(id_, ErrorType())
                line, lexpos = node.cases_positions[pos]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Class "{type_}" of case branch is undefined')
            
            # Cannot be dublicate Branches types
            if type_ in v:
                line, lexpos = node.cases_positions[pos]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Duplicate branch "{type_}" in case statement')

            v.append(type_)
            t.append(self.visit(expr, sc))
        
        return Type.multi_join(t)
        

    # variable
    @visitor.when(ast.ParamNode)
    def visit(self, node: ast.ParamNode, scope: Scope):
        scope.define_variable(node.name, node.type)

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, scope: Scope):
        var_ = scope.find_variable(node.lex)
        if var_ is None:
            if self.current_attribute is not None:
                name = self.current_attribute.name
            else:
                name = self.current_method.name
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - NameError: Variable "{node.lex}" is not defined in "{name}".')
            return ErrorType()
        return var_.type

    # operaciones aritmeticas
    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right.name == int_type.name and left.name == int_type.name:
            return int_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "+" is not defined between "{left.name}" and "{right.name}".')  
            return ErrorType()      
 
    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "-" is not defined between "{left.name}" and "{right.name}".') 
            return ErrorType()      

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "*" is not defined between "{left.name}" and "{right.name}".')   
            return ErrorType()      

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return int_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "/" is not defined between "{left.name}" and "{right.name}".') 
            return ErrorType()      


    # operaciones logicas
    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        bool_type = self.context.get_type('Bool')
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return bool_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "<" is not defined between "{left.name}" and "{right.name}".') 
            return ErrorType()      

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)
        bool_type = self.context.get_type('Bool')
        int_type = self.context.get_type('Int')

        if right == int_type and left == int_type:
            return bool_type
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "<=" is not defined between "{left.name}" and "{right.name}".') 
            return ErrorType()      

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        right = self.visit(node.right, scope)
        left = self.visit(node.left, scope)

        types_ = ['Int', 'Bool', 'String']
        if (right.name in types_ or left.name in types_) and right.name != left.name:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: For operation "=" if one of the expression has static type Int, Bool or String, then the other must have the same static type')
        
        return self.context.get_type('Bool')     


    # operaciones unarias
    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type('Int'):
            return type_
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "~" is not defined for "{type_.name}".')
            return ErrorType()

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type('Bool'):
            return type_
        else:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "not" is not defined for "{type_.name}".')
            return ErrorType()


    # operaciones atomicas
    @visitor.when(ast.NumberNode)
    def visit(self, node: ast.NumberNode, scope: Scope):
        node.lex = str(node.lex)
        return self.context.get_type('Int')

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        return self.context.get_type('Bool')

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        return self.context.get_type('String')

    # Parenthesis
    @visitor.when(ast.ExprParNode)
    def visit(self, node: ast.ExprParNode, scope: Scope):
        return self.visit(node.expr, scope)

      
class PositionateTokensInAST:
    def __init__(self, tokens):
        self.position = 0
        self.tokens = tokens

    def inc_position(self, value=1):
        self.position += value

    def binary_op(self, node: ast.BinaryNode):
        self.visit(node.left)

        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        self.inc_position() 

        self.visit(node.right)

    def single_op(self, node: ast.UnaryNode):
        token = self.tokens[self.position]
        node.operation_position = token.line, token.lexpos

        token = self.tokens[self.position + 1]
        node.set_position(token.line, token.lexpos)

        self.inc_position() 
        self.visit(node.expr)

    def atom(self, node: ast.Node):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        self.inc_position() 

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        for cl in node.class_list:
            self.visit(cl)
            self.inc_position()

        # there is always at least a class declaration
        first_declaration = node.class_list[0] 
        node.set_position(first_declaration.line, first_declaration.lexpos)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode):
        token = self.tokens[self.position]
        assert (token.value.lower() == "class"), f'Expected "class" instead of "{token.value}" in {node.name}'

        token = self.tokens[self.position + 1]
        node.set_position(token.line, token.lexpos)

        if node.parent is not None:
            token = self.tokens[self.position + 3]
            node.parent_pos = token.line, token.lexpos

        count = 3 if node.parent is None else 5
        self.inc_position(count)

        for d in node.data:
            self.visit(d)
            token = self.tokens[self.position]
            assert (token.value == ";"), f'Expected ";" instead of "{token.value}" in {d.name} of class {node.name}'
            self.inc_position()

        self.inc_position()

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)

        token = self.tokens[self.position + 2]
        node.type_pos = token.line, token.lexpos

        if node.expr is not None:
            self.inc_position(4)
            token = self.tokens[self.position]
            node.expr_pos = token.line, token.lexpos
            self.visit(node.expr)
            token = self.tokens[self.position]
            return

        self.inc_position(3)

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        self.inc_position(2)

        for i, _ in enumerate(node.params):
            self.inc_position(2)
            token = self.tokens[self.position]
            node.p_types_pos.append((token.line, token.lexpos))
            self.inc_position() 
            if i < len(node.params) - 1:
                self.inc_position() 

        self.inc_position(2) 
        token = self.tokens[self.position]
        node.r_types_pos = token.line, token.lexpos
        self.inc_position(2) 

        self.visit(node.expr)
        self.inc_position() 

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode):
        token = self.tokens[self.position]
        
        node.set_position(token.line, token.lexpos)
        self.inc_position()

        for _, _, expr in node.declaration:
            token = self.tokens[self.position]
            node.dec_names_pos.append((token.line, token.lexpos))
            token = self.tokens[self.position + 2]
            node.dec_types_pos.append((token.line, token.lexpos))
            if expr is not None:
                self.inc_position(4) 
                token = self.tokens[self.position]
                self.visit(expr)
                self.inc_position()
            else:
                self.inc_position(4) 

        self.visit(node.expr)

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)

        token = self.tokens[self.position + 1]
        assert token.value == "<-", f'Expected "<-" instead of "{token.value}" in assign'

        self.inc_position(2)  # ends after `<-`
        self.visit(node.expr)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode):
        token = self.tokens[self.position]
        assert token.value == "{", f'Expected "{{" instead of "{token.value}" in block'
        node.set_position(token.line, token.lexpos)
        self.inc_position() 

        for i, expr in enumerate(node.expr, start=1):
            self.visit(expr)
            token = self.tokens[self.position]
            assert (token.value == ";"), f'Expected ";" instead of "{token.value}" in instruction {i} of a block'
            self.inc_position() 

        token = self.tokens[self.position]
        assert (token.value == "}"), f'Expected "}}" instead of "{token.value}" at the end of a block'
        self.inc_position()

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode):
        # IF
        token = self.tokens[self.position]
        assert (token.value == "if"), f'Expected "if" instead of "{token.value}" in conditional'
        node.set_position(token.line, token.lexpos)
        self.inc_position() 
        self.visit(node.if_expr)
        # THEN
        token = self.tokens[self.position]
        assert (token.value == "then"), f'Expected "then" instead of "{token.value}" in conditional'
        self.inc_position() 
        self.visit(node.then_expr)
        # ELSE
        token = self.tokens[self.position]
        assert (token.value == "else"), f'Expected "else" instead of "{token.value}" in conditional'
        self.inc_position() 
        self.visit(node.else_expr)
        # FI
        token = self.tokens[self.position]
        assert (token.value == "fi"), f'Expected "fi" instead of "{token.value}" in conditional'
        self.inc_position() 

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        self.inc_position() 
        self.visit(node.cond)
        self.inc_position()  
        self.visit(node.data)
        self.inc_position()  

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        # CASE
        self.inc_position()  
        self.visit(node.expr)
        # OF
        self.inc_position()
        for _, _, expr in node.params:
            self.inc_position(2)
            token = self.tokens[self.position]
            node.cases_positions.append((token.line, token.lexpos))
            self.inc_position(2)
            self.visit(expr)
            self.inc_position()
        # ESAC
        self.inc_position()

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        node.id_position = token.line, token.lexpos

        _atom = node.atom is not None
        _type = node.type is not None

        if _atom:
            self.visit(node.atom)

            token = self.tokens[self.position]
            assert token.value in ("@","."), f"Expected '.' or '@' instead of {token.value}"
            self.inc_position()

            token = self.tokens[self.position]
            node.id_position = token.line, token.lexpos

        if _type:
            token = self.tokens[self.position]
            node.type_position = token.line, token.lexpos
            self.inc_position(2)
            token = self.tokens[self.position]
            node.id_position = token.line, token.lexpos

        self.inc_position(2) 
        token = self.tokens[self.position]
        if node.exprlist:
            for exp in node.exprlist:
                token = self.tokens[self.position]
                node.exprlist_positions.append((token.line, token.lexpos))
                self.visit(exp)
                token = self.tokens[self.position]
                assert token.value in (",", ")"), f"Expected ',' or ')' instead of {token.value}"
                self.inc_position()  
        else:
            self.inc_position()

    @visitor.when(ast.NumberNode)
    def visit(self, node: ast.NumberNode):
        self.atom(node)

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode):
        self.atom(node)

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode):
        self.atom(node)

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode):
        self.atom(node)

    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode):
        token = self.tokens[self.position]
        node.set_position(token.line, token.lexpos)
        token = self.tokens[self.position + 1]
        node.type_position = token.line, token.lexpos
        self.inc_position(2) 

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode):
        self.single_op(node)

    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode):
        self.single_op(node)

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode):
        self.single_op(node)

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode):
        self.binary_op(node)

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode):
        self.binary_op(node)

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode):
        self.binary_op(node)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode):
        self.binary_op(node)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode):
        self.binary_op(node)

    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode):
        self.binary_op(node)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode):
        self.binary_op(node)

    @visitor.when(ast.ExprParNode)
    def visit(self, node: ast.ExprParNode):
        token = self.tokens[self.position]
        assert token.value == "(", f'Expected "(" instead of "{token.value}" in parenthesis expression'
        self.inc_position()

        self.visit(node.expr)

        token = self.tokens[self.position]
        assert token.value == ")", f'Expected ")" instead of "{token.value}" in parenthesis expression'
        self.inc_position()



