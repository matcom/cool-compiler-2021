from utils import visitor
import asts.types_ast as sem_ast  # Semantic generated ast
from asts.ccil_ast import *  # CCIL generated ast
from typing import Tuple, List


# All operations that define an expression and where it is stored
VISITOR_RESULT = Tuple[List[OperationNode], StorageNode]

USER = "user"

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

    @visitor.when(sem_ast.BlocksNode)
    def visit(self, node:sem_ast.BlocksNode) -> VISITOR_RESULT:
        times = self.times(node)

        operations:List[OperationNode] = []
        fvalues:List[StorageNode] = []
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

        return(operations, in_fval)

    @visitor.when(sem_ast.VarDeclarationNode)
    def visit(self, node: sem_ast.VarDeclarationNode) -> VISITOR_RESULT:
        fvalue_id:str = USER + node.id

        if node.expr is None:
            return ([], create_uninitialized_storage(node, fvalue_id))

        (expr_ops, expr_fv) =  self.visit(node.expr)
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
    def visit(self, node:sem_ast.CaseNode) -> VISITOR_RESULT:
        times = self.times(node)

        (case_expr_ops, case_expr_fv) = self.visit(node.case_expr)

        type_of = create_type_of(
                    node,
                    f"case_{times}_typeOf",
                    extract_id(node, case_expr_fv)
                )

        operations = [*case_expr_ops, type_of]

        for (i, option) in enumerate(node.options):
            option_id = f"case_{times}_option_{i}"
            options_st = create_uninitialized_storage(option, option_id)
            # The type of the option node must be stored to do the pattern matching!

    @visitor.when(sem_ast.CaseOptionNode)
    def visit(self, node:sem_ast.CaseOptionNode) -> VISITOR_RESULT:
        times = self.times(node)

        

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

        fval = create_uninitialized_storage(node, f"loop_{times}_fv"),
        # Loop Nodes have void return type, how to express it??
        return (
            [*cond_ops, loop_label, if_false, *body_ops, go_to, end_loop_label, fval],
            fval
        )

    @visitor.when(sem_ast.ArithmeticNode)
    def visit(self, node: sem_ast.ArithmeticNode) -> VISITOR_RESULT:
        times = self.times(node)

        (left_ops, left_fval) = self.visit(node.left)
        (right_ops, right_fval) = self.visit(node.right)

        left_id = extract_id(node, left_fval)
        right_id = extract_id(node, right_fval)

        op: ReturnOpNode
        fval_id: str
        match node:
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
            case _:
                raise Exception("Pattern match failure visiting artihmetic expression")

        fval = StorageNode(node, fval_id, op)

        return ([*left_ops, *right_ops, fval], fval)

    def times(self, node):
        key: str = type(node).__name__
        try:
            self.time_record[key] += 1
        except KeyError:
            self.time_record[key] = 0
        return self.time_record[key]
