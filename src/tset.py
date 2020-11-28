class Tset:
    def __init__(self, parent=None):
        self.locals = {}
        self.parent = parent
        self.children = {}

    def create_child(self, node):
        child = Tset(self)
        self.children[node] = child
        return child

    def find_set(self, idx):
        if idx in self.locals.keys():
            return self.locals
        elif self.parent != None:
            return self.parent.find_set(idx)

        return None

    def __str__(self):
        output = ""

        for key, value in self.locals.items():
            output += "\t" + str(key) + ":" + str(value) + "\n"
        for key, chil in self.children.items():
            output += "\n"
            try:
                output += key.id + "--->"
            except AttributeError:
                output += "let or case --->"
            output += "\n"
            output += str(chil)
        return output
