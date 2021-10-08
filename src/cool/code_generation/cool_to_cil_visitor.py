from typing import Dict, List, Optional

import cool.code_generation.cil as cil
import cool.semantics.utils.astnodes as ast
import cool.visitor.visitor as visitor
from cool.code_generation.base import BaseCOOLToCILVisitor
from cool.semantics.utils.scope import Attribute, Context, Method, Scope, Type


class ConstructorCreator:
    def __init__(self, context: Context):
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.context: Context = context
        self.class_declarations = {}  # type: Dict[str, ast.ClassDeclarationNode]

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        declarations: List[ast.ClassDeclarationNode] = []

        for declaration in node.declarations:
            self.class_declarations[declaration.id] = declaration

        for declaration in node.declarations:
            declarations.append(self.visit(declaration, scope))

        return ast.ProgramNode(declarations)

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        ancestors = [
            self.class_declarations[owner.name]
            for _, owner in self.current_type.all_attributes()
        ]

        attrs = []
        visited = set()
        for ancestor in ancestors:
            if ancestor.id in visited:
                continue

            visited.add(ancestor.id)
            attrs += [
                feature
                for feature in ancestor.features
                if isinstance(feature, ast.AttrDeclarationNode)
            ]

        expressions: List[ast.ExprNode] = []
        for attr in attrs:
            expr = self.visit(attr, scope)

            if expr:
                expressions.append(expr)

        body = ast.BlockNode(expressions)
        constructor = ast.MethodDeclarationNode(
            "__init__", [], self.current_type.name, body
        )
        return ast.ClassDeclarationNode(
            node.id, [constructor] + node.features, node.parent
        )
    
    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode, scope: Scope):
        if node.expr is None:
            return None
        
        return ast.AssignNode(node.id, node.expr)


class CoolToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        for declaration in node.declarations:
            self.visit(declaration, scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(self.current_type.name)

        methods = [
            feature
            for feature in node.features
            if isinstance(feature, ast.MethodDeclarationNode)
        ]

        for attr, _ in self.current_type.all_attributes():
            self.visit(attr, scope)
            type_node.attributes.append(attr.name)

        for method, child_scope in zip(methods, scope.children):
            self.visit(method, child_scope)
            type_node.methods.append(
                (method.id, self.to_function_name(method.id, node.id))
            )

        self.dottypes.append(type_node)

    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode, scope: Scope):
        pass
