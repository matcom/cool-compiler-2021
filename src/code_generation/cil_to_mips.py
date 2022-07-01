from semantic.visitor import visitor
from nodes import cil_ast_nodes as CilAST
from nodes import cil_expr_nodes as CilExpr

class CilToMipsVisitor:
    def __init__(self):
        self.text = ''
        self.data = ''
        self.mips_op = {
            '+' : 'add',
            '-' : 'sub',
            '*' : 'mul',
            '/' : 'div',
            '<' : 'slt',
            '<=': 'sle',
            '=' : 'seq'
        }
        self.types = None
        self.current_function = None
        #Dictionaries for easy handlling of offset
        self.attributes_offset = {}
        self.methods_offset = {}
        self.variables_offset = {}

    #This method adds a line of code to the section of .data
    def add_data_code_line(self, line):
        self.data += f'{line}\n'

    #This method adds a line of code to the section of .text
    def add_text_code_line(self,line):
        self.text += f'{line}\n'

    #----------------------------------------Visitor--------------------------------------------#
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CilAST.ProgramNode)
    def visit(self, node):
        self.types = node.types

        #Generate and register runtime error
        runtime_errors = {
            'div_zero' : 'Runtime Error: Division by zero',
            'dispatch_void' : 'Runtime Error: A dispatch with void',
            'case_void' : 'Runtime Error: A case with void',
            'case_no_match' : 'Runtime Error: Execution of a case statement without a matching branch', 
            'heap' : 'Runtime Error: Heap overflow',     
            'substr' : 'Runtime Error: Index for substring out of range',           
        }
        for error in runtime_errors:
            #Save error message string in data
            self.add_data_code_line(f'{error}: .asciiz "{runtime_errors[error]}"')
            #Label for error
            self.add_text_code_line(f'{error}_error:')
            #Print error and stop execution
            self.add_text_code_line(f'la $a0, {error}')
            self.add_text_code_line('li $v0, 4')
            self.add_text_code_line('syscall')
            self.add_text_code_line('li $v0, 10')
            self.add_text_code_line('syscall')

        #Allocate space for a auxiliar variable to receive the input string
        self.add_data_code_line('input_str: .space 2048')
        #Store void
        self.add_data_code_line('void: .word 0')

        #Visiting all types
        for node_type in node.types.values():
            self.visit(node_type)
        #Adding all data
        for node_data in node.data.keys():
            self.add_data_code_line(f'{node_data}: .asciiz "{node.data[node_data]}"')
        #Visiting all functions
        for node_code in node.code:
            self.visit(node_code)

        #Code mips = .data + .text
        mips_code = '.data\n' + self.data + '.text\n' + self.text
        return mips_code.strip()

    @visitor.when(CilAST.TypeNode)
    def visit(self, node):
        #Adding Type name and methods to data
        self.add_data_code_line(f'{node.name}_name: .asciiz "{node.name}"')
        self.add_data_code_line(f'{node.name}_methods:')
        for method in node.methods.values():
            self.add_data_code_line(f'.word {method}')
        
        #Storing attributes offset for later use
        id = 0
        self.attributes_offset.__setitem__(node.name, {})
        for attribute in node.attributes:
            self.attributes_offset[node.name][attribute] = 4*id + 16
            id = id + 1

        #Storing methods offset for later use
        id = 0
        self.methods_offset.__setitem__(node.name, {})
        for method in node.methods:
            self.methods_offset[node.name][method] = 4*id
            id = id + 1

    @visitor.when(CilAST.FunctionNode)
    def visit(self, node):
        self.current_function = node

        #Saving function variables offset
        self.variables_offset.__setitem__(self.current_function.name, {})
        for id, variable in enumerate(self.current_function.local_vars + self.current_function.params):
            self.variables_offset[self.current_function.name][variable.name] = (id + 1) * 4
        
        self.add_text_code_line(f'{node.name}:')
        #Saving space in the stack for local variables
        self.add_text_code_line(f'addi $sp, $sp, {-4 * len(node.local_vars)}')
        #Saving return address
        self.add_text_code_line('addi $sp, $sp, -4')
        self.add_text_code_line('sw $ra, 0($sp)')

        #Visiting all instructions of current function
        for instruction in node.instructions:
            self.visit(instruction)
        
        #Recovering return address
        self.add_text_code_line('lw $ra, 0($sp)')
        #Pop local variables, parameters and return address from the stack
        total = 4 * len(node.local_vars) + 4 * len(node.params) + 4
        self.add_text_code_line(f'addi $sp, $sp, {total}')
        self.add_text_code_line('jr $ra')

    @visitor.when(CilExpr.ParamDeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(CilExpr.LocalVariableDeclarationNode)
    def visit(self, node):
        pass

    @visitor.when(CilExpr.AssignNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#AssignNode {node.dest} = {node.expression}')

        #Get offset of the destination variable
        offset = self.variables_offset[self.current_function.name][node.dest]
        if node.expression:
            if isinstance(node.expression,int):
                self.add_text_code_line(f'li $t1, {node.expression}')
            else:
                #Get offset of expression
                expr_offset = self.variables_offset[self.current_function.name][node.expression]
                self.add_text_code_line(f'lw $t1, {expr_offset}($sp)')
        else:
            self.add_text_code_line('la $t1, void')
        
        self.add_text_code_line(f'sw $t1, {offset}($sp)')

    @visitor.when(CilExpr.UnaryOperatorNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#UnaryOperator {node.op} {node.expr_value}')

        #Get offset of expression value
        expr_value_offset = self.variables_offset[self.current_function.name][node.expr_value]\

        self.add_text_code_line(f'lw $t1, {expr_value_offset}($sp)')
        if node.op == '~':
            self.add_text_code_line('neg $a0, $t1')
        else:
            self.add_text_code_line('xor $a0, $t1, 1')

        #Get offset of destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')
        
    @visitor.when(CilExpr.BinaryOperatorNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#BinaryOperator {node.left} {node.op} {node.right}')

        #Get equivalent instruction in mips for operator in Cil
        mips_op = self.mips_op[node.op]
        #Get offset of left and right locals variable
        left_offset = self.variables_offset[self.current_function.name][node.left]
        right_offset = self.variables_offset[self.current_function.name][node.right]

        self.add_text_code_line(f'lw $a0, {left_offset}($sp)')
        self.add_text_code_line(f'lw $t1, {right_offset}($sp)')
        if node.op == "/":
            #Adding jump to error if a div by zero error happens
            self.add_text_code_line('beq $t1, 0, div_zero_error')
        self.add_text_code_line(f'{mips_op} $a0, $a0, $t1')
        #Get offset of destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')

    @visitor.when(CilExpr.GetAttrNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#GetAttr {node.variable} = {node.type}.{node.attr}')
        #Getting self address
        self_offset = self.variables_offset[self.current_function.name][node.instance]
        self.add_text_code_line(f'lw $t0, {self_offset}($sp)')
        #Getting attribute
        attribute_offset = self.attributes_offset[node.type][node.attr]
        self.add_text_code_line(f'lw $t1, {attribute_offset}($t0)')
        #Storing attribute in local variable
        offset = self.variables_offset[self.current_function.name][node.variable]
        self.add_text_code_line(f'sw $t1, {offset}($sp)')

    @visitor.when(CilExpr.SetAttrNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#SetAttr {node.type}{node.attr} = {node.value if node.value else "void"}')
        #Getting self address
        self_offset = self.variables_offset[self.current_function.name][node.instance]
        self.add_text_code_line(f'lw $t0, {self_offset}($sp)')

        if node.value:
            value_offset = self.variables_offset[self.current_function.name][node.value]
            self.add_text_code_line(f'lw $t1, {value_offset}($sp)')
        else:
            # attribute not initialized
            self.add_text_code_line('la $t1, void')

        #Set attribute in instance
        offset = self.attributes_offset[node.type][node.attr]
        self.add_text_code_line(f'sw $t1, {offset}($t0)')
    
    @visitor.when(CilExpr.AllocateNode)
    def visit(self, node):
        total = len(self.types[node.type].attributes) + 4
        #Comment
        self.add_text_code_line(f'#Allocate {node.tag}:tag {node.type}:Class_name {total}:Class_size')

        #Allocate space for Object
        self.add_text_code_line(f'li $a0, {total * 4}')
        self.add_text_code_line('li $v0, 9')
        self.add_text_code_line('syscall')
        #If heap error jump to error
        self.add_text_code_line('bge $v0, $sp, heap_error')
        self.add_text_code_line('move $t0, $v0')

        #Initializing Object layout
        #Class tag
        self.add_text_code_line(f'li $t1, {node.tag}')
        self.add_text_code_line('sw $t1, 0($t0)')
        #Class name
        self.add_text_code_line(f'la $t1, {node.type}_name')
        self.add_text_code_line('sw $t1, 4($t0)')
        #Class size
        self.add_text_code_line(f'li $t1, {total}')
        self.add_text_code_line('sw $t1, 8($t0)')
        #Class methods pointer
        self.add_text_code_line(f'la $t1, {node.type}_methods') 
        self.add_text_code_line('sw $t1, 12($t0)')
        #Store instance address in destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t0, {offset}($sp)')

    @visitor.when(CilExpr.TypeOfNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#TypeOf {node.variable}')
        #Get offset of variable
        obj_offset = self.variables_offset[self.current_function.name][node.variable]
        #Getting object address
        self.add_text_code_line(f'lw $t0, {obj_offset}($sp)')
        #Getting type name from the second position in object layout
        self.add_text_code_line('lw $t1, 4($t0)')
        #Get offset of destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t1, {offset}($sp)') 

    @visitor.when(CilExpr.CallNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#CallNode {node.method_name}')

        self.add_text_code_line('move $t0, $sp')
        #Visit all parameters
        for param in node.params:
            self.visit(param)
        #Jump to the function
        self.add_text_code_line(f'jal {node.method_name}')
        #Store result in destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a1, {offset}($sp)')

    @visitor.when(CilExpr.VCallNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#VCall {node.method_name}')

        self.add_text_code_line('move $t0, $sp')
        #Visit all parameters
        for param in node.params:
            self.visit(param)

        #Getting instance address
        i_offset = self.variables_offset[self.current_function.name][node.instance]
        self.add_text_code_line(f'lw $t1, {i_offset}($t0)')
        #Adding jump to error in case of instance is void
        self.add_text_code_line('la $t0, void')
        self.add_text_code_line('beq $t1, $t0, dispatch_void_error')
        #Getting dispatch table address
        self.add_text_code_line(f'lw $t2, 12($t1)')
        #Getting method address
        method_offset = self.methods_offset[node.type][node.method_name]
        self.add_text_code_line(f'lw $t3, {method_offset}($t2)')
        #Jump to the function
        self.add_text_code_line('jal $t3')
        #Store result in destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a1, {offset}($sp)')
    
    @visitor.when(CilExpr.ArgNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'# Arg {node.arg_name}')
        #Get offset of arg
        offset = self.variables_offset[self.current_function.name][node.arg_name]
        #Save arg in stack
        self.add_text_code_line(f'lw $t1, {offset}($t0)')
        self.add_text_code_line('addi $sp, $sp, -4')
        self.add_text_code_line('sw $t1, 0($sp)')

    @visitor.when(CilExpr.IfGotoNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'# IFGoto {node.variable} -> {node.label}')
        #Get variable offset
        offset = self.variables_offset[self.current_function.name][node.variable]
        self.add_text_code_line(f'lw $t0, {offset}($sp)')
        #If condition is true jump to label
        self.add_text_code_line('lw $a0, 16($t0)')
        self.add_text_code_line(f'bnez $a0, {node.label}')

    @visitor.when(CilExpr.LabelNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#LabelNode {node.label}')
        #Declare label
        self.add_text_code_line(f'{node.label}:')

    @visitor.when(CilExpr.GotoNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Goto {node.label}')
        #Unconditionally branch to the instruction at the label
        self.add_text_code_line(f'b {node.label}')

    @visitor.when(CilExpr.ReturnNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Return {node.return_value}')
        #If function has return value, put it in $a1
        if node.return_value:
            offset = self.variables_offset[self.current_function.name][node.return_value]
            self.add_text_code_line(f'lw $a1, {offset}($sp)')
        #If not, put 0 in $a1
        else:
            self.add_text_code_line('move $a1, $zero')

    @visitor.when(CilExpr.LoadIntNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#LoadInt {node.num}')
        #Load integer
        self.add_text_code_line(f'li $t0, {node.num}')
        #Store result in destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t0, {offset}($sp)')
    
    @visitor.when(CilExpr.LoadStrNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#LoadStr {node.msg}')
        #Load string
        self.add_text_code_line(f'la $t0, {node.msg}')
        #Store result in destination local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t0, {offset}($sp)')

    @visitor.when(CilExpr.LengthNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Length of {node.variable}')
        #Get address of variable
        offset = self.variables_offset[self.current_function.name][node.variable]
        self.add_text_code_line(f'lw $t0, {offset}($sp)')
        self.add_text_code_line('lw $t0, 16($t0)')
        self.add_text_code_line('li $a0, 0')
        #Start loop count 
        self.add_text_code_line('count:')
        #Load current char
        self.add_text_code_line('lb $t1, 0($t0)')
        #Finish if zero was found
        self.add_text_code_line('beqz $t1, end')
        #Next char
        self.add_text_code_line('addi $t0, $t0, 1')
        #Length count + 1
        self.add_text_code_line('addi $a0, $a0, 1')
        #Next iteration
        self.add_text_code_line('j count')
        #End label
        self.add_text_code_line('end:')
        #Store length count address in variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')

    @visitor.when(CilExpr.ConcatNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Concat {node.str1} {node.str2}')

        #Get offsets of str1, str2, len1, len2
        str1_offset = self.variables_offset[self.current_function.name][node.str1]
        str2_offset = self.variables_offset[self.current_function.name][node.str2]
        len1_offset = self.variables_offset[self.current_function.name][node.len1]
        len2_offset = self.variables_offset[self.current_function.name][node.len2]

        #Reserve space for concatanation
        self.add_text_code_line(f'lw $a0, {len1_offset}($sp)')
        self.add_text_code_line(f'lw $t0, {len2_offset}($sp)')
        self.add_text_code_line('add $a0, $a0, $t0')
        #Adding one space more for '\0'
        self.add_text_code_line('addi $a0, $a0, 1') 
        #The beginning of the new reserved address is in $v0 and saved in $t3
        self.add_text_code_line('li $v0, 9')
        self.add_text_code_line('syscall')
        self.add_text_code_line('bge $v0, $sp, heap_error')
        self.add_text_code_line('move $t3, $v0')
        #Loading beginning of str1 and str2 address in $t0 and $t1 respectively
        self.add_text_code_line(f'lw $t0, {str1_offset}($sp)')
        self.add_text_code_line(f'lw $t1, {str2_offset}($sp)')

        #Copy string 1 starting in $t0 to $v0
        self.add_text_code_line('copy_str:')
        #Loading current char in str1
        self.add_text_code_line('lb $t2, 0($t0)')
        #Storing current char in result
        self.add_text_code_line('sb $t2, 0($v0)')
        #Jump to concat if zero is found
        self.add_text_code_line('beqz $t2, concat_str')
        #Next char
        self.add_text_code_line('addi $t0, $t0, 1')
        #Next availabe byte
        self.add_text_code_line('addi $v0, $v0, 1')
        #Next iteration
        self.add_text_code_line('j copy_str')

        #Concat string 2 starting in $t1 to $v0
        self.add_text_code_line('concat_str:')
        #Loading current char in str1
        self.add_text_code_line('lb $t2, 0($t1)')
        #Storing current char in result
        self.add_text_code_line('sb $t2, 0($v0)')
        #Jump to end if zero is found
        self.add_text_code_line('beqz $t2, end_concat_str')
        #Next char
        self.add_text_code_line('addi $t1, $t1, 1')
        #Next availabe byte
        self.add_text_code_line('addi $v0, $v0, 1')
        #Next iteration
        self.add_text_code_line('j concat_str')
        #End of loop
        self.add_text_code_line('end_concat_str:')
        #Putting '\0' at the end
        self.add_text_code_line('sb $0, ($v0)')

        #Store result string address in local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t3, {offset}($sp)')

    @visitor.when(CilExpr.SubStrNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Substr {node.str}:string {node.index}:index {node.len}:length')

        #Get offsets of index, str and len
        index_offset = self.variables_offset[self.current_function.name][node.index]
        str_offset = self.variables_offset[self.current_function.name][node.str]
        len_offset = self.variables_offset[self.current_function.name][node.len]

        #Reserve space for substring
        self.add_text_code_line(f'lw $a0, {len_offset}($sp)')
        #Adding one space more for '\0'
        self.add_text_code_line('addi $a0, $a0, 1')
        #The beginning of the new reserved address is in $v0 
        self.add_text_code_line('li $v0, 9')
        self.add_text_code_line('syscall')
        self.add_text_code_line('bge $v0, $sp, heap_error')

        #Load str, index, len
        self.add_text_code_line(f'lw $t0, {index_offset}($sp)')
        self.add_text_code_line(f'lw $t1, {len_offset}($sp)')
        self.add_text_code_line(f'lw $t4, {str_offset}($sp)')
        self.add_text_code_line('lw $t2, 16($t4)')

        #If index is not valid, jump to error
        self.add_text_code_line('bltz $t0, substr_error')
        #Reset $a0
        self.add_text_code_line('li $a0, 0')
        #Skip first index chars
        self.add_text_code_line('skip_char:')
        #If we are at char with pos == index, jump to end of loop
        self.add_text_code_line('beq $a0, $t0, end_skip')
        #Count of char
        self.add_text_code_line('addi $a0, $a0, 1')
        #Next char 
        self.add_text_code_line('addi $t2, $t2, 1')
        #End of string < index, error
        self.add_text_code_line('beq $t2, $zero, substr_error')
        #Next iteration
        self.add_text_code_line('j skip_char')
        #End of loop
        self.add_text_code_line('end_skip:')
        #Reset $a0
        self.add_text_code_line('li $a0, 0')
        #Saving start of substring
        self.add_text_code_line('move $t3, $v0')

        #Copy char from string $t2 until length stored in $t1 with initial index $t0
        self.add_text_code_line('substr_copy:')
        #If count of char equal length jump to end of loop
        self.add_text_code_line('beq $a0, $t1, end_substr_copy')
        #Reset $t0
        self.add_text_code_line('li $t0, 0')
        #Loading current char in str
        self.add_text_code_line('lb $t0, 0($t2)')
        #Storing current char in result
        self.add_text_code_line('sb $t0, 0($v0)')
        #Next char 
        self.add_text_code_line('addi $t2, $t2, 1')
        #End of string < index, error
        self.add_text_code_line('beq $t2, $zero, substr_error')
        #Next availabe byte
        self.add_text_code_line('addi $v0, $v0, 1')
        #Char count + 1
        self.add_text_code_line('addi $a0, $a0, 1')
        #Next iteration
        self.add_text_code_line('j substr_copy')
        #End of loop
        self.add_text_code_line('end_substr_copy:')
        #Putting '\0' at the end
        self.add_text_code_line('sb $0, ($v0)')

        #Store result substring address in local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $t3, {offset}($sp)')

    @visitor.when(CilExpr.ReadIntegerNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#ReadInteger {node.line}')
        #Read integer
        self.add_text_code_line('li $v0, 5')
        self.add_text_code_line('syscall')
        #Store integer address in local variable
        offset = self.variables_offset[self.current_function.name][node.line]
        self.add_text_code_line(f'sw $v0, {offset}($sp)')

    @visitor.when(CilExpr.ReadStringNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#ReadString {node.line}')
        #Read string
        self.add_text_code_line('la $a0, input_str')
        self.add_text_code_line('li $a1, 2048')
        self.add_text_code_line('li $v0, 8')
        self.add_text_code_line('syscall')

        self.add_text_code_line('move $t0, $a0')
        #Read char by char until the end of the string
        self.add_text_code_line('read_char:')
        #Reset $t1
        self.add_text_code_line('li $t1, 0')
        #Load current char
        self.add_text_code_line('lb $t1, 0($t0)')
        #If string final char found jump to the other loop
        self.add_text_code_line('beqz $t1, remove_characters_str_end')
        #Next char
        self.add_text_code_line('addi $t0, $t0, 1')
        #Next iteration
        self.add_text_code_line('j read_char')

        #Remove last characters if they are '\n' or '\r\n'
        self.add_text_code_line('remove_characters_str_end:')
        #Move to char at length - 1
        self.add_text_code_line('addi $t0, $t0, -1')
        #Reset $t1
        self.add_text_code_line('li $t1, 0')
        #Load current char
        self.add_text_code_line('lb $t1, 0($t0)')
        #Remove char only if it is '\n'
        self.add_text_code_line('bne $t1, 10, rcs_end')
        #Trying to remove '\r\n'
        self.add_text_code_line('sb $0, 0($t0)')
        #Move to char at length - 2
        self.add_text_code_line('addi $t0, $t0, -1')
        #Reset $t1
        self.add_text_code_line('lb $t1, 0($t0)')
        #Load current char
        self.add_text_code_line('bne $t1, 13, rcs_end')
        #Remove '\r\n'
        self.add_text_code_line('sb $0, 0($t0)')
        #Next iteration
        self.add_text_code_line('j remove_characters_str_end')
        #End of loop
        self.add_text_code_line('rcs_end:')

        #Store string address in local variable
        offset = self.variables_offset[self.current_function.name][node.line]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')

    @visitor.when(CilExpr.PrintIntegerNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#PrintInteger {node.line}')
        #Print
        self.add_text_code_line('li $v0, 1')
        #If line it is a value
        if isinstance(node.line, int):
            self.add_text_code_line(f'li $a0, {node.line}')
        #If line it is a variable
        else:
            #Get offset of variable
            offset = self.variables_offset[self.current_function.name][node.line]
            self.add_text_code_line(f'lw $a0, {offset}($sp)')
        self.add_text_code_line('syscall')

    @visitor.when(CilExpr.PrintStringNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#PrintString {node.line}')
        #Get offset of string
        offset = self.variables_offset[self.current_function.name][node.line]
        self.add_text_code_line(f'lw $a0, {offset}($sp)')
        #Print string
        self.add_text_code_line('li $v0, 4')
        self.add_text_code_line('syscall')

    @visitor.when(CilExpr.AbortNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Abort')
        #Abort
        self.add_text_code_line('li $v0, 10')
        self.add_text_code_line('syscall')

    @visitor.when(CilExpr.CaseNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Case {node.local_expr}')
        #Get offset
        offset = self.variables_offset[self.current_function.name][node.local_expr]
        self.add_text_code_line(f'lw $t0, {offset}($sp)')
        self.add_text_code_line('lw $t1, 0($t0)')
        self.add_text_code_line('la $a0, void')
        #Jump to first case if not void
        self.add_text_code_line(f'bne $t1, $a0, {node.first_label}')
        #If void jump to error
        self.add_text_code_line(f'b case_void_error')
    
    @visitor.when(CilExpr.ActionNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Action')
        #Jump to the corresponding label
        self.add_text_code_line(f'blt $t1, {node.tag}, {node.next_label}')
        self.add_text_code_line(f'bgt $t1, {node.max_tag}, {node.next_label}')

    @visitor.when(CilExpr.StringEqualsNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#StringEquals {node.str1} = {node.str2}')
        #Get offset of str1 and str2
        str1_offset = self.variables_offset[self.current_function.name][node.str1]
        str2_offset = self.variables_offset[self.current_function.name][node.str2]

        #Loading beginning of str1 and str2 address in $t1 and $t2 respectively
        self.add_text_code_line(f'lw $t1, {str1_offset}($sp)')
        self.add_text_code_line(f'lw $t2, {str2_offset}($sp)')

        #Comparing char by char
        self.add_text_code_line('compare_str:')
        #Reset $t3
        self.add_text_code_line('li $t3, 0')
        #Loading current char from str1
        self.add_text_code_line('lb $t3, 0($t1)')
        #Reset $t4
        self.add_text_code_line('li $t4, 0')
        #Loading current char from str2
        self.add_text_code_line('lb $t4, 0($t2)')
        #Compare current bytes
        self.add_text_code_line('seq $a0, $t3, $t4')
        #Jump to end if current char are differents
        self.add_text_code_line('beqz $a0, end_compare_str')
        #Jump to end if it is found the str1 final char
        self.add_text_code_line('beqz $t3, end_compare_str')
        #Jump to end if it is found the str2 final char
        self.add_text_code_line('beqz $t4, end_compare_str')
        #Next char str1
        self.add_text_code_line('addi $t1, $t1, 1')
        #Next char str2
        self.add_text_code_line('addi $t2, $t2, 1')
        #Next iteration
        self.add_text_code_line('j compare_str')
        #End of loop
        self.add_text_code_line('end_compare_str:')

        #Store result compare address in local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')

    @visitor.when(CilExpr.IsVoidNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#IsVoid {node.expr}')
        #Load void to $t0
        self.add_text_code_line('la $t0, void')
        #Get offset
        expr_offset = self.variables_offset[self.current_function.name][node.expr]
        self.add_text_code_line(f'lw $t1, {expr_offset}($sp)')
        #Check if it is void
        self.add_text_code_line('seq $a0, $t0, $t1')
        #Store result address in local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $a0, {offset}($sp)')

    @visitor.when(CilExpr.CopyNode)
    def visit(self, node):
        #Comment
        self.add_text_code_line(f'#Copy {node.type}')
        #Get self address
        self_offset = self.variables_offset[self.current_function.name][node.type]
        self.add_text_code_line(f'lw $t0, {self_offset}($sp)')
        #Get size
        self.add_text_code_line('lw $a0, 8($t0)')
        self.add_text_code_line('mul $a0, $a0, 4')
        self.add_text_code_line('li $v0, 9')
        self.add_text_code_line('syscall')
        #If heap error jump to error
        self.add_text_code_line('bge $v0, $sp, heap_error')
        self.add_text_code_line('move $t1, $v0')

        #Reset $a0
        self.add_text_code_line('li $a0, 0')
        #Load size
        self.add_text_code_line('lw $t3, 8($t0)')
        #copy all slots (attributes, methods, size, tag)
        self.add_text_code_line('copy_object:')
        #Load current object word from source
        self.add_text_code_line('lw $t2, 0($t0)')
        #Store current object word to destination 
        self.add_text_code_line('sw $t2, 0($t1)')
        #Next word source object
        self.add_text_code_line('addi $t0, $t0, 4')
        #Next word destination object
        self.add_text_code_line('addi $t1, $t1, 4')
        #Size count
        self.add_text_code_line('addi $a0, $a0, 1')
        #If there are still words for copy, jump to copy_object
        self.add_text_code_line('blt $a0, $t3, copy_object')

        #Store instance of object address in local variable
        offset = self.variables_offset[self.current_function.name][node.local_var]
        self.add_text_code_line(f'sw $v0, {offset}($sp)')





    

        



    



    





    

    