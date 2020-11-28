import src.cmp.nbpackage
import src.cmp.visitor as visitor

from src.ast_nodes import Node, ProgramNode, ExpressionNode
from src.ast_nodes import ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode
from src.ast_nodes import VarDeclarationNode, AssignNode, CallNode
from src.ast_nodes import (
    AtomicNode,
    BinaryNode,
    ArithmeticOperation,
    ComparisonOperation,
    IfNode,
    LetNode,
    CaseNode,
    CaseItemNode,
    WhileNode,
    BlockNode,
    IsvoidNode,
)
from src.ast_nodes import (
    ConstantNumNode,
    VariableNode,
    InstantiateNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    NegNode,
    NotNode,
    EqualNode,
    BooleanNode,
    StringNode,
)
from src.cool_visitor import FormatVisitor

from src.cmp.semantic import SemanticError
from src.cmp.semantic import Attribute, Method, Type
from src.cmp.semantic import VoidType, ErrorType, IntType
from src.cmp.semantic import Context

from src.cmp.semantic import Scope
from src.cmp.utils import find_least_type

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable("self", self.current_type)

        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)

        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        try:
            typex = self.context.get_type(node.type)

        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        if node.init_exp != None:
            init_expr_type = self.visit(node.init_exp, scope)
            if not init_expr_type.conforms_to(typex):
                self.errors.append(INCOMPATIBLE_TYPES % (init_expr_type, typex))

        return typex

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)

        child_scope = scope.create_child()

        for i in range(len(self.current_method.param_names)):
            child_scope.define_variable(
                self.current_method.param_names[i], self.current_method.param_types[i]
            )

        body_type = self.visit(node.body, child_scope)

        if not body_type.conforms_to(self.current_method.return_type):
            self.errors.append(
                INCOMPATIBLE_TYPES
                % (body_type.name, self.current_method.return_type.name)
            )

        if self.current_type.parent is not None:
            try:
                parent_method = self.current_type.parent.get_method(
                    self.current_method.name
                )
                if parent_method != self.current_method:
                    self.errors.append(WRONG_SIGNATURE % (parent_method.name, "parent"))
            except SemanticError:
                pass

        try:
            return_type = self.context.get_type(node.type)
            return return_type

        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        if scope.is_local(node.id):
            self.errors.append(
                LOCAL_ALREADY_DEFINED % (node.id, self.current_method.name)
            )
        elif node.id == "self":
            self.errors.append(SELF_IS_READONLY)
        try:
            static_type = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(error.text)
            static_type = ErrorType()

        expr_type = self.visit(node.expr, scope)
        if not expr_type.conforms_to(static_type):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, static_type.name))

        scope.define_variable(node.id, static_type)
        return static_type

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        if node.id == "self":
            self.errors.append(SELF_IS_READONLY)

        var_type = None
        if not scope.is_defined(node.id):
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.id, self.current_method.name)
            )
            var_type = ErrorType()
        else:
            var_type = scope.find_variable(node.id).type

        expr_type = self.visit(node.expr, scope)
        if not expr_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, var_type.name))

        return var_type

    @visitor.when(CallNode)
    def visit(self, node, scope):
        auto_type = self.context.get_type("AUTO_TYPE")
        typex = None
        if node.obj is not None:
            typex = self.visit(node.obj, scope)
            if typex == auto_type:
                return auto_type

        else:
            typex = self.current_type

        if typex == self.context.get_type("Void"):
            self.errors.append("Void type cannot dispatch")
            return ErrorType()

        method = None
        try:
            if node.at_type is not None:
                node_at_type = self.context.get_type(node.at_type)
                method = node_at_type.get_method(node.id)
                if not typex.conforms_to(node_at_type):
                    self.errors.append(
                        "The static type to the left of @ must conform to the type specified to the right of @ "
                    )
                    return ErrorType()
            else:
                method = typex.get_method(node.id)
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()

        if len(method.param_names) != len(node.args):
            self.errors.append(
                f"There is no definition of {method.name} that takes {len(node.args)} arguments "
            )

        for arg, ptype in zip(node.args, method.param_types):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(ptype):
                self.errors.append(INCOMPATIBLE_TYPES % (arg_type.name, ptype.name))

        if method.return_type == self.context.get_type("SELF_TYPE"):
            return typex

        return method.return_type

    @visitor.when(IfNode)
    def visit(self, node, scope):
        predicate_type = self.visit(node.if_expr, scope)

        if predicate_type.name != "Bool" and predicate_type.name != "AUTO_TYPE":
            self.errors.append("Expression must be bool")
            return ErrorType()

        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)

        least_type = find_least_type(then_type, else_type, self.context)
        return least_type

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        condition_type = self.visit(node.condition, scope)
        bool_type = self.context.get_type("Bool")

        if condition_type != bool_type:
            self.errors.append("Expression must be bool")
            return ErrorType()

        return self.context.get_type("Object")

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        typex = None
        for expr in node.expression_list:
            typex = self.visit(expr, scope)

        return typex

    @visitor.when(LetNode)
    def visit(self, node, scope):

        child_scope = scope.create_child()

        for var_dec in node.identifiers:
            self.visit(var_dec, child_scope)

        return self.visit(node.body, child_scope)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):

        static_type = None
        try:
            static_type = self.context.get_type(node.type)
            scope.define_variable(node.id, static_type)

        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        if node.expr != None:
            typex = self.visit(node.expr, scope)
            if not typex.conforms_to(static_type):
                self.errors.append(INCOMPATIBLE_TYPES % (typex, static_type))

        return static_type

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        # typex = self.visit(node.expr, scope)
        # if typex == self.context.get_type("Void"):
        #     self.errors.append("Case expression cannot be Void")
        #     return ErrorType()

        current_case_type = None
        for item in node.case_items:
            child_scope = scope.create_child()
            case_item_type = self.visit(item, child_scope)
            current_case_type = find_least_type(
                current_case_type, case_item_type, self.context
            )

        return current_case_type

    @visitor.when(CaseItemNode)
    def visit(self, node, scope):
        try:
            static_type = self.context.get_type(node.type)
            scope.define_variable(node.id, static_type)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        typex = self.visit(node.expr, scope)

        return typex

    @visitor.when(InstantiateNode)  # NewNode
    def visit(self, node, scope):
        try:
            typex = self.context.get_type(node.lex)
            return typex
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()

    @visitor.when(IsvoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        return self.context.get_type("Bool")

    @visitor.when(ArithmeticOperation)
    def visit(self, node, scope):
        int_type = self.context.get_type("Int")
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))

        return int_type

    @visitor.when(ComparisonOperation)
    def visit(self, node, scope):
        int_type = self.context.get_type("Int")
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))

        return self.context.get_type("Bool")

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        int_type = self.context.get_type("Int")
        string_type = self.context.get_type("String")
        bool_type = self.context.get_type("Bool")
        built_in_types = [int_type, string_type, bool_type]

        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type in built_in_types or right_type in built_in_types:
            if left_type != right_type:
                self.errors.append(
                    "Since one of the expressions of '=' operator is of type Int, String or Bool, the other must have the same static type"
                )

        return self.context.get_type("Void")

    @visitor.when(NotNode)
    def visit(self, node, scope):
        bool_type = self.context.get_type("Bool")
        typex = self.visit(node.expr, scope)

        if typex != bool_type:
            self.errors.append("Expression must be Bool")
            return ErrorType()

        return bool_type

    @visitor.when(NegNode)
    def visit(self, node, scope):
        int_type = self.context.get_type("Int")
        typex = self.visit(node.expr, scope)

        if typex != int_type:
            self.errors.append("Expression must be Int")
            return ErrorType()

        return int_type

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        return self.context.get_type("Int")

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        var = scope.find_variable(node.lex)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lex, self.current_method.name)
            )
            return ErrorType()
        return var.type

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return self.context.get_type("String")

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        return self.context.get_type("Bool")

