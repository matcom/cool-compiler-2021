from MIPS.builder import exceptions
import Utils.visitor as visitor
import MIPS.ast as mips

from CIL.ast import *

class MIPS:
    def __init__(self):
        self.data = ''
        self.text = ''

        #self.add_data(exceptions())
    
    def __str__(self):
        return f'\t\t.data\n{self.data}\n\t\t.text\n{self.text}'

    def add_data(self, value):
        self.data += f'{value}\n'
    
    def add_text(self, value):
        self.text += f'{value}\n'

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.class_tag = {type.name: i for i, type in enumerate(node.types)}

        for type in node.types:
            self.visit(type)

        self.add_data('heap:\n\t\t.word\t0')

        #for code in node.code:
        #    self.visit(code)

        return str(self)

    @visitor.when(TypeNode)
    def visit(self, node):
        name = node.name
        tag = self.class_tag[name]

         

    @visitor.when(CodeNode)
    def visit(self, node):
        self.add_text(f'{node.id}:')

        for instr in node.instrs:
            self.visit(instr)

    @visitor.when(AllocateNode)
    def visit(self, node):
        self.add_text(
        '''
        la	    $a0 Main_proto  	# create the Main object
        jal	    Object.copy		    # Call copy
        addiu	$sp $sp -4
        sw	    $a0 4($sp)		    # save the Main object on the stack
        move	$s0 $a0			    # set $s0 to point to self
        jal	    Main_init		    # initialize the Main object
        ''')