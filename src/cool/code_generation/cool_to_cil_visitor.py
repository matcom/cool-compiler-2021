from typing import Dict, List, Optional, Tuple

import cool.code_generation.cil as cil
import cool.code_generation.icool as icool
import cool.semantics.utils.astnodes as cool
import cool.semantics.utils.errors as err
import cool.visitor as visitor
import cool.visitor.visitor as visitor
from cool.code_generation.base import BaseCOOLToCILVisitor
from cool.semantics import TypeChecker
from cool.semantics.utils.scope import (
    Attribute,
    Context,
    ErrorType,
    Method,
    Scope,
    SemanticError,
    Type,
)


class ICoolTranslator:
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

        # Added the Type
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
                    icool.NullNode()
                )  # cool.WhileNode(cool.BooleanNode("false"), cool.IntegerNode("0"))

            return cool.AssignNode(node.id, expr)

        return cool.AssignNode(node.id, node.expr)


class ICoolTypeChecker:
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

        for elem in node.declarations:
            self.visit(elem, scope.create_child())

        return scope

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
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

            # if scope.is_local(_id):
            #     feature = self.current_method or self.current_attribute
            #     self.errors.append(
            #         err.LOCAL_ALREADY_DEFINED
            #         % (node.line, node.column, _id, feature.name)
            #     )
            # else:
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
        return_type = ErrorType()
        for expr in node.expressions:
            return_type = self.visit(expr, scope)
        return return_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
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
        return self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        return self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        return self.context.get_type("Bool")

    @visitor.when(icool.NullNode)
    def visit(self, node: icool.NullNode, scope: Scope):
        return icool.NullType()

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
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
        return self._check_unary_operation(
            node, scope, "not", self.context.get_type("Bool")
        )

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        return self._check_unary_operation(
            node, scope, "~", self.context.get_type("Int")
        )

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        self.visit(node.expr, scope)
        return self.context.get_type("Bool")

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "+", self.context.get_type("Int")
        )

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "-", self.context.get_type("Int")
        )

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "*", self.context.get_type("Int")
        )

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "/", self.context.get_type("Int")
        )

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "<=", self.context.get_type("Bool")
        )

    @visitor.when(cool.LessThanNode)
    def visit(self, node: cool.LessThanNode, scope: Scope):
        return self._check_int_binary_operation(
            node, scope, "<", self.context.get_type("Bool")
        )

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
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


# Notes:
# 1 - All the expression nodes are going to return a tuple [str, Type]


class CoolToCilTranslator(BaseCOOLToCILVisitor):
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        for i, declaration in enumerate(node.declarations):
            self.visit(declaration, scope.children[i])

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(self.current_type.name)

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
        pass

    @visitor.when(cool.MethodDeclarationNode)
    def visit(self, node: cool.MethodDeclarationNode, scope: Scope):
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
        i = 0
        for name, _, expr in node.declarations:
            self.register_local(name)

            if expr:
                source, _ = self.visit(expr, scope.children[i])
                if source:
                    self.register_instruction(cil.AssignNode(name, source))
                i += 1

        source, t = self.visit(node.expr, scope.children[i])

        return source, t

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        variable = scope.find_variable(node.id)
        variables = scope.find_all_variables(node.id)
        source, _ = self.visit(node.expr, scope)

        is_attribute = (
            self.current_type.contains_attribute(node.id) and len(variables) == 1
        )

        if is_attribute:
            self.register_instruction(cil.SetAttribNode("self", variable.name, source))
        else:
            self.register_instruction(cil.AssignNode(variable.name, source))

        return variable.name, variable.type

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        source, inst_type = None, None
        for expr in node.expressions:
            source, inst_type = self.visit(expr, scope)
        return source, inst_type

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        obj_source, obj_type = self.visit(node.obj, scope)

        args_sources = []
        for arg in node.args:
            arg_source, _ = self.visit(arg, scope)
            args_sources.append(arg_source)

        self.register_instruction(cil.ArgNode(obj_source))
        for arg_source in args_sources:
            self.register_instruction(cil.ArgNode(arg_source))

        call_dest = self.define_internal_local()
        method = obj_type.get_method(node.id)
        self.register_instruction(
            cil.DynamicCallNode(
                obj_type.name, self.to_function_name(node.id, obj_type.name), call_dest
            )
        )
        return call_dest, method.return_type

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        return node.lex, self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        return node.lex, self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        return node.lex, self.context.get_type("Bool")

    @visitor.when(icool.NullNode)
    def visit(self, node: icool.NullNode, scope: Scope):
        return node.lex, icool.NullType()

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        variable = scope.find_variable(node.lex)
        variables = scope.find_all_variables(node.lex)

        is_attribute = (
            self.current_type.contains_attribute(node.lex) and len(variables) == 1
        )

        if is_attribute:
            dest = self.define_internal_local()
            self.register_instruction(cil.GetAttribNode(dest, "self", variable.name))
            return dest, variable.type
        return variable.name, variable.type

    @visitor.when(cool.InstantiateNode)
    def visit(self, node: cool.InstantiateNode, scope: Scope):
        local = self.define_internal_local()
        self.instructions.append(cil.AllocateNode(node.lex, local))
        return local, self.context.get_type(node.lex)

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.PlusNode)

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.MinusNode)

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.StarNode)

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.DivNode)

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.LessEqualNode)

    @visitor.when(cool.LessThanNode)
    def visit(self, node: cool.LessThanNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.LessThanNode)

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        return self.visit_arith_node(node, scope, cil.EqualNode)


    def visit_arith_node(
        self, node: cool.BinaryNode, scope: Scope, cil_type: type
    ) -> Tuple[str, Type]:
        left, _ = self.visit(node.left, scope)
        right, _ = self.visit(node.right, scope)
        dest = self.define_internal_local()
        self.register_instruction(cil_type(dest, left, right))
        return dest, self.context.get_type("Int")
