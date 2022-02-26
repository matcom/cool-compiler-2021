from atexit import register
from typing import Any, Dict, List, Optional, Tuple

import cool.code_generation.ast_cil as cil
import cool.code_generation.ast_ecool as ecool
import cool.semantics.utils.astnodes as cool
import cool.semantics.utils.errors as err
import cool.visitor.visitor as visitor
from cool.semantics.utils.scope import (
    Attribute,
    Context,
    ErrorType,
    Method,
    Scope,
    SemanticError,
    Type,
)


class ExtendedCoolTranslator:
    """
    This class translate the Cool AST to a ExtendedCool AST, adding the new
    features like the new keyword null in the asignments and the creation of
    a default constructor for every class defined in the program.
    """
    def __init__(self, context: Context):
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.context: Context = context
        self.class_declarations = {}  # type: Dict[str, cool.ClassDeclarationNode]

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        declarations: List[cool.ClassDeclarationNode] = []

        for declaration in node.declarations:
            self.class_declarations[declaration.id] = declaration

        for declaration in node.declarations:
            declarations.append(self.visit(declaration))

        return cool.ProgramNode(declarations)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode):
        self.current_type = self.context.get_type(node.id)

        ancestors = [
            self.class_declarations[owner.name]
            for _, owner in self.current_type.all_attributes()
        ]

        attrs = []
        visited = set()
        for ancestor in ancestors:
            if ancestor.id in visited:
                continue

            visited.add(ancestor.id)
            attrs += [
                feature
                for feature in ancestor.features
                if isinstance(feature, cool.AttrDeclarationNode)
            ]

        expressions: List[cool.ExprNode] = []
        for attr in attrs:
            expressions.append(self.visit(attr))
        expressions.append(cool.VariableNode("self"))

        body = cool.BlockNode(expressions)
        constructor = cool.MethodDeclarationNode(
            "__init__", [], self.current_type.name, body
        )

        self.current_type.define_method("__init__", [], [], self.current_type)

        attrs = [
            feature
            for feature in node.features
            if isinstance(feature, cool.AttrDeclarationNode)
        ]
        methods = [
            feature
            for feature in node.features
            if isinstance(feature, cool.MethodDeclarationNode)
        ]

        features = attrs + [constructor] + methods

        return cool.ClassDeclarationNode(node.id, features, node.parent)

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode):
        if node.expr is None:
            expr = None
            if node.type == "Int":
                expr = cool.IntegerNode("0")
            elif node.type == "Bool":
                expr = cool.BooleanNode("false")
            elif node.type == "String":
                expr = cool.StringNode('""')
            else:
                expr = (
                    ecool.NullNode()
                )  # cool.WhileNode(cool.BooleanNode("false"), cool.IntegerNode("0"))

            return cool.AssignNode(node.id, expr)

        return cool.AssignNode(node.id, node.expr)


