from ast import Expression
from math import exp
from threading import local
from parsing.ast import *
from cmp.semantic import Scope
from cmp.semantic import ObjectType, IntType, StringType, BoolType, ErrorType, SelfType
import cmp.visitor as visitor
from .ast_CIL import *


class CILScope :
    def __init__(self):
        self.let_count = 0
        self.if_count = 0
        self.variables_count = 0
        self.locals = []
        self.instructions= []
        self.data = []
        self.functions = []
        self.current_class = ""

#pending 
def create_init_class(attributes, expresions):
    for attr,expr in zip(attributes,expresions):
        assig = CILAssignNode (attr.id,expr)

class CIL:
    def __init__(self):
        self.scope = CILScope()

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        types = []
        self.scope.locals = []
        self.scope.instuctions = []
        for dec in node.declarations:# organizar de modo q quede el main de primero
            (type,expressions) = self.visit( dec)
            types.append(type)
            #init_class = create_init_class (type.attributes,expressions)    
            #self.scope.functions.append (init_class)
            self.scope.locals = []
        self.scope.instuctions = []
        return CILProgramNode(types, self.scope.data, self.scope.functions)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.scope.current_class = node.id
        attributes = []
        expressions = []
        methods = []
        for feature in node.features:
            if isinstance (feature,AttrDeclarationNode):
                attr = self.visit(feature)
                attributes.append(attr)
                expression = self.visit(feature.expr)
                expressions.append(expression)
            else:
                function = self.visit(feature)
                self.scope.functions.append(function) 
                methods.append(CILMethodNode(feature.id, function.id))   
                
        methods.append(CILMethodNode('init', f'init_{node.id}'))               
        return (CILTypeNode (node.id, attributes,methods),expressions)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        return CILAttributeNode (node.id, node.type)
    
    @visitor.when(FuncDeclarationNode) 
    def visit(self, node):
        params = []
        self.scope.instructions = []
        self.scope.locals = []
        for param in node.params:
            id = param.id
            type =  param.type
            param_node = CILParamNode(id, type)
            params.append(param_node)
        self.visit(node.expr)    
        return CILFuncNode(f'{node.id}_{self.scope.current_class}', params, self.scope.locals, self.scope.instructions)
                   
    @visitor.when(BlockNode)
    def visit(self, node): 
        for expr in node.expr_lis:
            self.visit(expr)
            

    @visitor.when(DispatchNode)
    def visit(self, node):
        pass        

    @visitor.when(ConditionalNode)
    def visit(self, node):
       pass
            
    @visitor.when(LetNode)
    def visit(self, node):
        for variable in node.variables:
            self.visit(variable)
        temp_name = f't{self.scope.variables_count}'
        self.scope.variables_count += 1
        expr = self.visit(node.expr)
        self.scope.instructions.append(CILAssignNode( temp_name, expr))
        local = CILLocalNode(temp_name,node.computed_type.name)
        self.scope.locals.append(local)
        
    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        local = CILLocalNode(node.id,node.type)
        self.scope.locals.append(local)
        if node.expr is not None:
            expr = self.visit(node.expr)
            instruction = CILAssignNode (node.id, expr)
            self.scope.instructions.append(instruction)
        
    @visitor.when(LoopNode)
    def visit(self, node):
        pass
          
    @visitor.when(CaseNode)
    def visit(self, node):
        pass

    @visitor.when(CaseAttrNode)
    def visit(self, node):  
        pass
    
    @visitor.when(AssignNode)
    def visit(self, node):
        exp = self.visit(node.expr)
        return CILAssignNode(node.id.id, exp)
                                     
    @visitor.when(BinaryNode)
    def visit(self, node):
        if not isinstance(node.left, AtomicNode):
            name = "t" + str(self.scope.variables_count)
            self.scope.variables_count += 1
            type = node.left.computed_type.name
            self.scope.locals.append(CILLocalNode(name, type))
            expr = self.visit(node.left)
            self.scope.instructions.append(CILAssignNode(name, expr))
            left = CILVariableNode(name)
        else:
            left = self.visit(node.left)  

        if not isinstance(node.right, AtomicNode):
            name = "t" + str(self.scope.variables_count)
            self.scope.variables_count +=1
            type = node.right.computed_type.name
            self.scope.locals.append(CILLocalNode(name, type))
            expr = self.visit(node.right)
            self.scope.instructions.append(CILAssignNode(name, expr))
            right = CILVariableNode(name)
        else:
            right = self.visit(node.right)
        
        if isinstance(node, PlusNode):
            return CILPlusNode(left, right)
        elif isinstance(node, MinusNode):
            return CILMinusNode(left, right)
        elif isinstance(node, DivNode):
            return CILDivNode(left, right)
        elif isinstance(node, StarNode):
            return CILStarNode(left, right)
        elif isinstance(node, ElessNode):
            return CILElessNode(left, right)
        elif isinstance(node, LessNode):
            return CILLessNode(left, right)
        else:
            return CILEqualsNode(left, right)
                
    @visitor.when(PrimeNode)
    def visit(self, node):
        pass
   
    @visitor.when(NotNode)
    def visit(self, node):
       pass
    @visitor.when(StringNode)
    def visit(self, node):
        pass

    @visitor.when(IsVoidNode)
    def visit(self, node):
        pass
    
    @visitor.when(ConstantNumNode)
    def visit(self, node):
        return CILNumberNode(node.lex)

    @visitor.when(VariableNode)
    def visit(self, node):
        return CILVariableNode(node.lex) 
   
    @visitor.when(TrueNode)
    def visit(self, node):
       pass

    @visitor.when(FalseNode)
    def visit(self, node):
        pass   
    
    @visitor.when(InstantiateNode)
    def visit(self, node):
        pass 
