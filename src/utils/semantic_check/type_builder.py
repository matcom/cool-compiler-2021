import cmp.visitor as visitor
from utils.ast.AST_Nodes import ast_nodes as nodes
from cmp.semantic import SemanticError, ErrorType

NOT_INHERIT_FROM_BASICS_TYPES = '(%s, %s) - TypeError: Type %s cannot inherit from basic type %s'


class TypeBuilder:
    def __init__(self, context, errors):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(nodes.ProgramNode)
    def visit(self,node):
        for dec in node.declarations:
            self.visit(dec)
        return
    

    @visitor.when(nodes.ClassDeclarationNode)
    def visit(self,node):
        self.current_type = self.context.get_type(node.id)

        if node.parent is not None:

            if node.parent.lex in ['Int', 'String', 'SELF_TYPE', 'Bool']:
                self.errors.append(NOT_INHERIT_FROM_BASICS_TYPES % (node.id.line, node.id.column, node.id.lex, node.parent.lex))

            else:
                try:
                    parent_type = self.context.get_type(node.parent)
                except SemanticError as se:
                    parent_type = ErrorType()
                    self.errors.append(se.text)
                    
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError as se:
                    self.errors.append(se.text)

        elif not self.current_type.parent:
            self.current_type.set_parent(self.context.get_type('Object'))
        
        for feat in node.features:
            self.visit(feat)

        return
    

    @visitor.when(nodes.AttrDeclarationNode)
    def visit(self,node):
        try:
            attrType = self.context.get_type(node.type)
            self.current_type.define_attribute(node.id, attrType)
        except SemanticError as se:
            self.errors.append(se.text)
            self.current_type.define_attribute(node.id, ErrorType())

        return

    
    @visitor.when(nodes.MethDeclarationNode)
    def visit(self,node):
        param_names = []
        param_types = []

        for name, typex in node.params:
            param_names.append(name)

            try:
                param_types.append(self.context.get_type(typex))
            except SemanticError as se:
                self.errors.append(se.text)
                param_types.append(ErrorType())

        try:       
            returnType = self.context.get_type(node.type)
        except SemanticError as se:
            self.errors.append(se.text)
            returnType = ErrorType()
        
        try:
            self.current_type.define_method(node.id, param_names, param_types, returnType)
        except SemanticError as se:
            self.errors.append(se.text)

        return