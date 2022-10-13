from symbol import return_stmt
from . import ast_nodes as cool
from .semantic import *
from . import visitor
from typing import Any, Dict, List, Optional, Tuple
from copy import deepcopy

# creación del átomo y tipo que representará el NULL
 
class NullNode(cool.AtomicNode):
    def __init__(self):
        super().__init__("NULL")

class NullType(Type):
    def __init__(self):
        super().__init__("null")

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __str__(self):
        return self.name


class COOLwithNULL:
    
    def __init__(self, context: Context):
        self.current_method = None
        self.current_type = None
        self.context: Context = context
        
        # Dict[str, cool.ClassDecNode]
        self.class_declarations = {}  

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        # list de ClassDecNode
        newclassdec = []

        for type_ in ["Object", "IO",  "String", "Int", "Bool"]:
            t = self.context.get_type(type_)
            t.define_method("__init__", [], [], t)
            t.methods.move_to_end("__init__", last=False)

        for class_dec in node.class_list:
            self.class_declarations[class_dec.name] = class_dec

        for class_dec in node.class_list:
            newclassdec.append(self.visit(class_dec))

        return cool.ProgramNode(newclassdec)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        parents = [self.class_declarations[owner.name] for _, owner in self.current_type.all_attributes()]

        attrs, visited = [], set()
        
        for parent in parents:
            if parent.name in visited:
                continue

            visited.add(parent.name)
            attrs += [feature for feature in parent.data if isinstance(feature, cool.AttributeDecNode)]

        expressions: List[cool.ExprNode] = []
        for attr in attrs:
            expressions.append(self.visit(attr))
        expressions.append(cool.VariableNode("self"))

        body = cool.BlockNode(expressions)
        constructor = cool.MethodDecNode(
            "__init__", [], self.current_type.name, body
        )

        self.current_type.define_method("__init__", [], [], self.current_type)
        self.current_type.methods.move_to_end("__init__", last=False)

        attrs = [
            attrib
            for attrib in node.data
            if isinstance(attrib, cool.AttributeDecNode)
        ]
        methods = [
            meth
            for meth in node.data
            if isinstance(meth, cool.MethodDecNode)
        ]

        features = attrs + [constructor] + methods

        return cool.ClassDecNode(node.name, features, node.parent)

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode):
        if node.expr is None:
            expr = None
            if node._type == "Int":
                expr = cool.NumberNode("0")
            elif node._type == "Bool":
                expr = cool.BooleanNode("false")
            elif node._type == "String":
                expr = cool.StringNode('""')
            else:
                ## adicion del indicador de vacio
                expr = NullNode()
            return cool.AssignNode(node.name, expr)
        return cool.AssignNode(node.name, deepcopy(node.expr))


