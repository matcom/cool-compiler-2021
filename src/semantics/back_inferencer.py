from ast.inferencer_ast import (
    ClassDeclarationNode,
    ProgramNode,
    AttrDeclarationNode,
    Node,
)
from semantics.tools import Context, Scope, try_conform
import semantics.visitor as visitor

# Reducir los AUTO_TYPE declarados a base de el tipo de sus expresiones:

# No te debe hacer falta tirar ningun metodo nuevo, es solo ensamblar.

# Si te hace falta algo en tools.py al final hay varios metodos para trabajar con
# tipos, si no entiendes me escribes o me llamas. Si crees que te hace falta realizar
# una operacion que esos metodos no satisfacen la annades al repertorio, pero avisame
# tambien xq puede estar tirado por una esquina algo que haga algo parecido


class BackInferencer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.current_type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ProgramNode:
        scope: Scope = node.scope
        new_declaration = []
        for declaration in node.declarations:
            new_declaration.append(self.visit(declaration, scope.next_child()))

        program = ProgramNode(new_declaration, scope, node)
        return program

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> ClassDeclarationNode:
        self.current_type = self.context.get_type(node.id, unpacked=True)

        new_features = []
        for feature in node.features:
            new_features.append(self.visit(feature, scope))

        class_node = ClassDeclarationNode(new_features, node)
        return class_node

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        attr_node = AttrDeclarationNode(node)

        if not node.expr:
            return attr_node

        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type

        decl_type = node.inferenced_type
        # try conforms trata de disminuir la bolsa de tipos de decl_type a base de los
        # que tiene expr_type, en caso de que se quede vacio, se mantiene sin cambios
        # en la bolsa decl_type
        decl_type = try_conform(decl_type, expr_type)

        attr_node.expr = expr_node
        attr_node.inferenced_type = decl_type
        return attr_node

    # Ten ojo con los selftype dentro de los typebags ... Antes de trabajar con los
    # selftypes tienes que cambiarlo por el tipo determinado segun el contexo, utiliza
    # el metodo swap_self_type de los objetos TypeBag para realizar esto. Si se te
    # escapa un selftype cuando se intente realizar una operacion con el se lanza error

    # Este metodo deber ser innecesario pues todos los errores son recogidos previamente
    def add_error(self, node: Node, text: str):
        line, col = node.get_position() if node is not None else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))
