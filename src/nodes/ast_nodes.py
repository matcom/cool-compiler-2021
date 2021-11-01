class AST:
    def __init__(self):
        pass

class ProgramNode(AST):
    def __init__(self, classes):
        super(ProgramNode, self).__init__()
        self.classes = classes

class ClassNode(AST):
    def __init__(self, name, parent, features, row , col):
        super(ClassNode, self).__init__()
        self.name = name
        self.parent = parent
        self.features = features
        self.row = row
        self.col = col

class ClassMethodNode(AST):
    def __init__(self, name, params, expression, return_type, row , col):
        super(ClassMethodNode, self).__init__()
        self.name = name
        self.params = params
        self.expression = expression
        self.return_type = return_type
        self.row = row
        self.col = col

class AttrInitNode(AST):
    def __init__(self, name, attr_type, expression, row , col):
        super(AttrInitNode, self).__init__()
        self.name = name
        self.attr_type = attr_type
        self.expression = expression
        self.row = row
        self.col = col

class AttrDefNode(AST):
    def __init__(self, name, attr_type, row , col):
        super(AttrDefNode, self).__init__()
        self.name = name
        self.attr_type = attr_type
        self.row = row
        self.col = col

class LetInitNode(AST):
    def __init__(self, name, let_type, expression, row , col):
        super(LetInitNode, self).__init__()
        self.name = name
        self.let_type = let_type
        self.expression = expression
        self.row = row
        self.col = col

class LetDefNode(AST):
    def __init__(self, name, let_type, row , col):
        super(LetDefNode, self).__init__()
        self.name = name
        self.let_type = let_type
        self.row = row
        self.col = col

class FormalParamNode(AST):
    def __init__(self, name, param_type, row , col):
        super(FormalParamNode, self).__init__()
        self.name = name
        self.param_type = param_type
        self.row = row
        self.col = col