# analiza de nuevo los tipos y recopila errores, 
# esto no es necesario pero la recopilacion de errores se me hizo mas facil
class COOLwithNULL_Type:
    def __init__(self, context: Context, errors: list, program: str):
        self.context: Context = context
        self.errors = errors
        self.current_type = None
        self.current_method = None
        self.current_attribute = None
        self.program = program

    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    #############
    # main flow #
    #############

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope=None):
        if scope is None:
            scope = Scope()
        node.scope = scope

        for item in node.class_list:
            self.visit(item, scope.create_child())
        return scope

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.name)

        attrs = [ att for att in node.data if isinstance(att, cool.AttributeDecNode)]   
        methods = [ meth for meth in node.data if isinstance(meth, cool.MethodDecNode)]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        node.scope = scope
        if node.name == "self":
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Cannot set "self" as attribute of a class.')

        try:
            attr_type = (self.context.get_type(node._type) if node._type != "SELF_TYPE" else self.current_type)
        except SemanticError:
            attr_type = ErrorType()

        scope.define_variable("self", self.current_type)

        self.current_attribute = self.current_type.get_attribute(node.name)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                line, lexpos = node.expr_pos
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{attr_type.name}".')
        scope.define_variable(node.name, attr_type)

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        node.scope = scope
        self.current_method = self.current_type.get_method(node.name)
        self.current_attribute = None
        scope.define_variable("self", self.current_type)

        for param_name, param_type in zip(self.current_method.param_names, self.current_method.param_types):
            if scope.is_local_variable(param_name):
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - SemanticError: Variable "{param_name}" is already defined in method "{self.current_method.name}".')
            else:
                if param_type.name != "SELF_TYPE":
                    try:
                        scope.define_variable(param_name, self.context.get_type(param_type.name))
                    except SemanticError:
                        scope.define_variable(param_name, ErrorType())  
                else:
                    self.errors.append('(0, 0) - TypeError: "SELF_TYPE" cannot be a static type of a parameter.')
                    scope.define_variable(param_name, ErrorType())
        
        try:
            ret_type = (self.context.get_type(node.type) if node.type != "SELF_TYPE" else self.current_type)
        except SemanticError:
            ret_type = ErrorType()

        expr_type = self.visit(node.expr, scope)
        1
        if not expr_type.conforms_to(ret_type):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{ret_type.name}".')

    
    ###############
    # expressions #
    ###############
    
    
    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        node.scope = scope
        var_info = scope.find_variable(node.idx)

        if var_info.name == "self":
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - SemanticError: Variable "self" is read-only.')

        expr_type = self.visit(node.expr, scope)
        if var_info is None:
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - NameError: Variable "{node.idx}" is not defined in "{self.current_method.name}".')
        else:
            if not expr_type.conforms_to(var_info.type):
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{var_info.type.name}".')
        return expr_type

    
    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        node.scope = scope
        
        for i, (_id, _type, _expr) in enumerate(node.declaration):
            
            if _id == "self":
                line, lexpos = node.declaration_names_positions[i]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: "self" cannot be bound in a "let" expression')
                continue

            try:
                var_static_type = (self.context.get_type(_type) if _type != "SELF_TYPE" else self.current_type)
            
            except SemanticError:
                line, lexpos = node.declaration_types_positions[i]
                self.errors.append( f'({line}, {self.get_tokencolumn(self.program,lexpos)}) - TypeError: Type "{_type}" is not defined')
                var_static_type = ErrorType()

            scope.define_variable(_id, var_static_type)

            expr_type = (self.visit(_expr, scope.create_child()) if _expr is not None else None)
            
            if expr_type is not None and not expr_type.conforms_to(var_static_type):
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{var_static_type.name}".')

        return self.visit(node.expr, scope.create_child())
        
        

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        node.scope = scope
        return_type = ErrorType()
        
        for expr in node.expr:
            return_type = self.visit(expr, scope)
        
        return return_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        node.scope = scope
        
        if_type = self.visit(node.if_expr, scope)
        ##
        if if_type != self.context.get_type("Bool"):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Cannot convert "{if_type.name}" into "Bool".')
        
        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)
        
        return then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        node.scope = scope
        
        cond = self.visit(node.cond, scope)
        if cond != self.context.get_type("Bool"):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Cannot convert "{cond.name}" into "Bool".')

        self.visit(node.data, scope)
        return self.context.get_type("Object")

    @visitor.when(cool.CaseNode) 
    def visit(self, node: cool.CaseNode, scope: Scope):
        node.scope = scope

        self.visit(node.expr, scope)
        types = []
        visited = set()
        for i, (_id, _type, _expr) in enumerate(node.params):
            _scope = scope.create_child()
            try:
                if _type != "SELF_TYPE":
                    _scope.define_variable(_id, self.context.get_type(_type))
                else:
                    self.errors.append('(%d, %d) - TypeError: "%s" cannot be a static type of a case branch.' % _type)
            except SemanticError:
                _scope.define_variable(_id, ErrorType())
                line, lexpos = node.cases_positions[i]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Class "{_type}" of case branch is undefined')

            if _type in visited:
                line, lexpos = node.cases_positions[i]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Duplicate branch "{_type}" in case statement')

            visited.add(_type)
            types.append(self.visit(_expr, _scope))

        return Type.multi_join(types)


    @visitor.when(cool.MethodCallNode) 
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        node.scope = scope
        entre = None
        if node.atom is None:
            node.atom = cool.VariableNode("self")
            entre = 1
        atom_type = self.visit(node.atom, scope)
        atom_type
        
        if node.type is None:
            ancestor_type = atom_type
        else:
            try:
                ancestor_type = self.context.get_type(node.type)
            except SemanticError:
                ancestor_type = ErrorType()
                line, lexpos = node.type_position
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Type "{node.type}" is not defined')

            if not atom_type.conforms_to(ancestor_type):
                line, lexpos = node.type_position
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Class "{atom_type.name}" has no an ancestor class "{ancestor_type.name}".')

        try:
            entre
            method = ancestor_type.get_method(node.idx)
        except SemanticError:
            line, lexpos = node.id_position
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - AttributeError: Dispatch undefined method "{node.idx}" from type {atom_type.name}')

            for exp in node.exprlist:
                self.visit(exp, scope)
            return ErrorType()

        expr_count = len(node.exprlist)
        params_count = len(method.param_names)
        if expr_count != params_count:
            line, lexpos = node.id_position
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Method "{method.name}" of type "{atom_type.name}" called with wrong number of arguments. Expected {params_count} instead of {args_count}')

        number_of_args = min(expr_count, params_count)
        for i, arg in enumerate(node.exprlist[:number_of_args]):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(method.param_types[i]):
                line, lexpos = node.args_positions[i]
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Cannot convert "{arg_type.name}" into "{method.param_types[i].name}".')

        return (method.return_type if method.return_type.name != "SELF_TYPE" else ancestor_type)

    
    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        node.scope = scope
        
        variable = scope.find_variable(node.lex)
        
        if variable is not None:
            return variable.type
        else:
            # get the name in the att or the meth
            if self.current_attribute is not None:
                name = self.current_attribute.name
            else:
                name = self.current_method.name

            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - NameError: Variable "{node.lex}" is not defined in "{name}".')
            
            return ErrorType()
        

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        node.scope = scope
                
        try:
            if node.type == "SELF_TYPE":
                return self.current_type
            else:
                ret_type = self.context.get_type(node.type)
                return ret_type
        except SemanticError:
            line, lexpos = node.type_position
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Using "new" expresion with undefined type "{node.lex}"')
            
            return ErrorType()
        
    
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        node.scope = scope
        
        self.visit(node.expr, scope)
        return self.context.get_type("Bool")
   
    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope: Scope):
        node.scope = scope
        return self.visit(node.expr, scope)
   
    
    ####################
    # unary operations #
    ####################

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type("Bool"):
            return type_
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Operation "not" is not defined for "{type_.name}".')
        
        return ErrorType()

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        type_ = self.visit(node.expr, scope)
        if type_ == self.context.get_type("Int"):
            return type_
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program,node.lexpos)}) - TypeError: Operation "~" is not defined for "{type_.name}".')
        
        return ErrorType()


    #####################
    # binary operations #
    #####################
    
    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Int")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "+" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Int")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "-" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Int")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "*" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Int")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "/" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Bool")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "<=" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        if l_type == r_type == self.context.get_type("Int"):
            return self.context.get_type("Bool")
        self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: Operation "<" is not defined between "{l_type.name}" and "{r_type.name}".')
        
        return ErrorType()

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        node.scope = scope
        l_type = self.visit(node.left, scope)
        r_type = self.visit(node.right, scope)

        types_ = ("Bool", "Int", "String")
        if l_type.name != r_type.name and (l_type.name in types_ or l_type.name in types_):
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - TypeError: For operation "=" if one of the expression has static type Int, Bool or String, then the other must have the same static type')
        
        return self.context.get_type("Bool")
    
    
    ##############
    # atomic exp #
    ##############
    
    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Bool")

    @visitor.when(NullNode)
    def visit(self, node: NullNode, scope: Scope):
        node.scope = scope
        return NullType()


