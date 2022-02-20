from . import visitor
from .cil import ProgramNode, TypeNode, FunctionNode, ParamNode, AssignNode, PlusNode, MinusNode, StarNode, DivNode, \
    TypeOfNode, StaticCallNode, DynamicCallNode, ArgNode, ReturnNode, LocalNode, AllocateNode, DataNode, GetAttrNode, \
    PrintNode, LoadNode, SetAttrNode


class CILFormatter(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        types = '\n'.join(self.visit(t) for t in node.dot_types)
        data = '\n'.join(self.visit(t) for t in node.dot_data)
        code = '\n'.join(self.visit(t) for t in node.dot_code)

        return (
            '.TYPES\n' + (f'{types}\n\n' if types else '\n') +
            '.DATA\n' + (f'{data}\n\n' if data else '\n') +
            f'.CODE\n{code}'
        )

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        attributes = '\n    '.join(f'attribute {x}' for x in node.attributes)
        methods = '\n    '.join(f'method {x}: {y}' for x, y in node.methods.items())

        return (
            f'type {node.name} {{' +
            (f'\n    {attributes}\n' if attributes else '') +
            (f'\n    {methods}\n' if methods else '') + '}'
        )

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        return f'{node.name} = {node.value}'

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        params = '\n    '.join(self.visit(x) for x in node.params)
        local_vars = '\n    '.join(self.visit(x) for x in node.local_vars)
        instructions = '\n    '.join(self.visit(x) for x in node.instructions)

        return (
            f'function {node.name} {{' +
            (f'\n    {params}\n' if params else '') +
            (f'\n    {local_vars}\n' if local_vars else '') +
            (f'\n    {instructions}\n' if instructions else '') + '}'
        )

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode):
        return f'PARAM {node.name}'

    @visitor.when(LocalNode)
    def visit(self, node: LocalNode):
        return f'LOCAL {node.name}'

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        return f'{node.dest} = {node.source}'

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(GetAttrNode)
    def visit(self, node: GetAttrNode):
        return f'{node.dest} = GETATTR {node.src} {node.attr}'

    @visitor.when(SetAttrNode)
    def visit(self, node: SetAttrNode):
        return f'SETATTR {node.instance} {node.attr} {node.value}'

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        return f'ARG {node.name}'

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(LoadNode)
    def visit(self, node: LoadNode):
        return f'{node.dest} = LOAD {node.msg}'

    @visitor.when(PrintNode)
    def visit(self, node: PrintNode):
        return f'PRINT {node.str_addr}'

