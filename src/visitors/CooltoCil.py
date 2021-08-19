from cool_ast.cool_ast import *
import cil_ast as cil
from utils.semantic import Context, SemanticError, Type, Method, Scope, ErrorType, VariableInfo
import visitors.visitor as visitor
import cil_ast.cil as cil

class BaseCOOLToCILVisitor:
    def __init__(self, context):
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
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
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
        
        # Your code here!!! (Handle all the .TYPE section)
          
        func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)
                
        self.current_type = None
                
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id)
        
        # Your code here!!! (Handle PARAMS)
        
        for instruction, child_scope in zip(node.body, scope.children):
            value = self.visit(instruction, child_scope)
        # Your code here!!! (Handle RETURN)
        
        self.current_method = None

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # Your code here!!!
        pass

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # Your code here!!!
        pass

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        
        # Your code here!!!
        pass

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!! (Pretty easy ;-))
        pass

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        pass

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        pass

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
        
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.DivNode(dest, left, right))
        return dest
