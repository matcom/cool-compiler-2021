from cool.cil_builder.cil_ast import * 
from cool.semantic import visitor
from cool.utils.Errors.semantic_errors import *
from cool.semantic.semantic import *


class BaseCILToMIPSVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.label_id = 0

        self.text_section = ".text\n"
        self.text_section += "main:\n"
        self.data_section = ".data\n"
        self.mips_type = ""
        self.type_offset = {}
        self.attribute_offset = {}
        self.method_offset = {}
        self.method_original = {}
        self.var_offset = {}
        self.type_size = {} #quantity of attr. of that type
        

    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions

    def fill_dotdata_with_errors(self):
        self.data_section+= '''
#Errors
call_void_error: .asciiz "Runtime Error: A dispatch (static or dynamic) on void\n"
case_void_expr: .asciiz "Runtime Error: A case on void.\n"
case_branch_error: .asciiz "Runtime Error: Execution of a case statement without a matching branch.\n"
zero_division: .asciiz "Runtime Error: Division by zero.\n"
substring_out_of_range: .asciiz "Runtime Error: Substring out of range.\n"
heap_overflow: .asciiz "Runtime Error: Heap overflow.\n"
'''
    def fill_dottext_with_errors(self):
        self.text_section+= '\n\n'
        self.text_section+= 'error_call_void:\n' #dispatch error 1
        self.text_section+= 'la $a0,call_void_error\n'
        self.text_section+= 'j print_error\n'

        self.text_section+= 'error_expr_void:\n' #case error 2
        self.text_section+= 'la $a0,case_void_expr\n'
        self.text_section+= 'j print_error\n'
        
        self.text_section+= 'error_branch:\n' #branch error 3
        self.text_section+= 'la $a0,case_branch_error\n'
        self.text_section+= 'j print_error\n'

        self.text_section+= 'error_div_by_zero:\n' #division by zero error 4
        self.text_section+= 'la $a0,zero_division\n'
        self.text_section+= 'j print_error\n'

        self.text_section+= 'error_substring:\n' #substring out of range
        self.text_section+= 'la $a0,substring_out_of_range\n'
        self.text_section+= 'j print_error\n'

        self.text_section+= 'error_heap:\n'
        self.text_section+= 'la $a0,heap_overflow\n'


        self.text_section+= 'print_error:\n'
        self.text_section+= 'li $v0, 4\n'
        self.text_section+= 'syscall\n'
        self.text_section+= 'j end\n'

    def fill_dottext_with_comparison(self):
        #Equals
        self.text_section+= '\n'
        self.text_section+= 'Equals_comparison:\n'
        self.text_section+= 'beq $t1,$t2 equalsTrue\n'
        self.text_section+= 'li $t3,0\n'
        self.text_section+= 'j end_equals_comparison\n'
        self.text_section+= 'equalsTrue: \n'
        self.text_section+= 'li $t3,1\n'
        self.text_section+= 'end_equals_comparison:\n'
        self.text_section+= 'jr $ra\n'
        self.text_section+= '\n'
        #LessEqual
        self.text_section+= '\n'
        self.text_section+= 'LessEqual_comparison:\n'
        self.text_section+= 'ble $t1,$t2 lessEqualTrue\n'
        self.text_section+= 'li $t3,0\n'
        self.text_section+= 'j end_LessEqual_comparison\n'
        self.text_section+= 'lessEqualTrue: \n'
        self.text_section+= 'li $t3,1\n'
        self.text_section+= 'end_LessEqual_comparison:\n'
        self.text_section+= 'jr $ra\n'
        self.text_section+= '\n'
        #Less
        self.text_section+= '\n'
        self.text_section+= 'Less_comparison:\n'
        self.text_section+= 'blt $t1,$t2 lessTrue\n'
        self.text_section+= 'li $t3,0\n'
        self.text_section+= 'j end_less_comparison\n'
        self.text_section+= 'lessTrue: \n'
        self.text_section+= 'li $t3,1\n'
        self.text_section+= 'end_less_comparison:\n'
        self.text_section+= 'jr $ra\n'
        self.text_section+= '\n'
        #Is_void
        self.text_section+= '\n'
        self.text_section+= 'Void_comparison:\n'
        self.text_section+= 'la $t2 void_data \n'
        self.text_section+= 'blt $t1,$t2 VoidTrue\n'
        self.text_section+= 'li $t3,0\n'
        self.text_section+= 'j end_Void_comparison\n'
        self.text_section+= 'VoidTrue: \n'
        self.text_section+= 'li $t3,1\n'
        self.text_section+= 'end_Void_comparison:\n'
        self.text_section+= 'jr $ra\n'
        self.text_section+= '\n'

    def fill_compute_type_distance(self): 
    #tipo hijo se encuentra en $t1 y tipo padre se encuentra en $t2, los resultados se dejan en $s0 para el adress del menor type_k
    #en $s1 se deja el menor count desde $t1 a $s0 (desde el expr_0.type() hasta el type_k)
        self.text_section+= '\n'
        self.text_section+= 'calculateDistance:\n'
        self.text_section+= 'li $a1, 0 #calculateDistance Funct\n' # a1 : Counter

        self.text_section+= 'loop_distance_types:\n'
        self.text_section+= 'beq $t1, $t2 end_ancestor_search\n' #Encontre al padre y por tanto comparar si mejora
        self.text_section+= 'beqz $t1 end_method_compute_distance\n' #No encontre al padre y llegue a Object
        self.text_section+= 'lw  $t1,8($t1)\n' #Cargar al padre
        self.text_section+= 'addi $a1,$a1,1\n' #Aumentar el contador de padres encontrados
        self.text_section+= 'j loop_distance_types\n' #Repetir

        #Saltar a esta seccion si encontre en $t1 al ancestro $t2
        self.text_section+= 'end_ancestor_search:\n'
        self.text_section+= 'blt $a1,$s1 new_min_label_distance\n' #Preguntar si encontre un padre menor
        self.text_section+= 'jr $ra\n'

        self.text_section+= f'new_min_label_distance:\n'
        self.text_section+= 'move $s1,$a1\n'
        self.text_section+= 'move $s0,$t2\n' #Guardo el resultado que es un adress del padre
        self.text_section+= 'end_method_compute_distance:\n'
        self.text_section+= 'jr $ra\n'

    def fill_read_string(self):

        self.text_section+='\n'
        self.text_section+= 'read_string_function: \n'
        #Calculate length to free space
        self.text_section += 'move $t1,$a0\n' #Adress del data_aux_str
        self.text_section += 'li $s1, 0\n' #contador de caracteres

        self.text_section += 'loop_function_length_read:\n' 
        self.text_section += 'li $t2,0\n'
        self.text_section += 'lb $t2, ($t1)\n' #Cargo un caracter
        self.text_section += 'beqz $t2, end_function_length_read\n' #si el caracter que cargue es 0, termino
        self.text_section += 'addi $t1, $t1, 1\n' #sumo 1 a la direccion de donde estoy buscando el string
        self.text_section += 'addi $s1, $s1, 1\n' #Sumo 1 al contador
        self.text_section += 'j loop_function_length_read\n' #Reinicio el loop
        self.text_section += 'end_function_length_read:\n' #Fin del loop



        #En $s1 deje el contador
        #En $t1 un puntero al 0 del string de data que recibi de entrada

        self.text_section += '\n'
        self.text_section += 'addi $s1,$s1,1\n'

        #Fix data entry
        self.text_section += 'string_fix:\n'
        self.text_section += 'addi $t1, $t1, -1\n' # posicion anterior al 0
        self.text_section += 'addi $s1, $s1, -1\n' #Contador decrease
        self.text_section += 'li $t0, 0\n'
        self.text_section += 'lb $t0, ($t1)\n' #Cargo el byte de esa posicion
        self.text_section += 'bne $t0, 10, end_fix_str\n' #remuevo el \n
        self.text_section += 'sb $zero, ($t1)\n' # remuevo el \n'
        self.text_section += 'addi $s1,$s1,-1 \n'
        self.text_section += 'addi $t1, $t1, -1\n' # posicion anterior a la anterior
        self.text_section += 'lb $t0, ($t1)\n'
        self.text_section += 'bne $t0, 13, end_fix_str\n' # remuevo el \r
        self.text_section += 'sb $zero, ($t1)\n' # remuevo el '\r'
        self.text_section += 'j string_fix\n'
        self.text_section += 'end_fix_str:\n'


        self.text_section += 'move $a0,$s1\n'

        #Allocate space for new instance
        self.text_section += 'addi $a0,$a0,1\n'
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n' #dir3: se mueve para ir rellenando
        self.text_section += 'move $t4,$v0\n' #fijo

        #Copy data to heap
        self.text_section += 'la $t1, aux_input_string\n'

        self.text_section += f'loop_readString:\n'
        self.text_section += f'li $a1,0\n'
        self.text_section += f'lb $a1, ($t1)\n'
        self.text_section += f'sb $a1, ($t3)\n'
        self.text_section += f'addi $t1,$t1,1\n'
        self.text_section += f'addi $t3,$t3,1\n'
        self.text_section += f'beqz $a1,end_readString\n'
        self.text_section += f'j loop_readString\n'

        self.text_section+= 'end_readString:\n' 
        self.text_section += 'jr $ra\n'

    def fill_string_comparison(self):
        self.text_section += 'String_comparison_fun:\n'
        self.text_section += 'bne $a1,$a2, false_string_comparison \n'
        self.text_section += 'beqz $a1, true_string_comparison \n'
        # self.text_section += 'li $a1,0\n'
        # self.text_section += 'li $a1,0\n'
        self.text_section += 'lb $a1,($t1)\n'
        self.text_section += 'lb $a2,($t2)\n'
        self.text_section += 'addi $t1,$t1,1\n'
        self.text_section += 'addi $t2,$t2,1\n'
        self.text_section += 'j String_comparison_fun\n'

        # False comparison
        self.text_section += 'false_string_comparison:\n'   
        self.text_section += 'li $t3,0\n'
        self.text_section += 'j end_string_comparison\n'

        # True comparison
        self.text_section += 'true_string_comparison:\n'
        self.text_section += 'li $t3,1\n'
        self.text_section += 'end_string_comparison:'     
        self.text_section += 'jr $ra\n'


class CILtoMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramCilNode)
    def visit(self,node):
    ########################################
    # self.dottypes = dottypes [TypeNodeList]
    # self.dotdata = dotdata [DataNodeList]
    # self.dotcode = dotcode [FunctionNodeList]
    ########################################
        self.dottypes = node.dottypes
        self.dotcode = node.dotcode
        self.dotdata = node.dotdata
        self.fill_dotdata_with_errors()

        self.text_section+= 'jal entry\n'

        self.text_section+=f'\n'
        self.text_section+=f'end:\n' 
        self.text_section+=f'li, $v0, 10\n'
        self.text_section+=f'syscall\n'

        self.data_section+= 'abort_label: .asciiz "Abort called from class "\n'
        self.data_section+= 'slash_n: .asciiz "\\n" \n'

        self.fill_dottext_with_errors()
        self.fill_dottext_with_comparison()
        self.fill_compute_type_distance()

        self.fill_read_string()
        self.fill_string_comparison()

        self.data_section+= '\n#TYPES\n'
        for type in self.dottypes:
            self.visit(type)
        self.data_section+= '\n#DATA_STR\n'
        self.data_section+= 'empty_str_data: .asciiz ""\n'
        self.data_section+= 'void_data: .word 0\n'
        self.data_section+= 'aux_input_string: .space 1028\n\n'
        for data in self.dotdata:
            self.visit(data)
        self.text_section+= '\n#CODE\n'
        for code in self.dotcode:
            self.visit(code)

        return self.data_section+self.text_section

    @visitor.when(TypeCilNode)
    def visit(self,node):
        parent_name = self.context.get_type(node.name).parent 
        parent_name = 0 if parent_name is None else f'{parent_name.name}_methods'

        self.data_section+= f'type_{node.name}: .asciiz "{node.name}"\n'
        self.data_section+= f'{node.name}_methods:\n'


        for i,attr in enumerate(node.attributes):
            self.attribute_offset[node.name,attr] = 4*(i+1)
        self.type_size[node.name] = len(node.attributes)

        self.data_section+=f'.word {4*(len(node.attributes)+1)}\n' #Cantidad de espacio en memoria que pide una instancia del tipo actual
        self.data_section+= f'.word type_{node.name}\n' #Type_name adress del tipo
        self.data_section+= f'.word {parent_name}\n'

        for i,method in enumerate(node.methods):
            self.data_section+= f'.word {method[1]}\n'
            self.method_offset[node.name,method[1]] = 4*(i+3)
            self.method_original[node.name,method[0]] = method[1]

        self.data_section+= '\n'
      
    @visitor.when(DataCilNode)
    def visit(self,node):
        self.data_section += f'{node.name}: .asciiz "{node.value}"\n'
            
    @visitor.when(FunctionCilNode)
    def visit(self,node):
        #############################################3
        #     node.name = fname
        #     node.params = params
        #     node.localvars = localvars
        #     node.instructions = instructions
        #############################################3
        self.current_function = node
        for i,var in enumerate(node.localvars+node.params):
            self.var_offset[self.current_function.name,var.name] = 4*(i+1)

        self.text_section += '\n'
        self.text_section += f'{node.name}:\n'
        self.text_section += f'addi, $sp, $sp, {-4*(len(node.localvars)+1)}\n'#get space for vars and return adress
        self.text_section += 'sw $ra, ($sp)\n'

        for inst in node.instructions:
            self.visit(inst)

        self.text_section+= 'lw $ra, ($sp)\n'
        self.text_section+= f'addi $sp, $sp,{4*(len(node.localvars)+1)}\n'
        self.text_section+= 'jr $ra\n'


    # #7.2 Identifiers, not necesary cil Node

    @visitor.when(AssignCilNode)   # 7.3 Assignment
    def visit(self,node): 
        #########################################################################
        # node.dest = dest
        # node.source = source
        #########################################################################
        offset_dest =  self.var_offset[self.current_function.name,node.dest]
        offset_source = self.var_offset[self.current_function.name,node.source]
        self.text_section+= f'lw $t1, {offset_source}($sp)\n'
        self.text_section+= f'sw $t1, {offset_dest}($sp)\n'

        


    @visitor.when(StaticCallCilNode) #7.4 Distaptch Static
    def visit(self,node): 
        #########################################################################
        #node.dynamic = dynamic
        # node.type = type
        # node.method_name = method_name
        # node.args = args
        # node.result = result
        ########################################################################
        arg_amount = (len(node.args))*4

        
        self_dir = self.var_offset[self.current_function.name,node.args[0]]
        self.text_section+= f'lw $s4,{self_dir}($sp)\n'



        self.text_section+= f'move $t0, $sp #call to function {node.method_name}\n'
        self.text_section+= f'addi, $sp, $sp, -{arg_amount}\n'
    
        for i,arg in enumerate(node.args):
            arg_offset = self.var_offset[self.current_function.name,arg]
            self.text_section+= f'lw, $s0, {arg_offset}($t0) #loading param_{arg}\n'
            self.text_section+= f'sw, $s0 {(i)*4}($sp) #setting param for function call\n'

        if node.method_name[:5] == 'INIT_':
            self.text_section+= f'jal {node.method_name}\n'
        else:
            function_original_name = self.method_original[node.type,node.method_name]
            function_offset = self.method_offset[node.type,function_original_name]
            self.text_section+= 'lw $a1, ($s4)\n'
            self.text_section+= f'lw $a2, {function_offset} ($a1)\n'
            self.text_section+= f'jalr $a2\n'

        self.text_section+= f'addi, $sp, $sp, {arg_amount}\n'
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section += f'sw $s0, {result_offset}($sp) #Saving result on {node.result}\n'

       


    @visitor.when(DynamicCallCilNode) #7.4 Dispatch Dynamic
    def visit(self,node):
        #########################################################################
        # node.expresion_instance = expresion_instance
        # node.static_type = static_type
        # node.method_name = method_name
        # node.args = args
        # node.result = result
        ########################################################################
        arg_amount = (len(node.args))*4
        original_fun = self.method_original[node.static_type,node.method_name]

        self.text_section+= f'move $t0, $sp #Dynamic Call\n'
        self.text_section+= f'addi, $sp, $sp, -{arg_amount}\n'

        for i,arg in enumerate(node.args):
            arg_offset = self.var_offset[self.current_function.name,arg]
            self.text_section+= f'lw, $s0, {arg_offset}($t0)\n'
            self.text_section+= f'sw, $s0 {(i)*4}($sp)\n'


        expresion_offset = self.var_offset[self.current_function.name,node.expresion_instance]  
        self.text_section += f'lw $a0, {expresion_offset}($t0)\n' #Carga el data
        #El tipo dinamico se consigue a partir de expresion offset
        self.text_section += 'la $t1, void_data\n'
        self.text_section += 'beq $a0, $t1, error_call_void\n'
        

        #Selecting Function
        self.text_section += f'lw $a1, ($a0) #Loading_Adress\n'  #Cargar el adress
        self.text_section += f'lw $a2, {self.method_offset[node.static_type,original_fun]}($a1)#Function {node.method_name}:{original_fun}\n' #Carga la funcion
        self.text_section += 'jalr $a2\n'


        #Restoring SP and returning
        self.text_section+= f'addi, $sp, $sp, {arg_amount}\n'
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section += f'sw $s0, {result_offset}($sp)\n'


    @visitor.when(DynamicParentCallCilNode) #7.4 Dispatch Dynamic
    def visit(self,node):
        #########################################################################
        # node.expresion_instance = expresion_instance
        # node.static_type = static_type
        # node.method_name = method_name
        # node.args = args
        # node.result = result
        ########################################################################
        arg_amount = (len(node.args))*4
        self.text_section+= f'move $t0, $sp #Dynamic_Parent_Call\n'
        self.text_section+= f'addi, $sp, $sp, -{arg_amount}\n'

        original_fun = self.method_original[node.static_type,node.method_name]

        for i,arg in enumerate(node.args):
            arg_offset = self.var_offset[self.current_function.name,arg]
            self.text_section+= f'lw, $s0, {arg_offset}($t0)\n'
            self.text_section+= f'sw, $s0 {(i)*4}($sp)\n'

        #Conseguir el tipo estatico a partir de node.static_type aue es lo que existe en el @type
        self.text_section += 'la $t1, void_data\n'
        self.text_section += 'beq $v0, $t1, error_call_void\n'
        
        self.text_section += f'la $a1, {node.static_type}_methods\n'
        self.text_section += f'lw $a2, {self.method_offset[node.static_type,original_fun]}($a1) #FunctionToCall {original_fun}\n'
        self.text_section += 'jalr $a2\n'


        self.text_section+= f'addi, $sp, $sp, {arg_amount}\n'
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section += f'sw $s0, {result_offset}($sp)\n'


    @visitor.when(CaseCilNode)
    def visit(self,node):
        offset_expr_0 = self.var_offset[self.current_function.name,node.main_expr]  
        self.text_section+= '\n'
        self.text_section+= f'lw $t1,{offset_expr_0}($sp) \n'
        #comparar con void y dar error
        self.text_section += 'la $t3, void_data\n'
        self.text_section += 'beq $t1, $t3, error_expr_void\n'

        self.text_section+= f'lw $v1, ($t1) #Adress Method\n' #$t1 : adress del expr_0.type()
        self.text_section+= f'li $s0,0\n' #s0: adress del menor type_P tal que P>=C (0 si no se encuentra ninguno)
        self.text_section+= f'li $s1, 2147483647\n' #s1: distancia desde expr_0 hasta menor type_k actual(empieza en int.max)

    @visitor.when(BranchCilNode) #7.9 Case
    def visit(self,node):
        ##############################
        # node.type_k = type_k
        ##############################
        self.text_section+= 'move $t1,$v1\n'
        self.text_section+= f'la $t2,{node.type_k}\n'
        self.text_section+= 'jal calculateDistance\n' #tipo hijo(C) tiene que estar en $t1 y tipo ancestro(P) tiene que estar en $t2 

    @visitor.when(CaseEndCilNode)
    def visit(self,node):
        ##############################
        # node.result
        ##############################
        result_offset = self.var_offset[self.current_function.name,node.result] 
        self.text_section+='\n'
        self.text_section+= 'beqz $s0, error_branch\n'
        self.text_section+=f'sw $s0, {result_offset}($sp)\n'




    #Binary Aritmetic Operations
    @visitor.when(PlusCilNode)
    def visit(self, node):   
        ######################################
        # node.dest = dest
        # node.left = left
        # node.right = right
        ######################################
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load sum value\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3) #Load sum value\n'
        self.text_section+= f'add $t3,$t1,$t2\n' #resultado de la suma
        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'
        
        
    @visitor.when(MinusCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load minus value\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3) #Load minus value\n'
        self.text_section+= f'sub $t3,$t2,$t1\n' #resultado de la resta
        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(StarCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Star value\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3) #Load Star value\n'
        self.text_section+= f'mul $t3,$t1,$t2\n' #Operacion mul
        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(DivCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Div value\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3) #Load Div value\n'

        self.text_section+= f'beqz $t1 error_div_by_zero\n'

        self.text_section+= f'div $t3,$t2,$t1\n' #Operacion div
        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(EqualCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Equal Node\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3)\n'

        self.text_section+= f'jal Equals_comparison\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(EqualRefCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t1, {offset_right}($sp) #Load EqualRefNode\n'
        self.text_section+= f'lw, $t2, {offset_left}($sp)\n'

        self.text_section+= f'jal Equals_comparison\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(CompareStringCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load String Adress Node\n'
        self.text_section+= f'lw $a1,8($t3)\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3)\n'
        self.text_section+= f'lw $a2,8($t3)\n'


        self.text_section+= f'jal String_comparison_fun\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(LessEqualCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Less Equal\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3)\n'

        self.text_section+= f'jal LessEqual_comparison\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(LessCilNode)
    ######################################
    # node.dest = dest
    # node.left = left
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_left = self.var_offset[self.current_function.name,node.left]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_left}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Less \n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t2,4($t3)\n'

        self.text_section+= f'jal Less_comparison\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'



    @visitor.when(IsVoidCilNode)
    ######################################
    # node.dest = dest
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'move,$t1,$t3\n'

        self.text_section+= f'jal Void_comparison\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(NotCilNode)
    ######################################
    # node.dest = dest
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Not Node\n'

        self.text_section+= f'xor $t3,$t1,1\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'

    @visitor.when(NegateCilNode)
    ######################################
    # node.dest = dest
    # node.right = right
    ######################################
    def visit(self, node):
        offset_right = self.var_offset[self.current_function.name,node.right]
        offset_dest = self.var_offset[self.current_function.name,node.dest]
        self.text_section += '\n'
        self.text_section+= f'lw, $t3, {offset_right}($sp)\n'
        self.text_section+=f'lw,$t1,4($t3) #Load Negate\n'

        self.text_section+= f'neg $t3,$t1\n'

        self.text_section+=f'sw, $t3, {offset_dest}($sp)\n'



    @visitor.when(GetAttribCilNode)
    def visit(self,node):
        #######################################
            # node.instance = instance
            # node.type = type
            # node.attribute = attribute
            # node.result = result
        #######################################
        result_offset = self.var_offset[self.current_function.name,node.result]
        instance_offset = self.var_offset[self.current_function.name,node.instance]
        self.text_section+= f'lw $t3, {instance_offset}($sp) #getting instance {node.instance} \n' #Buscar la local que tiene la direccion del heap

        if node.attribute == 'self':
            self.text_section+= f'sw $t3, {result_offset}($sp)\n'
        else:
            attr_offset = self.attribute_offset[node.type,node.attribute]

            # (instance_offset+attr_offset)
            self.text_section += '\n'
            self.text_section+= f'lw, $t3, {instance_offset}($sp) #getting instance {node.instance} \n' #Buscar la local que tiene la direccion del heap
            self.text_section+= f'lw, $t1, {attr_offset}($t3)  #getting offset {node.attribute} \n' #Cargar en un registro el valor del atributo
            self.text_section+= f'sw, $t1, {result_offset}($sp)   \n' #Guardo el valor 

    @visitor.when(SetAttribCilNode)
    def visit(self,node):
    # class SetAttribCilNode(InstructionCilNode):
    #######################################
        # node.instance = instance
        # node.type = type
        # node.attribute = attribute
        # node.value = value
    #######################################
        attr_offset = self.attribute_offset[node.type,node.attribute]
        instance_offset = self.var_offset[self.current_function.name,node.instance]
        value_offset = self.var_offset[self.current_function.name,node.value]
        self.text_section += '\n'
        self.text_section+= f'lw, $t1, {value_offset}($sp)   \n' #Guardo el valor 
        self.text_section+= f'lw, $t3, {instance_offset}($sp)  \n' #Buscar la local que tiene la direccion del heap
        self.text_section+= f'sw, $t1, {attr_offset}($t3)   \n' #Cargar en un registro el valor del atributo(ojo puede q no haya q restar)


    @visitor.when(AllocateCilNode)
    def visit(self, node):
        #######################################
        #node.type = type
        #node.result = result
        #######################################
        result_offset = self.var_offset[self.current_function.name,node.result]
        type_size = (self.type_size[node.type] + 1) * 4 #mas 1 para guardar el addr del tipo
        self.text_section += '\n'
        
        self.text_section += f'addi $a0, $zero, {type_size}\n' #ojo pudiera faltar un +4
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n'

        self.text_section += f'la $t1,{node.type}_methods\n'#recupero el addr del tipo
        self.text_section += 'sw $t1, ($t3)\n' #guardo en el primer espacio de memoria de la nueva instancia el addr del tipo
        self.text_section += f'sw, $t3, {result_offset}($sp)\n'

    @visitor.when(AllocateDynamicCilNode)   
    def visit(self,node):
        #######################################
        # node.address_in_local = address_in_local
        # node.result = result
        #######################################
        address_in_local_offset = self.var_offset[self.current_function.name,node.address_in_local_offset]
        result_offset = self.var_offset[self.current_function.name,node.result]

        self.text_section += '\n'
        self.text_section+= f'lw $t1,{address_in_local_offset}$(sp)\n'   
        self.text_section+= f'lw $a0,($t1)\n'     
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n'

        self.text_section += 'sw $t1, ($t3)\n' #guardo en el primer espacio de memoria de la nueva instancia el addr del tipo
        self.text_section += f'sw, $t3, {result_offset}($sp)\n'


    @visitor.when(GetDataCilNode)
    def visit(self,node):
        #######################################
        # node.name = name
        # node.result = result
        #######################################
        self.text_section += f'\n'
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section += f'la $t1, {node.name}\n'
        self.text_section += f'sw $t1, {result_offset}($sp)\n'



    @visitor.when(ReturnCilNode)
    def visit(self,node):
        ###########################################
        #node.value = value
        ###########################################
        self.text_section += '\n'
        if node.value:
            offset_value = self.var_offset[self.current_function.name,node.value]
            self.text_section += f'lw $s0, {offset_value}($sp)\n'
        else:
            self.text_section += f'move $s0, $zero\n'

