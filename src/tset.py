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
        for key, child in self.children.items():
            output += "\n"
            try:
                output += key.id + "--->"
            except AttributeError:
                output += "let or case --->"
            output += "\n"
            output += str(child)
        return output

    def clone(self):
        solve = Tset()
        solve.parent = self.parent
        for idx, typex in self.locals.items():
            solve.locals[idx] = typex.copy()

        for key, value in self.children.items():
            solve.children[key] = value.clone()

        return solve

    def compare(self, other):
        if len(self.locals) != len(other.locals) or len(self.children) != len(
            other.children
        ):
            return False

        for (idx, tset), (idx_other, tset_other) in zip(
            self.locals.items(), other.locals.items()
        ):
            if idx != idx_other or tset != tset_other:
                return False
        for (key, value), (key_other, value_other) in zip(
            self.children.items(), other.children.items()
        ):
            if key != key_other or not value.compare(value_other):
                return False
        return True

    def clean(self):
        for typex in self.locals.values():
            if "InferenceError" in typex:
                typex.remove("InferenceError")
            if "!static_type_declared" in typex:
                typex.remove("!static_type_declared")
        for child in self.children.values():
            child.clean()

