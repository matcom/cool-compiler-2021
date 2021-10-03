class Node:
    def __init__(self, static_type = None) -> None:
        self.static_type = static_type

    def get_pos_to_error(self, lineno, index):
        self.lineno = lineno
        self.index = index

class Feature(Node):
    pass

class Expresion(Node):
    pass

class Statement(Expresion):
    pass