#Function Mips Implementattion
    @visitor.when(PrintStringCilNode)
    def visit(self, node):
        ###########################################
        # node.self_param = self_param
        # node.to_print = to_print
        ###########################################
        str_offset = self.var_offset[self.current_function.name,node.to_print]

        self.text_section += '\n'
        self.text_section+= f'li, $v0, 4\n'
        self.text_section+= f'lw, $a0, {str_offset}($sp)\n'
        self.text_section+= f'syscall\n'

    @visitor.when (PrintIntCilNode)
    def visit(self, node):
        ###########################################
        # node.to_print = to_print 
        ###########################################
        str_offset = self.var_offset[self.current_function.name,node.to_print]
        self.text_section += '\n'
        self.text_section+= f'li, $v0, 1\n'
        self.text_section+= f'lw, $a0, {str_offset}($sp)\n'
        self.text_section+= f'syscall\n'


    @visitor.when (LabelCilNode)
    def visit(self, node):
        ###########################################
        # self.label = label
        ###########################################
        self.text_section += f'{node.label}:\n'
        

    @visitor.when (GotoCilNode)
    def visit(self, node):
        # self.label = label
        self.text_section += f'j {node.label}\n'

    @visitor.when (GotoIfCilNode)
    def visit(self, node):
        ###########################################
        #node.val_dir = val_dir
        #node.label = label
        ###########################################
        offset_val_dir = self.var_offset[self.current_function.name,node.val_dir]
        self.text_section += f'lw $t0, {offset_val_dir}($sp) #Goto If Label\n' #Carga el bool
        self.text_section += f'lw $t0, 4($t0) #Load Bool Value\n' #Carga el valor del bool
        self.text_section += f'beq $t0, 1, {node.label}\n'

    @visitor.when (GotoBoolIfCilNode)
    def visit(self, node):
        ###########################################
        #node.val_dir = val_dir
        #node.label = label
        ###########################################
        offset_val_dir = self.var_offset[self.current_function.name,node.val_dir]
        self.text_section += f'lw $t0, {offset_val_dir}($sp) #Goto If Label\n' #Carga el bool
        self.text_section += f'beq $t0, 1, {node.label}\n'

    @visitor.when (NotGotoIfCilNode)
    def visit(self, node):
        ###########################################
        #node.val_dir = val_dir
        #node.label = label
        ###########################################
        offset_val_dir = self.var_offset[self.current_function.name,node.val_dir]
        self.text_section += f'lw $t0, {offset_val_dir}($sp) #If Label\n' #Carga el bool
        self.text_section += f'lw $t0, 4($t0)\n' #Carga el valor del bool
        self.text_section += f'beqz $t0 {node.label}\n'

    #TypesCilNodes falta bool ojo
    @visitor.when(IntCilNode)
    def visit(self, node):   
        #     node.value = value
        #     node.result = result
        offset_value = self.var_offset[self.current_function.name,node.result]
        self.text_section += '\n'
        self.text_section += f'addi, $t1, $zero, {node.value}\n'
        self.text_section += f'sw, $t1, {offset_value}($sp)\n'


    @visitor.when(StringCilNode)
    def visit(self, node):   
        ###############################
        #     node.dir1 = dir1
        #     node.dir2 = dir2
        ###############################
        dir1_offset = self.var_offset[self.current_function.name,node.dir1]
        dir2_offset = self.var_offset[self.current_function.name,node.dir2]
        self.text_section += '\n'
        self.text_section += f'lw, $t1, {dir1_offset}($sp)\n' #Cargo en t1 la direccion del string en data
        self.text_section += f'lw, $t2, {dir2_offset}($sp)\n' #Cargo en t2 la direccion donde guardare el string en el heap

        # self.text_section += 

    @visitor.when(LengthCilNode)
    def visit(self, node):
        #####################################  
        # node.self_dir = self_dir
        # node.length = length
        #####################################  

        offset_self = self.var_offset[self.current_function.name,node.self_dir]
        offset_length = self.var_offset[self.current_function.name,node.length]
        self.text_section += f'lw $t1, {offset_self}($sp)\n'

        self.text_section += 'li $s1, 0\n' #contador de caracteres (el ultimo es 0 y no se cuenta)
        self.text_section += 'loop_function_length:\n' 
        self.text_section += 'lb $t2, ($t1)\n' #Cargo un caracter
        self.text_section += 'beqz $t2, end_function_length\n' #si el caracter que cargue es 0, termino
        self.text_section += 'addi $t1, $t1, 1\n' #sumo 1 a la direccion de donde estoy buscando el string
        self.text_section += 'addi $s1, $s1, 1\n' #Sumo 1 al contador
        self.text_section += 'j loop_function_length\n' #Reinicio el loop
        self.text_section += 'end_function_length:\n' #Fin del loop

        self.text_section += f'sw $s1, {offset_length}($sp)\n'  #


    # #Function CilNodes 


    @visitor.when(AbortCilNode)
    def visit(self, node):
        #####################################  
        # node.self_from_call
        #####################################  
        self_offset = self.var_offset[self.current_function.name,node.self_from_call]
        self.text_section+= 'la $a0 abort_label\n'
        self.text_section+= 'li $v0,4\n'
        self.text_section+= 'syscall\n'
        self.text_section+= f'lw $a0 {self_offset}($sp)\n'
        self.text_section+= 'lw $a0 ($a0)\n'
        self.text_section+= 'lw $a0 4($a0)\n'
        self.text_section += 'syscall\n'
        self.text_section+='la $a0, slash_n\n'
        self.text_section+='syscall\n'
        self.text_section+= 'j end\n'


    @visitor.when(TypeNameCilNode)
    def visit(self, node):
        #####################################  
        # node.self_param = self_param
        # node.result = result
        #####################################  

        self_param_offset = self.var_offset[self.current_function.name,node.self_param]
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section+= '\n'
        self.text_section += f'lw $a0, {self_param_offset}($sp)\n' #Carga direccion del data
        #El tipo dinamico se consigue a partir de expresion offset
        #Selecting Function
        self.text_section += f'lw $a1, ($a0)\n'  #Cargar el adress
        self.text_section += f'lw $a2, 4($a1)\n' #Carga el adress del string
        self.text_section += f'sw $a2, {result_offset}($sp)' #Guardo el adress del string


    @visitor.when(CopyCilNode)
    def visit(self, node):
        #####################################  
        # node.self_param = self_param
        # node.result = result
        #####################################  
        self_param_offset = self.var_offset[self.current_function.name,node.self_param]
        result_offset = self.var_offset[self.current_function.name,node.result]
        self.text_section+= '\n'
        self.text_section += f'lw $t1, {self_param_offset}($sp)\n' #Carga direccion del data
        self.text_section += f'lw $t2, ($t1)\n'  #Cargar el adress
        self.text_section += f'lw $a0, ($t2)\n' #Carga el adress del string $a2 = Amount_attr

        #Allocate space for new instance
        self.text_section += '\n'
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n'
        self.text_section += 'move $t4,$v0\n'

        #t1 = old instance
        #t3 = new instance
        #t2 = aux
        #loop to copy t1 to t3
        self.text_section += f'loop_copyNode:\n'
        self.text_section += f'lw $t2, ($t1)\n'
        self.text_section += f'sw $t2, ($t3)\n'
        self.text_section += f'addi $t1,$t1,4\n'
        self.text_section += f'addi $t3,$t3,4\n'
        self.text_section += f'subu $a0,$a0,4\n'
        self.text_section += f'beqz $a0,end_loop_copy\n'
        self.text_section += f'j loop_copyNode\n'


        self.text_section += f'end_loop_copy:\n'
        self.text_section += f'sw $t4, {result_offset}($sp)\n'
    
    @visitor.when(InternalCopyCilNode)
    def visit(self, node):
        #####################################  
        # node.dir_child = dir_child
        # node.dir_ancestor = dir_ancestor
        #####################################  
        child_offset = self.var_offset[self.current_function.name,node.dir_child]
        ancestor_offset = self.var_offset[self.current_function.name,node.dir_ancestor]

        self.text_section+= '\n'
        self.text_section += f'lw $t1, {child_offset}($sp)\n' #Carga direccion del data_child
        self.text_section += f'lw $t2, {ancestor_offset}($sp)\n' #Carga direccion del data_ancestor

        self.text_section += f'lw $a2, ($t2)\n'  #Cargar el adress
        self.text_section += f'lw $a2, ($a2)\n'  #Catga el numero

        self.text_section+=f'addi $a2,$a2,-4\n'#cantidad de atributos a copiar
        self.text_section+=f'addi $t1,$t1,4\n'
        self.text_section+=f'addi $t2,$t2,4\n'


        self.text_section+= f'jal function_internalcopy\n'

        self.text_section += '\n'


    @visitor.when(ReadIntCilNode)
    def visit(self, node):
        #####################################  
        # node.dest = dest
        ##################################### 
        dest_offset = self.var_offset[self.current_function.name,node.dest]
        self.text_section+='\n'
        self.text_section+= 'li $v0,5 # Read_Int_Section\n'
        self.text_section+= 'syscall\n'
        self.text_section+= f'sw $v0,{dest_offset}($sp)\n'

    @visitor.when(ReadStringCilNode)
    def visit(self, node):
        #####################################  
        # node.dest = dest
        ##################################### 
        dest_offset = self.var_offset[self.current_function.name,node.dest]
        #Save input string on aux data
        self.text_section+='\n'
        self.text_section+= 'li $v0,8 # Read_string_Section\n'
        self.text_section+= 'la $a0,aux_input_string \n'
        self.text_section+= 'li $a1,1024\n'
        self.text_section+= 'syscall \n'

        self.text_section+= 'jal read_string_function\n'


        self.text_section+= f'sw $t4,{dest_offset}($sp)\n'

        #



    @visitor.when(ReadStrEndCilNode)
    def visit(self, node):
        #####################################  
        # node.dest = result
        # node.length = length
        ##################################### 
        result_offset = self.var_offset[self.current_function.name,node.result]
        length_offset = self.var_offset[self.current_function.name,node.length]

        self.text_section += '\n'
        self.text_section+= f'lw $a0,{length_offset}($sp)\n #END part of read'
        #Allocate space for new instance
        self.text_section += 'addi $a0,$a0,1\n'
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n' #dir3: se mueve para ir rellenando
        self.text_section += 'move $t4,$v0\n' #fijo
        #Copy data to heap
        self.text_section += 'la $t1, aux_input_string\n'

        self.text_section += f'loop_readString:\n'
        self.text_section += f'beqz $a0,end_readString\n'
        self.text_section += f'lb $a1, ($t1)\n'
        self.text_section += f'sb $a1, ($t3)\n'
        self.text_section += f'addi $a0,$a0,-1\n'
        self.text_section += f'addi $t1,$t1,1\n'
        self.text_section += f'addi $t3,$t3,1\n'
        self.text_section += f'j loop_readString\n'

        self.text_section+= 'end_readString:\n' 
        self.text_section += 'sb,$zero,($t3)\n'
        self.text_section+= f'sw $t4,{result_offset}($sp)\n'
    

    @visitor.when(ConcatCilNode)
    def visit(self, node):
        #####################################  
        # node.self_param = self_param
        # node.param_1 = param_1
        # node.result_addr = result_addr
        #####################################  
        self_param_offset = self.var_offset[self.current_function.name,node.self_param]
        param1_offset = self.var_offset[self.current_function.name,node.param_1]
        result_offset = self.var_offset[self.current_function.name,node.result_addr]
        self.text_section+= '\n'
        self.text_section += f'lw $t1, {self_param_offset}($sp)\n' #Carga direccion del data
        self.text_section += f'lw $t2, {param1_offset}($sp)\n'

        #Capturo los len de las instancias
        self.text_section += f'lw $a1, 8($t1)\n'  #Cargar el len de t1
        self.text_section += f'lw $a2, 8($t2)\n' #Carga el len de t2
        self.text_section += f'add $a0, $a1, $a2\n' #a0 = a1 + a2

        #Capturo los adress de los str
        self.text_section += f'lw $t1, 4($t1)\n'  #Cargar el addr de t1
        self.text_section += f'lw $t2, 4($t2)\n' #Carga el addr de t2

        #Allocate space for new instance
        self.text_section += '\n'
        self.text_section += 'addi $a0,$a0, 1\n' #OJO: Test generated space if correct or not
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n' #dir3: se mueve para ir rellenando
        self.text_section += 'move $t4,$v0\n' #fijo

        #Loop to fill
        self.text_section += f'loop_concat_dirSelf:\n'
        self.text_section += f'lb $a1, ($t1)\n'
        self.text_section += f'beqz $a1,loop_concat_dirParam\n'
        self.text_section += f'sb $a1, ($t3)\n'
        self.text_section += f'addi $t1,$t1,1\n'
        self.text_section += f'addi $t3,$t3,1\n'
        self.text_section += f'j loop_concat_dirSelf\n'

        self.text_section += f'loop_concat_dirParam:\n'
        self.text_section += f'lb $a1, ($t2)\n'
        self.text_section += f'sb $a1, ($t3)\n'
        self.text_section += f'addi $t2,$t2,1\n'
        self.text_section += f'addi $t3,$t3,1\n'
        self.text_section += f'beqz $a1,end_loop_concat\n'
        self.text_section += f'j loop_concat_dirParam\n'

        #End
        self.text_section += f'end_loop_concat:\n'
        self.text_section += f'sw $t4, {result_offset}($sp)\n'


    @visitor.when(SubstringCilNode)
    def visit(self, node):
        ###################################################
        # node.self_param = self_param
        # node.value1 = value1
        # node.value2 = value2
        # node.result = result
        ###################################################
        self_param_offset = self.var_offset[self.current_function.name,node.self_param]
        value1_offset = self.var_offset[self.current_function.name,node.value1]
        value2_offset = self.var_offset[self.current_function.name,node.value2]
        result_offset = self.var_offset[self.current_function.name,node.result]

        self.text_section+= '\n'
        self.text_section += f'lw $t0, {self_param_offset}($sp)\n' #Carga direccion de la instancia
        self.text_section += f'lw $t1, {value1_offset}($sp)\n'  #Carga direccion de Int i
        self.text_section += f'lw $t2, {value2_offset}($sp)\n' #Carga direccion de Int l

        self.text_section += f'lw $a2, 8($t0)\n' #len del string
        self.text_section += f'lw $a1, 4($t1)\n' #valor de i
        self.text_section += f'lw $a0, 4($t2)\n' #valor de l

        self.text_section += f'add $a3,$a1,$a0\n' # a3 = i + l
        self.text_section += f'bgt $a3,$a2, substring_out_of_range\n' #if (i+l)> len-> Erorr

        #Allocate space for isntance
        self.text_section += '\n'
        self.text_section += 'addi $a0,$a0,1\n' #OJO: Test generated space if correct or not
        self.text_section += 'li, $v0, 9\n'
        self.text_section += 'syscall\n'
        self.text_section += 'blt, $sp, $v0,error_heap\n'
        self.text_section += 'move, $t3, $v0\n' #dir3: se mueve para ir rellenando
        self.text_section += 'move $t4,$v0\n' #fijo

        self.text_section += f'lw $a2, 4($t0)\n' #adress del string
        self.text_section += f'add $a2,$a2,$a1\n' #empezar a partir de string[i]
        #Loop to fill

        self.text_section += f'lw $a0, 4($t2)\n' #valor de l

        self.text_section += f'loop_substring_dirSelf:\n'
        self.text_section += f'beqz $a0,end_loop_substr\n'
        self.text_section += f'lb $a1, ($a2)\n'
        self.text_section += f'sb $a1, ($t3)\n'
        self.text_section += f'addi $a2,$a2,1\n'
        self.text_section += f'addi $t3,$t3,1\n'
        self.text_section += f'addi $a0,$a0,-1\n'
        self.text_section += f'j loop_substring_dirSelf\n'

        #End
        self.text_section += f'end_loop_substr:\n'
        self.text_section += f'sb $zero, ($t3)\n'
        self.text_section += f'sw $t4, {result_offset}($sp)\n'
