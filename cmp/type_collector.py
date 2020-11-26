import cmp.visitor as visitor
from cmp.semantic import SemanticError, Type, Context, ObjectType, IOType, StringType, IntType, BoolType, SelfType, AutoType
from cmp.ast import ProgramNode, ClassDeclarationNode

built_in_types = []


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
        self.parent = {}
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.define_built_in_types()
        
        # Adding built-in types to context
        for typex in built_in_types:
            self.context.types[typex.name] = typex

        for declaration in node.declarations:
            self.visit(declaration)

        self.check_parents()
        self.check_cyclic_inheritance()

        # Order class declarations according to their depth in the inheritance tree
        node.declarations = self.order_types(node)
       
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        # flag will be True if the class is succesfully added to the context
        flag = False 
        try:
            self.context.create_type(node.id)
            flag = True
            self.parent[node.id] = node.parent
        except SemanticError as ex:
            self.errors.append(ex.text)

        # changing class id so it can be added to context
        while not flag:
            node.id = f'1{node.id}'
            try:
                self.context.create_type(node.id)
                flag = True
                self.parent[node.id] = node.parent
            except SemanticError:
                pass
    
    def define_built_in_types(self):
        objectx = ObjectType()
        iox = IOType()
        intx = IntType()
        stringx = StringType()
        boolx = BoolType()
        self_type = SelfType()
        autotype = AutoType()

        # Object Methods
        objectx.define_method('abort', [], [], objectx)
        objectx.define_method('type_name', [], [], stringx)
        objectx.define_method('copy', [], [], self_type)

        # IO Methods
        iox.define_method('out_string', ['x'], [stringx], self_type)
        iox.define_method('out_int', ['x'], [intx], self_type)
        iox.define_method('in_string', [], [], stringx)
        iox.define_method('in_int', [], [], intx)

        # String Methods
        stringx.define_method('length', [], [], intx)
        stringx.define_method('concat', ['s'], [stringx], stringx)
        stringx.define_method('substr', ['i', 'l'], [intx, intx], stringx)
        
        # Setting Object as parent
        iox.set_parent(objectx)
        stringx.set_parent(objectx)
        intx.set_parent(objectx)
        boolx.set_parent(objectx)

        built_in_types.extend([objectx, iox, stringx, intx, boolx, self_type, autotype])
        
    def check_parents(self):
        for item in self.parent.keys():
            item_type = self.context.get_type(item)
            if self.parent[item] is None:
                # setting Object as parent
                item_type.set_parent(built_in_types[0])
            else:
                try:
                    typex = self.context.get_type(self.parent[item])
                    if not typex.can_be_inherited():
                        self.errors.append(f'Class {item} can not inherit from {typex.name}')
                        typex = built_in_types[0]
                    item_type.set_parent(typex)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    item_type.set_parent(built_in_types[0])
    

    def check_cyclic_inheritance(self):
        flag = []
        
        def find(item):
            for i, typex in enumerate(flag):
                if typex.name == item.name:
                    return i
            return len(flag)

        def check_path(idx, item):
            while True:
                flag.append(item)
                parent = item.parent
                if parent is None:
                    break
                pos = find(parent)
                if pos < len(flag):
                    if pos >= idx:
                        self.errors.append(f'Class {item.name} can not inherit from {parent.name}')
                        item.parent = built_in_types[0]
                    break
                item = parent

        for item in self.context.types.values():
            idx = find(item)
            if idx == len(flag):
                check_path(idx, item)
        


    def order_types(self, node):
        sorted_declarations = []
        flag = [False] * len(node.declarations)
        obj_name = built_in_types[0].name
        
        change = True
        while change:
            change = False

            current = []
            for i, dec in enumerate(node.declarations):
                if not flag[i]:
                    typex = self.context.get_type(dec.id)
                    if typex.parent.name in [item.id for item in sorted_declarations] or typex.parent.name == obj_name:
                        current.append(dec)
                        flag[i] = True
                        change = True
            
            sorted_declarations.extend(current)

        return sorted_declarations