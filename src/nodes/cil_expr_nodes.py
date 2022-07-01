from .cil_ast_nodes import CilAST

class CilExprNode(CilAST):
    def __init__(self):
        super(CilExprNode, self).__init__()

class ParamDeclarationNode(CilExprNode):
    def __init__(self, name):
        super(ParamDeclarationNode, self).__init__()
        self.name = name

class LocalVariableDeclarationNode(CilExprNode):
    def __init__(self, name):
        super(LocalVariableDeclarationNode, self).__init__()
        self.name = name

class AssignNode(CilExprNode):
    def __init__(self, dest, expression):
        super(AssignNode, self).__init__()
        self.dest = dest
        self.expression = expression

class UnaryOperatorNode(CilExprNode):
    def __init__(self, local_var, op, expr_value):
        super(UnaryOperatorNode, self).__init__()
        self.local_var = local_var
        self.op = op
        self.expr_value = expr_value

class BinaryOperatorNode(CilExprNode):
    def __init__(self, local_var, left, op, right):
        super(BinaryOperatorNode, self).__init__()
        self.local_var = local_var
        self.left = left
        self.op = op
        self.right = right

class GetAttrNode(CilExprNode):
    def __init__(self, variable, type, attr, instance):
        super(GetAttrNode, self).__init__()
        self.variable = variable
        self.type =  type
        self.attr = attr
        self.instance = instance

class SetAttrNode(CilExprNode):
    def __init__(self, type, attr, value, instance):
        super(SetAttrNode, self).__init__()
        self.type = type
        self.attr = attr
        self.value = value
        self.instance = instance

class AllocateNode(CilExprNode):
    def __init__(self, local_var, type, tag):
        super(AllocateNode, self).__init__()
        self.local_var = local_var
        self.type = type
        self.tag = tag

class TypeOfNode(CilExprNode):
    def __init__(self, local_var, variable):
        super(TypeOfNode, self).__init__()
        self.local_var = local_var
        self.variable = variable

class CallNode(CilExprNode):
    def __init__(self, local_var, type, method_name, params):
        super(CallNode, self).__init__()
        self.local_var = local_var
        self.method_name = method_name
        self.params = params
        self.type = type

class VCallNode(CilExprNode):
    def __init__(self, local_var, type, method_name, params, instance):
        super(VCallNode, self).__init__()
        self.local_var = local_var
        self.type = type
        self.method_name = method_name
        self.params = params
        self.instance = instance

class ArgNode(CilExprNode):
    def __init__(self, arg_name):
        super(ArgNode, self).__init__()
        self.arg_name = arg_name

class IfGotoNode(CilExprNode):
    def __init__(self, variable, label):
        super(IfGotoNode, self).__init__()
        self.variable = variable
        self.label = label

class LabelNode(CilExprNode):
    def __init__(self, label):
        super(LabelNode, self).__init__()
        self.label = label

class GotoNode(CilExprNode):
    def __init__(self, label):
        super(GotoNode, self).__init__()
        self.label = label

class ReturnNode(CilExprNode):
    def __init__(self, return_value):
        super(ReturnNode, self).__init__()
        self.return_value = return_value

class IntegerNode(CilExprNode):
    def __init__(self, value):
        super(IntegerNode, self).__init__()
        self.valye = value

class StringNode(CilExprNode):
    def __init__(self, value):
        super(StringNode, self).__init__()
        self.valye = value

class LoadVoidNode(CilExprNode):
    def __init__(self, local_var):
        super(LoadVoidNode, self).__init__()
        self.local_var = local_var

class LoadStrNode(CilExprNode):
    def __init__(self, local_var, msg):
        super(LoadStrNode, self).__init__()
        self.local_var = local_var
        self.msg = msg

class LoadIntNode(CilExprNode):
    def __init__(self, local_var, num):
        super(LoadIntNode, self).__init__()
        self.local_var = local_var
        self.num = num

class LengthNode(CilExprNode):
    def __init__(self, local_var, variable):
        super(LengthNode, self).__init__()
        self.local_var = local_var
        self.variable = variable

class ConcatNode(CilExprNode):
    def __init__(self, local_var, str1, str2, len1, len2):
        super(ConcatNode, self).__init__()
        self.local_var = local_var
        self.str1 = str1
        self.str2 = str2
        self.len1 = len1
        self.len2 = len2

class SubStrNode(CilExprNode):
    def __init__(self, local_var, index, str, len):
        super(SubStrNode, self).__init__()
        self.local_var = local_var
        self.index = index
        self.str = str
        self.len = len

class StrNode(CilExprNode):
    def __init__(self,local_var, num):
        super(StrNode, self).__init__()
        self.local_var = local_var
        self.num = num

class ReadNode(CilExprNode):
    def __init__(self, line):
        super(ReadNode, self).__init__()
        self.line = line

class ReadIntegerNode(ReadNode):
    pass

class ReadStringNode(ReadNode):
    pass

class PrintNode(CilExprNode):
    def __init__(self, line):
        super(PrintNode, self).__init__()
        self.line = line

class PrintIntegerNode(PrintNode):
    pass

class PrintStringNode(PrintNode):
    pass

class AbortNode(CilExprNode):
    def __init__(self):
        super(AbortNode, self).__init__()

class CaseNode(CilExprNode):
    def __init__(self, local_expr, first_label):
        super(CaseNode, self).__init__()
        self.local_expr = local_expr
        self.first_label = first_label

class ActionNode(CilExprNode):
    def __init__(self, local_expr, tag, max_tag, next_label):
        super(ActionNode, self).__init__()
        self.local_expr = local_expr
        self.tag = tag
        self.max_tag = max_tag
        self.next_label = next_label

class StringEqualsNode(CilExprNode):
    def __init__(self, local_var, str1, str2):
        super(StringEqualsNode, self).__init__()
        self.local_var = local_var
        self.str1 = str1
        self.str2 = str2

class IsVoidNode(CilExprNode):
    def __init__(self, local_var, expr):
        super(IsVoidNode, self).__init__()
        self.local_var = local_var
        self.expr = expr

class CopyNode(CilExprNode):
    def __init__(self, local_var, type):
        super(CopyNode, self).__init__()
        self.local_var = local_var
        self.type = type