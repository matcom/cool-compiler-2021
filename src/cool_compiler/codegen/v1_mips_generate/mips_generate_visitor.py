from ..v0_cool_to_cil import cool_to_cil_ast as AST
from . import mips_generate_ast as ASTR
from ...cmp import visitor
from .stack import Stack
from .native_funcion import CoolNativeFunctions

class MipsGenerate:
    def __init__(self, _) -> None:
        self.func_list = ['main']
        self.native_func = CoolNativeFunctions()

    @visitor.on('node')
    def visit(node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node: AST.Program):
        self.cil_data = node.data
        self.cil_type = node.types
        self.cil_func = node.functions

        self.new_program = ASTR.Program()

        for data_label in self.cil_data.keys():
            self.new_program.data[data_label] = ASTR.Data(data_label, self.cil_data[data_label].value)

        for func in self.func_list:
            try: self.new_program.func[func] = self.native_func.call(func)
            except AttributeError: self.visit(self.cil_func[func])
        
        for func in list(self.cil_func.keys()) + self.native_func.method_list:
            if func in self.func_list: continue
            self.new_program.func[func] = ASTR.Func(func, 
                "Esta funcion no se invoca en la ejecucion del programa")

        return self.new_program

    @visitor.when(AST.Function)
    def visit(self, node: AST.Function):
        new_func = ASTR.Func(node.name)
        self.stack = Stack(node)
        
        for param in node.param:
            new_func.cmd += self.stack.def_param(param)

        for _local in node.local:
            new_func.cmd += self.stack.def_local(_local)
        
        new_func.cmd += self.stack.def_local('$ra')
        new_func.cmd += self.stack.write_local('$ra','$ra', f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {node.name}")

        for expr in node.expr:
            new_func.cmd += self.visit(expr)

        self.new_program.func[new_func.name] = new_func

    @visitor.when(AST.ALLOCATE)
    def visit(self, node: AST.ALLOCATE):
        memory_dir = node.x
        _type = node.y

        attr_list = self.cil_type[_type].attributes 
        _len = len(attr_list) * 4

        result = [ASTR.Header_Comment(f"Allocate a una class {_type}")]
        for i, attr in enumerate(attr_list):
            result.append(ASTR.Header_Comment(f'atributo {attr} en puntero + {i * 4}'))

        return result + [
            ASTR.LI('$a0', _len),
            ASTR.LI('$v0', 9),
            ASTR.SysCall()
            ] +  self.stack.write_local('$v0', memory_dir, f'Guardando en la variable local {memory_dir} puntero de la instancia de la clase {_type}')

    @visitor.when(AST.GetAttr)
    def visit(self, node: AST.GetAttr):
        memory_dest = node.x
        memory_dir_instance = node.y
        attr_name = node.z.split('@')
        _type = attr_name[0]
        attr = attr_name[1]

        attr_plus = self.cil_type[_type].attributes.index(attr) * 4 

        result = self.stack.read_local('$t0', memory_dir_instance, f'Instancia de la clase {_type}')
        result += [ASTR.LW('$t1', f'{attr_plus}($t0)', f'Lee la propiedad {attr}')]
        result += self.stack.write_local('$t1', memory_dest, f'Guarda el valor de la propiedad {attr} en la variable local {memory_dest}')
        return result
    
    @visitor.when(AST.SetAttr)
    def visit(self, node: AST.SetAttr):
        if node.y == 'type_name': 
            attr_plus = 0
            attr = 'type_name'
            _type = ""
        else: 
            attr_name = node.y.split('@')
            _type = attr_name[0]
            attr = attr_name[1]
            attr_plus = self.cil_type[_type].attributes.index(attr) * 4

        memory_dir_instance = node.x
        memory_dir_value = node.z

        result = self.stack.read_local('$t0', memory_dir_instance, f'Instancia de la clase {_type}')
        result += self.stack.read_local('$t1', memory_dir_value, f'Guarda el valor que se le asignara a la propieded {attr}')
        result += [ASTR.SW('$t1', f'{attr_plus}($t0)', f'Setea la propiedad {attr} con el valor de {memory_dir_value}')]

        return result

    @visitor.when(AST.Arg)
    def visit(self, node: AST.Arg):
        return self.stack.push(node.x)

    def call(self, func, memory_dest):
        self.stack.clean()

        return [ASTR.Jal(func)] + self.stack.write_local('$v0', memory_dest, f'Asigna el resultado de la funcion')
   
    @visitor.when(AST.SimpleCall)
    def visit(self, node: AST.SimpleCall):
        if not node.x in self.func_list: self.func_list.append(node.x)
        return self.call(node.x, 'self')[0: -1]

    @visitor.when(AST.VCall)
    def visit(self, node: AST.VCall):
        memory_dest = node.x
        _type = node.y
        try:
            func = self.cil_type[_type].methods[node.z]
            if not func in self.func_list: self.func_list.append(func)

            return self.call(func, memory_dest)
        except KeyError:
            if '__new__' in node.y: return self.call_magic_method(node.y, node.z, node.x)
            raise KeyError(node.z)

    @visitor.when(AST.New)
    def visit(self, node: AST.New):
        func = f'new_ctr_{node.y}'
        if not func in self.func_list: self.func_list.append(func)
        return self.call(f'new_ctr_{node.y}', node.x)

    @visitor.when(AST.Call)
    def visit(self, node: AST.Call):
        memory_dest = node.x
        _type, func_name = node.z.split('@')

        self.func_list += [func for func in self.cil_func.keys() 
            if func_name in func and  not func in self.func_list]

        self.func_list += [func for func in self.native_func.method_list 
            if func_name in func and  not func in self.func_list]

        func_address = self.cil_type[_type].method_list.index(func_name) * 4 + 12
        _result = self.stack.read_local('$t0', node.y)
        _result.append(ASTR.LW('$t1', '0($t0)', f"Leyendo el tipo dinamico de la instancia que hereda de {_type}"))
        _result.append(ASTR.LW('$t3', f'{func_address}($t1)', f"Buscando el metodo dinamico para la funcion {func_name}"))

        return _result + self.call('$t3', memory_dest)

    @visitor.when(AST.Return)
    def visit(self, node: AST.Return):
        if node.x == 0: 
            return [ASTR.LI('$v0', 10), ASTR.SysCall()]
        
        memory_dest = node.x
        _result = self.stack.read_local('$v0', memory_dest, f'Return {memory_dest}')
        _result += self.stack.read_local('$ra', '$ra', 'Lee $ra de la pila para retornar a la funcion anterior')

        return _result + self.stack.close() + [ASTR.Jr('$ra')]

    @visitor.when(AST.Load)
    def visit(self, node: AST.Load):
        memory_dest = node.x
        data_label = node.y
                
        return [ASTR.LA('$t0', data_label)] + self.stack.write_local('$t0', memory_dest)

    @visitor.when(AST.Label)
    def visit(self, node: AST.Label):
        return [ASTR.Label(node.x)]

    @visitor.when(AST.GoTo)
    def visit(self,node:AST.GoTo):
        label = node.x
        return [ASTR.Jump (label)]

    @visitor.when(AST.Assign)
    def visit(self,node:AST.Assign):
        if node.x == node.y: return []
        if type(node.y) == type(int()): return [ASTR.LI('$s4', node.y)]
        memory_dest = node.x
        dir_value = node.y
        _result = self.stack.read_local('$t0', dir_value)
        return _result + self.stack.write_local('$t0', memory_dest)
    
    def call_magic_method(self, func, *memory_dir):
        result = self.stack.read_local('$s6', 'self', f'Guarda self')

        for i, param in enumerate(memory_dir[0: -1]):
            result += self.stack.read_local(f'$a{i}', param, f"Guarda el parametro {i} -> {param}")
        
        result.append(ASTR.Jal(func))
        return result + self.stack.write_local('$v0', memory_dir[-1])

    @visitor.when(AST.Sum)
    def visit(self,node:AST.Sum):
        return self.call_magic_method('__int__sum__', node.y, node.z, node.x)
    
    @visitor.when(AST.Rest)
    def visit(self,node:AST.Rest):
        return self.call_magic_method('__int__sub__', node.y, node.z, node.x)

    @visitor.when(AST.Mult)
    def visit(self,node:AST.Mult):
        return self.call_magic_method('__int__mul__', node.y, node.z, node.x)

    @visitor.when(AST.Div)
    def visit(self,node:AST.Div):
        return self.call_magic_method('__int__div__', node.y, node.z, node.x)

    @visitor.when(AST.Less)
    def visit(self,node:AST.Less):
        cmp = self.call_magic_method('__int__le__', node.y, node.z, node.x)  
        int_to_bool = self.call_magic_method('__bool__new__', node.x)
        return cmp + [ASTR.Move('$a0', '$v0')] + int_to_bool

    @visitor.when(AST.LessOrEqual)
    def visit(self,node:AST.LessOrEqual):
        cmp = self.call_magic_method('__int__leq__', node.y, node.z, node.x)  
        int_to_bool = self.call_magic_method('__bool__new__', node.x)
        return cmp + [ASTR.Move('$a0', '$v0')] + int_to_bool

    @visitor.when(AST.Complemnet)
    def visit(self,node:AST.Complemnet):
        return self.call_magic_method('__int__complement__', node.y, node.x)  

    @visitor.when(AST.Neg)
    def visit(self,node:AST.Neg):
        cmp = self.call_magic_method('__int__neg__', node.y, node.x)  
        int_to_bool = self.call_magic_method('__bool__new__', node.x)
        return cmp + [ASTR.Move('$a0', '$v0')] + int_to_bool
    
    @visitor.when(AST.IfGoTo)
    def visit(self,node:AST.IfGoTo):
        result = [ASTR.Header_Comment('Check Condition And Try Jump')]
        result += self.stack.read_local('$t0', node.x, f"Guarda el parametro 0 -> {node.x}")
        result += [ASTR.LW(f'$t1', "4($t0)", f"Lee la propiedad **value** del bool")]
        result += [ASTR.LI(f'$t0', 1, f"Carga un 1 para comparar")]
        result += [ASTR.Beq('$t0', '$t1', node.y)]
        return result

    @visitor.when(AST.Equals)
    def visit(self,node:AST.Equals):
        if 'int_eq' in node.y:
            cmp = self.call_magic_method('__int__eq__', node.y, node.z, node.x)  
            int_to_bool = self.call_magic_method('__bool__new__', node.x)
            return cmp + [ASTR.Move('$a0', '$v0')] + int_to_bool
        elif 'str_eq' in node.y:
            cmp = self.call_magic_method('__str__cmp__', node.y, node.z, node.x)  
            int_to_bool = self.call_magic_method('__bool__new__', node.x)
            return cmp + [ASTR.Move('$a0', '$v0')] + int_to_bool
        elif 'ref_eq' in node.y:
            _result = self.stack.read_local('$t0', node.y)
            _result += self.stack.read_local('$t1', node.z)
            _result += [ASTR.Seq('$a0','$t1','$t0')]
            return (_result + 
                self.call_magic_method('__int__new__', node.x) + 
                [ASTR.Move('$a0', '$v0')] + 
                self.call_magic_method('__bool__new__', node.x))

        assert False, "La comparacion no es correcta"

    @visitor.when(AST.CheckType)
    def visit(self, node: AST.CheckType):
        result = self.call_magic_method('__bool__check__type__', node.y, node.z, node.x)
        result  += [ASTR.Move('$a0', '$v0')] + self.call_magic_method('__int__new__', node.x)
        result += [ASTR.Move('$a0', '$v0')] + self.call_magic_method('__bool__new__', node.x)
        return result  

    @visitor.when(AST.TypeOf)
    def visit(self, node: AST.TypeOf):
        result = self.stack.read_local('$t0', node.y)
        result += [ASTR.LW('$t1', '($t0)', 'Lee la propiedad **type** de la instancia')]
        result += [ASTR.LW('$t0', '8($t1)', 'Lee la propiedad **parents** de la propiedad **type**')]
        return result + self.stack.write_local('$t0', node.x)

    @visitor.when(AST.Comment)
    def visit(self, node: AST.Comment):
        return [ASTR.Header_Comment(node.x)]