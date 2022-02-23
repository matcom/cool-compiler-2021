class Node:
    def visit(self, tabs = 0):
        self.line = -1

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = -1
    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(child.visit( tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = -1

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
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        params = ', '.join(':'.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) : {node.type} -> <body>'
        body = node.body.visit( tabs + 1)
        self.line = -1
        return f'{ans}\n{body}'

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr = None):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.line = -1

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
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} : {node.type} = <expr>'
        expr = node.expr.visit( tabs + 1)
        return f'{ans}\n{expr}'

class AssignNode(AtomicNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__AssignNode: let {node.id} = <expr>'
        expr = node.expr.visit( tabs + 1)
        return f'{ans}\n{expr}'

class IsVoidNode(AtomicNode):
    def __init__(self, expr):
        self.expr = expr
        self.line = -1
    
    def visit(self, tabs = 0):
        ans = '\t'*tabs + "\\__IsVoid <expr>"
        return ans + '\n' + '\t'*(tabs+1) + self.expr.visit()

class NotNode(AtomicNode):
    def __init__(self, expr):
        self.expr = expr
        self.line = -1
    
    def visit(self, tabs = 0):
        ans = '\t'*tabs + "\\__NOT <expr>"
        return ans + '\n' + '\t'*(tabs+1) + self.expr.visit()

class NhanharaNode(AtomicNode):
    def __init__(self, expr):
        self.expr = expr
        self.line = -1
    
    def visit(self, tabs = 0):
        ans = '\t'*tabs + "\\__~ <expr>"
        return ans + '\n' + '\t'*(tabs+1) + self.expr.visit()
        

class CallNode(AtomicNode):
    def __init__(self, obj, idx, args = None, type = None):
        self.obj = obj
        self.id = idx
        if args is None:
            self.args = []
        else:
            self.args = args
        self.type = type
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        if not self.obj is None:
            obj = node.obj.visit( tabs + 1)
        else:
            obj = ""
        if not self.type is None:
            arroba = f'@{self.type}'
        else:
            arroba = ""

        if not self.args is None:
            ans = '\t' * tabs + f'\\__CallNode: <obj>{arroba}.{node.id}(<expr>, ..., <expr>)'
        else:
            ans = '\t' * tabs + f'\\__CallNode: <obj>{arroba}.{node.id}()'
        if not self.args is None:
            args = '\n'.join(arg.visit( tabs + 1) for arg in node.args)
        else:
            args = ""
        
        return f'{ans}\n{obj}\n{args}'
        
class IfNode(AtomicNode):
    def __init__(self, if_c, then_c, else_c):
        self.if_c = if_c
        self.then_c = then_c
        self.else_c = else_c
        self.line = -1
        
    def visit(self, tabs = 0):
        node = self
        ans = '\t'*tabs + 'if <expr> then <expr> else <expr> fi'
        ans += "\n" + '\t'*(tabs +1) + "IF: " + self.if_c.visit()
        ans += "\n" + '\t'*(tabs +1) + "then: " + self.then_c.visit()
        ans += "\n" + '\t'*(tabs +1) + "else: " + self.else_c.visit()
        return ans

class WhileNode(AtomicNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.line = -1
        
    def visit(self, tabs = 0):
        node = self
        ans = '\t'*tabs + 'while <expr> loop <expr> pool'
        ans += "\n" + '\t'*(tabs +1) + "condition: " + self.if_c.visit()
        ans += "\n" + '\t'*(tabs +1) + "body: " + self.then_c.visit()
        
        return ans

class BlockNode(AtomicNode):
    def __init__(self, expr_list):
        self.expr_list = expr_list
        self.line = -1

    def visit(self, tabs = 0):
        ans = '\t'*tabs + " {<expr>; .... <expr>;}\n"
        exprs = '\n'.join(param.visit( tabs + 1) for param in self.expr_list)
        return ans+exprs

class LetNode(AtomicNode):
    def __init__(self, list_decl, expr):
        self.list_decl = list_decl
        self.expr = expr
        self.line = -1

    def visit(self, tabs = 0):
        ans = '\t'*tabs + " LET <decl>, <decl> ... <decl> in <expr>\n "
        decl = '\n'.join('\t'*(tabs+1) + "decl: " + param.visit()  for param in self.list_decl)
        expr = "\n" + "IN" + self.expr.visit(tabs+1)
        return ans+decl+expr

class CaseNode(AtomicNode):
    def __init__(self, expr, list_case):
        self.list_case = list_case
        self.expr = expr
        self.line = -1

    def visit(self, tabs = 0):
        ans = '\t'*tabs + "\\__Case <expre> in <list-assign> esac"
        expr = '\t'*(tabs+1) + self.expr.visit()
        l = '\n'.join('\t'*(tabs+1) + "list_case[i]: " +  e.visit() for e in self.list_case)
        return ans+"\n"+expr+"\n" +l
        



class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.line = -1

    def visit(self, tabs = 0):
        node = self
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = node.left.visit( tabs + 1)
        right = node.right.visit( tabs + 1)
        return f'{ans}\n{left}\n{right}'

class ArithmeticNode(BinaryNode):
    pass

class ConstantNumNode(AtomicNode):
    pass

class ConstantStringNode(AtomicNode):
    pass

class ConstantBooleanNode(AtomicNode):
    pass

class SelfNode(AtomicNode):
    pass

class DispatchNode(ExpressionNode):
    def __init__(self, expr, f, params, typex = None):
        self.id = f
        self.expr = expr
        self.f = f
        if params is None:
            self.params = []
        else:
            self.params = params
        self.typex = typex
        self.line = -1
    
    def visit(self, tabs = 0):
        node = self
        if not self.typex:
            ans = '\t' * tabs + f'\\__<expr>.{self.f} <params>'
        else:
            ans = '\t' * tabs + f'\\__<expr>@{self.typex}.{self.f} <params>'
        expr = node.expr.visit( tabs + 1)
        params = '\n'.join(param.visit( tabs + 1) for param in node.params)
        return f'{ans}\n{expr}\n{params}'

class VariableNode(AtomicNode):
    pass
class InstantiateNode(AtomicNode):
    def visit(self, tabs):
        node = self
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.lex}()'
class PlusNode(ArithmeticNode):
    pass
class MinusNode(ArithmeticNode):
    pass
class StarNode(ArithmeticNode):
    pass
class DivNode(ArithmeticNode):
    pass

class MinorNode(ArithmeticNode):
    pass
class MinorEqualsNode(BinaryNode):
    pass
class EqualsNode(BinaryNode):
    pass