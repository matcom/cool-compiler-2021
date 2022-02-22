from cProfile import label


class Program:
    def __init__(self) -> None:
        self.data = {}
        self.func = {}
    
    def __str__(self) -> str:
        result = ".data"

        for key in self.data.keys():
            result += str(self.data[key]) + '\n'
        
        result += '.text\n.globl main\n'
        result += str(self.func['main']) + '\n'

        for key in self.func.keys():
            if key == 'main': continue
            result += str(self.func[key]) + '\n'

        return result

class Data:
    def __init__(self, _type, name, value) -> None:
        self.type = _type
        self.name = name
        self.value = value
    
    def __str__(self) -> str:
        return f'{self.name}: .{self.type} {self.value}'

class Func:
    def __init__(self, name, list_cmd= []) -> None:
        self.name = name
        self.cmd  = list_cmd

    def __str__(self) -> str:
        result = f'{self.name}:\n'

        for cmd in self.cmd:
            result += str(cmd) + '\n'

        return result

class Comment:
    def __init__(self, msg) -> None:
        self.msg = msg
    
    def __str__(self) -> str:
        return self.msg

class Load:
    def __init__(self, cmd ,registry, memory_dir) -> None:
        self.registry = registry
        self.memory_dir = memory_dir
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.registry}, {self.memory_dir}'

class Store:
    def __init__(self, cmd ,registry, memory_dir) -> None:
        self.registry = registry
        self.memory_dir = memory_dir
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.registry}, {self.memory_dir}'

class CmpNotJump:
    def __init__(self, cmd ,r_dest, r_src_1, r_src_2) -> None:
        self.r_assign =  r_dest
        self.r_op_1 = r_src_1
        self.r_op_2 = r_src_2
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.r_assign}, {self.r_op_1}, {self.r_op_2}'

# Commands
############################  Loads   ##################################################
class LW(Load):
    def __init__(self, registry, memory_dir) -> None:
        super().__init__('lw', registry, memory_dir)

############################  Store   ##################################################
############################  Cmp   ##################################################
