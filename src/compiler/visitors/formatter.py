import compiler.visitors.visitor as visitor
from ..cmp.ast import ProgramNode, ClassDeclarationNode, FuncDeclarationNode
from ..cmp.ast import AttrDeclarationNode, AssignNode, CallNode
from ..cmp.ast import CaseNode, BlockNode, LoopNode, ConditionalNode, LetNode, InstantiateNode
from ..cmp.ast import UnaryNode, BinaryNode, AtomicNode

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs=0):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = '' if node.parent is None else f"inherits {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(' : '.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.type} {{ <expr> }}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type}'
        if node.expr is not None:
            expr = self.visit(node.expr, tabs + 1)
            ans = f'{ans} <- <expr>\n{expr}'
        return f'{ans}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} <- <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        cast = '' if node.type is None else f'@{node.type}'
        ans = '\t' * tabs + f'\\__CallNode: <obj>{cast}.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(CaseNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CaseNode: case <expr> of [ <branch>, ..., <branch> ]'
        expr = self.visit(node.expr, tabs + 1)
        branches = []
        for branch in node.branch_list:
           branches.append('\t' * (tabs + 1) + f'{branch[0]} : {branch[1]} => <expr>\n{self.visit(branch[2], tabs + 2)}')
        branches = '\n'.join(branches)
        return f'{ans}\n{expr}\n{branches}'

    @visitor.when(BlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BlockNode: {{ <expr> ; ... ; <expr> ; }}'
        exprs = '\n'.join(self.visit(expr, tabs + 1) for expr in node.expr_list)
        return f'{ans}\n{exprs}'

    @visitor.when(LoopNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LoopNode: while <expr> loop <expr> pool'
        cond = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{cond}\n{body}'

    @visitor.when(ConditionalNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ConditionalNode: if <expr> then <expr> else <expr> fi'
        cond = self.visit(node.condition, tabs + 1)
        then_body = self.visit(node.then_body, tabs + 1)
        else_body = self.visit(node.else_body, tabs + 1)
        return f'{ans}\n{cond}\n{then_body}\n{else_body}'

    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetNode: let <iden_list> in <expr>'
        expr = self.visit(node.body, tabs + 1)
        iden_list = []
        for item in node.id_list:
            iden = '\t' * (tabs + 1) + f'{item[0]} : {item[1]}'
            if item[2] is not None:
                iden = f'{iden} <- <expr>\n{self.visit(item[2], tabs + 2)}'
            iden_list.append(iden)
        iden_list = '\n'.join(iden_list)
        return f'{ans}\n{iden_list}\n{expr}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        expr = self.visit(node.expr, tabs + 1)
        return '\t' * tabs + f'\\__ {node.__class__.__name__} <expr>\n{expr}'
    
    @visitor.when(InstantiateNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.lex}'