from __future__ import annotations

from coolcmp import errors as err
from coolcmp.utils import visitor
from coolcmp.utils.semantic import Context, Method, Type, SemanticError, ErrorType, VoidType, Scope
from coolcmp.utils.ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, BlockNode, \
    LetNode, CaseNode, AssignNode, ConditionalNode, WhileNode, CallNode, VariableNode, InstantiateNode, IntegerNode, \
    StringNode, BooleanNode, PlusNode, MinusNode, StarNode, DivNode, LessThanNode, LessEqualNode, EqualNode, \
    IsVoidNode, NegationNode, ComplementNode, BinaryNode, UnaryNode, CaseBranchNode, LetDeclarationNode, ParamNode


class TypeChecker:
    def __init__(self, context, errors):
        self.context: Context = context
        self.current_type: Type | None = None
        self.current_method: Method | None = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope = None):
        scope = Scope('Object')
        scope.define_variable('void', VoidType())

        for attr in self.context.get_type('Object').attributes:
            scope.define_variable(attr.name, attr.type, is_attr=True)

        pending = [(class_node.id, class_node) for class_node in node.declarations]
        scopes = {'Object': scope, 'IO': scope.create_child('IO')}

        while pending:

            actual = pending.pop(0)
            type_ = self.context.get_type(actual[0])

            if type_.parent.name != '<error>':
                try:
                    scopes[type_.name] = scopes[type_.parent.name].create_child(type_.name)
                    self.visit(actual[1], scopes[type_.name])
                except KeyError:  # Parent not visited yet
                    pending.append(actual)
            else:
                scopes[type_.name] = scope.create_child(type_.name)
                self.visit(actual[1], scopes[type_.name])

        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        # visit features
        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)
            elif isinstance(feature, FuncDeclarationNode):
                self.visit(feature, scope.create_child(feature.id))
            else:
                raise Exception(f'Invalid feature at class {node.id}')

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):
        # Check attribute override
        try:
            attr = self.current_type.parent.get_attribute(node.id, self.current_type.name)
            self.errors.append(err.ATTRIBUTE_DEFINED_IN_PARENT % (node.pos, attr.name))
        except SemanticError:
            pass

        if node.id == 'self':
            self.errors.append(err.SELF_INVALID_ID % (node.pos, ))

        try:
            attr_type = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError:
            attr_type = ErrorType()
            self.errors.append(err.UNDEFINED_TYPE % (node.type_pos, node.type))

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope)
            if not expr_type.conforms_to(attr_type):
                self.errors.append(err.INCOMPATIBLE_TYPES % (node.expr_pos, expr_type.name, attr_type.name))

        scope.define_variable(node.id, attr_type, is_attr=True)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.id)

        # Check method override
        try:
            method, method_owner = self.current_type.parent.get_method(node.id, get_owner=True)
            if method != self.current_method:
                self.errors.append(err.WRONG_SIGNATURE % (node.pos, node.id, method_owner.name))
        except SemanticError:
            pass

        scope.define_variable('self', self.current_type, is_param=True)

        for param_node in node.params:
            self.visit(param_node, scope)

        try:
            ret_type = self.context.get_type(node.return_type) if node.return_type != 'SELF_TYPE' else self.current_type
        except SemanticError:
            # this error is logged by type builder
            # self.errors.append(err.UNDEFINED_TYPE % (node.pos, node.return_type))
            ret_type = ErrorType()

        expr_type = self.visit(node.body, scope)
        if not expr_type.conforms_to(ret_type):
            self.errors.append(err.INCOMPATIBLE_TYPES % (node.pos, expr_type.name, ret_type.name))

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode, scope: Scope):
        if not scope.is_local(node.id):
            if node.type == 'SELF_TYPE':
                type_ = ErrorType()
                self.errors.append(err.SELF_TYPE_INVALID_PARAM_TYPE % (node.type_pos, ))
            else:
                try:
                    type_ = self.context.get_type(node.type)
                except SemanticError:
                    # this error is logged by the type builder
                    # self.errors.append(err.UNDEFINED_TYPE % (node.type_pos, node.type))
                    type_ = ErrorType()
            scope.define_variable(node.id, type_, is_param=True)
        else:
            self.errors.append(err.LOCAL_ALREADY_DEFINED % (node.pos, node.id, self.current_method.name))

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        ret_type = ErrorType()
        for expr in node.expressions:
            ret_type = self.visit(expr, scope)
        return ret_type

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = scope.create_child(tag='_let_node')
        for declaration in node.declarations:
            self.visit(declaration, child_scope)

        return self.visit(node.expr, child_scope)

    @visitor.when(LetDeclarationNode)
    def visit(self, node: LetDeclarationNode, scope: Scope):
        try:
            type_ = self.context.get_type(node.type) if node.type != 'SELF_TYPE' else self.current_type
        except SemanticError:
            self.errors.append(err.UNDEFINED_TYPE % (node.type_pos, node.type))
            type_ = ErrorType()

        if node.id == 'self':
            self.errors.append(err.SELF_INVALID_ID % (node.pos, ))
        else:
            scope.define_variable(node.id, type_)

        expr_type: Type = self.visit(node.expr, scope) if node.expr is not None else None
        if expr_type is not None and not expr_type.conforms_to(type_):
            self.errors.append(err.INCOMPATIBLE_TYPES % (node.expr_pos, expr_type.name, type_.name))

        return type_

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        self.visit(node.expr, scope)

        case_types = []
        reported_types = []
        for case_node in node.cases:
            type_ = case_node.type
            if type_ in case_types:
                if type_ not in reported_types:
                    self.errors.append(err.CASE_DUPLICATED_BRANCH % (case_node.type_pos, type_))
                    reported_types.append(case_node.type)
            else:
                case_types.append(type_)

        types = [
            self.visit(case, scope)
            for case in node.cases
        ]

        ret_type = types[0]
        for type_ in types[1:]:
            ret_type = ret_type.join(type_)

        return ret_type

    @visitor.when(CaseBranchNode)
    def visit(self, node: CaseBranchNode, scope: Scope):
        child_scope = scope.create_child('_case_branch')
        try:
            id_type = self.context.get_type(node.type)
        except SemanticError:
            self.errors.append(err.UNDEFINED_TYPE % (node.type_pos, node.type))
            id_type = ErrorType()

        if node.id == 'self':
            self.errors.append(err.SELF_INVALID_ID % (node.pos, ))
        else:
            child_scope.define_variable(node.id, id_type)

        return self.visit(node.expr, child_scope)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        if node.id == 'self':
            self.errors.append(err.SELF_IS_READONLY % (node.pos, ))

        var = scope.find_variable(node.id)
        expr_type = self.visit(node.expr, scope)
        if var is None:
            self.errors.append(err.VARIABLE_NOT_DEFINED % (node.pos, node.id, self.current_method.name))
        else:
            if not expr_type.conforms_to(var.type):
                self.errors.append(err.INCOMPATIBLE_TYPES % (expr_type.name, var.type.name))
        return expr_type

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        if_type = self.visit(node.if_expr, scope)
        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)

        if if_type != self.context.get_type('Bool'):
            self.errors.append(err.INCOMPATIBLE_TYPES % (node.pos, if_type.name, 'Bool'))

        return then_type.join(else_type)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond_type = self.visit(node.condition, scope)
        if cond_type != self.context.get_type('Bool'):
            self.errors.append(err.INCOMPATIBLE_TYPES % (node.pos, cond_type.name, 'Bool'))

        self.visit(node.body, scope)

        return self.context.get_type('Object')

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        if node.obj is None:
            obj_type = self.current_type
        else:
            obj_type = self.visit(node.obj, scope)

        try:
            _, owner = obj_type.get_method(node.id, get_owner=True)
            node.update_obj_dynamic_type(owner.name)
        except SemanticError:
            pass

        if node.type is not None:
            try:
                anc_type = self.context.get_type(node.type)
            except SemanticError:
                anc_type = ErrorType()
                self.errors.append(err.UNDEFINED_TYPE % (node.parent_pos, node.type))
            if not obj_type.conforms_to(anc_type):
                self.errors.append(err.INVALID_ANCESTOR % (node.pos, obj_type.name, anc_type.name))
        else:
            anc_type = obj_type

        try:
            method = anc_type.get_method(node.id)
        except SemanticError:
            self.errors.append(err.UNDEFINED_METHOD % (node.pos, node.id, anc_type.name))
            for arg in node.args:
                self.visit(arg, scope)
            return ErrorType()

        if len(node.args) != len(method.param_names):
            self.errors.append(err.WRONG_SIGNATURE % (node.pos, method.name, obj_type.name))
        else:
            for i, arg in enumerate(node.args):
                arg_type = self.visit(arg, scope)
                if not arg_type.conforms_to(method.param_types[i]):
                    self.errors.append(err.INCOMPATIBLE_TYPES % (arg.pos, arg_type.name, method.param_types[i].name))

        return method.return_type if method.return_type.name != 'SELF_TYPE' else anc_type

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        var = scope.find_variable(node.lex)
        if var is None:
            self.errors.append(err.VARIABLE_NOT_DEFINED % (node.pos, node.lex, self.current_method.name))
            return ErrorType()
        return var.type

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, _: Scope):
        try:
            return self.context.get_type(node.lex) if node.lex != 'SELF_TYPE' else self.current_type
        except SemanticError:
            self.errors.append(err.UNDEFINED_TYPE % (node.pos, node.lex))
            return ErrorType()

    @visitor.when(IntegerNode)
    def visit(self, _: IntegerNode, __: Scope):
        return self.context.get_type('Int')

    @visitor.when(StringNode)
    def visit(self, _: StringNode, __: Scope):
        return self.context.get_type('String')

    @visitor.when(BooleanNode)
    def visit(self, _: BooleanNode, __: Scope):
        return self.context.get_type('Bool')

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        ret_type = self.context.get_type('Int')
        return self._check_binary_node(node, scope, '+', ret_type)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        ret_type = self.context.get_type('Int')
        return self._check_binary_node(node, scope, '-', ret_type)

    @visitor.when(StarNode)
    def visit(self, node: StarNode, scope: Scope):
        ret_type = self.context.get_type('Int')
        return self._check_binary_node(node, scope, '*', ret_type)

    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: Scope):
        ret_type = self.context.get_type('Int')
        return self._check_binary_node(node, scope, '/', ret_type)

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode, scope: Scope):
        ret_type = self.context.get_type('Bool')
        return self._check_binary_node(node, scope, '<', ret_type)

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode, scope: Scope):
        ret_type = self.context.get_type('Bool')
        return self._check_binary_node(node, scope, '<=', ret_type)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        basic_types = ('Int', 'String', 'Bool')

        if left_type.name in basic_types or right_type.name in basic_types:
            if left_type.name != right_type.name:
                self.errors.append(err.INCOMPATIBLE_TYPES % (node.pos, left_type.name, right_type.name))

        return self.context.get_type('Bool')

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        self.visit(node.expr, scope)
        return self.context.get_type('Bool')

    @visitor.when(NegationNode)
    def visit(self, node: NegationNode, scope: Scope):
        return self._check_unary_node(node, scope, 'not', self.context.get_type('Bool'))

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode, scope: Scope):
        return self._check_unary_node(node, scope, '~', self.context.get_type('Int'))

    def _check_binary_node(self, node: BinaryNode, scope: Scope, oper: str, ret_type: Type):
        int_type = self.context.get_type('Int')
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if left_type == right_type == int_type:
            return ret_type
        else:
            self.errors.append(err.INVALID_BINARY_OPERATOR % (node.pos, oper, left_type.name, right_type.name))
            return ErrorType()

    def _check_unary_node(self, node: UnaryNode, scope: Scope, oper: str, expected_type: Type):
        type_ = self.visit(node.expr, scope)
        if type_ == expected_type:
            return type_
        else:
            self.errors.append(err.INVALID_UNARY_OPERATOR % (node.pos, oper, type_.name))
            return ErrorType()
