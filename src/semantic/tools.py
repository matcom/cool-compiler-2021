

class VariableInfo:
    def __init__(self, name, vtype, index=None):
        self.name = name
        self.type = vtype
        self.index = index

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)

