import cmp.visitor as visitor
from ast_nodes import (
    ProgramNode,
    ClassDeclarationNode,
    FuncDeclarationNode,
    AttrDeclarationNode,
    IfNode,
    WhileNode,
    LetNode,
    CaseNode,
    AssignNode,
    VarDeclarationNode,
    CaseItemNode,
    InstantiateNode,
    BlockNode,
    CallNode,
    BinaryNode,
    AtomicNode,
    UnaryNode,
)


class FormatVisitor(object):
    @visitor.on("node")
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__ProgramNode [<class> ... <class>]"
        statements = "\n".join(
            self.visit(child, tabs + 1) for child in node.declarations
        )
        return f"{ans}\n{statements}"

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = "" if node.parent is None else f"inherits {node.parent}"
        ans = (
            "\t" * tabs
            + f"\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}"
        )
        features = "\n".join(self.visit(child, tabs + 1) for child in node.features)
        return f"{ans}\n{features}"

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__AttrDeclarationNode: {node.id} : {node.type} <- <exp>"
        exp = "\t" * (tabs + 1) + "__NONE"
        if not node.init_exp is None:
            exp = "\n".join(self.visit(node.init_exp, tabs + 1))
        return f"{ans}\n{exp}"

    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__VarDeclarationNode: {node.id} : {node.type} <- <expr>"
        expr = "\t" * (tabs + 1) + "__NONE"
        if not node.expr is None:
            expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}"

    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__AssignNode: {node.id} <- <expr>"
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}"

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ", ".join(":".join(param) for param in node.params)
        ans = (
            "\t" * tabs
            + f"\\__FuncDeclarationNode: {node.id}({params}) : {node.type} -> <body>"
        )
        body = self.visit(node.body, tabs + 1)
        return f"{ans}\n{body}"

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__<expr> {node.__class__.__name__} <expr>"
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f"{ans}\n{left}\n{right}"

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return "\t" * tabs + f"\\__ {node.__class__.__name__}: {node.lex}"

    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        class_name = node.__class__.__name__.split("Node")[0]
        ans = "\t" * tabs + f"\\__ {node.__class__.__name__}: {class_name} <exp>"
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}"

    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        args = "\n".join(self.visit(arg, tabs + 1) for arg in node.args)
        if not node.obj is None:
            obj = self.visit(node.obj, tabs + 1)
            if not node.at_type is None:
                ans = (
                    "\t" * tabs
                    + f"\\__CallNode: <obj>@{node.at_type}.{node.id}(<expr>, ..., <expr>)"
                )
            else:
                ans = (
                    "\t" * tabs + f"\\__CallNode: <obj>.{node.id}(<expr>, ..., <expr>)"
                )
            return f"{ans}\n{obj}\n{args}"
        else:
            ans = "\t" * tabs + f"\\__CallNode: {node.id}(<expr>, ..., <expr>)"
            return f"{ans}\n{args}"

    @visitor.when(InstantiateNode)
    def visit(self, node, tabs=0):
        return "\t" * tabs + f"\\__ InstantiateNode: new {node.lex}()"

    @visitor.when(BlockNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__BlockNode: {{<exp>; ... <exp>;}}"
        body = "\n".join(self.visit(child, tabs + 1) for child in node.expresion_list)
        return f"{ans}\n{body}"

    @visitor.when(IfNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__IfNode: if <expr> then <expr> else <exp> fi"
        if_expr = self.visit(node.if_expr, tabs + 1)
        then_expr = self.visit(node.then_expr, tabs + 1)
        else_expr = self.visit(node.else_expr, tabs + 1)
        return f"{ans}\n{if_expr}\n{then_expr}\n{else_expr}"

    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__WhileNode: while <expr> loop <expr> pool"
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f"{ans}\n{condition}\n{body}"

    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__LetNode: let <identif-list> in <expr>"
        ident_list = "\n".join(
            self.visit(child, tabs + 1) for child in node.identifiers
        )
        body = self.visit(node.body, tabs + 1)
        return f"{ans}\n{ident_list}\n{body}"

    @visitor.when(CaseNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__LetNode: case <expr> of <case_block> esac"
        case_block = "\n".join(self.visit(child, tabs + 1) for child in node.case_items)
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}\n{case_block}"

    @visitor.when(CaseItemNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__CaseItemNode: {node.id} : {node.type} => <exp>;"
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}"

