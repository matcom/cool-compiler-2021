from __future__ import annotations

from coolcmp.utils import visitor, ast, cil
from coolcmp.utils.semantic import Context, Type


class DotTypesDataVisitor:
    """
    Builds the .TYPES and .DATA sections.
    """
    def __init__(self, context: Context):
        super().__init__()
        self.context = context
        self.current_type: Type | None = None
        self.root = cil.ProgramNode([], [], [])
        self.types = self.root.dot_types

    @visitor.on('node')
    def visit(self, node: ast.Node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        self.root.set_data('""')
        self.root.set_data('"halted\n"')

        # add Object, IO, String, Bool, Int and <void> to types
        self.types += [
            cil.TypeNode(
                name='Object',
                parent='_NoParent',
                attrs=[],
                methods={
                    'Object__init': 'Object__init',
                    'Object_abort': 'Object_abort',
                    'Object_type_name': 'Object_type_name',
                    'Object_copy': 'Object_copy',
                }
            ),
            cil.TypeNode(
                name='IO',
                parent='Object',
                attrs=[],
                methods={
                    'IO__init': 'IO__init',
                    'IO_abort': 'Object_abort',
                    'IO_type_name': 'Object_type_name',
                    'IO_copy': 'Object_copy',
                    'IO_out_string': 'IO_out_string',
                    'IO_out_int': 'IO_out_int',
                    'IO_in_string': 'IO_in_string',
                    'IO_in_int': 'IO_in_int',
                }
            ),
            cil.TypeNode(
                name='String',
                parent='Object',
                attrs=[
                    'String_value',
                ],
                methods={
                    'String__init': 'String__init',
                    'String_abort': 'Object_abort',
                    'String_type_name': 'Object_type_name',
                    'String_copy': 'Object_copy',
                    'String_length': 'String_length',
                    'String_concat': 'String_concat',
                    'String_substr': 'String_substr',
                }
            ),
            cil.TypeNode(
                name='Bool',
                parent='Object',
                attrs=[
                    'Bool_value',
                ],
                methods={
                    'Bool__init': 'Bool__init',
                    'Bool_abort': 'Object_abort',
                    'Bool_type_name': 'Object_type_name',
                    'Bool_copy': 'Object_copy',
                }
            ),
            cil.TypeNode(
                name='Int',
                parent='Object',
                attrs=[
                    'Int_value',
                ],
                methods={
                    'Int__init': 'Int__init',
                    'Int_abort': 'Object_abort',
                    'Int_type_name': 'Object_type_name',
                    'Int_copy': 'Object_copy',
                }
            ),
            cil.TypeNode(
                name='Void',
                parent='Object',
                attrs=[],
                methods={
                    'Void_init': 'Void__init',
                    'Void_abort': 'Object_abort',
                    'Void_type_name': 'Object_type_name',
                    'Void_copy': 'Object_copy',
                }
            ),
        ]

        for class_ in node.declarations:
            self.visit(class_)

        return self.root

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode):
        type_ = self.context.get_type(node.id)
        type_attributes: list[str] = []
        type_methods: dict[str, str] = {}
        type_node = cil.TypeNode(
            name=type_.name,
            parent=type_.parent.name,
            attrs=type_attributes,
            methods=type_methods
        )

        for attr, _ in type_.all_attributes():
            type_attributes.append(f'{type_.name}_{attr.name}')
            type_node.add_attr_node(f'{node.id}_{attr.name}', attr.node)

        for meth, owner in type_.all_methods():
            # if owner.name in ('Object', 'IO', 'String', 'String', 'Bool', 'Int', ):
            #     func_target = meth.name
            # else:
            type_methods[f'{node.id}_{meth.name}'] = f'{owner.name}_{meth.name}'

        self.types.append(type_node)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode):
        self.visit(node.expr)

    @visitor.when(ast.FuncDeclarationNode)
    def visit(self, node: ast.FuncDeclarationNode):
        self.visit(node.body)

    @visitor.when(ast.LetDeclarationNode)
    def visit(self, node: ast.LetDeclarationNode):
        self.visit(node.expr)

    @visitor.when(ast.ParenthesisExpr)
    def visit(self, node: ast.ParenthesisExpr):
        self.visit(node.expr)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode):
        for expr in node.expressions:
            self.visit(expr)

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.expr)

    @visitor.when(ast.CaseBranchNode)
    def visit(self, node: ast.CaseBranchNode):
        self.visit(node.expr)

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode):
        self.visit(node.expr)

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode):
        self.visit(node.expr)

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode):
        self.visit(node.if_expr)
        self.visit(node.then_expr)
        self.visit(node.else_expr)

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode):
        self.visit(node.condition)
        self.visit(node.body)

    @visitor.when(ast.CallNode)
    def visit(self, node: ast.CallNode):
        if node.obj is not None:
            self.visit(node.obj)

        for arg in node.args:
            self.visit(arg)

    @visitor.when(ast.BinaryNode)
    def visit(self, node: ast.BinaryNode):
        self.visit(node.left)
        self.visit(node.right)

    @visitor.when(ast.UnaryNode)
    def visit(self, node: ast.UnaryNode):
        self.visit(node.expr)

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode):
        self.root.set_data(node.lex)