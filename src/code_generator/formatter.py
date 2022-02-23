def get_formatter():

    class PrintVisitor(object):
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(Program)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes.values())
            dotdata = '\n'.join(f'{t}: {node.dotdata[t]}' for t in node.dotdata.keys())
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(Type)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x} : {node.methods[x]}' for x in node.methods.keys())

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(Function)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(ParamDec)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalDec)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(Assign)
        def visit(self, node):
            return f'{node.local_dest} = {node.right_expr}'

        @visitor.when(IfGoto)
        def visit(self, node):
            return f'IF {node.variable} GOTO {node.label}'
        
        @visitor.when(Label)
        def visit(self, node):
            return f'LABEL {node.label}'
        
        @visitor.when(Goto)
        def visit(self, node):
            return f'GOTO {node.label}'

        @visitor.when(UnaryOperator)
        def visit(self, node):
            return f'{node.local_dest} = {node.op} {node.expr_value}'

        @visitor.when(BinaryOperator)
        def visit(self, node):
            return f'{node.local_dest} = {node.left} {node.op} {node.right}'

        @visitor.when(Allocate)
        def visit(self, node):
            return f'{node.local_dest} = ALLOCATE {node.type}'

        @visitor.when(LoadStr)
        def visit(self, node):
            return f'{node.local_dest} = LOAD {node.msg}'

        @visitor.when(LoadInt)
        def visit(self, node):
            return f'{node.local_dest} = LOAD {node.num}'

        @visitor.when(LoadVoid)
        def visit(self, node):
            return f'{node.local_dest} = LOAD VOID'

        @visitor.when(GetAttr)
        def visit(self, node):
            return f'{node.local_dest} = GetAttr {node.instance} {node.attr} '

        @visitor.when(SetAttr)
        def visit(self, node):
            return f'SetAttr {node.instance} {node.attr} {node.value}'


        @visitor.when(TypeOf)
        def visit(self, node):
            return f'{node.local_dest} = TYPEOF {node.variable}'

        @visitor.when(Call)
        def visit(self, node):
            return f'{node.local_dest} = CALL {node.function}'

        @visitor.when(VCall)
        def visit(self, node):
            return f'{node.local_dest} = VCALL {node.dynamic_type} {node.function} '

        @visitor.when(Arg)
        def visit(self, node):
            return f'ARG {node.arg}'

        @visitor.when(Return)
        def visit(self, node):
            return f'\n RETURN {node.value if node.value is not None else ""}'

        @visitor.when(IsVoid)
        def visit(self, node):
            return f'{node.result_local} ISVOID {node.expre_value}'

        @visitor.when(Halt)
        def visit(self, node):
            return 'HALT'
        
        @visitor.when(Copy)
        def visit(self, node):
            return f'{node.local_dest} = COPY {node.type}'

        @visitor.when(Length)
        def visit(self, node):
            return f'{node.result} = LENGTH {node.variable}'

        @visitor.when(Concat)
        def visit(self, node):
            return f'{node.result} = CONCAT {node.str1}  {node.str2}'

        @visitor.when(SubStr)
        def visit(self, node):
            return f'{node.result} = SUBSTR {node.i}  {node.length}  {node.string}'
        
        @visitor.when(StringEquals)
        def visit(self, node):
            return f'{node.result} = {node.s1} = {node.s2}'

        @visitor.when(Read)
        def visit(self, node):
            return f'{node.result} = READ'

        @visitor.when(Print)
        def visit(self, node):
            return f'PRINT {node.variable}'

    printer = PrintVisitor()
    return (lambda ast: printer.visit(ast))
