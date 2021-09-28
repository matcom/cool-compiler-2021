import cool.ast.cil_ast as cil
from cool.ast.cool_ast import *
import cmp.visitor as visitor
from cmp.semantic import VariableInfo
from cool.semantic.context import Context

class CILPrintVisitor():
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        dottypes = '\n'.join(self.visit(t) for t in node.dottypes)
        dotdata = '\n'.join(self.visit(t) for t in node.dotdata)
        dotcode = '\n'.join(self.visit(t) for t in node.dotcode)

        return f'.TYPES\n{dottypes}\n\n.DATA\n{dotdata}\n\n.CODE\n{dotcode}'

    @visitor.when(cil.DataNode)
    def visit(self, node):
        return f"{node.name} = {node.value}"

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        attributes = '\n\t'.join(f'attribute {x}' for x in node.attributes)
        methods = '\n\t'.join(f'method {x}: {y}' for x,y in node.methods)

        return f'type {node.name} {{\n\t{attributes}\n\n\t{methods}\n}}'

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        params = '\n\t'.join(self.visit(x) for x in node.params)
        localvars = '\n\t'.join(self.visit(x) for x in node.localvars)
        instructions = '\n\t'.join(self.visit(x) for x in node.instructions)

        return f'function {node.name} {{\n\t{params}\n\n\t{localvars}\n\n\t{instructions}\n}}'

    @visitor.when(cil.ParamNode)
    def visit(self, node):
        return f'PARAM {node.name}'

    @visitor.when(cil.LocalNode)
    def visit(self, node):
        return f'LOCAL {node.name}'

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        return f'{node.dest} = {node.source}'

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} + {node.right}'

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} - {node.right}'

    @visitor.when(cil.StarNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} * {node.right}'

    @visitor.when(cil.DivNode)
    def visit(self, node):
        return f'{node.dest} = {node.left} / {node.right}'

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        return f'{node.dest} = ALLOCATE {node.type}'

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        return f'{node.dest} = VCALL {node.type} {node.method}'

    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        return f'{node.dest} = GETATTR {node.source} {node.attr}'

    @visitor.when(cil.SetAttribNode)
    def visit(self, node:cil.SetAttribNode):
        return f'SETATTR {node.source} {node.attr} {node.value}'

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        return f'ARG {node.name}'

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        return f'RETURN {node.value if node.value is not None else ""}'
    
    @visitor.when(cil.AbortNode)
    def visit(self, node):
        return f'ABORT'
    
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        return f'{node.result} = COPY {node.instance}'
    
    @visitor.when(cil.LengthNode)
    def visit(self, node):
        return f'{node.dest} = LENGTH {node.string}'
    
    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        return f'{node.dest} = CONCAT {node.string1} {node.string2}'

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        return f'{node.dest} = SUBSTRING {node.string} {node.index} {node.length}'

    @visitor.when(cil.PrintNode)
    def visit(self, node):
        return f'PRINT {node.str_addr}'

    @visitor.when(cil.ToStrNode)
    def visit(self, node):
        return f'{node.dest} = TOSTR {node.ivalue}'

    @visitor.when(cil.ReadNode)
    def visit(self, node):
        return f'{node.dest} = READ'

    @visitor.when(cil.LoadNode)
    def visit(self, node:cil.LoadNode):
        return f'{node.dest} = LOAD {node.msg}'

class COOLToCILVisitor():
    
    def __init__(self, context:Context, errors=[]):
        self.errors = errors
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
    
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
    
    def to_init_attr_function_name(self, attr_name, type_name):
        return f'init_{attr_name}_at_{type_name}'
    
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
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        main_type = self.context.get_type("Main")
        main_node = InstantiateNode(("Main",0,0),0,0)
        instance = self.visit(main_node, main_type.class_node.scope)
        # self.register_instruction(cil.AllocateNode('Main', instance)) # TODO Hacer Inicializador para los Allocate y los atributos
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for type_name, typex in self.context.types.items():
            if type_name in self.context.special_types and type_name not in ["Error", "Void"]:
                self.visit(typex.class_node, typex.class_node.scope)
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        type_node = self.register_type(self.current_type.name)
        
        for attr,typex in self.current_type.all_attributes():
            type_node.attributes.append(attr.name)
            new_function = self.register_function(self.to_init_attr_function_name(attr.name, self.current_type.name))
            type_node.methods.append((f"${new_function.name}", new_function.name)) # Prefixed with $ to avoid collisions
            self.current_function = new_function
            self.visit(attr.node, attr.node.scope)

        for method,typex in self.current_type.all_methods(): # Register methods  
            if typex != self.current_type:
                method_name = self.to_function_name(method.name, typex.name)
                if all(x.name != method_name for x in self.dotcode):
                    new_function = self.register_function(method_name)
                else:
                    new_function = next(x for x in self.dotcode if x.name == method_name)
                type_node.methods.append((method.name,new_function.name))



        
        func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature in func_declarations:
            self.current_function = self.register_function(self.to_function_name(feature.id,self.current_type.name))
            type_node.methods.append((feature.id,self.current_function.name))
            self.visit(feature, feature.scope)
                
        self.current_type = None
                
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id, len(node.params))
        
        # Your code here!!! (Handle PARAMS)
        self.current_function.params.append(cil.ParamNode('self'))
        for param in self.current_method.param_names:
            self.current_function.params.append(cil.ParamNode(param))

        value = self.visit(node.body, scope)
        
        # Your code here!!! (Handle RETURN)
        self.register_instruction(cil.ReturnNode(value))
        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        self.current_function.params.append(cil.ParamNode('self'))
        result = self.visit(node.expr, scope)
        self.register_instruction(cil.SetAttribNode("self", node.id, result))
        self.register_instruction(cil.ReturnNode())
        return result
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        # Your code here!!!
        local = scope.find_variable(node.id)
        cil_local = self.register_local(local) 
        local.cil = cil_local
        value = self.visit(node.expr,scope)
        self.register_instruction(cil.AssignNode(cil_local,value))
        return cil_local

    @visitor.when(SpecialNode)
    def visit(self, node, scope=None):
        return self.visit(node.cil_node_type(), scope)

    @visitor.when(cil.ObjectCopyNode)
    def visit(self, node, scope=None):
        instance = self.current_function.params[0]
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(instance.name, result))
        return result
    
    @visitor.when(cil.ObjectAbortNode)
    def visit(self, node, scope=None):
        self.register_instruction(cil.AbortNode())
        return "0"
    
    @visitor.when(cil.ObjectTypeNameNode)
    def visit(self, node, scope=None):
        instance = self.current_function.params[0]
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(instance.name, result))
        return result

    @visitor.when(cil.StringConcatNode)
    def visit(self, node, scope=None):
        string1 = self.current_function.params[0]
        string2 = self.current_function.params[1]
        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, string1.name, string2.name))
        return result
    
    @visitor.when(cil.StringLengthNode)
    def visit(self, node, scope=None):
        string = self.current_function.params[0]
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, string.name))
        return result
        
    
    @visitor.when(cil.StringSubstringNode)
    def visit(self, node, scope=None):
        string = self.current_function.params[0]
        index = self.current_function.params[1]
        length = self.current_function.params[2]
        result = self.define_internal_local()
        self.register_instruction(cil.SubstringNode(result, string.name, index.name, length.name))
        return result
    
    @visitor.when(cil.IOInStringNode)
    def visit(self, node, scope=None):
        result = self.define_internal_local()
        self.register_instruction(cil.ReadNode(result))
        return result

    @visitor.when(cil.IOInIntNode)
    def visit(self, node, scope=None):
        result = self.define_internal_local()
        self.register_instruction(cil.ReadNode(result))
        # TODO Convertir String a Int
        return result
    
    @visitor.when(cil.IOOutIntNode)
    def visit(self, node, scope=None):
        integer = self.current_function.params[1]
        string_message = self.define_internal_local()
        self.register_instruction(cil.ToStrNode(string_message, integer.name))
        self.register_instruction(cil.PrintNode(string_message))
        return "0"
    
    @visitor.when(cil.IOOutStringNode)
    def visit(self, node, scope=None):
        string = self.current_function.params[1]
        self.register_instruction(cil.PrintNode(string.name))
        return "0"

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        local = scope.find_variable(node.id)
        value = self.visit(node.expr,scope)
        if hasattr(local,'cil'):
            self.register_instruction(cil.AssignNode(local.cil,value))
            return local.cil
        else:
            if any(x for x in self.current_function.params if x.name == local.name):
                self.register_instruction(cil.AssignNode(local.name,value)) # Param
                return local.name
            else:
                self.register_instruction(cil.SetAttribNode('self',local.name,value))
                # value = self.define_internal_local() # Attr
                # self.register_instruction(cil.GetAttribNode('self',local.name,value))
                return value # or self ?

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        
        obj_value = self.visit(node.obj,scope)

        args = []
        method = node.obj.type.get_method(node.id, len(node.args))
        for arg_node in node.args:
            value = self.visit(arg_node,scope)
            args.append(value)
            
        result = self.define_internal_local()
        
        self.register_instruction(cil.ArgNode(obj_value)) # self
        for arg,value in zip(method.param_names,args):
            self.register_instruction(cil.ArgNode(value))
        
        self.register_instruction(cil.DynamicCallNode(node.obj.type.name,node.id,result))
        
        return result
        
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        return node.lex

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################

        # Your code here!!!
        try:
            return scope.find_variable(node.lex).cil # is a Local Variable
        except AttributeError:
            if any(x for x in self.current_function.params if x.name == node.lex):
                return node.lex # Param
            else:
                value = self.define_internal_local() # Attr
                self.register_instruction(cil.GetAttribNode('self',node.lex, value))
                return value
        
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.lex, instance))
        instance_typex = self.context.get_type(node.lex)
        for attr,typex in instance_typex.all_attributes(): # Initialize Attributes
            result = self.define_internal_local()
            self.register_instruction(cil.ArgNode(instance))
            self.register_instruction(cil.StaticCallNode(
                self.to_init_attr_function_name(attr.name, instance_typex.name), result))
        return instance
        
    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local()
        self.register_instruction(cil.PlusNode(value,left,right))
        return value

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local()
        self.register_instruction(cil.MinusNode(value,left,right))
        return value

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local()
        self.register_instruction(cil.StarNode(value,left,right))
        return value

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        value = self.define_internal_local()
        self.register_instruction(cil.DivNode(value,left,right))
        return value
        
    @visitor.when(StringNode)
    def visit(self, node, scope):
        value = self.register_data(node.lex)
        result = self.define_internal_local()
        self.register_instruction(cil.LoadNode(result, value.name))
        return result
        
    # ======================================================================
