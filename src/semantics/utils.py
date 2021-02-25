<<<<<<< HEAD
def conform_to_condition(type_set, parent) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result

def order_set_by_index(type_set):
    return sorted(list(type_set), key = lambda x: x.index)

def set_intersection(parent, type_set) -> set:
=======
from semantics.tools import Type, ErrorType, AutoType

def conforms(type1:Type, type2:Type):
    if isinstance(type1, ErrorType) or isinstance(type2, ErrorType):
        return ErrorType()
    if not isinstance(type1, AutoType) and isinstance(type2, AutoType):
        type2.set_upper_limmit([type1])
        return type1
    if not isinstance(type1, AutoType):
            type1 = AutoType("TEMP01", [type1], {type1})
    if not isinstance(type2, AutoType):
            type2 = AutoType("TEMP02", [type2], {type2})
    
    print("type 1 set:", ", ".join(typex.name for typex in type1.type_set))
    print("type 2 set:", ", ".join(typex.name for typex in type2.type_set))

    condition_set_list, conform_set_list = conforming(type1, type2)
    type1.set_new_conditions(condition_set_list, conform_set_list)
    
    print("Conditions obtained", [[typex.name for typex in type_set] for type_set in condition_set_list])
    print("Conforms obtained", [[typex.name for typex in type_set] for type_set in conform_set_list])
    print("Updated set:", ", ".join(typex.name for typex in type1.type_set),"\n")
    return type1

def conforming(auto1:AutoType, auto2:AutoType):
    ord_types2 = sorted(list(auto2.type_set), lambda x: x.index)

    condition_set_list = []
    conform_set_list = []
    for type2 in ord_types2:
        conforms = conform_intersection(auto1.type_set, type2)
        for i in range(len(condition_set_list)):
            prev_conform = conform_set_list[i]
            if len(prev_conform) == len(conforms) and len(conforms.intersection(prev_conform)) == len(conforms):
                condition_set_list[i].add(type2)
                break
        else:
            condition_set_list.append(set([type2]))
            conform_set_list.append(conforms)
    return condition_set_list, conform_set_list

def conform_intersection(type_set, parent) -> set:
>>>>>>> Added Type Builder and Type Collector
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
<<<<<<< HEAD
    return set_result

def from_dict_to_set(types:dict):
    type_set = set()
    for typex in types:
        type_set.add(types[typex])
    return type_set
=======
    return set_result
>>>>>>> Added Type Builder and Type Collector
