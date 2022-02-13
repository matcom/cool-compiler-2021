class AST:
    def __init__(self):
        self.static_type = None
    
    def pos(self, lineno, linepos):
        self.lineno = lineno
        self.linepos = linepos

    @property
    def clsname(self):
        return str(self.__class__.__name__)


# ############################## PROGRAM, TYPE AND OBJECT ##############################


class Program(AST):
    def __init__(self, classes):
        super(Program, self).__init__()
        self.classes = classes


class Class(AST):
    def __init__(self, name, parent, features):
        super(Class, self).__init__()
        self.name = name
        self.parent = parent
        self.features = features


class ClassFeature(AST):
    def __init__(self):
        super(ClassFeature, self).__init__()


class ClassMethod(ClassFeature):
    def __init__(self, name, formal_params, return_type, body):
        super(ClassMethod, self).__init__()
        self.name = name
        self.formal_params = formal_params
        self.return_type = return_type
        self.body = body


class ClassAttribute(ClassFeature):
    def __init__(self, name, attr_type, init_expr):
        super(ClassAttribute, self).__init__()
        self.name = name
        self.attr_type = attr_type
        self.init_expr = init_expr


class FormalParameter(ClassFeature):
    def __init__(self, name, param_type):
        super(FormalParameter, self).__init__()
        self.name = name
        self.param_type = param_type

class Formal(ClassFeature):
    def __init__(self, name, param_type, init_expr):
        super(Formal, self).__init__()
        self.name = name
        self.param_type = param_type
        self.init_expr = init_expr


class Object(AST):
    def __init__(self, name):
        super(Object, self).__init__()
        self.name = name


class Self(Object):
    def __init__(self):
        super(Self, self).__init__("self")


# ############################## CONSTANTS ##############################

class Constant(AST):
    def __init__(self):
        super(Constant, self).__init__()

class Integer(Constant):
    def __init__(self, content):
        super(Integer, self).__init__()
        self.content = content

class String(Constant):
    def __init__(self, content):
        super(String, self).__init__()
        self.content = content

class Boolean(Constant):
    def __init__(self, content):
        super(Boolean, self).__init__()
        self.content = content

# ############################## EXPRESSIONS ##############################


class Expr(AST):
    def __init__(self):
        super(Expr, self).__init__()


class NewObject(Expr):
    def __init__(self, new_type):
        super(NewObject, self).__init__()
        self.type = new_type



class IsVoid(Expr):
    def __init__(self, expr):
        super(IsVoid, self).__init__()
        self.expr = expr

class Assignment(Expr):
    def __init__(self, instance, expr):
        super(Assignment, self).__init__()
        self.instance = instance
        self.expr = expr


class Block(Expr):
    def __init__(self, expr_list):
        super(Block, self).__init__()
        self.expr_list = expr_list


class DynamicDispatch(Expr):
    def __init__(self, instance, method, arguments):
        super(DynamicDispatch, self).__init__()
        self.instance = instance
        self.method = method
        self.arguments = arguments if arguments is not None else list()



class StaticDispatch(Expr):
    def __init__(self, instance, dispatch_type, method, arguments):
        super(StaticDispatch, self).__init__()
        self.instance = instance
        self.dispatch_type = dispatch_type
        self.method = method
        self.arguments = arguments if arguments is not None else list()


class Let(Expr):
    def __init__(self, declarations, body):
        super(Let, self).__init__()
        self.declarations = declarations
        self.body = body


class If(Expr):
    def __init__(self, predicate, then_body, else_body):
        super(If, self).__init__()
        self.predicate = predicate
        self.then_body = then_body
        self.else_body = else_body


class WhileLoop(Expr):
    def __init__(self, predicate, body):
        super(WhileLoop, self).__init__()
        self.predicate = predicate
        self.body = body


class Case(Expr):
    def __init__(self, expr, actions):
        super(Case, self).__init__()
        self.expr = expr
        self.actions = actions



class Action(AST):
    def __init__(self, name, action_type, body):
        super(Action, self).__init__()
        self.name = name
        self.action_type = action_type
        self.body = body



# ############################## UNARY OPERATIONS ##################################


class UnaryOperation(Expr):
    def __init__(self):
        super(UnaryOperation, self).__init__()


class IntegerComplement(UnaryOperation):
    def __init__(self, integer_expr):
        super(IntegerComplement, self).__init__()
        self.symbol = "~"
        self.integer_expr = integer_expr



class BooleanComplement(UnaryOperation):
    def __init__(self, boolean_expr):
        super(BooleanComplement, self).__init__()
        self.symbol = "!"
        self.boolean_expr = boolean_expr



# ############################## BINARY OPERATIONS ##################################


class BinaryOperation(Expr):
    def __init__(self):
        super(BinaryOperation, self).__init__()

class Addition(BinaryOperation):
    def __init__(self, first, second):
        super(Addition, self).__init__()
        self.symbol = "+"
        self.first = first
        self.second = second



class Subtraction(BinaryOperation):
    def __init__(self, first, second):
        super(Subtraction, self).__init__()
        self.symbol = "-"
        self.first = first
        self.second = second


class Multiplication(BinaryOperation):
    def __init__(self, first, second):
        super(Multiplication, self).__init__()
        self.symbol = "*"
        self.first = first
        self.second = second


class Division(BinaryOperation):
    def __init__(self, first, second):
        super(Division, self).__init__()
        self.symbol = "/"
        self.first = first
        self.second = second


class Equal(BinaryOperation):
    def __init__(self, first, second):
        super(Equal, self).__init__()
        self.symbol = "="
        self.first = first
        self.second = second


class LessThan(BinaryOperation):
    def __init__(self, first, second):
        super(LessThan, self).__init__()
        self.symbol = "<"
        self.first = first
        self.second = second


class LessThanOrEqual(BinaryOperation):
    def __init__(self, first, second):
        super(LessThanOrEqual, self).__init__()
        self.symbol = "<="
        self.first = first
        self.second = second