class ExtendedCoolTypeChecker:
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.errors: List[str] = errors
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_attribute: Optional[Attribute] = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope = None):
        if scope is None:
            scope = Scope()

        node.scope = scope

        for elem in node.declarations:
            self.visit(elem, scope.create_child())

        return scope

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.id)

        attrs = [
            feature
            for feature in node.features
            if isinstance(feature, cool.AttrDeclarationNode)
        ]
        methods = [
            feature
            for feature in node.features
            if isinstance(feature, cool.MethodDeclarationNode)
        ]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        node.scope = scope
        if node.id == "self":
            self.errors.append(err.SELF_INVALID_ATTRIBUTE_ID % (node.line, node.column))

        try:
            attr_type = (
                self.context.get_type(node.type)
                if node.type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError:
            attr_type = ErrorType()

        scope.define_variable("self", self.current_type)

        # set the current attribute for analyze the body
        # and set the self.current_method variable to None
        self.current_attribute = self.current_type.get_attribute(node.id)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                line, column = node.expr_position
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (line, column, expr_type.name, attr_type.name)
                )
        scope.define_variable(node.id, attr_type)

    @visitor.when(cool.MethodDeclarationNode)
    def visit(self, node: cool.MethodDeclarationNode, scope: Scope):
        node.scope = scope
        self.current_method = self.current_type.get_method(node.id)
        self.current_attribute = None

        # Parameters can hide the attribute declaration, that's why we are not checking if there is defined,
        # instead we are checking for local declaration. Also it is checked that the static type of a parameter is
        # different of SELF_TYPE.

        scope.define_variable("self", self.current_type)

        for param_name, param_type in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            if not scope.is_local(param_name):
                if param_type.name == "SELF_TYPE":
                    self.errors.append(err.INVALID_PARAM_TYPE % "SELF_TYPE")
                    scope.define_variable(param_name, ErrorType())
                else:
                    try:
                        scope.define_variable(
                            param_name, self.context.get_type(param_type.name)
                        )
                    except SemanticError:
                        scope.define_variable(param_name, ErrorType())
            else:
                self.errors.append(
                    err.LOCAL_ALREADY_DEFINED
                    % (node.line, node.column, param_name, self.current_method.name)
                )

        try:
            return_type = (
                self.context.get_type(node.return_type)
                if node.return_type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError:
            return_type = ErrorType()

        expr_type = self.visit(node.body, scope)

        if not expr_type.conforms_to(return_type):
            self.errors.append(
                err.INCOMPATIBLE_TYPES
                % (node.line, node.column, expr_type.name, return_type.name)
            )

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        node.scope = scope
        for i, (_id, _type, _expr) in enumerate(node.declarations):
            if _id == "self":
                line, column = node.declaration_names_positions[i]
                self.errors.append(err.SELF_USED_IN_LET % (line, column))
                continue

            try:
                var_static_type = (
                    self.context.get_type(_type)
                    if _type != "SELF_TYPE"
                    else self.current_type
                )
            except SemanticError:
                line, column = node.declaration_types_positions[i]
                self.errors.append(err.UNDEFINED_TYPE % (line, column, _type))
                var_static_type = ErrorType()

            scope.define_variable(_id, var_static_type)

            expr_type = (
                self.visit(_expr, scope.create_child()) if _expr is not None else None
            )
            if expr_type is not None and not expr_type.conforms_to(var_static_type):
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (node.line, node.column, expr_type.name, var_static_type.name)
                )

        return self.visit(node.expr, scope.create_child())

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        node.scope = scope
        var_info = scope.find_variable(node.id)

        if var_info.name == "self":
            self.errors.append(err.SELF_IS_READONLY % (node.line, node.column))

        expr_type = self.visit(node.expr, scope)

        if var_info is None:
            self.errors.append(
                err.UNDEFINED_VARIABLE
                % (node.line, node.column, node.id, self.current_method.name)
            )
        else:
            if not expr_type.conforms_to(var_info.type):
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (node.line, node.column, expr_type.name, var_info.type.name)
                )

        return expr_type

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        node.scope = scope
        return_type = ErrorType()
        for expr in node.expressions:
            return_type = self.visit(expr, scope)
        return return_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        node.scope = scope
        if_type = self.visit(node.if_expr, scope)
        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)
        if if_type != self.context.get_type("Bool"):
            self.errors.append(
                err.INCOMPATIBLE_TYPES % (node.line, node.column, if_type.name, "Bool")
            )
        return then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        node.scope = scope
        condition = self.visit(node.condition, scope)
        if condition != self.context.get_type("Bool"):
            self.errors.append(
                err.INCOMPATIBLE_TYPES
                % (node.line, node.column, condition.name, "Bool")
            )

        self.visit(node.body, scope)
        return self.context.get_type("Object")

    @visitor.when(cool.SwitchCaseNode)
    def visit(self, node: cool.SwitchCaseNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        types = []
        visited = set()
        for i, (identifier, type_name, expr) in enumerate(node.cases):
            new_scope = scope.create_child()
            try:
                if type_name != "SELF_TYPE":
                    new_scope.define_variable(
                        identifier, self.context.get_type(type_name)
                    )
                else:
                    self.errors.append(err.INVALID_CASE_TYPE % type_name)
            except SemanticError:
                new_scope.define_variable(identifier, ErrorType())
                line, column = node.cases_positions[i]
                self.errors.append(
                    err.UNDEFINED_TYPE_IN_BRANCH % (line, column, type_name)
                )

            # Cannot be dublicate Branches types
            if type_name in visited:
                line, column = node.cases_positions[i]
                self.errors.append(
                    err.DUPLICATE_BARNCH_IN_CASE % (line, column, type_name)
                )

            visited.add(type_name)
            types.append(self.visit(expr, new_scope))

        return Type.multi_join(types)

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        node.scope = scope
        if node.obj is None:
            node.obj = cool.VariableNode("self")
        obj_type = self.visit(node.obj, scope)

        if node.type is not None:
            try:
                ancestor_type = self.context.get_type(node.type)
            except SemanticError:
                ancestor_type = ErrorType()
                line, column = node.type_position
                self.errors.append(err.UNDEFINED_TYPE % (line, column, node.type))

            if not obj_type.conforms_to(ancestor_type):
                line, column = node.type_position
                self.errors.append(
                    err.INVALID_ANCESTOR
                    % (line, column, obj_type.name, ancestor_type.name)
                )
        else:
            ancestor_type = obj_type

        try:
            method = ancestor_type.get_method(node.id)
        except SemanticError:
            line, column = node.id_position
            self.errors.append(
                err.DISPATCH_UNDEFINED_METHOD % (line, column, node.id, obj_type.name)
            )

            for arg in node.args:
                self.visit(arg, scope)
            return ErrorType()

        args_count = len(node.args)
        params_count = len(method.param_names)
        if args_count != params_count:
            line, column = node.id_position
            self.errors.append(
                err.DISPATCH_WITH_WRONG_NUMBER_OF_ARGS
                % (line, column, method.name, obj_type.name, params_count, args_count)
            )

        number_of_args = min(args_count, params_count)
        for i, arg in enumerate(node.args[:number_of_args]):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(method.param_types[i]):
                line, column = node.args_positions[i]
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (
                        line,
                        column,
                        arg_type.name,
                        method.param_types[i].name,
                    )
                )

        return (
            method.return_type
            if method.return_type.name != "SELF_TYPE"
            else ancestor_type
        )

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
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

    @visitor.when(ecool.NullNode)
    def visit(self, node: ecool.NullNode, scope: Scope):
        node.scope = scope
        return ecool.NullType()

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        node.scope = scope
        variable = scope.find_variable(node.lex)
        if variable is None:
            if self.current_attribute is not None:
                name = self.current_attribute.name
            else:
                name = self.current_method.name

            self.errors.append(
                err.UNDEFINED_VARIABLE % (node.line, node.column, node.lex, name)
            )
            return ErrorType()
        return variable.type

    @visitor.when(cool.InstantiateNode)
    def visit(self, node: cool.InstantiateNode, scope: Scope):
        node.scope = scope
        try:
            return (
                self.context.get_type(node.lex)
                if node.lex != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError as e:
            line, column = node.type_position
            self.errors.append(err.UNDEFINED_NEW_TYPE % (line, column, node.lex))
            return ErrorType()

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        node.scope = scope
        return self._check_unary_operation(
            node, scope, "not", self.context.get_type("Bool")
        )

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        node.scope = scope
        return self._check_unary_operation(
            node, scope, "~", self.context.get_type("Int")
        )

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        return self.context.get_type("Bool")

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "+", self.context.get_type("Int")
        )

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "-", self.context.get_type("Int")
        )

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "*", self.context.get_type("Int")
        )

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "/", self.context.get_type("Int")
        )

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "<=", self.context.get_type("Bool")
        )

    @visitor.when(cool.LessThanNode)
    def visit(self, node: cool.LessThanNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "<", self.context.get_type("Bool")
        )

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        node.scope = scope
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        basic_types = ("Int", "String", "Bool")
        if (
            left_type.name in basic_types or left_type.name in basic_types
        ) and left_type.name != right_type.name:
            self.errors.append(
                err.INVALID_EQ_COMPARISON_OPERATION % (node.line, node.column)
            )
        return self.context.get_type("Bool")

    def _check_int_binary_operation(
        self, node: cool.BinaryNode, scope: Scope, operation: str, return_type: Type
    ):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type == right_type == self.context.get_type("Int"):
            return return_type
        self.errors.append(
            err.INVALID_BINARY_OPERATION
            % (node.line, node.column, operation, left_type.name, right_type.name)
        )
        return ErrorType()

    def _check_unary_operation(
        self, node: cool.UnaryNode, scope: Scope, operation: str, expected_type: Type
    ):
        typex = self.visit(node.expr, scope)
        if typex == expected_type:
            return typex
        self.errors.append(
            err.INVALID_UNARY_OPERATION
            % (node.line, node.column, operation, typex.name)
        )
        return ErrorType()


