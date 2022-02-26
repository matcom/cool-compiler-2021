from pprint import pprint
import compiler.visitors.visitor as visitor
from ..cmp import cil_ast as cil
from ..cmp.semantic import (
    Scope,
    SemanticError,
    ErrorType,
    IntType,
    BoolType,
    SelfType,
    AutoType,
    LCA,
    VariableInfo,
)
from ..cmp.ast import (
    CaseBranchNode,
    LeqNode,
    LessNode,
    LetVarNode,
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    FuncDeclarationNode,
)
from ..cmp.ast import (
    AssignNode,
    CallNode,
    CaseNode,
    BlockNode,
    LoopNode,
    ConditionalNode,
    LetNode,
)
from ..cmp.ast import ArithmeticNode, ComparisonNode, EqualNode
from ..cmp.ast import VoidNode, NotNode, NegNode
from ..cmp.ast import (
    ConstantNumNode,
    ConstantStringNode,
    ConstantBoolNode,
    VariableNode,
    InstantiateNode,
)
from ..cmp.ast import PlusNode, MinusNode, StarNode, DivNode


class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
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
        new_vinfo.name = (
            f"local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}"
        )

        local_node = cil.LocalNode(new_vinfo.name)
        if id:
            self.ids[vinfo.name] = new_vinfo.name
        self.localvars.append(local_node)
        return new_vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo("internal", None, None)
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
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################

        self.current_function = self.register_function("entry")
        instance = self.register_local(VariableInfo("instance", None))
        self.register_instruction(cil.StaticCallNode(self.init_name("Main"), instance))
        self.register_instruction(cil.ArgNode(instance))
        result = self.define_internal_local()
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
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################

        self.current_type = self.context.get_type(node.id)

        # Your code here!!! (Handle all the .TYPE section)
        type_node = self.register_type(self.current_type.name)

        visited_func = []
        current = self.current_type
        while current is not None:
            attributes = [attr.name for attr in current.attributes]
            methods = [
                func.name for func in current.methods if func.name not in visited_func
            ]
            visited_func.extend(methods)
            type_node.attributes.extend(attributes[::-1])
            type_node.methods.extend(
                [
                    (item, self.to_function_name(item, current.name))
                    for item in methods[::-1]
                ]
            )
            current = current.parent

        type_node.attributes.reverse()
        type_node.methods.reverse()

        func_declarations = (
            f for f in node.features if isinstance(f, FuncDeclarationNode)
        )
        for feature, child_scope in zip(func_declarations, scope.children):
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
        if node.parent.lex != "Object" and node.parent.lex != "IO":
            self.register_instruction(cil.ArgNode(self.vself.name))
            self.register_instruction(
                cil.StaticCallNode(self.init_name(node.parent, attr=True), vtemp)
            )
        attr_declarations = (
            f for f in node.features if isinstance(f, AttrDeclarationNode)
        )
        for feature in attr_declarations:
            self.visit(feature, scope)

        self.current_function = func
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(
            cil.StaticCallNode(self.init_name(node.id, attr=True), vtemp)
        )

        self.register_instruction(cil.ReturnNode(instance))
        self.current_function = None
        self.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        if node.expr:
            value = self.visit(node.expr, scope)
            self.register_instruction(
                cil.SetAttribNode(self.vself.name, node.id, value, self.current_type)
            )

        elif node.type in self.value_types:
            value = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, value))
            self.register_instruction(
                cil.SetAttribNode(self.vself.name, node.id, value, self.current_type)
            )

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################

        self.current_method = self.current_type.get_method(node.id)

        # Your code here!!! (Handle PARAMS)
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, self.current_type.name)
        )

        self.params.append(cil.ParamNode(self.vself.name))
        self.params.extend([cil.ParamNode(p) for p in self.current_method.param_names])

        value = self.visit(node.body, scope)

        # Your code here!!! (Handle RETURN)
        if value is None:
            self.register_instruction(cil.ReturnNode(""))
        elif self.current_function.name == "entry":
            self.register_instruction(cil.ReturnNode(0))
        else:
            self.register_instruction(cil.ReturnNode(value))

        self.current_method = None

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################

        # Your code here!!!
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
            param_names = [pn.name for pn in self.current_function.params]
            if node.id in param_names:
                for n in param_names:
                    if node.id in n.split("_"):
                        vname = n
                        break
            else:
                for n in [lv.name for lv in self.current_function.localvars]:
                    if node.id in n.split("_"):
                        vname = n
                        break
            self.register_instruction(cil.AssignNode(vname, value))

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        # node.type -> str
        ###############################

        args = []
        for arg in node.args:
            vname = self.register_local(VariableInfo(f"{node.id}_arg", None), id=True)
            ret = self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, ret))
            args.append(cil.ArgNode(vname))
        result = self.register_local(
            VariableInfo(f"return_value_of_{node.id}", None), id=True
        )

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
            if computed_type.name == "SELF_TYPE":
                computed_type = computed_type.fixed_type
            self.register_instruction(
                cil.DynamicCallNode(type_of_node, node.id, result, computed_type.name)
            )

        return result

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.if_body -> ExpressionNode
        # node.else_body -> ExpressionNode
        ##################################

        then_label_node = self.register_label("then_label")
        else_label_node = self.register_label("else_label")
        continue_label_node = self.register_label("continue_label")

        cond_ret = self.visit(node.condition, scope)

        cond_ret_value = self.define_internal_local()

        self.register_instruction(
            cil.GetAttribNode(cond_ret_value, cond_ret, "value", "Bool")
        )
        self.register_instruction(cil.GotoIfNode(cond_ret_value, then_label_node.label))
        self.register_instruction(cil.GotoNode(else_label_node.label))

        value = self.register_local(VariableInfo("if_then_else_value", None))

        # Label then_label
        self.register_instruction(then_label_node)
        ret_then = self.visit(node.then_body, scope)
        self.register_instruction(cil.AssignNode(cond_ret_value, ret_then))
        self.register_instruction(cil.GotoNode(continue_label_node.label))

        # Label else_label
        self.register_instruction(else_label_node)
        ret_else = self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(cond_ret_value, ret_else))

        self.register_instruction(continue_label_node)
        return cond_ret_value

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.body -> ExpressionNode
        ###################################

        while_label_node = self.register_label("while_label")
        loop_label_node = self.register_label("loop_label")
        pool_label_node = self.register_label("pool_label")

        condition = self.define_internal_local()
        self.register_instruction(while_label_node)

        condition_value = self.visit(node.condition, scope)

        self.register_instruction(
            cil.GetAttribNode(condition, condition_value, "value", "Bool")
        )

        self.register_instruction(cil.GotoIfNode(condition, loop_label_node.label))
        self.register_instruction(cil.GotoNode(pool_label_node.label))
        self.register_instruction(loop_label_node)

        self.visit(node.body, scope)

        self.register_instruction(cil.GotoNode(while_label_node.label))

        self.register_instruction(pool_label_node)

        return cil.VoidNode()

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        #######################################
        # node.expr_list -> [ ExpressionNode ... ]
        #######################################
        ret = self.register_local(VariableInfo("block_node_value", None))

        for expr in node.expr_list:
            ret_value = self.visit(expr, scope)

        self.register_instruction(cil.AssignNode(ret, ret_value))

        return ret

    @visitor.when(LetNode)
    def visit(self, node, scope):
        ############################################
        # node.id_list -> [(id, type, expr), ...]
        # node.in_body -> ExpressionNode
        ############################################
        value = self.register_local(VariableInfo("let_in_value", None))

        for let_var in node.id_list:
            self.visit(let_var, scope)

        ret_val = self.visit(node.body, scope)
        self.register_instruction(cil.AssignNode(value, ret_val))

        return value

    @visitor.when(LetVarNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        if node.id in self.ids:
            vname = self.ids[node.id]
        else:
            vname = self.register_local(VariableInfo(node.id, node.typex), id=True)
        if node.expression:
            ret_value = self.visit(node.expression, scope)
            self.register_instruction(cil.AssignNode(vname, ret_value))
        elif node.typex in self.value_types:
            self.register_instruction(cil.AllocateNode(node.typex, vname))

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        ##############################################
        # node.expr -> ExpressionNode
        # node.branches -> [(id, type, expr), ... }
        ##############################################
        ret = self.register_local(VariableInfo("case_expr_value", None))
        ret_type = self.register_local(VariableInfo("typeName_value", None))
        vcond = self.register_local(VariableInfo("equal_value", None))
        value = self.register_local(VariableInfo("case_value", None))

        ret_val = self.visit(node.expr, scope)

        self.register_instruction(cil.AssignNode(ret, ret_val))
        self.register_instruction(cil.TypeOfNode(ret_type, ret_val))

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
        ret = self.register_local(VariableInfo("block_node_value", None))

        ret_value = self.visit(node.expression, scope)

        self.register_instruction(cil.AssignNode(ret, ret_value))

        return ret

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        ret = self.define_internal_local()
        ret_minus_1 = self.define_internal_local()
        value = self.define_internal_local()

        ret_value = self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(ret, ret_value, "value", "Bool"))
        self.register_instruction(cil.MinusNode(ret_minus_1, 1, ret))

        self.register_instruction(cil.ArgNode(ret_minus_1))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), value))
        return value

    @visitor.when(LeqNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        ret_value = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        value = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        self.register_instruction(cil.GetAttribNode(left_value, left, "value", "Bool"))
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "Bool")
        )
        self.register_instruction(cil.LeqNode(ret_value, left_value, right_value))

        self.register_instruction(cil.ArgNode(ret_value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), value))

        return value

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        value = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(left_value, left, "value", "Bool"))
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "Bool")
        )
        self.register_instruction(cil.LessNode(value, left_value, right_value))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), value))
        return value

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        return_vale = self.define_internal_local()
        type_left = self.define_internal_local()
        type_int = self.define_internal_local()
        type_bool = self.define_internal_local()
        type_string = self.define_internal_local()
        equal_result = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        ret = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        self.register_instruction(cil.TypeOfNode(type_left, left))
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
        self.register_instruction(cil.EqualNode(return_vale, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(string_node)
        self.register_instruction(
            cil.GetAttribNode(left_value, left, "value", "String")
        )
        self.register_instruction(
            cil.GetAttribNode(right_value, right, "value", "String")
        )
        self.register_instruction(
            cil.EqualStrNode(return_vale, left_value, right_value)
        )
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(reference_node)
        self.register_instruction(cil.EqualNode(return_vale, left, right))

        self.register_instruction(continue_node)
        self.register_instruction(cil.ArgNode(return_vale))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        value_left = self.define_internal_local()
        value_right = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(value_left, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(value_right, right, "value", "Int"))

        self.register_instruction(cil.PlusNode(value, value_left, value_right))

        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        value_left = self.define_internal_local()
        value_right = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(value_left, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(value_right, right, "value", "Int"))

        self.register_instruction(cil.LessNode(value, value_left, value_right))

        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        value_left = self.define_internal_local()
        value_right = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(value_left, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(value_right, right, "value", "Int"))

        self.register_instruction(cil.StarNode(value, value_left, value_right))

        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        value_left = self.define_internal_local()
        value_right = self.define_internal_local()
        left = self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(value_left, left, "value", "Int"))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(value_right, right, "value", "Int"))

        # Check division by 0
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, value_right, 0))
        self.register_runtime_error(
            equal_result,
            f"{node.token.pos} - RuntimeError: Division by zero\n",
        )

        self.register_instruction(cil.DivNode(value, value_left, value_right))

        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(VoidNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        void = cil.VoidNode()
        value = self.define_internal_local()
        left = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(value, left))

        ret = self.define_internal_local()
        self.register_instruction(cil.EqualNode(ret, value, void))
        self.register_instruction(cil.ArgNode(ret))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret

    @visitor.when(NegNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        complement_value = self.define_internal_local()
        ret = self.define_internal_local()
        left = self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(value, left, "value", "Int"))

        self.register_instruction(cil.ComplementNode(complement_value, value))
        self.register_instruction(cil.ArgNode(complement_value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.type -> str
        ###############################
        ret = self.define_internal_local()

        if node.computed_type.name == SelfType().name:
            value = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(value, node.computed_type.name))
            self.register_instruction(cil.AllocateNode(value, ret))
        elif node.computed_type.name == "Int" or node.computed_type.name == "Bool":
            self.register_instruction(cil.ArgNode(0))
        elif node.computed_type.name == "String":
            data_node = [dn for dn in self.dotdata if dn.value == ""][0]
            vmsg = self.register_local(VariableInfo("msg", None))
            self.register_instruction(cil.LoadNode(vmsg, data_node))
            self.register_instruction(cil.ArgNode(vmsg))

        self.register_instruction(
            cil.StaticCallNode(self.init_name(node.computed_type.name), ret)
        )
        return ret

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

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
                for n in param_names:
                    if node.lex == n:
                        return n
            else:
                return self.ids[node.lex]

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(int(node.lex)))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), instance))
        scope.ret_expr = instance

    @visitor.when(ConstantStringNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
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
        ###############################
        # node.lex -> str
        ###############################
        if node.lex == "true":
            v = 1
        else:
            v = 0
        ret = self.define_internal_local()
        self.register_instruction(cil.ArgNode(v))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret
