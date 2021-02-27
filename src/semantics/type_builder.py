import semantics.visitor as visitor
from parsing.ast import Node, ProgramNode, ClassDeclarationNode, MethodDeclarationNode, AttrDeclarationNode
from semantics.tools import SemanticError, TypeBag
from semantics.tools import ErrorType, SelfType
from semantics.tools import Context

class TypeBuilder:
    def __init__(self, context: Context, errors):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.build_default_classes()

        for class_def in node.declarations:
            self.visit(class_def)

        try:
            self.context.get_type('Main', unpacked=True).get_method('main', local=True)
        except SemanticError as err:
            self.add_error(node, err.text)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id, unpacked=True)

        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent, unpacked=True)
                self.current_type.set_parent(parent_type)
                for idx, _ in list(parent_type.all_attributes(True)):
                    self.current_type.attributes.append(idx)
            except SemanticError as err:
                self.add_error(node, err.text)
        
        for feature in node.features:
            self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(node, err.text)
            attr_type = ErrorType()
        
        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as err:
            self.add_error(err.text)
    
    @visitor.when(MethodDeclarationNode)
    def visit(self, node):
        try:
            ret_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(err.text)
            ret_type = ErrorType()
        
        params_type = []
        params_name = []
        for var in node.params:
            p_name = var.id
            p_type = var.type
            try:
                params_type.append(self.context.get_type(p_type))
            except SemanticError as err:
                params_type.append(ErrorType())
                self.add_error(node, err.text)
            params_name.append(p_name)
        
        try:
            self.current_type.define_method(node.id, params_name, params_type, ret_type)
        except SemanticError as err:
            self.add_error(node, err.text)

    def build_default_classes(self):
        Object = self.context.get_type("Object", unpacked=True)
        String = self.context.get_type("String", unpacked=True)
        Int = self.context.get_type("Int", unpacked=True)
        Io = self.context.get_type("IO", unpacked=True)
        Bool = self.context.get_type("Bool", unpacked=True)

        String.set_parent(Object)
        Int.set_parent(Object)
        Io.set_parent(Object)
        Bool.set_parent(Object)

        p_Object = self.context.get_type("Object")
        p_String = self.context.get_type("String")
        p_Int = self.context.get_type("Int")
        p_Self = TypeBag({SelfType()})

        Object.define_method("abort", [], [], p_Object)
        Object.define_method("type_name", [], [], p_String)
        Object.define_method("copy", [], [], p_Self)

        String.define_method("length", [], [], p_Int)
        String.define_method("concat", ["s"], [p_String], p_String)
        String.define_method("substr", ["i", "l"], [p_Int, p_Int], p_String)

        Io.define_method("out_string", ["x"],[p_String], p_Self)
        Io.define_method("out_int", ["x"],[p_Int], p_Self)
        Io.define_method("in_string", [],[], p_String)
        Io.define_method("in_int", [], [], p_Int)
    
    def add_error(self, node:Node, text:str):
        line, col = node.get_position() if node else 0, 0
        self.errors.append(f"({line}, {col}) - " + text)