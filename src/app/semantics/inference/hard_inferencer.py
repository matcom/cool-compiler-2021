from app.semantics.ast import *


from app.semantics.tools.type import Type
import app.shared.visitor as visitor
from app.semantics.tools.errors import InternalError
from app.semantics.tools import (
    Context,
    Scope,
    TypeBag,
    conforms,
    equal,
)


class DeepInferrer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.pos = set()
        self.current_type: Type

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ProgramNode:
        return ProgramNode.infer(node, self)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> ClassDeclarationNode:
        return ClassDeclarationNode.infer(node, scope, self)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        return AttrDeclarationNode.infer(node, scope, self)

    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scope: Scope):
        return MethodDeclarationNode.infer(node, scope, self)

    @visitor.when(BlocksNode)
    def visit(self, node, scope):
        return BlocksNode.infer(node, scope, self)

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        return ConditionalNode.infer(node, scope, self)

    @visitor.when(CaseNode)
    def visit(self, node, scope: Scope):
        return CaseNode.infer(node, scope, self)

    @visitor.when(CaseOptionNode)
    def visit(self, node, scope: Scope):
        return CaseOptionNode.infer(node, scope, self)

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        return LoopNode.infer(node, scope, self)

    @visitor.when(LetNode)
    def visit(self, node, scope: Scope):
        return LetNode.infer(node, scope, self)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope: Scope):
        return VarDeclarationNode.infer(node, scope, self)

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope):
        return AssignNode.infer(node, scope, self)

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope):
        return MethodCallNode.infer(node, scope, self)

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        return ArithmeticNode.infer(node, scope, self)

    @visitor.when(LessNode)
    def visit(self, node, scope: Scope):
        return LessNode.infer(node, scope, self)

    @visitor.when(LessOrEqualNode)
    def visit(self, node, scope: Scope):
        return LessOrEqualNode.infer(node, scope, self)

    @visitor.when(EqualsNode)
    def visit(self, node, scope):
        return EqualsNode.infer(node, scope, self)

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope):
        return VariableNode.infer(node, scope, self)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        return NotNode.infer(node, scope, self)

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        return ComplementNode.infer(node, scope, self)

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        return IsVoidNode.infer(node, scope, self)

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        return InstantiateNode.infer(node, scope, self)

    @visitor.when(IntNode)
    def visit(self, node, scope):
        return IntNode.infer(node, scope, self)

    @visitor.when(StringNode)
    def visit(self, node, scope):
        str_node = StringNode(node)
        str_node.inferenced_type = self.context.get_type("String")
        return str_node

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        return BooleanNode.infer(node, scope, self)

    def add_error(self, node: Node, text: str):
        line, col = node.lineno, node.columnno if node else (0, 0)
        if (line, col) in self.pos:
            return
        self.pos.add((line, col))
        self.errors.append(f"({line}, {col}) - " + text)

    def _check_member_types(self, left_node, right_node):
        if self._unrelated_types(left_node) or self._unrelated_types(right_node):
            return

        bag1: TypeBag = left_node.inferenced_type
        bag2: TypeBag = right_node.inferenced_type

        u_obj = self.context.get_type("Object", unpacked=True)
        u_int = self.context.get_type("Int", unpacked=True)
        u_bool = self.context.get_type("Bool", unpacked=True)
        u_string = self.context.get_type("String", unpacked=True)

        contains_obj = u_obj in bag1.type_set and u_obj in bag2.type_set
        contains_int = u_int in bag1.type_set and u_int in bag2.type_set
        contains_bool = u_bool in bag1.type_set and u_bool in bag2.type_set
        contains_string = u_string in bag1.type_set and u_string in bag2.type_set

        if contains_obj or (
            (contains_int and not (contains_bool or contains_string))
            and (contains_bool and not (contains_int or contains_string))
            and (contains_string and not (contains_int or contains_bool))
        ):
            if contains_obj:
                self._conform_to_type(left_node, TypeBag({u_obj}))
                self._conform_to_type(right_node, TypeBag({u_obj}))
            elif contains_int:
                self._conform_to_type(left_node, TypeBag({u_int}))
                self._conform_to_type(right_node, TypeBag({u_int}))
            elif contains_bool:
                self._conform_to_type(left_node, TypeBag({u_bool}))
                self._conform_to_type(right_node, TypeBag({u_bool}))
            elif contains_string:
                self._conform_to_type(left_node, TypeBag({u_string}))
                self._conform_to_type(right_node, TypeBag({u_string}))
            else:
                raise InternalError(
                    "Compiler is not working correctly(DeepInferrer._check_member_types)"
                )
        else:
            basic_set = {u_int, u_bool, u_string}
            if len(bag1.type_set.intersection(basic_set)) == 1:
                self._conform_to_type(right_node, bag1)
            elif len(bag2.type_set.intersection(basic_set)) == 1:
                self._conform_to_type(left_node, bag2)

    def _conform_to_type(self, node: Node, bag: TypeBag):
        node_type = node.inferenced_type
        node_name = node_type.generate_name()
        if not conforms(node_type, bag):
            self.add_error(
                node,
                f"TypeError: Equal Node: Expression type({node_name})"
                f"does not conforms to expression({bag.name})",
            )

    def _arithmetic_operation(self, node, scope):
        left_node = self.visit(node.left, scope)
        left_type = left_node.inferenced_type

        right_node = self.visit(node.right, scope)
        right_type = right_node.inferenced_type

        int_type = self.context.get_type("Int")
        if not equal(left_type, node.left.inferenced_type):
            if not conforms(left_type, int_type):
                left_clone = left_type.clone()
                self.add_error(
                    node.left,
                    f"TypeError: Arithmetic Error: Left member type({left_clone.name})"
                    "does not conforms to Int type.",
                )

        if not equal(right_type, node.right.inferenced_type):
            right_clone = right_type.clone()
            if not conforms(right_type, int_type):
                self.add_error(
                    node.right,
                    f"TypeError: Arithmetic Error: Right member "
                    f"type({right_clone.name})does not conforms to Int type.",
                )

        return left_node, right_node

    def _unrelated_types(self, node):
        typex: TypeBag = node.inferenced_type
        if typex.error_type:
            return True
        if len(typex.heads) > 1:
            self.add_error(
                node,
                "AutotypeError: AUTO_TYPE is ambigous {"
                + ", ".join(typez.name for typez in typex.heads),
                +"}",
            )
            node.inferenced_type = TypeBag(set())
            return True
        return False
