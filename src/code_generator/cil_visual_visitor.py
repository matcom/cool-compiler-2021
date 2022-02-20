from utils import visitor
from cil_ast import *

def get_formatter():
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

        #.TYPE
        @visitor.when(TypeNode)
        def visit(self, node):
            attributes = '\n\t'.join(f'attribute {x}: {y}' for x, y in node.attributes)
            methods = '\n\t'.join(f'method {x}: {y}' for x, y in node.methods)

            return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

        #.DATA
        @visitor.when(DataNode)
        def visit(self, node):
            return f'{node.name} = "{node.value}"'

        #.CODE
        @visitor.when(FunctionNode)
        def visit(self, node):
            params = '\n\t'.join(self.visit(x) for x in node.params)
            localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
            instructions = '\n\t'.join(self.visit(x) for x in node.instructions)
            return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'
        #InstructionNode
        @visitor.when(ParamNode)
        def visit(self, node):
            return f'PARAM {node.name}'

        @visitor.when(LocalNode)
        def visit(self, node):
            return f'LOCAL {node.name}'

        @visitor.when(AssignNode)
        def visit(self, node):
            return f'{node.dest} = {node.source}'
        #ArithNode
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

        @visitor.when(LessNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} < {node.right}'

        @visitor.when(LessEqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} <= {node.right}'

        @visitor.when(EqualNode)
        def visit(self, node):
            return f'{node.dest} = {node.left} = {node.right}'

        @visitor.when(NotNode)
        def visit(self, node):
            return f'{node.dest} = NOT {node.expr}'
        #Attr
        @visitor.when(GetAttrNode)
        def visit(self, node):
            return f'{node.dest} = GETATTR {node.obj} {node.attr}'

        @visitor.when(SetAttrNode)
        def visit(self, node):
            return f'SETATTR {node.obj} {node.attr} = {node.value}'
        #Memory
        @visitor.when(AllocateNode)
        def visit(self, node):
            return f'{node.dest} = ALLOCATE {node.type}'

        @visitor.when(TypeOfNode)
        def visit(self, node):
            return f'{node.dest} = TYPEOF {node.obj}'
        #Jumps
        @visitor.when(LabelNode)
        def visit(self, node):
            return f'LABEL {node.label}'

        @visitor.when(GoToNode)
        def visit(self, node):
            return f'GOTO {node.label}'
        
        @visitor.when(IfGoToNode)
        def visit(self, node):
            return f'IF {node.cond} GOTO {node.label}'
        #Static Invocation
        @visitor.when(CallNode)
        def visit(self, node):
            args = '\n\t'.join(self.visit(arg) for arg in node.args)
            return f'{args}\n' + f'\t{node.dest} = CALL {node.function}'
        #Dynamic Invocation
        @visitor.when(VCallNode)
        def visit(self, node):
            args = '\n\t'.join(self.visit(arg) for arg in node.args)
            return f'{args}\n' + f'\t{node.dest} = VCALL {node.type} {node.method}'
        #Args
        @visitor.when(ArgNode)
        def visit(self, node):
            return f'ARG {node.dest}'
        #Return
        @visitor.when(ReturnNode)
        def visit(self, node):
            return f'RETURN {node.value if node.value is not None else ""}'
        #IO
        @visitor.when(LoadNode)
        def visit(self, node):
            return f'{node.dest} = LOAD {node.msg}'

        @visitor.when(LengthNode)
        def visit(self, node):
            return f'{node.dest} = LENGTH {node.arg}'

        @visitor.when(ConcatNode)
        def visit(self, node):
            return f'{node.dest} = CONCAT {node.arg1} {node.arg2}'

        @visitor.when(SubstringNode)
        def visit(self, node):
            return f'{node.dest} = SUBSTRING {node.word} {node.begin} {node.end}'

        @visitor.when(StrNode)
        def visit(self, node):
            return f'{node.dest} = STR {node.ivalue}'

        @visitor.when(ReadNode)
        def visit(self, node):
            return f'{node.dest} = READ_STR'

    printer = PrintVisitor()
    return lambda ast: printer.visit(ast)
             