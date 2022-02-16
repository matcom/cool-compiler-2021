from core.tools import visitor
from core.tools.Semantic import *
from core.parser.Parser import ProgramNode, ClassDeclarationNode
from core.tools.Errors import SemanticError

# Visitor encargado de coleccionar los nombres de las clases que se definen
# en el codigo del programa COOL, chequea ademas que no se redeclaren e
# incluye los tipos builtin dentro del contexto

class Type_Collector:
    def __init__(self):
        self.errors = []

        self.Context = Context()

        self.Context.add_type(SelfType())

        self.Context.create_type('Object', 0, 0)
        self.Context.create_type('String', 0, 0)
        self.Context.create_type('IO', 0, 0)
        self.Context.create_type('Int', 0, 0)
        self.Context.create_type('Bool', 0, 0)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        for type in node.declarations:
            self.visit(type)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node : ClassDeclarationNode):
        try:
            self.Context.create_type(node.id.lex, node.line, node.column)
        except SemanticException as ex:
            self.errors.append(SemanticError(node.line, node.column, ex.text))