class BaseCoolToCilVisitor:
    def __init__(self, context: Context):
        self.dottypes: List[cil.TypeNode] = []
        self.dotdata: List[cil.DataNode] = []
        self.dotcode: List[cil.FunctionNode] = []

        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_function: Optional[cil.FunctionNode] = None

        self.context: Context = context

        self.locals_dict = {}
        self.param_set = set()
        self.attr_set = set()

    @property
    def params(self) -> List[cil.ParamNode]:
        return self.current_function.params

    @property
    def localvars(self) -> List[cil.LocalNode]:
        return self.current_function.local_vars

    @property
    def instructions(self) -> List[cil.InstructionNode]:
        return self.current_function.instructions

    def register_local(self, var_name: str, comment: str = "") -> str:
        local_name = (
            f"local_{self.current_function.name[9:]}_{var_name}_{len(self.localvars)}"
        )
        local_name = var_name
        local_node = cil.LocalNode(local_name).set_comment(comment)
        self.localvars.append(local_node)
        return local_name

    def define_internal_local(self, comment: str = "") -> str:
        return self.register_local(f"internal_{len(self.localvars)}", comment)

    def register_instruction(
        self, instruction: cil.InstructionNode
    ) -> cil.InstructionNode:
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name: str, type_name: str) -> str:
        return f"function_{method_name}_at_{type_name}"

    def register_function(self, function_name: str) -> cil.FunctionNode:
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name: str, parent_name: Optional[str] = None) -> cil.TypeNode:
        type_node = cil.TypeNode(name, parent_name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value: Any) -> cil.DataNode:
        data_name = f"data_{len(self.dotdata)}"
        data_node = cil.DataNode(data_name, value)
        self.dotdata.append(data_node)
        return data_node

    def register_comment(self, comment: str) -> cil.CommentNode:
        self.register_instruction(cil.CommentNode(comment))
    
    def register_empty_instruction(self):
        self.register_instruction(cil.EmptyInstruction())


