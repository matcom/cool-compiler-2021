# from atexit import register
# from pickle import TRUE
# from turtle import right
from .semantic import *
from utils import ast_nodes_cil as cil
from utils import ast_nodes as cool
from utils import visitor

class BaseCOOLToCILVisitor:
    def __init__(self, context,dict_attr,dict_method):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
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
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def add_basic_types():
        pass

    def add_basic_methods():
        pass

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cool.ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        #inicializar atributos de la clase main?
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for declaration, child_scope in zip(node.class_list, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(cool.ClassDecNode)
    def visit(self, node, scope):
        ####################################################################
        # node.name -> str
        # node.parent -> str
        # node.data -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.name)
        
        # Your code here!!! (Handle all the .TYPE section)
        current_type_cil = self.register_type(self.current_type.name)
        all_attributes =  [attr for attr,_ in self.current_type.all_attributes(True)]
        for attr in all_attributes:
            self.visit(attr,scope)
            current_type_cil.attributes.append(attr.name)
           
        #?? los metodos de las clases padres coinciden con los scopes hijos ??
        all_methods = [method  for method,_ in self.current_type.all_methods(True)]
        i = 0
        for attr in self.current_type.attributes:
            i += attr.expr != None  

        for i,method in enumerate(all_methods,start=i):
            self.visit(method, scope.children[i])
            function_name = self.to_function_name(method.name,current_type_cil.name)
            current_type_cil.methods.append((method.name,function_name))

        self.current_type = None
                
    @visitor.when(cool.MethodDecNode)
    def visit(self, node, scope):
        ###############################
        # node.name -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.expr -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.name)
        
        # Your code here!!! (Handle PARAMS)
        #registro la funcion, devuelve un funcNode del ast de CIL
        function_name = self.to_function_name(self.current_method.name)
        current_method_cil = self.register_function(function_name)

        # anado al FuncNode del ast de CIL un paramNode con el nombre de los parametros del metodo en el ast de COOL
        #el primer parametro es self
        current_method_cil.params.append(cil.ParamNode("self"))
        for param in self.current_method.params_name:
            current_method_cil.params.append(cil.ParamNode(param))
            
        # Your code here!!! (Handle RETURN)
        scope = node.scope
        value = self.visit(self.current_method.expr, scope)
    
        # if value is None:
        #     value = 0
        self.register_instruction(cil.ReturnNode(value))

        self.current_method = None

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node, scope):
        ###############################
        # node.name -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        pass

    @visitor.when(cool.AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.idx -> str
        # node.expr -> ExpressionNode
        ###############################
        
        #var_ = scope.find_variable(node.idx)
        right = self.visit(node.expr,scope)
        self.register_instruction(cil.AssignNode(node.idx,right))
        return right

    @visitor.when(cool.MethodCallNode)
    def visit(self, node, scope):
        ###############################
        # node.atom -> AtomicNode
        # node.idx -> str
        # node.exprlist -> [ ExpressionNode ... ]
        ###############################
        
        args = [self.visit(node.atom)]#self
        for param in node.exprlist:
            args.append(self.visit(param,scope))
            
        for arg in args:
            self.register_instruction(cil.ArgNode(arg))
        
        result = self.define_internal_local()
        function_name = self.to_function_name(node.idx,node.type.name)
        self.register_instruction(cil.DynamicCallNode(node.type.name,function_name,result))
        return result

    @visitor.when(cool.NumberNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return self.define_internal_local()

    @visitor.when(cool.VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        name = ""
        for local_var in self.localvars:
            if local_var.name == node.lex:
                return local_var.name

    @visitor.when(cool.NewNode)
    def visit(self, node, scope):
        ###############################
        # node.type -> str
        ###################

        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.type, instance))
        type_name = node.type
        list_attr = self.dict_attr[type_name]
        for attr in list_attr:
            #att-> .name,.expr,._type
            if attr.expr is not None:
                source = self.visit(attr.expr,scope)
                self.register_instruction(cil. SetAttribNode(instance,attr.name,source))
            else:
                 self.register_instruction(cil.AllocateNullNode(attr.name))
        return instance

    @visitor.when(cool.PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        result = self.define_internal_local()
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        self.register_instruction(cil.PlusNode(result,left,right))
        return result

    @visitor.when(cool.MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        result = self.define_internal_local()
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        self.register_instruction(cil.MinusNode(result,left,right))
        return result

    @visitor.when(cool.TimesNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        result = self.define_internal_local()
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        self.register_instruction(cil.StarNode(result,left,right))
        return result

    @visitor.when(cool.DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        result = self.define_internal_local()
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        self.register_instruction(cil.DivNode(result,left,right))
        return result
        
    @visitor.when(cool.StringNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        pass

