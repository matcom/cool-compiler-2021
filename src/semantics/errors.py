class InternalError(Exception):
    @property
    def text(self):
        return "Internal Error: " + self.args[0]


class SemanticError(Exception):
    @property
    def text(self):
        return "Semantic Error: " + self.args[0]


class TypeError(SemanticError):
    @property
    def text(self):
        return "Type Error: " + self.args[0]


class AttributeError(SemanticError):
    @property
    def text(self):
        return "Attribute Error: " + self.args[0]