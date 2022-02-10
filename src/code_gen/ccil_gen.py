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
        pass

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

        return [*if_ops, if_false, *then_ops, else_label, *else_ops, fvalue]

    @visitor.when(sem_ast.ArithmeticExprNode)
    def visit(self, node: sem_ast.ArithmeticExprNode):
        pass

    def times(self, node):
        return 0
