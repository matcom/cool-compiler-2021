from semantic.tools.context import Context
from semantic.tools.error import SemanticError, SemanticException
from nodes import ProgramNode, ClassNode
from semantic.visitor import visitor

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.context.create_builtin_types()
        for dec in node.classes:
            if dec.name in ['Object', 'Int', 'String', 'Bool', 'IO']:
                error = SemanticError("Is an error redefine a builint type", dec.row, dec.col)
                self.errors.append(error)
            else:
                self.visit(dec)

    @visitor.when(ClassNode)
    def visit(self, node):
        try:
            self.context.create_type(node)
        except SemanticException as e:
            error = SemanticError(e.text, node.row, node.col)
            self.errors.append(error)
