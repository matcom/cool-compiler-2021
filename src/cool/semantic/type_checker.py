from cool.Parser.AstNodes import *
from cool.semantic import visitor
from cool.semantic.semantic import ObjectType, Scope
from cool.semantic.semantic import get_common_parent,multiple_get_common_parent,is_local
from cool.semantic.semantic import SemanticException
from cool.semantic.semantic import ErrorType, IntType, BoolType
from cool.utils.Errors.semantic_errors import *


class TypeChecker:
    def __init__(self, context, errors=[],counter = 1):
        self.context = context
        self.current_type = None
        self.current_feature = None
        self.errors = errors
        self.counter = counter
        self.inference = []

    @visitor.on('node')
    def visit(self, node, scope,expected = None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None, expected = None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, expected = None):
        self.current_type = self.context.get_type(node.id)
        
        scope.define_variable('self', self.current_type)          
        for feature in node.features:
            if type(feature) == FuncDeclarationNode:
                self.visit(feature, scope.create_child())
            else:
                self.visit(feature, scope)
                attr = self.current_type.get_attribute(feature.id)
                scope.define_variable(attr.name, attr.type)
                
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope, expected = None):
        if node.expr:
            expected_child = None
            self.current_feature = self.current_type
            
            expected_child = node.type
                
            node_type = self.context.get_type(node.type)
            self.visit(node.expr, scope,expected_child)
            expr_type = node.expr.computed_type
            
            if not expr_type.conforms_to(node_type):
                text = INCOMPATIBLE_TYPES.replace('%s',expr_type.name,1).\
                    replace('%s', node.id, 1).replace('%s',node_type.name,1)
                error = TypeError(node.column,node.row,text)
                self.errors.append(error)

         
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope,expected = None):
        self.current_feature = self.current_type.get_method(node.id)
        
        for param in node.params:
            self.visit(param, scope)
            
        method_rtn_type = self.current_feature.return_type
        if method_rtn_type.name != 'Void':
            new_expected = self.current_feature.return_type.name
        else:
            new_expected = None

        self.visit(node.body, scope, expected = new_expected)
        expr_type = node.body.computed_type
        
        method_rtn_type = self.current_feature.return_type
        if method_rtn_type.name != 'Void':
            try:
                if not expr_type.conforms_to(method_rtn_type):
                    text = f'In class "{self.current_type.name}" in method "{self.current_feature.name}" return type:' + INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).\
                    replace('%s', self.current_feature.name, 1).replace('%s', method_rtn_type.name, 1)
                    error = TypeError(node.column,node.row,text)
                    self.errors.append(error)
            except Exception:
                text = f'In class "{self.current_type.name}" in method "{self.current_feature.name}" : ' + INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).\
                replace('%s', self.current_feature.name, 1).replace('%s', method_rtn_type.name, 1)
                error = TypeError(node.column,node.row,text)
                self.errors.append(error)

        self.current_type.change_param(node.id,scope)

    @visitor.when(ParamDeclarationNode)
    def visit(self, node, scope,expected = None):
        try:
            var_type = self.context.get_type(node.type)
        except SemanticException as ex:
            var_type = ErrorType()
            text = f'{ex.text} Of formal parameter {node.id}'
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)

        if node.id == 'self':
            text = "self cannot be the name of a formal parameter"
            error = SemanticError(node.column, node.row, text)
            self.errors.append(error)
        elif not is_local(scope.locals,node.id):
            scope.define_variable(node.id, var_type)
        else:
            text = MULTIPLY_DIFINED_PARAMTER.replace('%s', node.id, 1)
            error = SemanticError(node.column,node.row,text)
            self.errors.append(error)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope,expected = None):
        try:
            var_type = self.context.get_type(node.type)
        except SemanticException as ex:
            text = f'In class {self.current_type.name}: '+ ex.text
            var_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
        
        scope.define_variable(node.id, var_type)
        self.visit(node.expr, scope)
        expr_type = node.expr.computed_type
        
        node.computed_type = expr_type
            
    @visitor.when(ExpressionGroupNode)
    def visit(self, node, scope,expected = None):
        scope_child = scope.create_child()
        for i,child in enumerate(node.body):
            if(i == len(node.body)-1):
                self.visit(child , scope_child, expected)
            else:
                self.visit(child , scope_child)
        
        
        body_type = node.body[-1].computed_type
        node_type = body_type
        node.computed_type = node_type
    
    @visitor.when(IfNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.ifexp,scope,'Bool')
        if_type = node.ifexp.computed_type
        
        self.visit(node.thenexp, scope,expected)
        then_type = node.thenexp.computed_type
        
        self.visit(node.elseexp, scope,expected)
        else_type = node.elseexp.computed_type
        
        if not if_type.conforms_to(BoolType()):
            text = INVALID_CONDITION.replace('%s', 'if', 1)
            node_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
            
        node.computed_type = get_common_parent(then_type,else_type ,self.context)        


    @visitor.when(WhileNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.condition, scope, 'Bool' )
        condition_type = node.condition.computed_type
        
        self.visit(node.body, scope)
        body_type = node.body.computed_type
        
        if not condition_type.conforms_to(BoolType()):
            text = INVALID_CONDITION.replace('%s', 'while', 1)
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
                
        node.computed_type = ObjectType()
    
    @visitor.when(LetNode)
    def visit(self, node, scope,expected = None):
        child_scope = scope.create_child()
        for arg in node.params:
            if arg.type == 'SELF_TYPE':
                arg.type = self.current_type.name

            self.visit(arg,child_scope)
            arg_type = arg.computed_type
            
        self.visit(node.body, child_scope,expected)
        body_type = node.body.computed_type
        node_type = body_type
        
        node.computed_type = node_type
        
    @visitor.when(LetDeclarationNode)
    def visit(self, node, scope,expected = None):
        expected_child = node.type
        if node.id == 'self':
            text = '\'self\' cannot be bound in a \'let\' expression.'
            error = SemanticError(node.column,node.row,text)
            self.errors.append(error)
        try:
            node_type = self.context.get_type(node.type)
        except SemanticException as ex:
            text = f'In class "{self.current_type.name}": '+ ex.text
            node_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
        
        if node.expr:
            self.visit(node.expr, scope,expected_child)
            expr_type = node.expr.computed_type

            if not expr_type.conforms_to(node_type):
                text = INCOMPATIBLE_TYPES.replace('%s', expr_type.name, 1).\
                    replace('%s', node.id, 1).replace('%s', node_type.name, 1)
                error = TypeError(node.column,node.row,text)
                self.errors.append(error)

        if not scope.is_local(node.id):
            scope.define_variable(node.id, node_type)
        else:
            var = scope.find_variable(node.id)
            var.type = node_type
        
        node.computed_type = node_type
        
        
    @visitor.when(CaseNode)
    def visit(self, node, scope,expected = None): 
        
        self.visit(node.case, scope)
        body_type = None
        brnaches_type = []
        expr_types = []
        
        for branch in node.body:
            if branch.type in brnaches_type:
                text = f'Duplicate branch {branch.type} in case statement.'
                error = SemanticError(branch.column,branch.row,text)
                self.errors.append(error)
            else:
                brnaches_type.append(branch.type)

            self.visit(branch,scope.create_child())
            expr_types.append(branch.computed_type)
        
        
        node_type = multiple_get_common_parent(expr_types,self.context)
        node.computed_type = node_type
            
            
    @visitor.when(AssignNode)
    def visit(self, node, scope, expected=None):
        self.visit(node.expr, scope)
        node_type = node.expr.computed_type

        if scope.is_defined(node.id):
            var = scope.find_variable(node.id)

            if var.name == 'self':
                text = SELF_IS_READONLY 
                error = SemanticError(node.column, node.row,text)
                self.errors.append(error)
                node_type = ErrorType()
            elif not node_type.conforms_to(var.type):
                text = INCOMPATIBLE_TYPES.replace(
                    '%s', node_type.name, 1).replace('%s', var.name, 1).replace('%s', var.type.name, 1)
                error = TypeError(node.column, node.row, text)
                self.errors.append(error)
                node_type = ErrorType()
        
        else:
            try:
                var = self.current_type.get_attribute(node.id)
                node_type = self.context.get_type(var.type.name)
            except SemanticException as ex:
                text = VARIABLE_NOT_DEFINED.replace('%s', node.id, 1)
                error = NameError(node.column,node.row,text)
                self.errors.append(error)
                node_type = ErrorType()

        node.computed_type = node_type
    
    @visitor.when(CallNode)
    def visit(self, node, scope,expected = None):
        try:
            if node.obj is None:
                node.obj = InstantiateNode(self.current_type.name,node.row,node.column) 
                obj_type = self.current_type
                node.obj.computed_type = None
            else:
                self.visit(node.obj, scope)
                obj_type = node.obj.computed_type

            if node.parent and not obj_type.has_parent(self.context.get_type(node.parent)):
                text = f'In class {self.current_type.name}: '+ f'Expression type "{obj_type.name}" does not conform to declared static dispatch type "{node.parent}" in function call of "{node.id}"'
                error = TypeError(node.column,node.row,text)
                self.errors.append(error)

            try:
                obj_method = obj_type.get_method(node.id)

                if len(node.args) == len(obj_method.param_types):
                    for _,params in enumerate(zip(node.args, obj_method.param_types)):
                        arg, param_type = params
                        try:
                            self.visit(arg, scope,param_type.name)
                            arg_type = arg.computed_type
                        except SemanticException as ex:
                            text = f'In class {self.current_type.name}: '+ ex.text
                            node_type = ErrorType()
                            error = SemanticError(node.column,node.row,text)
                            self.errors.append(error)

                        if not arg_type.conforms_to(param_type):

                            try:
                                name_arg=arg.lex
                            except:
                                name_arg = arg.id
                            text = f'In class {self.current_type.name} in function call {node.id}: ' + INCOMPATIBLE_TYPES.replace('%s', arg_type.name, 1).replace('%s', name_arg, 1).replace('%s', param_type.name, 1)
                            error = TypeError(node.column,node.row,text)
                            self.errors.append(error)
                else:
                    text = f' In class {self.current_type.name}: Method "{obj_method.name}" from "{obj_type.name}" only accepts {len(obj_method.param_types)} argument(s)'
                    error = SemanticError(node.column,node.row,text)
                    self.errors.append(error)

                if obj_method.return_type.name == 'self':
                    node_type = obj_type
                else:
                    node_type = obj_method.return_type
                    
            except SemanticException as ex:
                text = f'In class {self.current_type.name}: '+ ex.text
                node_type = ErrorType()
                error = AttributeError(node.column,node.row,text)
                self.errors.append(error)

        except SemanticException as ex:
            text = f'In class {self.current_type.name}: '+ ex.text
            error = SemanticError(node.column,node.row,text)
            self.errors.append(error)
            for arg in node.args:
                self.visit(arg, scope)
            node_type = ErrorType()

        node.computed_type = node_type
    
    @visitor.when(BinaryIntNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.left, scope,'Int')
        left_type = node.left.computed_type
        
        self.visit(node.right, scope,'Int')
        right_type = node.right.computed_type
        
        if not left_type.conforms_to(IntType()) or not right_type.conforms_to(IntType()):
            text = INVALID_OPERATION.replace('%s', left_type.name, 1).\
                replace('%s',node.lex,1).replace('%s', right_type.name, 1)

            node_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
        else:
            node_type = IntType()
            
        node.computed_type = node_type
        
    @visitor.when(BinaryBoolNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.left, scope,'Int')
        left_type = node.left.computed_type
        
        self.visit(node.right, scope,'Int')
        right_type = node.right.computed_type
        
        if not left_type.conforms_to(IntType()) or not right_type.conforms_to(IntType()):
            text = INVALID_OPERATION.replace('%s', left_type.name, 1).\
                replace('%s',node.lex,1).replace('%s', right_type.name, 1)
            node_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
        else:
            node_type = BoolType()
            
        node.computed_type = node_type
        
    @visitor.when(EqualNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.left, scope)
        left_type = node.left.computed_type
        
        self.visit(node.right, scope)
        right_type = node.right.computed_type
    
        node_type = BoolType()

        if (left_type.name in ['Int', 'Bool', 'String'] or\
            right_type.name in ['Int', 'Bool', 'String']) and\
            left_type.name != right_type.name:
            text = WRONG_COMPARISON.replace('%s', left_type.name, 1).\
            replace('%s', right_type.name, 1)
            error = TypeError( node.column,node.row,text)
            self.errors.append(error)
            node_type = ErrorType()
            
        node.computed_type = node_type
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope,expected = None):
        node.computed_type = self.context.get_type('Int')
        
    @visitor.when(BooleanNode)
    def visit(self, node, scope,expected = None):
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(StringNode)
    def visit(self, node, scope,expected = None):
        node.computed_type = self.context.get_type('String')

    @visitor.when(VariableNode)
    def visit(self, node, scope,expected = None):
        
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            node_type = var.type
        else:
            try:
                var = self.current_type.get_attribute(node.lex)
                node_type = var.type
            except SemanticException as ex:
                node_type = ErrorType()
                error = NameError(node.column,node.row,ex.text)
                self.errors.append(error)

        node.computed_type = node_type

    @visitor.when(InstantiateNode)
    def visit(self, node, scope,expected = None):
        try:
            node_type = self.context.get_type(node.lex)
            if node_type.name == 'SELF_TYPE':
                node_type = self.current_type
        except SemanticException as ex:
            text = f'In class {self.current_type.name}: '+ ex.text
            node_type = ErrorType()
            error = TypeError(node.column,node.row,text)
            self.errors.append(error)
            
        node.computed_type = node_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.right, scope)
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(NotNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.right, scope)
        expr_type = node.right.computed_type
        node_type = self.context.get_type('Bool')

        if expr_type.name != 'Bool':
            text = WRONG_TYPE_EXPECTED.replace('%s', 'not', 1).\
                replace('%s', expr_type.name, 1).replace('%s','Bool', 1)
            error = TypeError(node.column, node.row, text)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type

    
    @visitor.when(NegateNode)
    def visit(self, node, scope,expected = None):
        self.visit(node.right, scope)
        expr_type = node.right.computed_type
        node_type = self.context.get_type('Int')

        if expr_type.name != 'Int':
            text = WRONG_TYPE_EXPECTED.replace('%s', '~', 1).\
                replace('%s', expr_type.name, 1).replace('%s','Int', 1)
            error = TypeError(node.column, node.row, text)
            self.errors.append(error)
            node_type = ErrorType()

        node.computed_type = node_type
