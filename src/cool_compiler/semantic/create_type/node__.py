class Node:
    def get_pos_to_error(self, lineno, index):
        self.lineno = lineno
        self.index = index

class Feature(Node):
    pass

class Expresion(Node):
    pass

class Statement(Expresion):
    pass
