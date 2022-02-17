from .semantic import Type, Context, Scope, Method, SemanticError
import utils.ast_nodes as ast
import utils.visitor as visitor


class ExecutionError(Exception):
    @property
    def text(self):
        return self.args[0]


class ExecutionObject:
    def __init__(self, type: Type, value=None):
        if value:
            self.value = id(self)

        self.type = type
        self.value = value
        self.attribute_instances = {}

    def __str__(self):
        return f'{self.type.name} -> {self.value}'

    def set_attribute(self, idx, instance):
        self.attribute_instances[idx] = instance

    def get_attribute(self, idx):
        try:
            return self.attribute_instances[idx]
        except KeyError:
            raise ExecutionError(f'La instancia \'{idx}\' no existe.')

    def get_method(self, name: str):
        return self.type.get_method(name)

class VoidObject(ExecutionObject):
    def __init__(self):
        super(VoidObject, self).__init__(None, None)
    
    def __eq__(self, obj):
        return isinstance(obj, VoidObject)


# Default Methods

def abort(obj, context):
    print('Terminando programa...')
    exit()


def copy(obj, context):
    x_copy = ExecutionObject(obj.type, obj.value if obj.type.name in ('Int', 'String', 'Bool') else None)
    x_copy.attribute_values = obj.attribute_values
    return x_copy


def type_name(obj, context):
    return ExecutionObject(context.get_type('String'), obj.type.name)


def out_string(obj, s, context):
    print(s.value, end='')
    return obj


def out_int(obj, s, context):
    print(s.value, end='')
    return obj


def in_string(obj, context):
    return ExecutionObject(context.get_type('String'), str(input()))


def in_int(obj, context):
    return ExecutionObject(context.get_type('Int'), int(input()))


def length(obj, context):
    return ExecutionObject(context.get_type('Int'), len(obj.value))


def concat(obj, s, context):
    return ExecutionObject(context.get_type('String'), obj.value + s.value)


def substr(obj, i, l, context):
    return ExecutionObject(context.get_type('String'), obj.value[i: i + l])


methods = {
    'Object': (['abort', 'type_name', 'copy'], [abort, type_name, copy]),
    'IO': (['out_string', 'out_int', 'in_string', 'in_int'], [out_string, out_int, in_string, in_int]),
    'String': (['lenght', 'concat', 'substr'], [length, concat, substr])
}