class CoolToCilTranslator(BaseCoolToCilVisitor):
    # Notes:
    # 1 - All the expression nodes are going to return a tuple [str, Type]
    
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        scope = node.scope
        default_class_names = ["Object", "IO", "Int", "String", "Bool"]
        for name in default_class_names:
            t = self.context.get_type(name)
            self.current_type = t
            cil_type_node = self.register_type(t.name, t.parent.name if t.parent is not None else None)
            for method, owner in t.all_methods():
                cil_type_node.methods.append((method.name, self.to_function_name(method.name, owner.name)))
            cil_type_node.methods.append(("__init__", self.to_function_name("__init__", t.name)))

        self.current_function = self.register_function("function_add")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Adding result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.PlusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_sub")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Substracting result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.MinusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        
        self.current_function = self.register_function("function_mult")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Multiting result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.StarNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_div")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Dividing result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.DivNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_xor")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Xor result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.XorNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_less_than")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Less than result")
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessThanNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        
        self.current_function = self.register_function("function_less_than_or_equal")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Less than or equal result")
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessEqualNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_equal")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Equal result")
        constant_null = self.define_internal_local("Null Pointer")
        is_null = self.define_internal_local("One of params is null")
        type_of_a = self.define_internal_local("Type of a")
        type_int = self.define_internal_local("Type Int")
        type_bool = self.define_internal_local("Type Bool")
        type_string = self.define_internal_local("Type String")
        type_a_equals_int = self.define_internal_local("Type of a equals int")
        type_a_equals_bool = self.define_internal_local("Type of a equals bool")
        type_a_equals_string = self.define_internal_local("Type of a equals string")
        
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.AllocateNullPtrNode(constant_null))
        self.register_instruction(cil.AllocateBoolNode(is_null, "0"))
        
        self.register_instruction(cil.EqualAddressNode(is_null, "a", constant_null))
        self.register_instruction(cil.EqualAddressNode(is_null, "b", constant_null))
        self.register_instruction(cil.GotoIfNode(is_null, "a_is_type_object"))

        self.register_instruction(cil.TypeOfNode(type_of_a, "a"))
        self.register_instruction(cil.TypeAddressNode(type_int, "Int"))
        self.register_instruction(cil.TypeAddressNode(type_bool, "Bool"))
        self.register_instruction(cil.TypeAddressNode(type_string, "String"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_bool, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_string, "0"))

        self.register_instruction(cil.EqualAddressNode(type_a_equals_int, type_of_a, type_int))
        self.register_instruction(cil.EqualAddressNode(type_a_equals_bool, type_of_a, type_bool))
        self.register_instruction(cil.EqualAddressNode(type_a_equals_string, type_of_a, type_string))
        self.register_empty_instruction()
        self.register_instruction(cil.GotoIfNode(type_a_equals_int, "a_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_a_equals_bool, "a_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_a_equals_string, "a_is_type_string"))       
        self.register_instruction(cil.GotoNode("a_is_type_object"))
        
        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("a_is_type_int_or_bool"))
        self.register_instruction(cil.EqualIntNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))

        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("a_is_type_string"))
        self.register_instruction(cil.EqualStrNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))

        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("a_is_type_object"))
        self.register_instruction(cil.EqualNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))
        
        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("end_of_equal"))

        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function("function_assign")
        self.current_function.params.append(cil.ParamNode("dest"))
        self.current_function.params.append(cil.ParamNode("source"))
        constant_null = self.define_internal_local("Null Pointer")
        is_null = self.define_internal_local("One of params is null")
        type_of_source = self.define_internal_local("Type of source")
        type_int = self.define_internal_local("Type Int")
        type_bool = self.define_internal_local("Type Bool")
        type_source_equals_int = self.define_internal_local("Type of source equals int")
        type_source_equals_bool = self.define_internal_local("Type of source equals bool")
       
        self.register_instruction(cil.AllocateNullPtrNode(constant_null))
        self.register_instruction(cil.AllocateBoolNode(is_null, "0"))
        self.register_instruction(cil.EqualAddressNode(is_null, "source", constant_null))
        self.register_instruction(cil.EqualAddressNode(is_null, "dest", constant_null))
        self.register_instruction(cil.GotoIfNode(is_null, "source_is_type_object"))

        self.register_instruction(cil.TypeOfNode(type_of_source, "source"))
        self.register_instruction(cil.TypeAddressNode(type_int, "Int"))
        self.register_instruction(cil.TypeAddressNode(type_bool, "Bool"))
        self.register_instruction(cil.AllocateBoolNode(type_source_equals_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_source_equals_bool, "0"))
        self.register_instruction(cil.EqualAddressNode(type_source_equals_int, type_of_source, type_int))
        self.register_instruction(cil.EqualAddressNode(type_source_equals_bool, type_of_source, type_bool))
        self.register_empty_instruction()
        self.register_instruction(cil.GotoIfNode(type_source_equals_int, "source_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_source_equals_bool, "source_is_type_int_or_bool"))
        self.register_instruction(cil.GotoNode("source_is_type_object"))

        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("source_is_type_int_or_bool"))

        self.register_instruction(cil.AssignIntNode("dest", "source"))
        self.register_instruction(cil.GotoNode("source_end_of_equal"))

        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("source_is_type_object"))
        self.register_instruction(cil.AssignNode("dest", "source"))
        self.register_instruction(cil.GotoNode("source_end_of_equal"))
        
        self.register_empty_instruction()
        self.register_instruction(cil.LabelNode("source_end_of_equal"))

        self.register_instruction(cil.ReturnNode("dest"))


        self.current_function = self.register_function(self.to_function_name("__init__", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.ReturnNode("self"))

        self.current_function = self.register_function(self.to_function_name("abort", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        msg1 = self.define_internal_local()
        msg2 = self.define_internal_local()
        endl = self.define_internal_local()
        msg = self.define_internal_local()
        self.register_instruction(cil.AllocateStrNode(msg1, "\"Abort called from class \""))
        self.register_instruction(cil.AllocateStrNode(endl, "\"\\n\""))
        self.register_instruction(cil.ArgNode("self", 0, 1))
        self.register_instruction(cil.DynamicCallNode("String", self.to_function_name("type_name", "Object"), msg2, 1))
        
        self.register_instruction(cil.ArgNode(msg1, 0, 2))
        self.register_instruction(cil.ArgNode(msg2, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", self.to_function_name("concat", "String"), msg, 2))

        self.register_instruction(cil.ArgNode(msg, 0, 2))
        self.register_instruction(cil.ArgNode(endl, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", self.to_function_name("concat", "String"), msg, 2))

        self.register_instruction(cil.PrintStringNode(msg))
        self.register_instruction(cil.HaltNode())
        self.register_instruction(cil.ReturnNode("self"))
        
        self.current_function = self.register_function(self.to_function_name("type_name", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        type_name = self.define_internal_local("type_name")
        self.register_instruction(cil.TypeNameNode(type_name, "self"))
        self.register_instruction(cil.ReturnNode(type_name))

        self.current_function = self.register_function(self.to_function_name("copy", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_copy = self.define_internal_local()
        self.register_instruction(cil.CopyNode(local_copy, "self"))
        self.register_instruction(cil.ReturnNode(local_copy))

        self.current_function = self.register_function(self.to_function_name("__init__", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.ReturnNode("self"))

        self.current_function = self.register_function(self.to_function_name("out_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintStringNode("x"))
        self.register_instruction(cil.ReturnNode("self"))

        self.current_function = self.register_function(self.to_function_name("out_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintIntNode("x"))
        self.register_instruction(cil.ReturnNode("self"))
        
        self.current_function = self.register_function(self.to_function_name("in_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.ReadStringNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))

        self.current_function = self.register_function(self.to_function_name("in_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(local_str, "0"))
        self.register_instruction(cil.ReadIntNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))

        self.current_function = self.register_function(self.to_function_name("__init__", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.ReturnNode("self"))

        self.current_function = self.register_function(self.to_function_name("length", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        len_local =  self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(len_local, "0"))
        self.register_instruction(cil.LengthNode(len_local, "self"))
        self.register_instruction(cil.ReturnNode(len_local))

        self.current_function = self.register_function(self.to_function_name("concat", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("s"))
        new_str =  self.define_internal_local()
        self.register_instruction(cil.ConcatNode(new_str, "self", "s"))
        self.register_instruction(cil.ReturnNode(new_str))

        self.current_function = self.register_function(self.to_function_name("substr", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("i"))
        self.current_function.params.append(cil.ParamNode("l"))
        substr =  self.define_internal_local()
        self.register_instruction(cil.SubstringNode(substr, "self", "i", "l"))            
        self.register_instruction(cil.ReturnNode(substr))
        
        self.current_function = self.register_function(self.to_function_name("__init__", "Int"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.AllocateIntNode("self", "0"))
        self.register_instruction(cil.ReturnNode("self"))

        self.current_function = self.register_function(self.to_function_name("__init__", "Bool"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.AllocateBoolNode("self", "0"))
        self.register_instruction(cil.ReturnNode("self"))

        for i, declaration in enumerate(node.declarations):
            self.visit(declaration, scope.children[i])

        self.current_function = self.register_function("main")
        local_main = self.define_internal_local()
        local_result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Main", local_main))
        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.DynamicCallNode("Main", self.to_function_name("__init__", "Main"), local_main, 1))
        self.register_empty_instruction()
        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.DynamicCallNode("Main", self.to_function_name("main", "Main"), local_result, 1))
        self.register_empty_instruction()
        self.register_instruction(cil.HaltNode())

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        scope = node.scope
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(self.current_type.name, self.current_type.parent.name)

        attrs = [
            feature
            for feature in node.features
            if isinstance(feature, cool.AttrDeclarationNode)
        ]

        methods = [
            feature
            for feature in node.features
            if isinstance(feature, cool.MethodDeclarationNode)
        ]

        for attr, _ in self.current_type.all_attributes():
            self.visit(attr, scope)
            type_node.attributes.append(attr.name)

        visited = set()
        for method, _ in self.current_type.all_methods():

            if method.name in visited:
                continue

            visited.add(method.name)
            _, ancestor = self.current_type.get_method(method.name, get_owner=True)

            type_node.methods.append(
                (method.name, self.to_function_name(method.name, ancestor.name))
            )

        i = len([attr for attr in attrs if attr.expr is not None])
        for i, method in enumerate(methods, start=i):
            self.visit(method, scope.children[i])

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        scope = node.scope
        pass

    @visitor.when(cool.MethodDeclarationNode)
    def visit(self, node: cool.MethodDeclarationNode, scope: Scope):
        scope = node.scope
        self.current_method, owner_type = self.current_type.get_method(
            node.id, get_owner=True
        )
        function_name = self.to_function_name(self.current_method.name, owner_type.name)
        self.current_function = self.register_function(function_name)

        self.current_function.params = [cil.ParamNode("self")] + [
            cil.ParamNode(param_name) for param_name, _ in node.params
        ]

        source, _ = self.visit(node.body, scope)

        self.register_instruction(cil.ReturnNode(source))

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        scope = node.scope
        x = " ".join([f"{name}: {type_name}" for name, type_name, _ in node.declarations])
        self.register_comment(f"Let {x}")
        
        i = 0
        for name, type_name, expr in node.declarations:
            self.register_local(name)

            if expr:
                self.register_empty_instruction()
                source, _ = self.visit(expr, scope.children[i])
                self.register_instruction(cil.ArgNode(name, 0, 2))
                self.register_instruction(cil.ArgNode(source, 1, 2))
                self.register_instruction(cil.StaticCallNode("function_assign", name, 2))        
                i += 1
            else:
                if type_name == "Int":
                    self.register_instruction(cil.AllocateIntNode(name, "0"))
                elif type_name == "Bool":
                    self.register_instruction(cil.AllocateBoolNode(name, "0"))
                elif type_name == "String":
                    self.register_instruction(cil.AllocateStrNode(name, "\"\""))
                else:
                    self.register_instruction(cil.AllocateNullPtrNode(name))
        source, t = self.visit(node.expr, scope.children[i])

        return source, t

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        scope = node.scope
        variable = scope.find_variable(node.id)
        variables = scope.find_all_variables(node.id)
        source, _ = self.visit(node.expr, scope)

        self.register_empty_instruction()
        is_attribute = (
            self.current_type.contains_attribute(node.id) and len(variables) == 1
        )

        if is_attribute:
            attr_names = [attr.name for attr, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.SetAttributeNode("self", variable.name, source, attr_names.index(variable.name)))
            return source, variable.type
        else:
            self.register_instruction(cil.ArgNode(variable.name, 0, 2))
            self.register_instruction(cil.ArgNode(source, 1, 2))
            self.register_instruction(cil.StaticCallNode("function_assign", variable.name, 2))
            # self.register_instruction(cil.AssignNode(variable.name, source))
            return variable.name, variable.type

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        scope = node.scope
        source, inst_type = None, None
        for expr in node.expressions:
            source, inst_type = self.visit(expr, scope)
        return source, inst_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        scope = node.scope
        self.register_instruction(cil.CommentNode("Conditional"))

        node_id = hash(node)
        result_address = self.define_internal_local()
        conditional_address = self.define_internal_local()

        self.register_instruction(cil.AllocateBoolNode(conditional_address, "0"))

        source, _ = self.visit(node.if_expr, scope)

        self.register_instruction(cil.AssignNode(conditional_address, source))
        self.register_instruction(cil.GotoIfNode(conditional_address, f"then_{node_id}"))
        self.register_instruction(cil.GotoNode(f"else_{node_id}"))

        self.register_instruction(cil.EmptyInstruction())
        self.register_instruction(cil.LabelNode(f"then_{node_id}"))
        then_source, then_type = self.visit(node.then_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, then_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EmptyInstruction())
        self.register_instruction(cil.LabelNode(f"else_{node_id}"))
        else_source, else_type = self.visit(node.else_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, else_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EmptyInstruction())
        self.register_instruction(cil.LabelNode(f"endif_{node_id}"))

        return result_address, then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        scope = node.scope
        # result_addres = self.define_internal_local()
        node_id = hash(node)
        self.register_empty_instruction()
        self.register_comment(f"While loop")

        # self.register_instruction(cil.AssignNode(result_addres, 0))
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))

        conditional_source, _ = self.visit(node.condition, scope)
        self.register_instruction(cil.GotoIfNode(conditional_source, f"while_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"while_end_{node_id}"))

        self.register_instruction(cil.EmptyInstruction())
        self.register_instruction(cil.LabelNode(f"while_body_{node_id}"))
        self.visit(node.body, scope)
        self.register_instruction(cil.GotoNode(f"while_start_{node_id}"))

        self.register_instruction(cil.EmptyInstruction())
        self.register_instruction(cil.LabelNode(f"while_end_{node_id}"))

        return "0", self.context.get_type("Object")

    @visitor.when(cool.SwitchCaseNode)
    def visit(self, node: cool.SwitchCaseNode, scope: Scope):
        scope = node.scope
        node_id = hash(node)
        swicth_expression, _ = self.visit(node.expr, scope)
        
        constant_zero_int = self.define_internal_local("Constant Integer 0 ")
        constant_one_int = self.define_internal_local("Constant Integer 1")
        constant_len_types_int = self.define_internal_local(f"Constant Integer {len(node.cases)}")
        constant_null_ptr = self.define_internal_local("Null pointer")
        count_of_ancestors_int = self.define_internal_local("Count of ancestors of the switch expression")
        switch_expr_type_address = self.define_internal_local("Switch expression type")
        ancestor_type_address = self.define_internal_local("Ancestor type")
        step1_comparison_result_bool = self.define_internal_local("Step 1 comparison result")
        ancestors_array = self.define_internal_local("Step 1 Array of ancestors")

        self.register_instruction(cil.AllocateIntNode(constant_zero_int, "0"))
        self.register_instruction(cil.AllocateIntNode(constant_one_int, "1"))
        self.register_instruction(cil.AllocateIntNode(constant_len_types_int, str(len(node.cases))))
        self.register_instruction(cil.AllocateNullPtrNode(constant_null_ptr))
        self.register_instruction(cil.AllocateIntNode(count_of_ancestors_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(step1_comparison_result_bool, "0"))
        self.register_empty_instruction()

        self.register_comment("Switch Case Algorithm Steps:")
        self.register_comment(" 1 - Count how many ancestors has the dynamic type of the expression")
        self.register_comment(" 2 - Create an array of the same size where to store the ancestors")
        self.register_comment(" 3 - For each branch type, store the ancestor index that match with it, if no one match, store `count of ancestors`")
        self.register_comment(" 4 - Find the minimum of the ancestors indexes")
        self.register_comment(" 5 - With the minimum index, get the correct branch type")

        ############################################
        # While loop to get the count of ancestors #
        ############################################

        self.register_empty_instruction()
        self.register_comment("######################################################################## #")
        self.register_comment("Step 1 - Count how many ancestors has the dynamic type of the expression #")
        self.register_comment("######################################################################## #")
        self.register_instruction(cil.TypeOfNode(switch_expr_type_address, swicth_expression).set_comment("Get the switch expression type"))
        self.register_instruction(cil.AssignNode(ancestor_type_address, switch_expr_type_address).set_comment("The first ancestor will be the type itself"))
        
        # self.register_instruction(cil.ArgNode(count_of_ancestors_int, 0, 2))
        # self.register_instruction(cil.ArgNode(constant_zero_int, 1, 2))
        # self.register_instruction(cil.StaticCallNode("function_assign", count_of_ancestors_int, 2))
        # self.register_instruction(cil.PrintIntNode(count_of_ancestors_int))
        
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))
        self.register_instruction(cil.EqualAddressNode(step1_comparison_result_bool, ancestor_type_address, constant_null_ptr))
        self.register_instruction(cil.GotoIfNode(step1_comparison_result_bool, f"while_end_{node_id}"))

        self.register_comment("Increment the count of ancestors")
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", count_of_ancestors_int, 2))
        # self.register_instruction(cil.PrintIntNode(count_of_ancestors_int))

        # self.register_instruction(cil.AssertTypeNode(ancestor_type_address))

        self.register_instruction(cil.AncestorNode(ancestor_type_address, ancestor_type_address))
        self.register_instruction(cil.GotoNode(f"while_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"while_end_{node_id}"))
        # #################################################
        # # End While loop to get the count of ancestors  #
        # #################################################


        # #######################################################################
        # # Foreach to create the array of ancestors and fill it with the types #
        # #######################################################################
        self.register_empty_instruction()
        self.register_comment("###################################################################### #")
        self.register_comment("Step 2 - Create an array of the same size where to store the ancestors #")
        self.register_comment("###################################################################### #")
        self.register_instruction(cil.AssignNode(ancestor_type_address, switch_expr_type_address).set_comment("The first ancestor will be the type itself"))
        self.register_instruction(cil.ArrayNode(ancestors_array, count_of_ancestors_int).set_comment("Create an array of ancestors"))
    
        step2_iter_index_int = self.define_internal_local("Step 2 iteration index")
        step2_comparison_result_bool = self.define_internal_local("Step 2 comparison result")
        
        self.register_instruction(cil.AllocateIntNode(step2_iter_index_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(step2_comparison_result_bool, "0"))
        
        # self.register_instruction(cil.AssignNode(step2_iter_index_int, constant_zero_int).set_comment("Initialize the index with the value 0"))
        
        self.register_instruction(cil.LabelNode(f"foreach_start_{node_id}"))

        self.register_instruction(cil.ArgNode(step2_iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step2_comparison_result_bool, 2))
        # self.register_instruction(cil.PrintIntNode(step2_iter_index_int))
        # self.register_instruction(cil.PrintIntNode(step2_comparison_result_bool))
        
        self.register_instruction(cil.GotoIfNode(step2_comparison_result_bool, f"foreach_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_body_{node_id}"))
        self.register_instruction(cil.SetIndexNode(ancestors_array, step2_iter_index_int, ancestor_type_address).set_comment("Set the index of the array with the ancestor type"))
        # self.register_instruction(cil.GetIndexNode(ancestor_type_address, ancestors_array, step2_iter_index_int))
        # self.register_instruction(cil.AssertTypeNode(ancestor_type_address))
        self.register_instruction(cil.AncestorNode(ancestor_type_address, ancestor_type_address).set_comment("Get the next ancestor"))
    

        self.register_instruction(cil.ArgNode(step2_iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", step2_iter_index_int, 2))
        
        self.register_instruction(cil.GotoNode(f"foreach_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_end_{node_id}"))
        self.register_empty_instruction()
        # ###########################################################################
        # # End Foreach to create the array of ancestors and fill it with the types #
        # ###########################################################################

        
        # self.register_comment("#################################################################################################### #")
        # self.register_comment("Step 3 - For each branch type, store the ancestor index that match with it (Simulating a double for) #")
        # self.register_comment("#################################################################################################### #")
        
        types = [self.context.get_type(type_name) for _, type_name, _ in node.cases]
        type_branch_array = self.define_internal_local("Array to store the branch types")
        nearest_ancestor_array = self.define_internal_local("Array to store the nearest ancestor index of the expression type of the i-th branch type ")
        self.register_instruction(cil.ArrayNode(type_branch_array, constant_len_types_int))
        self.register_instruction(cil.ArrayNode(nearest_ancestor_array, constant_len_types_int))
        for i_int, t in enumerate(types):
            x = self.define_internal_local(f"Address of the type {t.name}")
            i = self.define_internal_local(f"Index of the type {t.name}")
            self.register_instruction(cil.AllocateIntNode(i, i_int))
            self.register_instruction(cil.TypeAddressNode(x, t.name))
            self.register_instruction(cil.SetIndexNode(type_branch_array, i, x))
            # self.register_instruction(cil.GetIndexNode(x, ancestors_array, i))
            # self.register_instruction(cil.AssertTypeNode(x))
            self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i, count_of_ancestors_int))
            # self.register_instruction(cil.GetValueInIndexNode(count_of_ancestors_int, nearest_ancestor_array, i))
            # self.register_instruction(cil.PrintIntNode(count_of_ancestors_int))
            
        self.register_empty_instruction()

        i_int = self.define_internal_local("Step 3 - Iteration index of the branch types array")
        comp_i_bool = self.define_internal_local("Step 3 - Comparison for the index of the branch types array")
        type_i = self.define_internal_local("Step 3 - Type of the i-th branch")
        j_int = self.define_internal_local("Step 3 - Index of the ancestor")
        comp_j_bool = self.define_internal_local("Step 3 - Comparison for the index of the ancestor")
        type_j = self.define_internal_local("Step 3 - Type of the j-th ancestor")
        types_comparison_bool = self.define_internal_local("Step 3 - Comparison for the branch type nad the ancestor type")

        self.register_instruction(cil.AllocateIntNode(i_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comp_i_bool, "0"))
        self.register_instruction(cil.AllocateIntNode(j_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comp_j_bool, "0"))
        self.register_instruction(cil.AllocateBoolNode(types_comparison_bool, "0"))

        # self.register_comment("############# #")
        # self.register_comment("Outer Foreach #")
        # self.register_comment("############# #")
        # self.register_instruction(cil.AssignNode(i_int, constant_zero_int).set_comment("Initialize the index i of the case to 0"))
        self.register_instruction(cil.LabelNode(f"foreach_type_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(i_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", comp_i_bool, 2))
        # self.register_instruction(cil.PrintIntNode(i_int))
        # self.register_instruction(cil.PrintIntNode(comp_i_bool))
        
        self.register_instruction(cil.GotoIfNode(comp_i_bool, f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_type_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_i, type_branch_array, i_int).set_comment("Get the type of the i-th branch"))
        # self.register_instruction(cil.AssertTypeNode(type_i))
        
        # #################
        # # Inner Foreach #
        # #################
        # self.register_empty_instruction()
        # self.register_comment("############# #")
        # self.register_comment("Inner Foreach #")
        # self.register_comment("############# #")
        
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_zero_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", j_int, 2))
        # self.register_instruction(cil.PrintIntNode(j_int))

        self.register_instruction(cil.LabelNode(f"foreach_ancestor_start_{node_id}"))

        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", comp_j_bool, 2))
        # self.register_instruction(cil.PrintIntNode(j_int))
        # self.register_instruction(cil.PrintIntNode(comp_j_bool))
        # self.register_instruction(cil.LessThanNode(comp_j_bool, j_int, count_of_ancestors_int).set_comment("Check if the case index is less than the count of ancestors"))
        self.register_instruction(cil.GotoIfNode(comp_j_bool, f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_j, ancestors_array, j_int).set_comment("Get the j-th ancestor type"))
        # self.register_instruction(cil.AssertTypeNode(type_j))

        self.register_instruction(cil.EqualAddressNode(types_comparison_bool, type_i, type_j).set_comment("Compare if the type of the i-th branch is equal to the j-th ancestor"))
        # self.register_instruction(cil.PrintIntNode(types_comparison_bool))
        self.register_instruction(cil.GotoIfNode(types_comparison_bool, f"foreach_ancestor_end_{node_id}").set_comment("If the types are equal, we have a match, then we can exit"))
       
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", j_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i_int, j_int).set_comment("Set the counter of the i-th branch equals to j"))
        # self.register_instruction(cil.GetValueInIndexNode(j_int, nearest_ancestor_array, i_int))
        # self.register_instruction(cil.PrintIntNode(j_int))
        self.register_comment("#################### #")
        self.register_comment("End of Inner Foreach #")
        self.register_comment("#################### #")
        self.register_empty_instruction()
        # #######################
        # # End Inner Foreach 1 #
        # #######################
        
        self.register_instruction(cil.ArgNode(i_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", i_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_type_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_type_end_{node_id}"))
        self.register_comment("################# #")
        self.register_comment("End Outer Foreach #")
        self.register_comment("################# #")

        self.register_empty_instruction()
        self.register_comment("######################################## #")
        self.register_comment("Step 4 - Find the minimum ancestor index #")
        self.register_comment("######################################## #")
        step4_index_int = self.define_internal_local("Step 4 - Iteration index")
        step4_current_min_index_int = self.define_internal_local("Step 4 - Index of the minimum counter in the counter array")
        step4_temp_int = self.define_internal_local("Step 4 - Temporary variable")
        step4_current_min_int = self.define_internal_local("Step 4 - Current minimum of the counter array")
        step4_comparison_bool = self.define_internal_local("Step 4 - Comparison for the minimum of the counter array")
        
        endl =self.define_internal_local("endl")
        space  =self.define_internal_local("space")
        self.register_instruction(cil.AllocateStrNode(endl, '"\\n"'))
        self.register_instruction(cil.AllocateStrNode(space, '" "'))

        self.register_instruction(cil.AllocateIntNode(step4_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_current_min_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_temp_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_current_min_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(step4_comparison_bool, "0"))

        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_int, 2))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_int))
        
        self.register_instruction(cil.LabelNode(f"foreach_min_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(step4_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step4_comparison_bool, 2))
        # self.register_instruction(cil.PrintIntNode(step4_index_int))
        # self.register_instruction(cil.PrintStringNode(space))
        # self.register_instruction(cil.PrintIntNode(step4_comparison_bool))
        # self.register_instruction(cil.PrintStringNode(space))

        self.register_instruction(cil.GotoIfNode(step4_comparison_bool, f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GetValueInIndexNode(step4_temp_int, nearest_ancestor_array, step4_index_int).set_comment("Get the nearest ancestor index of the i-th branch type"))
        # self.register_instruction(cil.PrintIntNode(step4_temp_int))
        # self.register_instruction(cil.PrintStringNode(space))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_int))
        # self.register_instruction(cil.PrintStringNode(space))

        self.register_instruction(cil.ArgNode(step4_temp_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_current_min_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step4_comparison_bool, 2))
        # self.register_instruction(cil.PrintIntNode(step4_comparison_bool))
        # self.register_instruction(cil.PrintStringNode(space))      

        self.register_instruction(cil.GotoIfNode(step4_comparison_bool, f"update_min_{node_id}"))
        self.register_instruction(cil.GotoNode(f"update_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"update_min_{node_id}"))
        
        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_temp_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_int, 2))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_int))
        # self.register_instruction(cil.PrintStringNode(space))

        self.register_instruction(cil.ArgNode(step4_current_min_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_index_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_index_int, 2))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_index_int))
        # self.register_instruction(cil.PrintStringNode(space))

        self.register_instruction(cil.LabelNode(f"update_min_end_{node_id}"))

        self.register_instruction(cil.ArgNode(step4_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", step4_index_int, 2))
        
        # self.register_instruction(cil.PrintStringNode(endl))
        self.register_instruction(cil.GotoNode(f"foreach_min_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_end_{node_id}"))

        # self.register_instruction(cil.PrintStringNode(endl))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_int))
        # self.register_instruction(cil.PrintStringNode(space))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_index_int))
        # self.register_instruction(cil.PrintStringNode(space))

        self.register_empty_instruction()
        self.register_comment("################################################################# #")
        self.register_comment("Step 5 - Using the minimun ancestor index find the correct branch #")
        self.register_comment("################################################################# #")
        bool_array = self.define_internal_local("Step 5 - Bool array")
        self.register_instruction(cil.ArrayNode(bool_array, constant_len_types_int).set_comment("Create the bool array"))
        for i, _ in enumerate(types):
            x = self.define_internal_local(f"Step 5 - Branch {i}")
            self.register_instruction(cil.AllocateIntNode(x, f"{i}"))
            self.register_instruction(cil.SetValueInIndexNode(bool_array, x, constant_zero_int).set_comment("Initialize the bool array"))
            # self.register_instruction(cil.GetValueInIndexNode(constant_zero_int, bool_array, x))
            # self.register_instruction(cil.PrintIntNode(constant_zero_int))

        self.register_empty_instruction()
        exists_error_bool = self.define_internal_local("Step 5 - Exists an error")
        self.register_instruction(cil.AllocateBoolNode(exists_error_bool, "0"))
        
        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_equal", exists_error_bool, 2))
        # self.register_instruction(cil.PrintIntNode(exists_error_bool))

        self.register_instruction(cil.GotoIfNode(exists_error_bool, f"error_branch_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(bool_array, step4_current_min_index_int, constant_one_int).set_comment("Set the bool array in the correct index to 1"))
        # self.register_instruction(cil.PrintStringNode(endl))
        # self.register_instruction(cil.PrintIntNode(step4_current_min_index_int))
        # self.register_instruction(cil.PrintStringNode(space))
        
        step5_comparison = self.define_internal_local("Step 5 - Comparison for the correct branch result")
        self.register_instruction(cil.AllocateBoolNode(step5_comparison, "0"))
        self.register_empty_instruction()
        for i_int, t in enumerate(types):
            x = self.define_internal_local(f"Index {i_int}")
            self.register_instruction(cil.AllocateIntNode(x, f"{i_int}"))
            self.register_instruction(cil.GetValueInIndexNode(step5_comparison, bool_array, x).set_comment(f"Get the bool value of the branch {t.name}"))
            self.register_instruction(cil.GotoIfNode(step5_comparison, f"branch_{t.name}_{node_id}").set_comment("If the bool value is 1, then we have a match"))
            self.register_empty_instruction()

        resutl_address = self.define_internal_local("Result of the switch expression address")
        for i_int, (var_name, type_name, expr) in enumerate(node.cases):
            self.register_instruction(cil.LabelNode(f"branch_{type_name}_{node_id}"))
            var = self.register_local(var_name, f"Specialiced variable for the branch {type_name}")
            self.register_instruction(cil.ArgNode(var, 0, 2))
            self.register_instruction(cil.ArgNode(swicth_expression, 1, 2))
            self.register_instruction(cil.StaticCallNode("function_assign", var, 2))
            
            expr_source, _ = self.visit(expr, scope.children[i_int])
            self.register_instruction(cil.ArgNode(resutl_address, 0, 2))
            self.register_instruction(cil.ArgNode(expr_source, 1, 2))
            self.register_instruction(cil.StaticCallNode("function_assign", resutl_address, 2))
            self.register_instruction(cil.AssignNode(resutl_address, expr_source).set_comment("Assign the result"))
            self.register_instruction(cil.GotoNode(f"branch_end_{node_id}"))
            self.register_empty_instruction()
        self.register_instruction(cil.LabelNode(f"error_branch_{node_id}"))
        self.register_comment("Insert an error call")
        self.register_instruction(cil.LabelNode(f"branch_end_{node_id}"))

        return resutl_address, Type.multi_join(types)

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        scope = node.scope
        obj_source, obj_type = self.visit(node.obj, scope)
        if obj_type.name == "SELF_TYPE":
            obj_type = self.current_type

        args_sources = []
        for arg in node.args:
            arg_source, _ = self.visit(arg, scope)
            args_sources.append(arg_source)

        self.register_instruction(cil.ArgNode(obj_source, 0, len(args_sources) + 1))
        for index, arg_source in enumerate(args_sources, start=1):
            self.register_instruction(cil.ArgNode(arg_source, index, len(args_sources) + 1))

        call_dest = self.define_internal_local()
        method, owner = obj_type.get_method(node.id, get_owner=True)
        
        self.register_instruction(
            cil.DynamicCallNode(
                obj_type.name, self.to_function_name(node.id, owner.name), call_dest, len(args_sources) + 1
            )
        )
        return call_dest, method.return_type

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        scope = node.scope
        local_int = self.define_internal_local(f"Integer {node.lex}")
        self.register_instruction(cil.AllocateIntNode(local_int, node.lex))
        return local_int, self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        scope = node.scope
        local_str_var = self.define_internal_local(f"String {node.lex}")
        self.register_instruction(cil.AllocateStrNode(local_str_var, node.lex))
        return local_str_var, self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        scope = node.scope
        local_bool_var = self.define_internal_local(f"Boolean {node.lex}")
        self.register_instruction(cil.AllocateBoolNode(local_bool_var, ("1" if node.lex == "true" else "0")))
        return local_bool_var, self.context.get_type("Bool")

    @visitor.when(ecool.NullNode)
    def visit(self, node: ecool.NullNode, scope: Scope):
        scope = node.scope
        local_null_var = self.define_internal_local(f"Null")
        self.register_instruction(cil.AllocateNullPtrNode(local_null_var))
        return local_null_var, ecool.NullType

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        scope = node.scope
        variable = scope.find_variable(node.lex)
        variables = scope.find_all_variables(node.lex)

        is_attribute = (
            self.current_type.contains_attribute(node.lex) and len(variables) == 1
        )

        if is_attribute:
            dest = self.define_internal_local()
            attr_names = [a.name for a, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.GetAttributeNode(dest, "self", variable.name, attr_names.index(variable.name)))
            return dest, variable.type
        return variable.name, variable.type

    @visitor.when(cool.InstantiateNode)
    def visit(self, node: cool.InstantiateNode, scope: Scope):
        scope = node.scope
        local = self.define_internal_local(f"Store an instance of the class {node.lex}")
        self.register_instruction(cil.AllocateNode(node.lex, local).set_comment(f"Allocate the object {node.lex}"))
        self.register_instruction(cil.ArgNode(local, 0, 1).set_comment("Pass the instance to the constructor"))
        self.register_instruction(cil.DynamicCallNode(node.lex, self.to_function_name("__init__", node.lex), local, 1).set_comment("Call the constructor"))
        return local, self.context.get_type(node.lex)

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        scope = node.scope
        source, _ = self.visit(node.expr, scope)
        local_int = self.define_internal_local("Integer 1")
        result = self.define_internal_local(f"Store the negation of {source}")
        self.register_instruction(cil.AllocateIntNode(local_int, "1"))
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(local_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_xor", result, 2))
        # self.register_instruction(cil.AllocateIntNode(result, "0"))
        # self.register_instruction(cil.XorNode(result, source, local_int).set_comment(f"not {source}"))
        return result, self.context.get_type("Bool")

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        scope = node.scope
        source, _ = self.visit(node.expr, scope)
        local_int_0 = self.define_internal_local("Integer 1")
        local_int_1 = self.define_internal_local(f"Integer {2**32 - 1}")
        result = self.define_internal_local(f"Store the complement a2 of {source}")
        self.register_instruction(cil.AllocateIntNode(local_int_0, "1"))
        self.register_instruction(cil.AllocateIntNode(local_int_1, str(2**32 - 1)))
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(local_int_1, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_xor", result, 2))
        # self.register_instruction(cil.PrintIntNode(result))
        # self.register_instruction(cil.AllocateIntNode(result, "0"))
        # self.register_instruction(cil.XorNode(result, source, local_int_1).set_comment(f"Getting the complement a1 of {source}"))
        self.register_instruction(cil.ArgNode(result, 0, 2))
        self.register_instruction(cil.ArgNode(local_int_0, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", result, 2))
        # self.register_instruction(cil.PrintIntNode(result))
        # self.register_instruction(cil.PlusNode(result, result, local_int_0).set_comment(f"Adding 1 to the complement a1 we get the complement a2 of {source}")) 
        return result, self.context.get_type("Int")
    
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        scope = node.scope
        source, _ = self.visit(node.expr, scope)
        null_ptr = self.define_internal_local("Null pointer")
        result = self.define_internal_local(f"Store if {source} is NULL")
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.AllocateNullPtrNode(null_ptr))
        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(source, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_equal", result, 2))
        return result, self.context.get_type("Bool")

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_add", "Int")  

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_sub", "Int")  

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_mult", "Int")  

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_div", "Int")  

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_less_than_or_equal", "Bool")  

    @visitor.when(cool.LessThanNode)
    def visit(self, node: cool.LessThanNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_less_than", "Bool")  

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_equal", "Bool")       

    def visit_arith_node(
        self, node: cool.BinaryNode, scope: Scope, operation_function: str, return_type_name: str = "Int"
    ) -> Tuple[str, Type]:
        left, _ = self.visit(node.left, scope)
        right, _ = self.visit(node.right, scope)
        dest = self.define_internal_local(f"Store the result of the operation {operation_function}")
        self.register_empty_instruction()
        self.register_instruction(cil.ArgNode(left, 0, 2))
        self.register_instruction(cil.ArgNode(right, 1, 2))
        self.register_instruction(cil.StaticCallNode(operation_function, dest, 2))
        return dest, self.context.get_type(return_type_name)
