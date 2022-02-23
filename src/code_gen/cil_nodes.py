class CIL_Node:
    pass


class ProgramCil(CIL_Node):
    def __init__(self, types, data, code):
        self.types = types
        self.data = data
        self.code = code


class TypeCil(CIL_Node):
    def __init__(self, idx, attributes=[], methods=[]):
        self.id = idx
        self.attributes = attributes
        self.methods = methods


class AttributeCil(CIL_Node):
    def __init__(self, idx):
        self.id = idx


class MethodCil(CIL_Node):
    def __init__(self, idx, ref):
        self.id = idx
        self.ref = ref


class FunctionCil(CIL_Node):
    def __init__(self, idx, args=[], localsx=[], body=[]):
        self.id = idx
        self.args = args
        self.locals = localsx
        self.body = body


class IfCil(CIL_Node):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label


class ArgCil(CIL_Node):
    def __init__(self, idx):
        self.id = idx


class LocalCil(CIL_Node):
    def __init__(self, idx):
        self.id = idx


class AssignmentCil(CIL_Node):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class StringCil(CIL_Node):
    def __init__(self, idx: str, text: str):
        self.id = idx
        self.text = text


class LabelCil(CIL_Node):
    def __init__(self, idx):
        self.id = idx


class GotoCil(CIL_Node):
    def __init__(self, label):
        self.label = label
