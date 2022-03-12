from CodeGen.Assembler.mips_data import *
from CodeGen.Intermediate import cil
from Semantic import visitor


class CILToSPIMVisitor:
    
    def __init__(self):
        self.dotdata = list()
        self.dottext = list()
        self.current_function = None
        self.defined_types = None
        self.args_for_call = list()

    def add_data(self, data):
        self.dotdata.append(data)
    
    def add_instruction(self, instruction):
        self.dottext.append(instruction)
    
    def get_addr(self, offset, register):
        return f'{offset}({register})'
    
    def get_stack_addr(self, name, offset = 0):
        for i in range(len(self.current_function.params)):
            if name == self.current_function.params[i].name:
                return self.get_addr(4 * (i + 1 + len(self.current_function.localvars) + offset), sp_REGISTER)
        
        for i in range(len(self.current_function.localvars)):
            if name == self.current_function.localvars[i].name:
                return self.get_addr(4 * (i + 1 + offset), sp_REGISTER)
            

    @visitor.on('node')
    def visit(self, node):
        pass


    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        self.defined_types = node.dottypes
        self.add_data(Asciiz('abort_message', 'Abort called from class ').__mips__())
        self.add_data(Asciiz('eol', '\\n').__mips__())
        self.add_data(Asciiz('empty_string', "").__mips__())
        
        for _data in node.dotdata:
            self.visit(_data)
        for _type in node.dottypes:
            self.visit(_type)
        for _code in node.dotcode:
            self.visit(_code)
        
        return (self.dotdata, self.dottext)
    
    
    @visitor.when(cil.TypeNode)
    def visit(self, node):
        """
        node.name -> DataNode
        node.parent -> str
        node.attributes -> [ str ... ]
        node.methods = [ (str, str) ... ]
        """
        self.add_data(Type(node.name, node.parent, node.attributes, node.methods).__mips__())
    
    
    @visitor.when(cil.DataNode)
    def visit(self, node):
        """
        node.name -> str
        node.value -> str
        """
        self.add_data(Asciiz(node.name, node.value).__mips__())
    
    
    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        """
        node.name -> str
        node.params -> [ ParamNode ... ]
        node.localvars -> [ LocalNode ... ]
        node.instructions -> [ Node ... ]
        """
        self.current_function = node
        instructions = list()
        instructions.append(Addi(sp_REGISTER, sp_REGISTER, -4 * (len(self.current_function.localvars)+1)).__mips__())
        instructions.append(Sw(ra_REGISTER, self.get_addr(0, sp_REGISTER)).__mips__())
        
        for instr in node.instructions:
            instructions += self.visit(instr)
        
        self.add_instruction(Function(node.name, instructions).__mips__())
        self.current_function = None
        

    @visitor.when(cil.ParamNode)
    def visit(self, node):
        """
        node.name -> str
        """
        return []
    

    @visitor.when(cil.LocalNode)
    def visit(self, node):
        """
        node.name -> str
        """
        return []


    @visitor.when(cil.AssignNode)
    def visit(self, node):
        """
        node.dest -> str
        node.source -> str
        """
        instructions = list()
        
        source = self.get_stack_addr(node.source)
        dest = self.get_stack_addr(node.dest)
        
        instructions.append(Lw(a_REGISTERS[0], source).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(0, a_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(12, t_REGISTERS[0])).__mips__())
        instructions.append(Jalr(ra_REGISTER, t_REGISTERS[0]).__mips__())
        
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions


    @visitor.when(cil.IntComplementNode)
    def visit(self, node):
        """
        node.dest -> str
        node.source -> str
        """
        instructions = list()
        
        source = self.get_stack_addr(node.source)
        dest = self.get_stack_addr(node.dest)
        
        instructions.append(La(a_REGISTERS[0], "type_Int").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], source).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        
        instructions.append(Sub(t_REGISTERS[1], zero_REGISTER, t_REGISTERS[1]).__mips__())
        instructions.append(Sw(t_REGISTERS[1], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.BoolComplementNode)
    def visit(self, node):
        """
        node.dest -> str
        node.source -> str
        """
        instructions = list()
        
        source = self.get_stack_addr(node.source)
        dest = self.get_stack_addr(node.dest)

        instructions.append(La(a_REGISTERS[0], "type_Bool").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], source).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        
        instructions.append(Li(t_REGISTERS[2], 1).__mips__())
        instructions.append(Sub(t_REGISTERS[1], t_REGISTERS[2], t_REGISTERS[1]).__mips__())
        instructions.append(Sw(t_REGISTERS[1], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
        
    
    @visitor.when(cil.PlusNode)
    def visit(self, node):
        """
        node.dest -> str
        node.left -> str
        node.right -> str
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(La(a_REGISTERS[0], "type_Int").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Lw(t_REGISTERS[2], right).__mips__())
        instructions.append(Lw(t_REGISTERS[2], self.get_addr(4, t_REGISTERS[2])).__mips__())
        
        instructions.append(Add(t_REGISTERS[3], t_REGISTERS[1], t_REGISTERS[2]).__mips__())
        instructions.append(Sw(t_REGISTERS[3], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        """
        node.dest -> str
        node.left -> str
        node.right -> str
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(La(a_REGISTERS[0], "type_Int").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Lw(t_REGISTERS[2], right).__mips__())
        instructions.append(Lw(t_REGISTERS[2], self.get_addr(4, t_REGISTERS[2])).__mips__())
        
        instructions.append(Sub(t_REGISTERS[3], t_REGISTERS[1], t_REGISTERS[2]).__mips__())
        instructions.append(Sw(t_REGISTERS[3], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.StarNode)
    def visit(self, node):
        """
        node.dest -> str
        node.left -> str
        node.right -> str
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(La(a_REGISTERS[0], "type_Int").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Lw(t_REGISTERS[2], right).__mips__())
        instructions.append(Lw(t_REGISTERS[2], self.get_addr(4, t_REGISTERS[2])).__mips__())
        
        instructions.append(Mult(t_REGISTERS[1], t_REGISTERS[2]).__mips__())
        instructions.append(Mflo(t_REGISTERS[3]).__mips__())
        instructions.append(Sw(t_REGISTERS[3], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.DivNode)
    def visit(self, node):
        """
        node.dest -> str
        node.left -> str
        node.right -> str
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(La(a_REGISTERS[0], "type_Int").__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Lw(t_REGISTERS[2], right).__mips__())
        instructions.append(Lw(t_REGISTERS[2], self.get_addr(4, t_REGISTERS[2])).__mips__())
        
        instructions.append(Div(t_REGISTERS[1], t_REGISTERS[2]).__mips__())
        instructions.append(Mflo(t_REGISTERS[3]).__mips__())
        instructions.append(Sw(t_REGISTERS[3], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        """
        node.dest -> str       / Variable de destino
        node.instance -> str   / Variable instancia
        node.pos -> int        / Numero del atributo
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        instance = self.get_stack_addr(node.instance)
        
        instructions.append(Lw(t_REGISTERS[0], instance).__mips__())
        instructions.append(Lw(a_REGISTERS[0], self.get_addr(4 * (1 + node.pos), t_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(0, a_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(12, t_REGISTERS[0])).__mips__())
        instructions.append(Jalr(ra_REGISTER, t_REGISTERS[0]).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        
        return instructions
    
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        """
        node.source -> str      / Variable de origen
        node.instance -> str    / Variable instancia
        node.pos -> int         / Numero del Atributo
        """
        instructions = list()
        
        source = self.get_stack_addr(node.source)
        instance = self.get_stack_addr(node.instance)
        
        instructions.append(Lw(a_REGISTERS[0], source).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(0, a_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(12, t_REGISTERS[0])).__mips__())
        instructions.append(Jalr(ra_REGISTER, t_REGISTERS[0]).__mips__())
        
        instructions.append(Lw(t_REGISTERS[1], instance).__mips__())
        instructions.append(Sw(v_REGISTERS[0], self.get_addr(4 * (1 + node.pos), t_REGISTERS[1])).__mips__())
        instructions.append(Sw(t_REGISTERS[1], instance).__mips__())
        
        return instructions
    
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        """
        node.type -> str    / Direccion del Tipo
        node.dest -> str    / Variable a la que se le asignara la direccion del espacio en memoria
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        
        instructions.append(La(a_REGISTERS[0], node.type).__mips__())
        instructions.append(Jal('create_instance').__mips__())
        
        if not node.value is None:
            if node.type == 'type_String':
                instructions.append(La(t_REGISTERS[0], node.value).__mips__())
            else:
                instructions.append(Li(t_REGISTERS[0], node.value).__mips__())
            instructions.append(Sw(t_REGISTERS[0], self.get_addr(4, v_REGISTERS[0])).__mips__())
        
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions        


    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        """
        node.obj -> str     / Variable de Tipo T
        node.dest -> str    / Variable donde se almacenara la direccion al tipo T
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        obj = self.get_stack_addr(node.obj)
        
        
        instructions.append(Lw(a_REGISTERS[0], obj).__mips__())
        instructions.append(Lw(a_REGISTERS[0], self.get_addr(0, a_REGISTERS[0])).__mips__())
        instructions.append(Lw(a_REGISTERS[0], self.get_addr(8, a_REGISTERS[0])).__mips__())
        instructions.append(Jal('str_assigment_from_str').__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions        


    @visitor.when(cil.LabelNode)
    def visit(self, node):
        """
        node.name -> str    / Nombre de la etiqueta
        """
        return [Label(node.name).__mips__()]


    @visitor.when(cil.GotoNode)
    def visit(self, node):
        """
        node.label -> str   / Nombre de la etiqueta
        """
        return [J(node.label).__mips__()]
    

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        """
        node.vname -> str       / Variable de tipo Bool
        node.goto_label -> str  / Nombre de la etiqueta
        """
        instructions = list()
        
        vname = self.get_stack_addr(node.vname)
        
        instructions.append(Lw(t_REGISTERS[0], vname).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(4, t_REGISTERS[0])).__mips__())
        instructions.append(Li(t_REGISTERS[1], 1).__mips__())
        instructions.append(Beq(t_REGISTERS[0], t_REGISTERS[1], node.goto_label).__mips__())
        
        return instructions
    
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        """
        node.function -> str    / Nombre de la funcion (en formato `function_<name>_at_<class>`)
        node.dest -> str        / Variable que almacenara el valor de retorno
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        
        instructions.append(Addi(sp_REGISTER, sp_REGISTER, -4 * len(self.args_for_call)).__mips__())
        
        for i in range(len(self.args_for_call)):
            instance = self.get_stack_addr(self.args_for_call[i].name, len(self.args_for_call))
            instructions.append(Lw(t_REGISTERS[0], instance).__mips__())
            instructions.append(Sw(t_REGISTERS[0], self.get_addr(4 * i, sp_REGISTER)).__mips__())

        instructions.append(Jal(node.function).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(0, sp_REGISTER)).__mips__())
        instance0 = self.get_stack_addr(self.args_for_call[0].name, len(self.args_for_call))
        instructions.append(Sw(t_REGISTERS[0], instance0).__mips__())
        instructions.append(Addi(sp_REGISTER, sp_REGISTER, 4 * len(self.args_for_call)).__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        self.args_for_call = list()
        return instructions
    
    
    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        """
        node.xtype -> str       / Variable que contiene la direccion al nombre de su tipo dinamico
        node.function -> str    / Nombre de la funcion (Solo el nombre, no esta en formato `function_<name>_at_<class>`)
        node.dest -> str        / Variable que almacenara el valor de retorno
        """
        pass
    

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        """
        node.name -> str    / Variable cuyo valor se pasara como argumento
        """
        self.args_for_call.append(node)
        return []
    
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        """
        node.ret -> str     / Variable que contiene el valor de retorno
        """
        instructions = list()
        ret = self.get_stack_addr(node.ret)
        instructions.append(Lw(v_REGISTERS[0], ret).__mips__())
        instructions.append(Lw(ra_REGISTER, self.get_addr(0, sp_REGISTER)).__mips__())
        instructions.append(Addi(sp_REGISTER, sp_REGISTER, 4 * (len(self.current_function.localvars)+1)).__mips__())
        instructions.append(Jr(ra_REGISTER).__mips__())
        return instructions
    
    
    @visitor.when(cil.RunTimeNode)
    def visit(self, node):
        instructions = list()
        instructions.append(La(a_REGISTERS[0], node.error).__mips__())
        instructions.append(Jal('runtime_error').__mips__())
        return instructions
    
    
    @visitor.when(cil.EndProgramNode)
    def visit(self, node):
        instructions = list()
        instructions.append(Li(v_REGISTERS[0], 10).__mips__())
        instructions.append(Syscall().__mips__())
        return instructions
    
    
    @visitor.when(cil.LoadNode)
    def visit(self, node):
        """
        node.dest -> dest   / Variable destino
        node.msg -> msg     / Variable de la seccion .data
        """
        instructions = list()
        
        dest = self.get_stack_addr(node.dest)
        
        instructions.append(La(a_REGISTERS[0], node.msg).__mips__())
        instructions.append(Jal('str_assigment_from_str').__mips__())
        instructions.append(Sw(v_REGISTERS[0], dest).__mips__())
        return instructions
    
    
    @visitor.when(cil.BranchEqualNode)
    def visit(self, node):
        """
        node.left -> str    / Variable con el valor izquierdo
        node.right -> str   / Variable con el valor derecho
        node.label -> str   / Etiqueta de salto
        """
        instructions = list()
        
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(Lw(a_REGISTERS[0], left).__mips__())
        instructions.append(Lw(a_REGISTERS[1], right).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(0, a_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(16, t_REGISTERS[0])).__mips__())
        instructions.append(Jalr(ra_REGISTER, t_REGISTERS[0]).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(4, v_REGISTERS[0])).__mips__())
        instructions.append(Li(t_REGISTERS[1], 1).__mips__())
        instructions.append(Beq(t_REGISTERS[0], t_REGISTERS[1], node.label).__mips__())
        return instructions
    
    
    @visitor.when(cil.BranchLTNode)
    def visit(self, node):
        """
        node.left -> str    / Variable con el valor izquierdo
        node.right -> str   / Variable con el valor derecho
        node.label -> str   / Etiqueta de salto
        """
        instructions = list()
        
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(Lw(t_REGISTERS[0], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], right).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(4, t_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Blt(t_REGISTERS[0], t_REGISTERS[1], node.label).__mips__())
        return instructions
    
    
    @visitor.when(cil.BranchLENode)
    def visit(self, node):
        """
        node.left -> str    / Variable con el valor izquierdo
        node.right -> str   / Variable con el valor derecho
        node.label -> str   / Etiqueta de salto
        """
        instructions = list()
        
        left = self.get_stack_addr(node.left)
        right = self.get_stack_addr(node.right)
        
        instructions.append(Lw(t_REGISTERS[0], left).__mips__())
        instructions.append(Lw(t_REGISTERS[1], right).__mips__())
        instructions.append(Lw(t_REGISTERS[0], self.get_addr(4, t_REGISTERS[0])).__mips__())
        instructions.append(Lw(t_REGISTERS[1], self.get_addr(4, t_REGISTERS[1])).__mips__())
        instructions.append(Ble(t_REGISTERS[0], t_REGISTERS[1], node.label).__mips__())
        return instructions