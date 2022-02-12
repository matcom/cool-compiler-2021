import coolpyler.ast.cool.base as base

class CoolProgramNode(base.CoolProgramNode):
    def __init__(self, lineno, columnno, classes):
        super().__init__(lineno, columnno)

        self.classes = classes

class CoolClassNode(base.CoolClassNode):
    def __init__(self, lineno, columnno, type, features):
        super().__init__(lineno, columnno)

        self.type = type
        self.features = features


class CoolAttrDeclNode(base.CoolAttrDeclNode):
    def __init__(self, lineno, columnno, attr_info, body=None):
        super().__init__(lineno, columnno)

        self.attr_info = attr_info
        self.body = body


class CoolMethodDeclNode(base.CoolMethodDeclNode):
    def __init__(self, lineno, columnno, method_info, body):
        super().__init__(lineno, columnno)

        self.method_info = method_info
        self.body = body
