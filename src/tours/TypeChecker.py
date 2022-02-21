from parsing.ast import *
from .utils import find_parent_type, InferType, is_base_class
from cmp.semantic import Scope, SemanticError
from cmp.semantic import Type, ObjectType, IntType, StringType, BoolType, AutoType, ErrorType, SelfType, IOType
import cmp.visitor as visitor


SELF_IS_READONLY = "SemanticError: Cannot assign to 'self'."
SELF_IS_READONLY_LET = "SemanticError: 'self' cannot be bound in a 'let' expression."
SELF_IS_READONLY_PARAM = "SemanticError: 'self' cannot be the name of a formal parameter."
SELF_IS_READONLY_ATTRIBUTE = "SemanticError: 'self' cannot be the name of an attribute."
INCOMPATIBLE_ATTRIBUTE_TYPE = "TypeError: Inferred type %s of initialization of attribute %s does not conform to declared type %s."
INCOMPATIBLE_VARIABLE_TYPE = "TypeError: Inferred type %s of initialization of %s does not conform to identifier's declared type %s." 
INCOMPATIBLE_RET_FUNC_TYPE = "TypeError: Inferred return type %s of method %s does not conform to declared return type %s."
INCOMPATIBLE_DISPATCH_TYPE = "TypeError: In call of method %s, type %s of parameter %s does not conform to declared type %s."
INCOMPATIBLE_DISPATCH_DEC_TYPE = "TypeError: Expression type %s does not conform to declared static dispatch type %s."
VARIABLE_NOT_DEFINED = "NameError: Undeclared identifier %s."
INVALID_OPERATION = "TypeError: non-Int arguments: %s %s %s"
INVALID_BASIC_COMPARISON = "TypeError: Illegal comparison with a basic type."
OPERATION_NOT_DEFINED = "TypeError: Operation '%s' is not defined for type '%s'."
UNARY_OPERATION_NOT_DEFINED = "TypeError: Argument of '%s' has type %s instead of %s."
PREDICATE_OPERATIONS = "TypeError: %s condition does not have type Bool." 
WRONG_NUMBER_ARGUMENTS = "SemanticError: Method %s called with wrong number of arguments."
DUPLICATE_BRANCH = "SemanticError: Duplicate branch %s in case statement."
CASE_TYPE_UNDEFINED = "TypeError: Class %s of case branch is undefined."
UNDEFINED_METHOD = "AttributeError: Dispatch to undefined method %s."
PARENT_ATTRIBUTE_REDEFINED = "SemanticError: Attribute %s is an attribute of an inherited class."
UNDEFINED_VARIABLE_TYPE = "TypeError: Class %s of let-bound identifier %s is undefined."
METHOD_REDEFINED_PARAM = "SemanticError: In redefined method %s, parameter type %s is different from original type %s."
METHOD_REDEFINED_RETURN = "SemanticError: In redefined method %s, return type %s is different from original return type %s."
METHOD_REDEFINED_NPARAM = "SemanticError: Incompatible number of formal parameters in redefined method %s."
UNDEFINED_NEW_TYPE = "TypeError: 'new' used with undefined class %s."


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors
        self.current_type = None
        self.current_method = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for dec in node.declarations:
            self.visit(dec, scope.create_child(dec.id))
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable('self', self.current_type)

        for feature in node.features:
            # If two attributes with the same name are defined, the second one is not added to the attribute 
            # list, so I will only visit its expression.
            if isinstance(feature, AttrDeclarationNode):
                if self.current_type.get_attribute(feature.id).type.name == feature.type:
                    self.visit(feature, scope)
                elif feature.expr is not None:
                    self.visit(feature.expr, scope)
            else:
                self.visit(feature, scope)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        # Ask if the attribute is defined in the parent, if true an error is added
        parent = self.current_type.parent
        if parent is not None:
            try:
                parent.get_attribute(node.id)
                self.errors.append(PARENT_ATTRIBUTE_REDEFINED.replace('%s', node.id, 1))
            except SemanticError:
                pass
        
        if node.id == "self":
            self.errors.append(SELF_IS_READONLY_ATTRIBUTE)
         
        node_type = self.current_type.get_attribute(node.id).type
        if node_type == SelfType():
            node_type = self.current_type
        
        if node.expr is not None:
            self.visit(node.expr, scope)
            expr_type = node.expr.computed_type
            if expr_type == SelfType():
                expr_type = self.current_type
        
            if node_type != AutoType() and expr_type != AutoType() and not expr_type.conforms_to(node_type):
                self.errors.append(INCOMPATIBLE_ATTRIBUTE_TYPE.replace('%s', expr_type.name, 1).replace('%s', node.id, 1).replace('%s', node_type.name, 1))
            elif node_type == AutoType() and expr_type != AutoType():
                InferType(self.current_type, node_type, expr_type)
            elif node_type != AutoType() and expr_type == AutoType():
                InferType(self.current_type, expr_type, node_type)
             
    @visitor.when(FuncDeclarationNode) 
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        child = scope.create_child(scope.class_name, self.current_method.name)
        
        # Ask if the method is defined with a diffrent signature in the parent, if true an error is added
        parent = self.current_type.parent
        if parent is not None:
            try:
                method = parent.get_method(node.id)
                if method.return_type != self.current_method.return_type:
                    self.errors.append(METHOD_REDEFINED_RETURN.replace('%s', node.id, 1).replace('%s', self.current_method.return_type.name, 1).replace('%s', method.return_type.name, 1))
                if len(self.current_method.param_types) != len(method.param_types):
                    self.errors.append(METHOD_REDEFINED_NPARAM.replace('%s', node.id, 1))
                else:
                    for type_child, type_parent in zip(self.current_method.param_types, method.param_types):
                        if type_child != type_parent:
                            self.errors.append(METHOD_REDEFINED_PARAM.replace('%s', node.id, 1).replace('%s', type_child.name, 1).replace('%s', type_parent.name, 1))

            except SemanticError:
                pass
                
        for name, typex in zip(self.current_method.param_names, self.current_method.param_types):
            if name != "self":
                child.define_variable(name, typex)
            else:
                 self.errors.append(SELF_IS_READONLY_PARAM)
        
        self.visit(node.expr, child)

        return_type_exp = node.expr.computed_type if node.expr.computed_type != SelfType() else self.current_type
        return_type_met = self.current_method.return_type if self.current_method.return_type != SelfType() else self.current_type

        if return_type_met != AutoType() and return_type_exp != AutoType():
            if not return_type_exp.conforms_to(return_type_met):
                self.errors.append(INCOMPATIBLE_RET_FUNC_TYPE.replace('%s', return_type_exp.name, 1).replace('%s',node.id , 1).replace('%s',return_type_met.name , 1))       
        elif return_type_met == AutoType() and return_type_exp != AutoType():
            InferType(self.current_type, return_type_met, return_type_exp)
        elif return_type_met != AutoType() and return_type_exp == AutoType():
            InferType(self.current_type, return_type_exp, return_type_met)
           
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.expr_lis:
            self.visit(expr, scope)
        node.computed_type = node.expr_lis[-1].computed_type  

    @visitor.when(DispatchNode)
    def visit(self, node, scope):
        typee = None
        if node.expr is not None:
            self.visit(node.expr, scope)
            obj_type = node.expr.computed_type if node.expr.computed_type != SelfType() else self.current_type

            if node.type is not None:
                try:
                    typex = self.context.get_type(node.type)
                    if not obj_type.conforms_to(typex):
                        self.errors.append(INCOMPATIBLE_DISPATCH_DEC_TYPE.replace('%s', obj_type.name, 1).replace('%s', typex.name, 1))
                        typex = ErrorType()
                    obj_type = typex    
                except SemanticError as error:
                    self.errors.append(error.text)
                    obj_type = ErrorType()
        else:
            obj_type = scope.find_variable('self').type
        
        try:
            method = obj_type.get_method(node.id)
            if (node.arg is None and method.arg is None) or (len(node.arg) == len(method.param_types)):
                if node.arg is not None:
                    for arg, param_type, param_name in zip(node.arg, method.param_types, method.param_names):
                        self.visit(arg, scope)
                        arg_type = arg.computed_type if arg.computed_type != SelfType() else self.current_type 
                    
                        if param_type != AutoType() and arg_type != AutoType() and not arg_type.conforms_to(param_type):
                            self.errors.append(INCOMPATIBLE_DISPATCH_TYPE.replace('%s', node.id, 1).replace('%s', arg_type.name, 1).replace('%s', param_name, 1).replace('%s', param_type.name, 1))
                            typee = ErrorType()
                        elif param_type == AutoType() and arg_type != AutoType():
                            InferType(self.current_type, param_type, arg_type)

                        elif param_type != AutoType() and arg_type == AutoType():
                            InferType(self.current_type, arg_type, param_type)
            else:
                self.errors.append(WRONG_NUMBER_ARGUMENTS.replace('%s', method.name, 1))           

            if typee is None:
                ret_type = method.return_type if method.return_type != SelfType() else obj_type 
            else:
                ret_type = typee
        
        except SemanticError as error:
           self.errors.append(UNDEFINED_METHOD.replace('%s',node.id))
           ret_type = ErrorType()   
        
        node.computed_type = ret_type 

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type 
        
        self.visit(node.then, scope)
        self.visit(node.elsex, scope)

        if predicate_type != AutoType() and predicate_type.conforms_to(BoolType()):
            node.computed_type = find_parent_type(self.current_type, node.then.computed_type, node.elsex.computed_type)
        elif predicate_type != AutoType(): 
            self.errors.append(PREDICATE_OPERATIONS.replace('%s', "If", 1))
            node.computed_type = ErrorType()
        else:
            InferType(self.current_type, predicate_type, BoolType())
            
    @visitor.when(LetNode)
    def visit(self, node, scope):
        child = scope.create_child(scope.class_name, scope.method_name)
        for item in node.variables:
            self.visit(item, child)

        self.visit(node.expr, child)
        node.computed_type = node.expr.computed_type    

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        if node.id == 'self':
            self.errors.append(SELF_IS_READONLY_LET) 
        
        try:
            var_type = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(UNDEFINED_VARIABLE_TYPE.replace('%s', node.type, 1).replace('%s', node.id, 1))
            var_type = ErrorType()
        
        if node.expr is not None:    
            self.visit(node.expr, scope)
            expresion_type = node.expr.computed_type if node.expr.computed_type != SelfType() else self.current_type 
            
            if expresion_type != AutoType() and var_type != AutoType() and not expresion_type.conforms_to(var_type):
                self.errors.append(INCOMPATIBLE_VARIABLE_TYPE.replace('%s', expresion_type.name, 1).replace('%s', node.id, 1).replace('%s', var_type.name, 1))
            elif var_type == AutoType() and expresion_type != AutoType():
                InferType(self.current_type, var_type, expresion_type)
            elif var_type != AutoType() and expresion_type == AutoType():
                InferType(self.current_type, expresion_type, var_type)

        if scope.is_local(node.id):
            scope.remove_variable(node.id)
        else:  
            scope.define_variable(node.id, var_type)

        node.computed_type = var_type
        
    @visitor.when(LoopNode)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.computed_type
        self.visit(node.body, scope)
        
        if predicate_type != AutoType() and predicate_type.conforms_to(BoolType()):            
            node.computed_type = ObjectType()
        elif predicate_type != AutoType():    
            self.errors.append(PREDICATE_OPERATIONS.replace('%s',"Loop", 1))
            node.computed_type = ErrorType()
        else:
            InferType(self.current_type, predicate_type, BoolType())
            node.computed_type = ObjectType()
          
    @visitor.when(CaseNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        
        types_computed = []
        types = []
        for attr in node.cases:
            self.visit(attr, scope)
            types_computed.append(attr.computed_type)
            if attr.type in types:
                self.errors.append(DUPLICATE_BRANCH.replace('%s', attr.type, 1))
            else:
                types.append(attr.type)
    
        typex = types_computed[0] 
        for i in range(1,len(types_computed)):
            typex =  find_parent_type(self.current_type, typex, types_computed[i])
        node.computed_type = typex     

    @visitor.when(CaseAttrNode)
    def visit(self, node, scope):  
        try:
            typex = self.context.get_type(node.type)
            if typex == AutoType():
                self.errors.append("The type of a case attribute can not be AUTO_TYPE.")
                typex = ErrorType()
        except SemanticError as error:
            self.errors.append(CASE_TYPE_UNDEFINED.replace('%s', node.type, 1))
            typex = ErrorType()

        child_scope = scope.create_child(scope.class_name, scope.method_name)
        child_scope.define_variable(node.id, typex)
        self.visit(node.expr, child_scope)

        node.computed_type = node.expr.computed_type

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        self.visit(node.id, scope)
        var_type = node.id.computed_type
        
        self.visit(node.expr, scope)
        expresion_type = node.expr.computed_type if node.expr.computed_type != SelfType() else self.current_type  
        
        node.computed_type = expresion_type

        if node.id.lex == 'self':
            self.errors.append(SELF_IS_READONLY)
            node.computed_type = ErrorType() 
        elif var_type != AutoType() and expresion_type != AutoType() and not expresion_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_VARIABLE_TYPE.replace('%s', expresion_type.name, 1).replace('%s', node.id.lex).replace('%s', var_type.name, 1))
            node.computed_type = ErrorType() 
        elif var_type == AutoType() and expresion_type != AutoType():
            InferType(self.current_type, var_type, expresion_type)
        elif var_type != AutoType() and expresion_type == AutoType():
            InferType(self.current_type, expresion_type, var_type)
                                     
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left,scope)  
        left_type = node.left.computed_type
        self.visit(node.right,scope)
        right_type = node.right.computed_type
    
        if isinstance(node, PlusNode):
            operation = "+"
        elif isinstance(node, MinusNode):
            operation= "-"
        elif isinstance(node, DivNode):
            operation = "/" 
        elif isinstance(node, StarNode):
            operation = "*"  
        elif isinstance(node, ElessNode):
            operation = "<="
        elif isinstance(node, LessNode):
            operation = "<"           
        
        if left_type != AutoType() and right_type != AutoType():
            if not isinstance(node, EqualsNode):
                if left_type == IntType() and right_type == IntType(): 
                    if isinstance(node, ElessNode) or isinstance(node, LessNode):
                        node.computed_type = BoolType()
                    else:
                        node.computed_type = IntType()  
                else:
                    if(left_type == right_type):
                        self.errors.append(OPERATION_NOT_DEFINED.replace('%s', operation, 1).replace('%s', left_type.name, 1))
                    else:
                        self.errors.append(INVALID_OPERATION.replace('%s', left_type.name, 1).replace('%s', operation, 1).replace('%s', right_type.name, 1))
                    node.computed_type = ErrorType()
            else:
                if left_type == right_type:
                    if left_type == StringType() or left_type == IntType() or left_type == BoolType():
                        node.computed_type = BoolType()
                    else:
                        self.errors.append(OPERATION_NOT_DEFINED.replace('%s', "equals", 1).replace('%s', left_type.name, 1))
                        node.computed_type = ErrorType() 
                else:
                    if is_base_class(left_type.name) or is_base_class(right_type.name):
                        self.errors.append(INVALID_BASIC_COMPARISON)
                        node.computed_type = ErrorType()
                    else:
                        node.computed_type = BoolType()    
        
        else:
            if left_type == AutoType() and right_type == AutoType():
                if isinstance(node, ElessNode) or isinstance(node, LessNode) or isinstance(node, EqualsNode):
                    node.computed_type = BoolType()
                else:
                    node.computed_type = IntType()

                if not isinstance(node, EqualsNode):
                    InferType(self.current_type, left_type, IntType())
                    InferType(self.current_type, right_type, IntType())
            
            else:
                if left_type == AutoType():
                    auto_node = node.left
                    auto_var = left_type
                    not_auto_var = right_type
                else:
                    auto_node = node.right
                    auto_var = right_type
                    not_auto_var = left_type

                if not isinstance(node, EqualsNode):
                    if not_auto_var == IntType():
                        if isinstance(node, ElessNode) or isinstance(node, LessNode):
                            node.computed_type = BoolType()
                        else:
                            node.computed_type = IntType()
                    else:
                        self.errors.append(OPERATION_NOT_DEFINED.replace('%s', operation, 1).replace('%s', not_auto_var.name, 1))
                        node.computed_type = ErrorType()
                    InferType(self.current_type, auto_var, IntType())                      
                else:
                    if not_auto_var == StringType() or not_auto_var == IntType() or not_auto_var == BoolType():
                        node.computed_type = BoolType()
                        InferType(self.current_type, auto_var, not_auto_var)                       
                    else:
                        self.errors.append(OPERATION_NOT_DEFINED.replace('%s', "equals", 1).replace('%s', not_auto_var.name, 1))
                        node.computed_type = ErrorType() 

    @visitor.when(PrimeNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        type_expr = node.expr.computed_type
        
        if type_expr == IntType() or type_expr == AutoType():
            node.computed_type = IntType()
            if type_expr == AutoType():
                InferType(self.current_type, type_expr, IntType())
        else:     
            self.errors.append(UNARY_OPERATION_NOT_DEFINED.replace('%s', "~", 1).replace('%s', type_expr.name, 1).replace('%s', "Int", 1))
            node.computed_type = ErrorType()
   
    @visitor.when(NotNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        type_expr = node.expr.computed_type
        
        if type_expr == BoolType() or type_expr == AutoType():
            node.computed_type = BoolType()
            if type_expr == AutoType():
                InferType(self.current_type, type_expr, BoolType())
        else:     
            self.errors.append(UNARY_OPERATION_NOT_DEFINED.replace('%s', "not", 1).replace('%s', type_expr.name, 1).replace('%s', "Bool", 1))
            node.computed_type = ErrorType()

    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.computed_type = StringType()

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = BoolType()

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        node.computed_type = IntType()

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex, self.current_type):
            var_type = scope.find_variable_or_attribute(node.lex, self.current_type).type
        else:
            self.errors.append(VARIABLE_NOT_DEFINED.replace('%s', node.lex, 1))
            var_type = ErrorType()
        node.computed_type = var_type    
   
    @visitor.when(TrueNode)
    def visit(self, node, scope):
        node.computed_type = BoolType()

    @visitor.when(FalseNode)
    def visit(self, node, scope):
        node.computed_type = BoolType()    
    
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            var_type = self.context.get_type(node.lex)
            if var_type == AutoType():
                self.errors.append('Class AUTO_TYPE can not be instantiated.')
                var_type = ErrorType() 
        except SemanticError as error:
            self.errors.append(UNDEFINED_NEW_TYPE.replace('%s', node.lex, 1))
            var_type = ErrorType()  
        
        node.computed_type =  var_type     