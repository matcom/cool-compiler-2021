import compiler.visitors.visitor as visitor
from ..cmp import cil_ast as cil
from ..cmp.semantic import Scope, SemanticError, ErrorType, IntType, BoolType, SelfType, AutoType, LCA
from ..cmp.ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from ..cmp.ast import AssignNode, CallNode, CaseNode, BlockNode, LoopNode, ConditionalNode, LetNode
from ..cmp.ast import ArithmeticNode, ComparisonNode, EqualNode
from ..cmp.ast import VoidNode, NotNode, NegNode
from ..cmp.ast import ConstantNumNode, ConstantStringNode, ConstantBoolNode, VariableNode, InstantiateNode
from ..cmp.ast import PlusNode, MinusNode, StarNode, DivNode

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
        type_node = self.register_type(self.current_type.name)
        
        visited_func = []
        current = self.current_type
        while current is not None:
            attributes = [attr.name for attr in current.attributes]
            methods = [func.name for func in current.methods if func.name not in visited_func]
            visited_func.extend(methods)
            type_node.attributes.extend(attributes[::-1])
            type_node.methods.extend([(item, self.to_function_name(item, current.name)) for item in methods[::-1]])
            current = current.parent
        
        type_node.attributes.reverse()
        type_node.methods.reverse()
        
              
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
        self.current_function = self.register_function(self.to_function_name(self.current_method.name, self.current_type.name))
        self.current_vars = {}
        self.params.append(cil.ParamNode('self'))
        self.params.extend([cil.ParamNode(p) for p in self.current_method.param_names]) 
        
        value = None
        for instruction in node.body:
            value = self.visit(instruction, scope)
        
        # Your code here!!! (Handle RETURN)
        if isinstance(self.current_method.return_type, VoidType):
            value = None
        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
        
        self.current_method = None

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        
        # Your code here!!!
        
        #TODO!!!!
        
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
        return node.lex
        

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        
        # Your code here!!!
        return node.lex
    

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
        
        # Your code here!!!
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.PlusNode(var, left, right))
        return var
        
        

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.MinusNode(var, left, right))
        return var
        

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.StarNode(var, left, right))
        return var
        

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        
        # Your code here!!!
        var = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.DivNode(var, left, right))
        return var
        