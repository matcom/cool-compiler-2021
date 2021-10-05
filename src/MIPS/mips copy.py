from MIPS.builder import builder_proto
import Utils.visitor as visitor
import MIPS.ast as mips

from CIL.ast import *

class MIPS:
    def __init__(self):
        pass

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.class_tag = {type.name: i for i, type in enumerate(node.types)}
        
        self.text = []
        self.data = []

        self.data_str = {}
        self.data_int = {}

        self.data_proto = {proto.id : proto for proto in builder_proto(self.class_tag)}
   
        for data in node.data:
            self.visit(data)
        
        for type in node.types:
            self.visit(type)

        #for code in node.code:
        #    self.visit(code)

        
        return mips.ProgramNode(self.data, self.text)
    
    @visitor.when(DataNode)
    def visit(self, node):
        self.data_str[node.id] = self.add_str_const(node.value)

    @visitor.when(TypeNode)
    def visit(self, node):
        self.data_str[f'{node.name}_name'] = self.add_str_const(node.name)

        self.data.append(mips.DataNode(f'{node.name}_disp', 
            [mips.DataValuesNode('word', f'{meth[1]}.{meth[0]}') for meth in node.meths]))
        
        if node.name in ['Object', 'IO', 'Int', 'String', 'Bool']:
            self.data.append(self.data_proto[f'{node.name}_proto'])
        else:
            proto = [
                mips.DataValuesNode('word', self.class_tag[node.name]),
                mips.DataValuesNode('word', 3 + len(node.attrs)),
                mips.DataValuesNode('word', f'{node.name}_disp')]
            for attr in node.attrs:
                if attr[1].name in ['String', 'Int', 'Bool']:
                    proto.append(mips.DataValuesNode('word', f'{attr[1].name}_proto'))
                else:
                    proto.append(mips.DataValuesNode('word', 0))
            proto.append(mips.DataValuesNode('word', -1))
            self.data.append(mips.DataNode(f'{node.name}_proto', proto))

    @visitor.when(CodeNode)
    def visit(self, node):
        pass

    def add_str_const(self, value=''):
        name = f'str_const_{len(self.data_str)}'
        self.data.append(mips.DataNode(name, [
            mips.DataValuesNode('word', self.class_tag['String']),
            mips.DataValuesNode('word', 5),
            mips.DataValuesNode('word', 'String_disp'),
            mips.DataValuesNode('word', self.add_int_const(len(value))),
            mips.DataValuesNode('ascii', value if value else 0),
            mips.DataValuesNode('word', -1) ]))
        return name
            
    def add_int_const(self, value=0):
        name = f'int_const_{len(self.data_str)}'
        self.data.append(mips.DataNode(name, [
            mips.DataValuesNode('word', self.class_tag['Int']),
            mips.DataValuesNode('word', 4),
            mips.DataValuesNode('word', 'Int_disp'),
            mips.DataValuesNode('word', value),
            mips.DataValuesNode('word', -1)]))
        return name