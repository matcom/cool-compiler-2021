import MIPS.ast as mips
from MIPS.builder import *
import Utils.visitor as visitor

from CIL.ast import *

class MIPS:
    def __init__(self):
        self.data = ''
        self.text = ''
        self.text_local = ''
        
        self.int_data = ''
        self.string_data = ''
        self.bool_data = ''

        self.string_const = {}
        self.int_const = {}
        
        self.bool_const = {
            0:'bool_const_0', 
            1:'bool_const_1'}
    
    def __str__(self):
        data = self.string_data + self.int_data
        data +=  self.bool_data + self.data

        text = all_init
        for init in self.functions_init:
            text += init
        text += self.text
        
        return f'\t\t.data\n{data}\n\t\t.text\n{text}'

    def add_data(self, value):
        self.data += f'{value}'

    def add_int_const(self, value=0):
        name = f'int_const_{len(self.int_const)}'
        try:
            return self.int_const[value]
        except KeyError:
            tag = self.class_tag['Int']
            self.int_data += add_int(name, str(self.class_tag['Int']), str(value))
            self.int_const[value] = name
            return name
    
    def add_string_const(self, value=''):
        name = f'string_const_{len(self.string_const)}'
        try:
            return self.string_const[value]
        except KeyError:
            length = self.add_int_const(len(value))
            self.string_data += add_string(name, str(self.class_tag['String']), length, value)
            self.string_const[value] = name
            return name

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.name_tab = ''
        self.object_tab = ''
        self.disp = ''
        self.proto = ''
        self.attr_name = {}
        self.attr_type = {}
        self.functions_init = []
        self.class_tag = {type.name:i for i, type in enumerate(node.types)}

        self.bool_data += add_bool(str(self.class_tag['Bool']), 0)
        self.bool_data += add_bool(str(self.class_tag['Bool']), 1)
        self.add_int_const(0)
        self.add_string_const('')

        for type in node.types:
            self.visit(type)

        self.add_data('name_tab:\n' + self.name_tab)
        self.add_data('object_tab:\n' + self.object_tab)
        self.add_data(self.disp)
        self.add_data(self.proto)
        
        self.cil_string = {}
        for dat in node.data:
            self.visit(dat)

        self.text += basic_build
        
        for code in node.code:
            self.visit(code)

        self.text +=  main

        self.add_data('heap:\n\t\t.word\t0')
        return str(self)

    @visitor.when(TypeNode)
    def visit(self, node):
        self.name_tab += create_name_item(self.add_string_const(node.name))
        self.object_tab += create_object_item(node.name)
        self.disp += create_disp(node.name, node.meths)
        self.proto += create_proto(node.name, self.class_tag[node.name], node.attrs)
        self.attr_name[node.name] = [attr[0] for attr in node.attrs]
        self.attr_type[node.name] = [attr[1].name for attr in node.attrs]
    
    @visitor.when(DataNode)
    def visit(self, node):
        self.add_string_const(node.value)
        self.cil_string[node.id] = node.value

    @visitor.when(CodeNode)
    def visit(self, node):
        self.current_type = node.type

        try:
            self.current_attr_name = self.attr_name[self.current_type]
            self.current_attr_type = self.attr_type[self.current_type]
        except KeyError:
            pass

        self.text_local = ''  
        for inst in node.instrs:
            self.visit(inst)
        
        if node.id == 'init':
            self.functions_init.append(call_methodo(node.name, self.text_local))
        else:
            self.text += call_methodo(node.name, self.text_local)
            
        
    @visitor.when(SetAttributeNode)
    def visit(self, node):
        i = self.current_attr_name.index(node.value_2)
        if self.current_attr_type[i] == 'Int':
            self.text_local += f'        la      $a0 {self.add_int_const(node.value_3)}\n'
            self.text_local += f'        sw      $a0 {(3+i)*4}($s0)\n'
        if self.current_attr_type[i] == 'String':
            temp = self.add_string_const(self.cil_string[node.value_3])
            self.text_local += f'        la      $a0 {temp}\n'
            self.text_local += f'        sw      $a0 {(3+i)*4}($s0)\n'
        if self.current_attr_type[i] == 'Bool':
            self.text_local += f'        la      $a0 {self.bool_const[node.value_3]}\n'
            self.text_local += f'        sw      $a0 {(3+i)*4}($s0)\n'

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        self.cil_string[node.value_1] = self.cil_string[node.value_2]
