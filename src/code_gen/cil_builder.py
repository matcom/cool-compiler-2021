import cmp.nbpackage
import cmp.visitor as visitor

from ast_nodes import Node, ProgramNode, ExpressionNode
from ast_nodes import ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode
from ast_nodes import VarDeclarationNode, AssignNode, CallNode
from ast_nodes import (
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
from ast_nodes import (
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

from cil_nodes import (
    StringCil,
    TypeCil,
    AttributeCil,
    MethodCil,
    ProgramCil,
    FunctionCil,
    ArgCil,
    LocalCil,
    AssignmentCil,
    IfCil,
    LabelCil,
    GotoCil,
)
from cool_visitor import FormatVisitor

from cmp.semantic import SemanticError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType, IntType
from cmp.semantic import Context

from cmp.semantic import Scope
from cmp.utils import find_least_type

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


class CILBuilder:
    def __init__(self, errors=[]):
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.errors = errors
        self.method_count = 0
        self.string_count = 0
        self.temp_vars_count = 0
        self._count = 0
        self.context = None

    def generate_next_method_id(self):
        self.method_count += 1
        return "method_" + str(self.method_count)

    def generate_next_string_id(self):
        self.string_count += 1
        return "string_" + str(self.string_count)

    def generate_next_tvar_id(self):
        self.temp_vars_count += 1
        return "v_" + str(self.temp_vars_count)

    def next_id(self):
        self._count += 1
        return str(self._count)

    @visitor.on("node")
    def visit(self, node=None):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = node.context

        for declaration in node.declarations:
            self.visit(declaration)

        self.current_type = None
        self.current_method = None

        return ProgramCil(self.types, self.data, self.code)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = TypeCil(node.id)
        self.types.append(self.current_type)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        # Add attribute to current type's list of attributes (cool type of the attribute is ignored)
        self.current_type.attributes.append(AttributeCil(node.id))

        # Visit initial expression
        self.visit(node.init_exp)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        ref = self.generate_next_method_id()
        self.current_type.methods.append(MethodCil(node.id, ref))

        function = FunctionCil(ref)
        for pname, _ in node.params:
            function.args.append(ArgCil(pname))

        self.current_function = function
        self.code.append(function)

        self.visit(node.body)

    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        # Add LOCAL variable
        local = LocalCil(node.id)
        self.current_function.locals.append(local)

        # Add Assignment Node
        if node.expr:
            expr = self.visit(node.expr)
            self.current_function.body.append(AssignmentCil(local.id, expr))

    @visitor.when(AssignNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        self.current_function.body.append(AssignmentCil(node.id, expr))

    @visitor.when(CallNode)
    def visit(self, node):
        auto_type = self.context.get_type("AUTO_TYPE")
        typex = None
        if node.obj is not None:
            typex = self.visit(node.obj)
            if typex == auto_type:
                return auto_type

        else:
            typex = self.current_type

        method = None
        try:
            if node.at_type is not None:
                node_at_type = self.context.get_type(node.at_type)
                method = node_at_type.get_method(node.id)
                if not typex.conforms_to(node_at_type):
                    self.errors.append(
                        f"The static type to the left of @ ({typex.name}) must conform to the type specified to the right of @ ({node_at_type.name}) "
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
            arg_type = self.visit(arg)
            if not arg_type.conforms_to(ptype):
                self.errors.append(INCOMPATIBLE_TYPES % (arg_type.name, ptype.name))

        if method.return_type == self.context.get_type("SELF_TYPE"):
            return typex

        return method.return_type

    @visitor.when(IfNode)
    def visit(self, node):
        # Temp variable to store value of if_expr
        if_temp = self.generate_next_tvar_id()
        self.current_function.locals.append(LocalCil(if_temp))

        # Assign value
        if_expr = self.visit(node.if_expr)
        self.current_function.body.append(AssignmentCil(if_temp, if_expr))

        # IF x GOTO label
        then_label = "THEN_" + self.next_id()
        self.current_function.body.append(IfCil(if_temp, then_label))

        # Temp variable to store value of else_expr
        self.visit(node.else_expr)

        # GOTO end_label
        end_label = "END_IF_" + self.next_id()  # Example: END_IF_120
        self.current_function.body.append(GotoCil(end_label))

        # Then label
        self.current_function.body.append(LabelCil(then_label))
        self.visit(node.then_expr)

        # end_label
        self.current_function.body.append(LabelCil(end_label))

        # TODO: return something?

    @visitor.when(WhileNode)
    def visit(self, node):
        condition_type = self.visit(node.condition)
        bool_type = self.context.get_type("Bool")

        if condition_type != bool_type and condition_type.name != "AUTO_TYPE":
            self.errors.append(
                f"Expression after 'while' must be bool, current is {condition_type.name}"
            )
            return ErrorType()

        return self.context.get_type("Object")

    @visitor.when(BlockNode)
    def visit(self, node):
        typex = None
        for expr in node.expression_list:
            typex = self.visit(expr)

        return typex

    @visitor.when(LetNode)
    def visit(self, node):

        child_scope = scope.create_child()

        for var_dec in node.identifiers:
            self.visit(var_dec, child_scope)

        return self.visit(node.body, child_scope)

    @visitor.when(CaseNode)
    def visit(self, node):
        self.visit(node.expr)

        current_case_type = None
        for item in node.case_items:
            child_scope = scope.create_child()
            case_item_type = self.visit(item, child_scope)
            current_case_type = find_least_type(
                current_case_type, case_item_type, self.context
            )

        return current_case_type

    @visitor.when(CaseItemNode)
    def visit(self, node):
        try:
            static_type = self.context.get_type(node.type)
            scope.define_variable(node.id, static_type)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        typex = self.visit(node.expr)

        return typex

    @visitor.when(InstantiateNode)  # NewNode
    def visit(self, node):
        try:
            typex = self.context.get_type(node.lex)
            if typex.name == "SELF_TYPE":
                return self.current_type

            return typex
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()

    @visitor.when(IsvoidNode)
    def visit(self, node):
        self.visit(node.expr)
        return self.context.get_type("Bool")

    @visitor.when(ArithmeticOperation)
    def visit(self, node):
        int_type = self.context.get_type("Int")
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if (left_type != int_type and left_type.name != "AUTO_TYPE") or (
            right_type != int_type and right_type.name != "AUTO_TYPE"
        ):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))

        return int_type

    @visitor.when(ComparisonOperation)
    def visit(self, node):
        int_type = self.context.get_type("Int")
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if (left_type != int_type and left_type.name != "AUTO_TYPE") or (
            right_type != int_type and right_type.name != "AUTO_TYPE"
        ):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))

        return self.context.get_type("Bool")

    @visitor.when(EqualNode)
    def visit(self, node):
        int_type = self.context.get_type("Int")
        string_type = self.context.get_type("String")
        bool_type = self.context.get_type("Bool")
        built_in_types = [int_type, string_type, bool_type]

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type in built_in_types or right_type in built_in_types:
            if (
                left_type != right_type
                and left_type.name != "AUTO_TYPE"
                and right_type.name != "AUTO_TYPE"
            ):
                self.errors.append(
                    f"One of the expressions of '=' operator is of type Int, String or Bool, the other must have the same static type. Left type: {left_type.name}.Right type: {right_type.name}"
                )

        return self.context.get_type("Bool")

    @visitor.when(NotNode)
    def visit(self, node):
        bool_type = self.context.get_type("Bool")
        typex = self.visit(node.expr)

        if typex != bool_type and not typex.name == "AUTO_TYPE":
            self.errors.append(
                f"Expression after 'not' must be Bool, current is {typex.name}"
            )
            return ErrorType()

        return bool_type

    @visitor.when(NegNode)
    def visit(self, node):
        int_type = self.context.get_type("Int")
        typex = self.visit(node.expr)

        if typex != int_type and not typex.name == "AUTO_TYPE":
            self.errors.append(
                f"Expression after '~' must be Int, current is {typex.name}"
            )
            return ErrorType()

        return int_type

    @visitor.when(ConstantNumNode)
    def visit(self, node):
        return self.context.get_type("Int")

    @visitor.when(VariableNode)
    def visit(self, node):
        var = scope.find_variable(node.lex)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lex, self.current_method.name)
            )
            return ErrorType()
        return var.type

    @visitor.when(StringNode)
    def visit(self, node):
        idx = "str_" + self.generate_next_id()
        self.data.append(StringCil(idx, node.lex))

    @visitor.when(BooleanNode)
    def visit(self, node):
        return self.context.get_type("Bool")
