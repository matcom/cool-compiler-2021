from parsing.ast import *
from cmp.semantic import SemanticError
from cmp.semantic import ErrorType, StringType, IntType, BoolType, ObjectType, SelfType 
import cmp.visitor as visitor 


CANNOT_INHERIT = "SemanticError: Class %s cannot inherit class %s."
MAIN_NOT_DEFINED = "SemanticError: Method main must be defined in Main class."
MAIN_NOT_HERITABLE = "SemanticError: Class Main is not heritable."
CYCLES_IN_CLASES = "SemanticError: Class %s, or an ancestor of %s, is involved in an inheritance cycle."
NOT_SELF_TYPE = "TypeError: The type of the parameter %s can not be SELF_TYPE in method %s in class %s."
IDENTIFIER_USED = "SemanticError: Formal parameter %s is multiply defined."
ATTRIBUTE_REDEFINED = "SemanticError: Attribute %s is multiply defined in class."
METHOD_REDEFINED = "SemanticError: Method %s is multiply defined in class."
UNDEFINED_ATTRIBUTE_TYPE ="TypeError: Class %s of attribute %s is undefined."
PARENT_ATTRIBUTE_REDEFINED = "SemanticError: Attribute %s is an attribute of an inherited class."
PARENT_NOT_DEFINED = "TypeError: Class %s inhertits from an undefined class %s."
UNDEFINED_PARAM_TYPE = "TypeError: Class %s of formal parameter %s is undefined."
UNDEFINED_RETURN_TYPE = "TypeError: Undefined return type %s in method %s."


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
                if parent == BoolType() or parent == IntType() or parent == StringType() or parent == SelfType():
                    e = CANNOT_INHERIT.replace('%s', node.id, 1).replace('%s', parent.name, 1)
                    location = node.parent_location
                    self.errors.append(f'{location} - {e}')
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
                e = PARENT_NOT_DEFINED.replace('%s', node.id, 1).replace('%s', node.parent, 1)
                location = node.parent_location
                self.errors.append(f'{location} - {e}')
                parent = ErrorType()      

            if parent.conforms_to(self.current_type):
                e = CYCLES_IN_CLASES.replace('%s', node.id, 2)
                location = node.parent_location
                self.errors.append(f'{location} - {e}')
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
            e = UNDEFINED_ATTRIBUTE_TYPE.replace('%s', node.type, 1).replace('%s', node.id, 1)
            location = node.type_location
            self.errors.append(f'{location} - {e}')
            att_type = ErrorType()
        
        try:
            self.current_type.define_attribute(node.id, att_type)
        except SemanticError as error:
                x = self.current_type.get_attribute_parent(node.id)
                if x == self.current_type:
                    e = ATTRIBUTE_REDEFINED.replace('%s', node.id, 1)
                    self.errors.append(f'{node.location} - {e}')
                else:
                    e = PARENT_ATTRIBUTE_REDEFINED.replace('%s', node.id, 1)
                    self.errors.append(f'{node.location} - {e}')
                    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):  
        try:
            return_type = self.context.get_type(node.type)
        except SemanticError as error:
            e = UNDEFINED_RETURN_TYPE.replace('%s', node.type, 1).replace('%s', node.id, 1)
            location = node.type_location
            self.errors.append(f'{location} - {e}')
            return_type = ErrorType() 
        
        params = []
        types = []
        for var in node.params:
            try:
                param_type = self.context.get_type(var.type)
                if param_type == SelfType():
                    e = NOT_SELF_TYPE.replace('%s', var.id, 1).replace('%s', node.id, 1).replace('%s', self.current_type.name, 1)
                    location = var.type_location
                    self.errors.append(f'{location} - {e}')
                    param_type = ErrorType() 
            except SemanticError as error:
                e = UNDEFINED_PARAM_TYPE.replace('%s', var.type, 1).replace('%s', var.id, 1)
                location = var.type_location
                self.errors.append(f'{location} - {e}')
                param_type = ErrorType()
            
            if var.id in params:
                e = IDENTIFIER_USED.replace('%s', var.id, 1)
                self.errors.append(f'{var.location} - {e}')
            
            params.append(var.id)
            types.append(param_type)    
        
        try:
            self.current_type.define_method(node.id, params, types, return_type)
        except SemanticError as error:
            e = (METHOD_REDEFINED.replace('%s', node.id, 1))
            self.errors.append(f'{node.location} - {e}')
