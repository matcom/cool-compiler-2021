from semantics.tools import Type, ErrorType, AutoType, TypeBag

def conforms(bag1:TypeBag, bag2:TypeBag):
    ordered_set = order_set_by_index(bag2.type_set)

    condition_list = []
    conform_list = []
    for condition in ordered_set:
        conform = conform_to_condition(bag1.type_set, condition)
        for i in range(len(condition_list)):
            conform_i = conform_list[i]
            if len(conform_i) == len(conform) and len(conform.intersection(conform_i)) == len(conform):
                condition_list[i].add(condition)
                break
        else:
            condition_list.append({condition})
            conform_list.append(conform)
    
    bag1.set_conditions(condition_list, conform_list)
    return bag1

def conform_to_condition(type_set, parent) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result

def join(bag1:TypeBag, bag2:TypeBag) -> TypeBag:
    ancestor_set = set()
    head_list = []
    ordered_set1 = order_set_by_index(bag1.type_set)
    ordered_set2 = order_set_by_index(bag2.type_set)
    ordered_set1, ordered_set2 = (ordered_set1, ordered_set2) if len(ordered_set1) < len(ordered_set2) else (ordered_set2, ordered_set1)
    for type1 in ordered_set1:
        same_branch = False
        previous_ancestor = None
        previous_type = None
        for type2 in ordered_set2:
            if same_branch and type2.conforms_to(previous_type):
                previous_type = type2
                continue
            common_ancestor = type1.least_common_ancestor(type2)
            previous_type = type2
            if not previous_ancestor:
                smart_add(ancestor_set, head_list, common_ancestor)
                previous_ancestor = common_ancestor
            else:
                if previous_ancestor == common_ancestor:
                    same_branch = True
                else:
                    same_branch = False
                    smart_add(ancestor_set, head_list, common_ancestor)
                    previous_ancestor = common_ancestor
    
    join_result = TypeBag(ancestor_set, head_list)
    return join_result

def join_list(type_list):
    typex = type_list[0]
    for i in range(1, len(type_list)):
        type_i = type_list[i]
        typex = join(typex, type_i)
    return typex

def smart_add(type_set:set, head_list:list, typex:Type):
    if isinstance(typex, TypeBag):
        return auto_add(type_set, head_list, typex)

    type_set.add(typex)
    there_is = False
    for i in range(len(head_list)):
        head = head_list[i]
        ancestor = typex.least_common_ancestor(head)
        if ancestor in type_set:
            there_is = True
            if ancestor == typex:
                head_list[i] = typex
                break
    if not there_is:
        head_list.append(typex)
    return head_list, type_set

def auto_add(type_set:set, head_list:list, bag:TypeBag):
    type_set = type_set.union(bag.type_set)
    aux = set(bag.heads)
    for i in range(len(head_list)):
        head_i = head_list[i]
        for head in bag.heads:
            ancestor = head_i.least_common_ancestor(head)
            if ancestor in type_set:
                head_i[i] = ancestor
                aux.pop(head)
                break
    head_list += [typex for typex in aux]
    return head_list, type_set

def order_set_by_index(type_set):
    return sorted(list(type_set), lambda x: x.index)

def from_dict_to_set(types:dict):
    type_set = set()
    for typex in types:
        type_set.add(types[typex])
    return type_set

def set_intersection(parent, type_set) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result