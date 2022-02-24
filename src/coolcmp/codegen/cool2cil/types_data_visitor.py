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
        self.root.set_data('"Object"')
        self.root.set_data('"IO"')
        self.root.set_data('"String"')
        self.root.set_data('"Bool"')
        self.root.set_data('"Int"')
        self.root.set_data('"<void>"')

        # add Object, IO, String, Bool, Int and <void> to types
        self.types += [
            cil.TypeNode(
                name='Object',
                attrs=[
                    'Object__name',
                ],
                methods=[
                    'Object_abort',
                    'Object_type_name',
                    'Object_copy',
                ],
                attr_expr_nodes={
                    'Object__name': ast.StringNode('"Object"')
                }
            ),
            cil.TypeNode(
                name='IO',
                attrs=[
                    'IO__name',
                ],
                methods=[
                    'IO_out_string',
                    'Object_out_int',
                    'Object_in_string',
                    'IO_in_string',
                ],
                attr_expr_nodes={
                    'IO__name': ast.StringNode('"IO"')
                }
            ),
            cil.TypeNode(
                name='String',
                attrs=[
                    'String__name',
                    'value',
                ],
                methods=[
                    'String_length',
                    'String_concat',
                    'String_substr',
                ],
                attr_expr_nodes={
                    'String__name': ast.StringNode('"String"')
                }
            ),
            cil.TypeNode(
                name='Bool',
                attrs=[
                    'Bool__name',
                    'value',
                ],
                methods=[],
                attr_expr_nodes={
                    'Bool__name': ast.StringNode('"Bool"')
                }
            ),
            cil.TypeNode(
                name='Int',
                attrs=[
                    'Int__name',
                    'value',
                ],
                methods=[],
                attr_expr_nodes={
                    'Int__name': ast.StringNode('"Int"')
                }
            ),
            cil.TypeNode(
                name='Void',
                attrs=[
                    'Void__name',
                ],
                methods=[],
                attr_expr_nodes={
                    'Void__name': ast.StringNode('"<void>"')
                }
            ),
        ]

        for class_ in node.declarations:
            self.visit(class_)

        return self.root

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode):
        type_ = self.context.get_type(node.id)
        type_attributes: list[str] = [f'{node.id}__name']
        type_methods: list[str] = []
        type_node = cil.TypeNode(
            name=type_.name,
            attrs=type_attributes,
            methods=type_methods,
            attr_expr_nodes={
                f'{node.id}__name': ast.StringNode(f'"{node.id}"')
            }
        )
        self.root.set_data(f'"{node.id}"')

        for attr, _ in type_.all_attributes():
            type_attributes.append(f'{type_.name}_{attr.name}')
            type_node.add_attr_node(f'{node.id}_{attr.name}', attr.node)

        for meth, owner in type_.all_methods():
            # if owner.name in ('Object', 'IO', 'String', 'String', 'Bool', 'Int', ):
            #     func_target = meth.name
            # else:
            type_methods.append(f'{node.id}_{meth.name}')

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
