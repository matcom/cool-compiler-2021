from . import visitor
from . import ast_nodes_cil as cil
from . import ast_nodes_mips as mips


class BaseCILToMIPSVisitor:
    def __init__(self, context):
        self.dotdata = []
        self.dottext = []
        
        self.context = context

        self.current_function = None
        self.current_function_stk = []

    ## basic methods
    def register_instruction(self, instruction):
        self.dottext.append(instruction)
        return instruction

    def register_empty_instruction(self):
        self.dottext.append(mips.EmptyInstructionNode())
        return self.dottext[-1]
    
    def register_empty_data(self):
        self.dotdata.append(mips.EmptyDataNode())

    def register_comment(self, comment):
        self.dottext.append(mips.CommentNode(comment))
        return self.dottext[-1]
    
    ## register basic data types
    def register_word(self, name, value):
        data = mips.WordDataNode(name, value)
        self.dotdata.append(data)
        return data

    def register_asciiz(self, name, value):
        data = mips.AsciizDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_space(self, name, value):
        data = mips.SpaceDataNode(name, value)
        self.dotdata.append(data)
        return data
    
    def register_instantiation(self, size) -> mips.InstructionNode:
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        if isinstance(size, int):
            self.register_instruction(mips.AddiNode("$a0", "$zero", f"{size}"))
        if isinstance(size, str):
            self.register_instruction(mips.MoveNode("$a0", size))
        self.register_instruction(mips.SystemCallNode())

    def to_data_type(self, data_name: str, type_name: str):
        return f"type_{type_name}_{data_name}"

    def offset_of(self, local_name: str):
        stack_size = 4 * len(self.current_function_stk)
        index = 4 * self.current_function_stk.index(local_name)
        return stack_size - index - 4
    
        
