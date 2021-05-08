import cmp.visitor as visitor

from cmp.ast import ProgramNode, ClassNode
from cmp.semantic import Context
from cmp.errors import SemanticError, TypesError
from cmp.token import Token

class TypeCollector(object):
    def __init__(self, errors=[]):
        object.__init__(self)
        self.context = None
        self.errors = errors
        self.type_level = {}

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()

        for def_class in node.class_list:
            self.visit(def_class)

        def get_type_level(typex):
            try:
                parent = self.type_level[typex.value]
            except KeyError:
                return 0

            if parent == 0:
                self.errors.append(SemanticError.set_error(typex.line, typex.column, 'Class %s, or an ancestor of %s, is involved in an inheritance cycle.'%(typex.value, typex.value)))
            elif type(parent) is not int:
                self.type_level[typex.value] = 0 if parent else 1
                if type(parent) is Token:
                    self.type_level[typex.value] = get_type_level(parent) + 1
            return self.type_level[typex.value]
        
        node.class_list.sort(key = lambda node: get_type_level(node.type))

    @visitor.when(ClassNode)
    def visit(self, node):
        try:
            self.context.create_type(node.type.value)
            self.type_level[node.type.value] = node.parent
        except SemanticError as err:
            self.errors.append(SemanticError.set_error(node.type.line, node.type.column, err.text))