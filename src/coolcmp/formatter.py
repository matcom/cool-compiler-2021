from coolcmp import visitor
from coolcmp.ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, LetNode, \
    AssignNode, BlockNode, ConditionalNode, WhileNode, CaseNode, CallNode, BinaryNode, AtomicNode, InstantiateNode, \
    UnaryNode


class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, tabs: int = 0):
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '  ' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type}'
        return f'{ans}'

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, tabs: int = 0):
        params = ', '.join(f'{param.id}: {param.type}' for param in node.params)
        ans = '  ' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {node.return_type} -> <body>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(LetNode)
    def visit(self, node: LetNode, tabs: int = 0):
        declarations = []
        for declaration_node in node.declarations:
            _id = declaration_node.id
            _type = declaration_node.type
            _expr = declaration_node.expr
            if _expr is not None:
                declarations.append(
                    '  ' * tabs +
                    f'\\__VarDeclarationNode: {_id}: {_type} <-\n{self.visit(_expr, tabs + 1)}'
                )
            else:
                declarations.append('  ' * tabs +
                                    f'\\__VarDeclarationNode: {_id} : {_type}')
        declarations = '\n'.join(declarations)
        ans = '  ' * tabs + f'\\__LetNode:  let'
        expr = self.visit(node.expr, tabs + 2)
        return f'{ans}\n {declarations}\n' + '  ' * (tabs + 1) + 'in\n' + f'{expr}'

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__AssignNode: {node.id} <- <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__BlockNode:'
        body = '\n'.join(
            self.visit(child, tabs + 1) for child in node.expressions)
        return f'{ans}\n{body}'

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, tabs: int = 0):
        ifx = self.visit(node.if_expr, tabs + 2)
        then = self.visit(node.then_expr, tabs + 2)
        elsex = self.visit(node.else_expr, tabs + 2)

        return '\n'.join([
            '  ' * tabs +
            f'\\__ConditionalNode: if <expr> then <expr> else <expr> fi',
            '  ' * (tabs + 1) + f'\\__if \n{ifx}',
            '  ' * (tabs + 1) + f'\\__then \n{then}',
            '  ' * (tabs + 1) + f'\\__else \n{elsex}',
        ])

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, tabs: int = 0):
        condition = self.visit(node.condition, tabs + 2)
        body = self.visit(node.body, tabs + 2)

        return '\n'.join([
            '  ' * tabs + f'\\__WhileNode: while <expr> loop <expr> pool',
            '  ' * (tabs + 1) + f'\\__while \n{condition}',
            '  ' * (tabs + 1) + f'\\__loop \n{body}',
        ])

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, tabs: int = 0):
        cases = []
        for _id, _type, _expr in node.cases:
            expr = self.visit(_expr, tabs + 3)
            cases.append('  ' * tabs +
                         f'\\__CaseNode: {_id} : {_type} =>\n{expr}')
        expr = self.visit(node.expr, tabs + 2)
        cases = '\n'.join(cases)

        return '\n'.join([
            '  ' * tabs +
            f'\\__CaseNode: case <expr> of [<case> ... <case>] esac',
            '  ' * (tabs + 1) + f'\\__case \n{expr} of',
        ]) + '\n' + cases

    @visitor.when(CallNode)
    def visit(self, node: CallNode, tabs: int = 0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '  ' * tabs + f'\\__CallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode, tabs: int = 0):
        return '  ' * tabs + f'\\__{node.__class__.__name__}: {node.lex}'

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, tabs: int = 0):
        return '  ' * tabs + f'\\__InstantiateNode: new {node.lex}()'

    @visitor.when(UnaryNode)
    def visit(self, node: UnaryNode, tabs: int = 0):
        ans = '  ' * tabs + f'\\__{node.__class__.__name__}: <epxr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
