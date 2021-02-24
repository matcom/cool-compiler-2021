
class Attribute:
    def __init__(self, name, typex, index, tok=None):
        self.name = name
        self.type = typex
        self.index = index
        self.expr = None

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

