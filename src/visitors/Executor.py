from cool_ast.cool_ast import *
from typing import List, Dict
import visitors.visitor as visitor
from utils.semantic import Context, Type, Method, Scope
from typing import Any
from utils.exceptions import RuntimeException

class Pod:
    def __init__(self, typex, value = None):
        if value is None:
            value = id(self)

        self.type = typex
        self.value = value
        self.attr = {}

    def set_attribute(self, name, value):
        self.attr[name] = value

    def get_attribute(self, name):
        return self.attr[name]

    def get_method(self, name, typex, visited):
        return self.type.get_method(name, typex, visited)

    def __str__(self):
        return f'{self.type.name}: {self.value}'

def type_name(obj, context):
    return Pod(context.get_type('String'), obj.type.name)

def out_string(obj, s, context):
    print(s.value, end='')
    return obj

def out_int(obj, s, context):
    print(s.value, end='')
    return obj

def in_string(obj, context):
    return Pod(context.get_type('Int'), input())

def in_int(obj, context):
    return Pod(context.get_type('Int'), int(input()))

def ocopy(obj, context) -> None:
    x_copy = Pod(obj.type, obj.value if obj.type.name in ('Int', 'String', 'Bool') else None)
    x_copy.attr_values = obj.attr_values
    return x_copy

def length(obj, context):
    return Pod(context.get_type('Int'), len(obj.value))

def concat(obj, s, context):
    return Pod(context.get_type('String'), obj.value + s.value)

def substr(obj, i, l, context):
    return Pod(context.get_type('String'), obj.value[i.value: i.value + l.value])

def abort(obj, context):
    print('Aborting execution')
    exit()

cl_baseline = {
    ('Object', 'type_name'): type_name,
    ('Object', 'abort'): abort,
    ('Object', 'copy'): ocopy,
    ('IO', 'out_int'): out_int,
    ('IO', 'out_string'): out_string,
    ('IO', 'in_string'): in_string,
    ('IO', 'in_int'): in_int,
    ('String', 'concat'): concat,
    ('String', 'substr'): substr,
    ('String', 'length'): length
}

