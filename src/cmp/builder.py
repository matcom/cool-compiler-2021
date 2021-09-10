import cmp.visitor as visitor

from cmp.semantic import ErrorType
from cmp.ast import ProgramNode, ClassNode, AttributeNode, MethodNode
from cmp.errors import SemanticError, TypesError, ParamError

class TypeBuilder(object):
    def __init__(self, context, errors=[]):
        object.__init__(self)
        self.errors = errors
        self.context = context
        self.current_type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for def_class in node.class_list:
            self.visit(def_class)

    @visitor.when(ClassNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.type.value)

        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent.value)
                if parent_type.name in ['Bool', 'Int', 'String']:
                    self.errors.append(SemanticError.set_error(node.parent.line, node.parent.column, f'Class {node.type.value} cannot inherit class {parent_type.name}.'))
                else:
                    self.current_type.set_parent(parent_type)
            except SemanticError:
                self.errors.append(TypesError.set_error(node.parent.line, node.parent.column, f'Class {node.type.value} inherits from an undefined class {node.parent.value}.'))
        elif self.current_type != self.context.get_type('Object'):
            self.current_type.set_parent(self.context.get_type('Object'))

        for feature in node.feature_list:
            self.visit(feature)

    @visitor.when(AttributeNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type.value)
        except SemanticError:
            self.errors.append(TypesError.set_error(node.type.line, node.type.column, f'Class {node.type.value} of attribute {node.id.value} is undefined.'))
            attr_type = ErrorType()

        try:
            self.current_type.define_attribute(node.id.value, attr_type, node.expression)
        except SemanticError as err:
            self.errors.append(SemanticError.set_error(node.id.line, node.id.column, err.text))

    @visitor.when(MethodNode)
    def visit(self, node):

        param_names, param_types = [], []

        for iid, ttype in node.parameter_list:
            try:
                if iid.value == 'self':
                    raise ParamError(f'\'self\' cannot be the name of a formal parameter.')
                if ttype.value == 'SELF_TYPE':
                    param_type = self.current_type
                else:
                    param_type = self.context.get_type(ttype.value)
            except SemanticError:
                self.errors.append(TypesError.set_error(ttype.line, ttype.column, f'Class {ttype.value} of formal parameter {iid.value} is undefined.'))
                param_type = ErrorType()
            except ParamError as err:
                self.errors.append(SemanticError.set_error(iid.line, iid.column, err.text))
                param_type = ErrorType()
            
            if iid.value in param_names:
                self.errors.append(SemanticError.set_error(iid.line, iid.column, f'Formal parameter {iid.value} is multiply defined.'))
            else:
                param_names.append(iid.value)
                param_types.append(param_type)
        
        try:
            method = self.current_type.parent.get_method(node.id.value)
            param_parent_names = method.param_names
            param_paren_types = method.param_types

            if len(param_names) != len(param_parent_names):
                raise ParamError(f'Incompatible number of formal parameters in redefined method {node.id.value}')
            
            for (cid, ctype), pid, ptype in zip(node.parameter_list, param_parent_names, param_paren_types):
                if cid.value == pid:
                    if not self.context.get_type(ctype.value).conforms_to(ptype):
                        self.errors.append(SemanticError.set_error(cid.line, cid.column, f'In redefined method {node.id.value}, parameter type {ctype.value} is different from original type {ptype.name}.'))
            
            if not self.context.get_type(node.type.value).conforms_to(method.return_type):
                self.errors.append(SemanticError.set_error(node.type.line, node.type.column, f'In redefined method {node.id.value}, return type {node.type.value} is different from original return type {method.return_type.name}.'))
        
        except ParamError as err:
            self.errors.append(SemanticError.set_error(node.id.line, node.id.column, err.text))
        except:
            pass

        try:
            if node.type.value == 'SELF_TYPE':
                ret_type = self.current_type
            else:
                ret_type = self.context.get_type(node.type.value)
        except SemanticError:
            self.errors.append(TypesError.set_error(node.type.line, node.type.column, f'Undefined return type {node.type.value} in method {node.id.value}.'))
            ret_type = ErrorType()

        try:
            self.current_type.define_method(node.id.value, param_names, param_types, ret_type)
        except SemanticError as err:
            self.errors.append(SemanticError.set_error(node.id.line, node.id.column, err.text))
        