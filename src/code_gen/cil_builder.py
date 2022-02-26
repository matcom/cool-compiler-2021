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
    RuntimeErrorNode,
    CopyNode,
    TypeNameNode,
    SetAttribNode,
    GetAttribNode,
    DefaultValueNode,
    IsVoidNode,
)
from cool_visitor import FormatVisitor

from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType, IntType
from cmp.semantic import Context, VariableInfo

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
        self.internal_count = 0
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

    def to_data_name(self, type_name, value):
        return f"{type_name}_{value}"

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_instruction(self, instruction):
        self.current_function.instructions.append(instruction)

    def register_type(self, name):
        type_node = TypeNode(name)
        self.types.append(type_node)
        return type_node

    def register_function(self, function_name):
        function_node = FunctionNode(function_name, [], [], [])
        self.code.append(function_node)
        return function_node

    def register_local(self, vinfo):
        vinfo.name = f"local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.current_function.localvars)}"
        local_node = LocalNode(vinfo.name)
        self.current_function.localvars.append(local_node)
        return vinfo.name

    def register_param(self, vinfo):
        vinfo.name = self.build_internal_vname(vinfo.name)
        arg_node = ParamNode(vinfo.name)
        self.params.append(arg_node)
        return vinfo

    def build_internal_vname(self, vname):
        vname = f"{self.internal_count}_{self.current_function.name[9:]}_{vname}"
        self.internal_count += 1
        return vname

    def define_internal_local(self):
        vinfo = VariableInfo("internal", None)
        return self.register_local(vinfo)

    def register_data(self, name, value):
        data_node = DataNode(name, value)
        self.data.append(data_node)
        return data_node

    def is_attribute(self, vname):
        return vname not in [var.name for var in self.current_function.localvars]

    def build_constructor(self, node):
        attributeNodes = [
            feat for feat in node.features if isinstance(feat, cool.AttrDeclarationNode)
        ]

        expr_list = []
        for attr in attributeNodes:  # Assign default value first
            assign = cool.AssignNode(attr.id, cool.DefaultValueNode(attr.type))
            expr_list.append(assign)

        for attr in attributeNodes:  # Assign init_expr if not None
            if attr.init_exp:
                assign = cool.AssignNode(attr.id, attr.init_exp)
                expr_list.append(assign)

        body = cool.BlockNode(expr_list)
        self.current_type.define_method("constructor", [], [], "Object")
        return cool.FuncDeclarationNode("constructor", [], "Object", body)

    def add_builtin_functions(self):
        # Object
        obj_functions = [
            self.cil_predef_method("abort", "Object", self.object_abort),
            self.cil_predef_method("copy", "Object", self.object_copy),
            self.cil_predef_method("type_name", "Object", self.object_type_name),
        ]
        object_type = TypeNode("Object")
        object_type.attributes = []
        object_type.methods = obj_functions

        # "IO"
        functions = [
            self.cil_predef_method("out_string", "IO", self.io_outstring),
            self.cil_predef_method("out_int", "IO", self.io_outint),
            self.cil_predef_method("in_string", "IO", self.io_instring),
            self.cil_predef_method("in_int", "IO", self.io_inint),
        ]
        io_type = TypeNode("IO")
        io_type.attributes = []
        io_type.methods = obj_functions + functions

        # String
        functions = [
            self.cil_predef_method("length", "String", self.string_length),
            self.cil_predef_method("concat", "String", self.string_concat),
            self.cil_predef_method("substr", "String", self.string_substr),
        ]
        string_type = TypeNode("String")
        string_type.attributes = [
            VariableInfo("length").name,
            VariableInfo("str_ref").name,
        ]
        string_type.methods = obj_functions + functions

        # Int
        int_type = TypeNode("Int")
        int_type.attributes = [VariableInfo("value", is_attr=True).name]
        int_type.methods = obj_functions

        # Bool
        bool_type = TypeNode("Bool")
        bool_type.attributes = [VariableInfo("value", is_attr=True).name]
        bool_type.methods = obj_functions

        for typex in [object_type, io_type, string_type, int_type, bool_type]:
            self.types.append(typex)

    # predefined functions cil
    def cil_predef_method(self, mname, cname, specif_code):
        self.current_type = self.context.get_type(cname)
        self.current_method = self.current_type.get_method(mname)
        self.current_function = FunctionNode(
            self.to_function_name(mname, cname), [], [], []
        )

        specif_code()

        self.code.append(self.current_function)
        self.current_function = None
        self.current_type = None

        return (mname, self.to_function_name(mname, cname))

    def string_length(self):
        self.params.append(ParamNode("self"))

        result = self.define_internal_local()

        self.register_instruction(LengthNode(result, "self"))
        self.register_instruction(ReturnNode(result))

    def string_concat(self):
        self.params.append(ParamNode("self"))
        other_arg = VariableInfo("other_arg")
        self.register_param(other_arg)

        ret_vinfo = self.define_internal_local()

        self.register_instruction(ConcatNode(ret_vinfo, "self", other_arg.name))
        self.register_instruction(ReturnNode(ret_vinfo))

    def string_substr(self):
        self.params.append(ParamNode("self"))
        idx_arg = VariableInfo("idx_arg")
        self.register_param(idx_arg)
        length_arg = VariableInfo("length_arg")
        self.register_param(length_arg)

        ret_vinfo = self.define_internal_local()

        self.register_instruction(
            SubstringNode(ret_vinfo, "self", idx_arg.name, length_arg.name)
        )
        self.register_instruction(ReturnNode(ret_vinfo))

    def object_abort(self):
        self.register_instruction(RuntimeErrorNode("ABORT_SIGNAL"))

    def object_copy(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(CopyNode(ret_vinfo, "self"))
        self.register_instruction(ReturnNode(ret_vinfo))

    def object_type_name(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(TypeNameNode(ret_vinfo, "self"))
        self.register_instruction(ReturnNode(ret_vinfo))

    def io_outstring(self):
        self.params.append(ParamNode("self"))
        str_arg = VariableInfo("str")
        self.register_param(str_arg)
        self.register_instruction(PrintNode(str_arg.name))
        self.register_instruction(ReturnNode("self"))

    def io_outint(self):
        self.params.append(ParamNode("self"))
        int_arg = VariableInfo("int")
        self.register_param(int_arg)
        result = self.define_internal_local()
        self.register_instruction(ToStrNode(result, int_arg.name))
        self.register_instruction(ReturnNode(VariableInfo(result).name))

    def io_instring(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(ReadNode(ret_vinfo))
        self.register_instruction(ReturnNode(ret_vinfo))

    def io_inint(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(ReadNode(ret_vinfo))  # TODO: ReadInt?
        self.register_instruction(ReturnNode(ret_vinfo))

    @visitor.on("node")
    def visit(self, node=None):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node):
        self.context = node.context

        self.add_builtin_functions()

        # Add entry function and call Main.main()
        self.current_function = FunctionNode("entry", [], [], [])
        self.code.append(self.current_function)

        instance = "l_instance"
        self.register_instruction(LocalNode(instance))

        result = "l_result"
        self.register_instruction(LocalNode(result))

        main_method_name = self.to_function_name("Main", "main")
        self.register_instruction(AllocateNode("Main", instance))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(main_method_name, result))
        self.register_instruction(ReturnNode(0))

        self.current_function = None

        for declaration in node.declarations:
            self.visit(declaration)

        program_node = ProgramNode(self.types, self.data, self.code)

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

        return program_node

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(self.current_type.name)

        constructor = self.build_constructor(node)

        visited_func = []
        current_type = self.current_type
        while current_type is not None:
            attributes = [
                (node.id + "_" + attr.name) for attr in current_type.attributes
            ]
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

        self.visit(constructor)
        for feature in node.features:
            self.visit(feature)

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node):
        self.current_method = self.current_type.get_method(node.id)

        # Add function to .CODE
        self.current_function = self.register_function(
            self.to_function_name(node.id, self.current_type.name)
        )

        # Add params
        self.current_function.params.append(ParamNode("self"))
        for pname, _ in node.params:
            self.current_function.params.append(ParamNode(pname))

        # Body
        value = self.visit(node.body)

        # Return
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

        if self.is_attribute(node.id):
            self.register_instruction(SetAttribNode("self", node.id, expr))
        else:
            self.register_instruction(AssignNode(node.id, expr))

    @visitor.when(cool.CallNode)
    def visit(self, node):
        # TODO: Pending <expr>.id(<expr>,...,<expr>)
        # TODO: Pending <expr>@<type>.id(<expr>,...,<expr>)

        for arg in node.args:
            temp = self.define_internal_local()
            value = self.visit(arg)
            self.register_instruction(AssignNode(temp, value))
            self.register_instruction(ArgNode(temp))

        method_name = self.to_function_name(node.id, self.current_type.name)
        result = self.define_internal_local()
        self.register_instruction(StaticCallNode(method_name, result))

        return result

    @visitor.when(cool.IfNode)
    def visit(self, node):
        # IF condition GOTO label
        condition_value = self.visit(node.if_expr)
        then_label = "THEN_" + self.next_id()
        self.register_instruction(GotoIfNode(condition_value, LabelNode(then_label)))

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

        solve = self.define_internal_local()
        self.register_instruction(DefaultValueNode(solve, "Void"))

        return solve

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

        return self.visit(node.body)

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

        solve = self.define_internal_local()
        self.register_instruction(PlusNode(solve, left, right))

        return solve

    @visitor.when(cool.MinusNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(MinusNode(solve, left, right))

        return solve

    @visitor.when(cool.StarNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(StarNode(solve, left, right))

        return solve

    @visitor.when(cool.DivNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(DivNode(solve, left, right))

        return solve

    @visitor.when(cool.LessEqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(LessEqualNode(solve, left, right))

        return solve

    @visitor.when(cool.LessNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(LessNode(solve, left, right))

        return solve

    @visitor.when(cool.EqualNode)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        solve = self.define_internal_local()
        self.register_instruction(EqualNode(solve, left, right))

        return solve

    # Unary operators
    @visitor.when(cool.InstantiateNode)  # NewNode
    def visit(self, node):
        new_local = self.define_internal_local()
        self.register_instruction(AllocateNode(node.lex, new_local))

        return new_local

    @visitor.when(cool.IsvoidNode)
    def visit(self, node):
        value = self.visit(node.expr)
        solve = self.define_internal_local()
        self.register_instruction(IsVoidNode(solve, value))
        return solve

    @visitor.when(cool.NotNode)
    def visit(self, node):
        value = self.visit(node.expr)
        solve = self.define_internal_local()
        self.register_instruction(NotNode(solve, value))
        return solve

    @visitor.when(cool.NegNode)
    def visit(self, node):
        value = self.visit(node.expr)
        solve = self.define_internal_local()
        self.register_instruction(IntComplementNode(solve, value))
        return solve

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
        1 if node.lex == "true" else 0

    @visitor.when(cool.DefaultValueNode)
    def visit(self, node):
        solve = self.define_internal_local()
        self.register_instruction(DefaultValueNode(solve, node.type))
        return solve
