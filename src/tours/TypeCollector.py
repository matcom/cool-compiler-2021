from parsing.ast import *
from cmp.semantic import SemanticError, Context
from cmp.semantic import ObjectType, StringType, IntType, BoolType, IOType, SelfType
import cmp.visitor as visitor 
from .utils import is_base_class


BASIC_CLASS_REDEFINED = "SemanticError: Redefinition of basic class %s."
CLASS_REDEFINED = "SemanticError: Classes may not be redefined"
MAIN_NOT_DEFINED = "SemanticError: Class Main must be defined."


class TypeCollector(object):
    def __init__(self):
        self.context = None
        self.errors = []  
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        
        # Define base classes and their methods
        define_base_classes(self.context)

        for dec in node.declarations:
            self.visit(dec)

        # Check that class Main is defined
        try:
            self.context.get_type('Main')
        except SemanticError:
            self.errors.append(MAIN_NOT_DEFINED)
        
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.get_type(node.id)
            if is_base_class(node.id):
                e = BASIC_CLASS_REDEFINED.replace('%s', node.id, 1)
                self.errors.append(f"{node.location} - {e}")
            else:
                self.errors.append(f'{node.id_location} - {CLASS_REDEFINED}')
        except SemanticError:
            self.context.create_type(node.id)


def define_base_classes(context):
    object_type = context.types['Object'] = ObjectType()
    io_type = context.types['IO'] = IOType()
    int_type = context.types['Int'] = IntType()
    string_type = context.types['String'] = StringType()
    bool_type = context.types['Bool'] = BoolType()
    self_type = context.types['SELF_TYPE'] = SelfType()
    
    object_type.define_method('abort', [], [], object_type)
    object_type.define_method('type_name', [], [], string_type)
    object_type.define_method('copy', [], [], self_type)

    int_type.set_parent(object_type)

    string_type.set_parent(object_type)
    string_type.define_method('length', [], [], int_type)
    string_type.define_method('concat', ['s'], [string_type], string_type)
    string_type.define_method('substr', ['i', 'l'], [int_type, int_type], string_type)

    bool_type.set_parent(object_type)

    io_type.set_parent(object_type)
    io_type.define_method('out_string', ['x'], [string_type], self_type)
    io_type.define_method('out_int', ['x'], [int_type], self_type)
    io_type.define_method('in_string', [], [], string_type)
    io_type.define_method('in_int', [], [], int_type)
