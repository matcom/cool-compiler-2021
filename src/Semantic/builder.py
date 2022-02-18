from Tools import *
from Parser.ast import *

class TypeBuilder:
    def __init__(self, context, errors):
        self.errors = errors
        self.context = context

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.object_type = self.context.types['Object']
        
        for def_class in node.class_list:
            self.visit(def_class)

    @visitor.when(ClassNode)
    def visit(self, node):
        self.current_type = self.context.types[node.type.value]

        if node.parent:
            try: 
                self.current_type.set_parent(self.context.get_type(node.parent.value))
            except SemanticException as error:
                self.errors.append(SemanticErrors(node.parent.line, node.parent.column, error))
            except KeyError:
                self.errors.append(TypeErrors(node.parent.line, node.parent.column, f'Class {node.type.value} inherits from an undefined class {node.parent.value}.'))
        else:
            self.current_type.set_parent(self.object_type)

        for feature in node.feature_list:
            self.visit(feature)

        if self.current_type.name == 'Main':
            try:
                self.current_type.get_method('main')
            except MethodException:
                self.errors.append(SemanticErrors(node.type.line, node.type.column, 'No "main" method in class Main.'))


    @visitor.when(AttributeNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type.value)
        except KeyError:
            self.errors.append(TypeErrors(node.type.line, node.type.column, f'Class {node.type.value} of attribute {node.id.value} is undefined.'))
            attr_type = ErrorType()
        try:
            self.current_type.define_attribute(node.id.value, attr_type, node.expr)
        except AttributeException as error:
            self.errors.append(SemanticErrors(node.id.line, node.id.column, error))

    @visitor.when(MethodNode)
    def visit(self, node):
        param_names = [] 
        param_types = []
        for id, type in node.params:
            try:
                if id.value == 'self':
                    self.errors.append(SemanticErrors(id.line, id.column, f'\'self\' cannot be the name of a formal parameter.'))
                    param_type = ErrorType()
                if type.value == 'SELF_TYPE':
                    param_type = self.current_type
                else:
                    param_type = self.context.get_type(type.value)
            except KeyError:
                self.errors.append(TypeErrors(type.line, type.column, f'Class {type.value} of formal parameter {id.value} is undefined.'))
                param_type = ErrorType()         
            
            if id.value in param_names:
                self.errors.append(SemanticErrors(id.line, id.column, f'Formal parameter {id.value} is multiply defined.'))
            else:
                param_names.append(id.value)
                param_types.append(param_type)
        
        try:
            method = self.current_type.parent.get_method(node.id.value)
            param_parent_names = method.param_names
            param_paren_types = method.param_types

            if len(param_names) != len(param_parent_names):
                self.errors.append(SemanticErrors(node.id.line, node.id.column, f'Incompatible number of formal parameters in redefined method {node.id.value}'))
            else:    
                for (cid, ctype), pid, ptype in zip(node.params, param_parent_names, param_paren_types):
                    if cid.value == pid:
                        if not self.context.get_type(ctype.value).conforms_to(ptype):
                            self.errors.append(SemanticErrors(cid.line, cid.column, f'In redefined method {node.id.value}, parameter type {ctype.value} is different from original type {ptype.name}.'))
                    
                if not self.context.get_type(node.type.value).conforms_to(method.return_type):
                    self.errors.append(SemanticErrors(node.type.line, node.type.column, f'In redefined method {node.id.value}, return type {node.type.value} is different from original return type {method.return_type.name}.'))
        except:
            pass

        try:
            if node.type.value == 'SELF_TYPE':
                ret_type = self.current_type
            else:
                ret_type = self.context.get_type(node.type.value)
        except KeyError:
            self.errors.append(TypeErrors(node.type.line, node.type.column, f'Undefined return type {node.type.value} in method {node.id.value}.'))
            ret_type = ErrorType()

        try:
            self.current_type.define_method(node.id.value, param_names, param_types, ret_type)
        except MethodException as error:
            self.errors.append(SemanticErrors(node.id.line, node.id.column, error))
