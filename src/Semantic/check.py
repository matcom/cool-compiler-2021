import Utils.visitor as visitor

from Parser.ast import *
from Utils.scope import Scope
from Utils.context import ErrorType
from Utils.errors import MethodException, TypeException, TypeErrors, SemanticErrors, NameErrors, AttributeErrors

class TypeCheck:
    def __init__(self, context, errors):
        self.errors = errors
        self.context = context
        
        self.scope_class = {}
        self.basic_type = {
            'int' : self.context.get_type('Int'),
            'bool' : self.context.get_type('Bool'),
            'string' : self.context.get_type('String')}
        self.object_type = self.context.get_type('Object')

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()

        for def_class in node.class_list:
            self.visit(def_class, scope.create_child())
        return scope

    @visitor.when(ClassNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.type.value)
        self.scope_class[node.type.value] = scope
        scope.define_variable('self', self.current_type)
        
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)
            
        for feature in node.feature_list:
            self.visit(feature, scope)  

    @visitor.when(AttributeNode)
    def visit(self, node, scope):
        if node.id.value == 'self':
            self.errors.append(SemanticErrors(node.id.line, node.id.column, f'\'self\' cannot be the name of an attribute.'))
        
        if node.expr:
            self.visit(node.expr, scope)

            expr_type = node.expr.computed_type
            attr_type = self.current_type.get_attribute(node.id.value).type

            if not expr_type.conforms_to(attr_type):
                self.errors.append(TypeErrors(node.expr.line, node.expr.column, f'Inferred type {expr_type.name} of initialization of attribute {node.id.value} does not conform to declared type {attr_type.name}.'))
    
    @visitor.when(MethodNode)
    def visit(self, node, scope):
        scope = scope.create_child()

        self.current_method = self.current_type.get_method(node.id.value)

        for pname, ptype in zip(self.current_method.param_names, self.current_method.param_types):
            scope.define_variable(pname, ptype)

        self.visit(node.expr, scope)
        expression_line = node.expr.line
        expression_column = node.expr.column
        expression_type = node.expr.computed_type
        
        return_type = self.current_method.return_type

        if not expression_type.conforms_to(return_type):
            self.errors.append(TypeErrors(expression_line, expression_column, f'Inferred return type {expression_type.name} of method {node.id.value} does not conform to declared return type {return_type.name}.'))

    @visitor.when(AssignmentNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        expression_type = node.expr.computed_type

        if scope.is_defined(node.id.value, self.scope_class, self.current_type):
            variable = scope.find_variable(node.id.value, self.scope_class, self.current_type)
            variable_type = variable.type

            if variable.name == 'self':
                self.errors.append(SemanticErrors(node.key.line, node.key.column, f'Cannot assign to \'self\'.'))
            
            if not expression_type.conforms_to(variable_type):
                self.errors.append('0, 0, Incompatible type')
        
        else:
            self.errors.append('0, 0, Variable no defined')
        
        node.line = node.id.line
        node.column = node.id.column
        node.computed_type = expression_type

    @visitor.when(DispatchNode)
    def visit(self, node, scope):
        if node.expr:
            self.visit(node.expr, scope)
            expression_type = node.expr.computed_type

            if node.type:
                try:
                    if expression_type.conforms_to(self.context.get_type(node.type.value)):
                        expression_type = self.context.get_type(node.type.value)
                    else:
                        self.errors.append(TypeErrors(node.expr.line, node.expr.column, f'Expression type {expression_type.name} does not conform to declared static dispatch type {node.type.value}.'))
                        expression_type = ErrorType()
                    
                except KeyError as error:
                    self.errors.append(SemanticErrors(node.type.line, node.type.column, error))
            
            node.line = node.expr.line
            node.column = node.expr.column
        else:
            expression_type = self.current_type
            node.line = node.id.line
            node.column = node.id.column

        try:
            method = expression_type.get_method(node.id.value)

            if len(node.args) == len(method.param_types):
                for argument, tname, ttype in zip(node.args, method.param_names, method.param_types):
                    self.visit(argument, scope)
                    argument_type = argument.computed_type

                    if not argument_type.conforms_to(ttype):
                        self.errors.append(TypeErrors(argument.line, argument.column, f'In call of method {node.id.value}, type {argument_type.name} of parameter {tname} does not conform to declared type {ttype.name}.'))
            else:
                self.errors.append(SemanticErrors(node.id.line, node.id.column, f'Method {node.id.value} called with wrong number of arguments.'))
            
            node_type = method.return_type
        except MethodException:
            self.errors.append(AttributeErrors(node.id.line, node.id.column, f'Dispatch to undefined method {node.id.value}.'))
            node_type = ErrorType()

        node.computed_type = node_type

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        self.visit(node.pred, scope)
        pred_type = node.pred.computed_type
        
        if not pred_type.conforms_to(self.basic_type['bool']):
            self.errors.append(TypeErrors(node.pred.line, node.pred.column, f'pred of \'if\' does not have type Bool.'))

        self.visit(node.then, scope)
        then_type = node.then.computed_type

        self.visit(node.neth, scope)
        else_type = node.neth.computed_type

        node.line = node.key.line 
        node.column = node.key.column
        node.computed_type = then_type.join_type(else_type)

    @visitor.when(LoopsNode)
    def visit(self, node, scope):
        self.visit(node.pred, scope)
        pred_type = node.pred.computed_type

        if not pred_type.conforms_to(self.basic_type['bool']):
            self.errors.append(TypeErrors(node.pred.line, node.pred.column, 'Loop condition does not have type Bool.'))

        self.visit(node.expr, scope)

        node.computed_type = self.object_type
        node.line = node.key.line
        node.column = node.key.column

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expression in node.exprs:
            self.visit(expression, scope)
        
        node.computed_type = node.exprs[-1].computed_type
        node.line = node.key.line
        node.column = node.key.column

    @visitor.when(LetNode)
    def visit(self, node, scope):
        scope = scope.create_child()
        for idd, ttype, expression in node.assigs:
            if idd.value == 'self':
                self.errors.append(SemanticErrors(idd.line, idd.column, f'\'self\' cannot be bound in a \'let\' expression.'))

            try:
                if ttype == 'SELF_TYPE':
                    attribute_type = self.current_type
                else:
                    attribute_type = self.context.get_type(ttype.value)
            except KeyError:
                self.errors.append(TypeErrors(ttype.line, ttype.column, f'Class {ttype.value} of let-bound identifier {idd.value} is undefined.'))
                attribute_type = ErrorType()
            
            if expression:
                self.visit(expression, scope)
                expression_type = expression.computed_type

                if not expression_type.conforms_to(attribute_type):
                    self.errors.append(TypeErrors(expression.line, expression.column, f'Inferred type {expression_type.name} of initialization of {idd.value} does not conform to identifier\'s declared type {ttype.value}. '))

            scope.define_variable(idd.value, attribute_type)

        self.visit(node.expr, scope)
        node.line = node.key.line
        node.column = node.key.column
        node.computed_type = node.expr.computed_type

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)

        node_type = None
        type_list = []

        for iid, ttype, expression in node.tests:
            new_scope = scope.create_child()

            if ttype == 'SELF_TYPE':
                self.errors.append('The variable in each branch cant be SELF_TYPE')
                variable_type = ErrorType()
            else:
                try:
                    variable_type = self.context.get_type(ttype.value)
                except KeyError:
                    self.errors.append(TypeErrors(ttype.line, ttype.column, f'Class {ttype.value} of case branch is undefined.'))

                if variable_type.name in type_list:
                    self.errors.append(SemanticErrors(ttype.line, ttype.column, f'Duplicate branch {ttype.value} in case statement.'))
                else:
                    type_list.append(variable_type.name)

            new_scope.define_variable(iid.value, variable_type)
            self.visit(expression, new_scope)
            variable_type = expression.computed_type

            if not node_type:
                node_type = variable_type
            else:
                node_type = node_type.join_type(variable_type)
        
        node.line = node.key.line
        node.computed_type = node_type
        node.column = node.key.column

    @visitor.when(NewNode)
    def visit(self, node, scope):
        if node.type.value == 'SELF_TYPE':
            node_type = self.current_type
        else:
            try:
                node_type = self.context.get_type(node.type.value)
            except KeyError:
                self.errors.append(TypeErrors(node.type.line, node.type.column, f'\'new\' used with undefined class {node.type.value}.'))
                node_type = ErrorType()

        node.line = node.key.line
        node.computed_type = node_type
        node.column = node.key.column

    @visitor.when(IsvoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        node.computed_type = self.basic_type['bool']
        node.line = node.key.line
        node.column = node.key.column
    
    @visitor.when(NegationNode)
    def visit(self, node, scope):
        self.visit(node.node, scope)
        
        node.line = node.node.line
        node.column = node.node.column
        node_type = node.node.computed_type

        if not node_type.conforms_to(self.basic_type['bool']):
            self.errors.append(TypeErrors(node.line, node.column, f'Argument of \'not\' has type {node_type.name} instead of Bool.'))

        node.computed_type = self.basic_type['bool']

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        self.visit(node.node, scope)
        node_type = node.node.computed_type

        if not node_type.conforms_to(self.basic_type['int']):
            self.errors.append(TypeErrors(node.node.line, node.node.column, f'Argument of \'~\' has type {node_type.name} instead of Int.'))

        node.computed_type = self.basic_type['int']

    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type

        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if not left_type.conforms_to(self.basic_type['int']) or not right_type.conforms_to(self.basic_type['int']):
            self.errors.append(TypeErrors(node.key.line, node.key.column, f'non-Int arguments: {left_type.name} {node.key.value} {right_type.name}'))
        if isinstance(node, (LessNode, LequalNode)):
            node_type = self.basic_type['bool']
        else:
            node_type = self.basic_type['int']
        
        node.line = node.left.line
        node.column = node.left.column
        node.computed_type = node_type

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        self.visit(node.left, scope)
        left_type = node.left.computed_type

        self.visit(node.right, scope)
        right_type = node.right.computed_type

        if (left_type in self.basic_type.values() or right_type in self.basic_type.values()) and not left_type == right_type:
            self.errors.append(TypeErrors(node.key.line, node.key.column, f'Illegal comparison with a basic type.'))

        node.computed_type = self.basic_type['bool']
        node.line = node.left.line
        node.column = node.left.column

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.line = node.lexer.line
        node.column = node.lexer.column
        node.computed_type = self.basic_type['int']

    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.line = node.lexer.line
        node.column = node.lexer.column 
        node.computed_type = self.context.get_type('String')

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.line = node.lexer.line
        node.column = node.lexer.column 
        node.computed_type = self.context.get_type('Bool')

    @visitor.when(IdentifierNode)
    def visit(self, node, scope):  
        if scope.is_defined(node.lexer.value, self.scope_class, self.current_type):
            variable = scope.find_variable(node.lexer.value, self.scope_class, self.current_type)
            node_type = variable.type
        else:
            self.errors.append(NameErrors(node.lexer.line, node.lexer.column , f'Undeclared identifier {node.lexer.value}.'))
            node_type = ErrorType()

        node.line = node.lexer.line
        node.computed_type = node_type
        node.column = node.lexer.column 