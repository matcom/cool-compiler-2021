import utils.visitor as visitor
from ast_hierarchy import *
from utils.semantic import SemanticError, BasicTypes


class TypeBuilder:
    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)
        try:
            main_type = self.context.get_type('Main')
            try:
                main_type.get_method('main')
            except SemanticError as error:
                self.errors.append(f'(Line {node.lineno}) {error.text}')
        except SemanticError as error:
            self.errors.append(f'(Line {node.lineno}) {error.text}')

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.id)
        except SemanticError as error:
            # it should be registered in type_collector
            self.errors.append(f'(Line {node.lineno}) {error.text}')
            return

        if node.parent is not None:
            try:
                parent_type = self.context.get_type(node.parent)

                if parent_type.name in [BasicTypes.BOOL.value, BasicTypes.STRING.value, BasicTypes.INT.value]:
                    self.errors.append(f'(Line {node.lineno}) No class can inherit from "Bool", "String" or "Int"')

                current = parent_type
                while True:
                    if current.name == node.id:
                        self.errors.append(
                            f'(Line {node.lineno}) Cyclic inheritance between classes "{node.id}" and "{node.parent}".'
                        )
                        parent_type = self.context.get_type(BasicTypes.OBJECT.value)
                        break
                    if current.name == BasicTypes.OBJECT.value:
                        break
                    current = current.parent
            except SemanticError as error:
                self.errors.append(f'(Line {node.lineno}) {error.text}')
                parent_type = self.context.get_type(BasicTypes.ERROR.value)
                node.parent = BasicTypes.ERROR.value
            self.current_type.set_parent(parent_type)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            typex = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(f'(Line {node.lineno}) {error.text}')
            typex = self.context.get_type(BasicTypes.ERROR.value)
            node.type = BasicTypes.OBJECT.value

        try:
            self.current_type.define_attribute(node.id, typex)
        except SemanticError as error:
            self.errors.append(f'(Line {node.lineno}) {error.text}')

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        param_names = []
        param_types = []

        for param in node.params:
            param_names.append(param[0])
            try:
                typex = self.context.get_type(param[1])
            except SemanticError as error:
                self.errors.append(f'(Line {node.lineno}) {error.text}')
                typex = self.context.get_type(BasicTypes.ERROR.value)
            param_types.append(typex)

        try:
            typex = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(f'(Line {node.lineno}) {error.text}')
            typex = self.context.get_type(BasicTypes.ERROR.value)

        try:
            self.current_type.define_method(node.id, param_names, param_types, typex)
        except SemanticError as error:
            self.errors.append(f'(Line {node.lineno}) {error.text}')
