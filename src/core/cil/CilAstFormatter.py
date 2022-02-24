from ..tools import visitor
from .CilAst import *


class PrintVisitor(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
        dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
        dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visitor.when(TypeNode)
    def visit(self, node):
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}' for x in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\t{methods}\n}}'

    @visitor.when(DataNode)
    def visit(self, node):
        return f'DATA "{node.value}"'

    @visitor.when(FunctionNode)
    def visit(self, node):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\t{localvars}\n\n\t{instructions}\n}}'

    @visitor.when(ParamNode)
    def visit(self, node):
        return f'PARAM {node.name}'

    @visitor.when(LocalNode)
    def visit(self, node):
        return f'LOCAL {node.name}'

    @visitor.when(AssignNode)
    def visit(self, node):
        return f'{node.dest} = {node.source}'

    @visitor.when(PlusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(MinusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(StarNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(DivNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(AllocateNode)
    def visit(self, node):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(TypeOfNode)
    def visit(self, node):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(StaticCallNode)
    def visit(self, node):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(ArgNode)
    def visit(self, node):
        return f'ARG {node.name}'

    @visitor.when(ReturnNode)
    def visit(self, node):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(LoadNode)
    def visit(self, node):
        return f'{node.dest} = LOAD {self.visit(node.msg)}'

    @visitor.when(PrintStringNode)
    def visit(self, node: PrintStringNode):
        return f'PRINTSTRING {node.str_addr}'

    @visitor.when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        return f'PRINTINT {node.value}'

    @visitor.when(ExitNode)
    def visit(self, node: ExitNode):
        return f'EXIT'

    @visitor.when(CopyNode)
    def visit(self, node):
        return f'{node.dest} = COPY {node.value}'

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        return f'{node.dest} = GETATTRIB {node.obj}.{node.attr} {node.computed_type}'

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        return f'ERROR {self.visit(node.data)}'

    @visitor.when(ReadStringNode)
    def visit(self, node: ReadStringNode):
        return f'{node.dest} = READ'

    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        return f'{node.dest} = READ'

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        return f'SETATTR {node.obj}.{node.attr}: {node.computed_type} = {node.value}'

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        return f'{node.dest} = {node.left} < {node.right}'

    @visitor.when(GotoIfNode)
    def visit(self, node: GotoIfNode):
        return f'GOTOIF {node.condition} {node.label}'

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        return f'GOTO {node.label}'

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        return f'LABEL {node.label}'

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        return f'{node.dest} = SUBSTRING {node.str_value}[{node.index}:{node.index} up to {node.length}]'

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        return f'{node.dest} = CONCAT {node.prefix} + {node.suffix}'

    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        return f'{node.dest} = LENGTH {node.source}'

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @visitor.when(NameNode)
    def visit(self, node: NameNode):
        return f'{node.dest} = NAME {node.value}'

    @visitor.when(EqualStringNode)
    def visit(self, node: EqualStringNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode):
        return f'{node.dest} = ~{node.value}'

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode):
        return f'{node.dest} = {node.left} <= {node.right}'

    @visitor.when(PrefixNode)
    def visit(self, node: PrefixNode):
        return f'PREFFIXNODE'

    @visitor.when(ToStrNode)
    def visit(self, node: ToStrNode):
        return f'{node.dest} = str({node.value})'

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode):
        return 'VOID'

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        return f'{node.dest} = NOT {node.value}'

    @visitor.when(VarNode)
    def visit(self, node: VarNode):
        return f'{node.name}'

    @visitor.when(AttributeNode)
    def visit(self, node: AttributeNode):
        return f'ATTRIBUTE {node.type}.{node.name}'

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode):
        return f'{node.name}'


printer = PrintVisitor()
