from utils import visitor
import asts.types_ast as sem_ast  # Semantic generated ast
from asts.ccil_ast import *  # CCIL generated ast
from typing import Tuple, List


# All operations that define an expression and where it is stored
VISITOR_RESULT = Tuple[List[OperationNode], StorageNode]

# CCIL stands for Cool Cows Intermediate Language ;)
class CCILGenerator:
    """
    Using the visitor pattern it goes through the semantics ast and produce a ccil ast
    """

    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, _):
        self.time_record: Dict[str, int] = Dict()

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

        # Loop Nodes have void return type, how to express it??
        return (
            [*cond_ops, loop_label, if_false, *body_ops, go_to, end_loop_label],
            None,
        )

    @visitor.when(sem_ast.ArithmeticNode)
    def visit(self, node: sem_ast.ArithmeticNode) -> VISITOR_RESULT:
        times = self.times(node)

        (left_ops, left_fval) = self.visit(node.left)
        (right_ops, right_fval) = self.visit(node.right)

        left_id = extract_id(node, left_fval)
        right_id = extract_id(node, right_fval)

        op: ReturnOpNode
        match node:
            case sem_ast.PlusNode:
                op = SumOpNode(left_id, right_id)
            case sem_ast.MinusNode:
                op = MinusOpNode(left_id, right_id)
            case sem_ast.StarNode:
                op = MultOpNode(left_id, right_id)
            case sem_ast.DivNode:
                op = DivOpNode(left_id, right_id)
            case _:
                raise Exception("Pattern match failure visiting artihmetic expression")

        fval_id = f"arith_{times}"
        fval = StorageNode(node, fval_id, op)

        return ([*left_ops, *right_ops, fval], fval)

    def times(self, node):
        key: str = type(node).__name__
        try:
            self.time_record[key] += 1
        except KeyError:
            self.time_record[key] = 0
        return self.time_record[key]
