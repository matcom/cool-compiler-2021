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
    LeqNode,
    LessNode,
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

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_local(self, vinfo):
        vinfo.name = (
            f"local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}"
        )
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

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
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name("main", "Main")
        self.register_instruction(cil.AllocateNode("Main", instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
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

        self.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        expr = self.visit(node.expr, scope)
        if node.expr:
            self.register_instruction(cil.SetAttribNode(node.type, node.id, expr))

        elif node.type in self.value_types:
            value = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, value))
            self.register_instruction(cil.SetAttribNode(self.type, node.id, value))

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
        self.current_vars = {}
        self.params.append(cil.ParamNode("self"))
        self.params.extend([cil.ParamNode(p) for p in self.current_method.param_names])

        value = self.visit(node.body, scope)

        # Your code here!!! (Handle RETURN)
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None

        self.current_method = None

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################

        # Your code here!!!
        value = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(node.id, value))

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        # node.type -> str
        ###############################

        # Your code here!!!
        values = [self.visit(node.obj, scope)]
        values.extend([self.visit(arg, scope) for arg in node.args])
        local_vars = [self.define_internal_local() for v in values]
        for (var, val) in zip(local_vars, values):
            self.register_instruction(cil.AssignNode(var, val))

        for var in local_vars:
            self.register_instruction(cil.ArgNode(var))

        return_var = self.register_local(VariableInfo("call_node_value", None))
        if node.type:  # Dynamic Call
            self.register_instruction(
                cil.DynamicCallNode(node.type, node.id, return_var)
            )
        elif values[0] == "self":  # Static call
            function = self.to_function_name(node.id, self.current_type.name)
            self.register_instruction(cil.StaticCallNode(function, return_var))
        else:  # Dynamic Call with type of obj
            type_var = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(local_vars[0], type_var))
            self.register_instruction(
                cil.DynamicCallNode(type_var, node.id, return_var)
            )

        return return_var

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
        self.register_instruction(cil.GotoIfNode(cond_ret, then_label_node.label))
        self.register_instruction(cil.GotoNode(else_label_node.label))

        ret = self.register_local(VariableInfo("if_then_else_value", None))

        # Label then_label
        self.register_instruction(then_label_node)
        ret_then = self.visit(node.then_body, scope)
        self.register_instruction(cil.AssignNode(ret, ret_then))
        self.register_instruction(cil.GotoNode(continue_label_node.label))

        # Label else_label
        self.register_instruction(else_label_node)
        ret_else = self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(ret, ret_else))

        self.register_instruction(continue_label_node)
        return ret

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

        condition_ret = self.visit(node.condition, scope)
        self.register_instruction(cil.AssignNode(condition, condition_ret))

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
        # node.exprs -> [ ExpressionNode ... ]
        #######################################
        ret = self.register_local(VariableInfo("block_node_value", None))

        for expr in node.exprs:
            ret_value = self.visit(expr, scope)

        self.register_instruction(cil.AssignNode(ret, ret_value))

        return ret

    @visitor.when(LetNode)
    def visit(self, node, scope):
        ############################################
        # node.id_list -> [(id, type, expr), ...]
        # node.in_body -> ExpressionNode
        ############################################
        ret = self.register_local(VariableInfo("let_in_value", None))

        values = [self.visit(l.expr, scope) for l in node.id_list]
        local_vars = [self.define_internal_local() for _ in values]
        for (var, val) in zip(local_vars, values):
            self.register_instruction(cil.AssignNode(var, val))

        ret_val = self.visit(node.in_body, scope)
        self.register_instruction(cil.AssignNode(ret, ret_val))

        return ret

    # create case visitor
    # @visitor.when(CaseNode)
    # def visit(self, node, scope):
    #     ##############################################
    #     # node.expr -> ExpressionNode
    #     # node.branches -> [(id, type, expr), ... }
    #     ##############################################
    #     ret = self.register_local(VariableInfo("case_expr_value", None))
    #     ret_type = self.register_local(VariableInfo("typeName_value", None))
    #     vcond = self.register_local(VariableInfo("equal_value", None))
    #     ret = self.register_local(VariableInfo("case_value", None))

    #     ret_val = self.visit(node.expr, scope)

    #     self.register_instruction(cil.AssignNode(ret, ret_val))
    #     self.register_instruction(cil.TypeOfNode(ret_type, ret_val))

    #     # Check if node.expr is void and raise proper error if vexpr value is void
    #     void = cil.VoidNode()
    #     equal_result = self.define_internal_local()
    #     self.register_instruction(cil.EqualNode(equal_result, ret, void))

    #     self.register_runtime_error(
    #         equal_result,
    #         f"({node.position.row},{node.position.column}) - RuntimeError: Case on void\n",
    #     )

    #     end_label = self.register_label("end_label")
    #     labels = []
    #     old = {}

    #     # sorting the branches
    #     order = []
    #     for b in node.branches:
    #         count = 0
    #         t1 = self.context.get_type(b.type)
    #         for other in node.branches:
    #             t2 = self.context.get_type(other.type)
    #             count += t2.conforms_to(t1)
    #         order.append((count, b))
    #     order.sort(key=lambda x: x[0])

    #     for idx, (_, b) in enumerate(order):
    #         labels.append(self.register_label(f"{idx}_label"))
    #         h = self.buildHierarchy(b.type)
    #         if not h:
    #             self.register_instruction(cil.GotoNode(labels[-1].label))
    #             break
    #         h.add(b.type)
    #         for s in old:
    #             h -= s
    #         for t in h:
    #             vbranch_type_name = self.register_local(
    #                 VariableInfo("branch_type_name", None)
    #             )
    #             self.register_instruction(cil.NameNode(vbranch_type_name, t))
    #             self.register_instruction(
    #                 cil.EqualNode(vcond, vtype, vbranch_type_name)
    #             )
    #             self.register_instruction(cil.GotoIfNode(vcond, labels[-1].label))

    #     # Raise runtime error if no Goto was executed
    #     data_node = self.register_data(
    #         f"({token.row + 1 + len(node.branches)},{token.column - 5}) - RuntimeError: Execution of a case statement without a matching branch\n"
    #     )
    #     self.register_instruction(cil.ErrorNode(data_node))

    #     for idx, l in enumerate(labels):
    #         self.register_instruction(l)
    #         vid = self.register_local(VariableInfo(order[idx][1].id, None), id=True)
    #         self.register_instruction(cil.AssignNode(vid, vexpr))
    #         self.visit(order[idx][1], scope)
    #         self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
    #         self.register_instruction(cil.GotoNode(end_label.label))

    #     scope.ret_expr = vret
    #     self.register_instruction(end_label)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        value_minus_1 = self.define_internal_local()
        ret = self.define_internal_local()

        ret_value = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(value, ret_value))
        self.register_instruction(cil.MinusNode(value_minus_1, 1, value))

        self.register_instruction(cil.ArgNode(value_minus_1))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret

    @visitor.when(LeqNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        ret_value = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        ret = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        self.register_instruction(cil.AssignNode(left_value, left))
        self.register_instruction(cil.AssignNode(right_value, right))
        self.register_instruction(cil.LessEqualNode(ret_value, left_value, right_value))

        self.register_instruction(cil.ArgNode(ret_value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))

        return ret

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        value = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        ret = self.define_internal_local()

        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(left_value, left))
        self.register_instruction(cil.AssignNode(right_value, right))
        self.register_instruction(cil.LessNode(value, left_value, right_value))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name("Bool"), ret))
        return ret

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
        self.register_instruction(cil.AssignNode(left_value, left))
        self.register_instruction(cil.AssignNode(right_value, right))
        self.register_instruction(cil.EqualNode(return_vale, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(string_node)
        self.register_instruction(cil.AssignNode(left_value, left))
        self.register_instruction(cil.AssignNode(right_value, right))
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
        self.register_instruction(cil.AssignNode(value_left, left))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(value_right, right))

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
        self.register_instruction(cil.AssignNode(value_left, left))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(value_right, right))

        self.register_instruction(cil.MinusNode(value, value_left, value_right))

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
        self.register_instruction(cil.AssignNode(value_left, left))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(value_right, right))

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
        self.register_instruction(cil.AssignNode(value_left, left))
        right = self.visit(node.right, scope)
        self.register_instruction(cil.AssignNode(value_right, right))

        # Check division by 0
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, value_right, 0))
        self.register_runtime_error(
            equal_result,
            f"({node.position.row},{node.position.column}) - RuntimeError: Division by zero\n",
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
        self.register_instruction(cil.AssignNode(value, left))

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

        if node.type == SelfType().name:
            value = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(value, node.type))
            self.register_instruction(cil.AllocateNode(value, ret))
        elif node.type == "Int" or node.type == "Bool":
            self.register_instruction(cil.ArgNode(0))
        elif node.type == "String":
            data_node = [dn for dn in self.dotdata if dn.value == ""][0]
            vmsg = self.register_local(VariableInfo("msg", None))
            self.register_instruction(cil.LoadNode(vmsg, data_node))
            self.register_instruction(cil.ArgNode(vmsg))

        self.register_instruction(cil.StaticCallNode(self.init_name(node.type), ret))
        return ret

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

        ret = self.define_internal_local()
        self.register_instruction(cil.ArgNode(int(node.lex)))
        self.register_instruction(cil.StaticCallNode(self.init_name("Int"), ret))
        return ret

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

        self.current_type.get_attribute(node.lex)
        attr = self.register_local(VariableInfo(node.lex, None))
        self.register_instruction(cil.GetAttribNode(attr, node, node.lex))
        return attr

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
