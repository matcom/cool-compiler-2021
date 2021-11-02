import compiler.visitors.visitor as visitor


class PrintCILVisitor(object):
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
        methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

    @visitor.when(FunctionNode)
    def visit(self, node):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

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
        return f'{node.dest} = TYPEOF {node.type}'

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


