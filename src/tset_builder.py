import src.cmp.visitor as visitor
import src.cmp.nbpackage
import src.cmp.visitor as visitor

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


class Tset:
    def __init__(self, parent=None):
        self.tsets_dict = {}
        self.parent = parent
        self.children = {}

    def create_child(self, node):
        child = Tset(self)
        self.children[node] = child
        return child

    def __str__(self):
        output = ""

        for key, value in self.tsets_dict.items():
            output += "\t" + str(key) + ":" + str(value) + "\n"
        for key, chil in self.children.items():
            output += "\n"
            try:
                output += key.id + "--->"
            except AttributeError:
                output += "let or case --->"
            output += "\n"
            output += str(chil)
        return output


class TSetBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    def get_autotype_set(self):
        return set(self.context.types.keys())

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
        for feature in node.features:
            self.visit(feature, tset)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tset):
        static_type = self.context.get_type(node.type)
        if static_type.name == "AUTO_TYPE":
            tset.tsets_dict[node.id] = self.get_autotype_set()
        else:
            tset.tsets_dict[node.id] = set([static_type.name])
        if node.init_exp is not None:
            self.visit(node.init_exp, tset)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tset):
        child_set = tset.create_child(node)
        for param in node.params:
            typex = self.context.get_type(param[1])
            if typex.name == "AUTO_TYPE":
                child_set.tsets_dict[param[0]] = self.get_autotype_set()
            else:
                child_set.tsets_dict[param[0]] = set([typex.name])

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
            tset.tsets_dict[node.id] = self.get_autotype_set()
        else:
            tset.tsets_dict[node.id] = set([typex.name])

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
            tset.tsets_dict[node.id] = self.get_autotype_set()
        else:
            tset.tsets_dict[node.id] = set([typex.name])

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
