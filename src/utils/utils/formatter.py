import utils.ast_nodes as ast
import utils.visitor as visitor
from utils.semantic import Scope
from utils.code_generation import NullNode 


class CodeBuilder:
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, tabs: int = 0):
        return '\n\n'.join(self.visit(child, tabs) for child in node.class_list)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, tabs: int = 0):
        parent = '' if node.parent is None else f"inherits {node.parent} "
        return (f'class {node.name} {parent}{{\n' +
                '\n\n'.join(self.visit(child, tabs + 1) for child in node.data) +
                '\n}')

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, tabs: int = 0):
        expr = f' <- {self.visit(node.expr, 0)}' if node.expr is not None else ''
        return '    ' * tabs + f'{node.name}: {node._type}{expr};'

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, tabs: int = 0):
        params = ', '.join(': '.join([param.name, param.type]) for param in node.params)
        ans = '    ' * tabs + f'{node.name} ({params}): {node.type}'
        body = self.visit(node.expr, tabs + 1)
        return f'{ans} {{\n{body}\n    }};'

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, tabs: int = 0):
        declarations = []
        for _id, _type, _expr in node.declaration:
            if _expr is not None:
                declarations.append(f'{_id}: {_type} <- {self.visit(_expr)}')
            else:
                declarations.append(f'{_id} : {_type}')
        declarations = (',\n' + '    ' * (tabs + 1)).join(declarations)
        return '    ' * tabs + f'let {declarations} in\n{self.visit(node.expr, tabs + 1)}'

    @visitor.when(ast.ParamNode)
    def visit(self, node: ast.ParamNode, tabs: int = 0):
        return '    ' * tabs + f'({node.name}: {node.type.name})'

    @visitor.when(ast.ExprParNode)
    def visit(self, node: ast.ExprParNode, tabs: int = 0):
        return f"({self.visit(node.expr, tabs)})"
    
    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, tabs: int = 0):
        return f'Isvoid({self.visit(node.expr, tabs)})'

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, tabs: int = 0):
        return '    ' * tabs + f'{node.idx} <- {self.visit(node.expr, tabs)}'

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, tabs: int = 0):
        body = ';\n'.join(self.visit(child, tabs + 1) for child in node.expr)
        return '    ' * tabs + f'{{\n{body};\n' + '    ' * tabs + '}'

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, tabs: int = 0):
        ifx = self.visit(node.if_expr)
        then = self.visit(node.then_expr, tabs + 1)
        elsex = self.visit(node.else_expr, tabs + 1)

        return ('    ' * tabs + f'if {ifx}\n' +
                '    ' * tabs + f'then\n{then}\n' +
                '    ' * tabs + f'else\n{elsex}\n' +
                '    ' * tabs + 'fi')

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, tabs: int = 0):
        condition = self.visit(node.cond, 0)
        body = self.visit(node.data, tabs + 1)

        return '    ' * tabs + f'while {condition} loop\n {body}\n' + '    ' * tabs + 'pool'

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, tabs: int = 0):
        cases = []
        for _id, _type, _expr in node.params:
            expr = self.visit(_expr, tabs + 2)
            cases.append('    ' * (tabs + 1) + f'{_id} : {_type} =>\n{expr};')
        expr = self.visit(node.expr)
        cases = '\n'.join(cases)

        return '    ' * tabs + f'case {expr} of \n{cases}\n' + '    ' * tabs + 'esac'

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, tabs: int = 0):
        obj = f'{self.visit(node.atom, 0)}.' if node.atom is not None else ''
        str_params = [self.visit(arg, 0) for arg in node.exprlist]
        return '    ' * tabs + f'{obj}{node.idx}({", ".join(str_params)})'

    @visitor.when(ast.BinaryNode)
    def visit(self, node: ast.BinaryNode, tabs: int = 0):
        left = self.visit(node.left) if isinstance(node.left, ast.BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        return f'{left} {node.operation} {right}'

    
    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, tabs: int = 0):
        return f'~ {self.visit(node.expr, tabs)}'

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, tabs: int = 0):
        return f'not {self.visit(node.expr, tabs)}'

    @visitor.when(NullNode)
    def visit(self, node: NullNode, tabs):
        return 'NULL'

    @visitor.when(ast.AtomicNode)
    def visit(self, node: ast.AtomicNode, tabs: int = 0):
        lex = node.lex
        return f'{lex}'

    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, tabs: int = 0):
        return '    ' * tabs + f'(new {node.type})'

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, tabs: int = 0):
        return '    ' * tabs + f'{node.lex}'


