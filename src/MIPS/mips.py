from MIPS.builder import create_bool, create_disp, create_int, create_proto, create_string
from CIL.ast import *
import Tools.visitor as visitor

class MIPS:
    def __init__(self):
        self.data = ''
        self.text = ''

        self.int_data = ''
        self.int_const = {}
        
        self.string_data = ''
        self.string_const = {}   
        
        self.bool_data = ''
        self.bool_const = {
            0:'bool_const_0', 
            1:'bool_const_1'}
        
    def __str__(self):
        data = self.string_data \
            + self.int_data \
            + self.bool_data \
            + self.name_tab \
            + self.disp \
            + self.proto \
            + self.data

        return f'\t\t.data\n{data}\t\t.text\n{self.text}\n'

    def add_int_const(self, value=0):
        try:
            return self.int_const[value]
        except KeyError:
            name = f'int_const{len(self.int_const)}'
            self.int_data += create_int(name, self.tag['Int'], value)
            self.int_const[value] = name
            return name
    
    def add_string_const(self, value=''):
        try:
            return self.string_const[value]
        except KeyError:
            name = f'string_const{len(self.string_const)}'
            lenght = self.add_int_const(len(value))
            self.string_data += create_string(name, self.tag['String'], lenght, value)
            self.string_const[value] = name
            return name

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.disp = ''                  # Dispatsh of all object
        self.proto = ''                 # Prototype of all object
        self.name_tab = 'names_tab:\n'  # Table of all object name

        self.tag = {current_type.name : i for i, current_type in enumerate(node.types)}

        # Create Bool default values
        self.bool_data += create_bool(self.tag['Bool'])
        
        # Create Int and String default values
        self.add_string_const() 

        # Visit Type
        for type in node.types:
            self.visit(type)

        # Visit Code
        for code in node.code:
            self.visit(code)

        self.data += f'heap:\n\t\t.word\t0\n'

    @visitor.when(TypeNode)
    def visit(self, node):
        self.name_tab += f'\t\t.word\t{self.add_string_const(node.name)}\n'
        self.disp += create_disp(node.name, node.meths)
        self.proto += create_proto(node.name, self.tag[node.name], node.attrs)
    
    @visitor.when(CodeNode)
    def visit(self, node):
        self.current_function = node.meth
        
        self.visit(node.meth)
        for instr in node.instrs:
            self.visit(instr)
       
    @visitor.when(MethodNode)
    def visit(self, node):
        self.text += f'{node}:\n'
        
        if str(node) != 'main':
            self.text += f'\t\taddiu \t $sp $sp -12\n'
            self.text += f'\t\tsw    \t $fp 12($sp)\n'
            self.text += f'\t\tsw    \t $ra 8($sp)\n'
            self.text += f'\t\tsw    \t $s0 4($sp)\n'
            self.text += f'\t\taddiu \t $fp $fp 4\n'

    @visitor.when(AllocateNode)
    def visit(self, node):
        self.text += f'\t\tla   \t $a0 {node.value_2}_proto\n'
        self.text += f'\t\tjal  \t Object_copy\n'

    @visitor.when(ArgumentNode)
    def visit(self, node):
        self.text += f'\t\tmove \t $a0 $v0'

    @visitor.when(ReturnNode)
    def visit(self, node):
        self.text += f'\t\tlw    \t $fp 12($sp)\n'
        self.text += f'\t\tlw    \t $ra 8($sp)\n'
        self.text += f'\t\tlw    \t $s0 2($sp)\n'
        self.text += f'\t\taddiu \t $sp $sp 12\n'
        self.text += f'\t\tjr    \t $ra\n'