from utils import visitor
import asts.types_ast as sem_ast  # Semantic generated ast
from asts.ccil_ast import *  # CCIL generated ast
from typing import OrderedDict, Set, Tuple, List, Dict
from code_gen.tools import *
from collections import OrderedDict

from code_gen.constants import *

# All operations that define an expression and where it is stored
VISITOR_RESULT = Tuple[List[OperationNode], StorageNode]
CLASS_VISITOR_RESULT = Tuple[Class, List[FunctionNode]]
METHOD_VISITOR_RESULT = FunctionNode
ATTR_VISITOR_RESULT = List[OperationNode]

DEFAULT_STR = Data("default_str", "")
ZERO = "zero"
EMPTY = "empty"

# TODO:
# See how typeof should work, a special kind of equality?
# Define abort nodes with a text:
# * Dispatch on a void class (Done)
# * Case expr is void
# * No pattern match in case (Done)
# * Division by zero (Done)
# * Substring out of range (Done)
# * Heap Overflow (don't know yet how to handle this)

# TEST:
# * Built in methods


# BOSS:
# Test there are no runtimes errors during generation
# Test that generation is correct


# CCIL stands for Cool Cows Intermediate Language ;)
class CCILGenerator:
    """
    Using the visitor pattern it goes through the semantics ast and produce a ccil ast
    """

    def __init__(self) -> None:
        self.program_types: Dict[str, Class]
        self.program_codes: List[FunctionNode]
        # To keep track of how many times a certain expression has been evaluated
        self.time_record: Dict[str, int] = dict()
        # Track all constant values. Only strings for now
        self.data: List[Data]
        # Notify about possible but senseless combination of expressions
        self.warnings: List[str] = []

        # To keep track of the current class being analysed
        self.current_type: str
        # Locals defined for each function
        self.locals: Dict[str, str]

        # Link between cool names and their ccil name.
        # It is used as scope to know which cool name it is
        # referring when there are equals
        self.ccil_cool_names: Scope

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(sem_ast.ProgramNode)
    def visit(self, node: sem_ast.ProgramNode) -> None:
        self.data = [DEFAULT_STR]
        self.reset_locals()

        [obj, io, str, int, bool], builtin_methods = self.define_built_ins()
        self.program_types = OrderedDict(
            {OBJECT: obj, IO: io, STRING: str, INT: int, BOOL: bool}
        )
        self.program_codes: List[FunctionNode] = builtin_methods

        for builtin_name in [OBJECT, IO, STRING, INT, BOOL]:
            self.add_data(f"{CLASS}{builtin_name}", builtin_name)

        for type in node.declarations:
            classx, class_code = self.visit(type)
            self.program_types[classx.id] = classx
            self.program_codes += class_code

        program_types = update_self_type_attr(self.program_types.values())

        return CCILProgram(
            self.define_entry_func(),
            program_types,
            self.program_codes,
            self.data,
        )

    @visitor.when(sem_ast.ClassDeclarationNode)
    def visit(self, node: sem_ast.ClassDeclarationNode) -> CLASS_VISITOR_RESULT:
        self.reset_scope()
        self.current_type = node.id
        self.add_data(f"{CLASS}{node.id}", node.id)

        attributes: List[Attribute] = self.get_inherited_attributes(node)
        methods: List[Method] = []

        attr_nodes = []
        func_nodes = []
        for feature in node.features:
            if isinstance(feature, sem_ast.AttrDeclarationNode):
                attributes.append(
                    Attribute(ATTR + feature.id, feature.type.name, feature.id)
                )
                attr_nodes.append(feature)
            else:
                func_nodes.append(feature)

        # Create init func using attributes and their expressions
        init_func = self.create_class_init_func(node, attr_nodes)

        self.reset_scope()
        # Explore all functions
        self.ccil_cool_names.add_new_names(*[(a.cool_id, a.id) for a in attributes])
        class_code: List[FunctionNode] = []
        for func in func_nodes:
            f = self.visit(func)
            class_code.append(f)
            methods.append(Method(func.id, f))

        methods, inherited_methods = self.get_inherited_methods(node, methods)

        return (
            Class(
                node.id,
                attributes,
                inherited_methods + methods,
                init_func,
            ),
            class_code,
        )

    @visitor.when(sem_ast.AttrDeclarationNode)
    def visit(self, node: sem_ast.AttrDeclarationNode) -> ATTR_VISITOR_RESULT:
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        attr_id = ATTR + node.id
        self.ccil_cool_names.add_new_name_pair(node.id, attr_id)

        if node.expr is None:
            if node.type.name != STRING:
                value_0 = IdNode(ZERO)
            else:
                value_0 = IdNode(EMPTY)
            set_attr = SetAttrOpNode("self", attr_id, value_0, self.current_type)
            return [set_attr]

        (expr_op, expr_fval) = self.visit(node.expr)

        set_attr = SetAttrOpNode("self", attr_id, expr_fval.id, self.current_type)

        self.ccil_cool_names = self.ccil_cool_names.get_parent
        return [*expr_op, set_attr]

    @visitor.when(sem_ast.MethodDeclarationNode)
    def visit(self, node: sem_ast.MethodDeclarationNode) -> METHOD_VISITOR_RESULT:
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        params: List[Parameter] = [Parameter("self", self.current_type)]
        self.ccil_cool_names.add_new_name_pair("self", "self")

        for param in node.params:
            new_param_id = PARAM + param.id
            params.append(Parameter(new_param_id, param.type.name))
            self.ccil_cool_names.add_new_name_pair(param.id, new_param_id)

        self.reset_locals()
        (operations, fval) = self.visit(node.body)

        self.ccil_cool_names = self.ccil_cool_names.get_parent
        return FunctionNode(
            f"f_{node.id}_{self.current_type}",
            params,
            self.dump_locals(),
            operations,
            fval.id,
        )

    @visitor.when(sem_ast.BlocksNode)
    def visit(self, node: sem_ast.BlocksNode) -> VISITOR_RESULT:
        times = self.times(node)

        operations: List[OperationNode] = []
        fvalues: List[StorageNode] = []
        for expr in node.expr_list:
            (expr_ops, expr_fval) = self.visit(expr)
            operations += expr_ops
            fvalues.append(expr_fval)

        block_val = fvalues[-1]
        fval_id = f"block_{times}"

        fval = self.create_assignation(fval_id, node.type.name, block_val.id)
        operations.append(fval)

        return (operations, fval)

    @visitor.when(sem_ast.LetNode)
    def visit(self, node: sem_ast.LetNode) -> VISITOR_RESULT:
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        operations: List[OperationNode] = self.init_default_values()
        fvalues: List[StorageNode] = []

        for var in node.var_decl_list:
            (var_ops, var_fv) = self.visit(var)
            operations += var_ops
            fvalues.append(var_fv)

        (in_ops, in_fval) = self.visit(node.in_expr)
        operations += in_ops

        self.ccil_cool_names = self.ccil_cool_names.get_parent
        return (operations, in_fval)

    @visitor.when(sem_ast.VarDeclarationNode)
    def visit(self, node: sem_ast.VarDeclarationNode) -> VISITOR_RESULT:
        times = self.times(node, node.id)

        fvalue_id: str = f"{LET}{times}{node.id}"
        self.ccil_cool_names.add_new_name_pair(node.id, fvalue_id)

        if node.expr is None:
            if node.type.name != STRING:
                value_0 = IdNode(ZERO)
            else:
                value_0 = IdNode(EMPTY)
            fval = self.create_assignation(fvalue_id, node.type.name, value_0.value)
            return [fval], fval

        (expr_ops, expr_fv) = self.visit(node.expr)

        self.update_locals(expr_fv.id, fvalue_id)
        expr_fv.id = fvalue_id

        return (expr_ops, expr_fv)

    @visitor.when(sem_ast.AssignNode)
    def visit(self, node: sem_ast.AssignNode) -> VISITOR_RESULT:
        (expr_ops, expr_fval) = self.visit(node.expr)

        ccil_id, is_attr = self.ccil_cool_names.get_value_position(node.id)

        if is_attr:
            # Assignation occurring to an attribute Go update the attribute
            set_attr = SetAttrOpNode(
                "self", ccil_id, extract_id(expr_fval), self.current_type
            )
            return [*expr_ops, set_attr], expr_fval

        self.update_locals(expr_fval.id, ccil_id)
        expr_fval.id = ccil_id
        return (expr_ops, expr_fval)

    @visitor.when(sem_ast.ConditionalNode)
    def visit(self, node: sem_ast.ConditionalNode) -> VISITOR_RESULT:
        times = self.times(node)

        (if_ops, if_fval) = self.visit(node.condition)
        (then_ops, then_fval) = self.visit(node.then_body)
        (else_ops, else_fval) = self.visit(node.else_body)

        # translating condition to ccil
        label_id = f"ifElse_{times}"
        else_label = LabelNode(label_id)
        if_false = IfFalseNode(extract_id(if_fval), else_label)

        endif_label = LabelNode(f"endIf_{times}")
        goto_endif = GoToNode(endif_label)

        # Setting the final operation which will simbolize the return value of this expr
        pre_fvalue_id = f"if_{times}_pre_fv"
        self.update_locals(then_fval.id, pre_fvalue_id)
        self.update_locals(else_fval.id, pre_fvalue_id)
        then_fval.id = else_fval.id = pre_fvalue_id

        fvalue_id = f"if_{times}_fv"
        fvalue = self.create_assignation(fvalue_id, node.type.name, pre_fvalue_id)

        return (
            [
                *if_ops,
                if_false,
                *then_ops,
                goto_endif,
                else_label,
                *else_ops,
                endif_label,
                fvalue,
            ],
            fvalue,
        )

    @visitor.when(sem_ast.CaseNode)
    def visit(self, node: sem_ast.CaseNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Visiting case expression
        (case_expr_ops, case_expr_fv) = self.visit(node.case_expr)

        # Handling case expression is not void
        void_expr_error_ops = (
            self.throw_runtime_error(
                f"case_{times}_void_expr_error",
                f"RuntimeError: Case expression in {node.line}, {node.col} is void",
            )
            if node.case_expr.type.name not in {STRING, INT, BOOL}
            else []
        )

        # Storing the type of the resulting case expression
        expr_type = self.create_type_name(
            f"case_{times}_expr_type", case_expr_fv.id, node.case_expr.type.name
        )

        # Final label where all branch must jump to
        final_label = LabelNode(f"case_{times}_end")
        final_goto = GoToNode(final_label)

        # All branch must end in a var named like this
        pre_fvalue_id = f"case_{times}_pre_fv"
        # Holds strings for comparsion
        type_name_holder = self.add_local(f"case_{times}_type_name_holder", STRING)
        equality_holder = self.add_local(f"case_{times}_eq_holder", INT)

        pattern_match_ops = self.init_default_values()

        branch_ops = []
        visited_types = set()  # To optimize and reduce redundant calling
        for (i, option) in enumerate(node.options):
            # Initializing the branch var
            branch_var = self.create_assignation(
                f"case_{times}_option_{i}", option.branch_type.name, case_expr_fv.id
            )

            # Label that means the start of this branch logic
            branch_label = LabelNode(f"case_{times}_branch_{i}")

            # Compare expr type with node branch type and all of
            # it's successors
            branch_selection_ops = []
            if option.successors[0] != OBJECT:
                for type_names in option.successors:
                    if type_names in visited_types:
                        continue
                    visited_types.add(type_names)

                    load_class_name = StorageNode(
                        type_name_holder.id, LoadOpNode(f"{CLASS}{type_names}")
                    )
                    select_branch = StorageNode(
                        equality_holder.id,
                        EqualStrNode(
                            extract_id(expr_type), extract_id(load_class_name)
                        ),
                    )
                    # Conditional jump to the right branch label
                    if_op = IfNode(extract_id(select_branch), branch_label)
                    branch_selection_ops += [load_class_name, select_branch, if_op]
            else:
                branch_selection_ops = [GoToNode(branch_label)]

            # Storing logic to jump to branch logic if this branch is selected
            pattern_match_ops += [
                branch_var,
                *branch_selection_ops,
            ]

            # Translating the branch logic
            (expr_ops, expr_fval) = self.visit(option.expr)
            # Renaming the last stored value of the expression
            self.update_locals(expr_fval.id, pre_fvalue_id)
            expr_fval.id = pre_fvalue_id
            # Translating to ccil of branch logic
            branch_ops += [branch_label, *expr_ops, final_goto]

        self.locals[pre_fvalue_id] = node.type.name

        # Error handling when there is not pattern match
        pattern_match_error_ops = self.throw_runtime_error(
            f"case_{times}_pattern_match_fail",
            f"RuntimeError: Pattern match failure in {node.line}, {node.col}",
        )

        # Merging all expression operations in correct order
        # and saving all to final value
        fval_id = f"case_{times}_fv"
        fval = self.create_assignation(fval_id, node.type.name, pre_fvalue_id)
        operations = [
            *case_expr_ops,
            *void_expr_error_ops,
            expr_type,
            *pattern_match_ops,
            *pattern_match_error_ops,
            *branch_ops,
            final_label,
            fval,
        ]
        return (operations, fval)

    @visitor.when(sem_ast.LoopNode)
    def visit(self, node: sem_ast.LoopNode) -> VISITOR_RESULT:
        times = self.times(node)

        (cond_ops, cond_fval) = self.visit(node.condition)
        (body_ops, _) = self.visit(node.body)

        # Setting control flow labels
        loop_label_id = f"loop_{times}"
        loop_label = LabelNode(loop_label_id)
        end_loop_label_id = f"endLoop_{times}"
        end_loop_label = LabelNode(end_loop_label_id)

        # Setting control flow instructions ifFalse & GoTo
        if_false = IfFalseNode(cond_fval, end_loop_label)
        go_to = GoToNode(loop_label)

        fval = self.create_uninitialized_storage(f"loop_{times}_fv", VOID)
        # Loop Nodes have void return type, how to express it??
        return (
            [*cond_ops, loop_label, if_false, *body_ops, go_to, end_loop_label, fval],
            fval,
        )

    @visitor.when(sem_ast.ArithmeticNode)
    def visit(self, node: sem_ast.ArithmeticNode) -> VISITOR_RESULT:
        times = self.times(node)
        (left_ops, left_fval) = self.visit(node.left)
        (right_ops, right_fval) = self.visit(node.right)

        left_id = extract_id(left_fval)
        right_id = extract_id(right_fval)

        fval_id: str
        op: ArithmeticOpNode

        # Arithmetic Binary Nodes
        extra_ops: List[OperationNode] = []
        node_type = type(node)
        if node_type == sem_ast.PlusNode:
            op = SumOpNode(left_id, right_id)
            fval_id = f"sum_{times}"
        elif node_type == sem_ast.MinusNode:
            op = MinusOpNode(left_id, right_id)
            fval_id = f"minus_{times}"
        elif node_type == sem_ast.StarNode:
            op = MultOpNode(left_id, right_id)
            fval_id = f"mult_{times}"
        elif node_type == sem_ast.DivNode:
            op = DivOpNode(left_id, right_id)
            fval_id = f"div_{times}"
            # Generating divison by zero runtime error
            ok_label = LabelNode(f"ok_div_{times}")
            right_id_is_zero = self.create_equality(
                f"check_right_zero_{times}", left_id, IntNode("0")
            )
            if_id_is_not_zero = IfFalseNode(extract_id(right_id_is_zero), ok_label)
            error_msg = self.add_data(
                f"error_msg_div_zero_{times}",
                f"RuntimeError: Zero division detected on {node.line}, {node.col}.",
            )
            error_var = self.create_string_load_data(f"error_var_{times}", error_msg.id)
            extra_ops = [
                right_id_is_zero,
                if_id_is_not_zero,
                error_var,
                *self.notifiy_and_abort(error_var.id),
                ok_label,
            ]

        else:
            raise Exception(
                f"Pattern match failure visiting arithmetic expression"
                f" with {type(node).__name__}"
            )

        fval = self.create_storage(fval_id, node.type.name, op)
        return ([*left_ops, *right_ops, *extra_ops, fval], fval)

    @visitor.when(sem_ast.ComparerNode)
    def visit(self, node: sem_ast.ComparerNode) -> VISITOR_RESULT:
        times = self.times(node)

        (left_ops, left_fval) = self.visit(node.left)
        (right_ops, right_fval) = self.visit(node.right)

        left_id = extract_id(left_fval)
        right_id = extract_id(right_fval)

        fval_id: str
        op: BinaryOpNode
        node_type = type(node)
        # Boolean Binary Nodes
        if node_type == sem_ast.EqualsNode:
            op = (
                EqualIntNode(left_id, right_id)
                if node.left.type.name != STRING
                else EqualStrNode(left_id, right_id)
            )
            fval_id = f"eq_{times}"
        elif node_type == sem_ast.LessNode:
            op = LessOpNode(left_id, right_id)
            fval_id = f"le_{times}"
        elif node_type == sem_ast.LessOrEqualNode:
            op = LessOrEqualOpNode(left_id, right_id)
            fval_id = f"leq_{times}"
        else:
            raise Exception(
                f"Pattern match failure visiting binary expression with {type(node).__name__}"
            )

        fval = self.create_storage(fval_id, BOOL, op)
        return ([*left_ops, *right_ops, fval], fval)

    @visitor.when(sem_ast.UnaryNode)
    def visit(self, node: sem_ast.UnaryNode) -> VISITOR_RESULT:
        times = self.times(node)

        (expr_op, expr_fval) = self.visit(node.expr)
        expr_id = extract_id(expr_fval)

        fval_id: str
        op: UnaryOpNode

        node_type = type(node)
        if node_type == sem_ast.IsVoidNode:
            fval_id = f"is_void_fv_{times}"
            if node.expr.type.name in {BOOL, INT, STRING}:
                self.add_warning(
                    f"Redundant isVoid expression in {node.line}, {node.col}."
                    f" Type {node.expr.type.name} will always evaluate to false"
                )
                op = BoolNode("0")
            else:
                op = EqualIntNode(IdNode(fval_id), IntNode("0"))
        elif node_type == sem_ast.NotNode:
            fval_id = f"not_{times}"
            op = NotOpNode(expr_id)
        elif node_type == sem_ast.ComplementNode:
            fval_id = f"neg_{times}"
            op = NegOpNode(expr_id)
        else:
            raise Exception("Pattern match failure while visiting unary expression")

        fval = self.create_storage(fval_id, node.type.name, op)
        return [*expr_op, fval], fval

    @visitor.when(sem_ast.MethodCallNode)
    def visit(self, node: sem_ast.MethodCallNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Translate all call arguments to ccil
        # Name all fvalues as ARG <result>
        args_ops: List[OperationNode] = []
        args: List[IdNode] = []
        for arg_expr in node.args:
            (arg_op, arg_fval) = self.visit(arg_expr)
            args_ops += arg_op
            args += [extract_id(arg_fval)]

        # id(arg1, arg2, ..., argn)
        if node.expr is None:
            fval_id = f"vcall_{times}"
            call = self.create_vcall(
                fval_id,
                node.type.name,
                node.id,
                node.caller_type.name,
                [IdNode("self"), *args],
            )
            return [*args_ops, call], call

        (expr_ops, expr_fval) = self.visit(node.expr)

        if node.caller_type.name == STRING:
            fval_id = f"call_str_{times}"
            call = self.create_call(
                fval_id, node.type.name, node.id, STRING, [extract_id(expr_fval), *args]
            )
            return [*expr_ops, *args_ops, call], call

        # Runtime error depending if expr is void or not
        error_ops = []
        expr_fval_is_void = self.create_equality(
            f"expr_is_void_{times}", extract_id(expr_fval), IntNode("0")
        )
        ok_label = LabelNode(f"expr_is_not_void_{times}")
        if_is_not_void = IfFalseNode(extract_id(expr_fval_is_void), ok_label)
        error_msg = self.add_data(
            f"caller_void_err_{times}",
            f"RuntimeError: expresion in {node.line}, {node.col} is void",
        )
        load_err = self.create_string_load_data(
            f"caller_void_err_var_{times}", error_msg.id
        )
        print_and_abort = self.notifiy_and_abort(load_err.id)
        error_ops = [
            expr_fval_is_void,
            if_is_not_void,
            load_err,
            *print_and_abort,
            ok_label,
        ]

        # <expr>@type.id(arg1, arg2, ..., argn)
        if node.at_type is not None:
            fval_id = f"call_{times}"
            call = self.create_call(
                fval_id,
                node.type.name,
                make_unique_func_id(node.id, node.caller_type.name),
                node.caller_type.name,
                [extract_id(expr_fval), *args],
            )
            return [*expr_ops, *error_ops, *args_ops, call], call

        # <expr>.id(arg1, arg2, ..., argn)
        fval_id = f"vcall_{times}"
        call = self.create_vcall(
            fval_id,
            node.type.name,
            node.id,
            node.caller_type.name,
            [extract_id(expr_fval), *args],
        )

        return [*expr_ops, *error_ops, *args_ops, call], call

    @visitor.when(sem_ast.InstantiateNode)
    def visit(self, node: sem_ast.InstantiateNode) -> VISITOR_RESULT:
        times = self.times(node)

        fvalue_id = f"new_type_{times}"
        fvalue = self.create_new_type(fvalue_id, node.type.name)

        return [fvalue], fvalue

    @visitor.when(sem_ast.VariableNode)
    def visit(self, node: sem_ast.VariableNode) -> VISITOR_RESULT:
        times = self.times(node)

        id_id = f"id_{times}"
        ccil_id, is_attr = self.ccil_cool_names.get_value_position(node.value)

        if is_attr:
            get_attr = self.create_attr_extraction(
                id_id, node.type.name, "self", ccil_id, self.current_type
            )
            return [get_attr], get_attr

        fval = self.create_assignation(id_id, node.type.name, ccil_id)
        return [fval], fval

    @visitor.when(sem_ast.StringNode)
    def visit(self, node: sem_ast.StringNode) -> VISITOR_RESULT:
        times = self.times(node)

        data_id = f"dataString_{times}"
        self.data.append(Data(data_id, node.value))

        load_id = f"load_str_{times}"
        load_str = self.create_string_load_data(load_id, data_id)
        return [load_str], load_str

    @visitor.when(sem_ast.IntNode)
    def visit(self, node: sem_ast.IntNode) -> VISITOR_RESULT:
        times = self.times(node)

        int_id = f"int_{times}"
        int_node = self.create_int(int_id, node.value)

        return [int_node], int_node

    @visitor.when(sem_ast.BooleanNode)
    def visit(self, node: sem_ast.BooleanNode) -> VISITOR_RESULT:
        times = self.times(node)

        bool_id = f"bool_{times}"
        value = "0" if node.value == "false" else "1"

        bool_node = self.create_bool(bool_id, value)
        return [bool_node], bool_node

    def create_class_init_func(
        self,
        node: sem_ast.ClassDeclarationNode,
        attr_nodes: List[sem_ast.AttrDeclarationNode],
    ):
        self.reset_locals()
        self.reset_scope()

        init_params = self.init_func_params(node.id)
        # self.ccil_cool_names.add_new_name_pair("self", node.id)

        # First operation, initalizing parent attributes
        init_parent = self.create_call(
            f"call_parent_{node.parent}",
            INT,
            f"init_{node.parent}",
            node.parent,
            [IdNode("self")],
        )

        # Execute all attributes operation and set them
        init_attr_ops: List[OperationNode] = [init_parent, *self.init_default_values()]
        for attr in attr_nodes:
            attr_ops = self.visit(attr)
            init_attr_ops += attr_ops

        dummy_return = self.create_storage(f"init_type_{node.id}_ret", INT, IntNode(0))
        init_attr_ops.append(dummy_return)

        # return init function
        return FunctionNode(
            f"init_{node.id}",
            init_params,
            self.dump_locals(),
            init_attr_ops,
            dummy_return.id,
        )

    def define_built_ins(self):
        # Defining Object class methods
        self.reset_scope()
        params = self.init_func_params(OBJECT)
        abort_msg = self.add_data("abort_msg", "RuntimeError: Execution aborted")
        load = self.create_string_load_data("abort_temp", abort_msg.id)
        [print, abort] = self.notifiy_and_abort(load.id)
        abort_func = FunctionNode(
            "abort", params, self.dump_locals(), [load, print, abort], "self"
        )
        params = self.init_func_params(OBJECT)
        get_name = self.create_type_name("get_name", "self", OBJECT)
        type_name_func = FunctionNode(
            "type_name", params, self.dump_locals(), [get_name], get_name.id
        )
        params = self.init_func_params(OBJECT)
        new_instance = self.create_new_type("shallow_copy", SELFTYPE)
        update_instance = ShallowCopyOpNode(new_instance.id, "self")
        copy_func = FunctionNode(
            "copy",
            params,
            self.dump_locals(),
            [new_instance, update_instance],
            new_instance.id,
        )
        object_class = Class(
            OBJECT,
            [],
            [
                Method("abort", abort_func),
                Method("type_name", type_name_func),
                Method("copy", copy_func),
            ],
            self.define_builtin_init_func(OBJECT),
        )

        # Defining IO class methods
        self.reset_scope()
        params = self.init_func_params(IO)
        str_input = Parameter("x", STRING)
        params.append(str_input)
        print = PrintStrNode(str_input.id)
        out_string_func = FunctionNode(
            "out_string", params, self.dump_locals(), [print], "self"
        )
        params = self.init_func_params(IO)
        int_input = Parameter("x", INT)
        params.append(int_input)
        print = PrintIntNode(int_input.id)
        out_int_func = FunctionNode(
            "out_int", params, self.dump_locals(), [print], "self"
        )
        params = self.init_func_params(IO)
        read = self.create_read_str("read_str")
        in_string_func = FunctionNode(
            "in_string", params, self.dump_locals(), [read], read.id
        )
        params = self.init_func_params(IO)
        read = self.create_read_int("read_int")
        in_int_func = FunctionNode(
            "in_int", params, self.dump_locals(), [read], read.id
        )
        io_class = Class(
            IO,
            [],
            [
                *object_class.methods,
                Method("out_string", out_string_func),
                Method("out_int", out_int_func),
                Method("in_string", in_string_func),
                Method("in_int", in_int_func),
            ],
            self.define_builtin_init_func(IO),
        )

        # Defining substring class methods
        self.reset_scope()
        params = self.init_func_params(STRING)
        length = self.create_length("lenght_var", "self")
        lenght_func = FunctionNode(
            "length", params, self.dump_locals(), [length], length.id
        )
        self.reset_locals()
        params = self.init_func_params(STRING)
        input_s = Parameter("s", STRING)
        params.append(input_s)
        concat = self.create_storage(
            "concat_var", STRING, ConcatOpNode("self", input_s.id)
        )
        concat_func = FunctionNode(
            "concat", params, self.dump_locals(), [concat], concat.id
        )
        self.reset_locals()
        params = self.init_func_params(STRING)
        start_index = Parameter("s", INT)
        take = Parameter("l", INT)
        params += [start_index, take]
        length = self.create_length("length_var", "self")
        max_take = self.create_storage(
            "max_take", INT, SumOpNode(IdNode(start_index.id), IdNode(take.id))
        )
        upper_bound = self.create_storage(
            "upper_bound", BOOL, LessOpNode(extract_id(length), extract_id(max_take))
        )
        lesser_bound = self.create_storage(
            "lesser_bound", BOOL, LessOpNode(IdNode(start_index.id), IntNode("0"))
        )
        error_label = LabelNode("substring_error")
        ok_label = LabelNode("substring_success")
        if_upper_bound = IfNode(extract_id(upper_bound), error_label)
        if_lesser_bound = IfNode(extract_id(lesser_bound), error_label)
        error_msg = self.add_data(
            "substr_error", "RuntimeError: Index out of range exception"
        )
        error_var = self.create_string_load_data("substr_error_var", error_msg.id)
        print_and_abort = self.notifiy_and_abort(error_var.id)
        substr = self.create_storage(
            "substr_var",
            STRING,
            SubstringOpNode(IdNode(start_index.id), IdNode(take.id), IdNode("self")),
        )
        goto_ok = GoToNode(ok_label)
        operations = [
            length,
            max_take,
            upper_bound,
            lesser_bound,
            if_upper_bound,
            if_lesser_bound,
            substr,
            goto_ok,
            error_label,
            error_var,
            *print_and_abort,
            ok_label,
        ]
        substr_func = FunctionNode(
            "substr", params, self.dump_locals(), operations, substr.id
        )
        attributes = [Attribute("value", STRING, "value")]
        string_class = Class(
            STRING,
            attributes,
            [
                *object_class.methods,
                Method("length", lenght_func),
                Method("concat", concat_func),
                Method("substr", substr_func),
            ],
            self.define_builtin_init_func(STRING, attributes),
        )

        attributes = [Attribute("value", INT, "value")]
        int_class = Class(
            INT,
            attributes,
            object_class.methods,
            self.define_builtin_init_func(INT, attributes),
        )

        attributes = [Attribute("value", BOOL, "value")]
        bool_class = Class(
            BOOL,
            attributes,
            object_class.methods,
            self.define_builtin_init_func(BOOL, attributes),
        )

        return [object_class, io_class, string_class, int_class, bool_class], [
            abort_func,
            type_name_func,
            copy_func,
            out_string_func,
            out_int_func,
            in_string_func,
            in_int_func,
            lenght_func,
            concat_func,
            substr_func,
        ]

    def init_func_params(self, typex: str):
        return [Parameter("self", typex)]

    def create_assignation(self, idx: str, type_idx: str, target: str):
        self.add_local(idx, type_idx)
        return StorageNode(idx, IdNode(target))

    def create_uninitialized_storage(self, idx: str, type_idx: str):
        self.add_local(idx, type_idx)
        return StorageNode(idx, ZERO if type_idx != STRING else EMPTY)

    def create_storage(self, idx: str, type_idx: str, op: ReturnOpNode):
        self.add_local(idx, type_idx)
        return StorageNode(idx, op)

    def create_attr_extraction(
        self, idx: str, type_idx: str, from_idx: str, attr_idx: str, from_type_idx: str
    ):
        self.add_local(idx, type_idx)
        return StorageNode(idx, GetAttrOpNode(from_type_idx, from_idx, attr_idx))

    def create_new_type(self, idx: str, type_idx: str):
        self.add_local(idx, type_idx)
        return StorageNode(idx, NewOpNode(type_idx))

    def create_call(
        self,
        storage_idx: str,
        type_idx: str,
        method_idx: str,
        method_type_idx: str,
        args: List[StorageNode],
    ):
        self.add_local(storage_idx, type_idx)
        return StorageNode(storage_idx, CallOpNode(method_idx, method_type_idx, args))

    def create_vcall(
        self,
        storage_idx: str,
        type_idx: str,
        method_idx: str,
        method_type_idx: str,
        args: List[StorageNode],
    ):
        self.add_local(storage_idx, type_idx)
        return StorageNode(storage_idx, VCallOpNode(method_idx, method_type_idx, args))

    def create_type_of(self, idx: str, target: AtomOpNode):
        self.add_local(idx, ADDRESS)
        return StorageNode(idx, GetTypeOpNode(target))

    def create_equality(
        self, idx, left: AtomOpNode, right: AtomOpNode, string: bool = False
    ):
        self.add_local(idx, BOOL)
        op = EqualStrNode(left, right) if string else EqualIntNode(left, right)
        return StorageNode(idx, op)

    def notifiy_and_abort(self, target: str) -> List[OperationNode]:
        print = PrintStrNode(target)
        abort = Abort()
        return [print, abort]

    def create_string_load_data(self, idx: str, target: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, LoadOpNode(target))

    def create_int(self, idx: str, value: str):
        self.add_local(idx, INT)
        return StorageNode(idx, IntNode(value))

    def create_bool(self, idx: str, value: str):
        self.add_local(idx, BOOL)
        return StorageNode(idx, BoolNode(value))

    def create_int_to_str(self, idx: str, target: str):
        self.add_local(str, STRING)
        return StorageNode(idx, StrOpNode(target))

    def create_read_str(self, idx: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, ReadStrNode())

    def create_read_int(self, idx: str):
        self.add_local(idx, INT)
        return StorageNode(idx, ReadIntNode())

    def create_type_name(self, idx: str, target: str, static_type: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, CurrentTypeNameNode(target, static_type))

    def create_length(self, idx: str, target: str):
        self.add_local(idx, INT)
        return StorageNode(idx, LengthOpNode(target))

    def init_default_values(self):
        if not ZERO in self.locals and not EMPTY in self.locals:
            return [
                self.create_storage(ZERO, INT, IntNode("0")),
                self.create_string_load_data(EMPTY, DEFAULT_STR.id),
            ]
        return []

    def define_entry_func(self):
        self.reset_locals()
        program = self.create_new_type("program", "Main")
        execute = self.create_call(
            "execute_program",
            INT,
            make_unique_func_id("main", "Main"),
            INT,
            [IdNode(program.id)],
        )
        return FunctionNode(
            "main", [], self.dump_locals(), [program, execute], execute.id
        )

    def define_builtin_init_func(
        self, class_name: str, attributes: List[Attribute] = []
    ):
        self.reset_locals()
        params = self.init_func_params(class_name)
        dummy_return = self.create_storage(
            f"init_type_{class_name}_ret", INT, IntNode(0)
        )

        set_default_ops: List[OperationNode] = self.init_default_values()
        string_default = int_default = False
        for attr in attributes:
            if attr.type == STRING:
                value = IdNode(EMPTY)
                string_default = True
            else:
                value = IdNode(ZERO)
                int_default = True
            set_default_ops.append(SetAttrOpNode("self", attr.id, value, class_name))

        if not string_default:
            set_default_ops.pop(1)
            del self.locals[EMPTY]
        if not int_default:
            set_default_ops.pop(0)
            del self.locals[ZERO]

        return FunctionNode(
            f"init_{class_name}",
            params,
            self.dump_locals(),
            [*set_default_ops, dummy_return],
            dummy_return.id,
        )

    def times(self, node: sem_ast.Node, extra: str = ""):
        key: str = type(node).__name__ + extra
        try:
            self.time_record[key] += 1
        except KeyError:
            self.time_record[key] = 0
        return self.time_record[key]

    def add_data(self, idx: str, value: str):
        data = Data(idx, value)
        self.data.append(data)
        return data

    def update_locals(self, old_id: str, new_id: str):
        self.locals[new_id] = self.locals[old_id]
        del self.locals[old_id]

    def add_local(self, idx: str, typex: str):
        if idx in self.locals:
            raise Exception(f"Trying to insert {idx} again as local")
        self.locals[idx] = typex
        return Local(idx, typex)

    def reset_locals(self):
        """
        Apply at the beginning of every method to reset local vars
        """
        self.locals = dict()

    def dump_locals(self):
        var_locals = to_vars(self.locals, Local)
        self.locals = dict()
        return var_locals

    def reset_scope(self):
        self.ccil_cool_names = Scope()

    def add_warning(self, msg: str):
        self.add_warning(f"Warning: {msg}")

    def get_inherited_attributes(self, node: sem_ast.ClassDeclarationNode):
        return (
            [a for a in self.program_types[node.parent].attributes]
            if node.parent is not None
            else []
        )

    def get_inherited_methods(
        self, node: sem_ast.ClassDeclarationNode, defined_methods: List[Method]
    ):
        defined_methods: Dict[str, Method] = OrderedDict(
            (m.id, m) for m in defined_methods
        )

        new_defined_methods: List[Method] = []
        inherited_methods: List[Method] = []

        if node.parent is not None:
            parent_class: Class = self.program_types[node.parent]

            for method in parent_class.methods:
                try:
                    # Method override for an inherited method
                    override_method = defined_methods[method.id]
                except KeyError:
                    pass
                else:
                    method = Method(method.id, override_method.function)
                    del defined_methods[method.id]

                inherited_methods.append(method)

        new_defined_methods = list(defined_methods.values())
        return new_defined_methods, inherited_methods

    def throw_runtime_error(self, name: str, error_msg: str) -> List[OperationNode]:
        data = self.add_data(name + "_msg", error_msg)
        err_var = self.create_string_load_data(name + "_var", data.id)
        abort_ops = self.notifiy_and_abort(err_var.id)

        return [err_var, *abort_ops]

    def find_function_id(self, class_name: str, method_name: str):
        for method in self.program_types[class_name].methods:
            if method.id == method_name:
                return method.function.id
        raise Exception(f"Method: {method_name} was not found in {class_name}")


def make_unique_func_id(method_name: str, class_name: str):
    return f"f_{method_name}_{class_name}"


def to_vars(dict: Dict[str, str], const: BaseVar = BaseVar) -> List[BaseVar]:
    return list(map(lambda x: const(*x), dict.items()))


def update_self_type_attr(classes: List[Class]):
    new_classes: List[Class] = []
    for classx in classes:
        classx.attributes = list(
            map(
                lambda attr: attr
                if attr.type != SELFTYPE
                else Attribute(attr.id, classx.id),
                classx.attributes,
            )
        )
        new_classes.append(classx)
    return new_classes
