import visitors.visitor as visitor
from cool_ast.cool_ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode, LetInNode
from cool_ast.cool_ast import AssignNode, ChunkNode, ConditionalNode, WhileNode, SwitchCaseNode, CallNode
from cool_ast.cool_ast import PlusNode, MinusNode, StarNode, DivNode, LeqNode, LessNode, EqualNode, NotNode
from cool_ast.cool_ast import ComplementNode, IsVoidNode, AtomicNode, InstantiateNode, BinaryNode

class Depicter(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs = 0):
        return '\n\n'.join(self.visit(dec, tabs) for dec in node.declarations)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs = 0):
        par = '' if node.parent is None else f"inherits {node.parent}"
        depiction = f'class {node.id} {par} {{\n' + '\n'.join(self.visit(feature, tabs + 1) for feature in node.features) + '\n};'
        return (depiction)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs = 0):
        value = f' <- {self.visit(node.value, 0)}' if node.value else ''
        depiction = '    ' * tabs + f'{node.id}: {node.type}{value}'
        return depiction

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs = 0):
        params = ', '.join(': '.join(param) for param in node.params)
        header = '    ' * tabs + f'{node.id} ({params}): {node.type}'
        body = self.visit(node.body, tabs + 1)
        depiction = f'{header} {{\n{body}\n    }};'
        return depiction

    @visitor.when(ChunkNode)
    def visit(self, node, tabs = 0):
        exprs = ''
        for smth in node.chunk:
            to_concat = self.visit(smth, tabs + 1) 
            exprs += to_concat
            exprs += ';\n'
        depiction = '    ' * tabs + f'{{\n{exprs}\n' + '    ' * tabs + '};'
        return depiction

    @visitor.when(AssignNode)
    def visit(self, node, tabs = 0):
        depiction = '    ' * tabs + f'{node.id} <- {self.visit(node.expr)}'
        return depiction

    @visitor.when(ConditionalNode)
    def visit(self, node, tabs = 0):
        if_expr = self.visit(node.ifChunk, 0)#
        then_expr = self.visit(node.thenChunk, tabs + 1)
        else_expr = self.visit(node.elseChunk, tabs + 1)
        # depiction = '    ' * tabs + f'if {if_expr}\n' + '    ' * tabs + f'then\n{then_expr}\n' + '    ' * tabs + f'else\n{else_expr}\n' + '    ' * tabs + 'fi'
        depiction = '    ' * tabs + f'if {if_expr} then\n' + f'{then_expr}\n' + '    ' * tabs + f'else\n{else_expr}\n' + '    ' * tabs + 'fi'        
        return depiction

    @visitor.when(LetInNode)
    def visit(self, node, tabs = 0):
        decls = []
        for decl in node.decl_list:
            _id = decl.id
            _type = decl.type 
            _val = decl.expr
            if _val is not None:
                decls.append(f'{_id}: {_type} <- {self.visit(_val)}')
            else:
                decls.append(f'{_id} : {_type}')
        decls = ('\n' + '    ' * (tabs + 1)).join(decls)
        depiction = '    ' * tabs + f'let {decls} in \n{self.visit(node.expression, tabs + 1)}'
        return depiction

    @visitor.when(WhileNode)
    def visit(self, node, tabs = 0):
        _cond = self.visit(node.condition, 0)
        _loop = self.visit(node.loopChunk, tabs + 1)
        depiction = '    ' * tabs + f'while {_cond} loop\n {_loop}\n' + '    ' * tabs + 'pool'
        return depiction
    
    @visitor.when(SwitchCaseNode)
    def visit(self, node, tabs = 0):
        _case_list = []
        for case in node.case_list:
            _id = case[0]
            _type = case[1]
            _expr = case[2]
            expr = self.visit(_expr, tabs + 2)
            _case_list.append('    ' * (tabs + 1) + f'{_id} : {_type} =>\n{expr};')
        expr = self.visit(node.expr)
        _case_list = '\n'.join(_case_list)
        depiction = '    ' * tabs + f'case {expr} of \n{_case_list}\n' + '    ' * tabs + 'esac'
        return depiction
    
    @visitor.when(CallNode)
    def visit(self, node, tabs = 0):
        _id = f'{self.visit(node.obj, 0)}.' if node.obj is not None else ''
        depiction = '    ' * tabs + f'{_id}{node.method}({", ".join(self.visit(arg, 0) for arg in node.args)})'
        return depiction

    @visitor.when(NotNode)
    def visit(self, node, tabs = 0):
        expr = self.visit(node.expression) 
        depiction = f'Not {expr}'
        return depiction
    
    @visitor.when(InstantiateNode)
    def visit(self, node, tabs = 0):
        depiction = '  ' * tabs + f'new {node.lex}'
        return depiction

    @visitor.when(IsVoidNode)
    def visit(self, node, tabs = 0):
        expr = self.visit(node.method)
        depiction = f'IsVoid({expr})'
        return depiction

    @visitor.when(ComplementNode)
    def visit(self, node, tabs = 0):
        expr = self.visit(node.expr) 
        depiction = f'~ {expr}'  
        return depiction

    @visitor.when(AtomicNode)
    def visit(self, node, tabs = 0):
        depiction = '    ' * tabs + f'{node.lex}'
        return depiction

    @visitor.when(EqualNode)
    def visit(self, node, tabs = 0):
        l = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        r = self.visit(node.right)
        depiction = f'{l} = {r}'
        return depiction
    
    @visitor.when(PlusNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} + {right}'
        return depiction

    @visitor.when(MinusNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} - {right}'
        return depiction

    @visitor.when(StarNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} * {right}'
        return depiction

    @visitor.when(DivNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} / {right}'
        return depiction

    @visitor.when(LessNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} < {right}'
        return depiction

    @visitor.when(LeqNode)
    def visit(self, node, tabs = 0):
        left = self.visit(node.left) if isinstance(node.left, BinaryNode) else self.visit(node.left, tabs)
        right = self.visit(node.right)
        depiction = f'{left} <= {right}'
        return depiction

