from cool_compiler.semantic.v0_parser_return.factory_parser_return_ast import AtrDef


result = '@result'
self_name = 'self'
super_value = '<value>'

class StackData:
    def __init__(self, x = None) -> None:
        self.x = x

    def __str__(self) -> str:
        return self.x

class Local(StackData):
    pass

class Param(StackData):
    pass

class Node:
    def get_pos_to_error(self, lineno, index):
        self.lineno = lineno
        self.index = index

class Program(Node): 
    def __init__(self) -> None:
        self.ty_list = []
        self.types = {}
        self.data_list = []
        self.data = {}
        self.func_list = []
        self.functions = {}

    def __str__(self) -> str:
        result = ".TYPE\n" 

        for ty in self.ty_list:
            result += str(self.types[ty]) + '\n'
        
        result += ".DATA\n" 
        for data in self.data_list:
            result += str(self.data[data]) + '\n'

        result += ".FUNCTION\n" 
        for func in self.func_list:
            result += str(self.functions[func]) + '\n'

        return result
    def try_add_data(self, name, value):
        try: 
            _ = self.data[name]
        except KeyError: 
            self.data[name] = value

    def add_data(self, name, value):
        index = 0
        while f'{name}_{index}' in self.data_list: index += 1 
        self.data_list.append(f'{name}_{index}')
        self.data[self.data_list[-1]] = Data(self.data_list[-1], value)
        return self.data_list[-1]
        
    def add_type(self, type):
        self.ty_list.append(type.name)
        self.types[type.name] = type

    def add_func(self, func):
        self.func_list.append(func.name)
        self.functions[func.name] = func

class Type(Node): 
    def __init__(self, name) -> None:
        self.name = name 
        self.attributes = []
        self.attr = {}
        self.method_list = []
        self.methods = {}

    def attr_push(self, name, _name):
        if not name in self.attributes:
            self.attributes.append(name)

        self.attr[name] = _name

    def method_push(self, name, f):
        try: 
            self.methods[name]
        except KeyError:
            self.method_list.append(name)
            self.methods[name] = f

    def __str__(self) -> str:
        result = f'type {self.name}: ' + '{\n'

        for  att in self.attributes:
            result += '\tattribute ' + str(att) + ' '*(14 - len(str(att))) +  '->  ' + str(self.attr[att]) + '\n'
        
        for  func in self.method_list:
            result += '\tfunction ' + str(func) + ' '*(15 - len(str(func))) +  '->  ' + str(self.methods[func]) + '\n'

        return result + '}'

class Data(Node):
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'\tdata {self.name}: {self.value}'

class String(Data):
    pass
    
class Int(Data):
    pass

class Bool(Data):
    pass

class Function(Node):
    def __init__(self, name) -> None:
        self.name = name
        self.var_dir = {}
        self.param = []
        self.local = []
        self.expr = []
    
    def get_name(self, name):
        index = 0
        while True:
            try: 
                _ = self.var_dir[f'{name}@{index}']
                index += 1
            except KeyError:
                return f'{name}@{index}'

    def force_local(self,name, scope):
        scope.define_variable(name, name)
        self.var_dir[name] = 1
        self.local.append(Local(name))
        return name

    def force_parma(self,name, scope):
        self.var_dir[name] = 1
        scope.define_variable(name, name)
        self.param.append(Param(name))
        return name

    def param_push(self, name, scope):
        new_name = self.get_name(name)
        scope.define_variable(name, new_name)
        self.var_dir[new_name] = 1
        self.param.append(Param(new_name))
        return new_name
    
    def local_push(self, name, scope):
        new_name = self.get_name(name)
        scope.define_variable(name, new_name)
        self.var_dir[new_name] = 1
        self.local.append(Local(new_name))
        return new_name
    
    def expr_push(self, expr):
        self.expr.append(expr)

    def __str__(self) -> str:
        result = f'function {self.name}: ' + '{\n'

        for param in self.param:
            result += f'\tPARAM {str(param)}\n'
        
        for local in self.local:
            result += f'\tLOCAL {str(local)}\n'
        
        for exp in self.expr:
            result += '\t' + str(exp) + '\n'

        return result + '}'
    
class Expression(Node):
    def __init__(self, x = None, y = None, z = None) -> None:
        self.x = x
        self.y = y
        self.z = z

    def try_set_value(self, name):
        if self.x == super_value:
            self.x = name
            return True
        return False

    def set_value(self, name):
        if not self.x == super_value: 
            raise Exception("The expression is'nt set expression")
        self.x = name

    def __str__(self) -> str:
        result = self.__class__.__name__ + ' '

        if not self.x is None:
            result += str(self.x) + " "

        if not self.y is None:
            result += str(self.y) + " "
        
        if not self.z is None:
            result += str(self.z) + " "
        
        return result

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

class Less(Expression):
    pass

class LessOrEqual(Expression):
    pass

class CmpInt(Expression):
    pass

class CmpStr(Expression):
    pass

class CmpRef(Expression):
    pass

class CheckType(Expression):
    pass

class Return(Expression):
    pass

class Arg(Expression):
    pass

class VCall(Expression):
    pass

class Load(Expression):
    pass

class ALLOCATE(Expression):
    pass


class NegAssing(Expression):
    pass

class IfGoTo(Expression):
    pass

class GoTo(Expression):
    pass

class Label(Expression):
    pass

class TypeOf(Expression):
    pass

class New(Expression):
    pass

class Neg(Expression):
    pass

class Complemnet(Expression):
    pass

class Comment(Expression):
    def __str__(self) -> str:
        return ""


