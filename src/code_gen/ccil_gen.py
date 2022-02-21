from utils import visitor
import asts.types_ast as sem_ast  # Semantic generated ast
from asts.ccil_ast import *  # CCIL generated ast
from typing import Tuple, List
from code_gen.tools import *


# All operations that define an expression and where it is stored
VISITOR_RESULT = Tuple[List[OperationNode], StorageNode]
CLASS_VISITOR_RESULT = Tuple[ClassNode, List[MethodNode]]
METHOD_VISITOR_RESULT = MethodNode

USER = "user"
ATTR = "attr"

# CCIL stands for Cool Cows Intermediate Language ;)
class CCILGenerator:
    """
    Using the visitor pattern it goes through the semantics ast and produce a ccil ast
    """

    def __init__(self) -> None:
        self.types: List[Class] = list()
        self.time_record: Dict[str, int] = dict()

    @visitor.on("node")
    def visit(self, _):
        pass

    @visitor.when(sem_ast.ProgramNode)
    def visit(self, node: sem_ast.ProgramNode) -> None:
        program_types: List[ClassNode] = list()
        program_codes: List[MethodNode] = list()
        for type in node.declarations:
            classx, class_code = self.visit(type)
            program_types.append(classx)
            program_codes.append(class_code)

    @visitor.when(sem_ast.ClassDeclarationNode)
    def visit(self, node: sem_ast.ClassDeclarationNode) -> CLASS_VISITOR_RESULT:
        attributes: List[Attribute] = list()
        methods: List[Method] = list()

        class_code: List[MethodNode] = list()
        init_attr_ops: List[OperationNode] = list()

        for feature in node.features:
            if isinstance(feature, sem_ast.AttrDeclarationNode):
                attributes.append(Attribute(ATTR + feature.id, feature.type.name))
                (attr_ops, _) = self.visit(feature)
                init_attr_ops += attr_ops
            else:
                methods.append(feature.id)
                method_node = self.visit(feature)
                class_code.append(method_node)

        return (
            ClassNode(attributes, methods, init_attr_ops),
            class_code,
        )

    @visitor.when(sem_ast.AttrDeclarationNode)
    def visit(self, node: sem_ast.AttrDeclarationNode) -> VISITOR_RESULT:
        fval_id = ATTR + node.id

        if node.expr is None:
            op = LocalNode(node, fval_id, node.type.name)
            return [op], op

        (expr_op, expr_fval) = self.visit(node.expr)
        expr_fval.id = fval_id

        return (expr_op, expr_fval)


    @visitor.when(sem_ast.MethodDeclarationNode)
    def visit(self, node: sem_ast.MethodDeclarationNode):
        operations: List[OperationNode] = []
        for param in node.params:
            operations.append(ParamNode(param.id, param.type.name))

        (expr_op, _) = self.visit(node.body)

        operations += expr_op
        return MethodNode(node, node.id, operations)

    @visitor.when(sem_ast.BlocksNode)
    def visit(self, node: sem_ast.BlocksNode) -> VISITOR_RESULT:
        times = self.times(node)

        operations: List[OperationNode] = []
        fvalues: List[StorageNode] = []
        for expr in node.expr_list:
            (expr_ops, expr_fval) = self.visit(expr)
            operations += expr_ops
            fvalues += expr_fval

        fval = fvalues[-1]
        fval.id = f"block_{times}"

        return (operations, fval)

    @visitor.when(sem_ast.LetNode)
    def visit(self, node: sem_ast.LetNode) -> VISITOR_RESULT:
        operations: List[OperationNode] = []
        fvalues: List[StorageNode] = []

        for var in node.var_decl_list:
            (var_ops, var_fv) = self.visit(var)
            operations += var_ops
            fvalues += var_fv

        (in_ops, in_fval) = self.visit(node.in_expr)
        operations += in_ops

        return (operations, in_fval)

    @visitor.when(sem_ast.VarDeclarationNode)
    def visit(self, node: sem_ast.VarDeclarationNode) -> VISITOR_RESULT:
        fvalue_id: str = USER + node.id

        if node.expr is None:
            return ([], create_uninitialized_storage(node, fvalue_id))

        (expr_ops, expr_fv) = self.visit(node.expr)
        expr_fv.id = fvalue_id

        return (expr_ops, expr_fv)

    @visitor.when(sem_ast.AssignNode)
    def visit(self, node: sem_ast.AssignNode) -> VISITOR_RESULT:
        (expr_ops, expr_fval) = self.visit(node.expr)
        expr_fval.id = USER + node.id

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
        then_fval.id = else_fval.id = pre_fvalue_id
        fvalue_id = f"if_{times}_fv"
        fvalue = create_assignation(node, fvalue_id, pre_fvalue_id)

        return ([*if_ops, if_false, *then_ops, else_label, *else_ops, fvalue], fvalue)

    @visitor.when(sem_ast.CaseNode)
    def visit(self, node: sem_ast.CaseNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Visiting case expression
        (case_expr_ops, case_expr_fv) = self.visit(node.case_expr)

        # Storing the type of the resulting case expression
        type_of = create_type_of(
            node, f"case_{times}_typeOf", extract_id(node, case_expr_fv)
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
            branch_var = create_uninitialized_storage(option, branch_var_id)
            branch_var.decl_type = option.branch_type

            # Initializing var which holds the branch var type
            branch_var_type_id = f"case_{times}_optionTypeOf_{i}"
            branch_var_type_of = create_type_of(
                option, branch_var_type_id, extract_id(node, branch_var)
            )

            # Initializng var which holds the comparison result between
            # the case expression type of and branch var type of
            select_branch_id = f"case_{times}_optionSelect_{i}"
            select_branch = create_equality(
                option,
                select_branch_id,
                extract_id(node, type_of),
                extract_id(node, branch_var_type_of),
            )

            # Label that means the start of this branch logic
            branch_label_id = f"case_{times}_branch_{i}"
            branch_label = LabelNode(option, branch_label_id)

            # Conditional jump to the right branch label
            if_op = IfNode(option, extract_id(option, branch_var_type_of), branch_label)
            pattern_match_ops += [branch_var, branch_var_type_of, select_branch, if_op]

            # Visiting the branch logic
            (expr_ops, expr_fval) = self.visit(option.expr)

            # Renaming the last stored value of the expression accordingly
            expr_fval.id = pre_fvalue_id

            # Storing logic to jump to branch logic if this branch is selected
            pattern_match_ops += [branch_var, branch_var_type_of, select_branch, if_op]

            # Translating to ccil of branch logic
            branch_ops += [branch_label, *expr_ops, final_goto]

        # Merging all expression operations in correct order
        # and saving to expression final value
        fval_id = f"case_{times}_fv"
        fval = create_assignation(node, fval_id, pre_fvalue_id)
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
        (body_ops, body_fval) = self.visit(node.body)

        # Setting control flow labels
        loop_label_id = f"loop_{times}"
        loop_label = LabelNode(node, loop_label_id)
        end_loop_label_id = f"endLoop_{times}"
        end_loop_label = LabelNode(node, end_loop_label_id)

        # Setting control flow instructions ifFalse & GoTo
        if_false = IfFalseNode(node, cond_fval, end_loop_label)
        go_to = GoToNode(node, loop_label)

        fval = (create_uninitialized_storage(node, f"loop_{times}_fv"),)
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

        fval = StorageNode(node, fval_id, op)
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

        fval = StorageNode(node, fval_id, op)
        return [*expr_op, fval], fval

    @visitor.when(sem_ast.MethodCallNode)
    def visit(self, node: sem_ast.MethodCallNode) -> VISITOR_RESULT:
        times = self.times(node)

        # Translate all call arguments to ccil
        args_ops: List[OperationNode] = []
        args_fvals: List[StorageNode] = []
        for arg_expr in node.args:
            (arg_op, arg_fval) = self.visit(arg_expr)
            args_ops += arg_op
            args_fvals += [arg_fval]

        # it can have an @ or not
        if node.at_type is None:
            pass

        # It has also an at type

    def times(self, node):
        key: str = type(node).__name__
        try:
            self.time_record[key] += 1
        except KeyError:
            self.time_record[key] = 0
        return self.time_record[key]
