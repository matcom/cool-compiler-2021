from parsing.ast import *
from cmp.semantic import SemanticError
from cmp.semantic import ErrorType, StringType, IntType, AutoType, BoolType, ObjectType, IOType, SelfType 
import cmp.visitor as visitor 

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors
        self.current_type = None
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)
        
        # Check that class Main contains method main
        try:
            main_type = self.context.get_type('Main')
            try:
                main_type.get_method('main')
            except SemanticError:
                self.errors.append("Method 'main' must be defined in 'Main' class.")
        except SemanticError:
            pass
       
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        
        # Set class parent, if it does not exist then the class inherits from Object
        parent = self.context.get_type('Object')
        if node.parent is not None: 
            try:
                parent = self.context.get_type(node.parent)
                if parent == BoolType() or parent == IntType() or parent == StringType() or parent == SelfType() or parent == AutoType():
                    self.errors.append(f"Class '{parent.name}' is not heritable.")
                    parent = ErrorType()
                else:
                    try:
                        main_type = self.context.get_type('Main')
                        if parent == main_type:
                            self.errors.append(f"Class 'Main' is not heritable.")
                            parent = ErrorType()
                    except SemanticError:
                        pass
            except SemanticError as error:
                self.errors.append(error.text)
                parent = ErrorType()      

            if parent.conforms_to(self.current_type):
                self.errors.append(f"The graph defined by parent-child relation on classes may not contain cycles.")
                parent = ErrorType() 
                                    
        self.current_type.set_parent(parent)

        for feature in node.features:
            self.visit(feature)        
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            att_type = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(error.text)
            att_type = ErrorType()
        
        try:
            self.current_type.define_attribute(node.id, att_type)
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):  
        try:
            return_type = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(error.text)
            return_type = ErrorType() 
        
        params = []
        types = []
        for var in node.params:
            try:
                param_type = self.context.get_type(var.type)
                if param_type == SelfType():
                    self.errors.append(f"The type of the parameter '{var.id}' can not be SELF_TYPE in method '{node.id}' in class '{self.current_type.name}'.")
                    param_type = ErrorType() 
            except SemanticError as error:
                self.errors.append(error.text)
                param_type = ErrorType()
            
            if var.id in params:
                self.errors.append(f"The identifier '{var.id}' is already used in the param list of method '{node.id}' in class '{self.current_type.name}'.")
            
            params.append(var.id)
            types.append(param_type)    
        
        try:
            self.current_type.define_method(node.id, params, types, return_type)
        except SemanticError as error:
            self.errors.append(error.text)