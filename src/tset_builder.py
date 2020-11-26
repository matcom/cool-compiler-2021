import src.cmp.visitor as visitor
import src.cmp.nbpackage
import src.cmp.visitor as visitor

from src.ast_nodes import Node, ProgramNode, ExpressionNode
from src.ast_nodes import ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode
from src.ast_nodes import VarDeclarationNode, AssignNode, CallNode
from src.ast_nodes import (
    AtomicNode,
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


class Tset:
    def __init__(self, parent=None):
        self.tsets_dict = {}
        self.parent = parent
        self.children = {}

    def create_child(self, node):
        child = Tset(self)
        self.children[node] = child
        return child


class TSetBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    @visitor.on("node")
    def visit(self, node, tset):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tset=None):
        tset = Tset()
        for declaration in node.declarations:
            self.visit(declaration, tset.create_child())
        return tset

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tset):
        pass

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tset):
        pass

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tset):
        pass

    @visitor.when(LetNode)
    def visit(self, node, tset):
        pass

    @visitor.when(CaseNode)
    def visit(self, node, tset):
        pass

    @visitor.when(CaseItemNode)
    def visit(self, node, tset):
        pass


def get_autotype_set():
    pass
