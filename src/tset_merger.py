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
from src.cmp.utils import least_type


class TSetMerger:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    def get_autotype_set(self):
        solve = set(self.context.types.keys())
        solve.remove("AUTO_TYPE")
        return solve

    @visitor.on("node")
    def visit(self, node, tset):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tset):
        for declaration in node.declarations:
            self.visit(declaration, tset.children[declaration])

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tset):
        for feature in node.features:
            self.visit(feature, tset)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tset):
        typex = least_type(tset.locals[node.id], self.context)
        node.type = typex

        if node.init_exp is not None:
            self.visit(node.init_exp, tset)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tset):
        return_type = least_type(tset.locals[node.id], self.context)
        node.type = return_type

        child_tset = tset.children[node]
        args_types = []
        for param in node.params:
            typex = least_type(child_tset.locals[param[0]], self.context)
            args_types.append((param[0], typex))

        for i in range(len(args_types)):
            node.params[i] = args_types[i]
        self.visit(node.body, child_tset)

    @visitor.when(AssignNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)

    @visitor.when(LetNode)
    def visit(self, node, tset):
        child_set = tset.children[node]
        for var_dec in node.identifiers:
            self.visit(var_dec, child_set)

        self.visit(node.body, child_set)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, tset):
        typex = least_type(tset.locals[node.id], self.context)
        node.type = typex

        if node.expr is not None:
            self.visit(node.expr, tset)

    @visitor.when(IfNode)
    def visit(self, node, tset):
        self.visit(node.if_expr, tset)
        self.visit(node.then_expr, tset)
        self.visit(node.else_expr, tset)

    @visitor.when(WhileNode)
    def visit(self, node, tset):
        self.visit(node.condition, tset)
        self.visit(node.body, tset)

    @visitor.when(CaseNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)

        for item in node.case_items:
            self.visit(item, tset.children[item])

    @visitor.when(CaseItemNode)
    def visit(self, node, tset):
        typex = least_type(tset.locals[node.id], self.context)
        node.type = typex
        self.visit(node.expr, tset)

    @visitor.when(CallNode)
    def visit(self, node, tset):
        for arg in node.args:
            self.visit(arg, tset)

    @visitor.when(BlockNode)
    def visit(self, node, tset):
        for expr in node.expression_list:
            self.visit(expr, tset)

    @visitor.when(AtomicNode)
    def visit(self, node, tset):
        pass

    @visitor.when(UnaryNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)

    @visitor.when(BinaryNode)
    def visit(self, node, tset):
        self.visit(node.left, tset)
        self.visit(node.right, tset)
