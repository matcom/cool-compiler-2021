from cool_ast.cool_ast import *
from utils.semantic import Context, SemanticError, Type, Method, Scope, ErrorType, VariableInfo
import visitors.visitor as visitor
from utils.errors import _TypeError, _NameError, _SemanticError, _AtributeError
class TypeChecker:
    def __init__(self, context, errors, c_m = None, c_t = None):
        self.context = context
        self.errors = errors

        self.current_method = c_m
        self.current_type = c_t
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope = None):
        if scope is None:
            scope = Scope()

        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())

        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        _char = node.id[0]
        if _char not in ''.join(chr(n) for n in range(ord('A'),ord('Z')+1)):
            self.errors.append((f'Class names must be capitalized'))

        # attrs = []
        # methods = []
        # for feature in node.features:
        #     if isinstance(feature,AttrDeclarationNode):
        #         attrs.append(feature)
        #     else:
        #         methods.append(feature)
                
        for attr, owner in self.current_type.all_attributes(): #definir atributos de los ancestros
            if owner != self.current_type:
                scope.define_variable(attr.name, attr.type)
        # for attr in attrs:
        #     self.visit(attr, scope)

        # for method in methods:
        #     self.visit(method, scope.create_child())
        
        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)
            else:
                self.visit(feature, scope.create_child())

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id, self.current_type, False)
        scope.define_variable('self', self.current_type)
        _char = node.id[0]
        if _char not in ''.join(chr(n) for n in range(ord('a'),ord('z')+1)):
            self.errors.append((f'Class names must be capitalized'))            

        # for param_name, param_type in zip(self.current_method.param_names, self.current_method.param_types):
        for i in range(len(self.current_method.param_names)):
            ithParamName = self.current_method.param_names[i]
            ithParamType = self.current_method.param_types[i]
            if ithParamName == 'self':
                self.errors.append(_SemanticError %(node.token_list[0].lineno, node.token_list[0].col, f"'self' cannot be the name of a formal parameter."))
                continue
            if not scope.is_local(ithParamName):
                if ithParamType.name == 'SELF_TYPE':
                    self.errors.append('SELF_TYPE cannot be the type of a parameter.')
                    scope.define_variable(ithParamName, ErrorType())
                else:
                    # try:
                    #     param_t = self.context.get_type(ithParamType.name)
                    # except SemanticError as es:
                    #     self.errors.append(es.text())
                    #     param_t = ErrorType()
                    scope.define_variable(ithParamName, self.context.get_type(ithParamType.name))
            else:
                # self.errors.append(f'Variable {ithParamName} is already defined in {self.current_method.name}.')
                self.errors.append(_SemanticError %(node.token_list[0].lineno, node.token_list[0].col, f'Formal parameter {ithParamName} is multiply defined.'))

        if node.type != 'SELF_TYPE':
            rType = self.context.get_type(node.type) 
        else:
            rType = self.current_type

        exprType = self.visit(node.body, scope)

        if not exprType.conforms_to(rType):
            self.errors.append(_TypeError %(node.body.token_list[0].lineno, node.body.token_list[0].col, f'Infered return type {exprType.name} of method {node.id} does not conform to declared return type {rType.name}.'))
            # self.errors.append(f'{exprType.name} does not conform {rType.name}.')

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ifT = self.visit(node.ifChunk, scope.create_child())
        thenT = self.visit(node.thenChunk, scope.create_child())
        elseT = self.visit(node.elseChunk, scope.create_child())

        if ifT != self.context.get_type('Bool'):
            # self.errors.append(f"Can't convert {ifT.name} to Bool.")
            self.errors.append(_TypeError % (node.ifChunk.token_list[0].lineno, node.ifChunk.token_list[0].col,f"Predicate of 'if' does not have type Bool."))
        try:
            return thenT.join(elseT)
        except:
            return ErrorType()
    
    @visitor.when(LetInNode)
    def visit(self, node, scope):
        iteration = 0
        for nod in node.decl_list:
            _id = nod.id
            _t = nod.type
            _e = nod.expr

            if _id =='self':
                self.errors.append(_SemanticError %(node.decl_list[iteration].token_list[0].lineno, node.decl_list[iteration].token_list[0].col, f"'self' cannot be bound in a 'let' expression."))
                continue
            
            try:
                if _t != 'SELF_TYPE':
                    var_type = self.context.get_type(_t) 
                else:
                    var_type = self.current_type
            except SemanticError as e:
                # self.errors.append(e.text)
                self.errors.append(_TypeError %(node.decl_list[iteration].token_list[0].lineno, node.decl_list[iteration].token_list[2].col, f"Class {_t} of let-bound identifier {_id} is undefined."))
                var_type = ErrorType()

            # if scope.is_local(_id):
            #     self.errors.append(f'Variable {_id} is already defined in {self.current_method.name}.')
            # else:
            #     scope.define_variable(_id, var_type)
            scope.define_variable(_id, var_type)

            if _e is not None:
                expr = self.visit(_e, scope.create_child()) 
            else:
                expr = None
            if expr is not None and not expr.conforms_to(var_type):
                # self.errors.append(f"Can't convert {expr.name} to {var_type.name}.")
                self.errors.append(_TypeError %(node.decl_list[iteration].token_list[0].lineno, node.decl_list[iteration].token_list[0].col, f"Infered type {expr.name} of initialization of {_id} does not conform to identifier's declared type {var_type.name}"))
            iteration+=1
        return self.visit(node.expression, scope.create_child())

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if node.id == 'self':
                self.errors.append(_SemanticError %(node.token_list[0].lineno, node.token_list[0].col, f"'self' cannot be the name of an attribute."))
                return

        _char = node.id[0]

        if _char not in ''.join(chr(n) for n in range(ord('a'),ord('z')+1)):
            # self.errors.append((f'Attribute names must not be capitalized'))
            self.errors.append(_SemanticError %(node.token_list[0].lineno, node.token_list[0].col, f"Attribute names must not be capitalized."))

        if node.type != 'SELF_TYPE':
            attrType = self.context.get_type(node.type) 
        else:
            attrType = self.current_type

        if node.value is not None:
            value_t = self.visit(node.value, scope.create_child())
            if not value_t.conforms_to(attrType):
                # self.errors.append(f"Can't convert {value_t.name} to {attrType.name}.")
                self.errors.append(_TypeError %(node.value.token_list[0].lineno, node.value.token_list[0].col, f'Infered type {value_t.name} of initialization of attribute {node.id} does not conform to declared type {attrType.name}'))
        else:
            scope.create_child()

        scope.define_variable(node.id, attrType)
        
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        var_info = scope.find_variable(node.id)

        exprType = self.visit(node.expr, scope.create_child())
        
        if node.id == 'self':
            self.errors.append(_SemanticError % (node.token_list[1].lineno, node.token_list[1].col, f"Cannot assign to 'self'."))
            return ErrorType()
        
        if var_info is None:
            self.errors.append(f'Undefined variable {node.id} in {self.current_method.name}.')
        else:
            if not exprType.conforms_to(var_info.type):
                self.errors.append(f"Can't convert {exprType.name} to {var_info.name}.")

        return exprType

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        condition = self.visit(node.condition, scope)
        if condition != self.context.get_type('Bool'):
            # self.errors.append(f"Can't convert {condition.name} to Bool.")
            self.errors.append(_TypeError %(node.condition.token_list[0].lineno, node.condition.token_list[0].col, f'Loop condition does not have type Bool.'))

        self.visit(node.loopChunk, scope.create_child())
        return self.context.get_type('Object')

    @visitor.when(ChunkNode)
    def visit(self, node, scope):
        child_scope = scope.create_child()
        return_type = ErrorType()
        
        for expr in node.chunk:
            return_type = self.visit(expr, child_scope)
        return return_type
    
    @visitor.when(SwitchCaseNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        types = []
        t_set = set()
        # for i, t, e in node.case_list:
        for i, t, e, token_list  in node.case_list:
            child_scope = scope.create_child()
            try:
                if t != 'SELF_TYPE':
                    if t not in t_set:
                        t_set.add(t) 
                    else:
                        self.errors.append(_SemanticError % (token_list[2].lineno, token_list[2].col, f'Duplicate branch {t} in case statement.'))
                    t_typo = self.context.get_type(t)
                    child_scope.define_variable(i, t_typo)
                else:
                    self.errors.append(f'SELF_TYPE is not valid as the type of a case branch.')
            except SemanticError as exc:
                child_scope.define_variable(i, ErrorType())
                self.errors.append(_TypeError % (token_list[2].lineno, token_list[2].col, f'Class {t} of case branch is undefined.'))
                # self.errors.append(exc.text)
            
            types.append(self.visit(e, child_scope))

        return Type.multi_join(types)


    @visitor.when(PlusNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')

        if lt == rt == intType:
            return intType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' + '+str(rt.name)))
        # self.errors.append(f'Undefined operation "+" between {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')

        if lt == rt == intType:
            return intType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' - '+str(rt.name)))
        # self.errors.append(f'Undefined operation "-" between {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(StarNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')

        if lt == rt == intType:
            return intType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' * '+str(rt.name)))
        # self.errors.append(f'Undefined operation "*" between {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(DivNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')

        if lt == rt == intType:
            return intType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' / '+str(rt.name)))
        # self.errors.append(f'Undefined operation "/" between {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(CallNode)
    def visit(self, node, scope):
        if node.obj is None:
            node.obj = VariableNode('self')
        obj_type = self.visit(node.obj, scope)

        if node.parent is not None:
            try:
                ancestor_type = self.context.get_type(node.parent)
            except SemanticError as e:
                ancestor_type = ErrorType()
                # self.errors.append(e.text)

            if not obj_type.conforms_to(ancestor_type):
                self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, f'Expression type {obj_type.name} does not conform to declared static dispatch type {ancestor_type.name}.'))
                # self.errors.append(f'{obj_type.name} does not inherits from {ancestor_type.name}.')
        else:
            ancestor_type = obj_type

        try:
            method = ancestor_type.get_method(node.method, self.current_type, False)
        except SemanticError as e:
            self.errors.append(_AtributeError % (node.token_list[0].lineno, node.token_list[0].col, f'Dispatch to undefined method {node.method}'))
            # self.errors.append(e.text)
            for arg in node.args:
                self.visit(arg, scope)
            return ErrorType()

        # if len(node.args) != len(method.param_names):
        #     self.errors.append(f'Function {method.name} is already defined in {obj_type.name}.')

        if len(node.args) != len(method.param_types):
            self.errors.append(_SemanticError %(node.token_list[1].lineno, node.token_list[1].col, f"Method {method.name} called with wrong number of arguments"))
        else:
            for i, arg in enumerate(node.args):
                arg_type = self.visit(arg, scope)
                if not arg_type.conforms_to(method.param_types[i]):
                    # self.errors.append(f"Can't convert {arg_type.name} to {method.param_types[i].name}.")
                    self.errors.append(_TypeError %(node.args[i].token_list[0].lineno, node.args[i].token_list[0].col, f"In call of {method.name}, type {arg_type.name} of parameter {method.param_names[i]} does not conform to declare type {method.param_types[i].name}"))

        if method.return_type.name != 'SELF_TYPE':
            return method.return_type 
        else:
            return ancestor_type

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        return self.context.get_type('Int')

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return self.context.get_type('String')

    @visitor.when(TrueNode)
    def visit(self, node, scope):
        return self.context.get_type('Bool')

    @visitor.when(FalseNode)
    def visit(self, node, scope):
        return self.context.get_type('Bool')

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if node.lex == 'self':
            variable = VariableInfo('self', self.current_type)
        else:
            variable = scope.find_variable(node.lex)
            if variable is None:
                try:
                    _var = self.current_type.get_attribute(node.lex, self.current_type, False)
                    variable = VariableInfo(_var.name, _var.type)
                except SemanticError as e:
                    pass
        if variable is None:
            # self.errors.append(f'Variable {node.lex} is not defined in {self.current_method.name}.')
            self.errors.append(_NameError % (node.token_list[0].lineno, node.token_list[0].col, f"Undeclared identifier {node.lex}."))
            return ErrorType()
        return variable.type

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            if node.lex != 'SELF_TYPE':
                return self.context.get_type(node.lex) 
            else:
                return self.current_type
        except SemanticError as e:
            self.errors.append(_TypeError % (node.token_list[1].lineno, node.token_list[1].col, f"'new' used with undefined class {node.lex}."))
            # self.errors.append(e.text)
            return ErrorType()

    @visitor.when(NotNode)
    def visit(self, node, scope):
        tp = self.visit(node.expression, scope)
        if tp == self.context.get_type('Bool'):
            return tp
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, f"Argument of 'not' has type {tp.name} instead of Bool."))
        # self.errors.append(f'Undefined operation "not" for {tp.name}.')
        return ErrorType()

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        tp = self.visit(node.expr, scope)
        if tp == self.context.get_type('Int'):
            return tp
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, f"Argument of '~' has type {tp.name} instead of Int."))
        # self.errors.append(f'Undefined operation "~" for {tp.name}.')
        return ErrorType()

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.method, scope)
        return self.context.get_type('Bool')

    @visitor.when(LeqNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')
        boolType = self.context.get_type('Bool')

        if lt == rt == intType:
            return boolType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' <= '+str(rt.name)))
        # self.errors.append(f'Undefined operation "<=" for {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(LessNode)
    def visit(self, node, scope): 
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)

        intType = self.context.get_type('Int')
        boolType = self.context.get_type('Bool')
        if lt == rt == intType:
            return boolType
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, 'non-Int arguments: '+str(lt.name)+' < '+str(rt.name)))
        # self.errors.append(f'Undefined operation "<" for {lt.name} and {rt.name}.')
        return ErrorType()

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        lt = self.visit(node.left, scope)
        rt = self.visit(node.right, scope)
        # quite self type de los basicos aqui
        if lt.name not in ("Int", "String", "Bool", "IO", "Object") and rt.name not in ("Int", "String", "Bool", "IO", "Object"):
            return self.context.get_type('Bool')
        if lt == rt:
            return self.context.get_type('Bool')
        self.errors.append(_TypeError % (node.token_list[0].lineno, node.token_list[0].col, f'Illegal comparison with a basic type.'))
        return ErrorType()