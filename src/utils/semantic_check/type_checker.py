import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError, ErrorType, Scope

MAIN_DONT_EXISTS = '(0, 0) - TypeError: COOL program must have a class Main'
MAIN_METHOD_DONT_EXISTS = '(%s, %s) - TypeError: Main class must have a method main()'
MAIN_METHOD_DONT_HAVE_PARAMS = '(%s, %s) - TypeError: main method must not have params'

SELF_ERROR_ATTR = '(%s, %s) - SemanticError: \'self\' cannot be the name of an attribute.'
SELF_ERROR_LET = '(%s, %s) - SemanticError: \'self\' cannot be bound in a \'let\' expression.'
SELF_IS_READONLY = '(%s, %s) - SemanticError: Variable "self" is read-only.'
SELF_TYPE_ERROR = '(%s, %s) - TypeError: SELF_TYPE cannot be used as a parameter type in method %s'
SELF_TYPE_IN_DISPATCH = '(%s, %s) - TypeError: SELF_TYPE cannot be used as a type of a dispatch'
SELF_TYPE_IN_CASE_BRANCH = '(%s, %s) - TypeError: SELF_TYPE cannot be used as a type of a case branch'

INCOMPATIBLE_TYPES_ATTR = '(%s, %s) - TypeError: Inferred type %s of initialization of attribute %s does not conform to declared type %s.'
INCOMPATIBLE_TYPES_ARG = '(%s, %s) - TypeError: Argument of \'%s\' has type %s instead of %s.'
INCOMPATIBLE_TYPES_METH = '(%s, %s) - TypeError: Inferred return type %s of method %s does not conform to declared return type %s.'
INCOMPATIBLE_TYPES_IF = '(%s, %s) - TypeError: Predicate of \'%s\' does not have type %s.'
INCOMPATIBLE_TYPES_LET = '(%s, %s) - TypeError: Inferred type %s of initialization of %s does not conform to identifier\'s declared type %s.'
INCOMPATIBLE_TYPES_CALL = '(%s, %s) - TypeError: Expression type %s does not conform to declared static dispatch type %s.'
INCOMPATIBLE_TYPES = '(%s, %s) - TypeError: Cannot convert %s into %s.'

WRONG_SIGNATURE = '(%s, %s) - SemanticError: Incompatible number of formal parameters in redefined method %s.'
LOCAL_ALREADY_DEFINED = '(%s, %s) - SemanticError: Variable %s is already defined in method %s.'
INVALID_OPERATION = '(%s, %s) - TypeError: non-Int arguments: %s %s %s'
VARIABLE_NOT_DEFINED = '(%s, %s) - NameError: Undeclared identifier %s.'
INHERIT_ERROR = '(%s, %s) - SemanticError: Class %s, or an ancestor of %s, is involved in an inheritance cycle.'
METHOD_PARAMETERS = '(%s, %s) - SemanticError: Method %s defined in %s receive %d parameters'

DUPLICATE_BRANCH = '(%s, %s) - SemanticError: Duplicate branch %s in case statement.'
UNDEFINED_TYPE_BRANCH = '(%s, %s) - TypeError: Class %s of case branch is undefined.'
UNDEFINED_TYPE_NEW = '(%s, %s) - TypeError: \'new\' used with undefined class %s.'
UNDEFINED_TYPE_LET = '(%s, %s) - TypeError: Class %s of let-bound identifier %s is undefined.'
UNDEFINED_METHOD = '(%s, %s) - AttributeError: Dispatch to undefined method %s. '


