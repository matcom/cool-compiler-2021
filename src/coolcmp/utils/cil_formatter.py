from . import visitor, cil


class CILFormatter(object):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        types = '\n'.join(self.visit(t) for t in node.dot_types)
        data = '\n'.join(self.visit(t) for t in node.dot_data)
        code = '\n'.join(self.visit(t) for t in node.dot_code)

        return (
            '.TYPES\n' + (f'{types}\n\n' if types else '\n') +
            '.DATA\n' + (f'{data}\n\n' if data else '\n') +
            f'.CODE\n{code}'
        )

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        attributes = '\n    '.join(f'attribute {x}' for x in node.attributes)
        methods = '\n    '.join(f'method {x}: {y}' for x, y in node.methods.items())

        return (
            f'type {node.name} {{' +
            (f'\n    {attributes}\n' if attributes else '') +
            (f'\n    {methods}\n' if methods else '') + '}'
        )

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        return f'{node.name} = {repr(node.value)[1:-1]}'

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        params = '\n    '.join(self.visit(x) for x in node.params)
        local_vars = '\n    '.join(self.visit(x) for x in node.local_vars)
        instructions = '\n    '.join(self.visit(x) for x in node.instructions)

        return (
            f'function {node.name} {{' +
            (f'\n    {params}\n' if params else '') +
            (f'\n    {local_vars}\n' if local_vars else '') +
            (f'\n    {instructions}\n' if instructions else '') + '}'
        )

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        return f'PARAM {node.name}'

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        return f'LOCAL {node.name}'

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        return f'{node.dest} = {node.source}'

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        return f'{node.dest} = GETATTR {node.src} {node.attr}'

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        return f'SETATTR {node.instance} {node.attr} {node.value}'

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        return f'LABEL {node.name}'

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        return f'GOTO {node.label}'

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        return f'IF {node.condition} GOTO {node.label}'

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        return f'ARG {node.name}'

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        return f'{node.dest} = LOAD {node.msg}'

    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        return f'PRINT {node.addr}'

    @visitor.when(cil.NegationNode)
    def visit(self, node: cil.NegationNode):
        return f'{node.dest} = NOT {node.src}'

    @visitor.when(cil.ComplementNode)
    def visit(self, node: cil.ComplementNode):
        return f'{node.dest} = COMPLEMENT {node.src}'

    @visitor.when(cil.CompareNode)
    def visit(self, node: cil.CompareNode):
        return f'{node.dest} = {node.left} == {node.right}'
