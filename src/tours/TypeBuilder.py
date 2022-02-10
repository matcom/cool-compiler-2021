from parsing.ast import *
from cmp.semantic import SemanticError
from cmp.semantic import ErrorType, StringType, IntType, AutoType, BoolType, ObjectType, SelfType 
import cmp.visitor as visitor 


CANNOT_INHERIT = 'SemanticError: Class %s cannot inherit class %s.'
MAIN_NOT_DEFINED = 'Method "main" must be defined in "Main" class.'
MAIN_NOT_HERITABLE = 'Class "Main" is not heritable.'
CYCLES_IN_CLASES = 'The graph defined by parent-child relation on classes may not contain cycles.'
NOT_SELF_TYPE = 'The type of the parameter "%s" can not be SELF_TYPE in method "%s" in class "%s".'
IDENTIFIER_USED = 'The identifier "%s" is already used in the param list of method "%s" in class "%s.'


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
                self.errors.append(MAIN_NOT_DEFINED)
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
                    self.errors.append(CANNOT_INHERIT.replace('%s', node.id, 1).replace('%s', parent.name, 1))
                    parent = ErrorType()
                else:
                    try:
                        main_type = self.context.get_type('Main')
                        if parent == main_type:
                            self.errors.append(MAIN_NOT_HERITABLE)
                            parent = ErrorType()
                    except SemanticError:
                        pass
            except SemanticError as error:
                self.errors.append(error.text)
                parent = ErrorType()      

            if parent.conforms_to(self.current_type):
                self.errors.append(CYCLES_IN_CLASES)
                parent = ErrorType() 
        
        if self.current_type != ObjectType():                            
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
                    self.errors.append(NOT_SELF_TYPE.replace('%s', var.id, 1).replace('%s', node.id, 1).replace('%s', self.current_type.name, 1))
                    param_type = ErrorType() 
            except SemanticError as error:
                self.errors.append(error.text)
                param_type = ErrorType()
            
            if var.id in params:
                self.errors.append(IDENTIFIER_USED.replace('%s', var.id, 1).replace('%s', node.id, 1).replace('%s', self.current_type.name, 1))
            
            params.append(var.id)
            types.append(param_type)    
        
        try:
            self.current_type.define_method(node.id, params, types, return_type)
        except SemanticError as error:
            self.errors.append(error.text)