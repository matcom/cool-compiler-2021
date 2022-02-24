from utils import visitor
import asts.types_ast as sem_ast  # Semantic generated ast
from asts.ccil_ast import *  # CCIL generated ast
from typing import IO, Tuple, List, Dict
from code_gen.tools import *

from constants import *

# All operations that define an expression and where it is stored
VISITOR_RESULT = Tuple[List[OperationNode], StorageNode]
CLASS_VISITOR_RESULT = Tuple[Class, List[FunctionNode]]
METHOD_VISITOR_RESULT = FunctionNode

# TODO:
# Define abort nodes with a text:
# * Dispacth on a void class
# * No pattern match in case
# * Division by zero
# * Substring out of range (Done)
# * Heap Overflow (don't know yet how to handle this)


# BOSS:
# Test there are no runtimes errors
# Test that results are obtained as expected


# CCIL stands for Cool Cows Intermediate Language ;)
class CCILGenerator:
    """
    Using the visitor pattern it goes through the semantics ast and produce a ccil ast
    """

    def __init__(self) -> None:
        # To keep track of how many times a certain expression has been evaluated
        self.time_record: Dict[str, int] = dict()
        # Track all constant values. Only strings for now
        self.data: List[Data] = list()

        # To keep track of the current class being analysed
        self.current_type: str
        # Locals defined for each function
        self.locals: Dict[str, str]

        # Link between cool names and their ccil name.
        # It is used as scope to know which cool name it is
        # referring when there are equals
        self.ccil_cool_names: Scope

    @visitor.on("node")
    def visit(self, _):
        pass

    @visitor.when(sem_ast.ProgramNode)
    def visit(self, node: sem_ast.ProgramNode) -> None:
        program_types: List[Class] = list()
        program_codes: List[Method] = list()
        for type in node.declarations:
            classx, class_code = self.visit(type)
            program_types.append(classx)
            program_codes.append(class_code)

        return CCILProgram(program_types, program_codes, self.data)

    @visitor.when(sem_ast.ClassDeclarationNode)
    def visit(self, node: sem_ast.ClassDeclarationNode) -> CLASS_VISITOR_RESULT:
        self.current_type = node.id
        self.add_data(f"class_{node.id}", node.id)

        attr_nodes = []
        func_nodes = []
        for feature in node.features:
            if isinstance(feature, sem_ast.AttrDeclarationNode):
                attr_nodes.append(feature)
            else:
                func_nodes.append(feature)

        # Explore all attributes and join their operations in an initializer function
        self.reset_locals()
        self.reset_scope()
        attributes: List[Attribute] = list()
        init_attr_ops: List[OperationNode] = []
        for attr in attr_nodes:
            attributes.append(Attribute(ATTR + attr.id, attr.type.name))
            (attr_ops, _) = self.visit(attr)
            init_attr_ops += attr_ops

        # Return type is set as itself? Use selftype maybe?
        init_func = FunctionNode(
            node,
            f"init_{node.id}",
            [],
            to_vars(self.locals, Parameter),
            init_attr_ops,
            node.id,
        )

        # Explore all functions
        self.reset_scope()
        self.ccil_cool_names.add_new_names(
            (n.id, a.id) for (n, a) in zip(attr_nodes, attributes)
        )
        class_code: List[FunctionNode] = []
        methods: List[Method] = []
        for func in func_nodes:
            f = self.visit(func)
            class_code.append(f)
            methods.append(Method(func.id, f))

        return (Class(attributes, methods, init_func), class_code)

    @visitor.when(sem_ast.AttrDeclarationNode)
    def visit(self, node: sem_ast.AttrDeclarationNode) -> VISITOR_RESULT:
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        fval_id = ATTR + node.id
        self.ccil_cool_names.add_new_name_pair(node.id, fval_id)

        if node.expr is None:
            self.add_local(fval_id, node.type.name)
            return []

        (expr_op, expr_fval) = self.visit(node.expr)

        self.update_locals(expr_fval.id, fval_id)
        expr_fval.id = fval_id

        self.ccil_cool_names = self.ccil_cool_names.get_parent
        return (expr_op, expr_fval)

    @visitor.when(sem_ast.MethodDeclarationNode)
    def visit(self, node: sem_ast.MethodDeclarationNode) -> METHOD_VISITOR_RESULT:
        times = self.times(node)
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        params: List[Parameter] = [Parameter("self", self.current_type)]
        self.ccil_cool_names.add_new_name_pair("self", "self")
        for param in node.params:
            new_param_id = PARAM + param.id
            params.append(Parameter(new_param_id, param.type.name))
            self.ccil_cool_names.add_new_name_pair(param.id, new_param_id)

        self.locals = dict()
        (operations, fval_id) = self.visit(node.body)

        self.ccil_cool_names = self.ccil_cool_names.get_parent
        return FunctionNode(
            node,
            f"f_{times}",
            params,
            to_vars(self.locals, Parameter),
            operations,
            fval_id,
        )

    @visitor.when(sem_ast.BlocksNode)
    def visit(self, node: sem_ast.BlocksNode) -> VISITOR_RESULT:
        times = self.times(node)

        operations: List[OperationNode] = []
        fvalues: List[StorageNode] = []
        for expr in node.expr_list:
            (expr_ops, expr_fval) = self.visit(expr)
            operations += expr_ops
            fvalues += expr_fval

        block_val = fvalues[-1]
        fval_id = f"block_{times}"

        fval = self.create_assignation( fval_id, node.type.name, block_val.id)
        operations.append(fval)

        return (operations, fval)

    @visitor.when(sem_ast.LetNode)
    def visit(self, node: sem_ast.LetNode) -> VISITOR_RESULT:
        self.ccil_cool_names = self.ccil_cool_names.create_child()

        operations: List[OperationNode] = []
        fvalues: List[StorageNode] = []

        for var in node.var_decl_list:
            (var_ops, var_fv) = self.visit(var)
            operations += var_ops
            fvalues += var_fv

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
            self.add_local(fvalue_id, node.type.name)
            self.locals[fvalue_id] = node.type.name

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
            set_attr = SetAttrOpNode(node, "self", ccil_id, extract_id(node, expr_fval))
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
        else_label = LabelNode(node, label_id)
        if_false = IfFalseNode(node, if_fval, else_label)

        # Setting the final operation which will simbolize the return value of this expr
        pre_fvalue_id = f"if_{times}_pre_fv"
        self.update_locals(then_fval.id, pre_fvalue_id)
        self.update_locals(else_fval.id, pre_fvalue_id)
        then_fval.id = else_fval.id = pre_fvalue_id

        fvalue_id = f"if_{times}_fv"
        fvalue = self.create_assignation( fvalue_id, node.type.name, pre_fvalue_id)

        return (
            [*if_ops, if_false, *then_ops, else_label, *else_ops, fvalue],
            fvalue,
        )

    @visitor.when(sem_ast.CaseNode)
    def visit(self, node: sem_ast.CaseNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Visiting case expression
        (case_expr_ops, case_expr_fv) = self.visit(node.case_expr)

        # Storing the type of the resulting case expression
        type_of = self.create_type_of(
             f"case_{times}_typeOf", extract_id(node, case_expr_fv)
        )

        # Final label where all branch must jump to
        final_label_id = f"case_{times}_end"
        final_label = LabelNode(node, final_label_id)

        # Inconditional jump to final label
        final_goto = GoToNode(node, final_label)

        # All branch must end in a var named like this
        pre_fvalue_id = f"case_{times}_pre_fv"
        pattern_match_ops = []
        branch_ops = []
        for (i, option) in enumerate(node.options):
            # Initializing the branch var
            branch_var_id = f"case_{times}_option_{i}"
            branch_var = self.create_uninitialized_storage(
                branch_var_id, option.branch_type.name
            )

            # Initializing var which holds the branch var type
            branch_var_type_id = f"case_{times}_optionTypeOf_{i}"
            branch_var_type_of = self.create_type_of(
                branch_var_type_id, extract_id(node, branch_var)
            )

            # Initializng var which holds the comparison result between
            # the case expression type of and branch var type of
            select_branch_id = f"case_{times}_optionSelect_{i}"
            select_branch = self.create_equality(
                select_branch_id,
                extract_id(node, type_of),
                extract_id(node, branch_var_type_of),
            )

            # Label that means the start of this branch logic
            branch_label_id = f"case_{times}_branch_{i}"
            branch_label = LabelNode(option, branch_label_id)

            # Conditional jump to the right branch label
            if_op = IfNode(option, extract_id(option, branch_var_type_of), branch_label)
            # Storing logic to jump to branch logic if this branch is selected
            pattern_match_ops += [branch_var, branch_var_type_of, select_branch, if_op]

            # Translating the branch logic
            (expr_ops, expr_fval) = self.visit(option.expr)
            # Renaming the last stored value of the expression
            self.update_locals(expr_fval.id, pre_fvalue_id)
            expr_fval.id = pre_fvalue_id
            # Translating to ccil of branch logic
            branch_ops += [branch_label, *expr_ops, final_goto]

        # Merging all expression operations in correct order
        # and saving all to final value
        fval_id = f"case_{times}_fv"
        fval = self.create_assignation( fval_id, node.type.name, pre_fvalue_id)
        operations = [
            *case_expr_ops,
            type_of,
            *pattern_match_ops,
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
        loop_label = LabelNode(node, loop_label_id)
        end_loop_label_id = f"endLoop_{times}"
        end_loop_label = LabelNode(node, end_loop_label_id)

        # Setting control flow instructions ifFalse & GoTo
        if_false = IfFalseNode(node, cond_fval, end_loop_label)
        go_to = GoToNode(node, loop_label)

        fval = self.create_uninitialized_storage( f"loop_{times}_fv", VOID)
        # Loop Nodes have void return type, how to express it??
        return (
            [*cond_ops, loop_label, if_false, *body_ops, go_to, end_loop_label, fval],
            fval,
        )

    @visitor.when(sem_ast.BinaryNode)
    def visit(self, node: sem_ast.BinaryNode) -> VISITOR_RESULT:
        times = self.times(node)

        (left_ops, left_fval) = self.visit(node.left)
        (right_ops, right_fval) = self.visit(node.right)

        left_id = extract_id(node, left_fval)
        right_id = extract_id(node, right_fval)

        fval_id: str
        op: BinaryOpNode
        match node:
            # Arithmetic Binary Nodes
            case sem_ast.PlusNode:
                op = SumOpNode(left_id, right_id)
                fval_id = f"sum_{times}"
            case sem_ast.MinusNode:
                op = MinusOpNode(left_id, right_id)
                fval_id = f"minus_{times}"
            case sem_ast.StarNode:
                op = MultOpNode(left_id, right_id)
                fval_id = f"mult_{times}"
            case sem_ast.DivNode:
                op = DivOpNode(left_id, right_id)
                fval_id = f"div_{times}"
            # Boolean Binary Nodes
            case sem_ast.EqualsNode:
                op = EqualOpNode(left_id, right_id)
                fval_id = f"eq_{times}"
            case sem_ast.LessNode:
                op = LessOpNode(left_id, right_id)
                fval_id = f"le_{times}"
            case sem_ast.LessOrEqualNode:
                op = LessOrEqualOpNode(left_id, right_id)
                fval_id = f"leq_{times}"
            case _:
                raise Exception("Pattern match failure visiting binary expression")

        fval = self.create_storage( fval_id, node.type.id, op)
        return ([*left_ops, *right_ops, fval], fval)

    @visitor.when(sem_ast.UnaryNode)
    def visit(self, node: sem_ast.UnaryNode) -> VISITOR_RESULT:
        times = self.times(node)

        (expr_op, expr_fval) = self.visit(node.expr)
        expr_id = extract_id(node.expr, expr_fval)

        fval_id: str
        op: UnaryOpNode
        match node:
            case sem_ast.IsVoidNode:
                fval_id = f"isVoid_{times}"
                op = IsVoidOpNode(node, expr_id)
            case sem_ast.NotNode:
                fval_id = f"not_{times}"
                op = NotOpNode(node, expr_id)
            case sem_ast.ComplementNode:
                fval_id = f"neg_{times}"
                op = NegOpNode(node, expr_id)
            case _:
                raise Exception("Pattern match failure while visiting unary expression")

        fval = self.create_storage( fval_id, node.type.id, op)
        return [*expr_op, fval], fval

    @visitor.when(sem_ast.MethodCallNode)
    def visit(self, node: sem_ast.MethodCallNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Translate all call arguments to ccil
        # Name all fvalues as ARG <result>
        args_ops: List[OperationNode] = []
        args: List[StorageNode] = []
        for arg_expr in node.args:
            (arg_op, arg_fval) = self.visit(arg_expr)
            args_ops += arg_op
            args += [arg_fval]

        # id(arg1, arg2, ..., argn)
        if node.expr is None:
            fval_id = f"vcall_{times}"
            call = self.create_vcall(
                fval_id, node.type.id, node.id, node.caller_type.name
            )
            return [*args_ops, call], call

        (expr_ops, _) = self.visit(node.expr)

        # <expr>@type.id(arg1, arg2, ..., argn)
        if node.at_type is not None:
            fval_id = f"call_{times}"
            call = self.create_call(
                fval_id, node.type.name, node.id, node.caller_type.name
            )
            return [*args_ops, *expr_ops, call]

        # <expr>.id(arg1, arg2, ..., argn)
        fval_id = f"vcall_{times}"
        call = self.create_vcall( fval_id, node.type.id, node.id, node.caller_type)

        return [*args_ops, *expr_ops, call]

    @visitor.when(sem_ast.InstantiateNode)
    def visit(self, node: sem_ast.InstantiateNode) -> VISITOR_RESULT:
        times = self.times(node)

        fvalue_id = f"newType_{times}"
        fvalue = self.create_new_type( fvalue_id, node.type.name)

        return [fvalue], fvalue

    @visitor.when(sem_ast.VariableNode)
    def visit(self, node: sem_ast.VariableNode) -> VISITOR_RESULT:
        times = self.times(node)

        id_id = f"id_{times}"
        ccil_id, is_attr = self.ccil_cool_names.get_value_position(node.value)

        if is_attr:
            get_attr = self.create_attr_extraction(
                 id_id, node.type.name, "self", ccil_id
            )
            return [get_attr], get_attr

        fval = self.create_assignation( id_id, node.type.name, ccil_id)
        return [fval], fval

    @visitor.when(sem_ast.StringNode)
    def visit(self, node: sem_ast.StringNode) -> VISITOR_RESULT:
        times = self.times(node)

        data_id = f"dataString_{times}"
        self.data.append(Data(data_id, node.value))

        load_id = f"load_str_{times}"
        load_str = self.create_string_load_data( load_id, data_id)
        return [load_str], load_str

    @visitor.when(sem_ast.IntNode)
    def visit(self, node: sem_ast.IntNode) -> VISITOR_RESULT:
        times = self.times(node)

        int_id = f"int_{times}"
        int_node = self.create_int( int_id, node.value)

        return [int_node], int_node

    @visitor.when(sem_ast.BooleanNode)
    def visit(self, node: sem_ast.BooleanNode) -> VISITOR_RESULT:
        times = self.times(node)

        bool_id = f"bool_{times}"
        value = "0" if node.value == "False" else "1"

        bool_node = self.create_int( bool_id, value)
        return [bool_node], bool_node

    def times(self, node: sem_ast.Node, extra: str = ""):
        key: str = type(node).__name__ + extra
        try:
            self.time_record[key] += 1
        except KeyError:
            self.time_record[key] = 0
        return self.time_record[key]

    def create_call(
        self,
        storage_idx: str,
        type_idx: str,
        method_idx: str,
        args: List[StorageNode],
    ):
        self.add_local(storage_idx, type_idx)
        return StorageNode(storage_idx, CallOpNode(method_idx, args))

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

    def define_built_ins(self):
        # Defining Object class methods
        self.reset_scope()
        self.reset_locals()
        params = self.init_func_params(OBJECT)
        abort_msg = self.add_data("abort_msg", "Execution aborted")
        load = self.create_string_load_data("abort_temp", abort_msg.id)
        [print, abort] = self.notifiy_and_abort(load.id)
        abort_func = FunctionNode(
            "abort", params, to_vars(self.locals), [load, print, abort], "self"
        )
        self.reset_locals()
        params = self.init_func_params(OBJECT)
        get_name = self.create_current_type_name("get_name")
        type_name_func = FunctionNode(
            "type_name", params, self.locals, [get_name], get_name.id
        )
        self.reset_locals()
        params = self.init_func_params(OBJECT)
        new_instance = self.create_new_type("copy", SELFTYPE)
        copy_func = FunctionNode(
            "copy", params, to_vars(self.locals), [new_instance], new_instance.id
        )
        object_class = Class(
            OBJECT,
            [],
            [
                Method("abort", abort_func),
                Method("type_name", type_name_func),
                Method("copy", copy_func),
            ],
        )

        # Defining IO class methods
        self.reset_scope()
        self.reset_locals()
        params = self.init_func_params(IO)
        str_input = Parameter("x", STRING)
        params.append(str_input)
        print = PrintOpNode(str_input.id)
        out_string_func = FunctionNode(
            "out_string", params, to_vars(self.locals), [print], "self"
        )
        self.reset_locals()
        params = self.init_func_params(IO)
        int_input = Parameter("x", INT)
        params.append(int_input)
        int_to_str = self.create_int_to_str("int_to_str", int_input.id)
        print = PrintOpNode(int_to_str.id)
        out_int_func = FunctionNode(
            "out_int", params, to_vars(self.locals), [int_to_str, print], "self"
        )
        self.reset_locals()
        params = self.init_func_params(IO)
        read = self.create_read_str("read_str")
        in_string_func = FunctionNode("in_string", params, self.locals, [read], read.id)
        self.reset_locals()
        params = self.init_func_params(IO)
        read = self.create_read_int("read_int")
        in_int_func = FunctionNode("in_int", params, self.locals, [read], read.id)
        io_class = Class(
            IO,
            [],
            [
                Method("out_string", out_string_func),
                Method("out_int", out_int_func),
                Method("in_string", in_string_func),
                Method("in_int", in_int_func),
            ],
        )

        # Defining substring class methods
        self.reset_scope()
        self.reset_locals()
        params = self.init_func_params(STRING)
        length = self.create_length("lenght_var", "self")
        lenght_func = FunctionNode("length", params, self.locals, [length], length.id)
        self.reset_locals()
        params = self.init_func_params(STRING)
        input_s = Parameter("s", STRING)
        params.append(input_s)
        concat = self.create_storage(
            "concat_var", STRING, ConcatOpNode("self", input_s.id)
        )
        concat_func = FunctionNode("concat", params, self.locals, [concat], concat.id)
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
            "upper_bound", LessOpNode(extract_id(length), extract_id(max_take))
        )
        lesser_bound = self.create_storage(
            "lesser_bound", LessOpNode(IdNode(start_index.id), IntNode("0"))
        )
        error_label = LabelNode("substring_error")
        ok_label = LabelNode("substring_success")
        if_upper_bound = IfNode(extract_id(upper_bound), error_label)
        if_lesser_bound = IfNode(extract_id(lesser_bound), error_label)
        print_and_abort = self.notifiy_and_abort("Index out of range exception")
        substr = self.create_storage(
            "substr_var",
            STRING,
            SubstringOpNode(IdNode(start_index.id), IdNode(take.id)),
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
            *print_and_abort,
            ok_label,
        ]
        substr_func = FunctionNode("substr", params, self.locals, operations, substr.id)
        string_class = Class(
            STRING,
            [],
            [
                Method("length", lenght_func),
                Method("concat", concat_func),
                Method("substr", substr_func),
            ],
        )

        return [object_class, io_class, string_class], [
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
        return StorageNode(idx, VoidNode())

    def create_storage(self, idx: str, type_idx: str, op: ReturnOpNode):
        self.add_local(idx, type_idx)
        return StorageNode(idx, op)

    def create_attr_extraction(
        self, idx: str, type_idx: str, from_idx: str, attr_idx: str
    ):
        self.add_local(idx, type_idx)
        return StorageNode(idx, GetAttrOpNode(from_idx, attr_idx))

    def create_new_type(self, idx: str, type_idx: str):
        self.add_local(idx, type_idx)
        return StorageNode(idx, NewOpNode(type_idx))

    def create_type_of(self, idx: str, target: AtomOpNode):
        self.add_local(idx, ADDRESS)
        return StorageNode(idx, GetTypeOpNode(target))

    def create_equality(self, idx, left: AtomOpNode, right: AtomOpNode):
        self.add_local(idx, BOOL)
        return StorageNode(idx, EqualOpNode(left, right))

    def notifiy_and_abort(self, target: str):
        print = PrintOpNode(target)
        abort = Abort()
        return [print, abort]

    def create_string_load_data(self, idx: str, target: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, LoadOpNode(target))

    def create_int(self, idx: str, value: str):
        self.add_local(idx, INT)
        return StorageNode(idx, IntNode(value))

    def create_int_to_str(self, idx: str, target: str):
        self.add_local(str, STRING)
        return StorageNode(idx, StrOpNode(target))

    def create_read_str(self, idx: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, ReadStrNode())

    def create_read_int(self, idx: str):
        self.add_local(idx, INT)
        return StorageNode(idx, ReadIntNode())

    def create_current_type_name(self, idx: str):
        self.add_local(idx, STRING)
        return StorageNode(idx, CurrentTypeNameNode())

    def create_length(self, idx: str, target: str):
        self.add_local(idx, INT)
        return StorageNode(idx, LengthOpNode(target))

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
        self.defined_vars.add(idx)

    def reset_locals(self):
        """
        Apply at the beginning of every method to reset local vars
        """
        self.locals = dict()
        self.defined_vars = set()

    def reset_scope(self):
        self.scope = Scope()


def to_vars(dict: Dict[str, str], const: BaseVar = BaseVar) -> List[BaseVar]:
    return list(map(lambda x: const(*x), dict.items().mapping()))
