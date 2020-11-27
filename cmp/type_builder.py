import cmp.visitor as visitor
from cmp.ast import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from cmp.semantic import SemanticError, ErrorType, InferencerManager, AutoType


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.manager = InferencerManager(context)

    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)

        self.check_main_class()
    
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        for feat in node.features:
            self.visit(feat)
            
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):

        ## Building param-names and param-types of the method
        param_names = []
        param_types = []
        node.index = []
        for param in node.params:
            n, t = param
            param_names.append(n)
            node.index.append(None)
            try:
                t = self.context.get_type(t)
                if isinstance(t, AutoType):
                    node.index[-1] = self.manager.assign_id()
            except SemanticError as ex:
                self.errors.append(ex.text)
                t = ErrorType()
            param_types.append(t)
        
        # Checking return type
        try:
            rtype = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            rtype = ErrorType()
        
        node.idx = self.manager.assign_id() if isinstance(rtype, AutoType) else None
        
        # Defining the method in the current type. There can not be another method with the same name.
        try:
            self.current_type.define_method(node.id, param_names, param_types, rtype, node.index, node.idx)
        except SemanticError as ex:
            self.errors.append(ex.text)
            
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        # Checking attribute type
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            attr_type = ErrorType()

        node.idx = self.manager.assign_id() if isinstance(attr_type, AutoType) else None
        
        # Checking attribute name. No other attribute can have the same name
        flag = False
        try:
            self.current_type.define_attribute(node.id, attr_type, node.idx)
            flag = True
        except SemanticError as ex:
            self.errors.append(ex.text)
        
        while not flag:
            node.id = f'1{node.id}'
            try:
                self.current_type.define_attribute(node.id, attr_type, node.idx)
                flag = True
            except SemanticError:
                pass


    def check_main_class(self):
        try:
            typex = self.context.get_type('Main')
            if not any(method.name == 'main' for method in typex.methods):
                self.errors.append('Class Main must contain a method main')
        except SemanticError:
            self.errors.append('Program must contain a class Main')