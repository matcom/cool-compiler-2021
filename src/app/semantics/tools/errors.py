class InternalError(Exception):
    @property
    def text(self):
        return "InternalError: " + self.args[0]


class SemanticError(Exception):
    @property
    def text(self):
        return "SemanticError: " + self.args[0]


class TypeError(SemanticError):
    @property
    def text(self):
        return "TypeError: " + self.args[0]


class AttributeError(SemanticError):
    @property
    def text(self):
        return "AttributeError: " + self.args[0]
