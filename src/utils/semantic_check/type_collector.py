import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError

NOT_REDEFINE_BASIC_TYPES = '(%s, %s) - SemanticError: Redefinition of basic class %s.'
NOT_REDEFINE_CLASSES = '(%s, %s) - SemanticError: Classes may not be redefined'

class TypeCollector(object):
    def __init__(self, context, errors):
        self.context = context
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(nodes.ProgramNode)
    def visit(self, node):

        # añadimos algunos tipos predeterminados
        object_type = self.context.create_type('Object')
        self_type = self.context.create_type('SELF_TYPE')
        int_type = self.context.create_type('Int')
        string_type = self.context.create_type('String')
        bool_type = self.context.create_type('Bool')
        io_type = self.context.create_type('IO')

        # todos heredan de Object
        int_type.set_parent(object_type)
        string_type.set_parent(object_type)
        bool_type.set_parent(object_type)
        io_type.set_parent(object_type)

        # agregar los metodos a los tipos basicos
        object_type.define_method('abort', [], [], object_type) 
        object_type.define_method('type_name', [], [], string_type) 
        object_type.define_method('copy', [], [], self_type) 

        io_type.define_method('out_string', ['x'], [string_type], self_type) 
        io_type.define_method('out_int', ['x'], [int_type], self_type) 
        io_type.define_method('in_string', [], [], string_type) 
        io_type.define_method('in_int', [], [], int_type) 

        string_type.define_method('length', [], [], int_type) 
        string_type.define_method('concat', ['s'], [string_type], string_type) 
        string_type.define_method('substr', ['i', 'l'], [int_type, int_type], string_type) 

        for dec in node.declarations:
            self.visit(dec)
        return
    

    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self,node):
        try:
            if node.id in ["Object", "Int", "String", "Bool", "IO"]:
                self.errors.append(NOT_REDEFINE_BASIC_TYPES % (node.line, node.column, node.id))
                node.id = 'error_type'
            typex = self.context.create_type(node.id)
            typex.line = node.line
            typex.column = node.column
        except SemanticError as se:
            self.errors.append(NOT_REDEFINE_CLASSES % (node.classt_line, node.classt_column))
        return