from typing import List
from semantics.tools.type import Type, join_list
from utils import visitor

from semantics.tools import TypeBag, Scope
import ast.types_ast as types_ast
from ast.inferencer_ast import (
    BinaryNode,
    BooleanNode,
    ComplementNode,
    DivNode,
    EqualsNode,
    InstantiateNode,
    IntNode,
    LessNode,
    LessOrEqualNode,
    MinusNode,
    NotNode,
    PlusNode,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    AttrDeclarationNode,
    BlocksNode,
    ConditionalNode,
    CaseNode,
    CaseOptionNode,
    LoopNode,
    LetNode,
    StarNode,
    StringNode,
    VarDeclarationNode,
    AssignNode,
    MethodCallNode,
    ClassDeclarationNode,
    ProgramNode,
    AttrDeclarationNode,
    Node,
    VariableNode,
    IsVoidNode,
)


class TypesInferencer:
    def __init__(self) -> None:
        self.errors = []

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> types_ast.ProgramNode:
        class_decl = []
        scope = Scope()
        for decl in node.declarations:
            class_decl.append(self.visit(decl, scope.create_child()))

        return types_ast.ProgramNode(class_decl, node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> types_ast.ClassDeclarationNode:
        features = []
        for feature in node.features:
            features.append(self.visit(feature, scope))

        return types_ast.ClassDeclarationNode(features, node)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope) -> types_ast.AttrDeclarationNode:
        new_node = types_ast.AttrDeclarationNode(node)
        if node.expr:
            new_node.expr = self.visit(node.expr, scope)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode, scope: Scope) -> types_ast.MethodDeclarationNode:
        scope = scope.create_child()
        
        for param in node.params:
            param_type = self._reduce_to_type(param.inferenced_type,node, general=True)
            scope.define_variable(param.id, param_type)

        params = [self.visit(param, scope) for param in node.params]
        
        body = self.visit(node.body, scope)
        
        ret_type = self._reduce_to_type(node.inferenced_type, node)
        return types_ast.MethodDeclarationNode(params, ret_type, body, node)

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode, scope: Scope) -> types_ast.BlocksNode:
        expr_list = [self.visit(expr, scope) for expr in node.expr_list]

        new_node = types_ast.BlocksNode(expr_list, node)
        new_node.type = expr_list[-1].type
        return new_node

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope) -> types_ast.ConditionalNode:
        condition = self.visit(node.condition, scope)
        then_body = self.visit(node.then_body, scope)
        else_body = self.visit(node.else_body, scope)

        new_node = types_ast.ConditionalNode(condition, then_body, else_body, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope) -> types_ast.CaseNode:
        expr = self.visit(node.case_expr, scope)
        
        case_options = []
        for option in node.options:
            child_scope = scope.create_child()
            case_options.append(self.visit(option, child_scope))

        new_node = types_ast.CaseNode(expr, case_options, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode, scope: Scope) -> types_ast.CaseOptionNode:
        return types_ast.CaseOptionNode(self.visit(node.expr, scope), node)

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope: Scope) -> types_ast.LoopNode:
        condition = self.visit(node.condition, scope)
        body = self.visit(node.body, scope)
        new_node = types_ast.LoopNode(condition, body, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope) -> types_ast.LetNode:
        scope = scope.create_child()
        var_decl_list = [self.visit(var_decl, scope) for var_decl in node.var_decl_list]
        in_expr = self.visit(node.in_expr,scope)
        new_node = types_ast.LetNode(var_decl_list, in_expr, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope) -> types_ast.VarDeclarationNode:
        new_node = types_ast.VarDeclarationNode(node)
        if node.expr:
            new_node.expr = self.visit(node.expr, scope)

        var_info = scope.find_variable(node.id)
        general = var_info is not None # it's a param
        new_node.type = self._reduce_to_type(node.inferenced_type,node, general)

        return new_node

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope) -> types_ast.AssignNode:
        expr = self.visit(node.expr, scope)
        new_node = types_ast.AssignNode(expr, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope: Scope) -> types_ast.MethodCallNode:
        args = [self.visit(arg, scope) for arg in node.args]
        caller_expr = self.visit(node.expr, scope)
        new_node = types_ast.MethodCallNode(node.caller_type, caller_expr, args, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope) -> types_ast.VariableNode:
        new_node = types_ast.VariableNode(node)
        
        if node.defined:
            var_info = scope.find_variable(node.value)
            general = var_info is not None
            new_node.type = self._reduce_to_type(node.inferenced_type, node, general)
         
        return new_node

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope) -> types_ast.IsVoidNode:
        expr = self.visit(node.expr, scope)
        new_node = types_ast.IsVoidNode(expr, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope) -> types_ast.NotNode:
        expr = self.visit(node.expr, scope)
        new_node = types_ast.NotNode(expr, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode, scope: Scope) -> types_ast.ComplementNode:
        expr = self.visit(node.expr)
        new_node = types_ast.ComplementNode(expr, node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(BinaryNode)
    def visit(self, node, scope: Scope) -> types_ast.BinaryNode:
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        if isinstance(node, PlusNode):
            new_node = types_ast.PlusNode(left, right, node)
        elif isinstance(node, MinusNode):
            new_node = types_ast.MinusNode(left, right, node)
        elif isinstance(node, DivNode):
            new_node = types_ast.DivNode(left, right, node)
        elif isinstance(node, StarNode):
            new_node = types_ast.StarNode(left, right, node)
        elif isinstance(node, LessNode):
            new_node = types_ast.LessNode(left, right, node)
        elif isinstance(node, LessOrEqualNode):
            new_node = types_ast.LessOrEqualNode(left, right, node)
        elif isinstance(node, EqualsNode):
            new_node = types_ast.EqualsNode(left, right, node)

        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: Scope) -> types_ast.BooleanNode:
        new_node = types_ast.BooleanNode(node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope) -> types_ast.StringNode:
        new_node = types_ast.StringNode(node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(IntNode)
    def visit(self, node: IntNode, scope: Scope) -> types_ast.IntNode:
        new_node = types_ast.IntNode(node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope: Scope) -> types_ast.InstantiateNode:
        new_node = types_ast.InstantiateNode(node)
        new_node.type = self._reduce_to_type(node.inferenced_type, node)
        return new_node

    def _reduce_to_type(self, bag: TypeBag, node: Node, general=False):
        if len(bag.heads) > 1:
            self.add_error(
                node,
                f"TypeError: Ambiguous type declaration, multiple values {bag.generate_name()}",
            )
            return TypeBag(set())
        if len(bag.heads) == 0:
            self.add_error(node, "TypeError: Cannot infer expression's type")
            return TypeBag(set())

        if general:
            return bag.heads[0]

        order_types = list(bag.type_set)
        order_types.sort(key=lambda x: -1 * x.index)

        higher_index_types = [order_types[0]]
        higher_index = order_types[0].index
        for typex in order_types[2:]:
            if typex.index == higher_index:
                higher_index_types.append(typex)

        return self._join_types(higher_index_types)

    def _join_types(self, types : List[Type]):
        types_bags = []
        for typex in types:
            types_bags.append(TypeBag({typex}, heads=[typex]))
        return join_list(types_bags).heads[0]

    def add_error(self, node, text: str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))