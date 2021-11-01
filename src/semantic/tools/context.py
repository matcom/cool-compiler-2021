from .type import *
from .error import SemanticException

class Context:
    def __init__(self):
        self.types = {}
        self.graph = {}
        self.classes = {}
        self.types['ErrorType'] = Error_Type()

    def create_builtin_types(self):
        self.types['SELF_TYPE'] = Type('SELF_TYPE')

        self.types['Object'] = Object_Type()
        self.types['IO'] = IO_Type()
        self.types['String'] = String_Type()
        self.types['Int'] = Int_Type()
        self.types['Bool'] = Bool_Type()
        self.graph['Object'] = ['IO', 'String', 'Bool', 'Int']
        self.graph['IO'] = []
        self.graph['String'] = []
        self.graph['Int'] = []
        self.graph['Bool'] = []

        self.types['IO'].set_parent(self.types['Object'])
        self.types['String'].set_parent(self.types['Object'])
        self.types['Int'].set_parent(self.types['Object'])
        self.types['Bool'].set_parent(self.types['Object'])

        self.types['Object'].define_method('abort', [], [], self.types['Object'])
        self.types['Object'].define_method('type_name', [], [], self.types['String'])
        self.types['Object'].define_method('copy', [], [], self.types['SELF_TYPE'])

        self.types['IO'].define_method('out_string', ['x'], [self.types['String']], self.types['SELF_TYPE'])
        self.types['IO'].define_method('out_int', ['x'], [self.types['Int']], self.types['SELF_TYPE'])
        self.types['IO'].define_method('in_string', [], [], self.types['String'])
        self.types['IO'].define_method('in_int', [], [], self.types['Int'])

        self.types['String'].define_method('length', [], [], self.types['Int'])
        self.types['String'].define_method('concat', ['s'], [self.types['String']], self.types['String'])
        self.types['String'].define_method('substr', ['i', 'l'], [self.types['Int'], self.types['Int']], self.types['String'])



    def create_type(self, node):
        if node.name in self.types:
            raise SemanticException(
                f'Type with the same name ({node.name}) already in context.')
        typex = self.types[node.name] = Type(node.name)
        self.classes[node.name] = node
        if not self.graph.__contains__(node.name):
            self.graph[node.name] = []
        if self.graph.__contains__(node.parent):
            self.graph[node.parent].append(node.name)
        else:
            self.graph[node.parent] = [node.name]
        return typex

    def get_type(self, name: str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticException(f'Type "{name}" is not defined.')

    def set_type_tags(self, node='Object', tag=0):
        self.types[node].tag = tag
        for i,t in enumerate(self.graph[node]):
            self.set_type_tags(t, tag + i + 1)
            
    def set_type_max_tags(self, node='Object'):
        if not self.graph[node]:
            self.types[node].max_tag = self.types[node].tag
        else:
            for t in self.graph[node]:
                self.set_type_max_tags(t)
            maximum = 0
            for t in self.graph[node]:
                maximum = max(maximum, self.types[t].max_tag)
            self.types[node].max_tag = maximum
            

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)
