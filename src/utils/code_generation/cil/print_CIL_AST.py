from utils.code_generation.cil.AST_CIL import cil_ast as nodes
import cmp.visitor as visitor

def get_formatter():

    class PrintCIL(object):
        
        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(nodes.ProgramNode)
        def visit(self, node):
            dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
            dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
            dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

            return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

        @visitor.when(nodes.TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

            return f'type {node.id} {{\n\t{attributes}\n\n\t{methods}\n}}'

        @visitor.when(nodes.DataNode)
        def visit(self, node):
            return f'{node.id} = {node.value}'

        @visitor.when(nodes.FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions if self.visit(x) != [])

            return f'function {node.id} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

        @visitor.when(nodes.ParamNode)
        def visit(self, node):
            return f'PARAM {node.id}'

        @visitor.when(nodes.LocalNode)
        def visit(self, node):
            return f'LOCAL {node.id}'

        @visitor.when(nodes.AssignNode)
        def visit(self, node):
            return f'{node.left} = {node.right}'

        @visitor.when(nodes.PlusNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} + {node.op_r}'

        @visitor.when(nodes.MinusNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} - {node.op_r}'

        @visitor.when(nodes.StarNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} * {node.op_r}'

        @visitor.when(nodes.DivNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} / {node.op_r}'

        @visitor.when(nodes.LessEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} <= {node.op_r}'

        @visitor.when(nodes.LessThanNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} < {node.op_r}'

        @visitor.when(nodes.EqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.op_l} == {node.op_r}'

        @visitor.when(nodes.GetAttrNode)
        def visit(self, node):
            return f'{node.dest} = GETATTR {node.id} {node.attr}'

        @visitor.when(nodes.SetAttrNode)
        def visit(self, node):
            return f'SETATTR {node.id} {node.attr} {node.value}'

        @visitor.when(nodes.AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(nodes.TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.id}'

        @visitor.when(nodes.StaticCallNode)
        def visit(self, node):
            return f'{node.dest} = CALL {node.function}'

        @visitor.when(nodes.DynamicCallNode)
        def visit(self, node):
            return f'{node.dest} = VCALL {node.type} {node.function}'

        @visitor.when(nodes.ArgNode)
        def visit(self, node):
            return f'ARG {node.id}'
        
        @visitor.when(nodes.IfGotoNode)
        def visit(self, node):
            return f'IF {node.if_cond} GOTO {node.label}'

        @visitor.when(nodes.LabelNode)
        def visit(self, node):
            return f'LABEL {node.label}'
        
        @visitor.when(nodes.GotoNode)
        def visit(self, node):
            return f'GOTO {node.label}'

        @visitor.when(nodes.ReturnNode)
        def visit(self, node):
            return f'RETURN {node.id if node.id is not None else ""}'

        @visitor.when(nodes.LoadNode)
        def visit(self, node):
            return f'{node.dest} = LOAD {node.msg}'

        @visitor.when(nodes.LengthNode)
        def visit(self, node):
            return f'{node.dest} = LENGTH {node.id}'

        @visitor.when(nodes.ConcatNode)
        def visit(self, node):
            return f'{node.dest} = CONCAT {node.s1} {node.s2}'

        @visitor.when(nodes.SubstringNode)
        def visit(self, node):
            return f'{node.dest} = SUBSTRING {node.s} {node.i} {node.length}'

        @visitor.when(nodes.ReadStrNode)
        def visit(self, node):
            return f'{node.dest} = READSTR'
        
        @visitor.when(nodes.PrintStrNode)
        def visit(self, node):
            return f'PRINT {node.value}'
        
        @visitor.when(nodes.ErrorNode)
        def visit(self, node):
            return f'ERROR {node.data_node}'
        
        @visitor.when(nodes.TypeNameNode)
        def visit(self, node):
            return f'{node.dest} = TYPENAME {node.type}'

        @visitor.when(nodes.NameNode)
        def visit(self, node):
            return f'{node.dest} = NAME {node.id}'

        @visitor.when(nodes.AbortNode)
        def visit(self, node):
            return f'ABORT'
        
        @visitor.when(nodes.CopyNode)
        def visit(self, node):
            return f'{node.dest} = COPY {node.copy}'
        
        @visitor.when(nodes.ReadIntNode)
        def visit(self, node):
            return f'{node.dest} = READINT'

        @visitor.when(nodes.PrintIntNode)
        def visit(self, node):
            return f'PRINT {node.value}'
        
        @visitor.when(nodes.VoidNode)
        def visit(self, node):
            return 'VOID'
        
    printer = PrintCIL()
    return (lambda ast: printer.visit(ast))
    