class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        for type_node in node.dottypes:
            self.visit(type_node)

        for function_node in node.dotcode:
            self.visit(function_node)

        for data_node in node.data:
            self.visit(data_node)
        
        return mips.ProgramNode(self.dotdata, self.dottext)
    
    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        #por cada atributo reservo una palabra
        size = 4 * (len(node.attributes) + len(node.methods))

        self.register_word(f"type_{node.name}", str(size))
        self.register_word(self.to_data_type("inherits_from", node.name), f"type_{node.parent}" if node.parent != "null" else "0")
        self.register_word(self.to_data_type("name_address", node.name), f"type_{node.name}_name_size")
        
        for method, function in node.methods:
            self.register_word(self.to_data_type(method, node.name), function)
        
        self.register_empty_data()

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        pass

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        self.current_function = node
        self.register_instruction(mips.LabelNode(node.name))

        param_names = [x.name for x in self.current_function.params]
        local_names = [x.name for x in self.current_function.local_vars]
        ##
        ## self.current_function_stk = ["$ra"] + local_names
        self.current_function_stk = ["$ra"] + param_names + local_names

        locals_size = 4 * len(self.current_function.local_vars)
        stack_size = 4 * len(self.current_function_stk)
        

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        pass 

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        self.register_comment(f"{node.dest} <- {node.source}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
    
    @visitor.when(cil.AssignIntNode)
    def visit(self, node: cil.AssignIntNode):
        self.register_comment(f"{node.dest} <- {node.source} WHERE {node.source} IS INT")
        self.register_instantiation(12)
        
        # puntero para node.source
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        # $t1 = type of node.source
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)"))
        # $t2 = value of node.source
        self.register_instruction(mips.LoadWordNode("$t2", "8($t0)"))
    
        # Save type of node.dest
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)"))
        # Save size of node.dest
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        # Save value of node.dest
        self.register_instruction(mips.StoreWordNode("$t2", "8($v0)"))

        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    @visitor.when(cil.ParentNode)
    def visit(self, node: cil.ParentNode):
        self.register_comment(f"{node.dest} PARENT OF: {node.source}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "4($t0)"))
        
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        self.register_comment("ADD")
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t2 = $t0 + $t1
        self.register_instruction(mips.AddNode("$t2", "$t0", "$t1"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))


    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        self.register_comment("MINUS")
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t2 = $t0 - $t1
        self.register_instruction(mips.SubNode("$t2", "$t0", "$t1"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        self.register_comment("MULT")        
        
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t2 = $t0 * $t1
        self.register_instruction(mips.MultNode("$t0", "$t1"))
        # mode from LOW
        self.register_instruction(mips.MoveFromLowNode("$t2"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        self.register_comment("DIV")
        
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t2 = $t0 / $t1
        self.register_instruction(mips.DivNode("$t0", "$t1"))
        # move from low
        self.register_instruction(mips.MoveFromLowNode("$t2"))

        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))
    
    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        self.register_comment("EQUAL")
        
        # $t0 para el left
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t1 para el right
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # t2 = $t0 == $t1
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))

        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))

    @visitor.when(cil.XorNode)
    def visit(self, node: cil.XorNode):
        self.register_comment("XOR")
        
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t0 = $t0 ^ $t1
        self.register_instruction(mips.XorNode("$t2", "$t0", "$t1"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))
        
    
    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        self.register_comment("LESS EQUAL")
        
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        # $t2 = $t0 <= $t1
        self.register_instruction(mips.SleNode("$t2", "$t0", "$t1"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))
    
    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        self.register_comment("LESS THAN")
        ## procesando binary op
        # $t0 left op addr 
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        # $t0 left op value
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 right op addr
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        # $t1 right op value
        self.register_instruction(mips.LoadWordNode("$t1", "8($t1)"))
        
        #  $t2 = $t0 < $t1
        self.register_instruction(mips.SltNode("$t2", "$t0", "$t1"))
        
        # procesando op binaria de tipo Int
        self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))
    
    
    @visitor.when(cil.EndOfLineNode) ######
    def visit(self, node: cil.EndOfLineNode):
        pass

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        pass

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        pass

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        pass

    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        pass
    
    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode):
        pass

    @visitor.when(cil.SetMethodNode)
    def visit(self, node: cil.SetMethodNode):
        pass
    
    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode):
        pass

    @visitor.when(cil.SetValueInIndexNode)
    def visit(self, node: cil.SetValueInIndexNode):
        pass

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        self.register_comment(f"ALLOCATE {node.type}")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.LoadWordNode("$a0", f"type_{node.type}"))
        self.register_instruction(mips.SystemCallNode())
        
        # $t0 = tipo de direccion
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.type}"))
        # ajustando tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)"))
        # tamaño en la 2da word
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        # {node.dest} -> direccion de -> {node.type}
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.AllocateIntNode)
    def visit(self, node: cil.AllocateIntNode):
        self.register_comment(f"ALLOCATE INT {node.type}")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        
        # self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        # self.register_instruction(mips.LoadWordNode("$a0", f"type_{node.type}"))
        # self.register_instruction(mips.SystemCallNode())
        
        # $t0 = tipo de direccion
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.type}"))
        # ajustando tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)"))
        # tamaño en la 2da word
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        # {node.dest} -> direccion de -> {node.type}
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))
    
    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode):
        self.register_comment(f"ALLOCATE BOOL {node.value}")

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        self.register_empty_instruction()
        
        ##
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        # self.register_instruction(mips.LoadWordNode("$a0", f"type_{node.type}"))
        # self.register_instruction(mips.SystemCallNode())
        
        # $t0 = tipo de direccion
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.type}"))
        # ajustando tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)"))
        # tamaño en la 2da word
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        # {node.dest} -> direccion de -> {node.type}
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))
        
    
    @visitor.when(cil.AllocateStringNode)
    def visit(self, node: cil.AllocateStringNode):
        self.register_comment(f"ALLOCATING STRING")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        
        # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
        self.register_instruction(mips.AddiNode("$a0", "$zero", f"{9 + node.length}"))
        self.register_instruction(mips.SystemCallNode())
        
        self.register_empty_instruction()
        
        ### define type 
    
    @visitor.when(cil.AllocateNullNode)
    def visit(self, node: cil.AllocateNullNode):
        self.register_comment(f"ALLOCATE NUll into {node.dest}")
        
        # node.dest = 0
        self.register_instruction(mips.StoreWordNode("$zero", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.ArrayNode)
    def visit(self, node: cil.ArrayNode):
        self.register_comment(f"ARRAY OF SIZE [{node.size}]")
        
        # $t0 = {node.size}, $t0 = value of the size, $t1 = 4, $t0 = $t0 * 4
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.size)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4"))
        self.register_instruction(mips.MultNode("$t0", "$t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        
        self.register_instantiation("$t0")
        # destino = new Array[size]
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        self.register_comment(f"{node.dest} STORE <- TYPEOF {node.source}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        self.register_comment(f"GO TO {node.address}")
        
        self.register_instruction(mips.JumpNode(node.address))

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        self.register_comment(f"IF {node.condition} IS TRUE -> GO TO {node.address}")
        
        # addr de la condicion
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.condition)}($sp)"))
        # cargando valor y comparandolo con 1
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "1"))
        self.register_instruction(mips.BeqNode("$t0", "$t1", node.address))

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        self.register_comment(f"STATIC FUNCT CALL {node.function}")
        
        self.register_instruction(mips.JumpAndLinkNode(node.function))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        
        # guardar funct en destino
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)"))
        
        # espacio para args
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}"))


    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        self.register_comment(f"DYNAMIC FUNCT CALL {node.method_address}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.method_address) + 4 * node.total_args + 4}($sp)"))
        self.register_instruction(mips.JumpAndLinkRegisterNode("$t0"))
        self.register_instruction(mips.LoadWordNode("$ra", f"{4 * node.total_args}($sp)"))
        
        # guardar funct en destino
        self.register_instruction(mips.StoreWordNode("$v1", f"{self.offset_of(node.dest) + 4 * node.total_args + 4}($sp)"))
        # espacio para args
        self.register_instruction(mips.AddiNode("$sp", "$sp", f"{4 * node.total_args + 4}"))
    

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        if node.arg_index == 0:
            self.register_comment("FUNCT ARGS")
            ## reservando espacio para los argumentos
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"-{4 * node.total_args + 4}"))
            ## funcion de retorno (espacio)
            self.register_instruction(mips.StoreWordNode("$ra", f"{4 * (node.total_args)}($sp)"))
            self.register_empty_instruction()
        
        # self.register_comment(f"Argument {node.name}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.name) +  4 * node.total_args + 4}($sp)"))
        # guardando el node.name
        self.register_instruction(mips.StoreWordNode("$t0", f"{4 * (node.total_args - node.arg_index - 1)}($sp)"))


    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        if node.value.isdigit():
            self.register_instruction(mips.AddiNode("$v1", "$zero", f"{node.value}"))
            return
        offset = self.offset_of(node.value)
        self.register_instruction(mips.LoadWordNode("$v1", f"{offset}($sp)"))


    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        self.register_comment(f"LENGHT: {node.dest} <- {node.str_address}")
        ###
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "4($t0)"))
        
        # borrando el tipo, tamaño y el null-term
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        
        self.register_instruction(mips.StoreWordNode("$t1", "8($t0)"))

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        pass

    @visitor.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode):
        pass

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        pass

    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        pass
    
    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        pass
    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        pass
    
    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        pass
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        pass
    
    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.PrintIntNode):
        pass
    
    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode):
        pass

    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode):
        pass
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode):
        pass
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        pass
    
    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        self.register_comment("EXIT")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "10"))
        self.register_instruction(mips.SystemCallNode())
    
    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        pass
    
    @visitor.when(cil.EmptyInstructionNode)
    def visit(self, node: cil.EmptyInstructionNode):
        pass
    
    
    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        label = mips.LabelNode(node.label)
        self.register_instruction(label)
    
class MipsFormatter:
    pass