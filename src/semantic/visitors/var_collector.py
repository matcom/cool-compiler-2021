from utils.ast import *
from utils import visitor
from utils.errors import *
from semantic.tools import *
from semantic.types import *

class VarCollector:

    def __init__(self, context=Context, errors=[]):
        self.context = context
        self.errors = errors
        self.current_type = None

    @visitor.on('node')
    def visit(self, node:Node, scope:Scope):
        pass

    @visit.when('ProgramNode')
    def visit(self, node:ProgramNode, scope:Scope):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as exception:
            self.errors.append(exception)
            raise ErrorNode()

    @visit.when('ClassDeclarationNode')
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self._get_type(node.id, node.pos)
        scope.define_variable('self', self.current_type)

        for feature in self.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)

        for attr,_ in self.current_type.all_attributes():
            if scope.find_attributes(attr.name) is None:
                scope.define_attribute(attr)

        for feature in self.features:
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, scope)

    @visit.when('AttrDeclarationNode')
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        attr = self.current_type.get_attribute(node.id, node.pos)
        if node.expr is None:
            self._define_default_variable(attr.type, node)
        else:
            self.visit(node.expr, scope)
        attr.expr = node.expr
        scope.define_attribute(attr)

    def _define_default_variable(self, typex, node):
        if typex == IntType():
            node.expr = ConstantNumNode(0)
        elif typex == StringNode():
            node.expr = ConstantStrNode('')
        elif typex == BoolType():
            node.expr = ConstantBoolNode('false')
        else:
            node.expr = ConstantVoidNode(node.id)
