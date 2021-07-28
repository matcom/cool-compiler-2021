from typing import List
from cool.code_generation.cil import PlusNode

import cool.semantics.utils.astnodes as ast
import cool.visitor as visitor
from pyjapt import Token


class PositionAssigner:
    def __init__(self, tokens: List[Token]):
        self.position = 0
        self.tokens = tokens

    def inc_position(self, count: int = 1):
        self.position += count

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):

        for declaration in node.declarations:
            self.visit(declaration)
            self.inc_position()

        first_declaration = node.declarations[
            0
        ]  # There is always one or more declarations
        node.set_main_position(first_declaration.line, first_declaration.column)

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode):
        """
          *
        class type [inherits type] { feature-list }
        """
        token = self.tokens[self.position]
        assert (
            token.lex == "class"
        ), f'Expected "class" instead of "{token.lex}" in {node.id}'

        token = self.tokens[self.position + 1]
        node.set_main_position(token.line, token.column)

        if node.parent is not None:
            token = self.tokens[self.position + 3]
            node.parent_position = token.line, token.column

        count = 3 if node.parent is None else 5
        self.inc_position(count)

        for feature in node.features:
            self.visit(feature)

            token = self.tokens[self.position]
            assert (
                token.lex == ";"
            ), f'Expected ";" instead of "{token.lex}" in {feature.id} of class {node.id}'

            self.inc_position()  # ends after `;`

        self.inc_position()  # ends after `}`

    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode):
        """
        *
        id : type [<- expr]
        """
        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        token = self.tokens[self.position + 2]
        node.type_position = token.line, token.column

        if node.expr is not None:
            self.inc_position(4)  # ends after `<-`

            token = self.tokens[self.position]
            node.expr_position = token.line, token.column

            self.visit(node.expr)

            token = self.tokens[self.position]
            return

        self.inc_position(3)

    @visitor.when(ast.MethodDeclarationNode)
    def visit(self, node: ast.MethodDeclarationNode):
        """
        *
        id ( [params] ) : type { expr }
        """
        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        self.inc_position(2)  # ends after `(`

        for i, _ in enumerate(node.params):
            # *
            # id : type ,
            self.inc_position(2)  # ends in `type`

            token = self.tokens[self.position]
            node.param_types_positions.append((token.line, token.column))

            self.inc_position()  # ends in `,`

            if i < len(node.params) - 1:
                self.inc_position()  # ends in `,`
        # ends in `)`

        self.inc_position(2)  # ends in `type`
        token = self.tokens[self.position]
        node.return_type_position = token.line, token.column
        self.inc_position(2)  # ends after `{`

        self.visit(node.body)
        self.inc_position()  # ends after `}`

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode):
        """
        *
        let declaration-list in expr
        """
        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        self.inc_position()

        for _, _, expr in node.declarations:
            # *
            # id : type [<- expr] ,

            token = self.tokens[self.position]
            node.declaration_names_positions.append((token.line, token.column))

            token = self.tokens[self.position + 2]
            node.declaration_types_positions.append((token.line, token.column))

            if expr is not None:
                self.inc_position(4)  # ends after `<-`

                token = self.tokens[self.position]
                self.visit(expr)
                self.inc_position()  # ends after `,`
            else:
                self.inc_position(4)  # ends after `,` or `in` if last
        # ends after `in`

        self.visit(node.expr)

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode):
        """
        *
        id <- expr
        """

        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        token = self.tokens[self.position + 1]
        assert token.lex == "<-", f'Expected "<-" instead of "{token.lex}" in assign'

        self.inc_position(2)  # ends after `<-`
        self.visit(node.expr)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode):
        """
        *
        { block }
        """
        token = self.tokens[self.position]
        assert token.lex == "{", f'Expected "{{" instead of "{token.lex}" in block'

        node.set_main_position(token.line, token.column)
        self.inc_position()  # edns after `{`

        for i, expr in enumerate(node.expressions, start=1):
            # *
            # expr ;
            self.visit(expr)

            token = self.tokens[self.position]
            assert (
                token.lex == ";"
            ), f'Expected ";" instead of "{token.lex}" in instruction {i} of a block'

            self.inc_position()  # ends after `;`

        token = self.tokens[self.position]
        assert (
            token.lex == "}"
        ), f'Expected "}}" instead of "{token.lex}" at the end of a block'

        self.inc_position()  # ends after `}`

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode):
        """
        *
        if expr then expr else expr fi
        """

        token = self.tokens[self.position]
        assert (
            token.lex == "if"
        ), f'Expected "if" instead of "{token.lex}" in conditional'
        node.set_main_position(token.line, token.column)
        self.inc_position()  # ends after `if`
        self.visit(node.if_expr)

        token = self.tokens[self.position]
        assert (
            token.lex == "then"
        ), f'Expected "then" instead of "{token.lex}" in conditional'
        self.inc_position()  # ends after `then`
        self.visit(node.then_expr)

        token = self.tokens[self.position]
        assert (
            token.lex == "else"
        ), f'Expected "else" instead of "{token.lex}" in conditional'
        self.inc_position()  # ends after `else`
        self.visit(node.else_expr)

        token = self.tokens[self.position]
        assert (
            token.lex == "fi"
        ), f'Expected "fi" instead of "{token.lex}" in conditional'
        self.inc_position()  # ends after `fi`

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode):
        """
        *
        while expr loop expr pool
        """

        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        self.inc_position()  # ends after `while`
        self.visit(node.condition)

        self.inc_position()  # ends after `loop`
        self.visit(node.body)

        self.inc_position()  # ends after `pool`

    @visitor.when(ast.SwitchCaseNode)
    def visit(self, node: ast.SwitchCaseNode):
        """
        *
        case expr of case-list esac
        """

        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        self.inc_position()  # ends afte `case`
        self.visit(node.expr)

        self.inc_position()  # ends after `of`
        for _, _, expr in node.cases:
            # *
            # id : type => expr ;
            self.inc_position(2)  # ends in `type`

            token = self.tokens[self.position]
            node.cases_positions.append((token.line, token.column))

            self.inc_position(2)  # ends after `=>`
            self.visit(expr)
            self.inc_position()  # ends after `;`

        self.inc_position()  # ends afte `esac`

    @visitor.when(ast.MethodCallNode)
    def visit(self, node: ast.MethodCallNode):
        """
        *
        id ( expr-list )
        atom . id ( expr-list )
        atom @ type . id ( expr-list )
        """

        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)
        node.id_position = token.line, token.column

        obj_not_none = node.obj is not None
        type_not_none = node.type is not None

        if obj_not_none:
            self.visit(node.obj)

            token = self.tokens[self.position]
            assert token.lex in (
                ".",
                "@",
            ), f"Expected '.' or '@' instead of {token.lex}"

            self.inc_position()  # ends after `.` or `@`
            token = self.tokens[self.position]
            node.id_position = token.line, token.column

        if type_not_none:
            token = self.tokens[self.position]
            node.type_position = token.line, token.column

            self.inc_position(2)  # ends after `.`
            token = self.tokens[self.position]
            node.id_position = token.line, token.column

        self.inc_position(2)  # ends after `(`

        token = self.tokens[self.position]
        if node.args:
            for arg in node.args:
                # *
                # expr , expr-list
                token = self.tokens[self.position]
                node.args_positions.append((token.line, token.column))

                self.visit(arg)

                token = self.tokens[self.position]
                assert token.lex in (
                    "," ")"
                ), f"Expected ',' or ')' instead of {token.lex}"

                self.inc_position()  # ends after `,` or `)`
            # ends after `)`
        else:
            self.inc_position()

    @visitor.when(ast.IntegerNode)
    def visit(self, node: ast.IntegerNode):
        self._atom_node(node)

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode):
        self._atom_node(node)

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode):
        self._atom_node(node)

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode):
        self._atom_node(node)

    @visitor.when(ast.InstantiateNode)
    def visit(self, node: ast.InstantiateNode):
        """
        *
        new type
        """
        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)

        token = self.tokens[self.position + 1]
        node.type_position = token.line, token.column
        self.inc_position(2)  # ends after `type`

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode):
        self._check_unary_operation(node)

    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode):
        self._check_unary_operation(node)

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode):
        self._check_unary_operation(node)

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode):
        self._check_binary_operation(node)

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode):
        self._check_binary_operation(node)

    @visitor.when(ast.StarNode)
    def visit(self, node: ast.StarNode):
        self._check_binary_operation(node)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode):
        self._check_binary_operation(node)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode):
        self._check_binary_operation(node)

    @visitor.when(ast.LessThanNode)
    def visit(self, node: ast.LessThanNode):
        self._check_binary_operation(node)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode):
        self._check_binary_operation(node)

    def _check_binary_operation(self, node: ast.BinaryNode):
        """
        expr operation expr
        """
        self.visit(node.left)

        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)
        self.inc_position()  # ends after `operation`

        self.visit(node.right)

    def _check_unary_operation(self, node: ast.UnaryNode):
        """
        operation expr
        """
        token = self.tokens[self.position]
        node.operation_position = token.line, token.column

        token = self.tokens[self.position + 1]
        node.set_main_position(token.line, token.column)

        self.inc_position()  # ends after `operation`
        self.visit(node.expr)

    def _atom_node(self, node: ast.Node):
        token = self.tokens[self.position]
        node.set_main_position(token.line, token.column)
        self.inc_position()  # ends after `atom`
