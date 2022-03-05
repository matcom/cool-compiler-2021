import coolpyler.utils.meta as meta
import coolpyler.ast.cool.type_collected as type_collected

meta.from_module(type_collected)


class CoolClassNode(*meta.get_bases("CoolClassNode")):
    def __init__(self, lineno, columnno, type, features):
        super().__init__(lineno, columnno)
        self.type = type
        self.features = features


class CoolAttrDeclNode(*meta.get_bases("CoolAttrDeclNode")):
    def __init__(self, lineno, columnno, attr_info, body=None):
        super().__init__(lineno, columnno)
        self.attr_info = attr_info
        self.body = body


class CoolMethodDeclNode(*meta.get_bases("CoolMethodDeclNode")):
    def __init__(self, lineno, columnno, method_info, body):
        super().__init__(lineno, columnno)
        self.method_info = method_info
        self.body = body