class TypeChecker:
    def __init__(self, context, errors):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(nodes.ProgramNode)
    def visit(self, node, scope=None):
        # verificando que el programa tenga una clase Main
        try:
            self.context.get_type('Main')

        except SemanticError:
            self.errors.append(MAIN_DONT_EXISTS)

        scope = Scope() if scope == None else scope

        for dec in node.declarations:
            self.visit(dec, scope.create_child())

        return scope

    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable('self', self.current_type)

        # verificando la existencia del metodo main
        if self.current_type.name == 'Main':
            try:
                self.current_type.get_method('main')

            except SemanticError:
                self.errors.append(MAIN_METHOD_DONT_EXISTS %
                                   (node.line, node.column))

        # verficando herencia circular en los ancestros de current_type (deben llegar a object sin pasar por el nuevamente)
        current_parent = self.current_type.parent

        while current_parent != self.context.get_type('Object') and current_parent != None:
            if current_parent == self.current_type:
                self.errors.append(INHERIT_ERROR % (self.current_type.child.line, self.current_type.child.column,
                                   self.current_type.child.name, self.current_type.child.name))
                self.current_type.parent = ErrorType()
                break

            for attr in current_parent.attributes:
                scope.define_variable(attr.name, attr.type)

            current_parent = current_parent.parent

        attrs = [feat for feat in node.features if isinstance(
            feat, nodes.AttrDeclarationNode)]
        for attr in attrs:
            self.visit(attr, scope)

        meths = [feat for feat in node.features if isinstance(
            feat, nodes.MethDeclarationNode)]
        for meth in meths:
            self.visit(meth, scope.create_child())

        return

    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self, node, scope):
        try:
            attr_type = self.context.get_type(
                node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError:
            attr_type = ErrorType()

        if node.id == 'self':
            self.errors.append(SELF_ERROR_ATTR % (node.line, node.column))

        if node.expr:
            type_expr = self.visit(node.expr, scope.create_child())

            if not type_expr.conforms_to(attr_type):
                self.errors.append(INCOMPATIBLE_TYPES_ATTR % (
                    node.line, node.column, type_expr.name, node.id, attr_type.name))

        scope.define_variable(node.id, attr_type)

        return

    @visitor.when(nodes.MethDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)

        # verificando que el metodo main no tenga parametros
        if self.current_method.name == 'main' and self.current_method.param_names:
            self.errors.append(MAIN_METHOD_DONT_HAVE_PARAMS %
                               (node.line, node.column))

        # verificabdo redefinicion de metodos
        current_parent = self.current_type.parent

        while current_parent != self.context.get_type('Object') and current_parent != None:
            try:
                parent_method = current_parent.get_method(node.id)
                if parent_method != self.current_method:
                    self.errors.append(WRONG_SIGNATURE % (
                        node.line, node.column, self.current_method.name))
                    break
            except:
                pass
            current_parent = current_parent.parent

        scope.define_variable('self', self.current_type)

        for name, typex in zip(self.current_method.param_names, self.current_method.param_types):
            if scope.is_local(name):
                self.errors.append(LOCAL_ALREADY_DEFINED % (
                    node.line, node.column, name, self.current_method.name))

            elif typex == 'SELF_TYPE':
                self.errors.append(SELF_TYPE_ERROR % (
                    node.line, node.column, self.current_method.name))
                scope.define_variable(name, ErrorType())

            else:
                scope.define_variable(name, self.context.get_type(typex.name))

        body_type = self.visit(node.body, scope)
        try:
            returnType = self.context.get_type(
                node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError as se:
            returnType = ErrorType()

        if not body_type.conforms_to(returnType):
            self.errors.append(INCOMPATIBLE_TYPES_METH % (
                node.body_line, node.body_column, body_type.name, node.id, returnType.name))

        return

    @visitor.when(nodes.AssignNode)
    def visit(self, node, scope):
        var = scope.find_variable(node.id)

        type_expr = self.visit(node.expr, scope.create_child())

        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED %
                               (node.line, node.column, node.id))

        elif var.name == 'self':
            self.errors.append(SELF_IS_READONLY % (node.line, node.column))

        elif not type_expr.conforms_to(var.type):
            self.errors.append(INCOMPATIBLE_TYPES % (
                node.line, node.column, type_expr.name, var.type.name))

        return type_expr

    @visitor.when(nodes.CallNode)
    def visit(self, node, scope):
        if node.obj is None:
            obj_type = self.current_type
        else:
            obj_type = self.visit(node.obj, scope)
            node.obj.computed_type = obj_type

        if node.type is not None:
            if node.type == 'SELF_TYPE':
                self.errors.append(SELF_TYPE_IN_DISPATCH %
                                   (node.line, node.column))
                typex = ErrorType()

            else:
                try:
                    typex = self.context.get_type(node.type)
                except SemanticError as se:
                    self.errors.append(se.text)
                    typex = ErrorType()

                if not obj_type.conforms_to(typex):
                    self.errors.append(INCOMPATIBLE_TYPES_CALL % (
                        node.line, node.column, obj_type.name, typex.name))

            obj_type = typex

        try:
            meth = obj_type.get_method(node.id)
        except SemanticError as se:
            if se.text:
                self.errors.append(UNDEFINED_METHOD %
                                   (node.line, node.column, node.id))
            for arg in node.args:
                self.visit(arg, scope)
            return ErrorType()

        if len(node.args) != len(meth.param_names):
            self.errors.append(METHOD_PARAMETERS % (
                node.line, node.column, meth.name, obj_type.name, len(meth.param_names)))

        for i, arg in enumerate(node.args):
            type_arg = self.visit(arg, scope)
            if i < len(meth.param_types) and not type_arg.conforms_to(meth.param_types[i]):
                self.errors.append(INCOMPATIBLE_TYPES % (
                    node.line, node.column, type_arg.name, meth.param_types[i].name))

        return meth.return_type if meth.return_type.name != 'SELF_TYPE' else obj_type

    @visitor.when(nodes.IfThenElseNode)
    def visit(self, node, scope):
        if_type = self.visit(node.if_expr, scope.create_child())

        if not if_type.conforms_to(self.context.get_type('Bool')):
            self.errors.append(INCOMPATIBLE_TYPES_IF %
                               (node.line, node.column, 'if', 'Bool'))

        then_type = self.visit(node.then_expr, scope.create_child())
        else_type = self.visit(node.else_expr, scope.create_child())

        return then_type.join(else_type)

    @visitor.when(nodes.WhileNode)
    def visit(self, node, scope):
        type_conditional = self.visit(node.conditional_expr, scope)

        if not type_conditional.conforms_to(self.context.get_type('Bool')):
            self.errors.append(INCOMPATIBLE_TYPES % (
                node.line, node.column, type_conditional.name, 'Bool'))

        self.visit(node.loop_expr, scope.create_child())

        return self.context.get_type('Object')

    @visitor.when(nodes.BlockNode)
    def visit(self, node, scope):
        type_expr = ErrorType()

        for expr in node.expr_list:
            type_expr = self.visit(expr, scope.create_child())

        return type_expr

    @visitor.when(nodes.LetNode)
    def visit(self, node, scope):
        for idx, typex, id_expr in node.identifiers:
            try:
                id_type = self.context.get_type(
                    typex) if typex != 'SELF_TYPE' else self.current_type
            except SemanticError as se:
                id_type = ErrorType()
                self.errors.append(UNDEFINED_TYPE_LET %
                                   (node.line, node.column, typex, idx))

            if idx == 'self':
                self.errors.append(SELF_ERROR_LET % (node.line, node.column))

            if scope.is_local(idx):
                scope = scope.create_child()
                scope.define_variable(idx, id_type)
            else:
                scope.define_variable(idx, id_type)

            if id_expr is not None:
                id_expr_type = self.visit(id_expr, scope.create_child())
                if not id_expr_type.conforms_to(id_type):
                    self.errors.append(INCOMPATIBLE_TYPES_LET % (
                        node.line, node.column, id_expr_type.name, idx, id_type.name))

        body_type = self.visit(node.in_expr, scope.create_child())

        return body_type

    @visitor.when(nodes.CaseNode)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        case_type = None

        for i, branch in enumerate(node.branches):
            (idx, typex, expr) = branch
            (line, column) = node.branchesPos[i]
            if typex in [b[1] for b in node.branches[:i]]:
                self.errors.append(DUPLICATE_BRANCH % (line, column, typex))
            if typex == 'SELF_TYPE':
                self.errors.append(SELF_TYPE_IN_CASE_BRANCH % (line, column))
                id_type = ErrorType()

            else:
                try:
                    id_type = self.context.get_type(typex)
                except SemanticError as se:
                    id_type = ErrorType()
                    self.errors.append(UNDEFINED_TYPE_BRANCH %
                                       (line, column, typex))

            inner_scope = scope.create_child()
            inner_scope.define_variable(idx, id_type)

            type_expr = self.visit(expr, inner_scope)
            case_type = case_type.join(
                type_expr) if case_type is not None else type_expr

        return case_type

    @visitor.when(nodes.NotNode)
    def visit(self, node, scope):
        typex = self.visit(node.expr, scope)

        if not typex.conforms_to(self.context.get_type('Bool')):
            self.errors.append(INCOMPATIBLE_TYPES_ARG % (
                node.line, node.column, 'not', typex.name, 'Bool'))
            return ErrorType()

        return typex

    @visitor.when(nodes.ConstantNumNode)
    def visit(self, node, scope):
        return self.context.get_type('Int')

    @visitor.when(nodes.ConstantBoolNode)
    def visit(self, node, scope):
        return self.context.get_type('Bool')

    @visitor.when(nodes.ConstantStringNode)
    def visit(self, node, scope):
        return self.context.get_type('String')

    @visitor.when(nodes.VariableNode)
    def visit(self, node, scope):
        var = scope.find_variable(node.lex)

        if var is None:
            self.errors.append(VARIABLE_NOT_DEFINED %
                               (node.line, node.column, node.lex))
            return ErrorType()

        return var.type

    @visitor.when(nodes.InstantiateNode)
    def visit(self, node, scope):
        if node.lex == 'SELF_TYPE':
            return self.current_type

        try:
            return self.context.get_type(node.lex)
        except SemanticError as se:
            self.errors.append(UNDEFINED_TYPE_NEW %
                               (node.line, node.column, node.lex))
            return ErrorType()

    @visitor.when(nodes.IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.lex, scope)
        return self.context.get_type('Bool')

    @visitor.when(nodes.ComplementNode)
    def visit(self, node, scope):
        typex = self.visit(node.lex, scope)

        if not typex.conforms_to(self.context.get_type('Int')):
            self.errors.append(INCOMPATIBLE_TYPES_ARG % (
                node.line, node.column, '~', typex.name, 'Int'))
            return ErrorType()

        return typex

    @visitor.when(nodes.PlusNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '+', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Int')

    @visitor.when(nodes.MinusNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '-', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Int')

    @visitor.when(nodes.StarNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '*', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Int')

    @visitor.when(nodes.DivNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '/', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Int')

    @visitor.when(nodes.LessThanNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '<', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Bool')

    @visitor.when(nodes.LessEqualNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        if not type_left.conforms_to(self.context.get_type('Int')) or not type_right.conforms_to(self.context.get_type('Int')):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '<=', type_right.name))
            return ErrorType()

        else:
            return self.context.get_type('Bool')

    @visitor.when(nodes.EqualNode)
    def visit(self, node, scope):
        type_left = self.visit(node.left, scope)
        type_right = self.visit(node.right, scope)

        int_type = self.context.get_type('Int')
        bool_type = self.context.get_type('Bool')
        string_type = self.context.get_type('String')

        if type_left.name == 'AUTO_TYPE' or type_right.name == 'AUTO_TYPE':
            pass
        elif (type_left == int_type and not type_right.conforms_to(int_type)) or (type_right == int_type and not type_left.conforms_to(int_type)) or (type_left == bool_type and not type_right.conforms_to(bool_type)) or (type_right == bool_type and not type_left.conforms_to(bool_type)) or (type_left == string_type and not type_right.conforms_to(string_type)) or (type_right == string_type and not type_left.conforms_to(string_type)):
            self.errors.append(INVALID_OPERATION % (
                node.line, node.column, type_left.name, '=', type_right.name))
            return ErrorType()

        return bool_type
