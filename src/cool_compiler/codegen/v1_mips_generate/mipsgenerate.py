from cool_compiler.codegen.v1_mips_generate.stack import Stack
from ...cmp import visitor
from ..v0_type_data_code import type_data_code_ast as AST
from . import mipsgenerate_ast as ASTR

class MipsGenerate: 
    def __init__(self, errors) -> None:
        self.func_list = ['main']
        self.native_fun = {
            "IO_out_string": ASTR.Out_String,
            "IO_in_int":ASTR.In_Int,
            "IO_in_string":ASTR.In_String,
            "IO_out_int":ASTR.Out_Int,
            "String_length":ASTR.Length,
            #"String_length":ASTR.Length,
            "String_concat": ASTR.Concat,


            "String_substr":ASTR.SubStr
,
            "Object_copy": ASTR.Copy,
            "Object_type_name":ASTR.Type_Name,
            "Object_abort": ASTR.Abort,
            "String_substr":ASTR.SubStr
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
                self.new_program.func[func] = self.native_fun[func]()
            else:
                self.visit(self.cil_func[func])
        
        for func in list(self.cil_func.keys()) + list(self.native_fun.keys()):
            if func in self.func_list: continue
            self.new_program.func[func] = ASTR.Func(func)
            self.new_program.func[func].cmd += [ASTR.Comment("Esta funcion no se invoca en la ejecucion del programa")]

        return self.new_program

    @visitor.when(AST.Function)
    def visit(self, node: AST.Function):
        new_func = ASTR.Func(node.name)
        self.stack = Stack(node)
        
        for param in node.param:
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

    @visitor.when(AST.Param)
    def visit(self, node: AST.Param):
        self.stack.list.append(node.x)
        return [ASTR.Header_Comment(f'Parametro {node.x} en stackpoiner + {self.stack.initial_index}')]  

    @visitor.when(AST.Local)
    def visit(self, node: AST.Local):
        self.stack.list.append(node.x)
        return [
            ASTR.AddI('$sp', '$sp', -4), 
            ASTR.Comment(
            f'Push local var {node.x} stackpointer {self.stack.initial_index}')
        ]

    @visitor.when(AST.ALLOCATE)
    def visit(self, node: AST.ALLOCATE):
        memory_dir = node.x
        _type = node.y

        stack_plus = self.stack.index(memory_dir)
        attr_list = self.cil_type[_type].attributes 
        _len = len(attr_list) * 4

        result = [
            ASTR.Header_Comment(f"Allocate a una class {_type} puntero en sp + {stack_plus}"),
        ]

        for i, attr in enumerate(attr_list):
            result.append(ASTR.Header_Comment(f'atributo {attr} en puntero + {i * 4}'))

        return result + [
            ASTR.LI('$a0', _len),
            ASTR.LI('$v0', 9),
            ASTR.SysCall(),
            ASTR.SW('$v0', f'{stack_plus}($sp)'),
            ASTR.Comment(f'Guardando en la pila el pintero de la instancia de la clase {_type}')
        ]

    @visitor.when(AST.GetAttr)
    def visit(self, node: AST.GetAttr):
        memory_dest = node.x
        memory_dir_instance = node.y
        attr_name = node.z.split('@')
        _type = attr_name[0]
        attr = attr_name[1]

        stack_plus_dest = self.stack.index(memory_dest)
        stack_plus_instance = self.stack.index(memory_dir_instance)
        attr_plus = self.cil_type[_type].attributes.index(attr) * 4 

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
        if node.y == 'type_name': 
            attr_plus = 0
            attr = 'type_name'
            _type = "SELF"
        else: 
            attr_name = node.y.split('@')
            _type = attr_name[0]
            attr = attr_name[1]
            attr_plus = self.cil_type[_type].attributes.index(attr) * 4

        memory_dir_instance = node.x
        memory_dir_value = node.z

        stack_plus_dir_value = self.stack.index(memory_dir_value)
        stack_plus_instance = self.stack.index(memory_dir_instance)

        return [
            ASTR.LW('$t0', f'{stack_plus_instance}($sp)'),
            ASTR.Comment(f'Buscando en la pila la variable {node.x} y guarda la direccion a la que apunta'),
            ASTR.LW('$t1', f'{stack_plus_dir_value}($sp)'),
            ASTR.Comment(f'Buscando el valor que se va a guardar en la propiedad'),
            ASTR.SW('$t1', f'{attr_plus}($t0)'),
            ASTR.Comment(f'Seteando el valor {memory_dir_value} en la direccion de la memoria del la propiedad {attr} del objeto de typo {_type}'),
        ]

    @visitor.when(AST.Arg)
    def visit(self, node: AST.Arg):
        memory_dir = node.x
        
        stack_plus = self.stack.index(memory_dir)
        self.stack.push(memory_dir)

        return [
            ASTR.LW('$t0', f'{stack_plus}($sp)'),
            ASTR.Comment(f'Saca de la pila {node.x}'),
            ASTR.AddI('$sp', '$sp', -4),
            ASTR.SW('$t0', '0($sp)'),
            ASTR.Comment(f'Mete para la pila {node.x}'),
        ]        

    def call(self, func, memory_dest):
        self.stack.clean()
        stack_plus = self.stack.index(memory_dest)

        return [
            ASTR.JAL(func),
            ASTR.Comment(f'Call a la function {func}'),
            ASTR.SW('$s0', f'{stack_plus}($sp)' ),
            ASTR.Comment(f'Save el resultado de la funcion que esta en $s0 pa la pila'),
        ]
   
    @visitor.when(AST.SimpleCall)
    def visit(self, node: AST.SimpleCall):
        if not node.x in self.func_list: self.func_list.append(node.x)
        return self.call(node.x, 'self')[0: -2]

    @visitor.when(AST.VCall)
    def visit(self, node: AST.VCall):
        memory_dest = node.x
        _type = node.y
        func = self.cil_type[_type].methods[node.z]
        if not func in self.func_list: self.func_list.append(func)

        return self.call(func, memory_dest)

    @visitor.when(AST.New)
    def visit(self, node: AST.New):
        func = f'new_ctr_{node.y}'
        if not func in self.func_list: self.func_list.append(func)
        return self.call(f'new_ctr_{node.y}', node.x)

    @visitor.when(AST.Call)
    def visit(self, node: AST.Call):
        memory_dest = node.x
        instance_stack = self.stack.index(node.y)
        _type, func_name = node.z.split('@')

        self.func_list += [func for func in self.cil_func.keys() 
            if func_name in func and  not func in self.func_list]

        self.func_list += [func for func in self.native_fun.keys() 
            if func_name in func and  not func in self.func_list]

        func_address = self.cil_type[_type].method_list.index(func_name) * 4 + 12
        result = [
            ASTR.LW('$t0', f'{instance_stack}($sp)'),
            ASTR.Comment(f"Sacando la instancia de la pila (en {instance_stack - self.stack.local_push * 4}) de una clase que hereda de {_type}"),
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
        stack_plus = self.stack.index(memory_dest)

        return [
            ASTR.LW('$s0', f'{stack_plus}($sp)'),
            ASTR.Comment("Envia el resultado de la funcion en $s0"),
            ASTR.LW('$ra', '0($sp)'),#f'{(len(self.stack) - 1)* 4}($sp)'),
            ASTR.Comment("Lee el $ra mas profundo de la pila para retornar a la funcion anterior"),
            ASTR.AddI('$sp', '$sp', self.stack.close()),
            ASTR.Comment("Limpia la pila"),
            ASTR.JR('$ra')
        ]

    @visitor.when(AST.Load)
    def visit(self, node: AST.Load):
        memory_dest = node.x
        data_label = node.y
                
        stack_plus = self.stack.index(memory_dest)

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

        stack_plus_opr_1 = self.stack.index(dir_cmp1)
        stack_plus_opr_2 = self.stack.index(dir_cmp2)
        stack_plus_dest = self.stack.index(memory_dest)

        return [ ASTR.LW('$t1', f'{stack_plus_opr_1}($sp)')  ,
                 ASTR.Comment(f"carga en $t1 {dir_cmp1}  de la pos {stack_plus_opr_1} "),
                 ASTR.LW ('$t2', f'{stack_plus_opr_2}($sp)'),
                 ASTR.Comment(f"carga en $t2  {dir_cmp2} de la pos {stack_plus_opr_2} "),
                 ASTR.SEQ ('$t3','$t2','$t1'),
                 ASTR.Comment(f"$t3 = {dir_cmp1}  $t0  == {dir_cmp2} $ t1" ),
                 ASTR.SW ('$t3',f'{stack_plus_dest}($sp)'),
                 ASTR.Comment(f"Pon en la posicion {stack_plus_dest} el valor de $t3")
        ]

    @visitor.when(AST.CmpStr)
    def visit(self,node:AST.CmpStr):
        memory_dest = node.x
        memory_str1 = node.y
        memory_str2 = node.z

        stack_plus_str1 = self.stack.index(memory_str1)
        stack_plus_str2 = self.stack.index(memory_str2)
        stack_plus_dest = self.stack.index(memory_dest)

        return [ASTR.LW('$t0',f'{stack_plus_str1}'),
                ASTR.Comment(f"Si no viene como funcion pon el string {memory_str1} de la posicion {stack_plus_str1}"),
                ASTR.LW('$t1',f'{stack_plus_str2}'),
                ASTR.Comment(f"Si no viene como funcion pon el string {memory_str2} de la posicion {stack_plus_str2}"),
                ASTR.Compare_String(),
                ASTR.SW ('$s0', f'{stack_plus_dest}'),
                ASTR.Comment(f"Como no retorna sigue lineal entoces en $s0 esta el resultado y se pone en  {stack_plus_dest}")
        ]

    @visitor.when(AST.Less)
    def visit (self,node:AST.Less):
        memory_dest = node.x
        dir_cmp1 = node.y
        dir_cmp2 = node.z

        stack_plus_opr_1 = self.stack.index(dir_cmp1)
        stack_plus_opr_2 = self.stack.index(dir_cmp2)
        stack_plus_dest = self.stack.index(memory_dest)

        return [ ASTR.LW('$t1', f'{stack_plus_opr_1}($sp)')  ,
                 ASTR.Comment(f"carga en $t1  {dir_cmp1} lo que hay en {stack_plus_opr_1} "),
                 ASTR.LW ('$t2', f'{stack_plus_opr_2}($sp)'),
                 ASTR.Comment(f"carga en $t2 {dir_cmp2} lo que hay en {stack_plus_opr_2} "),
                 ASTR.SLT ('$t3','$t1','$t2'),
                 ASTR.Comment(f"$t3 = $t1 < $ t2 osea {dir_cmp1} < {dir_cmp2}" ),
                 ASTR.SW ('$t3',f'{stack_plus_dest}($sp)'),
                 ASTR.Comment(f"Pon en la posicion {stack_plus_dest} el valor de $t3")
                ]

    @visitor.when(AST.LessOrEqual)
    def visit (self,node:AST.LessOrEqual):
        memory_dest = node.x
        dir_cmp1 = node.y
        dir_cmp2 = node.z

        stack_plus_opr_1 = self.stack.index(dir_cmp1)
        stack_plus_opr_2 = self.stack.index(dir_cmp2)
        stack_plus_dest = self.stack.index(memory_dest)

        return [ ASTR.LW('$t1', f'{stack_plus_opr_1}($sp)')  ,
                 ASTR.Comment(f"carga en $t1 {dir_cmp1} lo que hay en {stack_plus_opr_1} "),
                 ASTR.LW ('$t2', f'{stack_plus_opr_2}($sp)'),
                 ASTR.Comment(f"carga en $t2 {dir_cmp2} lo que hay en {stack_plus_opr_2} "),
                 ASTR.SLE ('$t3','$t1','$t2'),
                 ASTR.Comment(f"$t3 = $t1 <= $t2 osea {dir_cmp1} <= {dir_cmp2}" ),
                 ASTR.SW ('$t3',f'{stack_plus_dest}($sp)'),
                 ASTR.Comment(f"Pon en la posicion {stack_plus_dest} el valor de $t3")
                ]

    @visitor.when(AST.Assign)
    def visit(self,node:AST.Assign):
        memory_dest = node.x
        dir_value = node.y
        stack_plus = self.stack.index(memory_dest)

        if type(dir_value) in [type(int()), type(float())]:
            return [ 
                     ASTR.LI('$t0' , str(dir_value)),
                     ASTR.Comment(f"Guarda el numbero que se va a asignar"),
                     ASTR.SW ('$t0',f'{stack_plus}($sp)'),
                     ASTR.Comment(f"Escribe en la pila el numero que se le asigno a {memory_dest}")
                   ]
        else:
            stack_plus_dir_value = self.stack.index(dir_value)
            return [ 
                     ASTR.LW ('$t0',f'{stack_plus_dir_value}($sp)'),
                     ASTR.Comment(f"Lee de la pila {dir_value} en {stack_plus_dir_value} para assignar"),
                     ASTR.SW ('$t0',f'{stack_plus}($sp)'),
                     ASTR.Comment(f"Escribe en la pila el valor que se le asigno a {memory_dest}")
                   ]           

    @visitor.when(AST.Neg)
    def visit(self,node:AST.Neg):
        memory_dest = node.x
        memory_op1  = node.y
        stack_plus_memory_dest = self.stack.index(memory_dest)
        stack_plus_opr_1 = self.stack.index(memory_op1)

        return [
                ASTR.LW ('$t0',f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment(f"Carga la pos {stack_plus_opr_1} en $t0"),
                ASTR.AddI ('$t1','$t0',-1 ),
                ASTR.Comment("$t1 =  $t0 + (-1)"),
                ASTR.MUL ('$t0','$t1',-1),
                ASTR.Comment("$t0 =  $t1 * (-1)"),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment(f"poner en la posicion {stack_plus_memory_dest} el contenido de $t0")
                ]                   

    @visitor.when(AST.Complemnet)
    def visit(self, node: AST.Complemnet):
        pass

    @visitor.when(AST.Sum)
    def visit(self,node:AST.Sum):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack.index(memory_dest)
        stack_plus_opr_1 = self.stack.index(memory_op1)
        stack_plus_opr_2 = self.stack.index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment(f"poner en registro $t0 {memory_op1} lo que hay en {stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment(f"poner en registro $t1 {memory_op2} lo que hay en {stack_plus_opr_2}"),
                ASTR.Add('$t0' , '$t0','$t1'),
                ASTR.Comment("en $t0 pon el resultado de la suma"),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment(f"poner en la posicion {stack_plus_memory_dest} el resultado ")
                ]

    @visitor.when(AST.Rest)
    def visit(self,node:AST.Rest):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack.index(memory_dest)
        stack_plus_opr_1 = self.stack.index(memory_op1)
        stack_plus_opr_2 = self.stack.index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment(f"poner en registro $t0 {memory_op1} lo que hay en {stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment("poner en registro $t1 {memory_op2} lo que hay en f'{stack_plus_opr_2}"),
                ASTR.SUB('$t0' , '$t0','$t1'),
                ASTR.Comment("poner en registro $t0 la RESTA"),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment(f"poner en {stack_plus_memory_dest} el resultado de la RESTA "),

                ]

    @visitor.when(AST.Mult)
    def visit(self , node :AST.Mult):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack.index(memory_dest)
        stack_plus_opr_1 = self.stack.index(memory_op1)
        stack_plus_opr_2 = self.stack.index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment(f"poner en registro $t0  {memory_op1} lo que hay en {stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment(f"poner en registro $t1 {memory_op2} lo que hay en {stack_plus_opr_2}"),
                ASTR.MUL('$t0' , '$t0','$t1'),
                ASTR.Comment("poner en registro $t0 la MULT "),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment(f"poner en {stack_plus_memory_dest} el resultado de la multiplicacion "),

                ]


    @visitor.when(AST.Div)
    def visit (self,node:AST.Div):
        memory_dest=node.x
        memory_op1=node.y
        memory_op2=node.z

        stack_plus_memory_dest = self.stack.index(memory_dest)
        stack_plus_opr_1 = self.stack.index(memory_op1)
        stack_plus_opr_2 = self.stack.index(memory_op2)

        return [ASTR.LW('$t0', f'{stack_plus_opr_1}($sp)'),
                ASTR.Comment(f"poner en registro $t0 {memory_op1} lo que hay en {stack_plus_opr_1}"),
                ASTR.LW('$t1', f'{stack_plus_opr_2}($sp)'),
                ASTR.Comment("poner en registro $t1 {memory_op2} lo que hay en f'{stack_plus_opr_2}"),
                ASTR.DIV('$t0' , '$t0','$t1'),
                ASTR.Comment("poner en registro $t0 la DIV "),
                ASTR.SW ('$t0', f'{stack_plus_memory_dest}($sp)'),
                ASTR.Comment(f"poner en {stack_plus_memory_dest} el resultado de la Division entera el resto esta en LO "),
                ]

    @ visitor.when(AST.IfGoTo)
    def visit(self,node:AST.IfGoTo):
        memory_cmp = node.x
        label_memory = node.y

        stack_plus_memory_cmp = self.stack.index(memory_cmp)
       
        return [ASTR.LI("$t0" ,1),
                ASTR.Comment("Cargar 1 a $t0 pa comparar"),
                ASTR.LW("$t1", f'{stack_plus_memory_cmp}($sp)' ),
                ASTR.Comment(f"Cargar el valor {memory_cmp}  de la pos  {stack_plus_memory_cmp} a $t1 pa comparar"),
                ASTR.BEQ("$t0","$t1", label_memory),
                ASTR.Comment(f"if $t1==$t0 then jump {label_memory}")
                ]

    @ visitor.when(AST.Label) 
    def visit(self,node:AST.Label):
        return [ASTR.Label(node.x),
                ASTR.Comment(f"Crea el label {node.x} ")
                ]  

    @visitor.when(AST.CheckType)
    def visit(self,node:AST.CheckType):
        memory_dir = node.x
        memory_instance = node.y
        type_name = node.z

        stack_plus_memory_dir = self.stack.index(memory_dir)
        stack_plus_memory_instance = self.stack.index(memory_instance)
        
        return [
                ASTR.LW('$s2',f'{stack_plus_memory_instance}($sp)'),
                ASTR.Comment(f' pon en $s2  {memory_instance} el contenido de {stack_plus_memory_instance}($sp)'),
                ASTR.LW('$a1', type_name),
                ASTR.Comment(f"guarda en $a1 {type_name} "),
                ASTR.JAL('Contain'),
                ASTR.Comment("Salta para Contain"),
                ASTR.SW ('$s0',f'{stack_plus_memory_dir}($sp)'),
                ASTR.Comment(f"Guarda en la pos {stack_plus_memory_dir}($sp) el contenido de $s0")
          ]

    @ visitor.when(AST.GoTo)
    def visit(self,node:AST.GoTo):
        label = node.x
        return [ASTR.Jump (label),
                ASTR.Comment(f"Salta para {label} ")
                ]


    @visitor.when(AST.Complemnet)
    def visit (self,node:AST.Complemnet):
        memory_dest = node.x
        memory_number = node.y

        stack_plus_memory_dest= self.stack.index(memory_dest)
        stack_plus_memory_number = self.stack.index(memory_number)

        # return [ASTR.LW('$t1', f'{stack_plus_memory_number}($sp)'),
        #         ASTR.MUL('$s0','$t1',-1),
        #         ASTR.SW ('$s0', f'{stack_plus_memory_dest}($sp)')
            

                
        #         ]
        return [ASTR.LI ('$t0',4294967295),
                ASTR.LW ('$t1', f'{stack_plus_memory_number}($sp)'),
                ASTR.XOR ("$s0" , '$t0','$t1'),
                ASTR.Add ('$s0' ,'$s0' ,'1'),
                ASTR.SW ('$s0', f'{stack_plus_memory_dest}($sp)')
                ]


