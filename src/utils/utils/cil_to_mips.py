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
        
        ##
        for type_node in node.dottypes: 
            self.register_word(self.to_data_type("name_size", type_node.name), str(len(type_node.name)))
            self.register_asciiz(self.to_data_type("name", type_node.name), f'"{type_node.name}"')
            self.register_empty_data()
        
        #
        self.register_space("buffer_input", 1024)
        self.register_asciiz("debug_log", '"debug_log\\n"')

        for function_node in node.dotcode:
            self.visit(function_node)

        return mips.ProgramNode(self.dotdata, self.dottext)
    
    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        #por cada atributo y metodo reservo una palabra + 2
        size = 4 * (len(node.attributes) + len(node.methods) + 2)

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
        local_names = [x.name for x in self.current_function.localvars]
        ##
        ## self.current_function_stk = ["$ra"] + local_names
        self.current_function_stk = ["$ra"] + param_names + local_names

        locals_size = 4 * len(self.current_function.localvars)
        stack_size = 4 * len(self.current_function_stk)
        
        # if node.name != "main":
        #     self.register_comment("FUNCT PARAMS")
            
        #     for i, name in enumerate(param_names, start=2):
        #         self.register_comment(f"  {name} = {stack_size - (4 * i)}($sp)")
                
        #     self.register_comment(f"  $ra = {stack_size - 4}($sp)")
            
        if self.current_function.localvars:
            # Espacio para las variables locales
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{-locals_size}"))
            self.register_empty_instruction()

        for inst in node.instructions:
            try:
                if isinstance(inst, (cil.EmptyInstructionNode, cil.CommentNode)):
                    continue
                self.visit(inst)
                self.register_empty_instruction()
            except Exception as e:
                print('ERROR ' + str(e))

        if node.name != "main" and self.current_function.localvars:
            self.register_comment("FREE SPACE FOR LOCALVARS")
            self.register_instruction(mips.AddiNode("$sp", "$sp", f"{locals_size}"))
            self.register_empty_instruction()

        if node.name != "main":
            self.register_instruction(mips.JumpRegisterNode("$ra"))
        self.register_empty_instruction()
        

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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
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
        # self.register_empty_instruction()
        # $t0 = node.dest
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        # asignando el valor en la 3era word del objeto
        self.register_instruction(mips.StoreWordNode("$t2", "8($t0)"))
    
    
    @visitor.when(cil.EndOfLineNode) ######
    def visit(self, node: cil.EndOfLineNode):
        pass

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        node_id = hash(node)
        self.register_comment(f"Get attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)"))# direccion de la instancia
        self.register_instruction(mips.LoadWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)")) # el atributo de la instancia

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_get_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_get_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_get_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.JumpNode(f"end_get_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_get_attribute_{node_id}"))
        self.register_instruction(mips.StoreWordNode("$t1",f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.LabelNode(f"end_get_attribute_{node_id}"))


    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        node_id = hash(node)
        self.register_comment(f"Set attribute {node.attr} of {node.instance}")
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)")) # instancia $t0
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.source)}($sp)")) # fuente source $t1

        self.register_instruction(mips.BeqNode("$t1", "$zero", f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadWordNode("$t2", "0($t1)"))
        self.register_instruction(mips.LoadAddressNode("$t3", "type_Int"))
        self.register_instruction(mips.LoadAddressNode("$t4", "type_Bool"))
        self.register_instruction(mips.AddiNode("$t5", "$zero", "1"))
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t3"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"int_set_attribute_{node_id}"))        
        self.register_instruction(mips.SeqNode("$t6", "$t2", "$t4"))
        self.register_instruction(mips.BeqNode("$t6", "$t5", f"bool_set_attribute_{node_id}"))
        self.register_instruction(mips.JumpNode(f"object_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"int_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t3", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        
        # {node.instance}.{node.attr} = {node.source}
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"bool_set_attribute_{node_id}"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.StoreWordNode("$t4", "0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.LoadWordNode("$t5", "8($t1)"))
        self.register_instruction(mips.StoreWordNode("$t5", "8($v0)"))
        
        #{node.instance}.{node.attr} = {node.source}
        self.register_instruction(mips.StoreWordNode("$v0", f"{4 * (node.attr_index + 2)}($t0)"))
        self.register_instruction(mips.JumpNode(f"end_set_attribute_{node_id}"))

        self.register_instruction(mips.LabelNode(f"object_set_attribute_{node_id}"))
        
        #{node.instance}.{node.attr} = {node.source}
        self.register_instruction(mips.StoreWordNode("$t1", f"{4 * (node.attr_index + 2)}($t0)"))
        self.register_instruction(mips.LabelNode(f"end_set_attribute_{node_id}"))

    @visitor.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        # ARRAY instance[4 * index] = source
        self.register_comment(f"{node.dest} = ARRAY {node.instance}[{node.index}]")
        
        # $t0 = i, $t0 = array[i], $t1 = 4, $t0 = $t0 * 4
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4"))
        self.register_instruction(mips.MultNode("$t0", "$t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))
        
        # $t1 = instancia, moviendo el puntero al indice, $t1 = valor en la pos
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)"))
        
        # en el destino se fuarda el valor del array[i]
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        # ARRAY instance[4 * index] = source
        self.register_comment(f"ARRAY {node.instance}[{node.index}] = {node.source}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)")) # $t0 = index
        
        # $t0 = valor del index
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        # $t1 = 4, $t0 = $t0 * 4
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4"))
        self.register_instruction(mips.MultNode("$t0", "$t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        # $t1 = node.instance, moviendo el puntero al indice
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        # guardando la word
        self.register_instruction(mips.StoreWordNode("$t0", "0($t1)"))

    
    @visitor.when(cil.GetMethodNode)
    def visit(self, node: cil.GetMethodNode):
        self.register_comment(f"GET METHOD {node.method_name} OF {node.type}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "12"))
        
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.method_index)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SllNode("$t1", "$t1", "2"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t0)"))
        
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.SetMethodNode)
    def visit(self, node: cil.SetMethodNode):
        pass
    
    @visitor.when(cil.GetValueInIndexNode)
    def visit(self, node: cil.GetValueInIndexNode):
        self.register_comment(f"ARRAY {node.instance}[{node.index}]")
        
        # $t0 = i, $t0 = array[i], $t1 = 4, $t0 = $t0 * 4
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.index)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", "8($t0)"))
        self.register_instruction(mips.AddiNode("$t1", "$zero", "4"))
        self.register_instruction(mips.MultNode("$t0", "$t1"))
        self.register_instruction(mips.MoveFromLowNode("$t0"))

        # $t1 = instancia, moviendo el puntero al indice, $t1 = valor en la pos
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.instance)}($sp)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "$t0"))
        self.register_instruction(mips.LoadWordNode("$t0", "0($t1)"))
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.dest)}($sp)"))
        
        self.register_instruction(mips.StoreWordNode("$t0", "8($t2)"))

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
        self.register_comment(f"ALLOCATE INT")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())

        # $t0 = tipo de direccion
        self.register_instruction(mips.LoadAddressNode("$t0", "type_Int"))
        # ajustando tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)"))
        # tamaño en la 2da word
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        # guardando el valoren la 3era word
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)"))
        # dest = dir del int allocado
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))


    @visitor.when(cil.AllocateBoolNode)
    def visit(self, node: cil.AllocateBoolNode):
        self.register_comment(f"ALLOCATE BOOL {node.value}")

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "12"))
        self.register_instruction(mips.SystemCallNode())
        
        # $t0 = tipo de direccion
        self.register_instruction(mips.LoadAddressNode("$t0", "type_Bool"))
        # ajustando tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", "0($v0)"))
        # tamaño en la 2da word
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)"))
        self.register_instruction(mips.AddiNode("$t0", "$zero", node.value))
        # guardando el valoren la 3era word
        self.register_instruction(mips.StoreWordNode("$t0", "8($v0)"))

        # dest = dir del int allocado
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.AllocateStringNode)
    def visit(self, node: cil.AllocateStringNode):
        self.register_comment(f"ALLOCATING STRING")
        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        
        # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
        self.register_instruction(mips.AddiNode("$a0", "$zero", f"{9 + node.length}"))
        self.register_instruction(mips.SystemCallNode())
        
        ####
        self.register_instruction(mips.LoadAddressNode("$t0", "type_String"))
        # tipo en la 1era word
        self.register_instruction(mips.StoreWordNode("$t0", f"0($v0)"))

        self.register_instruction(mips.AddiNode("$t0", "$zero", f"{9 + node.length}"))
        # len en la 2da word
        self.register_instruction(mips.StoreWordNode("$t0", f"4($v0)"))

        for i, c in enumerate(node.string):
            ec = c.replace('\n', '\\n').replace('\t', '\\t').replace('\b', '\\b').replace('\f', '\\f')
            self.register_instruction(mips.AddiNode("$t0", "$zero",  f"{ord(c)}"))
            self.register_instruction(mips.StoreByteNode("$t0", f"{i + 8}($v0)"))

        # null-term al final del str
        self.register_instruction(mips.StoreByteNode("$zero", f"{node.length + 8}($v0)"))
        # dest = valor
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))
 
    
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
        self.register_comment(f"DYNAMIC FUNCT CALL {node.method_addr}")
        
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
        self.register_comment(f"{node.dest} = CONCAT ({node.str1}, {node.str2})")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str1)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.str2)}($sp)"))
        # $t2 lenght de str1, $t3 lenght de str2
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)"))
        self.register_instruction(mips.LoadWordNode("$t3", "4($t1)"))
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))
        
        # length del la cadena concatenada
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "9"))

        self.register_instruction(mips.LoadInmediateNode("$v0", "9"))
        self.register_instruction(mips.MoveNode("$a0", "$t4"))
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.AddiNode("$t4", "$t4", "-9"))
        self.register_instruction(mips.AddNode("$t5", "$zero", "$v0"))
        self.register_instruction(mips.AddiNode("$t5", "$t5", "8"))
        
        self.register_instruction(mips.LoadAddressNode("$t8", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t8", f"0($v0)"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)"))

        # copiando s1 para el string nuevo
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6")) # $t6 c
        self.register_instruction(mips.LabelNode("while_copy_str1_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t2", "while_copy_str1_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t0", "$t0", "1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1"))
        self.register_instruction(mips.JumpNode("while_copy_str1_start"))
        self.register_instruction(mips.LabelNode("while_copy_str1_end"))

        # copiando s2 para el string nuevo
        self.register_instruction(mips.LabelNode("while_copy_str2_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t4", "while_copy_str2_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"8($t1)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddNode("$t1", "$t1", "1"))
        self.register_instruction(mips.AddNode("$t5", "$t5", "1"))
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1"))
        self.register_instruction(mips.JumpNode("while_copy_str2_start"))
        self.register_instruction(mips.LabelNode("while_copy_str2_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)"))
        self.register_empty_instruction()

        # valor de retorno
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))



    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        self.register_comment(f"{node.dest} <- {node.str_address}[{node.start}:{node.start} + {node.length}]")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_address)}($sp)")) # $t0 str dir
        self.register_instruction(mips.LoadWordNode("$t1", f"4($t0)")) # $t1 str tamaño
        self.register_instruction(mips.AddiNode("$t1", "$t1", "-9")) # $t1 str tamaño + 9
        self.register_instruction(mips.LoadWordNode("$t2", f"{self.offset_of(node.start)}($sp)")) # $t2 str init
        self.register_instruction(mips.LoadWordNode("$t2", "8($t2)"))
        self.register_instruction(mips.LoadWordNode("$t3", f"{self.offset_of(node.length)}($sp)")) # $t3 str tamaño
        self.register_instruction(mips.LoadWordNode("$t3", "8($t3)"))
        self.register_instruction(mips.AddNode("$t4", "$t2", "$t3")) # $t4 str init + tamaño de str

        self.register_empty_instruction()
        self.register_instruction(mips.BgtNode("$t4", "$t1", "substring_out_of_bounds"))
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$t3", "9"))
        self.register_instantiation("$t3")
        self.register_instruction(mips.AddiNode("$t3", "$t3", "-9"))

        self.register_empty_instruction()
        self.register_instruction(mips.LoadAddressNode("$t5", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t5", f"0($v0)")) # tipo en la primera word
        #
        
        self.register_empty_instruction()
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)")) # tamaño en la 2da word
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8")) #1er byte ddel str
        self.register_instruction(mips.AddNode("$t0", "$t0", "$t2")) #1er byte ddel substr
        self.register_instruction(mips.MoveNode("$t5", "$v0")) # new str dir
        self.register_instruction(mips.AddNode("$t5", "$t5", "8")) #1er byte ddel str
        self.register_instruction(mips.XorNode("$t6", "$t6", "$t6")) # counter
        self.register_instruction(mips.LabelNode("while_copy_substr_start"))
        self.register_instruction(mips.BeqNode("$t6", "$t3", "while_copy_substr_end"))
        self.register_instruction(mips.LoadByteNode("$t7", f"0($t0)"))
        self.register_instruction(mips.StoreByteNode("$t7", f"0($t5)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1")) # str addr ++
        self.register_instruction(mips.AddNode("$t5", "$t5", "1")) # new str addr ++
        self.register_instruction(mips.AddiNode("$t6", "$t6", "1")) # counter ++
        self.register_instruction(mips.JumpNode("while_copy_substr_start"))
        self.register_instruction(mips.LabelNode("while_copy_substr_end"))

        self.register_empty_instruction()
        self.register_instruction(mips.StoreByteNode("$zero", f"0($t5)")) # asignando el null del final
        
        self.register_empty_instruction()
        # {node.dest} = {node.str_address}[{node.start}:{node.start} + {node.length}]
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

        self.register_instruction(mips.JumpNode("substring_not_out_of_bounds"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_out_of_bounds"))
        # TODO: Throw an exception
        self.register_instruction(mips.LoadInmediateNode("$v0", "17"))
        self.register_instruction(mips.AddiNode("$a0", "$zero", "1"))
        self.register_instruction(mips.SystemCallNode())

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("substring_not_out_of_bounds"))


    @visitor.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        pass

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        pass
    
    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "8"))
        self.register_instruction(mips.LoadAddressNode("$a0", "buffer_input"))
        self.register_instruction(mips.LoadInmediateNode("$a1", "1024"))
        self.register_instruction(mips.SystemCallNode())

        self.register_instruction(mips.XorNode("$t0", "$t0", "$t0"))
        self.register_instruction(mips.LabelNode("while_read_start"))
        self.register_instruction(mips.LoadByteNode("$t1", "buffer_input($t0)"))
        
        # 
        
        self.register_instruction(mips.AddiNode("$t2", "$zero", "10"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t2", "$zero", "13"))
        self.register_instruction(mips.BeqNode("$t1", "$t2", "while_read_end"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1")) # ++
        self.register_instruction(mips.JumpNode("while_read_start"))
        self.register_instruction(mips.LabelNode("while_read_end"))

        # self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        # self.register_instruction(mips.MoveNode("$a0", "$t0"))
        # self.register_instruction(mips.SystemCallNode())
        #
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t0", "$t0", "9")) # espacio para sixe, tipo y null-term
        self.register_instantiation("$t0")
        self.register_instruction(mips.AddiNode("$t0", "$t0", "-9"))
        self.register_instruction(mips.LoadAddressNode("$t2", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t2", "0($v0)")) # tipo en la 1era word    
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)")) # len en la 2da
        
        self.register_empty_instruction()
        self.register_instruction(mips.AddiNode("$t3", "$v0", "8"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4"))
        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t0", "while_copy_from_buffer_end"))
        
        # cargando el byte
        self.register_instruction(mips.LoadByteNode("$t5", "buffer_input($t4)")) 
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1")) # ptr ++
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1")) # counter ++
        self.register_instruction(mips.JumpNode("while_copy_from_buffer_start"))
        self.register_instruction(mips.LabelNode("while_copy_from_buffer_end"))
        self.register_empty_instruction()
        
        self.register_instruction(mips.StoreByteNode("$zero", "0($t3)")) # guardando null 
        self.register_empty_instruction()
        
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        self.register_instruction(mips.LoadInmediateNode("$v0", "5"))
        
        self.register_instruction(mips.SystemCallNode())
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        
        self.register_instruction(mips.StoreWordNode("$v0", "8($t0)"))
    
    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        pass
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        self.register_comment(f"PRINT INT")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "1"))
        self.register_instruction(mips.LoadWordNode("$a0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$a0", "8($a0)"))
        
        self.register_instruction(mips.SystemCallNode())
        
    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        # $t0 = node.str_addr
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.str_addr)}($sp)"))
        # ptr al primer caracter en la cadena
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8"))

        self.register_comment(f"PRINT STRING -> {node.str_addr}")
        self.register_instruction(mips.LoadInmediateNode("$v0", "4"))
        self.register_instruction(mips.MoveNode("$a0", "$t0"))
        
        self.register_instruction(mips.SystemCallNode())

    
    @visitor.when(cil.TypeAddressNode)
    def visit(self, node: cil.TypeAddressNode):
        self.register_comment(f"{node.dest} <- DIRECTION OF ({node.name})")
        
        self.register_instruction(mips.LoadAddressNode("$t0", f"type_{node.name}"))
        self.register_instruction(mips.StoreWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
    
    @visitor.when(cil.EqualAddressNode)
    def visit(self, node: cil.EqualAddressNode):
        self.register_comment(f"{node.dest} <-- EQUAL ADDRESS({node.left}, {node.right})")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))

    @visitor.when(cil.EqualIntNode)
    def visit(self, node: cil.EqualIntNode):
        self.register_comment(f"{node.dest} <-- EQUAL INT ({node.left}, {node.right})")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t0", f"8($t0)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"8($t1)"))
        self.register_instruction(mips.SeqNode("$t2", "$t0", "$t1"))
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t2", f"8($t0)"))
    
    @visitor.when(cil.EqualStrNode)
    def visit(self, node: cil.EqualStrNode):
        self.register_comment(f"{node.dest} <-- EQUAL STRING ({node.left}, {node.right})")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.left)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", f"{self.offset_of(node.right)}($sp)"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "8"))

        self.register_empty_instruction()
        
        # se asume que son iguales por defecto
        self.register_instruction(mips.AddiNode("$t4", "$zero", "1"))
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$t4", f"8($t5)"))

        self.register_empty_instruction()
        self.register_instruction(mips.LabelNode("while_compare_strings_start"))
        self.register_instruction(mips.LoadByteNode("$t2", "0($t0)"))
        self.register_instruction(mips.LoadByteNode("$t3", "0($t1)"))

        self.register_instruction(mips.BeqNode("$t2", "$t3", "while_compare_strings_update"))
        
        self.register_empty_instruction()
        
        # si no son iguales: 
        self.register_instruction(mips.LoadWordNode("$t5", f"{self.offset_of(node.dest)}($sp)"))
        self.register_instruction(mips.StoreWordNode("$zero", f"8($t5)"))
        self.register_instruction(mips.JumpNode("while_compare_strings_end"))
        
        self.register_instruction(mips.LabelNode("while_compare_strings_update"))
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1"))
        self.register_instruction(mips.AddiNode("$t1", "$t1", "1"))
        self.register_instruction(mips.BeqNode("$t2", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.BeqNode("$t3", "$zero", "while_compare_strings_end"))
        self.register_instruction(mips.JumpNode("while_compare_strings_start"))
        self.register_instruction(mips.LabelNode("while_compare_strings_end"))
    
    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        self.register_comment(f"{node.dest} <- NAME {node.source}")
        
        # $t0, $t1, $t2 = source, type, lenght
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)"))
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)"))
        self.register_instruction(mips.LoadWordNode("$t2", "8($t1)"))
        
        # $t3, $t2 = direc name, length name
        self.register_instruction(mips.LoadAddressNode("$t3", "4($t2)"))
        self.register_instruction(mips.LoadWordNode("$t2", "0($t2)"))

        # $t2 teniendo espacio para el tipo 
        self.register_instruction(mips.AddiNode("$t2", "$t2", "9"))
        self.register_instantiation("$t2")
        # $t2 reintegrando espacio 
        self.register_instruction(mips.AddiNode("$t2", "$t2", "-9"))

        # asignando la primera palabra y la 2da para tipo y espacio
        self.register_instruction(mips.LoadAddressNode("$t4", "type_String"))
        self.register_instruction(mips.StoreWordNode("$t4", f"0($v0)"))
        self.register_instruction(mips.StoreWordNode("$a0", f"4($v0)"))

        self.register_instruction(mips.AddiNode("$t4", "$v0", 0)) # $t4 direccion del nievo str
        self.register_instruction(mips.AddiNode("$t4", "$t4", "8")) #puntero al promer char del string
        self.register_instruction(mips.XorNode("$t5", "$t5", "$t5")) # counter para el string
        self.register_instruction(mips.LabelNode("while_copy_name_start"))
        self.register_instruction(mips.BeqNode("$t5", "$t2", "while_copy_name_end"))
        self.register_instruction(mips.LoadByteNode("$t6", "0($t3)")) # cargando el char
        self.register_instruction(mips.StoreByteNode("$t6", "0($t4)"))
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1")) # ++
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1")) # ++ para el punter en node.source
        self.register_instruction(mips.AddiNode("$t5", "$t5", "1")) # ++
        # jmp pal while
        self.register_instruction(mips.JumpNode("while_copy_name_start"))
        self.register_instruction(mips.LabelNode("while_copy_name_end"))
        self.register_empty_instruction()

        self.register_instruction(mips.StoreByteNode("$zero", "0($t4)")) # poniendo el null
        self.register_empty_instruction()

        # guardando el str nuevo
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.HaltNode)
    def visit(self, node: cil.HaltNode):
        self.register_comment("EXIT")
        
        self.register_instruction(mips.LoadInmediateNode("$v0", "10"))
        self.register_instruction(mips.SystemCallNode())
    
    @visitor.when(cil.CopyNode)
    def visit(self, node: cil.CopyNode):
        self.register_comment(f"COPY {node.source} INTO {node.dest}")
        
        self.register_instruction(mips.LoadWordNode("$t0", f"{self.offset_of(node.source)}($sp)")) # $t0 source
        self.register_instruction(mips.LoadWordNode("$t1", "0($t0)")) # $t1 tipo de sourvce
        self.register_instruction(mips.LoadWordNode("$t2", "4($t0)")) #$t2 length
        
        self.register_instantiation("$t2")
        self.register_instruction(mips.MoveNode("$t3", "$v0")) # direccion del nuevo objeto
        self.register_instruction(mips.StoreWordNode("$t1", "0($v0)")) # asignandole el tipo (primera word)
        self.register_instruction(mips.StoreWordNode("$a0", "4($v0)")) # asignandole el tamaño (segunda word)
       
        self.register_empty_instruction()

        ##
        # incializando variables para el loop 
        ##
        self.register_instruction(mips.AddiNode("$t0", "$t0", "8"))
        self.register_instruction(mips.AddiNode("$t3", "$t3", "8"))
        self.register_instruction(mips.AddiNode("$t2", "$2", "-8"))
        self.register_instruction(mips.XorNode("$t4", "$t4", "$t4"))
        self.register_empty_instruction()

        # copiando el objeto
        self.register_instruction(mips.LabelNode("while_copy_start"))
        self.register_instruction(mips.BeqNode("$t4", "$t2", "while_copy_end"))
        self.register_instruction(mips.LoadByteNode("$t5", "0($t0)"))
        self.register_instruction(mips.StoreByteNode("$t5", "0($t3)"))
        
        self.register_instruction(mips.AddiNode("$t0", "$t0", "1")) # ++
        self.register_instruction(mips.AddiNode("$t3", "$t3", "1")) # ++ del nuevo obj
        self.register_instruction(mips.AddiNode("$t4", "$t4", "1")) # ++
        
        self.register_instruction(mips.JumpNode("while_copy_start"))
        self.register_instruction(mips.LabelNode("while_copy_end"))

        # guandando el nuevo objeto en el destino deseado
        self.register_instruction(mips.StoreWordNode("$v0", f"{self.offset_of(node.dest)}($sp)"))

    
    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        label = mips.LabelNode(node.label)
        self.register_instruction(label)
    
    
