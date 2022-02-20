from __future__ import annotations

from coolcmp.codegen.cool2cil import CILVisitor
from coolcmp.utils import visitor, ast, cil
from coolcmp.utils.semantic import Context, Type


class DotTypesDataVisitor(CILVisitor):
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
        for class_ in node.declarations:
            self.visit(class_)

        return self.root

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode):
        type_ = self.context.get_type(node.id)
        type_attributes: list[str] = []
        type_methods: dict[str, str] = {}

        for attr, _ in type_.all_attributes():
            type_attributes.append(f'{type_.name}_{attr.name}')

        for meth, owner in type_.all_methods():
            if owner.name in ('Object', 'IO', 'String', ):
                func_target = meth.name
            else:
                func_target = f'f{self.next_function_id}'
            type_methods[f'{node.id}_{meth.name}'] = func_target

        type_node = cil.TypeNode(type_.name, type_attributes, type_methods)
        self.types.append(type_node)

        for feature in node.features:
            if isinstance(feature, ast.AttrDeclarationNode):
                type_node.add_attr_node(f'{node.id}_{feature.id}', feature.expr)
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
