from app.semantics.tools.type import TypeBag, ErrorType
import itertools as itt


class VariableInfo:
    def __init__(self, name, vtype) -> None:
        self.name: str = name
        self.type: TypeBag = vtype

    def get_type(self) -> TypeBag or ErrorType:
        # if len(self.type.type_set) == 0:
        #     self.type = ErrorType()
        return self.type

    def __str__(self):
        return self.name + ":" + self.type


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.current_child = -1

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None) -> VariableInfo or None:
        locals = self.locals if index is None else itt.islice(
            self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            try:
                return (
                    self.parent.find_variable(vname, self.index)
                    if self.parent is not None
                    else None
                )
            except AttributeError:
                return None

    def get_variable(self, vname, index=None) -> VariableInfo:
        var = self.find_variable(vname, index)
        if var is None:
            raise Exception(f"Could not get variable {vname}.")

        return var

    def get_local_by_index(self, index):
        return self.locals[index]

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def next_child(self):
        self.current_child += 1
        return self.children[self.current_child]

    def reset(self):
        self.current_child = -1
        for child in self.children:
            child.reset()

    def get_all_names(self, s: str = "", level: int = 0):
        if self.locals:
            s += "\n ".join(
                [
                    x.name + ":" +
                    str([typex.name for typex in x.type.type_set])
                    for x in self.locals
                ]
            )
            s += "\n\n"
        for child in self.children:
            s = child.get_all_names(s, level + 1)
        return s