class MipsFormatter:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        dotdata = "\n\t".join([self.visit(data) for data in node.dotdata])

        # recorriendo el dottext
        inst = []
        for item in node.dottext:
            if isinstance(item, mips.LabelNode) and (item.name.startswith("function_") or item.name == "main"):
                inst.append(f"{self.visit(item)}")
            else:
                inst.append(f"\t{self.visit(item)}")
        
        dottext = "\n\t".join(inst)

        return dotdata, dottext

    @visitor.when(mips.DataNode)
    def visit(self, node: mips.DataNode):
        return f"{node.name}: {node.data_type} {node.value}"

    @visitor.when(mips.OneAddressNode)
    def visit(self, node: mips.OneAddressNode):
        return f"{node.code} {node.dest}"

    @visitor.when(mips.TwoAddressNode)
    def visit(self, node: mips.TwoAddressNode):
        return f"{node.code} {node.dest}, {node.source}"
        

    @visitor.when(mips.ThreeAddressNode)
    def visit(self, node: mips.ThreeAddressNode):
        return f"{node.code} {node.dest}, {node.source1}, {node.source2}"

    @visitor.when(mips.SystemCallNode)
    def visit(self, node: mips.SystemCallNode):
        return node.code
    
    @visitor.when(mips.LabelNode)
    def visit(self, node: mips.LabelNode):
        return f"{node.name}:"

    @visitor.when(mips.CommentNode)
    def visit(self, node: mips.CommentNode):
        return f"# {node.comment}"

    @visitor.when(mips.EmptyInstructionNode)
    def visit(self, node: mips.EmptyInstructionNode):
        return ""

    @visitor.when(mips.EmptyDataNode)
    def visit(self, node: mips.EmptyDataNode):
        return ""
