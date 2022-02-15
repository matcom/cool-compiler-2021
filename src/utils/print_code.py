import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes

class PrintCode:
    @visitor.on('node')
    def visit(self, node, tabs = 0):
        pass

    @visitor.when(nodes.ProgramNode)
    def visit(self, node, tabs = 0):
        return '\n'.join(self.visit(dec, tabs) for dec in node.declarations)


    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self, node, tabs = 0):
        parent = '' if node.parent is None else f'inherits {node.parent}'
        ans = '\t' * tabs + f'class {node.id} {parent}'
        features = '\n'.join(self.visit(feat, tabs + 1) for feat in node.features)
        return f'{ans} {{\n{features}\n}};'


    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self, node, tabs = 0):
        expr = '' if node.expr is None else f'<- {self.visit(node.expr)}'
        return '\t' * tabs + f'{node.id}: {node.type} {expr};'
    

    @visitor.when(nodes.MethDeclarationNode)
    def visit(self, node, tabs = 0):
        params = ', '.join(': '.join(param) for param in node.params)
        ans = '\t' * tabs + f'{node.id} ({params}): {node.type}'
        body = self.visit(node.body, tabs + 1)
        return f'{ans} {{\n{body}\n' + '\t' * tabs + '};'
    

    @visitor.when(nodes.AssignNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{node.id} <- {self.visit(node.expr)}'


    @visitor.when(nodes.CallNode)
    def visit(self, node, tabs = 0):
        obj = '' if node.obj is None else f'{self.visit(node.obj)}' if node.type else f'{self.visit(node.obj)}.'
        args = ', '.join(self.visit(arg) for arg in node.args)
        typex = '' if node.type is None else f'@ {node.type}'
        return '\t' * tabs + f'{obj}{typex}{node.id} ({args})'

    
    @visitor.when(nodes.IfThenElseNode)
    def visit(self, node, tabs = 0):
        ifx = self.visit(node.if_expr)
        then = self.visit(node.then_expr, tabs + 1)
        elsex = self.visit(node.else_expr, tabs + 1)

        return '\t' * tabs + f'if {ifx}\n' + '\t' * tabs + f'then\n{then}\n' + '\t' * tabs + f'else\n{elsex}\n' + '\t' * tabs + 'fi'


    @visitor.when(nodes.WhileNode)
    def visit(self, node, tabs = 0):
        ans = f'while {self.visit(node.conditional_expr)} loop'
        body = self.visit(node.loop_expr, tabs + 1)

        return '\t' * tabs + f'{ans}\n{body}\n' + '\t' * tabs + 'pool'


    @visitor.when(nodes.BlockNode)
    def visit(self, node, tabs = 0):
        expr_list = ';\n'.join(self.visit(expr, tabs + 1) for expr in node.expr_list)
        return '\t' * tabs + f'{{\n{expr_list};\n' + '\t' * tabs + '}'


    @visitor.when(nodes.LetNode)
    def visit(self, node, tabs = 0):
        identifiers = []
        for idx, typex, id_expr in node.identifiers:
            if id_expr:
                identifiers.append(f'{idx}: {typex} <- {self.visit(id_expr)}')
            else:
                identifiers.append(f'{idx}: {typex}')
        
        identifiers = (',\n' + '\t' * (tabs + 1)).join(identifiers)
        return '\t' * tabs + f'let {identifiers} in\n{self.visit(node.in_expr, tabs + 1)}'
    

    @visitor.when(nodes.CaseNode)
    def visit(self, node, tabs = 0):
        predicate = self.visit(node.predicate)
        branches = '\n'.join(f'\t' * (tabs + 1) + f'{idx}: {typex} =>\n{self.visit(expr, tabs + 2)};' for idx, typex, expr in node.branches)

        return '\t' * tabs + f'case {predicate} of \n{branches}\n' + '\t' * tabs + 'esac'

    @visitor.when(nodes.NotNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'not {self.visit(node.expr)}'


    @visitor.when(nodes.ConstantNumNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{node.lex}' 
    
    @visitor.when(nodes.ConstantBoolNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{node.lex}'

    @visitor.when(nodes.ConstantStringNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{node.lex}'

    @visitor.when(nodes.VariableNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{node.lex}'


    @visitor.when(nodes.InstantiateNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'(new {node.lex})'

    @visitor.when(nodes.IsVoidNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'isvoid {self.visit(node.lex)}'
    
    @visitor.when(nodes.ComplementNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'~ {self.visit(node.lex)}'


    @visitor.when(nodes.PlusNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} + {self.visit(node.right)}'

    @visitor.when(nodes.MinusNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} - {self.visit(node.right)}'
    
    @visitor.when(nodes.StarNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} * {self.visit(node.right)}'

    @visitor.when(nodes.DivNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} / {self.visit(node.right)}'

    @visitor.when(nodes.LessThanNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} < {self.visit(node.right)}'
    
    @visitor.when(nodes.LessEqualNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} <= {self.visit(node.right)}'
    
    @visitor.when(nodes.EqualNode)
    def visit(self, node, tabs = 0):
        return '\t' * tabs + f'{self.visit(node.left)} = {self.visit(node.right)}'