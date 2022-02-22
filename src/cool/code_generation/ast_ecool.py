"""
ExtendedCool is a language similar to Cool, but with some additional
features like the new keyword null in the asignments and the creation of
a default constructor for every class defined in the program.
"""

import cool.semantics.utils.astnodes as cool
from cool.semantics.utils.scope import Type


class NullType(Type):
    def __init__(self):
        super().__init__("null")

    def conforms_to(self, other: "Type") -> bool:
        return True

    def bypass(self) -> bool:
        return True

    def __str__(self):
        return self.name


class NullNode(cool.AtomicNode):
    def __init__(self):
        super().__init__("null")
