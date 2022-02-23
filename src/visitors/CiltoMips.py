from utils.mip_utils import registers, operations, datatype
import visitors.visitor as visitor
from cil_ast.cil_ast import *

class BaseCiltoMipsVisitor:
    def __init__(self, context):
        self.dotdata =[]
        self.dotcode =[]
        self.context = context
        
        
        


    # ======================================================================
    # =[ VISIT ]============================================================
    # ======================================================================

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        pass

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
        pass
        
    @visitor.when(MinusNode)
    def visit(self, node):
        pass

    @visitor.when(StarNode)
    def visit(self, node):
        pass

    @visitor.when(DivNode)
    def visit(self, node):
        pass

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
        pass

    @visitor.when(GotoIfNode)
    def visit(self, node):
        pass

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
        pass

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

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

# Input espacio a reservar en $a0
# Output direccion de memoria reservada en $a0
    def mem_alloc(self):
        self.write_to_text(f"# Declartation of the mem_alloc")

        self.write_to_text(f"mem_alloc:")
        self.write_to_text(f"{operations.add} {registers.gp} {registers.gp} {registers.a0}")
        self.write_to_text(f"{operations.blt} {registers.gp} {registers.s7} mem_alloc_end")# si se pasa del límite de memoria dar error
        self.write_to_text(f"{operations.j} mem_error")
        self.write_to_text(f"mem_alloc_end:")
        self.write_to_text(f"{operations.sub} {registers.a0} {registers.gp} {registers.a0}")    
        self.write_to_text(f"{operations.jr} {registers.ra}")
        self.write_to_text(f"")

# en a0 tengo el la instancia
    def get_parent_prot(self):
        self.write_to_text(f"# get parent prototype") #
        self.write_to_text(f"get_parent_prot:")
        self.write_to_text(f"{operations.lw} {registers.t0} ({registers.a0})")
        self.write_to_text(f"{operations.sll} {registers.t0} {registers.t0} 2")# mult por 4 pa tener el offset
        self.write_to_text(f"{operations.lw} {registers.t0} ({registers.s4})")
        self.write_to_text(f"{operations.move} {registers.a0} {registers.t0}")
        self.write_to_text(f"{operations.jr} {registers.ra}")
        self.write_to_text(f"")

# funciones para errores en runtime
    def zero_error(self): # error al dividir por 0
        self.write_to_text(f"# Declartation of the zero-div runtime error")

        self.write_to_text(f"zero_error:")
        self.write_to_text(f"{operations.la} {registers.a0} _zero")
        self.write_to_text(f"")

        self.write_to_text(f"{operations.li} {registers.v0} 4")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"{operations.li} {registers.v0} 10")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"")

    def substr_error(self):
        self.write_to_text(f"# Declartation of the substr-index.out.of.range runtime error")

        self.write_to_text(f"substr_error:")
        self.write_to_text(f"{operations.la} {registers.a0} _substr")
        self.write_to_text(f"")
        
        self.write_to_text(f"{operations.li} {registers.v0} 4")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"{operations.li} {registers.v0} 10")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"")
    
    def mem_error(self):
        self.write_to_text(f"# Declartation of the memory-overflow runtime error")
        self.write_to_text(f"mem_error:")
        self.write_to_text(f"{operations.la} {registers.a0} _mem")
        self.write_to_text(f"")
        
        self.write_to_text(f"{operations.li} {registers.v0} 4")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"{operations.li} {registers.v0} 10")
        self.write_to_text(f"{operations.syscall}")
        self.write_to_text(f"")


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