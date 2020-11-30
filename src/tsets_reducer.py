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
        self.current_type = None
        self.current_method = None
        self.errors = errors

    def get_autotype_set(self):
        return {self.context.types.keys()}

    @visitor.on("node")
    def visit(self, node, tset):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tset):
        backup_tset = Tset()
        while not backup_tset.compare(tset):
            backup_tset = tset.clone()

            for declaration in node.declarations:
                self.visit(declaration, tset.children[declaration])

        tset.clean()
        return tset

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tset):
        self.current_type = self.context.get_type(node.id)
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
        method = self.current_type.get_method(node.id)
        self.current_method = method

        current_tset = tset.children[node]
        body_set = self.visit(node.body, current_tset)
        tset.locals[node.id] = reduce_set(tset.locals[node.id], body_set)
        method.tset = tset.locals[node.id]

    @visitor.when(AssignNode)
    def visit(self, node, tset):
        expr_set = self.visit(node.expr, tset)
        var_set = tset.find_set(node.id)
        var_set[node.id] = reduce_set(var_set[node.id], expr_set)
        return var_set[node.id]

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

        solve = intersection(then_expr_set, else_expr_set)
        if len(solve) == 0:
            solve = union(then_expr_set, else_expr_set)

        return solve

    @visitor.when(WhileNode)
    def visit(self, node, tset):
        self.visit(node.condition, tset)

        if isinstance(node.condition, VariableNode):
            node_id = node.condition.lex
            tset_locals = tset.find_set(node_id)
            tset_locals[node_id] = reduce_set(tset_locals[node_id], {"Bool"})

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
            if item == "!static_type_declared":
                continue
            item_type = self.context.get_type(item)
            current_type = find_least_type([current_type, item_type], self.context)

        return {current_type.name}

    @visitor.when(CaseItemNode)
    def visit(self, node, tset):
        expr_tset = self.visit(node.expr, tset)
        tset.locals[node.id] = reduce_set(tset.locals[node.id], expr_tset)
        return tset.locals[node.id]

    @visitor.when(CallNode)
    def visit(self, node, tset):
        for expr in node.args:
            self.visit(expr, tset)

        if node.obj is not None:
            expr_set = self.visit(node.obj, tset)
        else:
            expr_set = {self.current_type.name}

        types_with_method = set()
        if node.at_type is not None:
            types_with_method.add(node.at_type)

        else:
            for typex in self.context.types.values():
                try:
                    method = typex.get_method(node.id)
                    if len(method.param_names) == len(node.args):
                        types_with_method.add(typex.name)
                except SemanticError:
                    continue

        # DUDA!!!!
        # if len(types_with_method) == 0:
        #     raise SemanticError(
        #         f"There is no method named {node.id} that takes {len(node.args)} arguments"
        #     )

        if isinstance(node.obj, VariableNode):
            node_id = node.obj.lex
            tset_locals = tset.find_set(node_id)

            tset_locals[node_id] = reduce_set(tset_locals[node_id], types_with_method)

        types_reduced = intersection(expr_set, types_with_method)

        if len(types_reduced) == 0:
            return {"InferenceError"}

        return_types = set()
        for item in types_reduced:
            item_type = self.context.get_type(item)
            method = item_type.get_method(node.id)
            for typex in method.tset:
                return_types.add(typex)

        return return_types

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
        self.visit(node.left, tset)
        self.visit(node.right, tset)

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

