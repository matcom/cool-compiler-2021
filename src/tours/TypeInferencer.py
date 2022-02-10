from parsing.ast import *
from .utils import InferType
from cmp.semantic import Scope, SemanticError
from cmp.semantic import Type, ObjectType, IntType, StringType, BoolType, AutoType, ErrorType, SelfType, IOType
import cmp.visitor as visitor


class TypeInferencer:
    def __init__(self, context=None, errors=[]):
        self.context = context
        self.errors = errors
        self.current_type = None
        self.current_method = None
        self.change = False

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)
        return self.change

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                if self.current_type.get_attribute(feature.id).type.name == feature.type:
                    self.visit(feature)
                elif feature.expr is not None:
                    self.visit(feature.expr)
            else:
                self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        node_type = self.current_type.get_attribute(node.id).type
        
        if node.expr is not None:
            self.visit(node.expr)
            expr_type = node.expr.computed_type
        
            if node_type == AutoType() and expr_type == AutoType():
                if expr_type.infered_type is not None:
                    self.change |= InferType(self.current_type, node_type, expr_type.infered_type)
                if node_type.infered_type is not None:
                    self.change |= InferType(self.current_type, expr_type, node_type.infered_type)

    @visitor.when(FuncDeclarationNode) 
    def visit(self, node):
        self.current_method = self.current_type.get_method(node.id)
        self.visit(node.expr)

        return_type_exp = node.expr.computed_type 
        return_type_met = self.current_method.return_type 

        if return_type_met == AutoType() and return_type_exp == AutoType():
            if return_type_exp.infered_type is not None:
                self.change |= InferType(self.current_type, return_type_met, return_type_exp.infered_type)
            if return_type_met.infered_type is not None:
                self.change |= InferType(self.current_type, return_type_exp, return_type_met.infered_type)
       
    @visitor.when(BlockNode)
    def visit(self,node):
        for expr in node.expr_lis:
            self.visit(expr)

    @visitor.when(DispatchNode)
    def visit(self, node):     
            if node.expr is not None:
                self.visit(node.expr)
                
                if node.computed_type != ErrorType():
                    obj_type = node.expr.computed_type
                    if node.type is not None:
                        obj_type = self.context.get_type(node.type)  
            else:
                obj_type = self.current_type
            
            try:
                method = obj_type.get_method(node.id)
                if (node.arg is None and method.arg is None) or (len(node.arg) == len(method.param_types)):
                    if node.arg is not None:
                        for arg, param_type in zip(node.arg, method.param_types):
                            self.visit(arg)
                            arg_type = arg.computed_type
                            if param_type == AutoType() and arg_type == AutoType():
                                if arg_type.infered_type is not None:
                                    self.change |= InferType(self.current_type, param_type, arg_type.infered_type)
                                if param_type.infered_type is not None:
                                    self.change |= InferType(self.current_type, arg_type, param_type.infered_type)
            except:
                pass               
                
    @visitor.when(ConditionalNode)
    def visit(self, node):
        self.visit(node.predicate)
        self.visit(node.then)
        self.visit(node.elsex)

    @visitor.when(LetNode)
    def visit(self, node):
        for item in node.variables:
            self.visit(item)
        self.visit(node.expr)            

    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        try:
            var_type = node.computed_type
            if node.expr is not None:    
                self.visit(node.expr)
                expresion_type = node.expr.computed_type 
            
                if var_type == AutoType() and expresion_type == AutoType():
                    if expresion_type.infered_type is not None:
                        self.change |= InferType(self.current_type, var_type, expresion_type.infered_type)
                    if var_type.infered_type is not None:
                        self.change |= InferType(self.current_type, expresion_type, var_type.infered_type)
        except:
            pass
             
    @visitor.when(LoopNode)
    def visit(self, node):
        self.visit(node.predicate)
        self.visit(node.body)
    
    @visitor.when(CaseNode)
    def visit(self, node):
        self.visit(node.expr)
        for attr in node.cases:
            self.visit(attr)

    @visitor.when(CaseAttrNode)
    def visit(self, node):  
        self.visit(node.expr)

    @visitor.when(AssignNode)
    def visit(self, node):
        self.visit(node.id)
        var_type = node.id.computed_type 
        self.visit(node.expr)
        expresion_type = node.expr.computed_type   

        if var_type == AutoType() and expresion_type == AutoType():
            if expresion_type.infered_type is not None:
                self.change |= InferType(self.current_type, var_type, expresion_type.infered_type)
            if var_type.infered_type is not None:
                self.change |= InferType(self.current_type, expresion_type, var_type.infered_type)

    @visitor.when(BinaryNode)
    def visit(self, node):
        self.visit(node.left)  
        self.visit(node.right)

        if isinstance(node, EqualsNode):      
            left_type = node.left.computed_type
            right_type = node.right.computed_type

            if left_type == AutoType() and right_type == AutoType():
                if left_type.infered_type is not None and (left_type.infered_type == StringType() or left_type.infered_type == BoolType() or left_type.infered_type == IntType()):
                    self.change |= InferType(self.current_type, right_type, left_type.infered_type)
            
                if right_type.infered_type is not None and (right_type.infered_type == StringType() or right_type.infered_type == BoolType() or right_type.infered_type == IntType()):
                    self.change |= InferType(self.current_type, left_type, right_type.infered_type)

    @visitor.when(PrimeNode)
    def visit(self, node):
        self.visit(node.expr)
    
    @visitor.when(NotNode)
    def visit(self, node):
        self.visit(node.expr)

    @visitor.when(StringNode)
    def visit(self, node):
        pass
    
    @visitor.when(IsVoidNode)
    def visit(self, node):
        self.visit(node.expr)
    
    @visitor.when(VariableNode)
    def visit(self, node):
        pass

    @visitor.when(TrueNode)
    def visit(self, node):
        pass

    @visitor.when(FalseNode)
    def visit(self, node):
        pass
    
    @visitor.when(InstantiateNode)
    def visit(self, node):
        pass     