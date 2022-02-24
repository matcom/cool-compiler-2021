import cmp.nbpackage
import cmp.visitor as visitor

import ast_nodes as cool

from cmp.cil import (
    ProgramNode,
    TypeNode,
    DataNode,
    FunctionNode,
    ParamNode,
    LocalNode,
    AssignNode,
    ArithmeticNode,
    AllocateNode,
    TypeOfNode,
    LabelNode,
    GotoIfNode,
    GotoNode,
    StaticCallNode,
    DynamicCallNode,
    ArgNode,
    ReturnNode,
    LoadNode,
    LengthNode,
    ConcatNode,
    PrefixNode,
    SubstringNode,
    ToStrNode,
    ReadNode,
    PrintNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    NotNode,
    IntComplementNode,
    LessNode,
    LessEqualNode,
    EqualNode,
)
from cool_visitor import FormatVisitor

from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType, IntType
from cmp.semantic import Context

from cmp.semantic import Scope


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

    def to_function_name(self, method_name, type_name):
        return f"function_{method_name}_at_{type_name}"

    def register_instruction(self, instruction):
        self.current_function.instructions.append(instruction)

    def register_type(self, name):
        type_node = TypeNode(name)
        self.types.append(type_node)
        return type_node

    @visitor.on("node")
    def visit(self, node=None):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node):
        self.context = node.context

        # Add entry function and call Main.main()
        self.current_function = FunctionNode("entry", [], [], [])
        self.code.append(self.current_function)

        instance = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(instance))

        result = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(result))

        main_method_name = self.to_function_name("Main", "main")
        self.register_instruction(AllocateNode("Main", instance))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(main_method_name, result))
        self.register_instruction(ReturnNode(0))

        self.current_function = None

        for declaration in node.declarations:
            self.visit(declaration)

        # Reset state
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.errors = []
        self.method_count = 0
        self.string_count = 0
        self.temp_vars_count = 0
        self._count = 0
        self.context = None

        return ProgramNode(self.types, self.data, self.code)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        self.types.append(self.current_type)

        type_node = self.register_type(self.current_type.name)

        visited_func = []
        current_type = self.current_type
        while current_type is not None:
            attributes = [attr.name for attr in current_type.attributes]
            methods = [
                func.name
                for func in current_type.methods
                if func.name not in visited_func
            ]
            visited_func.extend(methods)
            type_node.attributes.extend(attributes[::-1])
            type_node.methods.extend(
                [
                    (item, self.to_function_name(item, current_type.name))
                    for item in methods[::-1]
                ]
            )
            current_type = current_type.parent

        type_node.attributes.reverse()
        type_node.methods.reverse()

        for feature in node.features:
            self.visit(feature)

        self.current_type = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node):
        self.current_method = self.current_type.get_method(node.id)

        # Generate ref
        ref = self.generate_next_method_id()
        self.current_type.methods.append((node.id, ref))

        # Add params
        function = FunctionNode(ref, [], [], [])
        for pname, _ in node.params:
            function.params.append(ParamNode(pname))

        # Add function to .CODE
        self.current_function = function
        self.code.append(function)

        # Body
        value = self.visit(node.body)

        # Handle return
        if isinstance(self.current_method.return_type, VoidType):
            value = None

        self.register_instruction(ReturnNode(value))
        self.current_method = None
        self.current_function = None

    @visitor.when(cool.VarDeclarationNode)
    def visit(self, node):
        # Add LOCAL variable
        local = LocalNode(node.id)
        self.current_function.localvars.append(local)

        # Add Assignment Node
        if node.expr:
            expr = self.visit(node.expr)
            self.register_instruction(AssignNode(local.id, expr))

    @visitor.when(cool.AssignNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        self.register_instruction(AssignNode(node.id, expr))

    @visitor.when(cool.CallNode)
    def visit(self, node):
        pass

    @visitor.when(cool.IfNode)
    def visit(self, node):
        # IF condition GOTO label
        condition_value = self.visit(node.if_expr)
        then_label = "THEN_" + self.next_id()
        self.register_instruction(GotoIfNode(condition_value, then_label))

        # Else
        self.visit(node.else_expr)

        # GOTO end_label
        end_label = "END_IF_" + self.next_id()  # Example: END_IF_120
        self.register_instruction(GotoNode(end_label))

        # Then label
        self.register_instruction(LabelNode(then_label))
        self.visit(node.then_expr)

        # end_label
        self.register_instruction(LabelNode(end_label))

        # TODO: return something?

    @visitor.when(cool.WhileNode)
    def visit(self, node):
        # While label
        while_label = "WHILE_" + self.next_id()
        self.register_instruction(LabelNode(while_label))

        # Condition
        c = self.visit(node.condition)  # TODO: pop from stack

        # If condition GOTO body_label
        body_label = "BODY_" + self.next_id()
        self.register_instruction(GotoIfNode(c, body_label))

        # GOTO end_while label
        end_while_label = "END_WHILE_" + self.next_id()
        self.register_instruction(GotoNode(end_while_label))

        # Body
        self.register_instruction(LabelNode(body_label))
        self.visit(node.body)

        # GOTO while label
        self.register_instruction(GotoNode(while_label))

        # End while label
        self.register_instruction(LabelNode(end_while_label))

    @visitor.when(cool.BlockNode)
    def visit(self, node):
        value = None
        for expr in node.expression_list:
            value = self.visit(expr)

        return value

    @visitor.when(cool.LetNode)
    def visit(self, node):
        for var_dec in node.identifiers:
            self.visit(var_dec.expr)
            self.current_function.localvars.append(LocalNode(var_dec.id))

        self.visit(node.body)

    @visitor.when(cool.CaseNode)
    def visit(self, node):
        pass  # TODO: Pending!!!

    @visitor.when(cool.CaseItemNode)
    def visit(self, node):
        pass  # TODO: Pending!!!

    # Arithmetic and comparison operators
    @visitor.when(cool.PlusNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(PlusNode(local, left, right))

    @visitor.when(cool.MinusNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(MinusNode(local, left, right))

    @visitor.when(cool.StarNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(StarNode(local, left, right))

    @visitor.when(cool.DivNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(DivNode(local, left, right))

    @visitor.when(cool.LessEqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(LessEqualNode(local, left, right))

    @visitor.when(cool.LessNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(LessNode(local, left, right))

    @visitor.when(cool.EqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(EqualNode(local, left, right))

    # Unary operators
    @visitor.when(cool.InstantiateNode)  # NewNode
    def visit(self, node):
        new_local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(new_local))
        self.register_instruction(AllocateNode(node.lex, new_local))

    @visitor.when(cool.IsvoidNode)
    def visit(self, node):
        value = self.visit(node.expr)
        return value

    @visitor.when(cool.NotNode)
    def visit(self, node):
        value = self.visit(node.expr)
        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(NotNode(local, value))

    @visitor.when(cool.NegNode)
    def visit(self, node):
        value = self.visit(node.expr)
        local = self.generate_next_tvar_id()
        self.register_instruction(LocalNode(local))
        self.register_instruction(IntComplementNode(local, value))

    @visitor.when(cool.ConstantNumNode)
    def visit(self, node):
        return node.lex

    @visitor.when(cool.VariableNode)
    def visit(self, node):
        return node.lex

    @visitor.when(cool.StringNode)
    def visit(self, node):
        idx = self.generate_next_string_id()
        self.data.append(DataNode(idx, node.lex))
        return idx

    @visitor.when(cool.BooleanNode)
    def visit(self, node):
        if node.lex == "true":
            return 1
        else:
            return 0
