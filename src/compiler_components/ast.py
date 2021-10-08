class Node:
    def visit(self, tabs = 0):
        pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(child.visit( tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

    def visit(self, tabs = 0):
        node = self
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(child.visit( tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body

    def visit(self, tabs = 0):
        node = self
        params = ', '.join(':'.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) : {node.type} -> <body>'
        body = node.body.visit( tabs + 1)
        return f'{ans}\n{body}'

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr = None):
        self.id = idx
        self.type = typex
        self.expr = expr

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {node.type} <-- <expr>'
        if not self.expr is None:
            ans += "\n" + self.expr.visit(tabs+1)
        return f'{ans}'

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} : {node.type} = <expr>'
        expr = node.expr.visit( tabs + 1)
        return f'{ans}\n{expr}'

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__AssignNode: let {node.id} = <expr>'
        expr = node.expr.visit( tabs + 1)
        return f'{ans}\n{expr}'

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, type = None, args = None):
        self.obj = obj
        self.id = idx
        self.args = args

    def visit(self, tabs = 0):
        node = self
        obj = node.obj.visit( tabs + 1)
        
        if not self.args is None:
            ans = '\t' * tabs + f'\\__CallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        else:
            ans = '\t' * tabs + f'\\__CallNode: <obj>.{node.id}()'
        if not self.args is None:
            args = '\n'.join(arg.visit( tabs + 1) for arg in node.args)
        else:
            args = ""
        if self.type is None:
            return f'{ans}\n{obj}\n{args}'
        else:
            return f'@{self.type}{ans}\n{obj}\n{args}'

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

    def visit(self, tabs = 0):
        node = self
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = node.left.visit( tabs + 1)
        right = node.right.visit( tabs + 1)
        return f'{ans}\n{left}\n{right}'

class ConstantNumNode(AtomicNode):
    pass

class ConstantStringNode(AtomicNode):
    pass

class ConstantBooleanNode(AtomicNode):
    pass

class SelfNode(AtomicNode):
    pass

class DispatchNode(ExpressionNode):
    def __init__(self, expr, f, params, type = None):
        super().__init__(None)
        self.id = id
        self.f = f
        self.params = params
        self.type = type
    
    def visit(self, tabs = 0):
        node = self
        if not self.type:
            ans = '\t' * tabs + f'\\__<expr>.{self.f} <params>'
        else:
            ans = '\t' * tabs + f'\\__<expr>@{self.type}.{self.f} <params>'
        expr = node.expr.visit( tabs + 1)
        params = '\n'.join(param.visit( tabs + 1) for param in node.params)
        return f'{ans}\n{expr}\n{params}'

class VariableNode(AtomicNode):
    pass
class InstantiateNode(AtomicNode):
    def visit(self, tabs):
        node = self
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.lex}()'
class PlusNode(BinaryNode):
    pass
class MinusNode(BinaryNode):
    pass
class StarNode(BinaryNode):
    pass
class DivNode(BinaryNode):
    pass