def conform_to_condition(type_set, parent) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result

def order_set_by_index(type_set):
    return sorted(list(type_set), key = lambda x: x.index)

def set_intersection(parent, type_set) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result

def from_dict_to_set(types:dict):
    type_set = set()
    for typex in types:
        type_set.add(types[typex])
    return type_set