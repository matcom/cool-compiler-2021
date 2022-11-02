# from atexit import register
# from pickle import TRUE
# from turtle import right
from .semantic import *
from . import ast_nodes_cil as cil
from . import ast_nodes as cool
from . import visitor
from typing import Optional

def methods_declaration_order(t: Type):
    method_decl = []
    all_methods = t.all_methods()
    visited = set()
    for method, _ in all_methods:
        if method.name in visited:
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
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

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
                cil_type_node.methods.append((method.name, self.to_function_name(method.name, ancestor.name)))
           
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
        
        null_ptr = self.define_internal_local("Null Pointer")
        is_null = self.define_internal_local("One of params is null")
        type_source = self.define_internal_local("Type of source")
        type_int = self.define_internal_local("Type Int")
        type_bool = self.define_internal_local("Type Bool")
        type_source_equals_int = self.define_internal_local("Type of source equals int")
        type_source_equals_bool = self.define_internal_local("Type of source equals bool")
       
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
        
    def add_basic_methods(self):
        self.add_arith_methods()
    
    def add_main_funct(self): ###
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
    
    

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        scope = node.scope
        
        self.add_basic_types()    
        
        self.add_basic_methods()  
        1 
        
    
    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope):
        ####################################################################
        # node.name -> str
        # node.parent -> str
        # node.data -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        pass
                
    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope):
        ###############################
        # node.name -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.expr -> [ ExpressionNode ... ]
        ###############################
        
        # self.current_method = self.current_type.get_method(node.name)
        
        # # Your code here!!! (Handle PARAMS)
        # #registro la funcion, devuelve un funcNode del ast de CIL
        # function_name = self.to_function_name(self.current_method.name)
        # current_method_cil = self.register_function(function_name)

        # # anado al FuncNode del ast de CIL un paramNode con el nombre de los parametros del metodo en el ast de COOL
        # #el primer parametro es self
        # current_method_cil.params.append(cil.ParamNode("self"))
        # for param in self.current_method.params_name:
        #     current_method_cil.params.append(cil.ParamNode(param))
            
        # # Your code here!!! (Handle RETURN)
        # scope = node.scope
        # value = self.visit(self.current_method.expr, scope)
    
        # # if value is None:
        # #     value = 0
        # self.register_instruction(cil.ReturnNode(value))

        # self.current_method = None
        pass

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope):
        ###############################
        # node.name -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        pass


    ###############
    # EXPRESSIONS #
    ###############

    @visitor.when(cool.ParamNode)
    def visit(self, node: cool.ParamNode, scope):
        pass

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope):
        pass
    
    @visitor.when(cool.LetNode)
    def visit(self, node: cool.BooleanNode, scope):
        pass
    
    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope):
        pass

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope):
        ###############################
        # node.idx -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # #var_ = scope.find_variable(node.idx)
        # right = self.visit(node.expr,scope)
        # self.register_instruction(cil.AssignNode(node.idx,right))
        # return right
        pass

    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope):
        pass
    
    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope):
        pass
    
    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope):
        pass
  
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope):
        pass

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope):
        ###############################
        # node.atom -> AtomicNode
        # node.idx -> str
        # node.exprlist -> [ ExpressionNode ... ]
        ###############################
        
        # args = [self.visit(node.atom)]#self
        # for param in node.exprlist:
        #     args.append(self.visit(param, scope))
            
        # for arg in args:
        #     self.register_instruction(cil.ArgNode(arg))
        
        # result = self.define_internal_local()
        # function_name = self.to_function_name(node.idx,node.type.name)
        # self.register_instruction(cil.DynamicCallNode(node.type.name,function_name,result))
        # return result
        pass

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope):
        pass
        
    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # name = ""
        # for local_var in self.localvars:
        #     if local_var.name == node.lex:
        #         return local_var.name
        pass

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope):
        ###############################
        # node.type -> str
        ###################

        # instance = self.define_internal_local()
        # self.register_instruction(cil.AllocateNode(node.type, instance))
        # type_name = node.type
        # list_attr = self.dict_attr[type_name]
        # for attr in list_attr:
        #     #att-> .name,.expr,._type
        #     if attr.expr is not None:
        #         source = self.visit(attr.expr,scope)
        #         self.register_instruction(cil. SetAttribNode(instance,attr.name,source))
        #     else:
        #          self.register_instruction(cil.AllocateNullNode(attr.name))
        # return instance
        pass


    ###############
    # ARITHMETICS #
    ###############

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # result = self.define_internal_local()
        # left = self.visit(node.left,scope)
        # right = self.visit(node.right,scope)
        # self.register_instruction(cil.PlusNode(result,left,right))
        # return result
        pass

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # result = self.define_internal_local()
        # left = self.visit(node.left,scope)
        # right = self.visit(node.right,scope)
        # self.register_instruction(cil.MinusNode(result,left,right))
        # return result
        pass

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # result = self.define_internal_local()
        # left = self.visit(node.left,scope)
        # right = self.visit(node.right,scope)
        # self.register_instruction(cil.StarNode(result,left,right))
        # return result
        pass

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # result = self.define_internal_local()
        # left = self.visit(node.left,scope)
        # right = self.visit(node.right,scope)
        # self.register_instruction(cil.DivNode(result,left,right))
        # return result
        pass
    
    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope):
        pass
    
    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope):
        pass


    ##########
    # ATOMIC #
    ##########

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        pass

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope):
        pass
    
    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # return self.define_internal_local()
        pass
