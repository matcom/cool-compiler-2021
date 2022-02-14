from typing import Any, List, Tuple
import cool.visitor as visitor


class Node:
    comment: str = ""

    def set_comment(self, comment: str) -> "Node":
        self.comment = comment
        return self


class ProgramNode(Node):
    def __init__(
        self,
        dottypes: List["TypeNode"],
        dotdata: List["DataNode"],
        dotcode: List["FunctionNode"],
    ):
        self.dottypes: List[TypeNode] = dottypes
        self.dotdata: List[DataNode] = dotdata
        self.dotcode: List[FunctionNode] = dotcode


class TypeNode(Node):
    def __init__(self, name: str):
        self.name: str = name
        self.attributes: List[str] = []
        self.methods: List[Tuple[str, str]] = []


class DataNode(Node):
    def __init__(self, name: str, value: Any):
        self.name: str = name
        self.value: Any = value


class FunctionNode(Node):
    def __init__(
        self,
        name: str,
        params: List["ParamNode"],
        local_vars: List["LoadNode"],
        instructions: List["InstructionNode"],
    ):
        self.name: str = name
        self.params: List[ParamNode] = params
        self.local_vars: List[LocalNode] = local_vars
        self.instructions: List[InstructionNode] = instructions


class ParamNode(Node):
    def __init__(self, name: str):
        self.name: str = name


class LocalNode(Node):
    def __init__(self, name: str):
        self.name: str = name


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.dest: str = dest
        self.source: str = source


class ArithmeticNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.dest: str = dest
        self.left: str = left
        self.right: str = right


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class LessEqualNode(ArithmeticNode):
    pass


class LessThanNode(ArithmeticNode):
    pass


class EqualNode(ArithmeticNode):
    pass


class GetAttribNode(InstructionNode):
    def __init__(self, dest: str, instance: str, attr: str) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.attr: str = attr


class SetAttribNode(InstructionNode):
    def __init__(self, instance: str, attr: str, source: str) -> None:
        self.instance: str = instance
        self.attr: str = attr
        self.source: str = source


class GetIndexNode(InstructionNode):
    def __init__(self, dest: str, instance: str, index: str) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.index: str = index


class SetIndexNode(InstructionNode):
    def __init__(self, instance: str, index: int, source: str) -> None:
        self.instance: str = instance
        self.index: int = index
        self.source: str = source


class AllocateNode(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.type: str = itype
        self.dest: str = dest


class ArrayNode(InstructionNode):
    def __init__(self, dest: str, size: int) -> None:
        self.dest: str = dest
        self.size: int = size


class TypeOfNode(InstructionNode):
    def __init__(self, dest: str, obj: str, ):
        self.obj: str = obj
        self.dest: str = dest


class AncestorNode(InstructionNode):
    def __init__(self, dest: str, obj: str):
        self.obj: str = obj
        self.dest: str = dest


class TypeDirectionNode(InstructionNode):
    def __init__(self, dest: str, name: str):
        self.name: str = name
        self.dest: str = dest

class LabelNode(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class GotoNode(InstructionNode):
    def __init__(self, address: str):
        self.address: str = address


class GotoIfNode(InstructionNode):
    def __init__(self, condition: str, address: str):
        self.condition: str = condition
        self.address: str = address


class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype: str, method: str, dest: str):
        self.type = xtype
        self.method = method
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name: str):
        self.name: str = name


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    pass


class ConcatNode(InstructionNode):
    pass


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    pass


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class CommentNode(InstructionNode):
    def __init__(self, comment):
        self.comment = comment


class EmptyInstruction(InstructionNode):
    def __init__(self):
        pass


