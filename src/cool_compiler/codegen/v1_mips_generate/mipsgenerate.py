from ...cmp import visitor
from ..v0_type_data_code import type_data_code_ast as AST
from . import mipsgenerate_ast as ASTR

class MipsGenerate: 
    def __init__(self, errors) -> None:
        self.func_list = ['new_ctr_Main']
        self.native_fun = {
            "IO_out_string": ASTR.Out_String
        }

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
            if func in self.native_fun: 
                self.new_program.func[func]  = self.native_fun[func]()
            else:
                self.visit(self.cil_func[func])
        
        return self.new_program

    @visitor.when(AST.Function)
    def visit(self, node: AST.Function):
        new_func = ASTR.Func(node.name if not node.name == 'new_ctr_Main' else 'main')
        self.stack = []
        self.final_len_stack = len(node.param) + len(node.local) + 2
        self.local_push = 0
        
        for param in [AST.Param('Return $ra')] + node.param:
            new_func.cmd += self.visit(param)

        for _local in node.local + [AST.Local('$ra')]:
            new_func.cmd += self.visit(_local)

        new_func.cmd += (
            [ASTR.SW('$ra', "0($sp)")] + 
            [ASTR.Comment(f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {node.name}")])

        for expr in node.expr:
            new_func.cmd += self.visit(expr)

        self.new_program.func[new_func.name] = new_func

    #stack_pointer = 0
    #bsp = self.base_stack_pointer
    def stack_index(self, name):
        return (len(self.stack) - self.stack.index(name) - 1) * 4

    @visitor.when(AST.Param)
    def visit(self, node: AST.Param):
        self.stack.append(node.x)
        return [ASTR.Header_Comment(f'Parametro {node.x} en stackpoiner + {(self.final_len_stack - len(self.stack)) * 4}')]  

    @visitor.when(AST.Local)
    def visit(self, node: AST.Local):
        self.stack.append(node.x)
        return [
            ASTR.AddI('$sp', '$sp', -4), 
            ASTR.Comment(
            f'Push local var {node.x} stackpointer {(self.final_len_stack - len(self.stack)) * 4}')
        ]

    @visitor.when(AST.ALLOCATE)
    def visit(self, node: AST.ALLOCATE):
        memory_dir = node.x
        _type = node.y

        stack_plus = self.stack_index(memory_dir)
        attr_list = self.cil_type[_type].attributes 
        _len = len(attr_list) * 4 + 4

        result = [
            ASTR.Header_Comment(f"Allocate a una class {_type} puntero en sp + {stack_plus}"),
            ASTR.Header_Comment(f"atributo @type en puntero + 0"),
        ]

        for i, attr in enumerate(attr_list):
            result.append(ASTR.Header_Comment(f'atributo {attr} en puntero + {(i + 1) * 4}'))

        return result + [
            ASTR.LI('$a0', _len),
            ASTR.LI('$v0', 9),
            ASTR.SysCall(),
            ASTR.SW('$v0', f'{stack_plus}($sp)')
        ]

    @visitor.when(AST.GetAttr)
    def visit(self, node: AST.GetAttr):
        memory_dest = node.x
        memory_dir_instance = node.y
        attr_name = node.z.split('@')
        _type = attr_name[0]
        attr = attr_name[1]

        stack_plus_dest = self.stack_index(memory_dest)
        stack_plus_instance = self.stack_index(memory_dir_instance)
        attr_plus = self.cil_type[_type].attributes.index(attr) * 4 + 4

        return [
            ASTR.LW('$t0', f'{stack_plus_instance}($sp)'),
            ASTR.Comment(f'Buscando la instancia de la clase {_type} en la pila'),
            ASTR.LW('$t1', f'{attr_plus}($t0)'),
            ASTR.Comment(f'Buscando el valor de la propiedad {attr}'),
            ASTR.SW('$t1', f'{stack_plus_dest}($sp)'),
            ASTR.Comment(f'Salvando el valor de la propiedad {attr} en la pila en el valor local {memory_dest}'),
        ]
    
    @visitor.when(AST.SetAttr)
    def visit(self, node: AST.SetAttr):
        if node.y == 'type': 
            attr_plus = 0
        else: 
            attr_name = node.y.split('@')
            _type = attr_name[0]
            attr = attr_name[1]
            attr_plus = self.cil_type[_type].attributes.index(attr) * 4 + 4

        memory_dir_instance = node.x
        memory_dir_value = node.z

        stack_plus_dir_value = self.stack_index(memory_dir_value)
        stack_plus_instance = self.stack_index(memory_dir_instance)

        return [
            ASTR.LW('$t0', f'{stack_plus_instance}($sp)'),
            ASTR.Comment(f'Buscando la instancia en la pila {node.x}'),
            ASTR.LW('$t1', f'{stack_plus_dir_value}($sp)'),
            ASTR.Comment(f'Buscando el valor que se va a guardar en la propiedad'),
            ASTR.SW('$t1', f'{attr_plus}($t0)'),
            ASTR.Comment(f'Seteando el valor en la direccion de la memoria del objeto'),
        ]

    @visitor.when(AST.Arg)
    def visit(self, node: AST.Arg):
        memory_dir = node.x
        
        stack_plus = self.stack_index(memory_dir)
        self.local_push += 1
        self.stack.append(memory_dir)

        return [
            ASTR.LW('$t0', f'{stack_plus}($sp)'),
            ASTR.Comment(f'Saca de la pila {node.x}'),
            ASTR.AddI('$sp', '$sp', -4),
            ASTR.SW('$t0', '0($sp)'),
            ASTR.Comment(f'Mete para la pila {node.x}'),
        ]        

    def call(self, func, memory_dest):
        self.stack = self.stack[0: len(self.stack) - self.local_push]
        self.local_push = 0
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.JAL(func),
            ASTR.Comment(f'Call a la function {func}'),
            ASTR.SW('$s0', f'{stack_plus}($sp)' ),
            ASTR.Comment(f'Save el resultado de la funcion que esta en $s0 pa la pila'),
        ]

    @visitor.when(AST.VCall)
    def visit(self, node: AST.VCall):
        memory_dest = node.x
        _type = node.y
        func = self.cil_type[_type].methods[node.z]
        self.func_list.append(func)

        return self.call(func, memory_dest)

    @visitor.when(AST.New)
    def visit(self, node: AST.New):
        func = f'new_ctr_{node.y}'
        self.func_list.append(func)
        return self.call(f'new_ctr_{node.y}', node.x)

    @visitor.when(AST.Call)
    def visit(self, node: AST.Call):
        memory_dest = node.x
        instance_stack = self.stack_index(node.y)
        _type, func_name = node.z.split('@')

        self.func_list += [func for func in self.cil_func.keys() 
            if func_name in func and  not func in self.func_list]

        func_address = self.cil_type[_type].method_list.index(func_name) * 4 + 4
        result = [
            ASTR.LW('$t0', f'{instance_stack}($sp)'),
            ASTR.Comment(f"Sacando la instancia de la pila (en {instance_stack - self.local_push * 4}) de una clase que hereda de {_type}"),
            ASTR.LW('$t1', '0($t0)'),
            ASTR.Comment(f"Leyendo el tipo de la instancia que hereda de {_type}"),
            ASTR.LW('$t3', f'{func_address}($t1)'),
            ASTR.Comment(f"Buscando el metodo dinamico para la funcion {func_name}")
        ]
        return result + self.call('$t3', memory_dest)

    @visitor.when(AST.Return)
    def visit(self, node: AST.Return):
        if node.x == 0: 
            return [ASTR.LI('$v0', 10), ASTR.SysCall()]
        
        memory_dest = node.x
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.LW('$s0', f'{stack_plus}($sp)'),
            ASTR.Comment("Envia el resultado de la funcion en $s0"),
            ASTR.LW('$ra', f'{(len(self.stack) - 1)* 4}($sp)'),
            ASTR.Comment("Lee el $ra mas profundo de la pila para retornar a la funcion anterior"),
            ASTR.AddI('$sp', '$sp', len(self.stack) * 4),
            ASTR.Comment("Limpia la pila"),
            ASTR.JR('$ra')
        ]

    @visitor.when(AST.Load)
    def visit(self, node: AST.Load):
        memory_dest = node.x
        data_label = node.y
                
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.LA('$t0', data_label),
            ASTR.SW('$t0', f'{stack_plus}($sp)')
        ]

    @visitor.when(AST.Comment)
    def visit(self, node: AST.Comment):
        return [ASTR.Comment(node.x)]

    @visitor.when(AST.CmpInt)
    def visit(self,node:AST.CmpInt):
        memory_dest = node.x
        dir_cmp1 = node.y
        dir_cmp2 = node.z

        stack_plus_opr_1 = self.stack_index(dir_cmp1)
        stack_plus_opr_2 = self.stack_index(dir_cmp2)
        stack_plus_dest = self.stack_index(memory_dest)

        return [ ASTR.LW('$t1', f'{stack_plus_opr_1}($sp)')  ,
                 ASTR.Comment("carga en $t1 lo que hay en f'{stack_plus_opr_1} "),
                 ASTR.LW ('$t2', f'{stack_plus_opr_2}($sp)'),
                 ASTR.Comment("carga en $t2 lo que hay en f'{stack_plus_opr_2} "),
                 ASTR.SEQ ('$t3','$t2','$t1'),
                 ASTR.Comment("$t3 = $t2 == $ t1" ),
                 ASTR.SW ('$t3',f'{stack_plus_dest}($sp)'),
                 ASTR.Comment("Pon en la posicion f's{stack_plus_opr_1} el valor de $t3")
        ]

    @visitor.when(AST.Assign)
    def visit(self,node:AST.Assign):
        memory_dest = node.x
        dir_value = node.y
        stack_plus = self.stack_index(memory_dest)

        if(type(dir_value)==type(int()) or type(dir_value)==type(float())):
            return [ 
                     ASTR.LI('$t0' , str(dir_value)),
                     ASTR.Comment("pon en $t0  f'{dir_value}  "),
                     ASTR.SW ('$t0',f'{stack_plus}($sp)'),
                     ASTR.Comment("pon en la posicion  f'{dir_value} el valor $t0  ")
                   ]
        else:
            stack_plus_dir_value = self.stack_index(dir_value)
            return [ 
                     ASTR.LW ('$t0',f'{stack_plus_dir_value}($sp)'),
                     ASTR.Comment("pon en $t0  el contenido de la pos  f'{stack_plus_dir_value}  "),
                     ASTR.SW ('$t0',f'{stack_plus}($sp)'),
                     ASTR.Comment("pon en la pos  f'{stack_plus_dir_value}  el valor de $t0")
                   ]           

    @visitor.when(AST.Neg)
    def visit(self,node:AST.Neg):
        memory_dest = node.x
        memory_op1  = node.y
        stack_plus_memory_dest = self.stack_index(memory_dest)
        stack_plus_opr_1 = self.stack_index(memory_op1)

        return [
                ASTR.LW ('$t0',f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment("Carga la pos f'{stack_plus_opr_1} en $t0"),
                ASTR.AddI ('$t1','$t0',-1 ),
                ASTR.Comment("$t1 =  $t0 + (-1)"),
                ASTR.MUL ('$t0','$t1',-1),
                ASTR.Comment("$t0 =  $t1 * (-1)"),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment("poner en la posicion f'{stack_plus_memory_dest} el contenido de $t0")


                ]                   

    @ visitor.when(AST.Sum)
    def visit(self,node:AST.Sum):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack_index(memory_dest)
        stack_plus_opr_1 = self.stack_index(memory_op1)
        stack_plus_opr_2 = self.stack_index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment("poner en registro $t0 lo que hay en f'{stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment("poner en registro $t1 lo que hay en f'{stack_plus_opr_2}"),
                ASTR.Add('$t0' , '$t0','$t1'),
                ASTR.Comment("en $t0 pon el resultado de la suma"),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment("poner en la posicion f'{stack_plus_memory_dest} el resultado ")
                ]

    @ visitor.when(AST.Rest)
    def visit(self,node:AST.Rest):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack_index(memory_dest)
        stack_plus_opr_1 = self.stack_index(memory_op1)
        stack_plus_opr_2 = self.stack_index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment("poner en registro $t0 lo que hay en f'{stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment("poner en registro $t1 lo que hay en f'{stack_plus_opr_2}"),
                ASTR.SUB('$t0' , '$t0','$t1'),
                ASTR.Comment("poner en registro $t0 la suma "),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment("poner en f'{stack_plus_memory_dest} el resultado de la suma "),

                ]

    @ visitor.when(AST.IfGoTo)
    def visit(self,node:AST.IfGoTo):
        memory_cmp = node.x
        label_memory = node.y

        stack_plus_memory_cmp = self.stack_index(memory_cmp)
       
        return [ASTR.LI("$t0" ,1),
                ASTR.Comment("Cargar 1 a $t0 pa comparar"),
                ASTR.LW("$t1", f'{stack_plus_memory_cmp}($sp)' ),
                ASTR.Comment("Cargar el valor de la pos  f'{stack_plus_memory_cmp} a $t1 pa comparar"),
                ASTR.BEQ("$t0","$t1", label_memory),
                ASTR.Comment("if $t1==$t0 then jump f'{label_memory}")
                ]

    @ visitor.when(AST.Label) 
    def visit(self,node:AST.Label):
        return [ASTR.Label(node.x),
                ASTR.Comment("Crea el label f'{node.x} ")
                ]  

    @ visitor.when(AST.GoTo)
    def visit(self,node:AST.GoTo):
        label = node.x
        return [ASTR.Jump (label),
                ASTR.Comment("Salta para f{label} ")
                ]
