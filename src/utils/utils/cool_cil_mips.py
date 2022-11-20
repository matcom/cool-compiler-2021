from atexit import register
from copy import deepcopy
from typing import Any, Dict, List, Optional, Tuple, Union

from .semantic import *

from . import ast_nodes as cool
from . import ast_nodes_cil as cil
from . import ast_nodes_mips as mips

from . import visitor
from .code_generation import NullNode, NullType



class ExtendedCoolTranslator:
    
    def __init__(self, context: Context):
        self.current_type = None
        self.current_method = None
        self.context = context
        self.class_declarations = {}  # type: Dict[str, cool.ClassDecNode]

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        declarations: List[cool.ClassDecNode] = []

        default_class_names = ["Object", "IO",  "String", "Int", "Bool"]
        for name in default_class_names:
            t = self.context.get_type(name)
            t.define_method("__init__", [], [], t)
            t.methods_dict.move_to_end("__init__", last=False)

        for declaration in node.class_list:
            self.class_declarations[declaration.name] = declaration

        for declaration in node.class_list:
            declarations.append(self.visit(declaration))

        return cool.ProgramNode(declarations)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        ancestors = [
            self.class_declarations[owner.name]
            for _, owner in self.current_type.all_attributes()
        ]

        attrs = []
        visited = set()
        for ancestor in ancestors:
            if ancestor.name in visited:
                continue

            visited.add(ancestor.name)
            attrs += [
                feature
                for feature in ancestor.data
                if isinstance(feature, cool.AttributeDecNode)
            ]

        expressions: List[cool.ExprNode] = []
        for attr in attrs:
            expressions.append(self.visit(attr))
        expressions.append(cool.VariableNode("self"))

        body = cool.BlockNode(expressions)
        constructor = cool.MethodDecNode(
            "__init__", self.current_type.name, body, []
        )

        self.current_type.define_method("__init__", [], [], self.current_type)
        self.current_type.methods_dict.move_to_end("__init__", last=False)

        attrs = [
            feature
            for feature in node.data
            if isinstance(feature, cool.AttributeDecNode)
        ]
        methods = [
            feature
            for feature in node.data
            if isinstance(feature, cool.MethodDecNode)
        ]

        features = attrs + [constructor] + methods

        return cool.ClassDecNode(node.name, features, node.parent)

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode):
        if node.expr is None:
            expr = None
            if node._type == "Int":
                expr = cool.NumberNode("0")
            elif node._type == "Bool":
                expr = cool.BooleanNode("false")
            elif node._type == "String":
                expr = cool.StringNode('""')
            else:
                expr = NullNode()
            return cool.AssignNode(node.name, expr)
        return cool.AssignNode(node.name, deepcopy(node.expr))


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

        for elem in node.class_list:
            self.visit(elem, scope.create_child())

        return scope

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.name)

        attrs = [feature for feature in node.data if isinstance(feature, cool.AttributeDecNode)]
        methods = [feature for feature in node.data if isinstance(feature, cool.MethodDecNode)]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        node.scope = scope
        if node.name == "self":
            'error'

        try:
            attr_type = (self.context.get_type(node._type) \
                if node._type != "SELF_TYPE" else self.current_type)
        except SemanticError:
            attr_type = ErrorType()

        scope.define_variable("self", self.current_type)

        # set the current attribute for analyze the body
        # and set the self.current_method variable to None
        self.current_attribute = self.current_type.get_attribute(node.name)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                line, column = node.expr_position
                self.errors.append('error')
        
        scope.define_variable(node.name, attr_type)

    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope: Scope):
        node.scope = scope
        return self.visit(node.expr, scope)

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        node.scope = scope
        self.current_method = self.current_type.get_method(node.name)
        self.current_attribute = None

        # Parameters can hide the attribute declaration, that's why we are not checking if there is defined,
        # instead we are checking for local declaration. Also it is checked that the static type of a parameter is
        # different of SELF_TYPE.

        scope.define_variable("self", self.current_type)

        for param_name, param_type in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            if not scope.is_local_variable(param_name):
                if param_type.name == "SELF_TYPE":
                    self.errors.append('error')
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
                    'error'
                )

        try:
            return_type = (
                self.context.get_type(node.type)
                if node.type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError:
            return_type = ErrorType()

        expr_type = self.visit(node.expr, scope)

        if not expr_type.conforms_to(return_type):
            self.errors.append(
                'error'
            )

    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope):
        scope = node.scope
        parnode = self.visit(node.expr, scope)
        return parnode

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        node.scope = scope
        for i, (_id, _type, _expr) in enumerate(node.declaration):
            if _id == "self":
                line, column = node.dec_names_pos[i]
                self.errors.append('error')
                continue

            try:
                var_static_type = (
                    self.context.get_type(_type)
                    if _type != "SELF_TYPE"
                    else self.current_type
                )
            except SemanticError:
                line, column = node.dec_types_pos[i]
                self.errors.append('error')
                var_static_type = ErrorType()

            scope.define_variable(_id, var_static_type)

            expr_type = (
                self.visit(_expr, scope.create_child()) if _expr is not None else None
            )
            if expr_type is not None and not expr_type.conforms_to(var_static_type):
                self.errors.append('error')

        return self.visit(node.expr, scope.create_child())

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        node.scope = scope
        var_info = scope.find_variable(node.idx)

        if var_info.name == "self":
            self.errors.append('error')

        expr_type = self.visit(node.expr, scope)

        if var_info is None:
            self.errors.append(
                'error'
            )
        else:
            if not expr_type.conforms_to(var_info.type):
                self.errors.append(
                    'error'
                )

        return expr_type

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        node.scope = scope
        return_type = ErrorType()
        for expr in node.expr:
            return_type = self.visit(expr, scope)
        return return_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        node.scope = scope
        if_type = self.visit(node.if_expr, scope)
        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)
        if if_type != self.context.get_type("Bool"):
            self.errors.append('error')
        return then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        node.scope = scope
        condition = self.visit(node.cond, scope)
        if condition != self.context.get_type("Bool"):
            self.errors.append('error')

        self.visit(node.data, scope)
        return self.context.get_type("Object")

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        types = []
        visited = set()
        for i, (identifier, type_name, expr) in enumerate(node.params):
            new_scope = scope.create_child()
            try:
                if type_name != "SELF_TYPE":
                    new_scope.define_variable(identifier, self.context.get_type(type_name))
                else:
                    self.errors.append('error')
            except SemanticError:
                new_scope.define_variable(identifier, ErrorType())
                line, column = node.cases_positions[i]
                self.errors.append('error')

            # Cannot be dublicate Branches types
            if type_name in visited:
                line, column = node.cases_positions[i]
                self.errors.append('error')

            visited.add(type_name)
            types.append(self.visit(expr, new_scope))

        return Type.multi_join(types)

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        node.scope = scope
        if node.atom is None:
            node.atom = cool.VariableNode("self")
        obj_type = self.visit(node.atom, scope)

        if node.type is not None:
            try:
                ancestor_type = self.context.get_type(node.type)
            except SemanticError:
                ancestor_type = ErrorType()
                line, column = node.type_position
                self.errors.append('error')

            if not obj_type.conforms_to(ancestor_type):
                line, column = node.type_position
                self.errors.append('error')
        else:
            ancestor_type = obj_type

        try:
            method = ancestor_type.get_method(node.idx)
        except SemanticError:
            line, column = node.id_position
            self.errors.append('error')

            for arg in node.exprlist:
                self.visit(arg, scope)
            return ErrorType()

        args_count = len(node.exprlist)
        params_count = len(method.param_names)
        if args_count != params_count:
            line, column = node.id_position
            self.errors.append('error')

        number_of_args = min(args_count, params_count)
        for i, arg in enumerate(node.exprlist[:number_of_args]):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(method.param_types[i]):
                line, column = node.exprlist_positions[i]
                self.errors.append('error')

        return (
            method.return_type
            if method.return_type.name != "SELF_TYPE"
            else ancestor_type
        )

    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
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

    @visitor.when(NullNode)
    def visit(self, node: NullNode, scope: Scope):
        node.scope = scope
        return NullType()

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        node.scope = scope
        variable = scope.find_variable(node.lex)
        if variable is None:
            if self.current_attribute is not None:
                name = self.current_attribute.name
            else:
                name = self.current_method.name

            self.errors.append('error')
            return ErrorType()
        return variable.type

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        node.scope = scope
        try:
            return (
                self.context.get_type(node.type)
                if node.type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError as e:
            line, column = node.type_position
            self.errors.append('error')
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

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
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

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
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
        if (left_type.name in basic_types or left_type.name in basic_types\
            ) and left_type.name != right_type.name:
            self.errors.append('error')
        return self.context.get_type("Bool")

    def _check_int_binary_operation(
        self, node: cool.BinaryNode, scope: Scope, operation: str, return_type: Type
    ):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type == right_type == self.context.get_type("Int"):
            return return_type
        self.errors.append('error')
        return ErrorType()

    def _check_unary_operation(
        self, node: cool.UnaryNode, scope: Scope, operation: str, expected_type: Type
    ):
        typex = self.visit(node.expr, scope)
        if typex == expected_type:
            return typex
        self.errors.append('error')
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
    def params(self) :
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self) :
        return self.current_function.instructions

    def register_local(self, var_name: str, comment: str = "") :
        local_name = (f"local_{self.current_function.name[9:]}_{var_name}_{len(self.localvars)}")
        local_name = var_name
        local_node = cil.LocalNode(local_name).set_comment(comment)
        self.localvars.append(local_node)
        return local_name

    def define_internal_local(self, comment: str = "") :
        return self.register_local(f"internal_{len(self.localvars)}", comment)

    def register_instruction(self, instruction) :
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name: str, type_name: str) :
        return f"function_{method_name}_at_{type_name}"

    def register_function(self, function_name: str):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name: str, parent_name: Optional[str] = None):
        type_node = cil.TypeNode(name, parent_name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value: Any) :
        data_name = f"data_{len(self.dotdata)}"
        data_node = cil.DataNode(data_name, value)
        self.dotdata.append(data_node)
        return data_node

    def register_comment(self, comment: str):
        self.register_instruction(cil.CommentNode(comment))
    
    def register_empty_instruction(self):
        self.register_instruction(cil.EndOfLineNode())

    def add_function_main(self):
        self.current_function = self.register_function("main")
        local_main = self.define_internal_local()
        local_result = self.define_internal_local()
        method_index = self.define_internal_local()
        method_address = self.define_internal_local()

        self.register_instruction(cil.AllocateNode("Main", local_main))
        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.StaticCallNode(self.to_function_name("__init__", "Main"), local_main, 1))
        self.register_empty_instruction()

        
        all_methods = methods_declaration_order(self.context.get_type("Main"))
        i = [m.name for m, _ in all_methods].index("main")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, local_main, method_index, "main", "Main"))

        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.DynamicCallNode("Main", method_address, local_result, 1))
        
        #########
        self.register_empty_instruction()
        self.register_instruction(cil.HaltNode())

    def add_function_add(self):
        self.current_function = self.register_function("function_add")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Adding result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.PlusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

    def add_function_sub(self):
        self.current_function = self.register_function("function_sub")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Substracting result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.MinusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))

    def add_function_mul(self):
        self.current_function = self.register_function("function_mult")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Multiting result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.StarNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
    
    def add_function_div(self):
        self.current_function = self.register_function("function_div")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Dividing result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.DivNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
    
    def add_function_xor(self):
        self.current_function = self.register_function("function_xor")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Xor result")
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.XorNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
    
    def add_function_less_than(self):
        self.current_function = self.register_function("function_less_than")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Less than result")
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessThanNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
    
    def add_function_less_than_or_equal(self):
        self.current_function = self.register_function("function_less_than_or_equal")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local("Less than or equal result")
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessEqualNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
    
    def add_function_equal(self):
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
        self.register_instruction(cil.AllocateNullNode(constant_null))
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

    def add_function_assign(self): 
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
       
        self.register_instruction(cil.AllocateNullNode(constant_null))
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

    def add_function_init(self, type_name: str):
        self.current_function = self.register_function(self.to_function_name("__init__", type_name))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.ReturnNode("self"))

    def add_function_abort(self):
        self.current_function = self.register_function(self.to_function_name("abort", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        msg1 = self.define_internal_local()
        msg2 = self.define_internal_local()
        msg = self.define_internal_local()
        endl = self.define_internal_local()
        method_index = self.define_internal_local()
        method_address = self.define_internal_local()
        
        self.register_instruction(cil.AllocateStringNode(msg1, "\"Abort called from class \""))
        self.register_instruction(cil.AllocateStringNode(endl, "\"\\n\""))
        
        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("type_name")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "type_name", "String"))

        self.register_instruction(cil.ArgNode("self", 0, 1))
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg2, 1))
       
        
        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("concat")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "concat", "String"))

        self.register_instruction(cil.ArgNode(msg1, 0, 2))
        self.register_instruction(cil.ArgNode(msg2, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg, 2))

        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("concat")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "concat", "String"))

        self.register_instruction(cil.ArgNode(msg, 0, 2))
        self.register_instruction(cil.ArgNode(endl, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg, 2))

        self.register_instruction(cil.PrintStringNode(msg))
        self.register_instruction(cil.HaltNode())
        self.register_instruction(cil.ReturnNode("self"))

    def add_function_type_name(self):
        self.current_function = self.register_function(self.to_function_name("type_name", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        type_name = self.define_internal_local("type_name")
        self.register_instruction(cil.TypeNameNode(type_name, "self"))
        self.register_instruction(cil.ReturnNode(type_name))

    def add_function_copy(self):
        self.current_function = self.register_function(self.to_function_name("copy", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_copy = self.define_internal_local()
        self.register_instruction(cil.CopyNode(local_copy, "self"))
        self.register_instruction(cil.ReturnNode(local_copy))
#
    def add_function_out_string(self):
        self.current_function = self.register_function(self.to_function_name("out_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintStringNode("x"))
        self.register_instruction(cil.ReturnNode("self"))

    def add_function_out_int(self):
        self.current_function = self.register_function(self.to_function_name("out_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintIntNode("x"))
        self.register_instruction(cil.ReturnNode("self"))
    
    def add_function_in_string(self):
        self.current_function = self.register_function(self.to_function_name("in_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.ReadStringNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))
    
    def add_function_in_int(self):
        self.current_function = self.register_function(self.to_function_name("in_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(local_str, "0"))
        self.register_instruction(cil.ReadIntNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))

    def add_function_length(self):
        self.current_function = self.register_function(self.to_function_name("length", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        len_local =  self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(len_local, "0"))
        self.register_instruction(cil.LengthNode(len_local, "self"))
        self.register_instruction(cil.ReturnNode(len_local))

    def add_function_concat(self):
        self.current_function = self.register_function(self.to_function_name("concat", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("s"))
        new_str =  self.define_internal_local()
        self.register_instruction(cil.ConcatNode(new_str, "self", "s"))
        self.register_instruction(cil.ReturnNode(new_str))

    def add_function_substr(self):
        self.current_function = self.register_function(self.to_function_name("substr", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("i"))
        self.current_function.params.append(cil.ParamNode("l"))
        substr =  self.define_internal_local()
        self.register_instruction(cil.SubstringNode(substr, "self", "i", "l"))            
        self.register_instruction(cil.ReturnNode(substr))
#
    def debug_print_type(self, source: str):
        endl = self.define_internal_local()
        dest = self.define_internal_local()
        self.register_instruction(cil.AllocateStringNode(endl, '"\\n"'))
        self.register_instruction(cil.ArgNode(source, 0, 1))
        self.register_instruction(cil.StaticCallNode("function_type_name_at_Object", dest, 1))
        self.register_instruction(cil.PrintStringNode(dest))
        self.register_instruction(cil.PrintStringNode(endl))


def methods_declaration_order(t: Type):
    method_decl = []
    all_methods = t.all_methods()
    visited = set()
    for method, _ in all_methods:
        if method.name in visited:# or method.name == 'get_type':
            continue
        
        meths = list(all_methods)[::-1]
        method_decl.append(
            [(x, y) for x, y in meths if x.name == method.name][0]
        )
        visited.add(method.name)
    return method_decl

class CoolToCilTranslator(BaseCoolToCilVisitor):
    # Notes:
    # 1 - All the expression nodes are going to return a tuple [str, Type]
    
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        scope = node.scope
        default_class_names = ["Object", "IO",  "String", "Int", "Bool"]
        for name in default_class_names:
            current_type = self.context.get_type(name)
            self.current_type = current_type
            cil_type_node = self.register_type(current_type.name, current_type.parent.name if current_type.parent is not None else None)

            for method, ancestor in methods_declaration_order(current_type):
                cil_type_node.methods.append((method.name, self.to_function_name(method.name, ancestor.name)))
               
        self.add_function_add()
        self.add_function_sub()
        self.add_function_mul()
        self.add_function_div()
        self.add_function_xor()
        self.add_function_less_than()
        self.add_function_less_than_or_equal()
        self.add_function_equal()
        self.add_function_assign()

        self.add_function_init("Object")
        self.add_function_abort()
        self.add_function_type_name()
        self.add_function_copy()

        self.add_function_init("IO")
        self.add_function_out_string()
        self.add_function_out_int()
        self.add_function_in_string()
        self.add_function_in_int()
        
        self.add_function_init("String")
        self.add_function_length()
        self.add_function_concat()
        self.add_function_substr()
        
        self.add_function_init("Int")
        self.add_function_init("Bool")

        for i, declaration in enumerate(node.class_list):
            self.visit(declaration, scope.children[i])

        self.add_function_main()

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        scope = node.scope
        self.current_type = self.context.get_type(node.name)

        type_node = self.register_type(self.current_type.name, self.current_type.parent.name)

        attrs = [
            feature
            for feature in node.data
            if isinstance(feature, cool.AttributeDecNode)
        ]

        methods = [
            feature
            for feature in node.data
            if isinstance(feature, cool.MethodDecNode)
        ]

        for attr, _ in self.current_type.all_attributes():
            self.visit(attr, scope)
            type_node.attributes.append(attr.name)

        for method, t in methods_declaration_order(self.current_type):
            type_node.methods.append((method.name, self.to_function_name(method.name, t.name)))

        i = len([attr for attr in attrs if attr.expr is not None])
        for i, method in enumerate(methods, start=i):
            self.visit(method, scope.children[i])

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        scope = node.scope
        pass

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        scope = node.scope
        self.current_method, owner_type = self.current_type.get_method(
            node.name, owner=True
        )
        function_name = self.to_function_name(self.current_method.name, owner_type.name)
        self.current_function = self.register_function(function_name)

        self.current_function.params = [cil.ParamNode("self")] + [
            cil.ParamNode(param_name[0]) for param_name in node.params
        ]

        source, _ = self.visit(node.expr, scope)

        self.register_instruction(cil.ReturnNode(source))

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        scope = node.scope
        x = " ".join([f"{name}: {type_name}" for name, type_name, _ in node.declaration])
        self.register_comment(f"Let {x}")
        
        i = 0
        for name, type_name, expr in node.declaration:
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
                    self.register_instruction(cil.AllocateStringNode(name, "\"\""))
                else:
                    self.register_instruction(cil.AllocateNullNode(name))
        source, t = self.visit(node.expr, scope.children[i])

        return source, t

    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope: Scope):
        scope = node.scope
        return self.visit(node.expr, scope)

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        scope = node.scope
        variable = scope.find_variable(node.idx)
        variables = scope.find_all_variables_with_name(node.idx)
        source, _ = self.visit(node.expr, scope)

        self.register_empty_instruction()
        is_attribute = (
            self.current_type.contains_attribute(node.idx) and len(variables) == 1
        )

        if is_attribute:
            attr_names = [attr.name for attr, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.SetAttribNode("self", variable.name, source, attr_names.index(variable.name)))
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
        for expr in node.expr:
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

        self.register_instruction(cil.EndOfLineNode())
        self.register_instruction(cil.LabelNode(f"then_{node_id}"))
        then_source, then_type = self.visit(node.then_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, then_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EndOfLineNode())
        self.register_instruction(cil.LabelNode(f"else_{node_id}"))
        else_source, else_type = self.visit(node.else_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, else_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EndOfLineNode())
        self.register_instruction(cil.LabelNode(f"endif_{node_id}"))

        return result_address, then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        scope = node.scope
        node_id = hash(node)
        result_addres = self.define_internal_local()
        self.register_empty_instruction()
        self.register_comment(f"While loop")

        self.register_instruction(cil.AllocateNullNode(result_addres))
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))

        conditional_source, _ = self.visit(node.cond, scope)
        self.register_instruction(cil.GotoIfNode(conditional_source, f"while_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"while_end_{node_id}"))

        self.register_instruction(cil.EndOfLineNode())
        self.register_instruction(cil.LabelNode(f"while_body_{node_id}"))
        self.visit(node.data, scope)
        self.register_instruction(cil.GotoNode(f"while_start_{node_id}"))

        self.register_instruction(cil.EndOfLineNode())
        self.register_instruction(cil.LabelNode(f"while_end_{node_id}"))

        return result_addres, self.context.get_type("Object")

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        scope = node.scope
        node_id = hash(node)
        swicth_expression, _ = self.visit(node.expr, scope)

        constant_zero_int = self.define_internal_local("Constant Integer 0 ")
        constant_one_int = self.define_internal_local("Constant Integer 1")
        constant_len_types_int = self.define_internal_local(f"Constant Integer {len(node.params)}")
        constant_null_ptr = self.define_internal_local("Null pointer")
        count_of_ancestors_int = self.define_internal_local("Count of ancestors of the switch expression")
        step1_comparison_result_bool = self.define_internal_local("Step 1 comparison result")
        switch_expr_type_address = self.define_internal_local("Switch expression type")
        ancestor_type_address = self.define_internal_local("Ancestor type")
        ancestors_array = self.define_internal_local("Step 1 Array of ancestors")

        self.register_instruction(cil.AllocateIntNode(constant_zero_int, "0"))
        self.register_instruction(cil.AllocateIntNode(constant_one_int, "1"))
        self.register_instruction(cil.AllocateIntNode(constant_len_types_int, str(len(node.params))))
        self.register_instruction(cil.AllocateNullNode(constant_null_ptr))
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
        
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))
        self.register_instruction(cil.EqualAddressNode(step1_comparison_result_bool, ancestor_type_address, constant_null_ptr))
        self.register_instruction(cil.GotoIfNode(step1_comparison_result_bool, f"while_end_{node_id}"))

        self.register_comment("Increment the count of ancestors")
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", count_of_ancestors_int, 2))

        self.register_instruction(cil.ParentNode(ancestor_type_address, ancestor_type_address))
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
        self.register_instruction(cil.LabelNode(f"foreach_start_{node_id}"))

        self.register_instruction(cil.ArgNode(step2_iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step2_comparison_result_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(step2_comparison_result_bool, f"foreach_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_body_{node_id}"))
        self.register_instruction(cil.SetIndexNode(ancestors_array, step2_iter_index_int, ancestor_type_address).set_comment("Set the index of the array with the ancestor type"))
        self.register_instruction(cil.ParentNode(ancestor_type_address, ancestor_type_address).set_comment("Get the next ancestor"))
    

        self.register_instruction(cil.ArgNode(step2_iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", step2_iter_index_int, 2))
        
        self.register_instruction(cil.GotoNode(f"foreach_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_end_{node_id}"))
        self.register_empty_instruction()
        # ###########################################################################
        # # End Foreach to create the array of ancestors and fill it with the types #
        # ###########################################################################

        
        self.register_comment("#################################################################################################### #")
        self.register_comment("Step 3 - For each branch type, store the ancestor index that match with it (Simulating a double for) #")
        self.register_comment("#################################################################################################### #")
        
        types = [self.context.get_type(type_name) for _, type_name, _ in node.params]
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
            self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i, count_of_ancestors_int))
            
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

        self.register_comment("############# #")
        self.register_comment("Outer Foreach #")
        self.register_comment("############# #")
        self.register_instruction(cil.LabelNode(f"foreach_type_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(i_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", comp_i_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(comp_i_bool, f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_type_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_i, type_branch_array, i_int).set_comment("Get the type of the i-th branch"))
        
        #################
        # Inner Foreach #
        #################
        self.register_empty_instruction()
        self.register_comment("############# #")
        self.register_comment("Inner Foreach #")
        self.register_comment("############# #")
        
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_zero_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", j_int, 2))

        self.register_instruction(cil.LabelNode(f"foreach_ancestor_start_{node_id}"))

        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", comp_j_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(comp_j_bool, f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_j, ancestors_array, j_int).set_comment("Get the j-th ancestor type"))

        self.register_instruction(cil.EqualAddressNode(types_comparison_bool, type_i, type_j).set_comment("Compare if the type of the i-th branch is equal to the j-th ancestor"))
        self.register_instruction(cil.GotoIfNode(types_comparison_bool, f"foreach_ancestor_end_{node_id}").set_comment("If the types are equal, we have a match, then we can exit"))
       
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", j_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i_int, j_int).set_comment("Set the counter of the i-th branch equals to j"))
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

        self.register_instruction(cil.AllocateIntNode(step4_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_current_min_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_temp_int, "0"))
        self.register_instruction(cil.AllocateIntNode(step4_current_min_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(step4_comparison_bool, "0"))

        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_int, 2))
        
        self.register_instruction(cil.LabelNode(f"foreach_min_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(step4_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step4_comparison_bool, 2))

        self.register_instruction(cil.GotoIfNode(step4_comparison_bool, f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GetValueInIndexNode(step4_temp_int, nearest_ancestor_array, step4_index_int).set_comment("Get the nearest ancestor index of the i-th branch type"))

        self.register_instruction(cil.ArgNode(step4_temp_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_current_min_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_less_than", step4_comparison_bool, 2)) 

        self.register_instruction(cil.GotoIfNode(step4_comparison_bool, f"update_min_{node_id}"))
        self.register_instruction(cil.GotoNode(f"update_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"update_min_{node_id}"))
        
        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_temp_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_int, 2))

        self.register_instruction(cil.ArgNode(step4_current_min_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(step4_index_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_assign", step4_current_min_index_int, 2))

        self.register_instruction(cil.LabelNode(f"update_min_end_{node_id}"))
        self.register_instruction(cil.ArgNode(step4_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(constant_one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", step4_index_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_min_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_end_{node_id}"))

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

        self.register_empty_instruction()
        exists_error_bool = self.define_internal_local("Step 5 - Exists an error")
        self.register_instruction(cil.AllocateBoolNode(exists_error_bool, "0"))
        
        self.register_instruction(cil.ArgNode(step4_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_equal", exists_error_bool, 2))

        self.register_instruction(cil.GotoIfNode(exists_error_bool, f"error_branch_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(bool_array, step4_current_min_index_int, constant_one_int).set_comment("Set the bool array in the correct index to 1"))
 
        
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
        for i_int, (var_name, type_name, expr) in enumerate(node.params):
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
        obj_source, obj_type = self.visit(node.atom, scope)
        if obj_type.name == "SELF_TYPE":
            obj_type = self.current_type

        ancestor_call = False
        if node.type is not None:
            ancestor_call = True
            obj_type = self.context.get_type(node.type)

        args_sources = []
        for arg in node.exprlist:
            arg_source, _ = self.visit(arg, scope)
            args_sources.append(arg_source)

        all_methods = methods_declaration_order(obj_type)
        i = [m.name for m, _ in all_methods].index(node.idx)
        method = obj_type.get_method(node.idx)

        call_dest = self.define_internal_local("Function call destination")
        method_index = self.define_internal_local(f"Index of {method.name}")
        method_address = self.define_internal_local(f"Address of {method.name}")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, obj_source, method_index, method.name, obj_type.name))

        self.register_instruction(cil.ArgNode(obj_source, 0, len(args_sources) + 1))
        for index, arg_source in enumerate(args_sources, start=1):
            self.register_instruction(cil.ArgNode(arg_source, index, len(args_sources) + 1))

        if ancestor_call:
            self.register_instruction(cil.StaticCallNode(self.to_function_name(method.name, obj_type.name), call_dest, len(args_sources) + 1))
        else:
            self.register_instruction(cil.DynamicCallNode(obj_type.name, method_address, call_dest, len(args_sources) + 1))
        return call_dest, method.return_type

    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
        scope = node.scope
        local_int = self.define_internal_local(f"Integer {node.lex}")
        self.register_instruction(cil.AllocateIntNode(local_int, node.lex))
        return local_int, self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        scope = node.scope
        local_str_var = self.define_internal_local(f"String {node.lex}")
        self.register_instruction(cil.AllocateStringNode(local_str_var, node.lex))
        return local_str_var, self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        scope = node.scope
        local_bool_var = self.define_internal_local(f"Boolean {node.lex}")
        self.register_instruction(cil.AllocateBoolNode(local_bool_var, ("1" if node.lex == "true" else "0")))
        return local_bool_var, self.context.get_type("Bool")

    @visitor.when(NullNode)
    def visit(self, node: NullNode, scope: Scope):
        scope = node.scope
        local_null_var = self.define_internal_local(f"Null")
        self.register_instruction(cil.AllocateNullNode(local_null_var))
        return local_null_var, NullType

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        scope = node.scope
        variable = scope.find_variable(node.lex)
        variables = scope.find_all_variables_with_name(node.lex)

        is_attribute = (self.current_type.contains_attribute(node.lex) and len(variables) == 1)

        if is_attribute:
            dest = self.define_internal_local()
            attr_names = [a.name for a, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.GetAttribNode(dest, "self", variable.name, attr_names.index(variable.name)))
            return dest, variable.type
        return variable.name, variable.type

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        scope = node.scope
        local = self.define_internal_local(f"Store an instance of the class {node.type}")
        
        self.register_instruction(cil.AllocateNode(node.type, local).set_comment(f"Allocate the object {node.type}"))
        self.register_instruction(cil.ArgNode(local, 0, 1).set_comment("Pass the instance to the constructor"))
        self.register_instruction(cil.StaticCallNode(self.to_function_name("__init__", node.type), local, 1).set_comment("Call the constructor"))
        return local, self.context.get_type(node.type)

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
        
        self.register_instruction(cil.ArgNode(result, 0, 2))
        self.register_instruction(cil.ArgNode(local_int_0, 1, 2))
        self.register_instruction(cil.StaticCallNode("function_add", result, 2))
        return result, self.context.get_type("Int")
    
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        scope = node.scope
        
        source, _ = self.visit(node.expr, scope)
        null_ptr = self.define_internal_local("Null pointer")
        result = self.define_internal_local(f"Store if {source} is NULL")
        
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.AllocateNullNode(null_ptr))

        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(null_ptr, 1, 2))
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

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
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

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_less_than", "Bool")  

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "function_equal", "Bool")       

    def visit_arith_node(self, node: cool.BinaryNode, scope: Scope, operation_function: str, return_type_name: str = "Int"):# -> Tuple[str, Type]:
        left, _ = self.visit(node.left, scope)
        right, _ = self.visit(node.right, scope)
        dest = self.define_internal_local(f"Store the result of the operation {operation_function}")
        self.register_empty_instruction()
        self.register_instruction(cil.ArgNode(left, 0, 2))
        self.register_instruction(cil.ArgNode(right, 1, 2))
        self.register_instruction(cil.StaticCallNode(operation_function, dest, 2))
        return dest, self.context.get_type(return_type_name)



class BaseCilToMipsVisitor:
    def __init__(self, context: Context) -> None:
        self.dotdata: List[mips.DataNode] = []
        self.dottext: List[mips.InstructionNode] = []

        #
        self.current_function: Optional[cil.FunctionNode] = None
        self.current_function_stack: List[str] = []

        self.context = context

    def register_word(self, name: str, value: str) -> mips.WordDataNode:
        data = mips.WordDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_asciiz(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_space(self, name: str, value: str) -> mips.AsciizDataNode:
        data = mips.SpaceDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_instruction(self, instruction: mips.InstructionNode) -> mips.InstructionNode:
        self.dottext.append(instruction)
        return instruction

    def register_empty_instruction(self) -> mips.EmptyInstructionNode:
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]

    def register_empty_data(self):
        self.dotdata.append(mips.EmptyDataNode())

    def register_comment(self, comment: str) -> mips.CommentNode:
        self.dottext.append(mips.CommentNode(comment))
        return self.dottext[-1]

    def to_data_type(self, data_name: str, type_name: str) -> str:
        return f"type_{type_name}_{data_name}"

    def offset_of(self, local_name: str) -> int:
        stack_size = 4 * len(self.current_function_stack)
        index = 4 * self.current_function_stack.index(local_name)
        return stack_size - index - 4

    def register_instantiation(self, size: Union[int, str]) -> mips.InstructionNode:
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        if isinstance(size, int):
            self.register_instruction(mips.AddiNode("$a0", "$zero", f"{size}"))
        if isinstance(size, str):
            self.register_instruction(mips.MoveNode("$a0", size))
        self.register_instruction(mips.SystemCallNode())


class CilToMipsTranslator(BaseCilToMipsVisitor):
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode) ####
    def visit(self, node: cil.ProgramNode):

        for type_node in node.dottypes:
            self.visit(type_node)
        
        for type_node in node.dottypes: 
            self.register_word(self.to_data_type("name_size", type_node.name), str(len(type_node.name)))
            self.register_asciiz(self.to_data_type("name", type_node.name), f'"{type_node.name}"')
            self.register_empty_data()
        
        self.register_space("buffer_input", 1024)
        self.register_asciiz("debug_log", '"debug_log\\n"')

        for function_node in node.dotcode:
            self.visit(function_node)

        return mips.ProgramNode(self.dotdata, self.dottext)

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        size = 4 * (2 + len(node.attributes) + len(node.methods)) #### +2

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name), f"type_{node.parent}" if node.parent != "null" else "0")
        self.register_word(self.to_data_type("name_address", node.name), f"type_{node.name}_name_size")
        for method, function in node.methods:
            self.register_word(self.to_data_type(method, node.name), function)
        self.register_empty_data()

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        self.current_function = node
        self.register_instruction(mips.LabelNode(node.name))

        param_names = [x.name for x in self.current_function.params]
        local_names = [x.name for x in self.current_function.localvars]
        self.current_function_stack = ["$ra"] + param_names + local_names

        locals_size = 4 * len(self.current_function.localvars)
        stack_size = 4 * len(self.current_function_stack)


        ##
        if node.name != "main":
            self.register_comment("Function parameters")
            self.register_comment(f"  $ra = {stack_size - 4}($sp)")
            for i, param_name in enumerate(param_names, start=2):
                self.register_comment(f"  {param_name} = {stack_size - (4 * i)}($sp)")
            self.register_empty_instruction()

        if self.current_function.localvars:
            self.register_comment("Reserving space for local variables")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{-locals_size}"))
            self.register_empty_instruction()

        for instruction in node.instructions:
            # TODO: Remove the try/except block when the visitor is fixed
            try:
                if isinstance(instruction, (cil.EndOfLineNode, cil.CommentNode)):
                    continue
                self.visit(instruction)
                self.register_empty_instruction()
            except Exception as e:
                print(f"error {e} in {node.name} {type(instruction)}")

        if node.name != "main" and self.current_function.localvars:
            self.register_comment("Freeing space for local variables")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{locals_size}"))
            self.register_empty_instruction()

        if node.name != "main":
            self.register_instruction(mips.JumpRegisterNode("$ra"))
        self.register_empty_instruction()

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        self.register_comment(f"{node.dest} = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode):
        self.register_comment(f"{node.dest} = {node.source} where {node.source} is an integer")
        self.register_instantiation(12)
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"Pointer to {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t0)").set_comment(f"$t2 = value of {node.source}"))
    
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)").set_comment(f"Save type of {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment(f"Save size of {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$t2", "8($v0)").set_comment(f"Save value of {node.dest}"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        if node.arg_index == 0:
            self.register_comment("Passing function arguments")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"-{4 * node.total_args + 4}").set_comment("Reserving space for arguments"))
            self.register_instruction(mips.StoreWordNode("$ra", f"{4 * (node.total_args)}($sp)").set_comment("Storing return address"))
            self.register_empty_instruction()
        self.register_comment(f"Argument {node.name}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.name) +  4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{4 * (node.total_args - node.arg_index - 1)}($sp)").set_comment(f"Storing {node.name}"))

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        self.register_comment(f"Calling function {node.method_addr}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.method_addr) + 4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.JumpAndLinkRegisterNode("$t0"))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)").set_comment(f"{node.dest} = result of {node.method_addr}"))
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}").set_comment("Freeing space for arguments"))
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        self.register_comment(f"Calling function {node.function}")
        self.register_instruction(mips.JumpAndLinkNode(node.function))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)").set_comment(f"{node.dest} = result of {node.function}"))
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}").set_comment("Freeing space for arguments"))

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        self.register_comment(f"Allocating {node.type}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.LoadWordNode("$a0", f"type_{node.type}"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.type}").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of th object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of th object"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object {node.type}"))

    @visitor.when(cil.AllocateIntNode)
    def visit(self, node: cil.AllocateIntNode):
        self.register_comment(f"Allocating Int {node.value}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        #
        self.register_instruction(mips.LoadAddressNode("$t0", "type_Int").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of the object"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)").set_comment("Setting value in the third word of the object"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object Int"))

    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode):
        self.register_comment(f"Allocating Bool {node.value}")

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t0", "type_Bool").set_comment("$t0 = address of the type"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting size in the second word of the object"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)").set_comment("Setting value in the third word of the object"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = address of allocated object Int"))

    @visitor.when(cil.AllocateStringNode)
    def visit(self, node: cil.AllocateStringNode):
        self.register_comment(f"Allocating String")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", f"{9 + node.length}").set_comment("$a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        
        ####
        self.register_instruction(mips.LoadAddressNode("$t0", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t0", f"0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t0", "$zero", f"{9 + node.length}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"4($v0)").set_comment("Setting length of the string in the second word of the object"))
        self.register_empty_instruction()

        for i, c in enumerate(node.string):
            ec = c.replace('\n', '\\n').replace('\t', '\\t').replace('\b', '\\b').replace('\f', '\\f')
            # ec = ec.replace('\t', '\\t')
            # ec = ec.replace('\b', '\\b')
            # ec = ec.replace('\f', '\\f')
            self.register_instruction(mips.AddiNode("$t0", "$zero",  f"{ord(c)}"))
            self.register_instruction(mips.StoreByteNode("$t0", f"{i + 8}($v0)").set_comment(f"{node.dest}[{i}] = '{ec}'"))
            self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"{node.length + 8}($v0)").set_comment(f"Null-terminator at the end of the string"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.value}"))

    @visitor.when(cil.AllocateNullNode)
    def visit(self, node: cil.AllocateNullNode):
        self.register_comment(f"Allocating NUll to {node.dest}")
        self.register_instruction(mips.StoreWordNode("$zero", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = 0"))

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        self.register_comment(f"{node.dest} = length of {node.str_address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "4($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9").set_comment("Subtracting 9 for the type, length, and null-terminator"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t1", "8($t0)"))

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        self.register_comment(f"{node.dest} = {node.str1} + {node.str2}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str1)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.str2)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)").set_comment("$t2 = length of str1"))
        self.register_instruction(mips.LoadWordNode("$t3", "4($t1)").set_comment("$t3 = length of str2"))
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))
        
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3").set_comment("$t4 = length of str1 + str2"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "9").set_comment("Adding the space for the type (4bytes), the length(4bytes) and the null-terminator(1byte)"))
        self.register_empty_instruction()

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.MoveNode("$a0", "$t4"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.AddiNode("$t4", "$t4", "-9").set_comment("Restoring $t4 = length of str1 + str2"))
        self.register_instruction(mips.AddNode("$t5", "$zero", "$v0").set_comment("$t5 = address of the new string object"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "8").set_comment("$t5 = address of the first byte of the new string"))
        self.register_empty_instruction()
        
        self.register_instruction(mips.LoadAddressNode("$t8", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t8", f"0($v0)").set_comment("Setting type in the first word of th object"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length of the string in the second word of the object"))
        self.register_empty_instruction()

        self.register_comment(f"Copying str1 to the new string")
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6").set_comment("$t6 = 0 Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_str1_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t2", "while_copy_str1_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of str1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_str1_start"))
        self.register_instruction(mips.LabelNode("while_copy_str1_end"))
        self.register_empty_instruction()

        self.register_comment(f"Copying str2 to the new string")
        self.register_instruction(mips.LabelNode("while_copy_str2_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t4", "while_copy_str2_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t1)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of str1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_str2_start"))
        self.register_instruction(mips.LabelNode("while_copy_str2_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)").set_comment("Setting the null-terminator"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.str1} + {node.str2}"))

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        self.register_comment(f"{node.dest} = {node.str_address}[{node.start}:{node.start} + {node.length}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)").set_comment("$t0 = address of the string"))
        self.register_instruction(mips.LoadWordNode("$t1", f"4($t0)").set_comment("$t1 = length of the string"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9").set_comment("$t1 = length of the string + 9"))
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.start)}($sp)").set_comment("$t2 = start of the substring"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t2)"))
        self.register_instruction(mips.LoadWordNode("$t3", f"{self.offset_of(node.length)}($sp)").set_comment("$t3 = length of the substring"))
        self.register_instruction(mips.LoadWordNode("$t3", "8($t3)"))
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3").set_comment("$t4 = start of the substring + length of the substring"))

        self.register_empty_instruction()
        self.register_instruction(mips.BgtNode("$t4", "$t1", "substring_out_of_bounds"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$t3", "9"))
        self.register_instantiation("$t3")
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))

        self.register_empty_instruction()
        self.register_instruction(mips.LoadAddressNode("$t5", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t5", f"0($v0)").set_comment("Setting type in the first word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length in the second word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("pointing to the first byte of the string"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t2").set_comment("pointing to the first byte of the substring"))
        self.register_instruction(mips.MoveNode("$t5", "$v0").set_comment("$t5 = address of the new string"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "8").set_comment("pointing to the first byte of the string"))
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6").set_comment("$t6 = 0 Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_substr_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t3", "while_copy_substr_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"0($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("$t0 = $t0 + 1 Incrementing the address of the string"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1").set_comment("$t5 = $t5 + 1 Incrementing the address of the new string"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1").set_comment("$t6 = $t6 + 1 Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_substr_start"))
        self.register_instruction(mips.LabelNode("while_copy_substr_end"))

        self.register_empty_instruction()
        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)").set_comment("Setting the null-terminator"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.str_address}[{node.start}:{node.start} + {node.length}]"))

        self.register_instruction(mips.JumpNode("substring_not_out_of_bounds"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_out_of_bounds"))
        # TODO: Throw an exception
        self.register_instruction(mips.LoadInmediateNode("$v0", "17"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "1"))
        self.register_instruction(mips.SystemCallNode())

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_not_out_of_bounds"))

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        node_id = hash(node)
        self.register_comment(f"Get attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"Get the address of {node.instance}"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"Get the attribute '{node.attr}' from the {node.instance}"))

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_get_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_get_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_get_attribute_{node_id}"))
        self.register_instruction(mips.StoreWordNode("$t1",f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = {node.instance}.{node.attr}"))
        self.register_instruction(mips.LabelNode(f"end_get_attribute_{node_id}"))

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        node_id = hash(node)
        self.register_comment(f"Set attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t0 = {node.instance}"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t1 = {node.source}"))

        self.register_instruction(mips.BeqNode("$t1", "$zero", f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_set_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_set_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_set_attribute_{node_id}"))
        self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)").set_comment(f"{node.instance}.{node.attr} = {node.source}"))
        self.register_instruction(mips.LabelNode(f"end_set_attribute_{node_id}"))

    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode):
        self.register_comment(f"Get method {node.method_name} of {node.type}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "12"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.method_index)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SllNode("$t1", "$t1", "2"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode):
        self.register_comment(f"initialize Array [{node.size}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.size)}($sp)").set_comment(f"$t0 = {node.size}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the size"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        self.register_instantiation("$t0")
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = new Array[{node.size}]"))

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        self.register_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)").set_comment("$t1 = value in the position"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]"))

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        self.register_comment(f"array {node.instance}[4 * {node.index}] = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($t1)"))

    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode):
        self.register_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)").set_comment("$t1 = value in the position"))
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.dest)}($sp)").set_comment(f"{node.dest} = array {node.instance}[4 * {node.index}]"))
        self.register_instruction(mips.StoreWordNode("$t0", "8($t2)"))

    @visitor.when(cil.SetValueInIndexNode)
    def visit(self, node: cil.SetValueInIndexNode):
        self.register_comment(f"array {node.instance}[4 * {node.index}] = {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)").set_comment(f"$t0 = {node.index}"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("$t0 = value of the index"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4").set_comment("$t1 = 4"))
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t0 = $t0 * 4"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)").set_comment(f"$t1 = {node.instance}"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0").set_comment("Move the pointer to the index"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", "0($t1)"))

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        self.register_comment(f"{node.dest} = typeof {node.obj} that is the first word of the object")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.obj)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ParentNode)
    def visit(self, node: cil.ParentNode):
        self.register_comment(f"{node.dest} = ancestor of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "4($t0)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode):
        self.register_comment(f"{node.dest} = direction of {node.name}")
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.name}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        self.register_comment(f"{node.dest} = name of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t1)").set_comment(f"$t2 = direction of the type name"))
        self.register_instruction(mips.LoadAddressNode("$t3", "4($t2)").set_comment(f"$t3 = address of the name"))
        self.register_instruction(mips.LoadWordNode("$t2", "0($t2)").set_comment(f"$t2 = length of the name"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t2", "$t2", "9").set_comment(f"Setting space for the type, the size and the null byte"))
        self.register_instantiation("$t2")
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9").set_comment(f"Restoring space for the type, the size and the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.LoadAddressNode("$t4", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t4", f"0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()

        self.register_instruction(mips.AddiNode("$t4", "$v0", 0).set_comment("$t4 = direction of the new string"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.XorNode("$t5", "$t5", "$t5").set_comment("Initializing counter"))
        self.register_instruction(mips.LabelNode("while_copy_name_start"))
        self.register_instruction(mips.BeqNode("$t5", "$t2", "while_copy_name_end"))
        self.register_instruction(mips.LoadByteNode("$t6", "0($t3)").set_comment("Loading the character"))
        self.register_instruction(mips.StoreByteNode("$t6", "0($t4)"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing the pointer to the new string"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment(f"Incrementing the pointer to the string in {node.source}"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_name_start"))
        self.register_instruction(mips.LabelNode("while_copy_name_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", "0($t4)").set_comment("Setting the null byte"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new string in {node.dest}"))

    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        self.register_comment(f"{node.dest} = copy of {node.source}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)").set_comment(f"$t0 = {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)").set_comment(f"$t1 = type of {node.source}"))
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)").set_comment(f"$t2 = length of {node.source} in bytes"))
        self.register_empty_instruction()

        self.register_comment("Allocating space for the new object")
        self.register_instantiation("$t2")
        self.register_instruction(mips.MoveNode("$t3", "$v0").set_comment("$t3 = direction of the new object"))
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)").set_comment("Setting type in the first word of the object"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting length in the second word of the object"))
        self.register_empty_instruction()

        self.register_comment("Initializing the variable of the loop")
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("Pointer to the first character of the object"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "8").set_comment("Pointer to the first character of the object"))
        self.register_instruction(mips.AddiNode("$t2", "$2", "-8").set_comment("Decrementing in 8 the length of the object"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4").set_comment("Initializing counter"))
        self.register_empty_instruction()

        self.register_comment("Loop copying the object")
        self.register_instruction(mips.LabelNode("while_copy_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t2", "while_copy_end"))
        self.register_instruction(mips.LoadByteNode("$t5", "0($t0)").set_comment("Loading the byte"))
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)").set_comment("Storing the byte"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("Incrementing the pointer to the object"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment("Incrementing the pointer to the new object"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_start"))
        self.register_instruction(mips.LabelNode("while_copy_end"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new object in {node.dest}"))

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_addr)}($sp)").set_comment(f"$t0 = {node.str_addr}"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8").set_comment("Pointer to the first character of the string"))
        self.register_empty_instruction()

        self.register_comment(f"Printing the String {node.str_addr}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        self.register_comment(f"Printing the Int {node.int_source}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        self.register_instruction(mips.LoadWordNode("$a0", f"{self.offset_of(node.int_source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$a0", "8($a0)"))
        self.register_instruction(mips.SystemCallNode())
    
    @visitor.when(cil.PrintTypeNameNode)
    def visit(self, node: cil.PrintTypeNameNode):
        self.register_comment("Printing the type name")
        self.register_empty_instruction()
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.address)}($sp)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "12"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "4"))
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "8"))
        self.register_instruction(mips.LoadAddressNode("$a0", "buffer_input"))
        self.register_instruction(mips.LoadInmediateNode("$a1", "1024"))
        self.register_instruction(mips.SystemCallNode())


        self.register_empty_instruction()
        self.register_instruction(mips.XorNode("$t0", "$t0", "$t0").set_comment("Initializing counter"))
        self.register_instruction(mips.LabelNode("while_read_start"))
        self.register_instruction(mips.LoadByteNode("$t1", "buffer_input($t0)").set_comment("Loading the byte"))
        
        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.MoveNode("$a0", "$t1"))
        # self.register_instruction(mips.SystemCallNode())

        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.LoadInmediateNode("$a0", "0"))
        # self.register_instruction(mips.SystemCallNode())
        
        self.register_instruction(mips.AddiNode("$t2", "$zero", "10"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t2", "$zero", "13"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_read_start"))
        self.register_instruction(mips.LabelNode("while_read_end"))

        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.MoveNode("$a0", "$t0"))
        # self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "9").set_comment("Adding space for the type, the size and the null byte"))
        self.register_instantiation("$t0")
        self.register_instruction(mips.AddiNode("$t0", "$t0", "-9").set_comment("Adding space for the type, the size and the null byte"))
        self.register_instruction(mips.LoadAddressNode("$t2", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t2", "0($v0)").set_comment("Setting type in the first word of the object"))        
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)").set_comment("Setting length in the second word of the object"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$v0", "8").set_comment("Pointer to the first character of the string"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4").set_comment("Initializing counter"))
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t0", "while_copy_from_buffer_end"))
        self.register_instruction(mips.LoadByteNode("$t5", "buffer_input($t4)").set_comment("Loading the byte"))
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)").set_comment("Storing the byte"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1").set_comment("Imcremeenting pointer"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1").set_comment("Incrementing counter"))
        self.register_instruction(mips.JumpNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_end"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreByteNode("$zero", "0($t3)").set_comment("Storing the null byte"))
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"Storing the new object in {node.dest}"))

    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "5"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$v0", "8($t0)"))

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        self.register_instruction(mips.LabelNode(node.label))
    
    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        self.register_comment(f"Jumping to {node.addr}")
        self.register_instruction(mips.JumpNode(node.addr))
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        self.register_comment(f"If {node.condition} then goto {node.address}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.condition)}($sp)").set_comment("Loading the address of the condition"))
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)").set_comment("Loading the value of the condition"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "1").set_comment("Setting the value to 1 for comparison"))
        self.register_instruction(mips.BeqNode("$t0", "$t1", node.address))

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        self.register_comment("Addition operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.AddNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 + $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        self.register_comment("Subtraction operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SubNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 - $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        self.register_comment("Multiplication operation")        
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.MultNode("$t0", "$t1").set_comment("$t2 = $t0 * $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t2"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        self.register_comment("Division operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.DivNode("$t0", "$t1").set_comment("$t2 = $t0 / $t1"))
        self.register_instruction(mips.MoveFromLowNode("$t2"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        self.register_comment("Xor operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.XorNode("$t2", "$t0", "$t1").set_comment("$t0 = $t0 ^ $t1"))
        self.postprocess_binary_int_operation(node, "Int")

    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SltNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 < $t1"))
        self.postprocess_binary_int_operation(node, "Bool")
    
    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        self.register_comment("Less than operation")
        self.preprocess_binary_operation(node)
        self.register_instruction(mips.SleNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 <= $t1"))
        self.postprocess_binary_int_operation(node, "Bool")

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        self.register_comment("Equal operation")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand address"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand address"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1").set_comment("$t2 = $t0 == $t1"))
        self.postprocess_binary_int_operation(node, "Bool")

    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.EqualAddressNode):
        self.register_comment(f"{node.dest} = EqualAddress({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))
    
    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode):
        self.register_comment(f"{node.dest} = EqualInt({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))

    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode):
        self.register_comment(f"{node.dest} = EqualStr({node.left}, {node.right})")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "8"))

        self.register_empty_instruction()
        self.register_comment(f"By default we assume the strings are equals")
        self.register_instruction(mips.AddiNode("$t4", "$zero", "1"))
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t4", f"8($t5)"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_compare_strings_start"))
        self.register_instruction(mips.LoadByteNode("$t2", "0($t0)"))
        self.register_instruction(mips.LoadByteNode("$t3", "0($t1)"))

        self.register_instruction(mips.BeqNode("$t2", "$t3", "while_compare_strings_update"))
        
        self.register_empty_instruction()
        self.register_comment(f"The strings are no equals")
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$zero", f"8($t5)"))
        self.register_instruction(mips.JumpNode("while_compare_strings_end"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_compare_strings_update"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "1"))
        self.register_instruction(mips.BeqNode("$t2", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.BeqNode("$t3", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.JumpNode("while_compare_strings_start"))
        self.register_instruction(mips.LabelNode("while_compare_strings_end"))

    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        self.register_comment("Exit program")
        self.register_instruction(mips.LoadInmediateNode("$v0", "10"))
        self.register_instruction(mips.SystemCallNode())

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        if node.value.isdigit():
            self.register_comment("Loading return value in $v1")
            self.register_instruction(mips.AddiNode("$v1", "$zero", f"{node.value}"))
            return
        offset = self.offset_of(node.value)
        self.register_comment("Loading return value in $v1")
        self.register_instruction(mips.LoadWordNode("$v1", f"{offset}($sp)"))

    
    def preprocess_binary_operation(self, node: cil.ArithmeticNode):
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)").set_comment("Save in $t0 the left operand address"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)").set_comment("Save in $t0 the left operand value"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)").set_comment("Save in $t1 the right operand address"))
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)").set_comment("Save in $t1 the rigth operand value"))

    def postprocess_binary_int_operation(self, node: cil.ArithmeticNode, t: str):
        # self.register_instantiation(12)
        self.register_empty_instruction()
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)").set_comment(f"$t0 = {node.dest}"))
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)").set_comment(f"Setting value in the third word of the {t} object"))



class MipsFormatter1:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        def is_function_label(node: mips.InstructionNode):
            return isinstance(node, mips.LabelNode) and (
                node.name.startswith("function_") or node.name == "main"
            )

        dotdata = "\n\t".join([self.visit(data) for data in node.dotdata])

        instructions = [
            (
                f"{self.visit(inst)}"
                if is_function_label(inst)
                else f"\t{self.visit(inst)}"
            )
            for inst in node.dottext
        ]

        dottext = "\n\t".join(instructions)

        return f".data\n\t{dotdata}\n\n.text\n\t{dottext}"

    @visitor.when(mips.DataNode)
    def visit(self, node: mips.DataNode):
        return (
            f"{node.name}: {node.data_type} {node.value}"
            if node.comment == ""
            else f"{node.name}: {node.data_type} {node.value} # {node.comment}"
        )

    @visitor.when(mips.OneAddressNode)
    def visit(self, node: mips.OneAddressNode):
        return (
            f"{node.code} {node.dest}"
            if node.comment == ""
            else f"{node.code} {node.dest} # {node.comment}"
        )

    @visitor.when(mips.TwoAddressNode)
    def visit(self, node: mips.TwoAddressNode):
        return (
            f"{node.code} {node.dest}, {node.source}"
            if node.comment == ""
            else f"{node.code} {node.dest}, {node.source} # {node.comment}"
        )

    @visitor.when(mips.ThreeAddressNode)
    def visit(self, node: mips.ThreeAddressNode):
        return (
            f"{node.code} {node.dest}, {node.source1}, {node.source2}"
            if node.comment == ""
            else f"{node.code} {node.dest}, {node.source1}, {node.source2} # {node.comment}"
        )

    @visitor.when(mips.SystemCallNode)
    def visit(self, node: mips.SystemCallNode):
        return node.code
    
    @visitor.when(mips.LabelNode)
    def visit(self, node: mips.LabelNode):
        return (
            f"{node.name}:" if node.comment == "" else f"{node.name}: # {node.comment}"
        )

    @visitor.when(mips.CommentNode)
    def visit(self, node: mips.CommentNode):
        return f"# {node.comment}"

    @visitor.when(mips.EmptyInstructionNode)
    def visit(self, node: mips.EmptyInstructionNode):
        return ""

    @visitor.when(mips.EmptyDataNode)
    def visit(self, node: mips.EmptyDataNode):
        return ""
