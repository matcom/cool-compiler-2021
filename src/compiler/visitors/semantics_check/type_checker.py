from ...cmp.ast import (
    BinaryNode,
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    FuncDeclarationNode,
    AssignNode,
    CallNode,
    CaseNode,
    BlockNode,
    LoopNode,
    ConditionalNode,
    LetNode,
    ArithmeticNode,
    ComparisonNode,
    EqualNode,
    VoidNode,
    NotNode,
    NegNode,
    ConstantNumNode,
    ConstantStringNode,
    ConstantBoolNode,
    VariableNode,
    InstantiateNode,
)
from ...cmp.semantic import (
    Context,
    InferencerManager,
    Method,
    Scope,
    SemanticError,
    ErrorType,
    SelfType,
    AutoType,
    LCA,
    Type,
)
from ..utils import *
from typing import List, Optional, Tuple

import compiler.visitors.visitor as visitor


class TypeChecker:
    def __init__(self, context, manager):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.errors: List[Tuple[Exception, Tuple[int, int]]] = []
        self.manager: InferencerManager = manager

        # built-in types
        self.obj_type = self.context.get_type("Object")
        self.int_type = self.context.get_type("Int")
        self.bool_type = self.context.get_type("Bool")
        self.string_type = self.context.get_type("String")

    @visitor.on("node")
    def visit(self, node, scope=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Optional[Scope] = None) -> Scope:
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable("self", SelfType(self.current_type))
        attributes = self.current_type.all_attributes()
        for values in attributes:
            attr, _ = values
            scope.define_variable(attr.name, attr.type, attr.idx)

        for feature in node.features:
            self.visit(feature, scope.create_child())

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):
        var = scope.find_variable(node.id)
        attr_type = var.type

        if node.expr is not None:
            computed_type = self.visit(node.expr, scope)
            if not self.check_conformance(computed_type, attr_type):
                self.errors.append(
                    (
                        TypeError(INCOMPATIBLE_TYPES % (computed_type.name, node.type)),
                        node.token.pos,
                    )
                )

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.id)

        # checking overwriting
        try:
            method = self.current_type.parent.get_method(node.id)
            if not len(self.current_method.param_types) == len(method.param_types):
                self.errors.append(
                    (
                        SemanticError(
                            WRONG_SIGNATURE % (node.id, self.current_type.name)
                        ),
                        node.token.pos,
                    )
                )
            else:
                for i, t in enumerate(self.current_method.param_types):
                    if not method.param_types[i] == t:
                        self.errors.append(
                            (
                                SemanticError(
                                    WRONG_SIGNATURE % (node.id, self.current_type.name)
                                ),
                                node.token.pos,
                            )
                        )
                        break
                else:
                    if not self.current_method.return_type == method.return_type:
                        self.errors.append(
                            (
                                SemanticError(
                                    WRONG_SIGNATURE % (node.id, self.current_type.name)
                                ),
                                node.typeToken.pos,
                            )
                        )
        except SemanticError:
            pass

        # defining variables in new scope
        for i, var in enumerate(self.current_method.param_names):
            if scope.is_local(var):
                self.errors.append(
                    (
                        SemanticError(
                            LOCAL_ALREADY_DEFINED % (var, self.current_method.name)
                        ),
                        node.token.pos,
                    )
                )
            else:
                scope.define_variable(
                    var,
                    self.current_method.param_types[i],
                    self.current_method.param_idx[i],
                )

        computed_type = self.visit(node.body, scope)

        # checking return type
        rtype = self.current_method.return_type
        if not self.check_conformance(computed_type, rtype):
            self.errors.append(
                (
                    TypeError(
                        INCOMPATIBLE_TYPES
                        % (computed_type.name, self.current_method.return_type.name)
                    ),
                    node.typeToken.pos,
                )
            )

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope) -> Type:
        if node.id == "self":
            self.errors.append((SemanticError(SELF_IS_READONLY), node.idToken.pos))

        # checking variable is defined
        var = scope.find_variable(node.id)
        if var is None:
            self.errors.append(
                (
                    NameError(VARIABLE_NOT_DEFINED % (node.id, self.current_type.name)),
                    node.idToken.pos,
                )
            )
            var = scope.define_variable(node.id, ErrorType())

        computed_type = self.visit(node.expr, scope.create_child())

        if not self.check_conformance(computed_type, var.type):
            self.errors.append(
                (
                    TypeError(INCOMPATIBLE_TYPES % (computed_type.name, var.type.name)),
                    node.token.pos,
                )
            )
        node.computed_type = computed_type
        return computed_type

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        # Evaluate object
        obj_type = self.visit(node.obj, scope)

        # Check object type conforms to cast type
        cast_type = obj_type
        if not node.type == "":
            try:
                cast_type = self.context.get_type(node.type)
                if isinstance(cast_type, AutoType):
                    raise SemanticError(AUTOTYPE_ERROR)
                if isinstance(cast_type, SelfType):
                    cast_type = SelfType(self.current_type)
            except (SemanticError, TypeError) as ex:
                cast_type = ErrorType()
                self.errors.append((ex, node.typeToken.pos))
        if not self.check_conformance(obj_type, cast_type):
            self.errors.append(
                (
                    TypeError(INCOMPATIBLE_TYPES % (obj_type.name, cast_type.name)),
                    node.typeToken.pos,
                )
            )

        # if the obj that is calling the function is autotype, let it pass
        if isinstance(cast_type, AutoType):
            node.computed_type = cast_type
            return cast_type

        if isinstance(cast_type, SelfType):
            cast_type = self.current_type

        # Check this function is defined for cast_type
        try:
            method = cast_type.get_method(node.id)
            # Check equal number of parameters
            if not len(node.args) == len(method.param_types):
                self.errors.append(
                    (
                        SemanticError(
                            INVALID_OPERATION % (method.name, cast_type.name)
                        ),
                        node.token.pos,
                    )
                )
                node.computed_type = ErrorType()
                return node.computed_type

            # Check conformance to parameter types
            for i, arg in enumerate(node.args):
                computed_type = self.visit(arg, scope)
                if not self.check_conformance(computed_type, method.param_types[i]):
                    self.errors.append(
                        (
                            TypeError(
                                INCOMPATIBLE_TYPES
                                % (computed_type.name, method.param_types[i].name)
                            ),
                            node.token.pos,
                        )
                    )

            # check self_type
            rtype = method.return_type
            if isinstance(rtype, SelfType):
                rtype = obj_type
            node.computed_type = rtype
            return rtype

        except SemanticError:
            self.errors.append(
                (
                    AttributeError(METHOD_NOT_DEFINED % (node.id)),
                    node.token.pos,
                )
            )
            node.computed_type = ErrorType()
            return node.computed_type

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        # check expression
        self.visit(node.expr, scope)

        nscope = scope.create_child()

        # check branches
        types = []
        node.branch_idx = []
        decTypes = set()
        size = 0
        for branch in node.branch_list:
            node.branch_idx.append(None)

            # check idx is not self
            if branch.id == "self":
                self.errors.append(
                    (SemanticError(SELF_IS_READONLY), branch.idToken.pos)
                )

            # check no branch repeats type
            decTypes.add(branch.typex)
            if size == len(decTypes):
                self.errors.append(
                    (
                        SemanticError(CASE_BRANCH_ERROR % (branch.typex)),
                        branch.typexToken.pos,
                    )
                )
            size += 1

            try:
                var_type = self.context.get_type(branch.typex)
                if isinstance(var_type, SelfType):
                    var_type = SelfType(self.current_type)
            except TypeError as ex:
                self.errors.append((ex, branch.typexToken.pos))
                var_type = ErrorType()

            # check type is autotype and assign an id in the manager
            if isinstance(var_type, AutoType):
                node.branch_idx[-1] = self.manager.assign_id(self.obj_type)

            new_scope = nscope.create_child()
            new_scope.define_variable(branch.id, var_type, node.branch_idx[-1])

            computed_type = self.visit(branch.expression, new_scope)
            types.append(computed_type)

        node.computed_type = LCA(types)
        return node.computed_type

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        nscope = scope.create_child()

        # Check expressions
        computed_type = None
        for expr in node.expr_list:
            computed_type = self.visit(expr, nscope)

        # return the type of the last expression of the list
        node.computed_type = computed_type
        return computed_type

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope: Scope):
        nscope = scope.create_child()

        # checking condition: it must conform to bool
        cond_type = self.visit(node.condition, nscope)
        if not cond_type.conforms_to(self.bool_type):
            self.errors.append(
                (
                    TypeError(
                        INCOMPATIBLE_TYPES % (cond_type.name, self.bool_type.name)
                    ),
                    node.token.pos,
                )
            )

        # checking body
        self.visit(node.body, nscope)

        node.computed_type = self.obj_type
        return node.computed_type

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):

        # check condition conforms to bool
        cond_type = self.visit(node.condition, scope)
        if not cond_type.conforms_to(self.bool_type):
            self.errors.append(
                (
                    TypeError(
                        INCOMPATIBLE_TYPES % (cond_type.name, self.bool_type.name)
                    ),
                    node.token.pos,
                )
            )

        then_type = self.visit(node.then_body, scope.create_child())
        else_type = self.visit(node.else_body, scope.create_child())

        node.computed_type = LCA([then_type, else_type])
        return node.computed_type

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        nscope = scope.create_child()

        node.idx_list = [None] * len(node.id_list)
        for i, item in enumerate(node.id_list):
            # create a new_scope for every variable defined
            new_scope = nscope.create_child()

            # check id in let can not be self
            if item.id == "self":
                self.errors.append((SemanticError(SELF_IS_READONLY), item.idToken.pos))
                item.id = f"1{item.id}"
                node.id_list[i] = (item.id, item.typex, item.expression)

            try:
                typex = self.context.get_type(item.typex)
                if isinstance(typex, SelfType):
                    typex = SelfType(self.current_type)
            except TypeError as ex:
                self.errors.append((ex, item.typexToken.pos))
                typex = ErrorType()

            if isinstance(typex, AutoType):
                node.idx_list[i] = self.manager.assign_id(self.obj_type)

            if item.expression is not None:
                expr_type = self.visit(item.expression, new_scope)
                if not self.check_conformance(expr_type, typex):
                    self.errors.append(
                        (
                            TypeError(
                                INCOMPATIBLE_TYPES % (expr_type.name, typex.name)
                            ),
                            item.token.pos,
                        )
                    )

            new_scope.define_variable(item.id, typex, node.idx_list[i])
            nscope = new_scope

        node.computed_type = self.visit(node.body, nscope)
        return node.computed_type

    @visitor.when(ArithmeticNode)
    def visit(self, node: ArithmeticNode, scope: Scope):
        self.check_expr(node, scope)
        node.computed_type = self.int_type
        return node.computed_type

    @visitor.when(ComparisonNode)
    def visit(self, node: ComparisonNode, scope: Scope):
        self.check_expr(node, scope)
        node.computed_type = self.bool_type
        return node.computed_type

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        types = [self.int_type, self.bool_type, self.string_type]

        def check_equal(typex, other):
            for t in types:
                if typex.conforms_to(t):
                    if not other.conforms_to(t):
                        self.errors.append(
                            (
                                TypeError(INCOMPATIBLE_TYPES % (other.name, t.name)),
                                node.token.pos,
                            )
                        )
                    return True
            return False

        ok = check_equal(left, right)
        if not ok:
            check_equal(right, left)

        node.computed_type = self.bool_type
        return node.computed_type

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode, scope: Scope):
        self.visit(node.expr, scope)

        node.computed_type = self.bool_type
        return node.computed_type

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        typex = self.visit(node.expr, scope)
        if not typex.conforms_to(self.bool_type):
            self.errors.append(
                (
                    TypeError(INCOMPATIBLE_TYPES % (typex.name, self.bool_type.name)),
                    node.token.pos,
                )
            )

        node.computed_type = self.bool_type
        return node.computed_type

    @visitor.when(NegNode)
    def visit(self, node: NegNode, scope: Scope):
        typex = self.visit(node.expr, scope)
        if not typex.conforms_to(self.int_type):
            self.errors.append(
                (
                    TypeError(INCOMPATIBLE_TYPES % (typex.name, self.int_type.name)),
                    node.token.pos,
                )
            )

        node.computed_type = self.int_type
        return node.computed_type

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        node.computed_type = self.int_type
        return node.computed_type

    @visitor.when(ConstantBoolNode)
    def visit(self, node, scope):
        node.computed_type = self.bool_type
        return node.computed_type

    @visitor.when(ConstantStringNode)
    def visit(self, node, scope):
        node.computed_type = self.string_type
        return node.computed_type

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        var = scope.find_variable(node.lex)
        if var is None:
            self.errors.append(
                (
                    NameError(
                        VARIABLE_NOT_DEFINED % (node.lex, self.current_type.name)
                    ),
                    node.token.pos,
                )
            )
            var = scope.define_variable(node.lex, ErrorType())

        node.computed_type = var.type
        return var.type

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope: Scope):
        try:
            typex = self.context.get_type(node.lex)
            if isinstance(typex, AutoType):
                raise SemanticError(AUTOTYPE_ERROR)
            if isinstance(typex, SelfType):
                typex = SelfType(self.current_type)
        except (SemanticError, TypeError) as ex:
            self.errors.append((ex, node.token.pos))
            typex = ErrorType()

        node.computed_type = typex
        return typex

    def check_expr(self, node: BinaryNode, scope: Scope):
        # checking left expr
        left = self.visit(node.left, scope)
        if not left.conforms_to(self.int_type):
            self.errors(
                (
                    TypeError(INCOMPATIBLE_TYPES % (left.name, self.int_type.name)),
                    node.token.pos,
                )
            )

        # checking right expr
        right = self.visit(node.right, scope)
        if not right.conforms_to(self.int_type):
            self.errors.append(
                (
                    TypeError(INCOMPATIBLE_TYPES % (right.name, self.int_type.name)),
                    node.token.pos,
                )
            )

    def check_conformance(self, computed_type, attr_type):
        return computed_type.conforms_to(attr_type) or (
            isinstance(computed_type, SelfType)
            and self.current_type.conforms_to(attr_type)
        )