class Execution:
    def __init__(self, context: Context):
        self.context = context
        self.current_type: Type = None
        self.current_instance: ExecutionObject = None
        self.stack = []

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        if scope is None:
            scope = Scope()

        for p in node.class_list:
            self.visit(p, None)

        try:
            main = self.context.get_type('Main')
            main.get_method('main')
        except SemanticError as e:
            print(e.text)
            exit()

        self.visit(ast.MethodCallNode('main', [], ast.NewNode('Main')), scope)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode, scope: Scope):
        self.current_type = self.context.get_type(node.name)
        for item in node.data:
            self.visit(item, None)

    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode, scope: Scope):
        self.current_type.get_method(node.name).expr = node.expr

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode, scope: Scope):

        if node.expr is None:
            if node._type == 'Int':
                node.expr = ast.NumberNode('0')
            if node._type == 'String':
                node.expr = ast.StringNode('')
            if node._type == 'Bool':
                node.expr = ast.BooleanNode('false')
        
        try:
            self.current_type.get_attribute(node.name).expr = node.expr
        except ExecutionError as e:
            print(e.text)
            exit()

    # Expressions
    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        cond = self.visit(node.cond, scope).value
        while cond:
            self.visit(node.data, scope.create_child())
            cond = self.visit(node.cond, scope).value
        return VoidObject()

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        for id_, _, expr_ in node.declaration:
            instance = VoidObject() if expr_ is None else \
                        self.visit(expr_, scope.create_child())
            scope.define_variable(id_, instance.type).instance = instance

        return self.visit(node.expr, scope.create_child())


    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        variable_info = scope.find_variable(node.idx)
        if variable_info is None:
            self.current_instance.set_attribute(node.idx, self.visit(node.expr, scope))
            try:
                return self.current_instance.get_attribute(node.idx)
            except ExecutionError as e:
                print(e.text)
                exit()

        variable_info.instance = self.visit(node.expr, scope)
        return variable_info.instance

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        sc = scope.create_child()
        inst = None
        for expr in node.expr:
            inst = self.visit(expr, sc)
        return inst

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        if self.visit(node.if_expr, scope).value:
            return self.visit(node.then_expr, scope.create_child())
        return self.visit(node.else_expr, scope.create_child())

    @visitor.when(ast.ParenthesisNode)
    def visit(self, node: ast.ParenthesisNode, scope: Scope):
        return self.visit(node.expr, scope)

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, scope: Scope):
        expr0 = self.visit(node.expr, scope)
        if isinstance(expr0, VoidObject):
            raise ExecutionError('La clausula \'Case\' no puede devolver \'Void\'.')
        
        types = [(pos, self.context.get_type(type_))\
            for pos, (_, type_, _) in enumerate(node.params) \
                if expr0.type.conforms_to(self.context.get_type(type_))]
        
        if not types:
            raise ExecutionError('Ninguno de los tipos propuestos en la clausula \'Case\' coinciden con el tipo de la expresión.')
        
        i, type_ = types[0]
        for i_, t in enumerate(types):
            if t[1].conforms_to(type_):
                i, type_ = i_, t[1]

        sc = scope.create_child()
        name, typex, expr = node.params[i]
        sc.define_variable(name, self.context.get_type(typex)).instance = expr0
        return self.visit(expr, sc)

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, scope: Scope):
        return ExecutionObject(self.context.get_type('Bool'), \
            isinstance(self.visit(node.expr, scope), VoidObject))

    # Arithmetic and Boolean Expressions
    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value
        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError(
                'Los terminos de la operación \'+\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Int'), left + right)

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value
        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError(
                'Los terminos de la operación \'-\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Int'), left - right)

    @visitor.when(ast.TimesNode)
    def visit(self, node: ast.TimesNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value
        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError(
                'Los terminos de la operación \'*\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Int'), left * right)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value
        if right == 0:
            raise ZeroDivisionError()
        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError(
                'Los terminos de la operación \'/\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Int'), left / right)

    @visitor.when(ast.LessNode)
    def visit(self, node: ast.LessNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value
        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError('Los terminos de la operación \'<\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Bool'), left < right)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value

        if not isinstance(left, int) or not isinstance(right, int):
            raise ExecutionError(
                'Los terminos de la operación \'<=\' deben ser enteros (int).')
        return ExecutionObject(self.context.get_type('Bool'), left <= right)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        left = self.visit(node.left, scope).value
        right = self.visit(node.right, scope).value

        if type(left) !=  type(right):
            raise ExecutionError(
                'Los terminos de la operación \'=\' deben tener el mismo tipo.')
        return ExecutionObject(self.context.get_type('Bool'), left == right)

    # Unary Expressions
    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, scope: Scope):
        return ExecutionObject(self.context.get_type('Int'), ~ self.visit(node.expr).value)

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, scope: Scope):
        return ExecutionObject(self.context.get_type('Bool'), not self.visit(node.expr, scope).value)

    # Atomic Expressions
    @visitor.when(ast.NumberNode)
    def visit(self, node: ast.NumberNode, scope: Scope):
        return ExecutionObject(self.context.get_type('Int'), int(node.lex))

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        return ExecutionObject(self.context.get_type('String'), str(node.lex[1:-1]).replace('\\n', '\n'))

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        return ExecutionObject(self.context.get_type('Bool'), node.lex == 'true')

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, scope: Scope):
        if node.lex == 'i':
            'i'
        variable_info = scope.find_variable(node.lex)
        if variable_info is not None:
            return variable_info.instance
        else:
            try:
                return self.current_instance.get_attribute(node.lex)
            except ExecutionError as e:
                print(e.text)
                exit()

    @visitor.when(ast.NewNode)
    def visit(self, node: ast.NewNode, scope: Scope):
        value = None
        if node.type == 'Int':
            value = 0
        elif node.type == 'String':
            value = ''
        elif node.type == 'Bool':
            value = False
        
        inst = ExecutionObject(self.context.get_type(node.type), value)
        self.stack.append(self.current_instance)
        self.current_instance = inst
        
        fake_sc = Scope()
        for attr, _ in inst.type.all_attributes():
            attr_instance = self.visit(attr.expr, fake_sc) if attr.expr is not None else VoidObject()
            fake_sc.define_variable(attr.name, attr.type).instance = attr_instance
            self.current_instance.set_attribute(attr.name, attr_instance)
        self.current_instance = self.stack.pop()
        return inst

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode, scope: Scope):

        if not node.atom:
            node.atom = ast.NewNode(self.current_type.name)

        obj_inst = self.visit(node.atom, scope)

        if isinstance(obj_inst, VoidObject):
            raise ExecutionError('El objeto referenciado no es una instancia de Objeto.')
        

        if obj_inst.type.conforms_to(self.context.get_type('Object')) and node.idx in methods['Object'][0]:
            args = (obj_inst,) + tuple(self.visit(arg, scope) for arg in node.exprlist) + (self.context,)
            i = methods['Object'][0].index(node.idx)
            return methods['Object'][1][i](*args)

        if obj_inst.type.conforms_to(self.context.get_type('IO')) and node.idx in methods['IO'][0]:
            args = (obj_inst,) + tuple(self.visit(arg, scope) for arg in node.exprlist) + (self.context,)
            i = methods['IO'][0].index(node.idx)
            return methods['IO'][1][i](*args)

        if obj_inst.type.conforms_to(self.context.get_type('String')) and node.idx in methods['String'][0]:
            args = (obj_inst,) + tuple(self.visit(arg, scope) for arg in node.exprlist) + (self.context,)
            i = methods['String'][0].index(node.idx)
            return methods['String'][1][i](*args)

        new_scope = Scope()

        method = obj_inst.get_method(node.idx)
        new_scope.define_variable(
            'self', obj_inst.type).instance = obj_inst
        for name, typex, arg in zip(method.param_names, method.param_types, node.exprlist):
            new_scope.define_variable(
                name, typex).instance = self.visit(arg, scope)

        self.stack.append(self.current_instance)
        self.current_instance = obj_inst
        output = self.visit(method.expr, new_scope)
        self.current_instance = self.stack.pop()
        return output
