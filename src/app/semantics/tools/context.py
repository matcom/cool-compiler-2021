from app.semantics.tools.errors import *
from app.semantics.tools.type import TypeBag, Type, SelfType
from typing import Dict


class Context:
    def __init__(self) -> None:
        self.types = {}
        self.type_graph: Dict = None

    def create_type(self, name: str) -> Type:
        if name in self.types:
            raise SemanticError(
                f"Type with the same name ({name}) already exists.")
        typex = self.types[name] = Type(name)
        return typex

    def get_type(
        self,
        name: str,
        selftype=True,
        autotype=True,
        unpacked=False,
    ) -> Type or TypeBag:
        if selftype and name == "SELF_TYPE":
            # raise TypeError(f"Cannot use SELF_TYPE.")
            return TypeBag({SelfType()})
        if autotype and name == "AUTO_TYPE":
            return TypeBag(self.types, [self.types["Object"]])
        try:
            if unpacked:
                return self.types[name]
            return TypeBag({self.types[name]})
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')

    def get_method_by_name(self, name: str, args: int) -> list:
        def dfs(root: str, results: list):
            try:
                for typex in self.type_graph[root]:
                    for method in self.types[typex].methods:
                        if name == method.name and args == len(method.param_names):
                            results.append((self.types[typex], method))
                            break
                    else:
                        dfs(typex, results)
            except KeyError:
                pass

        results = []
        dfs("Object", results)
        return results

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values()
                          for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)
