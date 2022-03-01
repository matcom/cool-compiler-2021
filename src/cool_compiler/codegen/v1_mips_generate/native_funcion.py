import inspect
from . import mips_generate_ast as ASTR
from ..v0_cool_to_cil import cool_to_cil_ast as AST
from .stack import Stack


class CoolNativeFunctions:
    def __init__(self) -> None:
        self.method_list = [            
            "IO_out_string",
            "IO_in_int",
            "IO_in_string",
            "IO_out_int",
            "String_length",
            "String_concat",
            "String_substr",
            "Object_copy",
            "Object_type_name",
            "Object_abort"]

    def call(self, func):
        method_to_call = getattr(self, func.lower())
        self.node = AST.Function(func)
        return method_to_call()

    # @property
    # def method_list(self):
    #     return  [method for method in inspect.getmembers(self, predicate=inspect.ismethod)]
    
    def call_magic_method(self, func,*memory_dir):
        new_func = ASTR.Func(self.node.name)
        self.node.param = memory_dir
        self.stack = Stack(self.node)
        result = []

        for param in ['self'] + list(self.node.param):
            result += self.stack.def_param(param)
        
        result += self.stack.def_local('$ra')
        result += self.stack.write_local('$ra','$ra', f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {self.node.name}")

        result += self.stack.read_local('$s6', 'self', f'Guarda self')

        for i, param in enumerate(memory_dir):
            result += self.stack.read_local(f'$a{i}', param, f"Guarda el parametro {i} -> {param}")
        
        result.append(ASTR.Jal(func))
        result += self.stack.read_local('$ra', '$ra')
        result += self.stack.close()
        result.append(ASTR.Jr('$ra'))
        new_func.cmd = result
        return new_func

    def io_out_string(self):
        return self.call_magic_method('__str__print__','string')

    def io_out_int(self):
        return self.call_magic_method('__int__print__','number')

    def io_in_string(self):
        return self.call_magic_method('__str__input__')

    def io_in_int(self):
        return self.call_magic_method('__int__input__')


    def string_length(self):
        return self.call_magic_method('__str__length__')

    def string_concat(self):
        return self.call_magic_method('__str__concat__', 'string')

    def string_substr(self):
        return self.call_magic_method('__str__substr__', 'index', 'count')

    def object_abort(self):
        new_func = ASTR.Func(self.node.name)
        self.stack = Stack(self.node)
        result = self.stack.def_param('self')
        result += self.stack.def_local('$ra')
        result += self.stack.write_local('$ra','$ra', f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {self.node.name}")
        result += self.stack.read_local('$s6', 'self', f'Guarda self')

        result.append(ASTR.LA('$a0', '_______error______'))
        result.append(ASTR.Jal('__str__new__'))
        result.append(ASTR.Move('$a0', '$v0'))
        result.append(ASTR.Jal('__str__print__', 'Print "Abort called from class "'))

        result.append(ASTR.LW('$t0', '($s6)', 'Read type property of self'))
        result.append(ASTR.LW('$a0', '($t0)', 'Read type_name of self type'))
        result.append(ASTR.Jal('__str__new__'))
        result.append(ASTR.Move('$a0', '$v0'))
        result.append(ASTR.Jal('__str__print__', 'Type class"'))

        result.append(ASTR.LA('$a0', '_______endline_______'))
        result.append(ASTR.Jal('__str__new__'))
        result.append(ASTR.Move('$a0', '$v0'))
        result.append(ASTR.Jal('__str__print__', 'Print "endline"'))

        new_func.cmd = result + [ASTR.LI('$v0', 10), ASTR.SysCall()]
        return new_func

    def object_type_name(self):
        new_func = ASTR.Func(self.node.name)
        self.stack = Stack(self.node)
        result = self.stack.def_param('self')
        result += self.stack.def_local('$ra')
        result += self.stack.write_local('$ra','$ra', f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {self.node.name}")
        result += self.stack.read_local('$s6', 'self', f'Guarda self')

        result.append(ASTR.LW('$t0', '($s6)', 'Read type property of self'))
        result.append(ASTR.LW('$a0', '($t0)', 'Read type_name of self type'))
        result.append(ASTR.Jal('__str__new__'))

        result += self.stack.read_local('$ra', '$ra')
        result += self.stack.close()
        result.append(ASTR.Jr('$ra'))
        new_func.cmd = result
        return new_func


    def object_clone(self):
        new_func = ASTR.Func(self.node.name)
        self.stack = Stack(self.node)
        result = self.stack.def_param('self')
        result += self.stack.def_local('$ra')
        result += self.stack.write_local('$ra','$ra', f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {self.node.name}")
        result += self.stack.read_local('$s6', 'self', f'Guarda self')

        result.append(ASTR.LiteralMips("""
        lw $t0, ($s6)       #Read type property of self
        lw $t1, 4($t0)      #Read type_account of self types
        mul $t1, $t1, 4

        move $a0, $t1       #tamaño que ocupa en el heap 
        li $v0, 9        
        syscall             #En $v0 la nueva instancia

        move $t0, $s6       #Crear puntero a self
        move $t2, $v0       #Crear puntero al clone
        li $t3, 0           #Crear contador de propiedades 

        __object__loop_clone__: 
            lw $t5, ($t0)                   #Lee una propiedad de self
            sw $t5, ($t2)                   #Escribe la propiedad en el clone
            addi $t3, $t3, 4                #Aumenta el contador de props 
            beq  $t3, $t1, __end__clone__   
            addi $t0, $t0, 4                #Mueve el puntero de self 
            addi $t3, $t3, 4                #Mueve el puntero del clone 
            j __object__loop_clone__
        
        __end__clone__:
        """))


        result += self.stack.read_local('$ra', '$ra')
        result += self.stack.close()
        result.append(ASTR.Jr('$ra'))
        new_func.cmd = result
        return new_func





