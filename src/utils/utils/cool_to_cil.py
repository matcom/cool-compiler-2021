# from atexit import register
# from pickle import TRUE
# from turtle import right
from .semantic import *
from . import ast_nodes_cil as cil
from . import ast_nodes as cool
from . import visitor
from typing import Optional
from .code_generation import NullNode, NullType

def methods_declaration_order(t: Type):
    method_decl = []
    all_methods = t.all_methods()
    visited = set()
    for method, _ in all_methods:
        if method.name in visited or method.name == 'get_type':
            continue
        
        meths = list(all_methods)[::-1]
        method_decl.append(
            [(x, y) for x, y in meths if x.name == method.name][0]
        )
        visited.add(method.name)
    return method_decl

class BaseCOOLToCILVisitor:
    def __init__(self, context,dict_attr,dict_method):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type: Optional[Type] = None
        self.current_method: Optional[cil.DataNode] = None
        self.current_function: Optional[cil.FunctionNode] = None
        
        self.context: Context = context
        
        self.dict_attr = dict_attr
        self.dict_method = dict_method
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo):
        local_name = (f"local_{self.current_function.name[9:]}_{vinfo}_{len(self.localvars)}")
        local_name = vinfo
        local_node = cil.LocalNode(local_name)
        self.localvars.append(local_node)
        return local_name

    def define_internal_local(self):
        # vinfo = VariableInfo('internal', None)
        return self.register_local(f"internal_{len(self.localvars)}")

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name, parent):
        type_node = cil.TypeNode(name, parent)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_comment(self, comm):
        self.register_instruction(cil.CommentNode(comm))

    def register_EOL(self):
        self.register_instruction(cil.EndOfLineNode())

    def add_basic_types(self):
        default_class_names = ["Object", "IO", "String", "Int", "Bool"]
        for name in default_class_names:
            current_type = self.context.get_type(name)
            self.current_type = current_type
            cil_type_node = self.register_type(current_type.name, current_type.parent.name if current_type.parent is not None else None)

            for method, ancestor in methods_declaration_order(current_type):
                if method.name == 'get_type': continue
                cil_type_node.methods.append((method.name, self.to_function_name(method.name, ancestor.name)))
        1
           
    def add_arith_methods(self):
        ### ADD FUNCTION ###
        self.current_function = self.register_function('add_funct')
        self.register_comment("ADD FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.PlusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()
        
        ### MINUS FUNCTION ###
        self.current_function = self.register_function('minus_funct')
        self.register_comment("MINUS FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.MinusNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()
        
        ### TIMES FUNCTION ###
        self.current_function = self.register_function('times_funct')
        self.register_comment("TIMES FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.StarNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()

        ### DIV FUNCTION ###
        self.current_function = self.register_function('div_funct')
        self.register_comment("DIV FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.DivNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()
        
        ### LESS THAN FUNCTION ###
        self.current_function = self.register_function('lessthan_funct')
        self.register_comment("LESS THAN FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessThanNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()
        
        ### LESS EQUAL FUNCTION ###
        self.current_function = self.register_function('lesseq_funct')
        self.register_comment("LESS EQUAL FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.LessEqualNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result))
        self.register_EOL()
        
        ### XOR FUNCTION ###
        self.current_function = self.register_function('xor_funct')
        self.register_comment("XOR FUNCTION")
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        self.register_instruction(cil.XorNode(result, "a", "b"))
        self.register_instruction(cil.ReturnNode(result)) 
        self.register_EOL()
    
    def add_function_equal(self):
        self.current_function = self.register_function("equal_funct")
        self.register_comment('EQUAL FUNCTION')
        self.current_function.params.append(cil.ParamNode("a"))
        self.current_function.params.append(cil.ParamNode("b"))
        result = self.define_internal_local()
        constant_null = self.define_internal_local()
        is_null = self.define_internal_local()
        type_of_a = self.define_internal_local()
        type_int = self.define_internal_local()
        type_bool = self.define_internal_local()
        type_string = self.define_internal_local()
        type_a_equals_int = self.define_internal_local()
        type_a_equals_bool = self.define_internal_local()
        type_a_equals_string = self.define_internal_local()
        self.register_EOL()
        
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.AllocateNullNode(constant_null))
        self.register_instruction(cil.AllocateBoolNode(is_null, "0"))
        
        self.register_instruction(cil.EqualAddressNode(is_null, "a", constant_null))
        self.register_instruction(cil.EqualAddressNode(is_null, "b", constant_null))
        self.register_instruction(cil.GotoIfNode(is_null, "a_is_type_object"))

        self.register_instruction(cil.TypeOfNode(type_of_a, "a"))
        self.register_instruction(cil.TypeAddressNode(type_int, "Int"))
        self.register_instruction(cil.TypeAddressNode(type_bool, "Bool"))
        self.register_instruction(cil.TypeAddressNode(type_string, "String"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_bool, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_a_equals_string, "0"))

        self.register_instruction(cil.EqualAddressNode(type_a_equals_int, type_of_a, type_int))
        self.register_instruction(cil.EqualAddressNode(type_a_equals_bool, type_of_a, type_bool))
        self.register_instruction(cil.EqualAddressNode(type_a_equals_string, type_of_a, type_string))
        self.register_EOL()
        self.register_instruction(cil.GotoIfNode(type_a_equals_int, "a_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_a_equals_bool, "a_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_a_equals_string, "a_is_type_string"))       
        self.register_instruction(cil.GotoNode("a_is_type_object"))
        
        self.register_EOL()
        self.register_instruction(cil.LabelNode("a_is_type_int_or_bool"))
        self.register_instruction(cil.EqualIntNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))

        self.register_EOL()
        self.register_instruction(cil.LabelNode("a_is_type_string"))
        self.register_instruction(cil.EqualStrNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))

        self.register_EOL()
        self.register_instruction(cil.LabelNode("a_is_type_object"))
        self.register_instruction(cil.EqualNode(result, "a", "b"))
        self.register_instruction(cil.GotoNode("end_of_equal"))
        
        self.register_EOL()
        self.register_instruction(cil.LabelNode("end_of_equal"))

        self.register_instruction(cil.ReturnNode(result))

    def add_function_assign(self): 
        self.current_function = self.register_function("assign_funct")
        self.register_comment('ASSIGN FUNCTION')
        self.current_function.params.append(cil.ParamNode("dest"))
        self.current_function.params.append(cil.ParamNode("source"))
        
        null_ptr = self.define_internal_local()
        is_null = self.define_internal_local()
        type_source = self.define_internal_local()
        type_int = self.define_internal_local()
        type_bool = self.define_internal_local()
        type_source_equals_int = self.define_internal_local()
        type_source_equals_bool = self.define_internal_local()
        self.register_EOL()
       
        ## null ptr
        self.register_instruction(cil.AllocateNullNode(null_ptr))
        self.register_instruction(cil.AllocateBoolNode(is_null, "0"))
        self.register_instruction(cil.EqualAddressNode(is_null, "source", null_ptr))
        self.register_instruction(cil.EqualAddressNode(is_null, "dest", null_ptr))
        self.register_instruction(cil.GotoIfNode(is_null))

        # types
        self.register_instruction(cil.TypeOfNode(type_source, "source"))
        self.register_instruction(cil.TypeAddressNode(type_int, "Int"))
        self.register_instruction(cil.TypeAddressNode(type_bool, "Bool"))
        self.register_instruction(cil.AllocateBoolNode(type_source_equals_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(type_source_equals_bool, "0"))
        self.register_instruction(cil.EqualAddressNode(type_source_equals_int, type_source, type_int))
        self.register_instruction(cil.EqualAddressNode(type_source_equals_bool, type_source, type_bool))
        self.register_EOL()
        
        self.register_instruction(cil.GotoIfNode(type_source_equals_int, "source_is_type_int_or_bool"))
        self.register_instruction(cil.GotoIfNode(type_source_equals_bool, "source_is_type_int_or_bool"))
        self.register_instruction(cil.GotoNode("source_is_type_object"))

        self.register_EOL()
        self.register_instruction(cil.LabelNode("source_is_type_int_or_bool"))

        self.register_instruction(cil.AssignIntNode("dest", "source"))
        self.register_instruction(cil.GotoNode("source_end_of_equal"))

        self.register_EOL()
        self.register_instruction(cil.LabelNode("source_is_type_object"))
        self.register_instruction(cil.AssignNode("dest", "source"))
        self.register_instruction(cil.GotoNode("source_end_of_equal"))
        
        self.register_EOL()
        self.register_instruction(cil.LabelNode("source_end_of_equal"))
        self.register_instruction(cil.ReturnNode("dest"))
        self.register_EOL()        
        
    def add_function_init(self, type_name: str):
        self.current_function = self.register_function(self.to_function_name("_init_", type_name))
        self.current_function.params.append(cil.ParamNode("self"))
        self.register_instruction(cil.ReturnNode("self")) 
        self.register_EOL()   
    
    def add_function_abort(self):
        self.current_function = self.register_function(self.to_function_name("abort", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        msg1 = self.define_internal_local()
        msg2 = self.define_internal_local()
        msg = self.define_internal_local()
        endl = self.define_internal_local()
        method_index = self.define_internal_local()
        method_address = self.define_internal_local()
        self.register_EOL()
        
        self.register_instruction(cil.AllocateStringNode(msg1, "\"Abort called from class \""))
        self.register_instruction(cil.AllocateStringNode(endl, "\"\\n\""))
        
        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("type_name")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "type_name", "String"))

        self.register_instruction(cil.ArgNode("self", 0, 1))
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg2, 1))
       
        
        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("concat")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "concat", "String"))

        self.register_instruction(cil.ArgNode(msg1, 0, 2))
        self.register_instruction(cil.ArgNode(msg2, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg, 2))

        all_methods = methods_declaration_order(self.context.get_type("String"))
        i = [m.name for m, _ in all_methods].index("concat")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, "self", method_index, "concat", "String"))

        self.register_instruction(cil.ArgNode(msg, 0, 2))
        self.register_instruction(cil.ArgNode(endl, 1, 2)) 
        self.register_instruction(cil.DynamicCallNode("String", method_address, msg, 2))

        self.register_instruction(cil.PrintStringNode(msg))
        self.register_instruction(cil.HaltNode())
        self.register_instruction(cil.ReturnNode("self"))

    def add_function_copy(self):
        self.current_function = self.register_function(self.to_function_name("copy", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_copy = self.define_internal_local()
        self.register_instruction(cil.CopyNode(local_copy, "self"))
        self.register_instruction(cil.ReturnNode(local_copy))
        self.register_EOL()

    def add_function_type_name(self):
        self.current_function = self.register_function(self.to_function_name("type_name", "Object"))
        self.current_function.params.append(cil.ParamNode("self"))
        #type_name
        type_name = self.define_internal_local()
        self.register_instruction(cil.TypeNameNode(type_name, "self"))
        self.register_instruction(cil.ReturnNode(type_name))
        self.register_EOL()


    def add_function_out_string(self):
        self.current_function = self.register_function(self.to_function_name("out_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintStringNode("x"))
        self.register_instruction(cil.ReturnNode("self"))
        self.register_EOL()

    def add_function_out_int(self):
        self.current_function = self.register_function(self.to_function_name("out_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("x"))
        self.register_instruction(cil.PrintIntNode("x"))
        self.register_instruction(cil.ReturnNode("self"))
        self.register_EOL()
    
    def add_function_in_string(self):
        self.current_function = self.register_function(self.to_function_name("in_string", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.ReadStringNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))
        self.register_EOL()
    
    def add_function_in_int(self):
        self.current_function = self.register_function(self.to_function_name("in_int", "IO"))
        self.current_function.params.append(cil.ParamNode("self"))
        local_str = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(local_str, "0"))
        self.register_instruction(cil.ReadIntNode(local_str))
        self.register_instruction(cil.ReturnNode(local_str))
        self.register_EOL()

    def add_function_length(self):
        self.current_function = self.register_function(self.to_function_name("length", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        len_local =  self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(len_local, "0"))
        self.register_instruction(cil.LengthNode(len_local, "self"))
        self.register_instruction(cil.ReturnNode(len_local))
        self.register_EOL()

    def add_function_concat(self):
        self.current_function = self.register_function(self.to_function_name("concat", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("s"))
        new_str =  self.define_internal_local()
        self.register_instruction(cil.ConcatNode(new_str, "self", "s"))
        self.register_instruction(cil.ReturnNode(new_str))
        self.register_EOL()

    def add_function_substr(self):
        self.current_function = self.register_function(self.to_function_name("substr", "String"))
        self.current_function.params.append(cil.ParamNode("self"))
        self.current_function.params.append(cil.ParamNode("i"))
        self.current_function.params.append(cil.ParamNode("l"))
        substr =  self.define_internal_local()
        self.register_instruction(cil.SubstringNode(substr, "self", "i", "l"))            
        self.register_instruction(cil.ReturnNode(substr))
        self.register_EOL()


        
    def add_basic_methods(self):
        # +, -, *, /, xor
        self.add_arith_methods()
        
        ## initializing main types
        self.add_function_init("Object")
        self.add_function_abort()
        self.add_function_type_name()
        self.add_function_copy()

        self.add_function_init("IO")
        self.add_function_out_string()
        self.add_function_out_int()
        self.add_function_in_string()
        self.add_function_in_int()
        
        self.add_function_init("String")
        self.add_function_length()
        self.add_function_concat()
        self.add_function_substr()
        
        self.add_function_init("Bool")
        self.add_function_init("Int")
        
            
    def add_main_funct(self): 
        self.current_function = self.register_function("main")
        local_main = self.define_internal_local()
        local_result = self.define_internal_local()
        method_index = self.define_internal_local()
        method_address = self.define_internal_local()

        self.register_instruction(cil.AllocateNode("Main", local_main))
        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.StaticCallNode(self.to_function_name("_init_", "Main"), local_main, 1))
        self.register_EOL()

        all_methods = methods_declaration_order(self.context.get_type("Main"))
        i = [m.name for m, _ in all_methods].index("main")
        self.register_instruction(cil.AllocateIntNode(method_index, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, local_main, method_index, "main", "Main"))

        self.register_instruction(cil.ArgNode(local_main, 0, 1))
        self.register_instruction(cil.DynamicCallNode("Main", method_address, local_result, 1))
        self.register_EOL()
        
        self.register_instruction(cil.HaltNode())

    def visit_arith_node(self, node: cool.BinaryNode, scope: Scope, operation_function: str, return_type_name: str = "Int"):
        left, _ = self.visit(node.left, scope)
        right, _ = self.visit(node.right, scope)
        dest = self.define_internal_local()
        self.register_EOL()
        self.register_instruction(cil.ArgNode(left, 0, 2))
        self.register_instruction(cil.ArgNode(right, 1, 2))
        self.register_instruction(cil.StaticCallNode(operation_function, dest, 2))
        return dest, self.context.get_type(return_type_name)
 

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    # MAIN FLOW almost done
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope):
        scope = node.scope
        
        self.add_basic_types()    
        self.add_basic_methods()  
        # self.add_main_funct()
        
        for i, class_ in enumerate(node.class_list):
            self.visit(class_, scope.children[i])

        self.add_main_funct()

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
            
    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope):
        scope = node.scope
        self.current_type = self.context.get_type(node.name)

        type_node = self.register_type(self.current_type.name, self.current_type.parent.name)

        attrs = [data_ for data_ in node.data if isinstance(data_, cool.AttributeDecNode)]
        meths = [data_ for data_ in node.data if isinstance(data_, cool.MethodDecNode)]

        for attr, _ in self.current_type.all_attributes():
            self.visit(attr, scope)
            type_node.attributes.append(attr.name)

        for method, t in methods_declaration_order(self.current_type):
            type_node.methods.append((method.name, self.to_function_name(method.name, t.name)))

        i_ = len([attr for attr in attrs if attr.expr is not None])
        for i, method in enumerate(meths, start=i_):
            self.visit(method, scope.children[i])
                
    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope):
        scope = node.scope
        self.current_method, owner_type = self.current_type.get_method(node.name, owner=True)
        function_name = self.to_function_name(self.current_method.name, owner_type.name)
        self.current_function = self.register_function(function_name)
        1 #forcing breakpoint
        self.current_function.params = [cil.ParamNode("self")] + [cil.ParamNode(item.name) for item in node.params]

        source, _ = self.visit(node.expr, scope)

        self.register_instruction(cil.ReturnNode(source))

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope):
        scope = node.scope
        pass


    ###############
    # EXPRESSIONS #
    ###############

    @visitor.when(cool.ParamNode)
    def visit(self, node: cool.ParamNode, scope):
        scope = node.scope
        # case solved
        pass

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope):
        scope = node.scope
        node_id = hash(node)
        result_addres = self.define_internal_local()
        
        #self.register_EOL()
        self.register_comment(f"while")

        self.register_instruction(cil.AllocateNullNode(result_addres))
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))

        conditional_source, _ = self.visit(node.cond, scope)
        self.register_instruction(cil.GotoIfNode(conditional_source, f"while_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"while_end_{node_id}"))

        self.register_instruction(cil.EmptyInstructionNode())
        self.register_instruction(cil.LabelNode(f"while_body_{node_id}"))
        self.visit(node.data, scope)
        self.register_instruction(cil.GotoNode(f"while_start_{node_id}"))

        self.register_instruction(cil.EmptyInstructionNode())
        self.register_instruction(cil.LabelNode(f"while_end_{node_id}"))

        return result_addres, self.context.get_type("Object")
    
    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope):
        scope = node.scope
        return self.visit(node.expr, scope)
    
    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope):
        scope = node.scope
        source, inst_type = None, None
        
        for expr in node.expr:
            source, inst_type = self.visit(expr, scope)
            
        return source, inst_type
    
    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope):
        scope = node.scope
        self.register_instruction(cil.CommentNode("cond"))

        node_id = hash(node)
        result_address = self.define_internal_local()
        conditional_address = self.define_internal_local()

        self.register_instruction(cil.AllocateBoolNode(conditional_address, "0"))

        source, _ = self.visit(node.if_expr, scope)

        self.register_instruction(cil.AssignNode(conditional_address, source))
        self.register_instruction(cil.GotoIfNode(conditional_address, f"then_{node_id}"))
        self.register_instruction(cil.GotoNode(f"else_{node_id}"))

        self.register_instruction(cil.EmptyInstructionNode())
        self.register_instruction(cil.LabelNode(f"then_{node_id}"))
        then_source, then_type = self.visit(node.then_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, then_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EmptyInstructionNode())
        self.register_instruction(cil.LabelNode(f"else_{node_id}"))
        else_source, else_type = self.visit(node.else_expr, scope)
        self.register_instruction(cil.AssignNode(result_address, else_source))
        self.register_instruction(cil.GotoNode(f"endif_{node_id}"))

        self.register_instruction(cil.EmptyInstructionNode())
        self.register_instruction(cil.LabelNode(f"endif_{node_id}"))

        return result_address, then_type.join(else_type)
    
    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope):
        scope = node.scope
        # x = " ".join([f"{name}: {type_name}" for name, type_name, _ in node.declaration])
        self.register_comment("let expr")
        
        i = 0
        for name, type, expr in node.declaration:
            self.register_local(name)

            if expr:
                # self.register_EOL()
                source, _ = self.visit(expr, scope.children[i])
                self.register_instruction(cil.ArgNode(name, 0, 2))
                self.register_instruction(cil.ArgNode(source, 1, 2))
                self.register_instruction(cil.StaticCallNode("assign_funct", name, 2))        
                i += 1
            else:
                if type == "String":
                    self.register_instruction(cil.AllocateStringNode(name, "\"\""))
                elif type == "Int":
                    self.register_instruction(cil.AllocateIntNode(name, "0"))
                elif type == "Bool":
                    self.register_instruction(cil.AllocateBoolNode(name, "0"))
                else:
                    self.register_instruction(cil.AllocateNullNode(name))

        return self.visit(node.expr, scope.children[i])
    
    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope):
        scope = node.scope
        
        node_id = hash(node)
        case_expression, _ = self.visit(node.expr, scope)

        zero_int = self.define_internal_local()
        one_int = self.define_internal_local()
        len_types_int = self.define_internal_local()
        null_ptr = self.define_internal_local()
        count_of_ancestors_int = self.define_internal_local()
        comparison_result_bool = self.define_internal_local()
        case_expr_type_address = self.define_internal_local()
        ancestor_type_address = self.define_internal_local()
        ancestors_array = self.define_internal_local()
        
        
        self.register_instruction(cil.AllocateIntNode(zero_int, "0"))
        self.register_instruction(cil.AllocateIntNode(one_int, "1"))
        self.register_instruction(cil.AllocateIntNode(len_types_int, str(len(node.params))))
        self.register_instruction(cil.AllocateNullNode(null_ptr))
        
        self.register_instruction(cil.AllocateIntNode(count_of_ancestors_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comparison_result_bool, "0"))

        self.register_EOL()
        
        ##
        # contar los ancentros de el tipo de la expresion del case
        ##
        self.register_instruction(cil.TypeOfNode(case_expr_type_address, case_expression))
        self.register_instruction(cil.AssignNode(ancestor_type_address, case_expr_type_address))
        
        self.register_instruction(cil.LabelNode(f"while_start_{node_id}"))
        self.register_instruction(cil.EqualAddressNode(comparison_result_bool, ancestor_type_address, null_ptr))
        self.register_instruction(cil.GotoIfNode(comparison_result_bool, f"while_end_{node_id}"))

        # self.register_comment("Increment the count of ancestors")
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 0, 2))
        self.register_instruction(cil.ArgNode(one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", count_of_ancestors_int, 2))

        self.register_instruction(cil.ParentNode(ancestor_type_address, ancestor_type_address))
        self.register_instruction(cil.GotoNode(f"while_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"while_end_{node_id}"))
        self.register_EOL()
        
        ##
        # arrays de ancestros
        ##
        self.register_instruction(cil.AssignNode(ancestor_type_address, case_expr_type_address))
        self.register_instruction(cil.ArrayNode(ancestors_array, count_of_ancestors_int))
    
        iter_index_int = self.define_internal_local()
        comparison_result_bool = self.define_internal_local()
        
        self.register_instruction(cil.AllocateIntNode(iter_index_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comparison_result_bool, "0"))
        self.register_instruction(cil.LabelNode(f"foreach_start_{node_id}"))

        self.register_instruction(cil.ArgNode(iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("lessthan_funct", comparison_result_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(comparison_result_bool, f"foreach_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_body_{node_id}"))
        self.register_instruction(cil.SetIndexNode(ancestors_array, iter_index_int, ancestor_type_address))
        self.register_instruction(cil.ParentNode(ancestor_type_address, ancestor_type_address))

        self.register_instruction(cil.ArgNode(iter_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", iter_index_int, 2))
        
        self.register_instruction(cil.GotoNode(f"foreach_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_end_{node_id}"))
        self.register_EOL()
        
        ##
        # por cada tipo de rama guardar el indice del ancestro que le corresponde
        # sino guardar la cantidad de anccestros        
        ##
        types = [self.context.get_type(type_name) for _, type_name, _ in node.params]
        type_branch_array = self.define_internal_local()
        nearest_ancestor_array = self.define_internal_local()
        
        self.register_instruction(cil.ArrayNode(type_branch_array, len_types_int))
        self.register_instruction(cil.ArrayNode(nearest_ancestor_array, len_types_int))
        
        for i_int, t in enumerate(types):
            x = self.define_internal_local()
            i = self.define_internal_local()
            self.register_instruction(cil.AllocateIntNode(i, i_int))
            self.register_instruction(cil.TypeAddressNode(x, t.name))
            self.register_instruction(cil.SetIndexNode(type_branch_array, i, x))
            self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i, count_of_ancestors_int))
            
        self.register_EOL()

        i_int = self.define_internal_local()
        comp_i_bool = self.define_internal_local()
        type_i = self.define_internal_local()
        j_int = self.define_internal_local()
        comp_j_bool = self.define_internal_local()
        type_j = self.define_internal_local()
        types_comparison_bool = self.define_internal_local()

        self.register_instruction(cil.AllocateIntNode(i_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comp_i_bool, "0"))
        self.register_instruction(cil.AllocateIntNode(j_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(comp_j_bool, "0"))
        self.register_instruction(cil.AllocateBoolNode(types_comparison_bool, "0"))

        self.register_instruction(cil.LabelNode(f"foreach_type_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(i_int, 0, 2))
        self.register_instruction(cil.ArgNode(len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("lessthan_funct", comp_i_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(comp_i_bool, f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_type_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_type_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_i, type_branch_array, i_int))
        
        
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(zero_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("assign_funct", j_int, 2))

        self.register_instruction(cil.LabelNode(f"foreach_ancestor_start_{node_id}"))

        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("lessthan_funct", comp_j_bool, 2))
        
        self.register_instruction(cil.GotoIfNode(comp_j_bool, f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_body_{node_id}"))
        self.register_instruction(cil.GetIndexNode(type_j, ancestors_array, j_int))

        self.register_instruction(cil.EqualAddressNode(types_comparison_bool, type_i, type_j))
        self.register_instruction(cil.GotoIfNode(types_comparison_bool, f"foreach_ancestor_end_{node_id}"))
       
        self.register_instruction(cil.ArgNode(j_int, 0, 2))
        self.register_instruction(cil.ArgNode(one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", j_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_ancestor_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_ancestor_end_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(nearest_ancestor_array, i_int, j_int))
        
        self.register_EOL
        
        self.register_instruction(cil.ArgNode(i_int, 0, 2))
        self.register_instruction(cil.ArgNode(one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", i_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_type_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_type_end_{node_id}"))

        self.register_EOL()
        
        ###
        # encontrar el menor indice del ancestro
        ###
        s_index_int = self.define_internal_local()
        s_current_min_index_int = self.define_internal_local()
        s_temp_int = self.define_internal_local()
        s_current_min_int = self.define_internal_local()
        s_comparison_bool = self.define_internal_local()

        self.register_instruction(cil.AllocateIntNode(s_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(s_current_min_index_int, "0"))
        self.register_instruction(cil.AllocateIntNode(s_temp_int, "0"))
        self.register_instruction(cil.AllocateIntNode(s_current_min_int, "0"))
        self.register_instruction(cil.AllocateBoolNode(s_comparison_bool, "0"))

        self.register_instruction(cil.ArgNode(s_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("assign_funct", s_current_min_int, 2))
        
        self.register_instruction(cil.LabelNode(f"foreach_min_start_{node_id}"))
        
        self.register_instruction(cil.ArgNode(s_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(len_types_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("lessthan_funct", s_comparison_bool, 2))

        self.register_instruction(cil.GotoIfNode(s_comparison_bool, f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GotoNode(f"foreach_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_body_{node_id}"))
        self.register_instruction(cil.GetValueInIndexNode(s_temp_int, nearest_ancestor_array, s_index_int))

        self.register_instruction(cil.ArgNode(s_temp_int, 0, 2))
        self.register_instruction(cil.ArgNode(s_current_min_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("lessthan_funct", s_comparison_bool, 2)) 

        self.register_instruction(cil.GotoIfNode(s_comparison_bool, f"update_min_{node_id}"))
        self.register_instruction(cil.GotoNode(f"update_min_end_{node_id}"))
        self.register_instruction(cil.LabelNode(f"update_min_{node_id}"))
        
        self.register_instruction(cil.ArgNode(s_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(s_temp_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("assign_funct", s_current_min_int, 2))

        self.register_instruction(cil.ArgNode(s_current_min_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(s_index_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("assign_funct", s_current_min_index_int, 2))

        self.register_instruction(cil.LabelNode(f"update_min_end_{node_id}"))
        self.register_instruction(cil.ArgNode(s_index_int, 0, 2))
        self.register_instruction(cil.ArgNode(one_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", s_index_int, 2))
        self.register_instruction(cil.GotoNode(f"foreach_min_start_{node_id}"))
        self.register_instruction(cil.LabelNode(f"foreach_min_end_{node_id}"))
        
        
        ###
        # con el indice minimo obtener rama correcta
        ###
        bool_array = self.define_internal_local()
        self.register_instruction(cil.ArrayNode(bool_array, len_types_int))
        for i, _ in enumerate(types):
            x = self.define_internal_local()
            self.register_instruction(cil.AllocateIntNode(x, f"{i}"))
            self.register_instruction(cil.SetValueInIndexNode(bool_array, x, zero_int))

        self.register_EOL()
        
        exists_error_bool = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(exists_error_bool, "0"))
        
        self.register_instruction(cil.ArgNode(s_current_min_int, 0, 2))
        self.register_instruction(cil.ArgNode(count_of_ancestors_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("equal_funct", exists_error_bool, 2))

        self.register_instruction(cil.GotoIfNode(exists_error_bool, f"error_branch_{node_id}"))
        self.register_instruction(cil.SetValueInIndexNode(bool_array, s_current_min_index_int, one_int))
 
        
        s_comparison = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(s_comparison, "0"))
        self.register_EOL()
        self.register_EOL()
        
        for i_int, t in enumerate(types):
            x = self.define_internal_local()
            self.register_instruction(cil.AllocateIntNode(x, f"{i_int}"))
            self.register_instruction(cil.GetValueInIndexNode(s_comparison, bool_array, x))
            self.register_instruction(cil.GotoIfNode(s_comparison, f"branch_{t.name}_{node_id}"))
            self.register_EOL()

        resutl_address = self.define_internal_local()
        for i_int, (var_name, type_name, expr) in enumerate(node.params):
            self.register_instruction(cil.LabelNode(f"branch_{type_name}_{node_id}"))
            var = self.register_local(var_name)
            self.register_instruction(cil.ArgNode(var, 0, 2))
            self.register_instruction(cil.ArgNode(case_expression, 1, 2))
            self.register_instruction(cil.StaticCallNode("assign_funct", var, 2))
            
            expr_source, _ = self.visit(expr, scope.children[i_int])
            self.register_instruction(cil.ArgNode(resutl_address, 0, 2))
            self.register_instruction(cil.ArgNode(expr_source, 1, 2))
            self.register_instruction(cil.StaticCallNode("assign_funct", resutl_address, 2))
            self.register_instruction(cil.AssignNode(resutl_address, expr_source))
            self.register_instruction(cil.GotoNode(f"branch_end_{node_id}"))
            self.register_EOL()
            
        self.register_instruction(cil.LabelNode(f"error_branch_{node_id}"))
        # self.register_comment("Insert an error call")
        self.register_instruction(cil.LabelNode(f"branch_end_{node_id}"))

        return resutl_address, Type.multi_join(types)

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope):
        scope = node.scope
        variable = scope.find_variable(node.idx)
        variables = scope.find_all_variables_with_name(node.idx)
        source, _ = self.visit(node.expr, scope)

        # self.register_EOL()
        is_attribute = (self.current_type.contains_attribute(node.idx) and len(variables) == 1)

        if is_attribute:
            attr_names = [attr.name for attr, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.SetAttribNode("self", variable.name, source, attr_names.index(variable.name)))
            return source, variable.type
        else:
            self.register_instruction(cil.ArgNode(variable.name, 0, 2))
            self.register_instruction(cil.ArgNode(source, 1, 2))
            self.register_instruction(cil.StaticCallNode("assign_funct", variable.name, 2))

            return variable.name, variable.type

  
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope):
        scope = node.scope
        
        source, _ = self.visit(node.expr, scope)
        null_ptr = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        self.register_instruction(cil.AllocateNullNode(null_ptr))

        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(null_ptr, 1, 2))
        self.register_instruction(cil.StaticCallNode("equal_funct", result, 2))
        
        return result, self.context.get_type("Bool")
    
    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope):
        scope = node.scope
        
        obj_source, obj_type = self.visit(node.atom, scope)
        if obj_type.name == "SELF_TYPE":
            obj_type = self.current_type

        ancestor_call = False
        if node.type is not None:
            ancestor_call = True
            obj_type = self.context.get_type(node.type)

        expr_srcs = []
        for expr in node.exprlist:
            ep_source, _ = self.visit(expr, scope)
            expr_srcs.append(ep_source)

        all_methods = methods_declaration_order(obj_type)
        i = [m.name for m, _ in all_methods].index(node.idx)
        method = obj_type.get_method(node.idx)

        call_dest = self.define_internal_local()
        i_method = self.define_internal_local()
        method_address = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(i_method, f"{i}"))
        self.register_instruction(cil.GetMethodNode(method_address, obj_source, i_method, method.name, obj_type.name))

        self.register_instruction(cil.ArgNode(obj_source, 0, len(expr_srcs) + 1))
        for index, arg_source in enumerate(expr_srcs, start=1):
            self.register_instruction(cil.ArgNode(arg_source, index, len(expr_srcs) + 1))

        if ancestor_call:
            self.register_instruction(cil.StaticCallNode(self.to_function_name(method.name, obj_type.name), call_dest, len(expr_srcs) + 1))
        else:
            self.register_instruction(cil.DynamicCallNode(obj_type.name, method_address, call_dest, len(expr_srcs) + 1))
        return call_dest, method.return_type

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope):
        scope = node.scope
        
        local = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.type, local))
        self.register_instruction(cil.ArgNode(local, 0, 1))
        self.register_instruction(cil.StaticCallNode(self.to_function_name("_init_", node.type), local, 1))
        
        return local, self.context.get_type(node.type)
     
    ###############
    # ARITHMETICS #
    ###############

    ## basic arith funct

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "add_funct", "Int")  

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "minus_funct", "Int") 
    
    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "times_funct", "Int") 

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "div_funct", "Int") 
    
    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "lesseq_funct", "Int") 
    
    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "lessthan_funct", "Int") 

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope):
        scope = node.scope
        return self.visit_arith_node(node, scope, "equal_funct", "Int") 

    ## other arith funct

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope):
        scope = node.scope
        source, _ = self.visit(node.expr, scope)
        local_int_0 = self.define_internal_local()
        local_int_1 = self.define_internal_local()
        result = self.define_internal_local()
        
        self.register_instruction(cil.AllocateIntNode(local_int_0, "1"))
        self.register_instruction(cil.AllocateIntNode(local_int_1, str(2**32 - 1)))
        self.register_instruction(cil.AllocateIntNode(result, "0"))
        
        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(local_int_1, 1, 2))
        self.register_instruction(cil.StaticCallNode("xor_funct", result, 2))
        
        self.register_instruction(cil.ArgNode(result, 0, 2))
        self.register_instruction(cil.ArgNode(local_int_0, 1, 2))
        self.register_instruction(cil.StaticCallNode("add_funct", result, 2))
        return result, self.context.get_type("Int")
    
    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope):
        scope = node.scope
        source, _ = self.visit(node.expr, scope)
        local_int = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(local_int, "1"))
        self.register_instruction(cil.AllocateBoolNode(result, "0"))
        
        self.register_instruction(cil.ArgNode(source, 0, 2))
        self.register_instruction(cil.ArgNode(local_int, 1, 2))
        self.register_instruction(cil.StaticCallNode("xor_funct", result, 2))
        
        return result, self.context.get_type("Bool")

    ##########
    # ATOMIC #   ## almost done!
    ##########

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope):
        scope = node.scope
        variable = scope.find_variable(node.lex)
        all_variables = scope.find_all_variables_with_name(node.lex)

        is_attribute = (self.current_type.contains_attribute(node.lex) and len(all_variables) == 1)

        if is_attribute:
            dest = self.define_internal_local()
            attr_names = [a.name for a, _ in self.current_type.all_attributes()]
            self.register_instruction(cil.GetAttribNode(dest, "self", variable.name, attr_names.index(variable.name)))
            return dest, variable.type
        return variable.name, variable.type

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope):
        scope = node.scope
        local_str_var = self.define_internal_local()
        self.register_instruction(cil.AllocateStringNode(local_str_var, node.lex))
        return local_str_var, self.context.get_type("String")
        
    
    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope):
        scope = node.scope
        local_bool_var = self.define_internal_local()
        self.register_instruction(cil.AllocateBoolNode(local_bool_var, ("1" if node.lex.lower() == "true" else "0")))
        return local_bool_var, self.context.get_type("Bool")
    
    
    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope):
        scope = node.scope
        local_int = self.define_internal_local()
        self.register_instruction(cil.AllocateIntNode(local_int, node.lex))
        return local_int, self.context.get_type("Int")
   
    @visitor.when(NullNode)
    def visit(self, node: NullNode, scope):
        scope = node.scope
        local_null_var = self.define_internal_local()
        self.register_instruction(cil.AllocateNullNode(local_null_var))
        return local_null_var, NullType

