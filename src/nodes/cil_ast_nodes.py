class CilAST:
    def __init__(self):
        pass

class ProgramNode(CilAST):
    def __init__(self, types, data, code):
        super(ProgramNode, self).__init__()
        self.types = types
        self.data = data
        self.code = code

class TypeNode(CilAST):
    def __init__(self, name):
        super(TypeNode, self).__init__()
        self.name = name
        self.attributes = []
        self.methods = {}

class FunctionNode(CilAST):
    def __init__(self, name, params = [], local_vars = [], instructions = []):
        super(FunctionNode, self).__init__()
        self.name = name
        self.params = params
        self.local_vars = local_vars
        self.instructions = instructions