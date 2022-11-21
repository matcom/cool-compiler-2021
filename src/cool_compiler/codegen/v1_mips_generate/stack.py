from cool_compiler.cmp.visitor import result
from . import mips_generate_ast as ASTR

class Stack:
    def __init__(self, node) -> None:
        self.name = node.name
        self.init_size = len(node.param) + len(node.local) + 1
        self.list = []
        self.local_push = 0 

    def push(self, name):
        self.local_push += 1

        if name == '_':
            _result = [ASTR.Move('$t0', '$s4', f'Lee el valor de la operacion anterior')]
        elif type(name) == type(int()):
            _result = [ASTR.LI('$t0', name, f'Guarda en valor entero')]
        else:
            _result = [ASTR.LW('$t0', f'{self.index(name)}($sp)', f'Lee el valor de la var {name}')]
            
        self.list.append(name)
        return _result + [
            ASTR.AddI('$sp', '$sp', -4),
            ASTR.SW('$t0', '0($sp)', f'Push a la pila con {name}')]    

    @property
    def initial_index(self):
        return (self.init_size - len(self.list)) * 4

    def index(self, name):
        return (len(self.list) - self.list.index(name) - 1) * 4
    
    def clean(self):
        self.list = self.list[0: len(self.list) - self.local_push]
        assert self.list[-1] == '$ra', "El ultimo de la pila no es $ra"
        self.local_push = 0

    def close(self):
        if not any(self.list): return []
        result = len(self.list) * 4
        self.local_push
        self.list = []
        return [ASTR.AddI('$sp', '$sp', result)]
    
    def def_param(self, name):
        self.list.append(name)
        return [ASTR.Header_Comment(f'Parametro {name} en stackpoiner + {self.initial_index}')]  
    
    def def_local(self, name):
        self.list.append(name)
        return [ASTR.AddI('$sp', '$sp', -4, f'Push local var {name} stackpointer {self.initial_index}')]
    
    def write_local(self, registry, name, commnet = ''):
        if name == '_':
            return [ASTR.Move(f'$s4', registry, commnet)] 
        # if name == 'self':
        #     return [ASTR.Move(f'$s6', registry, commnet)]
        return [ASTR.SW(registry, f'{self.index(name)}($sp)', commnet)]

    def read_local(self, registry, name, commnet = ''):
        if name == '_':
            return [ASTR.Move(registry, f'$s4', commnet)] 
        # if name == 'self':
        #     return [ASTR.Move(registry, f'$s6', commnet)]
        return [ASTR.LW(registry, f'{self.index(name)}($sp)', commnet)]