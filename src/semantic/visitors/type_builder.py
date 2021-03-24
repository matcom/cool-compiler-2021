from utils.ast import *
from utils import visitor
from utils.errors import *
from semantic.types import *
from semantic.tools import Context

class TypeBuilder:
    def __init__(self, context : Context, errors : list) -> None:
        self.context:Context = context
        self.errors:list = errors
        self.current_type:Type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node : ClassDeclarationNode):
        try:
            self.current_type = self.context.get_type(node.id, node.pos)
        except SemanticError as exception:
            self.current_type = ErrorType()
            self.errors.append(exception)

        if node.parent is not None:
            if node.parent in ['Int', 'Bool', 'String']:
                error_text = SemanticError.INHERIT_ERROR % (node.id, node.parent)
                self.errors.append(SemanticError(*node.parent_pos, error_text))

            try:
                parent = self.context.get_type(node.parent, node.parent_pos)
            except SemanticError:
                error_text = TypesError.INHERIT_UNDEFINED % (node.id, node.parent)
                self.errors.append(TypesError(*node.parent_pos, error_text))
                parent = None

            try:
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        error_text = SemanticError.CIRCULAR_DEPENDENCY % (self.current_type.name, self.current_type.name)
                        raise SemanticError(*node.pos, error_text)
                    current = current.parent
            except SemanticError as exception:
                parent = ErrorType()
                self.errors.append(exception)

            self.current_type.set_parent(parent)
        
        for feature in node.features:
            self.visit(feature)
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node : FuncDeclarationNode):
        args_names, args_types = [], []

        for name, type_ in node.params:
            if name in args_names:
                error_text = SemanticError.PARAMETER_MULTY_DEFINED % name
                self.errors.append(SemanticError(*type_.pos, error_text))
            args_names.append(name)
            
            try:
                arg_type = self.context.get_type(type_.value, type_.pos)
            except SemanticError:
                error_text = TypesError.PARAMETER_UNDEFINED % (type_.value, name)
                self.errors.append(TypesError(*type_.pos, error_text))
                arg_type = ErrorType()

            args_types.append(arg_type)
            
        try:
            return_type = self.context.get_type(node.type, node.type_pos)
        except SemanticError as exception:
            error_text = TypesError.RETURN_TYPE_UNDEFINED % (node.type, node.id)
            self.errors.append(TypesError(*node.type_pos, error_text))
            return_type = ErrorType(node.type_pos)
    
        try:
            self.current_type.define_method(node.id, args_names, args_types, return_type, node.pos)
        except SemanticError as exception:
            self.errors.append(exception)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node : AttrDeclarationNode):
        try:
            attr_type = self.context.get_type(node.type, node.pos)
        except SemanticError as exception:
            error_text = TypesError.ATTR_TYPE_UNDEFINED %(node.type, node.id)
            attr_type = ErrorType(node.type_pos)
            self.errors.append(TypesError(*node.type_pos, error_text))
        
        if node.id == 'self':
            error_text = SemanticError.SELF_ATTR
            self.errors.append(SemanticError(*node.pos, error_text))

        try:
            self.current_type.define_attribute(node.id, attr_type, node.pos)
        except SemanticError as exception:
            self.errors.append(exception)