class PrintingScope:
    
    def printing(self, scope: Scope, tabs=0):
        print(tabs * '    ', "parent: ", scope.parent)
        print(tabs * '    ', "variables locales:", type(scope.local_variable), scope.local_variable)
        
        if scope.children:
            print(tabs * '    ', f'childrens: ({len(scope.children)})')
            for item in scope.children:
                self.printing(item, tabs+1)
            
        return "end"
    
class Formatter:
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, tabs: int = 0):
        ans = '    ' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.class_list)
        return f'{ans}\n{statements}'

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, tabs: int = 0):
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '    ' * tabs + f'\\__ClassDeclarationNode: class {node.name} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.data)
        return f'{ans}\n{features}'

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, tabs: int = 0):
        ans = '    ' * tabs + f'\\__AttrDeclarationNode: {node.name} : {node._type}'
        return f'{ans}'

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, tabs: int = 0):
        params = ', '.join(':'.join(param) for param in node.params) if node.params is not None else ''
        ans = '    ' * tabs + f'\\__FuncDeclarationNode: {node.name}({params}) : {node.type if node.type is not None else ""} -> <body>'
        body = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, tabs: int = 0):
        declarations = []
        for _id, _type, _expr in node.declaration:
            if _expr is not None:
                declarations.append('    ' * tabs + f'\\__VarDeclarationNode: {_id}: {_type} <-\n{self.visit(_expr, tabs + 1)}')
            else:
                declarations.append('    ' * tabs + f'\\__VarDeclarationNode: {_id} : {_type}')

        declarations = '\n'.join(declarations)
        ans = '    ' * tabs + f'\\__LetNode:  let'
        expr = self.visit(node.expr, tabs + 2)
        return f'{ans}\n {declarations}\n' + '    ' * (tabs + 1) + 'in\n' + f'{expr}'

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, tabs: int = 0):
        ans = '    ' * tabs + f'\\__AssignNode: {node.idx} <- <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, tabs: int = 0):
        ans = '    ' * tabs + f'\\__BlockNode:'
        body = '\n'.join(self.visit(child, tabs + 1) for child in node.expr)
        return f'{ans}\n{body}'

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, tabs: int = 0):
        ifx = self.visit(node.if_expr, tabs + 2)
        then = self.visit(node.then_expr, tabs + 2)
        elsex = self.visit(node.else_expr, tabs + 2)

        return '\n'.join([
            '    ' * tabs + f'\\__IfThenElseNode: if <expr> then <expr> else <expr> fi',
            '    ' * (tabs + 1) + f'\\__if \n{ifx}',
            '    ' * (tabs + 1) + f'\\__then \n{then}',
            '    ' * (tabs + 1) + f'\\__else \n{elsex}',
        ])

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, tabs: int = 0):
        condition = self.visit(node.cond, tabs + 2)
        body = self.visit(node.data, tabs + 2)

        return '\n'.join([
            '    ' * tabs + f'\\__WhileNode: while <expr> loop <expr> pool',
            '    ' * (tabs + 1) + f'\\__while \n{condition}',
            '    ' * (tabs + 1) + f'\\__loop \n{body}',
        ])

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, tabs: int = 0):
        cases = []
        for _id, _type, _expr in node.params:
            expr = self.visit(_expr, tabs + 3)
            cases.append('    ' * tabs + f'\\__CaseNode: {_id} : {_type} =>\n{expr}')
        expr = self.visit(node.expr, tabs + 2)
        cases = '\n'.join(cases)

        return '\n'.join([
            '    ' * tabs + f'\\__SwitchCaseNode: case <expr> of [<case> ... <case>] esac',
            '    ' * (tabs + 1) + f'\\__case \n{expr} of',
        ]) + '\n' + cases

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, tabs: int = 0):
        obj = self.visit(node.atom, tabs + 1)
        ans = '    ' * tabs + f'\\__CallNode: <obj>.{node.idx}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.exprlist)
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(ast.BinaryNode)
    def visit(self, node: ast.BinaryNode, tabs: int = 0):
        ans = '    ' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(ast.AtomicNode)
    def visit(self, node: ast.AtomicNode, tabs: int = 0):
        return '    ' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, tabs: int = 0):
        return '    ' * tabs + f'\\__ NewNode: new {node.lex}()'
