import core.tools.COOLAst as cool
from .BaseCOOLToCILVisitor import *
from core.tools import visitor
from ..tools.Semantic import Scope


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    def __init__(self, context):
        super().__init__(context)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        self.current_function = self.register_function('entry', line=0, column=0)
        main_instance = self.define_internal_local(line=0, column=0)
        self.register_instruction(cil.StaticCallNode(self.init_name('Main'), main_instance, line=0, column=0))
        self.register_instruction(cil.ArgNode(main_instance, line=0, column=0))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'),
                                                     main_instance, line=0, column=0))
        self.register_instruction(cil.ReturnNode(line=0, column=0, value=0))

        self.register_builtin()
        self.current_function = None

        for x, y in zip(node.declarations, scope.childs):
            self.visit(x, y)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode, line=0, column=0)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id.lex)

        # Inicializando los atributos de la clase y llamando al constructor del padre
        if self.current_type.parent.name not in ('Object', 'IO'):
            variable = self.define_internal_local(line=node.line, column=node.column)
            self.register_instruction(cil.ArgNode(self.vself.name, line=node.line, column=node.column))
            self.register_instruction(cil.StaticCallNode(
                self.init_attr_name(self.current_type.parent.name), variable, line=node.line, column=node.column))

        # Inicializando los atributos de la clase
        self.current_function = self.register_function(self.init_attr_name(node.id.lex),
                                                       line=node.line, column=node.column)
        instance = self.register_param(VariableInfo('instance', ''), line=node.line, column=node.column)
        for feat, child in zip(node.features, scope.childs):
            if isinstance(feat, cool.AttrDeclarationNode):
                self.visit(feat, child)
                self.register_instruction(cil.SetAttribNode(instance, feat.id.lex, feat.ret_expr, feat.type.lex,
                                                            line=node.line, column=node.column))
        # TODO: Deberia retornar algo aqui?

        # TypeNode de la clase
        type = self.register_type(node.id.lex, line=node.line, column=node.column)
        type.attributes = [i.name for i in self.current_type.attributes]

        # Guardar métodos de las clases padres
        iter_type = self.current_type
        while iter_type is not None:
            type.methods.update({i: self.to_function_name(i, iter_type.name) for i in iter_type.methods.keys()})
            iter_type = iter_type.parent

        # Visitar funciones dentro de la clase
        for feat, child in zip(node.features, scope.childs):
            if isinstance(feat, cool.FuncDeclarationNode):
                self.visit(feat, child)

        # Allocate de la clase
        self.current_function = self.register_function(self.init_name(node.id.lex), line=node.line, column=node.column)
        instance = self.define_internal_local(line=node.line, column=node.column)
        self.register_instruction(cil.AllocateNode(node.id.lex, instance, line=node.line, column=node.column))

        variable = self.define_internal_local(line=node.line, column=node.column)
        self.register_instruction(cil.ArgNode(instance, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_attr_name(node.id.lex), variable,
                                                     line=node.line, column=node.column))

        if 'init' in self.current_type.methods.keys():
            self.register_instruction(cil.ArgNode(instance, line=node.line, column=node.column))
            self.register_instruction(cil.StaticCallNode(
                self.to_function_name('init', self.current_type.name), variable, line=node.line, column=node.column))

        self.register_instruction(cil.ReturnNode(value=instance, line=node.line, column=node.column))

        self.current_function = None
        self.current_type = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        variable = self.define_internal_local(line=node.line, column=node.column)
        if node.expression:
            self.visit(node.expression, scope.childs[0])
            self.register_instruction(cil.AssignNode(variable, node.expression.ret_expr,
                                                     line=node.expression.line, column=node.expression.column))
        elif node.type.lex in self.value_types:
            self.register_instruction(cil.AllocateNode(node.type.lex, variable, line=node.line, column=node.column))
        self.register_local(VariableInfo(node.id.lex, node.type.lex), line=node.line, column=node.column)
        node.ret_expr = variable

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node: cool.FuncDeclarationNode, scope: Scope):
        self.current_method = self.current_type.get_method(node.id.lex)
        self.current_function = self.register_function(self.to_function_name(self.current_method.name,
                                                                             self.current_type.name),
                                                       line=node.line, column=node.column)

        self_param = self.register_param(self.vself, line=node.line, column=node.column)
        self.vself.name = self_param
        for param, type in node.params:
            self.register_param(VariableInfo(param.lex, type.lex), line=param.line, column=param.column)

        self.visit(node.body, scope.childs[0])
        self.register_instruction(cil.ReturnNode(value=node.body.ret_expr,
                                                 line=node.body.line, column=node.body.column))
        self.current_method = None
        self.vself.name = 'self'

    @visitor.when(cool.IfThenElseNode)
    def visit(self, node: cool.IfThenElseNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        condition = self.define_internal_local(line=node.line, column=node.column)

        then_label = self.register_label('then_label', line=node.line, column=node.column)
        continue_label = self.register_label('continue_label', line=node.line, column=node.column)

        # IF
        self.visit(node.condition, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(condition, node.condition.ret_expr, 'value', 'Bool',
                                                    line=node.condition.line, column=node.condition.column))
        self.register_instruction(cil.GotoIfNode(condition, then_label.label, line=node.condition.line,
                                                 column=node.condition.column))

        # ELSE
        self.visit(node.else_body, scope.childs[2])
        self.register_instruction(cil.AssignNode(ret, node.else_body.ret_expr, line=node.else_body.line,
                                                 column=node.else_body.column))
        self.register_instruction(cil.GotoNode(continue_label.label, line=node.else_body.line,
                                               column=node.else_body.column))

        # THEN
        self.register_instruction(then_label)
        self.visit(node.if_body, scope.childs[1])
        self.register_instruction(cil.AssignNode(ret, node.if_body.ret_expr, line=node.if_body.line,
                                                 column=node.if_body.column))

        self.register_instruction(continue_label)
        node.ret_expr = ret

    @visitor.when(cool.WhileLoopNode)
    def visit(self, node: cool.WhileLoopNode, scope: Scope):
        while_label = self.register_label('while_label', line=node.line, column=node.column)
        loop_label = self.register_label('loop_label', line=node.line, column=node.column)
        pool_label = self.register_label('pool_label', line=node.line, column=node.column)
        condition = self.define_internal_local(line=node.line, column=node.column)

        self.register_instruction(while_label)
        self.visit(node.condition, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(condition, node.condition.ret_expr, 'value', 'Bool',
                                                    line=node.condition.line, column=node.condition.column))
        self.register_instruction(cil.GotoIfNode(condition, loop_label.label, line=node.condition.line,
                                                 column=node.condition.column))
        self.register_instruction(cil.GotoNode(pool_label.label, line=node.condition.line,
                                               column=node.condition.column))

        self.register_instruction(loop_label)
        self.visit(node.body, scope.childs[1])
        self.register_instruction(
            cil.GotoNode(while_label.label, line=node.condition.line, column=node.condition.column))

        self.register_instruction(pool_label)
        # TODO: No estoy seguro de si deberia retornar el nodo directamente o guardarlo antes en una variable
        node.ret_expr = cil.VoidNode()

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        for expr, child in zip(node.expressions, scope.childs):
            self.visit(expr, child)
        node.ret_expr = node.expressions[-1].ret_expr

    @visitor.when(cool.LetInNode)
    def visit(self, node: cool.LetInNode, scope: Scope):
        for (id, type, expr), child in zip(node.let_body, scope.childs[:-1]):
            # TODO TYPE OF ID
            variable = self.register_local(VariableInfo(id.lex, type.lex), line=id.line, column=id.column)
            if expr:
                self.visit(expr, child)
                self.register_instruction(cil.AssignNode(variable, expr.ret_expr, line=expr.line, column=expr.column))
            elif type.lex in self.value_types:
                self.register_instruction(cil.AllocateNode(type.lex, variable, line=type.line, column=type.column))

        self.visit(node.in_body, scope.childs[-1])
        node.ret_expr = node.in_body.ret_expr

    @visitor.when(cool.CaseOfNode)
    def visit(self, node: cool.CaseOfNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        vtype = self.define_internal_local(line=node.line, column=node.column)
        cond = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.TypeOfNode(vtype, node.expression.ret_expr, line=node.expression.line,
                                                 column=node.expression.column))

        isvoid = self.define_internal_local(line=node.line, column=node.column)
        self.register_instruction(cil.EqualNode(isvoid, node.expression.ret_expr, cil.VoidNode(),
                                                line=node.expression.line, column=node.expression.column))
        self.register_runtime_error(isvoid, f'{node.expression.line, node.expression.column} - '
                                            f'RuntimeError: Case on void',
                                    line=node.expression.line, column=node.expression.column)

        end_label = self.register_label('case_end_label', line=node.line, column=node.column)

        branch_type = self.define_internal_local(line=node.line, column=node.column)
        seen = []
        labels = []
        branches = sorted(node.branches, key=lambda x: self.context.get_type(x[1].lex).depth, reverse=True)
        for p, (id, type, expr) in enumerate(branches):
            # TODO Revisar tipo de id para la linea y columna
            labels.append(self.register_label(f'case_label_{p}', line=id.line, column=id.column))

            for t in self.context.subtree(type.lex):
                if t not in seen:
                    seen.append(t)
                    self.register_instruction(cil.NameNode(branch_type, t.name, line=id.line, column=id.column))
                    self.register_instruction(cil.EqualNode(cond, branch_type, vtype, line=id.line, column=id.column))
                    self.register_instruction(cil.GotoIfNode(cond, labels[-1].label, line=id.line, column=id.column))

        data = self.register_data(f'{node.expression.line, node.expression.column} - '
                                  f'RuntimeError: Case statement without a match branch',
                                  line=node.expression.line, column=node.expression.column)
        self.register_instruction(cil.ErrorNode(data, line=node.expression.line, column=node.expression.column))

        for p, label in enumerate(labels):
            id, type, expr = branches[p]
            sc = scope.childs[p + 1]

            self.register_instruction(label)
            var = self.register_local(VariableInfo(id.lex, vtype), line=id.line, column=id.column)
            self.register_instruction(cil.AssignNode(var, node.expression.ret_expr, line=node.expression.line,
                                                     column=node.expression.column))
            self.visit(expr, sc)
            self.register_instruction(cil.AssignNode(ret, expr.ret_expr, line=expr.line, column=expr.column))
            self.register_instruction(cil.GotoNode(end_label.label, line=expr.line, column=expr.column))

        self.register_instruction(end_label)
        node.ret_expr = ret

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        var = self.var_names[node.id.lex]
        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.AssignNode(var, node.expression.ret_expr,
                                                 line=node.expression.line, column=node.expression.column))
        node.ret_expr = var

    @visitor.when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)
        neg_value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(value, node.expression.ret_expr, 'value', 'Bool',
                                                    line=node.expression.line, column=node.expression.column))
        self.register_instruction(cil.NotNode(neg_value, value,
                                              line=node.expression.line, column=node.expression.column))
        self.register_instruction(cil.ArgNode(neg_value, line=node.expression.line, column=node.expression.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))

        node.ret_expr = ret

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.LessEqualNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))

        node.ret_expr = ret

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.LessNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))

        node.ret_expr = ret

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.PlusNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret,line=node.line, column=node.column))

        node.ret_expr = ret

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.MinusNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret, line=node.line, column=node.column))

        node.ret_expr = ret

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.StarNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.left.line, column=node.left.line))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.line))
        self.register_instruction(cil.DivNode(value, left, right, line=node.line, column=node.column))

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        answer = self.define_internal_local(line=node.line, column=node.column)

        void = cil.VoidNode()
        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.EqualNode(answer, node.expression.ret_expr, void,
                                                line=node.expression.line, column=node.expression.node))

        self.register_instruction(cil.ArgNode(answer, line=node.expression.line, column=node.expression.node))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)
        answer = self.define_internal_local(line=node.line, column=node.column)

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(value, node.expression.ret_expr, 'value', 'Int',
                                                    line=node.expression.line, column=node.expression.node))
        self.register_instruction(cil.ComplementNode(answer, value,
                                                     line=node.expression.line, column=node.expression.node))

        self.register_instruction(cil.ArgNode(answer,line=node.expression.line, column=node.expression.node))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)
        left = self.define_internal_local(line=node.line, column=node.column)
        right = self.define_internal_local(line=node.line, column=node.column)
        type_left = self.define_internal_local(line=node.line, column=node.column)
        type_int = self.define_internal_local(line=node.line, column=node.column)
        type_string = self.define_internal_local(line=node.line, column=node.column)
        type_bool = self.define_internal_local(line=node.line, column=node.column)
        equal = self.define_internal_local(line=node.line, column=node.column)
        value = self.define_internal_local(line=node.line, column=node.column)

        int_comparisson = self.register_label('int_comparisson', line=node.line, column=node.column)
        string_comparisson = self.register_label('string_comparisson', line=node.line, column=node.column)
        bool_comparisson = self.register_label('bool_comparisson', line=node.line, column=node.column)
        continue_label = self.register_label('continue_label', line=node.line, column=node.column)

        self.visit(node.left, scope.childs[0])
        self.visit(node.right, scope.childs[1])

        self.register_instruction(cil.TypeOfNode(type_left, node.left.ret_expr,
                                                 line=node.left.line, column=node.left.column))
        self.register_instruction(cil.NameNode(type_int, 'Int', line=node.line, column=node.column))
        self.register_instruction(cil.NameNode(type_string, 'String', line=node.line, column=node.column))
        self.register_instruction(cil.NameNode(type_bool, 'Bool', line=node.line, column=node.column))

        self.register_instruction(cil.EqualNode(equal, type_left, type_int,
                                                line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GotoIfNode(equal, int_comparisson.label,
                                                 line=node.left.line, column=node.left.column))
        self.register_instruction(cil.EqualNode(equal, type_left, type_string,
                                                line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GotoIfNode(equal, string_comparisson.label,
                                                 line=node.left.line, column=node.left.column))
        self.register_instruction(cil.EqualNode(equal, type_left, type_bool,
                                                line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GotoIfNode(equal, bool_comparisson.label,
                                                 line=node.left.line, column=node.left.column))

        self.register_instruction(cil.EqualNode(value, node.left.ret_expr, node.right.ret_expr,
                                                line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GotoNode(continue_label,
                                               line=node.left.line, column=node.left.column))

        self.register_instruction(int_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.column))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int',
                                                    line=node.right.line, column=node.right.column))
        self.register_instruction(cil.EqualNode(value, left, right, line=node.line, column=node.column))
        self.register_instruction(cil.GotoNode(continue_label, line=node.line, column=node.column))

        self.register_instruction(string_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'String',
                                                    line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'String',
                                                    line=node.right.line, column=node.right.column))
        self.register_instruction(cil.EqualStringNode(value, left, right,
                                                      line=node.right.line, column=node.right.column))
        self.register_instruction(cil.GotoNode(continue_label, line=node.line, column=node.column))

        self.register_instruction(bool_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Bool',
                                                    line=node.left.line, column=node.left.column))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Bool',
                                                    line=node.right.line, column=node.right.column))
        self.register_instruction(cil.EqualNode(value, left, right,
                                                line=node.right.line, column=node.right.column))
        self.register_instruction(cil.GotoNode(continue_label, line=node.line, column=node.column))

        self.register_instruction(continue_label)

        self.register_instruction(cil.ArgNode(value, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.FunctionCallNode)
    def visit(self, node: cool.FunctionCallNode, scope: Scope):
        args = []
        for arg, child in zip(node.args, scope.childs[1:]):
            self.visit(arg, child)
            args.append(cil.ArgNode(arg.ret_expr, line=arg.line, column=arg.column))

        self.visit(node.obj, scope.childs[0])

        void = cil.VoidNode()
        isvoid = self.define_internal_local(line=node.line, column=node.column)
        self.register_instruction(cil.EqualNode(isvoid, node.obj.ret_expr, void,
                                                line=node.obj.line, column=node.obj.column))
        self.register_runtime_error(isvoid, f'{node.id.line, node.id.column} - RuntimeError: Dispatch on void',
                                    line=node.id.line, column=node.id.column)

        # TODO: Creo que deberia annadir los parametros al reves para luego sacarlos en el orden correcto
        self.register_instruction(cil.ArgNode(node.obj.ret_expr, line=node.obj.line, column=node.obj.column))
        for arg in args:
            self.register_instruction(arg)

        ret = self.define_internal_local(line=node.line, column=node.column)
        stype = node.type
        if stype is None: stype = node.obj.static_type.name
        self.register_instruction(cil.StaticCallNode(self.types_map[stype].methods[node.id.lex], ret,
                                                          line=node.id.line, column=node.id.column))
        node.ret_expr = ret

    @visitor.when(cool.MemberCallNode)
    def visit(self, node: cool.MemberCallNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)

        args = []
        for arg, child in zip(node.args, scope.childs):
            self.visit(arg, child)
            args.append(cil.ArgNode(arg.ret_expr, line=arg.line, column=arg.column))

        # TODO: Creo que deberia annadir los parametros al reves para luego sacarlos en el orden correcto
        self.register_instruction(cil.ArgNode(self.vself.name, line=node.line, column=node.column))
        for arg in args: self.register_instruction(arg)

        stype = self.current_type.name
        self.register_instruction(cil.StaticCallNode(self.types_map[stype].methods[node.id.lex], ret, line=node.id.line, column=node.id.column))
        node.ret_expr = ret

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)

        if node.type == 'SELF_TYPE':
            variable = self.define_internal_local(line=node.line, column=node.column)
            self.register_instruction(cil.TypeOfNode(ret, self.vself.name, line=node.line, column=node.column))
            # TODO: ALLOCATE a veces recibe el nombre de la clase como string, necesito cambiar este ya
            #  que el nombre de la clase se encuentra dentro de la variable, o cambiar los demas para
            #  que funcionen con self.register_instruction(cil.LoadNode(variable, data))
            self.register_instruction(cil.AllocateNode(variable, ret, line=node.line, column=node.column))
        else:
            if node.type == 'Int':
                self.register_instruction(cil.ArgNode(0, line=node.type.line, column=node.type.column))
            elif node.type == 'Bool':
                self.register_instruction(cil.ArgNode(False, line=node.type.line, column=node.type.column))
            elif node.type == 'String':
                data = self.emptystring_data
                variable = self.define_internal_local(line=node.line, column=node.column)
                self.register_instruction(cil.LoadNode(variable, data, line=node.line, column=node.column))
                self.register_instruction(cil.ArgNode(variable, line=node.line, column=node.column))

            self.register_instruction(cil.StaticCallNode(self.init_name(node.type.lex), ret,
                                                         line=node.type.line, column=node.type.column))
        node.ret_expr = ret

    @visitor.when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):
        if node.token.lex == 'self':
            node.ret_expr = self.vself.name
        else:
            node.ret_expr = self.var_names[node.token.lex]

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        try:
            data = [i for i in self.dotdata if i.value == node.token.lex][0]
        except IndexError:
            data = self.register_data(node.token.lex, line=node.token.line, column=node.token.column)

        variable = self.define_internal_local(line=node.line, column=node.column)
        ret = self.define_internal_local(line=node.line, column=node.column)

        self.register_instruction(cil.LoadNode(variable, data, line=node.line, column=node.column))
        self.register_instruction(cil.ArgNode(variable, line=node.line, column=node.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), ret,
                                                     line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)

        # TODO: Hay algunos ArgNode que reciben variables y otros valores especificos
        self.register_instruction(cil.ArgNode(node.token.lex, line=node.token.line, column=node.token.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret, line=node.line, column=node.column))
        node.ret_expr = ret

    @visitor.when(cool.BoolNode)
    def visit(self, node: cool.BoolNode, scope: Scope):
        ret = self.define_internal_local(line=node.line, column=node.column)

        # TODO: Hay algunos ArgNode que reciben variables y otros valores especificos
        self.register_instruction(cil.ArgNode(node.token.lex, line=node.token.line, column=node.token.column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret, line=node.line, column=node.column))
        node.ret_expr = ret
