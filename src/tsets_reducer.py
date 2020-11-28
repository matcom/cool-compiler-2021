import src.cmp.visitor as visitor
import src.cmp.nbpackage
import src.cmp.visitor as visitor

from src.tset import Tset
from src.cmp.semantic import (
    ObjectType,
    IntType,
    StringType,
    VoidType,
    BoolType,
    ErrorType,
    AutoType,
    SelfType,
    SemanticError,
)
from src.ast_nodes import Node, ProgramNode, ExpressionNode
from src.ast_nodes import ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode
from src.ast_nodes import VarDeclarationNode, AssignNode, CallNode
from src.ast_nodes import (
    AtomicNode,
    UnaryNode,
    BinaryNode,
    ArithmeticOperation,
    ComparisonOperation,
    IfNode,
    LetNode,
    CaseNode,
    CaseItemNode,
    WhileNode,
    BlockNode,
    IsvoidNode,
)
from src.ast_nodes import (
    ConstantNumNode,
    VariableNode,
    InstantiateNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    NegNode,
    NotNode,
    EqualNode,
    BooleanNode,
    StringNode,
)
from src.cmp.utils import find_least_type, union, intersection, reduce_set


class TSetReducer:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    def get_autotype_set(self):
        return {self.context.types.keys()}

    @visitor.on("node")
    def visit(self, node, tset):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tset):
        for declaration in node.declarations:
            self.visit(declaration, tset.children[declaration])
        return tset

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tset):
        for feature in node.features:
            self.visit(feature, tset)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tset):
        if node.init_exp is not None:
            init_expr_set = self.visit(node.init_exp, tset)
            tset.locals[node.id] = reduce_set(tset.locals[node.id], init_expr_set)
            return tset.locals[node.id]

        return tset.locals[node.id]

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tset):
        current_tset = tset.children[node]
        self.visit(node.body, current_tset)

    @visitor.when(AssignNode)
    def visit(self, node, tset):
        expr_set = self.visit(node.expr, tset)
        var_set = tset.find_set(node.id)
        var_set[node.id] = reduce_set(var_set[node.id], expr_set)
        return var_set

    @visitor.when(LetNode)
    def visit(self, node, tset):
        current_tset = tset.children[node]
        for var_dec in node.identifiers:
            self.visit(var_dec, current_tset)

        return self.visit(node.body, current_tset)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, tset):
        if node.expr is not None:
            expr_set = self.visit(node.expr, tset)
            tset.locals[node.id] = reduce_set(tset.locals[node.id], expr_set)

        return tset.locals[node.id]

    @visitor.when(IfNode)
    def visit(self, node, tset):
        self.visit(node.if_expr, tset)
        if isinstance(node.if_expr, VariableNode):
            tset_locals = tset.find_set(node.if_expr.lex)
            tset_locals[node.if_expr.lex] = reduce_set(
                tset_locals[node.if_expr.lex], {"Bool"}
            )
        then_expr_set = self.visit(node.then_expr, tset)
        else_expr_set = self.visit(node.else_expr, tset)

        _union = union(then_expr_set, else_expr_set)

        current_type = None
        for item in _union:
            typex = self.context.get_type(item)
            current_type = find_least_type(current_type, typex, self.context)

        return {current_type.name}

    @visitor.when(WhileNode)
    def visit(self, node, tset):
        self.visit(node.condition, tset)
        self.visit(node.body, tset)

        return {"Object"}

    @visitor.when(CaseNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)

        union_set = set()
        for item in node.case_items:
            item_set = self.visit(item, tset.children[item])
            union_set = union(union_set, item_set)

        current_type = None
        for item in union_set:
            current_type = find_least_type(current_type, item, self.context)

        return current_type

    @visitor.when(CaseItemNode)
    def visit(self, node, tset):
        expr_tset = self.visit(node.expr, tset)
        return reduce_set(tset.locals[node.id], expr_tset)

    @visitor.when(CallNode)
    def visit(self, node, tset):
        pass

    @visitor.when(BlockNode)
    def visit(self, node, tset):
        current_set = None
        for expr in node.expression_list:
            current_set = self.visit(expr, tset)

        return current_set

    @visitor.when(InstantiateNode)  # NewNode
    def visit(self, node, tset):
        return {node.lex}

    @visitor.when(IsvoidNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)
        return {"Bool"}

    @visitor.when(BinaryNode)
    def visit(self, node, tset):
        self.visit(node.left, tset)
        self.visit(node.right, tset)

        int_set = {"Int"}
        if isinstance(node.left, VariableNode):
            node_id = node.left.lex
            tset_locals = tset.find_set(node_id)
            tset_locals[node_id] = reduce_set(tset_locals[node_id], int_set)

        if isinstance(node.right, VariableNode):
            node_id = node.right.lex
            tset_locals = tset.find_set(node_id)
            tset_locals[node_id] = reduce_set(tset_locals[node_id], int_set)

        return int_set

    @visitor.when(EqualNode)
    def visit(self, node, tset):
        pass

    @visitor.when(NotNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)
        return {"Bool"}

    @visitor.when(NegNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)
        return {"Int"}

    @visitor.when(ConstantNumNode)
    def visit(self, node, tset):
        return {"Int"}

    @visitor.when(VariableNode)
    def visit(self, node, tset):
        tset_locals = tset.find_set(node.lex)
        return tset_locals[node.lex]

    @visitor.when(StringNode)
    def visit(self, node, tset):
        return {"String"}

    @visitor.when(BooleanNode)
    def visit(self, node, tset):
        return {"Bool"}

