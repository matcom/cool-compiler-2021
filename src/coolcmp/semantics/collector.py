from __future__ import annotations

from coolcmp import errors as err
from coolcmp.utils import visitor
from coolcmp.utils.ast import ProgramNode, ClassDeclarationNode
from coolcmp.utils.semantic import Context, SemanticError, IntType, VoidType, ErrorType


class TypeCollector(object):
    def __init__(self):
        self.context: Context | None = None
        self.errors: list[str] = []

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()

        # Default types definition
        self.context.types['<error>'] = ErrorType()
        void = self.context.types['<void>'] = VoidType()
        self_ = self.context.create_type('SELF_TYPE')
        object_ = self.context.create_type('Object')
        io = self.context.create_type('IO')
        string = self.context.create_type('String')
        int_ = self.context.types['Int'] = IntType()
        bool_ = self.context.create_type('Bool')

        # Default types inheritance
        void.set_parent(object_)
        io.set_parent(object_)
        string.set_parent(object_)
        int_.set_parent(object_)
        bool_.set_parent(object_)

        # Default types attributes
        object_.define_attribute('void', void)

        # Default types methods
        object_.define_method('abort', [], [], object_)
        object_.define_method('type_name', [], [], string)
        object_.define_method('copy', [], [], self_)

        io.define_method('out_string', ['x'], [string], self_)
        io.define_method('out_int', ['x'], [int_], self_)
        io.define_method('in_string', [], [], string)
        io.define_method('in_int', [], [], int_)

        string.define_method('length', [], [], int_)
        string.define_method('concat', ['s'], [string], string)
        string.define_method('substr', ['i', 'l'], [int_, int_], string)

        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        try:
            self.context.create_type(node.id)
        except SemanticError:
            self.errors.append(err.TYPE_ALREADY_DEFINED % (node.pos, node.id))
