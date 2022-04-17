from __future__ import annotations

from coolcmp.utils import ast
from coolcmp.utils import extract_feat_name
from coolcmp.utils.semantic import Scope


class Node:
    pass


class ProgramNode(Node):
    def __init__(
        self,
        dot_types: list[TypeNode],
        dot_data: list[DataNode],
        dot_code: list[FunctionNode],
    ):
        self.dot_types = dot_types
        self.dot_data = dot_data
        self.dot_code = dot_code
        self.all_methods: list[str] = []

    def get_type(self, name: str) -> TypeNode:
        for type_ in self.dot_types:
            if type_.name == name:
                return type_

    def get_function(self, name: str) -> FunctionNode:
        for func in self.dot_code:
            if func.name == name:
                return func
        raise ValueError(f'Unexpected function name: {name}')

    def get_data_name(self, value: str):
        for data in self.dot_data:
            if data.value == value:
                return data.name
        raise ValueError(f"No data defined for value {value}")

    def set_data(self, value: str):
        if value not in [data.value for data in self.dot_data]:
            self.dot_data.append(DataNode(f"s{len(self.dot_data) + 1}", value))

    def update_method_indexes(self):
        all_methods = set()
        for type_ in self.dot_types:
            all_methods.update([extract_feat_name(m) for m in type_.methods.values()])

        self.all_methods = sorted(list(all_methods))
        for type_ in self.dot_types:
            meths = type_.methods
            new_methods = [
                MethodAt(
                    name=meths[m],
                    index=self.all_methods.index(extract_feat_name(meths[m]))
                ) for m in meths
            ]
            type_.methods = sorted(new_methods)
            type_.total_methods = len(self.all_methods)


class MethodAt:
    def __init__(self, name: str, index: int = -1):
        self.tname = (name, )
        self.index = index

    @property
    def name(self):
        return self.tname[0]

    def __lt__(self, other: MethodAt):
        return extract_feat_name(self.name).__lt__(extract_feat_name(other.name))

    def __eq__(self, other: MethodAt):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'MethodAt({self.name}, {self.index})'


class AttributeAt:
    def __init__(self, name: str, index: int = -1):
        self.name = name
        self.index = index

    def __eq__(self, other: MethodAt):
        return self.name == other.name

    def __str__(self):
        return self.name


class TypeNode(Node):
    def __init__(self,
                 name: str,
                 parent: str | None,
                 attrs: list[str],
                 methods: dict[MethodAt | str, str],
                 attr_expr_nodes: dict[str, tuple[ast.ExpressionNode, Scope]] = None):
        self.name = name
        self.parent = parent
        self.attributes = attrs
        self.methods = methods
        self.attr_expr_nodes = attr_expr_nodes or {}
        self.total_methods: int | None = None
        self.init_locals: list[LocalNode] = []

    # Add the expression node of the attributes, so when is created an instance
    #   get quick access to the instructions of the attribute initialization.
    def add_attr_node(self, attr: str, node: ast.ExpressionNode | int | str, scope: Scope):
        self.attr_expr_nodes[attr] = (node, scope)

    def get_attr_node(self, attr: str) -> tuple[ast.ExpressionNode | int | str, Scope]:
        return self.attr_expr_nodes.get(attr)

    def add_local(self, local: LocalNode):
        return self.init_locals.append(local)


class DataNode(Node):
    def __init__(self, vname: str, value: str):
        self.name = vname
        self.value = value


class FunctionNode(Node):
    def __init__(
        self,
        name: str,
        params: list[ParamNode],
        local_vars: list[LocalNode],
        instructions: list[InstructionNode],
    ):
        self.name = name
        self.params = params
        self.local_vars = local_vars
        self.instructions = instructions

    @property
    def args_space(self):
        """
        Returns the size of the space used by this function args in the stack.
        """
        return len(self.params) * 4


class ParamNode(Node):
    def __init__(self, name: str):
        self.name = name


class LocalNode(Node):
    def __init__(self, name: str):
        self.name = name


class InstructionNode(Node):
    pass


class CommentNode(InstructionNode):
    def __init__(self, text: str):
        self.text = text


class AssignNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.dest = dest
        self.source = source


class ArithmeticNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.dest = dest
        self.left = left
        self.right = right


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class ConformsNode(ArithmeticNode):
    pass


class GetAttrNode(InstructionNode):
    def __init__(self, dest: str, src: str, attr: str):
        self.dest = dest
        self.src = src
        self.attr = attr


class SetAttrNode(InstructionNode):
    def __init__(self, instance: str, attr: AttributeAt, value: str):
        self.instance = instance
        self.attr = attr
        self.value = value


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, type_: str, dest: str):
        self.type = type_
        self.dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.type = None
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    def __init__(self, name: str):
        self.name = name


class GotoNode(InstructionNode):
    def __init__(self, label: str):
        self.label = label


class GotoIfNode(InstructionNode):
    def __init__(self, condition: str, label: str):
        self.condition = condition
        self.label = label


class StaticCallNode(InstructionNode):
    def __init__(self, function: str, dest: str):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, obj: str, method: str, dest: str, type_: str | None, dtype: str):
        self.obj = obj
        self.method = method
        self.dest = dest
        self.type = type_
        self.dtype = dtype


class ArgNode(InstructionNode):
    def __init__(self, name: str):
        self.name = name


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest: str, msg: str):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    def __init__(self, src: str, dest: str):
        self.src = src
        self.dest = dest


class ConcatNode(InstructionNode):
    def __init__(self, dest: str, str1: str, str2: str):
        self.dest = dest
        self.str1 = str1
        self.str2 = str2


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    def __init__(self, dest: str, src: str, index: str, length: str):
        self.dest = dest
        self.src = src
        self.index = index
        self.length = length


class ToStrNode(InstructionNode):
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ReadIntNode(ReadNode):
    pass


class ReadStringNode(ReadNode):
    pass


class PrintNode(InstructionNode):
    def __init__(self, addr: str):
        self.addr = addr


class PrintIntNode(PrintNode):
    pass


class PrintStringNode(PrintNode):
    pass


class NegationNode(InstructionNode):
    def __init__(self, dest: str, src: str):
        self.dest = dest
        self.src = src


class ComplementNode(InstructionNode):
    def __init__(self, dest: str, src: str):
        self.dest = dest
        self.src = src


class CompareNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.dest = dest
        self.left = left
        self.right = right


class LessThanNode(CompareNode):
    pass


class LessEqualNode(CompareNode):
    pass


class EqualNode(CompareNode):
    pass


class IsVoidNode(InstructionNode):
    def __init__(self, dest: str, src: str):
        self.dest = dest
        self.src = src


class TypeNameNode(InstructionNode):
    def __init__(self, dest: str, src: str):
        self.dest = dest
        self.src = src


class InitNode(InstructionNode):
    def __init__(self, dest: str, type_name: str):
        self.type_name = type_name
        self.dest = dest


class AbortNode(InstructionNode):
    pass


class RuntimeErrorNode(InstructionNode):
    pass


class CaseMatchRuntimeErrorNode(RuntimeError):
    pass


class ExprVoidRuntimeErrorNode(RuntimeError):
    pass
