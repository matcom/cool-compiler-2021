class Stack:
    def __init__(self, node) -> None:
        self.name = node.name
        self.init_size = len(node.param) + len(node.local) + 1
        self.list = []
        self.local_push = 0 

    def push(self, name):
        self.local_push += 1
        self.list.append(name)

    @property
    def initial_index(self):
        return (self.init_size - len(self.list)) * 4

    def index(self, name):
        return (len(self.list) - self.list.index(name) - 1) * 4
    
    def clean(self):
        self.list = self.list[0: len(self.list) - self.local_push]
        assert self.list[-1] == '$ra', "El ultimo de la pila no es $ra"
        self.local_push = 0

    def close(self):
        result = len(self.list) * 4
        self.local_push
        self.list = []
        return result