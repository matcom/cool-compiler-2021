from utils.mip_utils import registers as r, operations as o, datatype as dt
import visitors.visitor as visitor
from cil_ast.cil_ast import *

class CiltoMipsVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata =[]
        self.dotcode =[]
        self.context = context
        self.code = []
        self.data = []
        self.current_function: FunctionNode = None

    def stack_offset(self, name):
        all_ = self.current_function.params + self.current_function.localvars
        return -4*all_.index(name)
    
    def write_data(self, instruction):
        self.data.append(instruction)

    def write_code(self, instruction):
        self.code.append(instruction)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.dottypes = node.dottypes
        self.dotdata = node.dotdata
        self.dotcode = node.dotcode

        self.write_data('.data')  # initialize the .data segment
        self.write_data(f'p_error: {dt.asciiz} "Aborting from String"')
        self.write_data(f'zero_error: {dt.asciiz} "Division by zero"')
        self.write_data(f'range_error: {dt.asciiz} "Index out of range"')

    @visitor.when(TypeNode)
    def visit(self, node):
        pass

    @visitor.when(DataNode)
    def visit(self, node):
        pass

    @visitor.when(FunctionNode)
    def visit(self, node):
        methods = [
            'Object_abort',
            'Object_type_name',
            'Object_copy',
            'String_concat',
            'String_substr',
            'String_length',
            'IO_in_int',
            'IO_out_int',
            'IO_in_string',
            'IO_out_string',
        ]
        if node.fname in methods: 
            return
        pass
    
    @visitor.when(ParamNode)
    def visit(self, node):
        pass

    @visitor.when(LocalNode)
    def visit(self, node):
        pass

    @visitor.when(AssignNode)
    def visit(self, node):
        pass

    @visitor.when(PlusNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {}, {} # saving to $t1 the result'.format(o.add, r.t1, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))
        
    @visitor.when(MinusNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {}, {} # saving to $t1 the result'.format(o.sub, r.t1, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(StarNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {} # multiply'.format(o.mul, r.t1, r.t2))
        self.write_code('{} {} # get the result in lo'.format(o.mflo, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(DivNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        # zero exception
        # self.write_code("la $t0, zero_error")
        # self.write_code("sw $t0, ($sp)")
        # self.write_code("subu $sp, $sp, 4")
        self.write_code("beqz $t2, .raise")
        # self.write_code("addu $sp, $sp, 4")
        #
        self.write_code('{} {}, {} # divide'.format(o.div, r.t1, r.t2))
        self.write_code('{} {} # get the result in lo'.format(o.mflo, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(EqualNode)
    def visit(self, node):
        pass

    @visitor.when(LessNode)
    def visit(self, node):
        pass

    @visitor.when(LeqNode)
    def visit(self, node):
        pass

    @visitor.when(GotoNode)
    def visit(self, node):
        self.write_code('# goto ')
        self.write_code('{} {} # jump unconditionally'.format(o.j, node.label))

    @visitor.when(GotoIfNode)
    def visit(self, node):
        pos = self.stack_offset(node.condition)
        self.write_code('# goto if')
        self.write_code( '{} {} {}({}) # heap address'.format(o.lw, r.t0, pos, r.fp))
        self.write_code('{} {} 8({}) # value of condition'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {} {} # branch on not equal to 0'.format(o.bnez, r.t1, node.label))
        
    @visitor.when(GetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(SetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(AllocateNode)
    def visit(self, node):
        pass

    @visitor.when(TypeOfNode)
    def visit(self, node):
        pass

    @visitor.when(LabelNode)
    def visit(self, node):
        self.write_code("# a label")
        self.write_code("{}:".format(node.name))

    @visitor.when(IsTypeNode)
    def visit(self, node):
        pass

    @visitor.when(ParentTypeNode)
    def visit(self, node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self, node):
        pass

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        pass
    
    @visitor.when(ArgNode)
    def visit(self, node):
        pass

    @visitor.when(ReturnNode)
    def visit(self, node):
        pass

    @visitor.when(LoadNode)
    def visit(self, node):
        pass

    @visitor.when(LengthNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(PrefixNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(ToStrNode)
    def visit(self, node):
        pass

# Input espacio a reservar en $a0
# Output direccion de memoria reservada en $a0
    def mem_alloc(self):
        self.write_code(f"# Declartation of the mem_alloc")

        self.write_code(f"mem_alloc:")
        self.write_code(f"{o.add} {r.gp} {r.gp} {r.a0}")
        self.write_code(f"{o.blt} {r.gp} {r.s7} mem_alloc_end")# si se pasa del límite de memoria dar error
        self.write_code(f"{o.j} mem_error")
        self.write_code(f"mem_alloc_end:")
        self.write_code(f"{o.sub} {r.a0} {r.gp} {r.a0}")    
        self.write_code(f"{o.jr} {r.ra}")
        self.write_code(f"")

# en a0 tengo el la instancia
    def get_parent_prot(self):
        self.write_code(f"# get parent prototype") #
        self.write_code(f"get_parent_prot:")
        self.write_code(f"{o.lw} {r.t0} ({r.a0})")
        self.write_code(f"{o.sll} {r.t0} {r.t0} 2")# mult por 4 pa tener el offset
        self.write_code(f"{o.lw} {r.t0} ({r.s4})")
        self.write_code(f"{o.move} {r.a0} {r.t0}")
        self.write_code(f"{o.jr} {r.ra}")
        self.write_code(f"")

# funciones para errores en runtime
    def zero_error(self): # error al dividir por 0
        self.write_code(f"# Declartation of the zero-div runtime error")

        self.write_code(f"zero_error:")
        self.write_code(f"{o.la} {r.a0} _zero")
        self.write_code(f"")

        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")

    def substr_error(self):
        self.write_code(f"# Declartation of the substr-index.out.of.range runtime error")

        self.write_code(f"substr_error:")
        self.write_code(f"{o.la} {r.a0} _substr")
        self.write_code(f"")
        
        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")
    
    def mem_error(self):
        self.write_code(f"# Declartation of the memory-overflow runtime error")
        self.write_code(f"mem_error:")
        self.write_code(f"{o.la} {r.a0} _mem")
        self.write_code(f"")
        
        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")


    def utils_functs(self):
        self.mem_alloc()
        self.get_parent_prot()
        self.object_copy()
        self.str_eq()
        self.str_concat()
        self.str_substr()
        self.length()
        self.zero_error()
        self.mem_error()
        self.substr_error()