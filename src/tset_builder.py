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


class TSetBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

    def get_autotype_set(self):
        solve = set(self.context.types.keys())
        solve.remove("AUTO_TYPE")
        return solve

    @visitor.on("node")
    def visit(self, node, tset):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tset=None):
        tset = Tset()
        for declaration in node.declarations:
            self.visit(declaration, tset.create_child(declaration))
        return tset

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tset):
        self.current_type = self.context.get_type(node.id)
        for feature in node.features:
            self.visit(feature, tset)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tset):
        static_type = self.context.get_type(node.type)
        if static_type.name == "AUTO_TYPE":
            tset.locals[node.id] = self.get_autotype_set()
        else:
            tset.locals[node.id] = {static_type.name, "!static_type_declared"}
        if node.init_exp is not None:
            self.visit(node.init_exp, tset)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tset):
        if node.type == "AUTO_TYPE":
            tset.locals[node.id] = self.get_autotype_set()
        else:
            tset.locals[node.id] = {node.type, "!static_type_declared"}

        child_set = tset.create_child(node)
        method = self.current_type.get_method(node.id)
        method.tset = child_set

        for param in node.params:
            typex = self.context.get_type(param[1])
            if typex.name == "AUTO_TYPE":
                child_set.locals[param[0]] = self.get_autotype_set()
            else:
                child_set.locals[param[0]] = {typex.name, "!static_type_declared"}

        self.visit(node.body, child_set)

    @visitor.when(AssignNode)
    def visit(self, node, tset):
        self.visit(node.expr, tset)

    @visitor.when(LetNode)
    def visit(self, node, tset):
        child_set = tset.create_child(node)
        for var_dec in node.identifiers:
            self.visit(var_dec, child_set)

        self.visit(node.body, child_set)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, tset):
        typex = self.context.get_type(node.type)
        if typex.name == "AUTO_TYPE":
            tset.locals[node.id] = self.get_autotype_set()
        else:
            tset.locals[node.id] = {typex.name, "!static_type_declared"}

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
            self.visit(item, tset.create_child(item))

    @visitor.when(CaseItemNode)
    def visit(self, node, tset):
        typex = self.context.get_type(node.type)
        if typex.name == "AUTO_TYPE":
            tset.locals[node.id] = self.get_autotype_set()
        else:
            tset.locals[node.id] = {typex.name, "!static_type_declared"}

        self.visit(node.expr, tset)

    @visitor.when(CallNode)
    def visit(self, node, tset):
        pass

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
