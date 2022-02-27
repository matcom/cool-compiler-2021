from ...cmp import cil_ast as cil
from ...cmp.ast import (
    AssignNode,
    AttrDeclarationNode,
    BlockNode,
    CallNode,
    CaseBranchNode,
    CaseNode,
    ClassDeclarationNode,
    ConditionalNode,
    ConstantBoolNode,
    ConstantNumNode,
    ConstantStringNode,
    DivNode,
    EqualNode,
    FuncDeclarationNode,
    InstantiateNode,
    LeqNode,
    LessNode,
    LetNode,
    LetVarNode,
    LoopNode,
    MinusNode,
    NegNode,
    NotNode,
    PlusNode,
    ProgramNode,
    StarNode,
    VariableNode,
    VoidNode,
)
from ...cmp.semantic import (
    Context,
    Method,
    Scope,
    SemanticError,
    SelfType,
    Type,
    VariableInfo,
)
from typing import List, Optional
import compiler.visitors.visitor as visitor


class BaseCOOLToCILVisitor:
    def __init__(self, context: Context):
        self.dottypes: List[cil.TypeNode] = []
        self.dotdata: List[cil.DataNode] = []
        self.dotcode: List[cil.FunctionNode] = []
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_function: Optional[cil.FunctionNode] = None
        self.context = context
        self.vself = VariableInfo("self", None)
        self.value_types = ["String", "Int", "Bool"]

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def ids(self):
        return self.current_function.ids

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_local(self, vinfo, id=False):
        new_vinfo = VariableInfo("", None)
        if (
            len(self.current_function.name) >= 8
            and self.current_function.name[:8] == "function"
        ):
            new_vinfo.name = f"local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}"
        else:
            new_vinfo.name = f"local_{self.current_function.name[5:]}_{vinfo.name}_{len(self.localvars)}"

        local_node = cil.LocalNode(new_vinfo.name)
        if id:
            self.ids[vinfo.name] = new_vinfo.name
        self.localvars.append(local_node)
        return new_vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo("internal", None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f"function_{method_name}_at_{type_name}"

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_param(self, vinfo):
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f"data_{len(self.dotdata)}"
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f"{label}_{self.current_function.labels_count}"
        self.current_function.labels_count += 1
        return cil.LabelNode(lname)

    def register_runtime_error(self, condition, msg):
        error_node = self.register_label("error_label")
        continue_node = self.register_label("continue_label")
        self.register_instruction(cil.GotoIfNode(condition, error_node.label))
        self.register_instruction(cil.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(cil.ErrorNode(data_node))

        self.register_instruction(continue_node)

    def init_name(self, type_name, attr=False):
        if attr:
            return f"init_attr_at_{type_name}"
        return f"init_at_{type_name}"

    def buildHierarchy(self, t: str):
        if t == "Object":
            return None
        return {
            x.name
            for x in self.context.types.values()
            if x.name != "AUTO_TYPE" and x.conforms_to(self.context.get_type(t))
        }

    def register_built_in(self):
        # Object
        type_node = self.register_type("Object")

        # init Object
        self.current_function = self.register_function(self.init_name("Object"))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Object", instance))
        self.register_instruction(cil.ReturnNode(instance))

        # abort Object
        self.current_function = self.register_function(
            self.to_function_name("abort", "Object")
        )
        self.register_param(self.vself)
        vname = self.define_internal_local()
        data_node = [
            dn for dn in self.dotdata if dn.value == "Abort called from class "
        ][0]
        self.register_instruction(cil.LoadNode(vname, data_node))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.TypeNameNode(vname, self.vself.name))
        self.register_instruction(cil.PrintStrNode(vname))
        data_node = self.register_data("\n")
        self.register_instruction(cil.LoadNode(vname, data_node))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ExitNode())

        # type_name Object
        self.current_function = self.register_function(
            self.to_function_name("type_name", "Object")
        )
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeNameNode(result, self.vself.name))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name("String"), instance)
        )
        self.register_instruction(cil.ReturnNode(instance))

        # copy Object
        self.current_function = self.register_function(
            self.to_function_name("copy", "Object")
        )
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        # Object
        type_node.methods = [
            (name, self.to_function_name(name, "Object"))
            for name in ["abort", "type_name", "copy"]
        ]
        type_node.methods += [("init", self.init_name("Object"))]
        obj_methods = ["abort", "type_name", "copy"]

        ##############################################

        # IO
        type_node = self.register_type("IO")

        # init IO
        self.current_function = self.register_function(self.init_name("IO"))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("IO", instance))
        self.register_instruction(cil.ReturnNode(instance))

        # out_string IO
        self.current_function = self.register_function(
            self.to_function_name("out_string", "IO")
        )
        self.register_param(self.vself)
        self.register_param(VariableInfo("x", None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, "x", "value", "String"))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        # out_int IO
        self.current_function = self.register_function(
            self.to_function_name("out_int", "IO")
        )
        self.register_param(self.vself)
        self.register_param(VariableInfo("x", None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, "x", "value", "Int"))
        self.register_instruction(cil.PrintIntNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        # in_string IO
        self.current_function = self.register_function(
            self.to_function_name("in_string", "IO")
        )
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadStrNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name("String"), instance)
        )
        self.register_instruction(cil.ReturnNode(instance))

        # in_int IO
        self.current_function = self.register_function(
            self.to_function_name("in_int", "IO")
        )
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        self.register_instruction(cil.ReturnNode(instance))

        # IO
        type_node.methods = [
            (method, self.to_function_name(method, "Object")) for method in obj_methods
        ]
        type_node.methods += [
            (name, self.to_function_name(name, "IO"))
            for name in ["out_string", "out_int", "in_string", "in_int"]
        ]
        type_node.methods += [("init", self.init_name("IO"))]

        ##############################################

        # String
        type_node = self.register_type("String")
        type_node.attributes = ["value", "length"]

        # init String
        self.current_function = self.register_function(self.init_name("String"))
        self.register_param(VariableInfo("val", None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("String", instance))
        self.register_instruction(cil.SetAttribNode(instance, "value", "val", "String"))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, "val"))
        attr = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), attr))
        self.register_instruction(cil.SetAttribNode(instance, "length", attr, "String"))
        self.register_instruction(cil.ReturnNode(instance))

        # length String
        self.current_function = self.register_function(
            self.to_function_name("length", "String")
        )
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(
            cil.GetAttribNode(result, self.vself.name, "length", "String")
        )
        self.register_instruction(cil.ReturnNode(result))

        # concat String
        self.current_function = self.register_function(
            self.to_function_name("concat", "String")
        )
        self.register_param(self.vself)
        self.register_param(VariableInfo("s", None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        length_1 = self.define_internal_local()
        length_2 = self.define_internal_local()
        self.register_instruction(
            cil.GetAttribNode(str_1, self.vself.name, "value", "String")
        )
        self.register_instruction(cil.GetAttribNode(str_2, "s", "value", "String"))
        self.register_instruction(
            cil.GetAttribNode(length_1, self.vself.name, "length", "String")
        )
        self.register_instruction(cil.GetAttribNode(length_2, "s", "length", "String"))
        self.register_instruction(cil.GetAttribNode(length_1, length_1, "value", "Int"))
        self.register_instruction(cil.GetAttribNode(length_2, length_2, "value", "Int"))
        self.register_instruction(cil.PlusNode(length_1, length_1, length_2))

        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, str_1, str_2, length_1))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name("String"), instance)
        )
        self.register_instruction(cil.ReturnNode(instance))

        # subst String
        self.current_function = self.register_function(
            self.to_function_name("substr", "String")
        )
        self.register_param(self.vself)
        self.register_param(VariableInfo("i", None))
        self.register_param(VariableInfo("l", None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(
            cil.GetAttribNode(str_value, self.vself.name, "value", "String")
        )
        self.register_instruction(cil.GetAttribNode(index_value, "i", "value", "Int"))
        self.register_instruction(cil.GetAttribNode(length_value, "l", "value", "Int"))
        # Check Out of range error
        self.register_instruction(
            cil.GetAttribNode(length_attr, self.vself.name, "length", "String")
        )
        self.register_instruction(
            cil.PlusNode(length_substr, length_value, index_value)
        )
        self.register_instruction(cil.LessNode(less_value, length_attr, length_substr))
        self.register_runtime_error(less_value, "Substring out of range")
        self.register_instruction(
            cil.SubstringNode(result, str_value, index_value, length_value)
        )
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name("String"), instance)
        )
        self.register_instruction(cil.ReturnNode(instance))

        # String
        type_node.methods = [
            (method, self.to_function_name(method, "Object")) for method in obj_methods
        ]
        type_node.methods += [
            (name, self.to_function_name(name, "String"))
            for name in ["length", "concat", "substr"]
        ]
        type_node.methods += [("init", self.init_name("String"))]

        ##############################################

        # Int
        type_node = self.register_type("Int")
        type_node.attributes = ["value"]

        # init Int
        self.current_function = self.register_function(self.init_name("Int"))
        self.register_param(VariableInfo("val", None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Int", instance))
        self.register_instruction(cil.SetAttribNode(instance, "value", "val", "Int"))
        self.register_instruction(cil.ReturnNode(instance))

        # Int
        type_node.methods = [
            (method, self.to_function_name(method, "Object")) for method in obj_methods
        ]
        type_node.methods += [("init", self.init_name("Int"))]

        # Bool
        type_node = self.register_type("Bool")
        type_node.attributes = ["value"]

        # init Bool
        self.current_function = self.register_function(self.init_name("Bool"))
        self.register_param(VariableInfo("val", None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Bool", instance))
        self.register_instruction(cil.SetAttribNode(instance, "value", "val", "Bool"))
        self.register_instruction(cil.ReturnNode(instance))

        # Bool
        type_node.methods = [
            (method, self.to_function_name(method, "Object")) for method in obj_methods
        ]
        type_node.methods += [("init", self.init_name("Bool"))]


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        self.current_function = self.register_function("entry")
        result = self.define_internal_local()
        instance = self.register_local(VariableInfo("instance", None))
        self.register_instruction(cil.StaticCallNode(self.init_name("Main"), instance))
        self.register_instruction(cil.ArgNode(instance))
        main_method_name = self.to_function_name("main", "Main")
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))

        self.register_data("Abort called from class ")
        self.register_built_in()
        self.current_function = None

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current_type: Type = self.context.get_type(node.id)

        # Handle all the .TYPE section
        type_node = self.register_type(self.current_type.name)

        # TODO Check change next loop to use all_attributes and all_methods functions
        type_node.attributes.extend(
            [attr.name for attr, _ in self.current_type.all_attributes()]
        )
        type_node.methods.extend(
            [
                (method.name, self.to_function_name(method.name, typex.name))
                for method, typex in self.current_type.all_methods()
            ]
        )
        # visited_func = []
        # current = self.current_type
        # while current is not None:
        #     attributes = [attr.name for attr in current.attributes]
        #     methods = [
        #         func.name for func in current.methods if func.name not in visited_func
        #     ]
        #     visited_func.extend(methods)
        #     type_node.attributes.extend(attributes[::-1])
        #     type_node.methods.extend(
        #         [
        #             (item, self.to_function_name(item, current.name))
        #             for item in methods[::-1]
        #         ]
        #     )
        #     current = current.parent

        # type_node.attributes.reverse()
        # type_node.methods.reverse()

        for feature, child_scope in zip(node.features, scope.children):
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, child_scope)

        # init
        self.current_function = self.register_function(self.init_name(node.id))
        # allocate
        instance = self.register_local(VariableInfo("instance", None))
        self.register_instruction(cil.AllocateNode(node.id, instance))

        func = self.current_function
        vtemp = self.define_internal_local()

        # init_attr
        self.current_function = self.register_function(
            self.init_name(node.id, attr=True)
        )
        self.register_param(self.vself)
        parent_type = self.context.get_type(node.id).parent
        if parent_type.name != "Object" and parent_type.name != "IO":
            self.register_instruction(cil.ArgNode(self.vself.name))
            self.register_instruction(
                cil.StaticCallNode(self.init_name(parent_type.name, attr=True), vtemp)
            )

        for feature, child_scope in zip(node.features, scope.children):
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, child_scope)

        self.current_function = func
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(
            cil.StaticCallNode(self.init_name(node.id, attr=True), vtemp)
        )

        self.register_instruction(cil.ReturnNode(instance))
        self.current_function = None
        self.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):
        if node.expr:
            value = self.visit(node.expr, scope)
            self.register_instruction(
                cil.SetAttribNode(self.vself.name, node.id, value, self.current_type)
            )
            return value

        elif node.type in self.value_types:
            value = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, value))
            self.register_instruction(
                cil.SetAttribNode(self.vself.name, node.id, value, self.current_type)
            )
            return value

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.id)

        # Handle PARAMS
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, self.current_type.name)
        )

        self.register_param(self.vself)
        for param_name, _ in node.params:
            self.register_param(VariableInfo(param_name.lex, None))

        # Handle RETURN
        value = self.visit(node.body, scope)
        if value is None:
            self.register_instruction(cil.ReturnNode(""))
        elif self.current_function.name == "entry":
            self.register_instruction(cil.ReturnNode(0))
        else:
            self.register_instruction(cil.ReturnNode(value))

        self.current_method = None

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        value = self.visit(node.expr, scope)

        try:
            self.current_type.get_attribute(node.id)
            self.register_instruction(
                cil.SetAttribNode(
                    self.vself.name, node.id, value, self.current_type.name
                )
            )
        except SemanticError:
            vname = None
            # TODO - Splits by _ won't work
            param_names = [pn.name for pn in self.current_function.params]
            if node.id in param_names:
                vname = node.id
            else:
                vname = self.ids[node.id]
                # return self.data
                # for n in [lv.name for lv in self.current_function.localvars]:
                #     if node.id in n.split("_"):
                #         vname = n
                #         break
            self.register_instruction(cil.AssignNode(vname, value))

        return value

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        args = []
        for arg in node.args:
            vname = self.register_local(VariableInfo(f"{node.id}_arg", None), id=True)
            ret = self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, ret))
            args.append(cil.ArgNode(vname))
        result = self.register_local(
            VariableInfo(f"return_value_of_{node.id}", None), id=True
        )

        # static call node
        if (
            isinstance(node.obj, VariableNode)
            and node.obj.lex == self.vself.name
            and not node.type
        ):
            self.register_instruction(cil.ArgNode(self.vself.name))
            for arg in args:
                self.register_instruction(arg)

            type_of_node = self.register_local(
                VariableInfo(f"{self.vself.name}_type", None)
            )
            self.register_instruction(cil.TypeOfNode(self.vself.name, type_of_node))
            self.register_instruction(
                cil.DynamicCallNode(
                    type_of_node, node.id, result, self.current_type.name
                )
            )
            return result

        vobj = self.define_internal_local()
        ret = self.visit(node.obj, scope)
        self.register_instruction(cil.AssignNode(vobj, ret))

        # Check if node.obj is void
        void = cil.VoidNode()
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vobj, void))

        self.register_runtime_error(
            equal_result,
            f"{node.token.pos} - RuntimeError: Dispatch on void\n",
        )

        # self
        self.register_instruction(cil.ArgNode(vobj))
        for arg in args:
            self.register_instruction(arg)

        if node.type:
            # Call of type <obj>@<type>.id(<expr>,...,<expr>)
            self.register_instruction(
                cil.StaticCallNode(self.to_function_name(node.id, node.type), result)
            )
        else:
            # Call of type <obj>.<id>(<expr>,...,<expr>)
            type_of_node = self.register_local(
                VariableInfo(f"{node.id}_type", None), id=True
            )
            self.register_instruction(cil.TypeOfNode(vobj, type_of_node))
            computed_type = node.obj.computed_type
            if isinstance(computed_type, SelfType):
                computed_type = computed_type.fixed_type
            self.register_instruction(
                cil.DynamicCallNode(type_of_node, node.id, result, computed_type.name)
            )

        return result

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        vret = self.register_local(VariableInfo("if_then_else_value", None))
        vcondition = self.define_internal_local()

        then_label_node = self.register_label("then_label")
        else_label_node = self.register_label("else_label")
        continue_label_node = self.register_label("continue_label")

        # If condition GOTO then_label
        ret = self.visit(node.condition, scope)
        self.register_instruction(cil.GetAttribNode(vcondition, ret, "value", "Bool"))
        self.register_instruction(cil.GotoIfNode(vcondition, then_label_node.label))
        # GOTO else_label
        self.register_instruction(cil.GotoNode(else_label_node.label))
        # Label then_label
        self.register_instruction(then_label_node)
        retif = self.visit(node.then_body, scope)
        self.register_instruction(cil.AssignNode(vret, retif))
        self.register_instruction(cil.GotoNode(continue_label_node.label))
        # Label else_label
        self.register_instruction(else_label_node)
        retelse = self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(vret, retelse))

        self.register_instruction(continue_label_node)
        return vret

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope: Scope):
        vcondition = self.define_internal_local()
        while_label_node = self.register_label("while_label")
        loop_label_node = self.register_label("loop_label")
        pool_label_node = self.register_label("pool_label")
        # Label while
        self.register_instruction(while_label_node)
        # If condition GOTO loop
        ret = self.visit(node.condition, scope)
        self.register_instruction(cil.GetAttribNode(vcondition, ret, "value", "Bool"))
        self.register_instruction(cil.GotoIfNode(vcondition, loop_label_node.label))
        # GOTO pool
        self.register_instruction(cil.GotoNode(pool_label_node.label))
        # Label loop
        self.register_instruction(loop_label_node)
        ret = self.visit(node.body, scope)
        # GOTO while
        self.register_instruction(cil.GotoNode(while_label_node.label))
        # Label pool
        self.register_instruction(pool_label_node)

        # The result of a while loop is void
        return cil.VoidNode()

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        ret_value = None
        for expr in node.expr_list:
            ret_value = self.visit(expr, scope)

        return ret_value

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        vret = self.register_local(VariableInfo("let_in_value", None))

        for let_var_node in node.id_list:
            self.visit(let_var_node, scope)
        ret = self.visit(node.body, scope)
        self.register_instruction(cil.AssignNode(vret, ret))
        return vret

    @visitor.when(LetVarNode)
    def visit(self, node: LetVarNode, scope: Scope):
        try:
            vname = self.ids[node.id]
        except KeyError:
            vname = self.register_local(VariableInfo(node.id, node.typex), id=True)

        if node.expression:
            ret_value = self.visit(node.expression, scope)
            self.register_instruction(cil.AssignNode(vname, ret_value))
        elif node.typex in self.value_types:
            self.register_instruction(cil.AllocateNode(node.typex, vname))

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        ret = self.register_local(VariableInfo("case_expr_value", None))
        ret_type = self.register_local(VariableInfo("typeName_value", None))
        vcond = self.register_local(VariableInfo("equal_value", None))
        value = self.register_local(VariableInfo("case_value", None))

        ret_val = self.visit(node.expr, scope)

        self.register_instruction(cil.AssignNode(ret, ret_val))
        self.register_instruction(cil.TypeNameNode(ret_type, ret_val))

        # Check if node.expr is void and raise proper error if vexpr value is void
        void = cil.VoidNode()
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, ret, void))

        self.register_runtime_error(
            equal_result,
            f"{node.token.pos} - RuntimeError: Case on void\n",
        )

        # sorting the branches
        order = []
        for b in node.branch_list:
            count = 0
            t1 = self.context.get_type(b.typex)
            for other in node.branch_list:
                t2 = self.context.get_type(other.typex)
                count += t2.conforms_to(t1)
            order.append((count, b))
        order.sort(key=lambda x: x[0])

        labels = []
        old = {}
        for idx, (_, b) in enumerate(order):
            labels.append(self.register_label(f"{idx}_label"))
            h = self.buildHierarchy(b.typex)
            if not h:
                self.register_instruction(cil.GotoNode(labels[-1].label))
                break
            # TODO - Esto no hace falta
            h.add(b.typex)
            for s in old:
                h -= s
            for t in h:
                vbranch_type_name = self.register_local(
                    VariableInfo("branch_type_name", None)
                )
                self.register_instruction(cil.NameNode(vbranch_type_name, t))
                self.register_instruction(
                    cil.EqualNode(vcond, ret_type, vbranch_type_name)
                )
                self.register_instruction(cil.GotoIfNode(vcond, labels[-1].label))

        # Raise runtime error if no Goto was executed
        data_node = self.register_data(
            f"({node.token.pos[0] + 1 + len(node.branch_list)},{node.token.pos[1] - 5}) - RuntimeError: Execution of a case statement without a matching branch\n"
        )
        self.register_instruction(cil.ErrorNode(data_node))

        end_label = self.register_label("end_label")
        for idx, l in enumerate(labels):
            self.register_instruction(l)
            vid = self.register_local(VariableInfo(order[idx][1].id, None), id=True)
            self.register_instruction(cil.AssignNode(vid, ret))
            ret_2 = self.visit(order[idx][1], scope)
            self.register_instruction(cil.AssignNode(value, ret_2))
            self.register_instruction(cil.GotoNode(end_label.label))

        self.register_instruction(end_label)
        return value

    @visitor.when(CaseBranchNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        return self.visit(node.expression, scope)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        value = self.define_internal_local()
        instance = self.define_internal_local()

        ret = self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(value, ret, "value", "Bool"))
        self.register_instruction(cil.MinusNode(vname, 1, value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), instance))
        return instance

    @visitor.when(LeqNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(left_value, left, "value", "Bool"))
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "Bool")
        )
        self.register_instruction(cil.LeqNode(vname, left_value, right_value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), instance))
        return instance

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(left_value, left, "value", "Bool"))
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "Bool")
        )
        self.register_instruction(cil.LessNode(vname, left_value, right_value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), instance))
        return instance

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        type_left = self.define_internal_local()
        type_int = self.define_internal_local()
        type_bool = self.define_internal_local()
        type_string = self.define_internal_local()
        equal_result = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        self.register_instruction(cil.TypeNameNode(type_left, left))
        self.register_instruction(cil.NameNode(type_int, "Int"))
        self.register_instruction(cil.NameNode(type_bool, "Bool"))
        self.register_instruction(cil.NameNode(type_string, "String"))

        int_node = self.register_label("int_label")
        string_node = self.register_label("string_label")
        reference_node = self.register_label("reference_label")
        continue_node = self.register_label("continue_label")
        self.register_instruction(cil.EqualNode(equal_result, type_left, type_int))
        self.register_instruction(cil.GotoIfNode(equal_result, int_node.label))
        self.register_instruction(cil.EqualNode(equal_result, type_left, type_bool))
        self.register_instruction(cil.GotoIfNode(equal_result, int_node.label))
        self.register_instruction(cil.EqualNode(equal_result, type_left, type_string))
        self.register_instruction(cil.GotoIfNode(equal_result, string_node.label))
        self.register_instruction(cil.GotoNode(reference_node.label))

        self.register_instruction(int_node)
        self.register_instruction(cil.GetAttribNode(left_value, left, "value", "Int"))
        self.register_instruction(cil.GetAttribNode(right_value, right, "value", "Int"))
        self.register_instruction(cil.EqualNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(string_node)
        self.register_instruction(
            cil.GetAttribNode(left_value, left, "value", "String")
        )
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "String")
        )
        self.register_instruction(cil.EqualStrNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(reference_node)
        self.register_instruction(cil.EqualNode(vname, left, right))

        self.register_instruction(continue_node)
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), instance))
        return instance

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, right, "value", "Int"))
        self.register_instruction(cil.PlusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, right, "value", "Int"))
        self.register_instruction(cil.MinusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, right, "value", "Int"))
        self.register_instruction(cil.StarNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(vleft, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(vright, right, "value", "Int"))

        # Check division by 0
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vright, 0))
        self.register_runtime_error(
            equal_result,
            f"{node.token.pos} - RuntimeError: Division by zero\n",
        )

        self.register_instruction(cil.DivNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(VoidNode)
    def visit(self, node, scope):
        void = cil.VoidNode()
        value = self.define_internal_local()
        ret = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(value, ret))
        result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(result, value, void))
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), result))
        return result

    @visitor.when(NegNode)
    def visit(self, node, scope):
        vname = self.define_internal_local()
        value = self.define_internal_local()
        instance = self.define_internal_local()
        ret = self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(value, ret, "value", "Int"))
        self.register_instruction(cil.ComplementNode(vname, value))
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        instance = self.define_internal_local()

        if node.computed_type.name == SelfType().name:
            vtype = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(self.vself.name, vtype))
            self.register_instruction(cil.AllocateNode(vtype, instance))
        elif node.computed_type.name == "Int" or node.computed_type.name == "Bool":
            self.register_instruction(cil.ArgNode(0))
        elif node.computed_type.name == "String":
            data_node = [dn for dn in self.dotdata if dn.value == ""][0]
            vmsg = self.register_local(VariableInfo("msg", None))
            self.register_instruction(cil.LoadNode(vmsg, data_node))
            self.register_instruction(cil.ArgNode(vmsg))

        self.register_instruction(
            cil.StaticCallNode(self.init_name(node.computed_type.name), instance)
        )
        return instance

    @visitor.when(VariableNode)
    def visit(self, node, scope):

        try:
            self.current_type.get_attribute(node.lex)
            attr = self.register_local(VariableInfo(node.lex, None), id=True)
            self.register_instruction(
                cil.GetAttribNode(
                    attr, self.vself.name, node.lex, self.current_type.name
                )
            )
            return attr
        except SemanticError:
            param_names = [pn.name for pn in self.current_function.params]
            if node.lex in param_names:
                return node.lex
            else:
                return self.ids[node.lex]

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(int(node.lex)))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        return instance

    @visitor.when(ConstantStringNode)
    def visit(self, node, scope):
        try:
            data_node = [dn for dn in self.dotdata if dn.value == node.lex][0]
        except IndexError:
            data_node = self.register_data(node.lex)

        vmsg = self.register_local(VariableInfo("msg", None))
        ret = self.define_internal_local()
        self.register_instruction(cil.LoadNode(vmsg, data_node))
        self.register_instruction(cil.ArgNode(vmsg))
        self.register_instruction(cil.StaticCallNode(self.init_name("String"), ret))
        return ret

    @visitor.when(ConstantBoolNode)
    def visit(self, node, scope):
        if node.lex == "true":
            v = 1
        else:
            v = 0
        ret = self.define_internal_local()
        self.register_instruction(cil.ArgNode(v))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret
