from cool_ast.cool_ast import *
import cil_ast.cil_ast as cil
from utils.semantic import Context, SemanticError, Type, Method, Scope, ErrorType, VariableInfo
import visitors.visitor as visitor
# from utils.errors import _TypeError, _NameError, _SemanticError, _AtributeError

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context

        self.locals = {}
        self.attrs = set()
        self.parameters = set()
        self.instances = []

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


class MiniCOOLToCILVisitor(BaseCOOLToCILVisitor):
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
        self.instances.append(instance)
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        self.instances.pop()
        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        # Your code here!!! (Handle all the .TYPE section)
        type_node = self.register_type(node.id)

        attributes = []
        methods = []
        self.attrs.clear()
        
        current_type = self.current_type
        while current_type.parent is not None:
            attr_temp = []
            method_temp = []
            for attr in current_type.attributes:
                self.attrs.add(attr.name)
                attr_temp.append(attr.name)
            
            for method in current_type.methods:
                method_temp.append((method.name, self.to_function_name(method.name, current_type.name)))
            
            attributes = attr_temp + attributes
            methods = method_temp + methods
            
            current_type = current_type.parent
            
        
        type_node.attributes = attributes
        type_node.methods = methods
        
        
        # func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature, child_scope in zip(node.features, scope.children):
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, child_scope)
        
        #falta visitar los atributos
        
        self.current_type = None


    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id, self.current_type, False)
        
        # Your code here!!! (Handle PARAMS)
        self.current_function = self.register_function(self.to_function_name(node.id, self.current_type.name))

        self.parameters.clear()
        self.params.append(cil.ParamNode('self'))
        for arg_name, _ in node.params:
            self.params.add(arg_name)
            self.params.append(cil.ParamNode(arg_name))
        
        self.locals.clear()
        return_value = self.visit(node.body, scope.children[0])
        # for instruction, child_scope in zip(node.body, scope.children):
        #     value = self.visit(instruction, child_scope)

        # Your code here!!! (Handle RETURN)
        if node.body and 'Void' != node.type: 
            self.register_instruction(cil.ReturnNode(return_value))
        else:
            self.register_instruction(cil.ReturnNode())
            
        self.current_method = None

    @visitor.when(VarDeclarationNode) # AssignNode
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # Your code here!!!
        var = scope.find_variable(node.id)
        dest = self.locals[var.name] = self.register_local(var)
        
        if node.expr is not None:
            source = self.visit(node.expr, scope)
        else:
            # asignar valor por default
            if node.type.lower() == 'int':
                source = 0
            elif node.type.lower() == 'string':
                source = ''
            elif node.type.lower() == 'bool':
                source = False
            else:
                source = None 
        self.register_instruction(cil.AssignNode(dest, source))
        return dest
            

    @visitor.when(AssignNode) # 
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # Your code here!!!
        if node.id in self.parameters:
            dest = node.id
            source = self.visit(node.expr, scope)
            self.register_instruction(cil.AssignNode(dest, source))
        elif node.id in self.locals:
            dest = self.locals[node.id]
            source = self.visit(node.expr, scope)
            self.register_instruction(cil.AssignNode(dest, source))
        elif node.id in self.attrs:
            source = self.visit(node.expr, scope)
            self.register_instruction(cil.SetAttribNode(self.instances[-1], node.id, source))

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.method -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        
        # Your code here!!!
        if node.obj is not None: # dynamic
            obj = self.visit(node.obj, scope)
            self.instances.append(obj)
            if isinstance(node.obj, InstantiateNode):
                obj_type = node.obj.lex
            else:
                obj_type = scope.find_variable(node.obj.lex).type.name
            
            local = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(obj, local))
            
            self.register_instruction(cil.ArgNode(obj))
            for arg in node.args:
                self.register_instruction(cil.ArgNode(self.visit(arg, scope)))
            
            dest = self.define_internal_local()
            obj_type = obj_type if node.parent == None else node.parent
            self.register_instruction(cil.DynamicCallNode(local, self.to_function_name(node.method, obj_type), dest))
        else: # static
            self.register_instruction(cil.ArgNode(self.instances[-1]))
            for arg in node.args:
                self.register_instruction(cil.ArgNode(self.visit(arg, scope)))
                
            dest = self.define_internal_local()
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.method, self.current_type.type.name), dest))
        self.instances.pop()
        return dest

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
        
        pass

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        dest = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.lex, dest))
        return dest

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.PlusNode(dest, left, right))
        return dest

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.MinusNode(dest, left, right))
        return dest

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.StarNode(dest, left, right))
        return dest

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.DivNode(dest, left, right))
        return dest