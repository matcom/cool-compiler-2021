from utils import visitor
from asts.inferencer_ast import (
    AssignNode,
    AtomicNode,
    AttrDeclarationNode,
    BinaryNode,
    BlocksNode,
    CaseOptionNode,
    MethodCallNode,
    CaseNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    ComplementNode,
    ConditionalNode,
    InstantiateNode,
    IsVoidNode,
    LetNode,
    NotNode,
    ProgramNode,
    VarDeclarationNode,
    LoopNode,
)
from semantics.tools import Context, Scope


class TypeLogger(object):
    def __init__(self, context) -> None:
        self.context: Context = context

    @visitor.on("node")
    def visit(self, node, scope, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope: Scope, tabs=0):
        ans = "\t" * tabs + f"\\__ProgramNode [<class> ... <class>]"
        statements = "\n".join(
            self.visit(child, scope.next_child(), tabs + 1)
            for child in node.declarations
        )
        return f"{ans}\n{statements}"

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, tabs=0):
        parent = "" if node.parent is None else f": {node.parent}"
        attr_list = self.context.get_type(node.id, unpacked=True).attributes
        name_list = ["self"]
        for attr in attr_list:
            name_list.append(attr.name)
        format_scope = defined_format(name_list, scope, tabs)
        ans = (
            "\t" * tabs
            + f"\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}"
        )
        ans += format_scope
        features = "\n".join(
            str(self.visit(child, scope, tabs + 1)) for child in node.features
        )
        return f"{ans}\n{features}"

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope: Scope, tabs=0):
        extra = computed_info(node)
        ans = "\t" * tabs + f"\\__AttrDeclarationNode: {node.id} : {node.type}" + extra
        if node.expr != None:
            ans += f"\n{self.visit(node.expr, scope, tabs +1)}"
        return f"{ans}"

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans = (
            "\t" * tabs
            + f"\\__VarDeclarationNode: {node.id} : {node.type} = <expr>"
            + extra
        )
        if node.expr != None:
            ans += f"\n{self.visit(node.expr, scope, tabs + 1)}"
        return f"{ans}"

    @visitor.when(BlocksNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans = "\t" * tabs + "\\__BlocksNode: { <expr>; ... <expr>; }" + extra
        body = "\n".join(self.visit(child, scope, tabs + 1) for child in node.expr_list)
        return f"{ans}\n{body}"

    @visitor.when(ConditionalNode)
    def visit(self, node, scope, tabs=0):
        ifexpr = self.visit(node.condition, scope, tabs + 1)
        thenexpr = self.visit(node.then_body, scope, tabs + 1)
        elseexpr = self.visit(node.else_body, scope, tabs + 1)
        extra = computed_info(node)
        ans = (
            "\t" * tabs
            + f"\\ConditionalNode: if <expr> then <expr> else <expr>{extra}\n"
        )
        ifs = "\t" * (tabs + 1) + f"if:\n{ifexpr}\n"
        ths = "\t" * (tabs + 1) + f"then:\n{thenexpr}\n"
        els = "\t" * (tabs + 1) + f"else:\n{elseexpr}"
        ans = ans + ifs + ths + els
        return ans

    @visitor.when(CaseNode)
    def visit(self, node, scope: Scope, tabs=0):
        extra = computed_info(node)
        header = (
            "\t" * tabs + f"\\CaseNode: case <expr> of ( <var> => <expr> ...){extra}\n"
        )
        caseexpr = self.visit(node.case_expr, scope, tabs + 1)
        case = "\t" * (tabs + 1) + f"case:\n{caseexpr}\n"
        # casevars =  '\n'.join([self.visit(child, scope.next_child(), tabs + 1) for child in node.options])
        casevars = "\n".join(
            [self.visit(child, scope.next_child(), tabs + 1) for child in node.options]
        )
        of = "\t" * (tabs + 1) + f"of:\n{casevars}"
        return header + case + of

    @visitor.when(CaseOptionNode)
    def visit(self, node, scope: Scope, tabs=0):
        type_info = computed_info(node)
        return "\t" * (tabs) + "\\_" + node.id + ":" + node.type + type_info

    @visitor.when(LetNode)
    def visit(self, node, scopex, tabs=0):
        scope = scopex.next_child()
        extra = computed_info(node)
        header = (
            "\t" * tabs + f"\\LetNode: Let (<var> <- <expr> ...) in <expr>{extra}\n"
        )
        name_list = []
        for name_var in node.var_decl_list:
            name_list.append(name_var.id)
        format_scope = defined_format(name_list, scope, tabs)
        letvars = "\n".join(
            self.visit(child, scope, tabs + 1) for child in node.var_decl_list
        )
        expr = self.visit(node.in_expr, scope, tabs + 1)
        let = "\t" * (tabs + 1) + f"let: \n{letvars}\n"
        inx = "\t" * (tabs + 1) + f"in: \n{expr}"
        return header + let + inx

    @visitor.when(LoopNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        header = "\t" * tabs + f"\\__LoopNode: while <expr> loop ( <expr> ){extra}\n"
        body = self.visit(node.body, scope, tabs + 1)
        whilex = self.visit(node.condition, scope, tabs + 1) + "\n"
        text1 = "\t" * (tabs + 1) + f"while:\n {whilex}"
        text2 = "\t" * (tabs + 1) + f"loop:\n {body}"
        return header + text1 + text2

    @visitor.when(AssignNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans = "\t" * tabs + f"\\__AssignNode: {node.id} = <expr>" + extra
        expr = self.visit(node.expr, scope, tabs + 1)
        return f"{ans}\n{expr}"

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode, scopex, tabs=0):
        scope = scopex.next_child()
        extra = computed_info(node)
        params = ", ".join([f"{param.id}:{param.type}" for param in node.params])
        ans = (
            "\t" * tabs
            + f"\\__MethodDeclarationNode: {node.id}({params}) : {node.type}"
            + extra
        )
        name_list = []
        for param in node.params:
            name_list.append(param.id)
        format_scope = defined_format(name_list, scope, tabs)
        ans += format_scope
        body = "\n" + self.visit(node.body, scope, tabs + 1)
        return f"{ans}{body}"

    @visitor.when(IsVoidNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans1 = "\t" * tabs + f"\\__IsVoidNode: isvoid <expr>" + extra
        ans2 = self.visit(node.expr, scope, tabs + 1)
        return ans1 + "\n" + ans2

    @visitor.when(ComplementNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans1 = "\t" * tabs + f"\\ComplementNode: ~ <expr>" + extra
        ans2 = self.visit(node.expr, scope, tabs + 1)
        return ans1 + "\n" + ans2

    @visitor.when(NotNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans1 = "\t" * tabs + f"\\__NotNode: not <expr>" + extra
        ans2 = self.visit(node.expr, scope, tabs + 1)
        return ans1 + "\n" + ans2

    # @visitor.when(IsVoidDeclarationNode)
    # def visit(self, node, scope, tabs=0):
    #    extra = computed_info(node)
    #    ans1 = '\t' * tabs + f'\\__IsVoidNode: isvoid <expr>' + extra
    #    ans2 = self.visit(node.lex, scope, tabs+1)
    #    return ans1 + "\n" + ans2

    @visitor.when(BinaryNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        ans = "\t" * tabs + f"\\__<expr> {node.__class__.__name__} <expr>" + extra
        left = self.visit(node.left, scope, tabs + 1)
        right = self.visit(node.right, scope, tabs + 1)
        return f"{ans}\n{left}\n{right}"

    @visitor.when(AtomicNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        return "\t" * tabs + f"\\__ {node.__class__.__name__}: {node.value}" + extra

    @visitor.when(MethodCallNode)
    def visit(self, node, scope, tabs=0):
        extra = computed_info(node)
        extra2 = ""
        if node.caller_type:
            extra2 = node.caller_type.name + "."
        ans = (
            "\t" * tabs
            + f"\\__MethodCallNode: {extra2}{node.id}(<expr>, ..., <expr>)"
            + extra
        )
        args = "\n".join(self.visit(arg, scope, tabs + 1) for arg in node.args)
        if len(node.args) > 0:
            return f"{ans}\n{args}"
        return f"{ans}"

    @visitor.when(InstantiateNode)
    def visit(self, node, scope, tabs=0):
        return "\t" * tabs + f"\\__ InstantiateNode: new {node.value}()"


def defined_format(name_list: list, scope: Scope, tabs=0):
    if len(name_list) == 0:
        return ""

    header = "\n" + "\t" * tabs + f"  Variables Defined:" + "\n" + "\t" * tabs + "  |  "
    defined = str("\n" + "\t" * tabs + f"  |  ").join(
        [defined_info(name, scope) for name in name_list]
    )
    end = "\n" + "\t" * tabs + f"  -----------------------------------"
    return header + defined + end


def defined_info(name: str, scope: Scope, only_local=True):
    if only_local and not scope.is_local(name):
        return f'<Variable "{name}" not defined locally>'
    var = scope.find_variable(name)
    if not only_local and not var:
        return f'<Variable "{name}" not defined>'
    try:
        return f"{var.name}:{var.type.name}"
    except AttributeError:
        return f'<Error while accessing Variable "{var.name}" type: "{var.type}">'


def computed_info(node):
    return " -> " + node.inferenced_type.name
    try:
        if node.type != "AUTO_TYPE":
            return ""
    except AttributeError:
        pass
    try:
        node.computed_type
        try:
            return f" -> {node.computed_type.name}"
        except AttributeError:
            return (
                f" -> <Error While accessing Computed Type Name({node.computed_type})>"
            )
    except AttributeError:
        return " -> <Not Computed>"
