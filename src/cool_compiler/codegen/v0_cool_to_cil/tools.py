from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from .cool_to_cil_ast import super_value

class BaseCoolToCIL:
    def __init__(self) -> None:
        self.label_list = {}

    def parent_list(self, node: AST.CoolClass):
        parent_list = []
        parent = node
        while True:
            if parent is None: break
            parent_list.append(parent)
            parent = parent.parent

        parent_list.reverse()
        return parent_list


    def new_name(self, name, _dict = None):
        if _dict is None: _dict = self.label_list
        index = 0
        while True:
            try: 
                _ = _dict[f'{name}_{index}']
                index += 1
            except KeyError:
                _dict[f'{name}_{index}'] = 1
                return f'{name}_{index}'

    def map_type(self, name):
        try: return self.type_dir[name]
        except KeyError:
            self.type_dir[name] = len(self.type_dir.keys()) + 1
            return self.type_dir[name]

    def try_funsion(self, _list, var):
        if not _list[-1].can_fusion: return _list, var

        if _list[-1].x == var: return _list[0:-1], _list[-1].y