class CILFormatter:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        dottypes = "\n".join(self.visit(t) for t in node.dottypes)
        dotdata = "\n".join(self.visit(t) for t in node.dotdata)
        dotcode = "\n".join(self.visit(t) for t in node.dotcode)

        return f".TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}"

    @visitor.when(TypeNode)
    def visit(self, node):
        attributes = "\n\t".join(f"attribute {x}" for x in node.attributes)
        methods = "\n\t".join(f"method {x}: {y}" for x, y in node.methods)

        return f"type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}"

    @visitor.when(FunctionNode)
    def visit(self, node):
        params = "\n\t".join(self.visit(x) for x in node.params)
        local_vars = "\n\t".join(self.visit(x) for x in node.local_vars)
        instructions = "\n\t".join(self.visit(x) for x in node.instructions)

        return f"function {node.name} {{\n\t{params}\n\n\t{local_vars}\n\n\t{instructions}\n}}"

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode):
        return (
            f"PARAM {node.name}"
            if node.comment == ""
            else f"PARAM {node.name} # {node.comment}"
        )

    @visitor.when(LocalNode)
    def visit(self, node):
        return (
            f"LOCAL {node.name}"
            if node.comment == ""
            else f"LOCAL {node.name} # {node.comment}"
        )

    @visitor.when(AssignNode)
    def visit(self, node):
        return (
            f"{node.dest} = {node.source}"
            if node.comment == ""
            else f"{node.dest} = {node.source} # {node.comment}"
        )

    @visitor.when(PlusNode)
    def visit(self, node):
        return (
            f"{node.dest} = {node.left} + {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} + {node.right} # {node.comment}"
        )

    @visitor.when(MinusNode)
    def visit(self, node):
        return (
            f"{node.dest} = {node.left} - {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} - {node.right} # {node.comment}"
        )

    @visitor.when(StarNode)
    def visit(self, node):
        return (
            f"{node.dest} = {node.left} * {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} * {node.right} # {node.comment}"
        )

    @visitor.when(DivNode)
    def visit(self, node):
        return (
            f"{node.dest} = {node.left} / {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} / {node.right} # {node.comment}"
        )

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        return (
            f"{node.dest} = {node.left} == {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} == {node.right} # {node.comment}"
        )

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        return (
            f"{node.dest} = {node.left} < {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} < {node.right} # {node.comment}"
        )

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode):
        return (
            f"{node.dest} = {node.left} <= {node.right}"
            if node.comment == ""
            else f"{node.dest} = {node.left} <= {node.right} # {node.comment}"
        )

    @visitor.when(AllocateNode)
    def visit(self, node):
        return (
            f"{node.dest} = ALLOCATE {node.type}"
            if node.comment == ""
            else f"{node.dest} = ALLOCATE {node.type} # {node.comment}"
        )

    @visitor.when(TypeOfNode)
    def visit(self, node):
        return (
            f"{node.dest} = TYPEOF {node.obj}"
            if node.comment == ""
            else f"{node.dest} = TYPEOF {node.obj} # {node.comment}"
        )

    @visitor.when(TypeDirectionNode)
    def visit(self, node: TypeDirectionNode):
        return (
            f"{node.dest} = TYPEDIR {node.name}"
            if node.comment == ""
            else f"{node.dest} = TYPEDIR {node.name} # {node.comment}"
        )

    @visitor.when(AncestorNode)
    def visit(self, node):
        return (
            f"{node.dest} = ANCESTOR {node.obj}"
            if node.comment == ""
            else f"{node.dest} = ANCESTOR {node.obj} # {node.comment}"
        )

    @visitor.when(StaticCallNode)
    def visit(self, node):
        return (
            f"{node.dest} = CALL {node.function}"
            if node.comment == ""
            else f"{node.dest} = CALL {node.function} # {node.comment}"
        )

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        return (
            f"{node.dest} = VCALL {node.type} {node.method}"
            if node.comment == ""
            else f"{node.dest} = VCALL {node.type} {node.method} # {node.comment}"
        )

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        return (
            f"{node.dest} = GETATTR {node.instance} {node.attr}"
            if node.comment == ""
            else f"{node.dest} = GETATTR {node.instance} {node.attr} # {node.comment}"
        )

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        return (
            f"SETATTR {node.instance} {node.attr} {node.source}"
            if node.comment == ""
            else f"SETATTR {node.instance} {node.attr} {node.source} # {node.comment}"
        )

    @visitor.when(ArgNode)
    def visit(self, node):
        return (
            f"ARG {node.name}"
            if node.comment == ""
            else f"ARG {node.name} # {node.comment}"
        )

    @visitor.when(ReturnNode)
    def visit(self, node):
        return (
            f"\n\tRETURN {node.value if node.value is not None else 0}"
            if node.comment == ""
            else f"\n\tRETURN {node.value if node.value is not None else 0} # {node.comment}"
        )

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        return (
            f"GOTO {node.address}"
            if node.comment == ""
            else f"GOTO {node.address} # {node.comment}"
        )

    @visitor.when(GotoIfNode)
    def visit(self, node: GotoNode):
        return (
            f"IF {node.condition} GOTO {node.address}"
            if node.comment == ""
            else f"IF {node.condition} GOTO {node.address} # {node.comment}"
        )

    @visitor.when(LabelNode)
    def visit(self, node):
        return (
            f"{node.label}:"
            if node.comment == ""
            else f"{node.label}: # {node.comment}"
        )

    @visitor.when(ArrayNode)
    def visit(self, node: ArrayNode):
        return (
            f"{node.dest} = ARRAY {node.size}"
            if node.comment == ""
            else f"{node.dest} = ARRAY {node.size} # {node.comment}"
        )

    @visitor.when(GetIndexNode)
    def visit(self, node: GetIndexNode):
        return (
            f"{node.dest} = GETINDEX {node.instance} {node.index}"
            if node.comment == ""
            else f"{node.dest} = GETINDEX {node.instance} {node.index} # {node.comment}"
        )

    @visitor.when(SetIndexNode)
    def visit(self, node: SetIndexNode):
        return (
            f"SETINDEX {node.instance} {node.index} {node.source}"
            if node.comment == ""
            else f"SETINDEX {node.instance} {node.index} {node.source} # {node.comment}"
        )

    @visitor.when(CommentNode)
    def visit(self, node):
        return f"# {node.comment}"

    @visitor.when(EmptyInstruction)
    def visit(self, node: EmptyInstruction):
        return "" if node.comment == "" else f"# {node.comment}"
