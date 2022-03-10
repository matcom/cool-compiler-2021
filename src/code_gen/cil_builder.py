
import cmp.nbpackage
import cmp.visitor as visitor

import ast_typed_nodes as cool

from cmp.cil import (
    ProgramNode,
    TypeNode,
    DataNode,
    FunctionNode,
    ParamNode,
    LocalNode,
    AssignNode,
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
    SubstringNode,
    ReadStringNode,
    ReadIntNode,
    PrintStrNode,
    PrintIntNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    NotNode,
    IntComplementNode,
    LessNode,
    LessEqualNode,
    EqualNode,
    StrEqualNode,
    RuntimeErrorNode,
    CopyNode,
    TypeNameNode,
    SetAttribNode,
    GetAttribNode,
    DefaultValueNode,
    IsVoidNode,
    ExitNode,
    CompareTypes
)
from cool_visitor import FormatVisitor

from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType, IntType
from cmp.semantic import Context, VariableInfo

from cmp.semantic import Scope


class CILBuilder:
    def __init__(self):
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.string_count = 0
        self._count = 0
        self.internal_count = 0
        self.context = None
        self.self_var = None
        self.methods = {}
        self.attrs = {}

    def generate_next_string_id(self):
        self.string_count += 1
        return "string_" + str(self.string_count)

    def next_id(self):
        self._count += 1
        return str(self._count)

    def to_function_name(self, method_name, type_name):
        return f"{type_name}_{method_name}"

    def to_data_name(self, type_name, value):
        return f"{type_name}_{value}"

    def to_attr_name(self, type_name, attr_name):
        return f"{type_name}_{attr_name}"

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def get_method_id(self, typex, name):
        method_id, _ = self.methods[typex][name]
        return method_id

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

    def get_local(self, name):
        return f"local_{name}"

    def register_local(self, name=None):
        local_name = (
            f"local_{name}" if name else f"local_{len(self.current_function.localvars)}"
        )
        local_node = LocalNode(local_name)
        self.current_function.localvars.append(local_node)
        return local_name

    def register_param(self, vinfo):
        vinfo.name = self.build_internal_vname(vinfo.name)
        arg_node = ParamNode(vinfo.name)
        self.params.append(arg_node)
        return vinfo

    def get_param(self, name):
        return f"param_{name}"

    def build_internal_vname(self, vname):
        vname = f"param_{vname}"
        self.internal_count += 1
        return vname

    def define_internal_local(self):
        return self.register_local()

    def is_attribute(self, vname):
        return vname not in [var.name for var in self.current_function.localvars] and (
            vname not in [param.name for param in self.current_function.params]
        )

    def add_builtin_constructors(self):
        builtin_types = ["Object", "IO", "Int", "Bool", "String"]
        for typex in builtin_types:
            self.current_function = FunctionNode(
                self.to_function_name("constructor", typex), [], [], []
            )
            instance = self.define_internal_local()
            self.register_instruction(AllocateNode(typex, instance))
            self.register_instruction(ReturnNode(instance))
            self.code.append(self.current_function)

        self.current_function = None

    def build_constructor(self, node):
        self.current_function = self.register_function(
            self.to_function_name("constructor", node.id)
        )
        self.current_type.define_method("constructor", [], [], "Object")

        self_var = self.define_internal_local()
        self.self_var = self_var

        self.register_instruction(AllocateNode(node.id, self_var))

        attributeNodes = [
            feat for feat in node.features if isinstance(feat, cool.AttrDeclarationNode)
        ]

        for attr in attributeNodes:  # Assign default value first
            default_var = self.define_internal_local()
            self.register_instruction(DefaultValueNode(default_var, attr.type))
            self.register_instruction(
                SetAttribNode(
                    self_var,
                    self.to_attr_name(self.current_type.name, attr.id),
                    default_var,
                    node.id,
                )
            )

        for attr in attributeNodes:  # Assign init_expr if not None
            if attr.init_exp:
                init_expr_value = self.define_internal_local()
                self.visit(attr.init_exp, init_expr_value)
                self.register_instruction(
                    SetAttribNode(
                        self_var,
                        self.to_attr_name(self.current_type.name, attr.id),
                        init_expr_value,
                        node.id,
                    )
                )

        self.register_instruction(ReturnNode(self_var))

    def add_builtin_functions(self):
        # Object
        obj_functions = [self.cil_predef_method("abort", "Object", self.object_abort)]
        object_type = TypeNode("Object")
        object_type.attributes = []
        object_type.methods = obj_functions.copy()
        object_type.methods.append(
            self.cil_predef_method("copy", "Object", self.object_copy)
        )
        object_type.methods.append(
            self.cil_predef_method("type_name", "Object", self.object_type_name)
        )

        # "IO"
        functions = [
            self.cil_predef_method("copy", "IO", self.object_copy),
            self.cil_predef_method("type_name", "IO", self.object_type_name),
            self.cil_predef_method("out_string", "IO", self.io_outstring),
            self.cil_predef_method("out_int", "IO", self.io_outint),
            self.cil_predef_method("in_string", "IO", self.io_instring),
            self.cil_predef_method("in_int", "IO", self.io_inint),
        ]
        io_type = TypeNode("IO")
        io_type.attributes = []
        io_type.methods = obj_functions + functions

        # String
        self.attrs["String"] = {"length": (0, "Int"), "str_ref": (1, "String")}
        functions = [
            self.cil_predef_method("copy", "String", self.object_copy),
            self.cil_predef_method("type_name", "String", self.object_type_name),
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
        # self.attrs["Int"] = {"value": (0, "Int")}
        int_type = TypeNode("Int")
        int_type.attributes = [VariableInfo("value").name]
        int_type.methods = obj_functions + [
            self.cil_predef_method("copy", "Int", self.object_copy),
            self.cil_predef_method("type_name", "Int", self.object_type_name),
        ]

        # Bool
        # self.attrs["Bool"] = {"value": (0, "Int")}
        bool_type = TypeNode("Bool")
        bool_type.attributes = [VariableInfo("value").name]
        bool_type.methods = obj_functions + [
            self.cil_predef_method("copy", "Bool", self.object_copy),
            self.cil_predef_method("type_name", "Bool", self.object_type_name),
        ]

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

    def register_copy(self):
        self.current_function = FunctionNode(
            self.to_function_name("copy", self.current_type.name), [], [], []
        )
        self.object_copy()
        self.code.append(self.current_function)
        self.current_function = None

    def register_type_name(self):
        self.current_function = FunctionNode(
            self.to_function_name("type_name", self.current_type.name), [], [], []
        )
        self.object_type_name()
        self.code.append(self.current_function)
        self.current_function = None

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
        copy_local = self.define_internal_local()
        self.register_instruction(AllocateNode(self.current_type.name, copy_local))

        for attr in self.attrs[self.current_type.name].keys():
            attr_copy_local = self.define_internal_local()
            attr_name = (
                self.to_attr_name(self.current_type.name, attr)
                if self.current_type.name not in ["Int", "String", "Bool"]
                else attr
            )
            self.register_instruction(
                GetAttribNode(
                    attr_copy_local,
                    "self",
                    attr_name,
                    self.current_type.name,
                )
            )
            self.register_instruction(
                SetAttribNode(
                    copy_local,
                    attr_name,
                    attr_copy_local,
                    self.current_type.name,
                )
            )

        self.register_instruction(ReturnNode(copy_local))

    def object_type_name(self):
        self.params.append(ParamNode("self"))
        # solve = self.define_internal_local()
        self.data.append(
            DataNode(f"type_name_{self.current_type.name}", f"{self.current_type.name}")
        )
        # self.register_instruction(AllocateNode("String", solve))
        type_name = self.define_internal_local()
        self.register_instruction(
            LoadNode(
                type_name,
                VariableInfo(
                    f"type_name_{self.current_type.name}",
                    None,
                    f"{self.current_type.name}",
                ),
            )
        )
        # self.register_instruction(AssignNode(solve, type_name))
        self.register_instruction(ReturnNode(type_name))

    def io_outstring(self):
        self.params.append(ParamNode("self"))
        str_arg = VariableInfo("str")
        self.register_param(str_arg)
        self.register_instruction(PrintStrNode(str_arg.name))
        self.register_instruction(ReturnNode("self"))

    def io_outint(self):
        self.params.append(ParamNode("self"))
        int_arg = VariableInfo("int")
        self.register_param(int_arg)
        self.register_instruction(PrintIntNode(int_arg.name))
        self.register_instruction(ReturnNode("self"))

    def io_instring(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(ReadStringNode(ret_vinfo))
        self.register_instruction(ReturnNode(ret_vinfo))

    def io_inint(self):
        self.params.append(ParamNode("self"))
        ret_vinfo = self.define_internal_local()
        self.register_instruction(ReadIntNode(ret_vinfo))  # TODO: ReadInt?
        self.register_instruction(ReturnNode(ret_vinfo))

    def reset_state(self):
        self.types = []
        self.code = []
        self.data = []
        self.current_type = None
        self.current_function = None
        self.string_count = 0
        self._count = 0
        self.context = None

    @visitor.on("node")
    def visit(self, node=None, return_var=None):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node, return_var=None):
        self.context = node.context

        for type in self.context.types.values():
            self.attrs[type.name] = {
                attr.name: (i, htype.name)
                for i, (attr, htype) in enumerate(type.all_attributes())
            }
            self.methods[type.name] = {
                method.name: (i, htype.name)
                if htype.name != "Object" or method.name not in ["type_name", "copy"]
                else (i, type.name)
                for i, (method, htype) in enumerate(type.all_methods())
            }
        # self.dottypes.append(
        #     cil.TypeNode(
        #         type.name,
        #         list(self.attrs[type.name].keys()),
        #         [
        #             self.get_func_id(htype, method)
        #             for method, (_, htype) in self.methods[type.name].items()
        #         ],
        #     )
        # )

        self.current_function = FunctionNode("main", [], [], [])
        self.code.append(self.current_function)

        instance = self.define_internal_local()
        result = self.define_internal_local()

        main_constructor = self.to_function_name("constructor", "Main")
        main_method_name = self.to_function_name("main", "Main")

        # Get instance from constructor
        self.register_instruction(StaticCallNode(main_constructor, instance))

        # Pass instance as parameter and call Main_main
        self.register_instruction(ArgNode(instance))
        self.register_instruction(StaticCallNode(main_method_name, result))

        # self.register_instruction(ReturnNode(0))
        self.register_instruction(ExitNode())

        self.current_function = None

        self.add_builtin_functions()
        self.add_builtin_constructors()

        for declaration in node.declarations:
            self.visit(declaration)

        program_node = ProgramNode(self.types, self.data, self.code)

        self.reset_state()

        return program_node

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node, return_var=None):
        self.current_type = self.context.get_type(node.id)

        self.register_copy()
        self.register_type_name()

        type_node = self.register_type(self.current_type.name)
        self.build_constructor(node)

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

        index = type_node.methods.index(
            ("copy", self.to_function_name("copy", "Object"))
        )
        type_node.methods[index] = (
            "copy",
            self.to_function_name("copy", self.current_type.name),
        )

        index = type_node.methods.index(
            ("type_name", self.to_function_name("type_name", "Object"))
        )
        type_node.methods[index] = (
            "type_name",
            self.to_function_name("type_name", self.current_type.name),
        )
        for feature in node.features:
            self.visit(feature)

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node, return_var=None):
        pass

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node, return_var=None):
        self.current_method = self.current_type.get_method(node.id)

        # Add function to .CODE
        self.current_function = self.register_function(
            self.to_function_name(node.id, self.current_type.name)
        )

        # Add params
        self.current_function.params.append(ParamNode("self"))
        for pname, _ in node.params:
            self.register_param(VariableInfo(pname))

        # Body
        value = self.define_internal_local()
        self.visit(node.body, value)

        # Return
        if isinstance(self.current_method.return_type, VoidType):
            value = None

        self.register_instruction(ReturnNode(value))

        self.current_method = None
        self.current_function = None

    @visitor.when(cool.AssignNode)
    def visit(self, node, return_var):
        self.visit(node.expr, return_var)

        local_id = self.get_local(node.id)
        if any(local_id == l.name for l in self.current_function.localvars):
            self.register_instruction(AssignNode(local_id, return_var))
            return

        param_id = self.get_param(node.id)
        if any(param_id == p.name for p in self.current_function.params):
            self.register_instruction(AssignNode(param_id, return_var))
            return

        self.register_instruction(
            SetAttribNode(
                "self",
                self.to_attr_name(self.current_type.name, node.id),
                return_var,
                self.current_type.name,
            )
        )

    @visitor.when(cool.CallNode)
    def visit(self, node, return_var):
        obj_type = self.current_type.name
        instance = self.define_internal_local()
        if node.obj:
            self.visit(node.obj, instance)
            obj_type = node.obj.static_type.name

        else:
            self.register_instruction(AssignNode(instance, "self"))

        instance_type = None
        if not node.at_type:
            instance_type = self.define_internal_local()
            if obj_type in ["Int","Bool"]:
                self.register_instruction(TypeOfNode(instance, instance_type,True,obj_type))
            else:
                self.register_instruction(TypeOfNode(instance, instance_type))

        args = [instance]
        for arg in node.args:
            arg_value = self.define_internal_local()
            self.visit(arg, arg_value)
            args.append(arg_value)

        for arg in args:
            self.register_instruction(ArgNode(arg))

        if node.at_type:
            self.register_instruction(
                StaticCallNode(self.to_function_name(node.id, node.at_type), return_var)
            )

        else:
            method_index = self.get_method_id(obj_type, node.id)
            self.register_instruction(
                DynamicCallNode(instance_type, method_index, return_var)
            )

    @visitor.when(cool.IfNode)
    def visit(self, node, return_var):
        # IF condition GOTO label
        condition_value = self.define_internal_local()
        self.visit(node.if_expr, condition_value)
        then_label = "THEN_" + self.next_id()
        self.register_instruction(GotoIfNode(condition_value, then_label))

        # Else
        self.visit(node.else_expr, return_var)

        # GOTO end_label
        end_label = "END_IF_" + self.next_id()  # Example: END_IF_120
        self.register_instruction(GotoNode(end_label))

        # Then label
        self.register_instruction(LabelNode(then_label))
        self.visit(node.then_expr, return_var)

        # end_label
        self.register_instruction(LabelNode(end_label))

    @visitor.when(cool.WhileNode)
    def visit(self, node, return_var):
        # While label
        while_label = "WHILE_" + self.next_id()
        self.register_instruction(LabelNode(while_label))

        # Condition
        c = self.define_internal_local()
        self.visit(node.condition, c)

        # If condition GOTO body_label
        body_label = "BODY_" + self.next_id()
        self.register_instruction(GotoIfNode(c, body_label))

        # GOTO end_while label
        end_while_label = "END_WHILE_" + self.next_id()
        self.register_instruction(GotoNode(end_while_label))

        # Body
        self.register_instruction(LabelNode(body_label))
        self.visit(node.body, self.define_internal_local())

        # GOTO while label
        self.register_instruction(GotoNode(while_label))

        # End while label
        self.register_instruction(LabelNode(end_while_label))

        self.register_instruction(DefaultValueNode(return_var, "Void"))

    @visitor.when(cool.BlockNode)
    def visit(self, node, return_var):
        for expr in node.expression_list:
            self.visit(expr, return_var)

    @visitor.when(cool.LetNode)
    def visit(self, node, return_var):
        for var_dec in node.identifiers:
            self.visit(var_dec)

        self.visit(node.body, return_var)

    @visitor.when(cool.VarDeclarationNode)
    def visit(self, node, return_var=None):
        # Add LOCAL variable
        idx = self.get_local(node.id)
        if not any(idx == l.name for l in self.current_function.localvars):
            self.register_local(node.id)

        # Add Assignment Node
        if node.expr:
            self.visit(node.expr, idx)
        else:
            self.register_instruction(DefaultValueNode(idx, node.type))

    @visitor.when(cool.CaseNode)
    def visit(self, node, return_var=None):
        def get_children(static_type):
            children = []
            for t in self.context.types.values():
                 if t.conforms_to(static_type):
                     children.append(t)

            return children

        def get_least_type(expr_dynamic_type):
            case_item_types = [case_item.type for case_item in node.case_items]
            solve = expr_dynamic_type
            while solve is not None:
                if solve.name in case_item_types:
                    return solve.name
                solve = solve.parent

            return None

        def get_asserted_branch(least_type:str):
            for case_item in node.case_items:
                if case_item.type == least_type:
                    return case_item
            return None

        expr_value = self.define_internal_local()
        self.visit(node.expr, expr_value)

        possible_dynamic_types = get_children(node.expr.static_type)

        branch_labels = []
        for t in possible_dynamic_types:
            dynamic_type = self.define_internal_local()
            self.register_instruction(TypeOfNode(expr_value, dynamic_type))

            label = "BRANCH" + self.next_id()
            equals = self.define_internal_local()
            self.register_instruction(CompareTypes(equals, dynamic_type, t.name))
            self.register_instruction(GotoIfNode(equals,label))

            least_type = get_least_type(t)
            asserted_branch = get_asserted_branch(least_type)
            branch_labels.append((asserted_branch, label))
        

        self.data.append(
            DataNode("runtime_error", "No branch can be selected for evaluation")
        )
        error = self.define_internal_local()
        self.register_instruction(
            LoadNode(
                error,
                VariableInfo(
                    "runtime_error",
                    None,
                    "No branch can be selected for evaluation",
                ),
            )
        )
        self.register_instruction(RuntimeErrorNode(error))

        end_case_label = "END_CASE_" + self.next_id()
        for branch, label in branch_labels:
            if not branch:
                continue
            self.register_instruction(LabelNode(label))
            new_local = self.register_local(branch.id)
            self.register_instruction(AssignNode(new_local, expr_value))

            self.visit(branch.expr, return_var)
            self.register_instruction(GotoNode(end_case_label))

        self.register_instruction(LabelNode(end_case_label))

    @visitor.when(cool.CaseItemNode)
    def visit(self, node, return_var=None):
        pass  # TODO: Pending!!!

    # Arithmetic and comparison operators
    @visitor.when(cool.PlusNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(PlusNode(return_var, left, right))

    @visitor.when(cool.MinusNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(MinusNode(return_var, left, right))

    @visitor.when(cool.StarNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(StarNode(return_var, left, right))

    @visitor.when(cool.DivNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(DivNode(return_var, left, right))

    @visitor.when(cool.LessEqualNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(LessEqualNode(return_var, left, right))

    @visitor.when(cool.LessNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)

        self.register_instruction(LessNode(return_var, left, right))

    @visitor.when(cool.EqualNode)
    def visit(self, node, return_var):
        left = self.define_internal_local()
        self.visit(node.left, left)

        right = self.define_internal_local()
        self.visit(node.right, right)
        
        if node.left.static_type.name == "String":
            self.register_instruction(StrEqualNode(return_var, left, right))
        else:
            self.register_instruction(EqualNode(return_var, left, right))

    # Unary operators
    @visitor.when(cool.InstantiateNode)  # NewNode
    def visit(self, node, return_var):
        self.register_instruction(
            StaticCallNode(self.to_function_name("constructor", node.lex), return_var)
        )

    @visitor.when(cool.IsvoidNode)
    def visit(self, node, return_var):
        value = self.define_internal_local()
        self.visit(node.expr, value)
        self.register_instruction(IsVoidNode(return_var, value))

    @visitor.when(cool.NotNode)
    def visit(self, node, return_var):
        value = self.define_internal_local()
        self.visit(node.expr, value)
        constant = self.define_internal_local()
        self.register_instruction(
            StaticCallNode(self.to_function_name("constructor", "Bool"), constant)
        )
        self.register_instruction(AssignNode(constant, 1))
        self.register_instruction(MinusNode(return_var, constant, value))

    @visitor.when(cool.NegNode)
    def visit(self, node, return_var):
        value = self.define_internal_local()
        self.visit(node.expr, value)
        self.register_instruction(IntComplementNode(return_var, value))

    @visitor.when(cool.ConstantNumNode)
    def visit(self, node, return_var):
        self.register_instruction(AssignNode(return_var, int(node.lex)))

    @visitor.when(cool.VariableNode)
    def visit(self, node, return_var):

        if node.lex == "self":
            self.register_instruction(AssignNode(return_var, "self"))
            return

        local_id = self.get_local(node.lex)
        if any(local_id == l.name for l in self.current_function.localvars):
            self.register_instruction(AssignNode(return_var, local_id))
            return

        param_id = self.get_param(node.lex)
        if any(param_id == p.name for p in self.current_function.params):
            self.register_instruction(AssignNode(return_var, param_id))
            return

        self.register_instruction(
            GetAttribNode(
                return_var,
                "self",
                self.to_attr_name(self.current_type.name, node.lex),
                self.current_type.name,
            )
        )

    @visitor.when(cool.StringNode)
    def visit(self, node, return_var):
        idx = self.generate_next_string_id()
        self.data.append(DataNode(idx, node.lex))
        self.register_instruction(
            LoadNode(return_var, VariableInfo(idx, None, node.lex))
        )

    @visitor.when(cool.BooleanNode)
    def visit(self, node, return_var):
        self.register_instruction(
            AssignNode(return_var, 1 if node.lex == "true" else 0)
        )

    @visitor.when(cool.DefaultValueNode)
    def visit(self, node, return_var):
        self.register_instruction(DefaultValueNode(return_var, node.type))
