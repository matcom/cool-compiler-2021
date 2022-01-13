result = '@result'
self_name = 'self'
super_value = '<value>'


class Node:
    def get_pos_to_error(self, lineno, index):
        self.lineno = lineno
        self.index = index

class Program(Node): 
    def __init__(self, types = {}, data = {}, functions = {}) -> None:
        self.types = types
        self.data = data
        self.functions = functions

class Type(Node): 
    def __init__(self, name) -> None:
        self.name = name
        self.attributes = []
        self.method_list = []
        self.methods = {}

    def attr_push(self, name):
        if not name in self.attributes:
            self.attributes.append(name)

    def method_push(self, name, f):
        try: self.methods[name]
        except KeyError:
            self.method_list.append(name)
            self.methods[name] = f

class Data(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class String(Data):
    pass
    
class Int(Data):
    pass

class Bool(Data):
    pass

class Function(Node):
    def __init__(self, name) -> None:
        self.name = name
        self.param = []
        self.local = []
        self.expr = []
    
    def param_push(self, name, save = False):
        index = 0
        while f'name@{index}' in self.param:
            index += 1
        if save: self.param.append(f'name@{index}')
        return f'name@{index}'
    
    def local_push(self, name):
        self.local.append(name)
    
    def expr_push(self, expr):
        self.expr.append(expr)
    
class Expression(Node):
    def __init__(self, x = None, y = None, z = None) -> None:
        self.x = x
        self.y = y
        self.z = z

    def try_set_value(self, name):
        if self.x == super_value:
            self.x = super_value
            return True
        return False

    def set_value(self, name):
        if not self.x == super_value: 
            raise Exception("The expression is'nt set expression")
        self.x = name


class Assign(Expression):
    pass

class GetAttr(Expression):
    pass

class SetAttr(Expression):
    pass

class Sum(Expression):
    pass

class Rest(Expression):
    pass

class Div(Expression):
    pass

class Mult(Expression):
    pass

class Return(Expression):
    pass

class Arg(Expression):
    pass

class Call(Expression):
    pass

class VCall(Expression):
    pass