class Executor:
    def __init__(self, context: Context):
        self.context: Context = context
        self.currentType = None
        self.currentPod = None
        self.stack = []

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        for declaration in node.declarations:
            self.visit(declaration, None)

        main_callnode = CallNode('main', [], InstantiateNode('Main'))
        self.visit(main_callnode, scope)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.currentType = self.context.get_type(node.id)

        attrs = [f for f in node.features if isinstance(f, AttrDeclarationNode)]
        methods = [f for f in node.features if isinstance(f, FuncDeclarationNode)]

        for attr in attrs:
            self.visit(attr, None)

        for method in methods:
            self.visit(method, None)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        self.currentType.get_attribute(node.id, self.currentType, False).expr = node.value

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.currentType.get_method(node.id, self.currentType, False).expr = node.body

    @visitor.when(CallNode)
    def visit(self, node, scope):
        token = self.visit(node.obj, scope)

        if isinstance(token, VoidPod):
            raise RuntimeException('Reference to an instance of a void object.')

        _o = self.context.get_type('Object')
        _s = self.context.get_type('String')
        _io = self.context.get_type('IO')

        if token.type.conforms_to(_o) and (_o.name, node.method) in cl_baseline:
            args = (token,) + tuple(self.visit(arg, scope) for arg in node.args) + (self.context,)
            return cl_baseline[_o.name, node.method](*args)

        if token.type.conforms_to(_s) and (_s.name, node.method) in cl_baseline:
            args = (token,) + tuple(self.visit(arg, scope) for arg in node.args) + (self.context,)
            return cl_baseline[_s.name, node.method](*args)

        if token.type.conforms_to(_io) and (_io.name, node.method) in cl_baseline:
            args = (token,) + tuple(self.visit(arg, scope) for arg in node.args) + (self.context,)
            return cl_baseline[_io.name, node.method](*args)

        #si es una instantiate.f() meter en el scope hijo todos sus atributos
        _funcCall_scope = Scope()
        #para el caso a@b.f()
        if not node.parent is None:
            parent_t = self.context.get_type(node.parent)
            method = parent_t.get_method(node.method, parent_t, False)
        else:
            method = token.get_method(node.method, self.currentType, False)
        
        for _id, _t, _arg in zip(method.param_names, method.param_types, node.args):
            _funcCall_scope.define_variable(_id, _t).token = self.visit(_arg, scope)

        
        _funcCall_scope.define_variable('self', token.type).token = token
        # atrbs = []
        # if node.obj.lex != 'self':
        #     for attr in token.attr_values.keys():
        #         if scope.is_local(attr):
        #             pass
        #         else:
        #             child_scope.define_variable(attr, token.attr_values[attr].type).token = token.attr_values[attr]
        #             atrbs.append(attr)
        self.stack.append(self.currentPod)
        self.currentPod = token
        
        result = self.visit(method.expr, _funcCall_scope)
        
        # for name in atrbs:
        #     token.attr_values[name] = child_scope.find_variable(name).token

        self.currentPod = self.stack.pop()
        return result

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        a = 0
        
        for nod in node.decl_list:
            _id = nod.id
            _t = nod.type
            _expr = nod.expr
            if _t in ['Int', 'String', 'Bool'] and _expr is None:
                tempNode = InstantiateNode(_t)
                token = self.visit(tempNode, scope)
            else:
                if _expr is not None:
                    token = self.visit(_expr, scope.create_child())    
                else:
                    token = VoidPod()
            
            if isinstance(token, VoidPod):
                try:
                    token.type = self.context.get_type(_t)
                except:
                    pass
            scope.define_variable(_id, token.type).token = token

        return self.visit(node.expression, scope.create_child())

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        variable_info = scope.find_variable(node.id)
        if variable_info is None:
            token = self.visit(node.expr, scope)
            attr = self.currentPod.get_attribute(node.id)
            self.currentPod.set_attribute(node.id, token)
            return token
        
        variable_info.token = self.visit(node.expr, scope)
        return variable_info.token

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if node.lex == 'self':
            return self.currentPod
        
        variable_info = scope.find_variable(node.lex)
        
        if variable_info is not None and not isinstance(variable_info.token, VoidPod):
            return variable_info.token
        try:
            return self.currentPod.get_attribute(node.lex)
        except:
            return variable_info.token
        
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        start_value = None
        if node.lex == 'Int':
            start_value = 0
        elif node.lex == 'Bool':
            start_value = False
        elif node.lex == 'String':
            start_value = ''
        
        token = Pod(self.context.get_type(node.lex), start_value)

        self.stack.append(self.currentPod)
        self.currentPod = token
        for attr, _t in token.type.all_attributes():
            if attr.expr is not None:
                attr_token = self.visit(attr.expr, scope)
            else:
                attr_token = VoidPod()
            # scope.define_variable(attr.name, attr.type).token = attr_token
            self.currentPod.set_attribute(attr.name, attr_token)
        self.currentPod = self.stack.pop()
        return token

    @visitor.when(ChunkNode)
    def visit(self, node, scope):
        child_scope = scope.create_child()
        token = None
        for expr in node.chunk:
            token = self.visit(expr, child_scope)
        return token

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        if_token = self.visit(node.ifChunk, scope)

        if if_token.value:
            return self.visit(node.thenChunk, scope.create_child())

        return self.visit(node.elseChunk, scope.create_child())

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), self.visit(node.left, scope).value == self.visit(node.right, scope).value)
    
    @visitor.when(LeqNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), self.visit(node.left, scope).value <= self.visit(node.right, scope).value)

    @visitor.when(LessNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), self.visit(node.left, scope).value < self.visit(node.right, scope).value)

    @visitor.when(SwitchCaseNode)
    def visit(self, node, scope):
        token = self.visit(node.expr, scope)

        if isinstance(token, VoidPod):
            raise RuntimeException('Reference to an instance of a void object.')

        types = [(i, self.context.get_type(t)) for i, (_, t, _) in enumerate(node.case_list)
                 if token.type.conforms_to(self.context.get_type(t))]

        if len(types) == 0:
            raise RuntimeException('NotTypeFoundError: None of the types were valid')

        (index, temp) = types[0]
        for i, t in types:
            if t.conforms_to(temp):
                index, temp = i, t

        child_scope = scope.create_child()
        _id, _t, _e = node.case_list[index]
        child_scope.define_variable(_id, self.context.get_type(_t)).token = token
        return self.visit(_e, child_scope)

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        # if isinstance(node.condition, ConditionalNode) and isinstance(node.condition.ifChunk, CallNode):
        a = 0
        while self.visit(node.condition, scope).value:
            self.visit(node.loopChunk, scope.create_child())
        
        return VoidPod()

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Int'), int(node.lex))

    @visitor.when(StringNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('String'), str(node.lex[1:-1].replace('\\n', '\n')).replace('\\t', '\t'))

    @visitor.when(TrueNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), True)

    @visitor.when(FalseNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), False)

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Int'), self.visit(node.left, scope).value + self.visit(node.right, scope).value)

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Int'), self.visit(node.left, scope).value - self.visit(node.right, scope).value)

    @visitor.when(StarNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Int'), self.visit(node.left, scope).value * self.visit(node.right, scope).value)

    @visitor.when(DivNode)
    def visit(self, node, scope):
        try:
            return Pod(self.context.get_type('Int'), self.visit(node.left, scope).value // self.visit(node.right, scope).value)
        except ZeroDivisionError as err:
            raise RuntimeException('Runtime exception: ' + err.args[0])

    @visitor.when(NotNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), not self.visit(node.expression, scope).value)

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Bool'), isinstance(self.visit(node.method, scope), VoidPod))

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        return Pod(self.context.get_type('Int'), ~ self.visit(node.expression, scope).value)

    
##
class VoidPod(Pod):
    def __init__(self):
        super(VoidPod, self).__init__(None, None)
        # raise Exception('hola worl')

    def __eq__(self, cousin):
        return isinstance(cousin, VoidPod)