import CIL.ast as cil
import Utils.visitor as visitor

from Parser.ast import *
from CIL.builder import builder_init, builder_main, builder_params, builder_types

class CIL:
    def __init__(self, context):
        self.context = context
        self.label_count = 0
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.data = {}
        self.code = [builder_main()]
        self.types = builder_types(self.context)

        for def_class in node.class_list:
            self.visit(def_class)

        return cil.ProgramNode(self.types.values(), self.data.values(), self.code)

    @visitor.when(ClassNode)
    def visit(self, node):
        self.current = self.context.get_type(node.type.value)
        
        if self.current.attributes:
            self.code.append(builder_init(self))

        for feature in node.feature_list:
            self.visit(feature)

    @visitor.when(MethodNode)
    def visit(self, node):
        self.locals = {}
        self.local_data = {}
        self.instructions = []
        self.params = builder_params(self.current.get_method(node.id.value))

        self.visit(node.expr)

        self.instructions.append(cil.ReturnNode(node.expr.computed_value))
        self.code.append(cil.CodeNode(f'{self.current.name}.{node.id.value}', self.params, self.locals.values(), self.instructions))

    @visitor.when(LetNode)
    def visit(self, node):
        for assigs in node.assigs:
            if assigs[2]:
                self.visit(assigs[2])
                local = self.add_local(assigs[0].value)
                self.instructions.append(cil.AssignmentNode(local, assigs[2].computed_value))
        
        self.visit(node.expr)
        node.computed_value = self.add_local()
        self.instructions.append(cil.AssignmentNode(node.computed_value, node.expr.computed_value))
    
    @visitor.when(BlockNode)
    def visit(self, node):
        for expr in node.exprs:
            self.visit(expr)
        node.computed_value = node.exprs[-1].computed_value

    @visitor.when(LoopsNode)
    def visit(self, node):
        label_1 = self.add_label()
        self.instructions.append(cil.LabelNode(label_1))
        self.visit(node.pred)
        
        local = self.add_local()
        self.instructions.append(cil.AssignmentNode(local, node.pred.computed_value))

        label_2 = self.add_label()
        self.instructions.append(cil.ConditionalNode(local, label_2))

        label_3 = self.add_label()
        self.instructions.append(cil.GotoNode(label_3))
        self.instructions.append(cil.LabelNode(label_2))

        self.visit(node.expr)
        self.instructions.append(cil.GotoNode(label_1))
        self.instructions.append(cil.LabelNode(label_3))

        node.computed_value = self.add_local()
        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))

    @visitor.when(ConditionalNode)
    def visit(self, node):
        self.visit(node.pred)
        
        local = self.add_local()
        self.instructions.append(cil.AssignmentNode(local, node.pred.computed_value))
        label_1 = self.add_label()
        self.instructions.append(cil.ConditionalNode(local, label_1))
        node.computed_value = self.add_local()    
        
        self.visit(node.neth)
        
        self.instructions.append(cil.AssignmentNode(node.computed_value, node.neth.computed_value))
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))
        
        self.visit(node.then)
        
        self.instructions.append(cil.AssignmentNode(node.computed_value, node.then.computed_value))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(CaseNode)
    def visit(self, node):
        self.visit(node.expr)
        local = self.add_local()
        self.instructions.append(cil.TypeOfNode(local, node.expr.computed_value))

        labels = [self.add_label() for i in range(len(node.tests))]
        node.computed_value = self.add_local()

        for i, branch in enumerate(node.tests):
            local_1 = self.add_local()
            self.instructions.append(cil.AssignmentNode(local_1, branch[1].value))

            local_2 = self.add_local()
            self.instructions.append(cil.MinusNode(local_2, local, local_1))

            self.instructions.append(cil.ConditionalNode(local_2, labels[i]))

            id_1 = self.add_local(branch[0].value)
            self.instructions.append(cil.AssignmentNode(id_1, node.expr.computed_value))

            self.visit(branch[2])
            self.instructions.append(cil.AssignmentNode(node.computed_value, branch[2].computed_value))

            if i != len(node.tests) - 1:
                self.instructions.append(cil.GotoNode(labels[-1]))
            
            self.instructions.append(cil.LabelNode(labels[i]))

    @visitor.when(NewNode)
    def visit(self, node):
        type_name = node.type.value
        if type_name == 'SELF_TYPE': type_name = self.current.name
        local = self.add_local()
        self.instructions.append(cil.AllocateNode(local, type_name))
        self.instructions.append(cil.ArgumentNode(local))
        node.computed_value = self.add_local()
        self.instructions.append(cil.DynamicCallNode(node.computed_value, type_name, 'init'))

    @visitor.when(IsvoidNode)
    def visit(self, node):
        self.visit(node.expr)
        
        local_1 = self.add_local()
        self.instructions.append(cil.TypeOfNode(local_1, node.expr.computed_value))

        local_2 = self.add_local()
        self.instructions.append(cil.MinusNode(local_2, local_1, 'void'))

        label_1 = self.add_label()
        self.instructions.append(cil.ConditionalNode(local_2, label_1))

        node.computed_value = self.add_local()
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))

        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(IdentifierNode)
    def visit(self, node):
        try:
            node.computed_value = self.locals[node.lexer.value]
        except KeyError:
            try:
                node.computed_value = self.params[node.lexer.value]
            except KeyError:
                node.computed_value = self.add_local()
                self.instructions.append(cil.GetAttributeNode(node.computed_value, self.params['self'], node.lexer.value))

    @visitor.when(IntegerNode)
    def visit(self, node):
        node.computed_value = node.lexer.value
    
    @visitor.when(StringNode)
    def visit(self, node):
        data = self.add_data(node.lexer.value)
        node.computed_value = self.add_local_data(data)
    
    @visitor.when(BoolNode)
    def visit(self, node):
        node.computed_value = 1 if node.lexer.value == 'true' else 0
    
    @visitor.when(BinaryNode)
    def visit(self, node):
        self.visit(node.left)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.left.computed_value))

        self.visit(node.right)
        local_2 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_2, node.right.computed_value))

        node.computed_value = self.add_local()
        if isinstance(node, PlusNode):
            self.instructions.append(cil.PlusNode(node.computed_value, local_1, local_2))
        if isinstance(node, MinusNode):
            self.instructions.append(cil.MinusNode(node.computed_value, local_1, local_2))
        if isinstance(node, StarNode):
            self.instructions.append(cil.StarNode(node.computed_value, local_1, local_2))
        if isinstance(node, DivideNode):
            self.instructions.append(cil.DivideNode(node.computed_value, local_1, local_2))

    @visitor.when(EqualNode)
    def visit(self, node):
        self.visit(node.left)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.left.computed_value))
        self.visit(node.right)
        local_2 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_2, node.right.computed_value))
        local_3 = self.add_local()
        self.instructions.append(cil.MinusNode(local_3, local_1, local_2))
        label_1 = self.add_label()
        node.computed_value = self.add_local()
        self.instructions.append(cil.ConditionalNode(local_3, label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(LessNode)
    def visit(self, node):
        self.visit(node.left)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.left.computed_value))
        self.visit(node.right)
        local_2 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_2, node.right.computed_value))
        local_3 = self.add_local()
        self.instructions.append(cil.DivideNode(local_3, local_1, local_2))
        label_1 = self.add_label()
        node.computed_value = self.add_local()
        self.instructions.append(cil.ConditionalNode(local_3, label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(LequalNode)
    def visit(self, node):
        self.visit(node.left)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.left.computed_value))
        self.visit(node.right)
        local_2 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_2, node.right.computed_value))
        local_3 = self.add_local()
        self.instructions.append(cil.DivideNode(local_3, local_1, local_2))
        label_1 = self.add_label()
        node.computed_value = self.add_local()
        self.instructions.append(cil.ConditionalNode(local_3, label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))
        local_4 = self.add_local()
        self.instructions.append(cil.MinusNode(local_4, local_1, local_2))
        label_3 = self.add_label()
        self.instructions.append(cil.ConditionalNode(local_4, label_3))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_3))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(ComplementNode)
    def visit(self, node):
        self.visit(node.expr)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.expr.computed_value))
        local_2 = self.add_local()
        self.instructions.append(cil.PlusNode(local_2, local_1, 1))
        node.computed_value = self.add_local()
        self.instructions.append(cil.MinusNode(node.computed_value, 0, local_2))

    @visitor.when(NegationNode)
    def visit(self, node):
        self.visit(node.expr)
        local_1 = self.add_local()
        self.instructions.append(cil.AssignmentNode(local_1, node.expr.computed_value))
        label_1 = self.add_label()
        node.computed_value = self.add_local()
        self.instructions.append(cil.ConditionalNode(local_1, label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 1))
        label_2 = self.add_label()
        self.instructions.append(cil.GotoNode(label_2))
        self.instructions.append(cil.LabelNode(label_1))
        self.instructions.append(cil.AssignmentNode(node.computed_value, 0))
        self.instructions.append(cil.LabelNode(label_2))

    @visitor.when(AssignmentNode)
    def visit(self, node):
        self.visit(node.expr)
        node.computed_value = self.add_local()
        self.instructions.append(cil.AssignmentNode(node.computed_value, node.expr.computed_value))
        try:
            self.locals[node.id.value]
            self.instructions.append(cil.AssignmentNode(node.id.value, node.computed_value))
        except KeyError:
            try:
                self.params[node.id.value]
                self.instructions.append(cil.AssignmentNode(node.id.value, node.computed_value))
            except KeyError:
                self.instructions.append(cil.SetAttributeNode(self.params['self'], node.id.value, node.computed_value))

    @visitor.when(DispatchNode)
    def visit(self, node):
        if node.expr:
            self.visit(node.expr)
            expr_value = node.expr.computed_value
        else:
            expr_value = self.params['self']
        
        if not node.type: 
            local_1 = self.add_local()
            self.instructions.append(cil.TypeOfNode(local_1, expr_value))

        for arg in node.args:
            self.visit(arg)
            local_2 = self.add_local()
            self.instructions.append(cil.AssignmentNode(local_2, arg.computed_value))
            self.instructions.append(cil.ArgumentNode(local_2))
        
        node.computed_value = self.add_local()
        if node.type:
            self.instructions.append(cil.StaticCallNode(node.computed_value, f'{node.type.value}.{node.id.value}'))
        else:
            self.instructions.append(cil.DynamicCallNode(node.computed_value, local_1, node.id.value))

    def add_local(self, value=None):
        if value is None:
            value = f'local_{len(self.locals)}'
        local = cil.LocalNode(value)
        self.locals[value] = local
        return local

    def add_data(self, value):
        try:
            return self.data[value].id
        except KeyError:
            self.data[value] =  cil.DataNode(f'data_{len(self.data)}', value) 
            return self.data[value].id
    
    def add_local_data(self, value):
        try:
            return self.local_data[value]
        except KeyError:
            local = self.add_local()
            self.local_data[value] = local
            self.instructions.append(cil.LoadAddressNode(local, value))
            return local

    def add_label(self):
        self.label_count += 1
        return f'label_{self.label_count}'        