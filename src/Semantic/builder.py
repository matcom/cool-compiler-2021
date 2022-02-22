import Tools.visitor as visitor

from Parser.ast import *
from Tools.messages import *
from Tools.context import ErrorType
from Tools.errors import SemanticError, TypesError

class TypeBuilder:
    def __init__(self, contex):
        self.context = contex
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.id, node.pos)
        except SemanticError as error:
            self.current_type = ErrorType()
            self.errors.append(error)    
        if node.parent is not None:
            if node.parent in ['Int', 'String', 'Bool']:
                self.errors.append(SemanticError(INHERIT_ERROR % (node.id, node.parent), *node.parent_pos))
            try:
                parent = self.context.get_type(node.parent, node.parent_pos)
            except SemanticError:
                self.errors.append(TypesError(INHERIT_UNDEFINED % (node.id, node.parent), *node.parent_pos))
                parent = None
            try:
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        raise SemanticError(CIRCULAR_DEPENDENCY %(self.current_type.name, self.current_type.name) , *node.pos)
                    current = current.parent
            except SemanticError as e:
                parent = ErrorType()
                self.errors.append(e)
            self.current_type.set_parent(parent)    
        for feature in node.features:
            self.visit(feature)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode):
        args_names = []
        args_types = []
        for name, type_ in node.params:
            if name in args_names:
                self.errors.append(SemanticError(PARAMETER_MULTY_DEFINED % name, *type_.pos))
            args_names.append(name)      
            try:
                arg_type = self.context.get_type(type_.value, type_.pos)
            except SemanticError:
                self.errors.append(TypesError(PARAMETER_UNDEFINED % (type_.value, type_.value), *type_.pos))
                arg_type = ErrorType()
            args_types.append(arg_type)      
        try:
            return_type = self.context.get_type(node.type, node.type_pos)
        except SemanticError as error:
            self.errors.append(TypesError(RETURN_TYPE_UNDEFINED % (node.type, node.id), *node.type_pos))
            return_type = ErrorType(node.type_pos) 
        try:
            self.current_type.define_method(node.id, args_names, args_types, return_type, node.pos)
        except SemanticError as error:
            self.errors.append(error)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode):
        try:
            attr_type = self.context.get_type(node.type, node.pos)
        except SemanticError as error:
            attr_type = ErrorType(node.type_pos)
            self.errors.append(TypesError(ATTR_TYPE_UNDEFINED %(node.type, node.id), *node.type_pos))      
        if node.id == 'self':
            self.errors.append(SemanticError(SELF_ATTR, *node.pos)) 
        try:
            self.current_type.define_attribute(node.id, attr_type, node.pos)
        except SemanticError as error:
            self.errors.append(error)  