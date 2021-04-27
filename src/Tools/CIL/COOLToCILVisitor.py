import Tools.Tools.COOLAst as cool
from .BaseCOOLToCILVisitor import *
from Tools.Tools import visitor
from ..Tools.Semantic import Scope

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    def __init__(self, context):
        super().__init__(context)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node : cool.ProgramNode, scope : Scope):
        self.current_function = self.register_function('entry')
        return_value = self.define_internal_local()
        main_instance = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode(self.init_name('Main'), main_instance))
        self.register_instruction(cil.ArgNode(main_instance))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'), return_value))
        self.register_instruction(cil.ReturnNode(0))

        #self.register_builtin()
        self.current_function = None

        for x, y in zip(node.declarations, scope.childs):
            self.visit(x, y)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)


    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node : cool.ClassDeclarationNode, scope : Scope):
        self.current_type = self.context.get_type(node.id.lex)

        # Inicializando los atributos de la clase y llamando al constructor del padre
        self.current_function = self.register_function(self.init_attr_name(node.id.lex))
        if self.current_type.parent.name not in ('Object', 'IO'):
            # TODO: Este self deberia ser el que paso por parametro?
            variable = self.define_internal_local()
            self.register_instruction(cil.ArgNode(self.vself.name))
            self.register_instruction(cil.StaticCallNode(
                self.init_attr_name(self.current_type.parent.name), variable))
        for feat, child in zip(node.features, scope.childs):
            if isinstance(feat, cool.AttrDeclarationNode):
                self.visit(feat, child)
        # TODO: Deberia retornar algo aqui?

        type = self.register_type(node.id.lex)
        type.attributes = [i.name for i in self.current_type.attributes]
        iter_type = self.current_type
        while iter_type is not None:
            type.methods += [self.to_function_name(i, iter_type.name) for i in iter_type.methods.keys()]
            iter_type = iter_type.parent
        type.methods.reverse()

        for feat, child in zip(node.features, scope.childs):
            if isinstance(feat, cool.FuncDeclarationNode):
                self.visit(feat, child)

        # TODO: Que hacer si la clase ya tiene definido el metodo init?
        self.current_function = self.register_function(self.init_name(node.id.lex))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.id.lex, instance))

        variable = self.define_internal_local()
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(self.init_attr_name(node.id.lex), variable))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = None
        self.current_type = None

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node : cool.AttrDeclarationNode, scope : Scope):
        if node.expression:
            self.visit(node.expression, scope.childs[0])
            self.register_instruction(cil.SetAttribNode(
                self.vself.name, node.id, node.expression.ret_expr, self.current_type))
        elif node.type.lex in self.value_types:
            variable = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type.lex, variable))
            self.register_instruction(cil.SetAttribNode(
                self.vself.name, node.id, variable, self.current_type))
        variable = self.register_local(VariableInfo(node.id.lex, node.type.lex))
        node.ret_expr = variable

    @visitor.when(cool.FuncDeclarationNode)
    def visit(self, node : cool.FuncDeclarationNode, scope : Scope):
        self.current_method = self.current_type.get_method(node.id.lex)
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, self.current_type.name))

        self.register_param(self.vself)
        for param, type in node.params:
            self.register_param(VariableInfo(param.lex, type.lex))

        self.visit(node.body, scope.childs[0])
        self.register_instruction(cil.ReturnNode(node.body.ret_expr))
        self.current_method = None

    @visitor.when(cool.IfThenElseNode)
    def visit(self, node : cool.IfThenElseNode, scope : Scope):
        ret = self.define_internal_local()
        condition = self.define_internal_local()

        then_label = self.register_label('then_label')
        continue_label = self.register_label('continue_label')

        self.visit(node.condition, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(condition, node.condition.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.GotoIfNode(condition, then_label.label))

        self.visit(node.else_body, scope.childs[2])
        self.register_instruction(cil.AssignNode(ret, node.else_body.ret_expr))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(then_label)
        self.visit(node.if_body, scope.childs[1])
        self.register_instruction(cil.AssignNode(ret, node.if_body.ret_expr))

        self.register_instruction(continue_label)
        node.ret_expr = ret

    @visitor.when(cool.WhileLoopNode)
    def visit(self, node : cool.WhileLoopNode, scope : Scope):
        while_label = self.register_label('while_label')
        loop_label = self.register_label('loop_label')
        pool_label = self.register_label('pool_label')
        condition = self.define_internal_local()

        self.register_instruction(while_label)
        self.visit(node.condition, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(condition, node.condition.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.GotoIfNode(condition, loop_label.label))
        self.register_instruction(cil.GotoNode(pool_label.label))

        self.register_instruction(loop_label)
        self.visit(node.body, scope.childs[1])
        self.register_instruction(cil.GotoNode(while_label.label))

        self.register_instruction(pool_label)
        # TODO: No estoy seguro de si deberia retornar el nodo directamente o guardarlo antes en una variable
        node.ret_expr = cil.VoidNode()

    @visitor.when(cool.BlockNode)
    def visit(self, node : cool.BlockNode, scope : Scope):
        for expr, child in zip(node.expressions, scope.childs):
            self.visit(expr, child)
        node.ret_expr = node.expressions[-1].ret_expr

    @visitor.when(cool.LetInNode)
    def visit(self, node : cool.LetInNode, scope : Scope):
        for (id, type, expr), child in zip(node.let_body, scope.childs[:-1]):
            variable = self.register_local(VariableInfo(id.lex, type.lex))
            if expr:
                self.visit(expr, child)
                self.register_instruction(cil.AssignNode(variable, expr.ret_expr))
            elif type.lex in self.value_types:
                self.register_instruction(cil.AllocateNode(type.lex, variable))

        self.visit(node.in_body, scope.childs[-1])
        node.ret_expr = node.in_body.ret_expr


    @visitor.when(cool.CaseOfNode)
    def visit(self, node : cool.CaseOfNode, scope : Scope):
        ret = self.define_internal_local()
        vtype = self.define_internal_local()
        cond = self.define_internal_local()

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.TypeOfNode(vtype, node.expression.ret_expr))

        void = cil.VoidNode()
        isvoid = self.define_internal_local()
        self.register_instruction(cil.EqualNode(isvoid, node.expression.ret_expr, void))
        self.register_runtime_error(isvoid, f'{node.expression.line, node.expression.column} - '
                                            f'RuntimeError: Case on void')

        end_label = self.register_label('case_end_label')

        branch_type = self.define_internal_local()
        seen = []
        labels = []
        branches = sorted(node.branches, key=lambda x: self.context.get_type(x[1].lex).depth, reverse=True)
        for p, (id, type, expr) in enumerate(branches):
            labels.append(self.register_label(f'case_label_{p}'))

            for t in self.context.subtree(type.lex):
                if not t in seen:
                    seen.append(t)
                    self.register_instruction(cil.NameNode(branch_type, t.name))
                    self.register_instruction(cil.EqualNode(cond, branch_type, vtype))
                    self.register_instruction(cil.GotoIfNode(cond, labels[-1].label))

        data = self.register_data(f'{node.expression.line, node.expression.column} - '
                                  f'RuntimeError: Case statement without a match branch')
        self.register_instruction(cil.ErrorNode(data))

        for p, label in enumerate(labels):
            id, type, expr = branches[p]
            sc = scope.childs[p + 1]

            self.register_instruction(label)
            var = self.register_local(VariableInfo(id.lex, vtype))
            self.register_instruction(cil.AssignNode(var, node.expression.ret_expr))
            self.visit(expr, sc)
            self.register_instruction(cil.AssignNode(ret, expr.ret_expr))
            self.register_instruction(cil.GotoNode(end_label.label))

        self.register_instruction(end_label)
        node.ret_expr = ret


    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        var = self.var_names[node.id.lex]
        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.AssignNode(var, node.expression.ret_expr))
        node.ret_expr = var

    @visitor.when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope: Scope):
        ret = self.define_internal_local()
        value = self.define_internal_local()
        neg_value = self.define_internal_local()

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(value, node.expression.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.NotNode(neg_value, value))
        self.register_instruction(cil.ArgNode(neg_value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))

        node.ret_expr = ret


    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.LessEqualNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))

        node.ret_expr = ret

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.LessNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))

        node.ret_expr = ret

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.PlusNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))

        node.ret_expr = ret

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.MinusNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))

        node.ret_expr = ret

    @visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.StarNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))
        node.ret_expr = ret

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope.childs[1])
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.DivNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))
        node.ret_expr = ret


    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        ret = self.define_internal_local()
        value = self.define_internal_local()
        answer = self.define_internal_local()

        void = cil.VoidNode()
        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.AssignNode(value, node.expression.ret_expr))
        self.register_instruction(cil.EqualNode(answer, value, void))

        self.register_instruction(cil.ArgNode(answer))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))
        node.ret_expr = ret

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        ret = self.define_internal_local()
        value = self.define_internal_local()
        answer = self.define_internal_local()

        self.visit(node.expression, scope.childs[0])
        self.register_instruction(cil.GetAttribNode(value, node.expression.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.ComplementNode(answer, value))

        self.register_instruction(cil.ArgNode(answer))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))
        node.ret_expr = ret

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        ret = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        type_left = self.define_internal_local()
        type_int = self.define_internal_local()
        type_string = self.define_internal_local()
        type_bool = self.define_internal_local()
        type = self.define_internal_local()
        equal = self.define_internal_local()
        value = self.define_internal_local()

        int_comparisson = self.register_label('int_comparisson')
        string_comparisson = self.register_label('string_comparisson')
        bool_comparisson = self.register_label('bool_comparisson')
        continue_label = self.register_label('continue_label')

        self.visit(node.left, scope.childs[0])
        self.visit(node.right, scope.childs[1])

        self.register_instruction(cil.TypeOfNode(type_left, node.left.ret_expr))
        self.register_instruction(cil.NameNode(type_int, 'Int'))
        self.register_instruction(cil.NameNode(type_string, 'String'))
        self.register_instruction(cil.NameNode(type_bool, 'Bool'))

        self.register_instruction(cil.EqualNode(equal, type_left, type_int))
        self.register_instruction(cil.GotoIfNode(equal, int_comparisson.label))
        self.register_instruction(cil.EqualNode(equal, type_left, type_string))
        self.register_instruction(cil.GotoIfNode(equal, string_comparisson.label))
        self.register_instruction(cil.EqualNode(equal, type_left, type_bool))
        self.register_instruction(cil.GotoIfNode(equal, bool_comparisson.label))

        self.register_instruction(cil.EqualNode(value, node.left.ret_expr, node.right.ret_expr))
        self.register_instruction(cil.GotoNode(continue_label))

        self.register_instruction(int_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.EqualNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label))

        self.register_instruction(string_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'String'))
        self.register_instruction(cil.EqualStringNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label))

        self.register_instruction(bool_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.GetAttribNode(right, node.right.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.EqualNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label))

        self.register_instruction(continue_label)

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))
        node.ret_expr = ret


    @visitor.when(cool.FunctionCallNode)
    def visit(self, node: cool.FunctionCallNode, scope: Scope):
        args = []
        for arg, child in zip(node.args, scope.childs[1:]):
            self.visit(arg, child)
            args.append(cil.ArgNode(arg.ret_expr))

        self.visit(node.obj, scope.childs[0])

        void = cil.VoidNode()
        isvoid = self.define_internal_local()
        self.register_instruction(cil.EqualNode(isvoid, node.obj.ret_expr, void))
        self.register_runtime_error(isvoid, f'{node.id.line, node.id.column} - RuntimeError: Dispatch on void')

        self.register_instruction(cil.ArgNode(node.obj.ret_expr))
        for arg in args: self.register_instruction(arg)

        ret = self.define_internal_local()
        if node.type:
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.id, node.type.name), ret))
        else:
            type = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(type, node.obj.ret_expr))
            self.register_instruction(cil.DynamicCallNode(type, node.id, ret))
        node.ret_expr = ret

    @visitor.when(cool.MemberCallNode)
    def visit(self, node: cool.MemberCallNode, scope: Scope):
        ret = self.define_internal_local()
        type = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(type, self.vself.name))

        args = []
        for arg, child in zip(node.args, scope.childs):
            self.visit(arg, child)
            args.append(cil.ArgNode(arg.ret_expr))

        self.register_instruction(cil.ArgNode(self.vself.name))
        for arg in args: self.register_instruction(arg)

        self.register_instruction(cil.DynamicCallNode(type, node.id, ret))
        node.ret_expr = ret

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        ret = self.define_internal_local()

        if node.type == 'SELF_TYPE':
            variable = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(ret, self.vself.name))
            self.register_instruction(cil.AllocateNode(variable, ret))
        else:
            if node.type == 'Int':
                self.register_instruction(cil.ArgNode(0))
            elif node.type == 'Bool':
                self.register_instruction(cil.ArgNode(False))
            elif node.type == 'String':
                data = self.emptystring_data
                variable = self.define_internal_local()
                self.register_instruction(cil.LoadNode(variable, data))
                self.register_instruction(cil.ArgNode(variable))

            self.register_instruction(cil.StaticCallNode(self.init_name(node.type.lex), ret))
        node.ret_expr = ret

    @visitor.when(cool.IdNode)
    def visit(self, node: cool.IdNode, scope: Scope):
        if node.token.lex == 'self': node.ret_expr = self.vself.name
        else: node.ret_expr = self.var_names[node.token.lex]

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        try:
            data = [i for i in self.dotdata if i.value == node.token.lex][0]
        except IndexError:
            data = self.register_data(node.token.lex)

        variable = self.define_internal_local()
        ret = self.define_internal_local()

        self.register_instruction(cil.LoadNode(variable, data))
        self.register_instruction(cil.ArgNode(variable))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), ret))
        node.ret_expr = ret

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(node.token.lex))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), ret))
        node.ret_expr = ret

    @visitor.when(cool.BoolNode)
    def visit(self, node: cool.BoolNode, scope: Scope):
        ret = self.define_internal_local()

        self.register_instruction(cil.ArgNode(node.token.lex))
        self.register_instruction(cil.StaticCallNode(self.init_name('Bool'), ret))
        node.ret_expr = ret


