from .ASTs import ast0_factory_return as AST_init
from .ASTs import ast1_create_type_return as AST_result
from . import visitor

class ASTPrint:
    def __init__(self, error) -> None:
        self.cool_error = error
    
    @visitor.on("node")
    def visit(self, node, str):
        pass

    @visitor.when(AST_init.Program)
    #@visitor.result(AST_result.Program)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Program, tabs = 0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.class_list)
        return f'{ans}\n{statements}'
    
    @visitor.when(AST_init.CoolClass)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.CoolClass, tabs):
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.name} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.feature_list)
        return f'{ans}\n{features}'
    
    @visitor.when(AST_init.AtrDef)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.AtrDef, tabs):
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.name} : {node.type}'
        expr = '' if node.expr is None else self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(AST_init.FuncDef)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.FuncDef, tabs):
        params = ', '.join(':'.join(param) for param in node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.name}({params}) : {node.return_type} -> <body>'
        body = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(AST_init.CastingDispatch)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.CastingDispatch, tabs):
        ans = '\t' * tabs + f'\\__CastingDispatch: {node.type} @ {node.id} \\__Object:'
        obj = self.visit(node.expr, tabs + 1)
        param = '\t' * tabs + f'\\__Params:'
        params = '\n'.join( self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{obj}\n{param}\n{params}'

    @visitor.when(AST_init.Dispatch)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Dispatch, tabs):
        ans = '\t' * tabs + f'\\__Dispatch: {node.id} \\__Object:'
        obj = self.visit(node.expr, tabs + 1)
        param = '\t' * tabs + f'\\__Params:'
        params = '\n'.join( self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{obj}\n{param}\n{params}'

    @visitor.when(AST_init.StaticDispatch)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.StaticDispatch, tabs):
        ans = '\t' * tabs + f'\\__StaticDispatch: {node.id} \\__Params:'
        params = '\n'.join( self.visit(param, tabs + 1) for param in node.params)
        return f'{ans}\n{params}'

    @visitor.when(AST_init.Assing)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Assing, tabs):
        ans = '\t' * tabs + f'\\__AssignNode: {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'

    @visitor.when(AST_init.IfThenElse)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.IfThenElse, tabs):
        _if = '\t' * tabs + f'\\__IfNode:'
        cond = self.visit(node.condition, tabs + 1)
        then = '\t' * tabs + f'\\__Then:'
        then_expr = self.visit(node.then_expr, tabs + 1)
        _else = '\t' * tabs + f'\\__Else:'
        else_expr = self.visit(node.else_expr, tabs + 1)
        return f'{_if}\n{cond}\n{then}\n{then_expr}\n{_else}\n{else_expr}'


    @visitor.when(AST_init.While)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.While, tabs):
        _while = '\t' * tabs + f'\\__WhileNode:'
        cond = self.visit(node.condiction, tabs + 1)
        loop = '\t' * tabs + f'\\__Loop:'
        body = self.visit(node.loop_expr, tabs + 1)
        pool = '\t' * tabs + f'\\__Pool:'
        return f'{_while}\n{cond}\n{loop}\n{body}\n{pool}'

    @visitor.when(AST_init.Block)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Block, tabs):
        block = '\t' * tabs + f'\\__BlocksNode:'
        _list = '\n'.join(self.visit(expr, tabs + 1 ) for expr in node.expr_list)
        return f'{block}\n{_list}'

    @visitor.when(AST_init.LetIn)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.LetIn, tabs):
        ans = '\t' * tabs + f'\\__LetNode:'
        var_list = '\n'.join('\t' * (tabs + 1) + idx + " : " + typ + "\n" + self.visit(exp, tabs + 1) for idx, typ, exp in node.assing_list)
        expr = '\t' * tabs + f'\\__In:\n' + self.visit(node.expr, tabs + 2)
        return f'{ans}\n{var_list}\n{expr}'

    @visitor.when(AST_init.Case)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Case, tabs):
        case = '\t' * tabs + f'\\__CaseNode:'
        expr = self.visit(node.expr, tabs + 1)
        _list = '\t' * tabs + f'\\__OptionsList:'
        list_case = '\n'.join(self.visit(case, tabs + 1) for case in node.case_list)
        return f'{case}\n{expr}\n{_list}\n{list_case}'
        

    @visitor.when(AST_init.Sum)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Sum, tabs):
        ans = '\t' * tabs + f'\\__<expr> Sum <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'


    @visitor.when(AST_init.Rest)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Rest, tabs):
        ans = '\t' * tabs + f'\\__<expr> Rest <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.Mult)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Mult, tabs):
        ans = '\t' * tabs + f'\\__<expr> Mult <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.Div)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Div, tabs):
        ans = '\t' * tabs + f'\\__<expr> Div <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.Less)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Less, tabs):
        ans = '\t' * tabs + f'\\__<expr> Less <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.LessOrEquals)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.LessOrEquals, tabs):
        ans = '\t' * tabs + f'\\__<expr> LOrE <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.Equals)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Equals, tabs):
        ans = '\t' * tabs + f'\\__<expr> Equals <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AST_init.Void)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Void, tabs):
        exp = self.visit(node.item, tabs + 1)
        return '\t' * tabs + f'\\__ Void\n {exp}'
        

    @visitor.when(AST_init.New)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.New, tabs):
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.item}()'

    @visitor.when(AST_init.Complement)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Complement, tabs):
        exp = self.visit(node.item, tabs + 1)
        return '\t' * tabs + f'\\__Complemnt\n {exp}'

    @visitor.when(AST_init.Neg)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Neg, tabs):
        exp = self.visit(node.item, tabs + 1)
        return '\t' * tabs + f'\\__Neg\n {exp}'

    @visitor.when(AST_init.Id)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Id, tabs):
        return '\t' * tabs + f'\\__ Id:{node.item}'

    @visitor.when(AST_init.Int)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Int, tabs):
        return '\t' * tabs + f'\\__ Int:{node.item}'


    @visitor.when(AST_init.Bool)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Bool, tabs):
        return '\t' * tabs + f'\\__ Bool:{node.item}'

    @visitor.when(AST_init.Str)
    #@visitor.result(AST_result.CoolClass)
    #@visitor.inmutable_visit
    def visit(self, node: AST_init.Str, tabs):
        return '\t' * tabs + f'\\__ Str:{node.item}'
