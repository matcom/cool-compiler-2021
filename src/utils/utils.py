import os
import itertools
from semantic.types import Type, SelfType

class Token:
    def __init__(self, line, column, type, lex):
        self.line = line
        self.column = column
        self.type = type
        self.lex = lex

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type} : {self.lex}'

    def __repr__(self):
        return str(self)

class Utils:

    @staticmethod
    def GetName(input_file : str) -> str:
        path,_ = os.path.splitext(input_file)
        arr = path.split('/')
        name = arr[-1]
        return name

    @staticmethod
    def Write(path : str, extention : str, text : str) -> None:
        with open(path + extention, 'w+') as file:
            file.write(text)

    def GetRulesParsing():
        path = 'parsing/parser.out'
        file = open(path, encoding='utf-8')
        lines = file.readlines()
        rules = [ line for idx,line in enumerate(lines) 
                        if idx >= 2 and line.count('Rule', 0, len(line)) > 0 ]
        file.close
        return rules

    @staticmethod
    def PathToObjet(typex) -> list:
        print(f'tipo de tipex es {type(typex)} en PathToObject')
        path = []
        c_type = typex

        while c_type:
            path.append(c_type)
            c_type = c_type.parent

        path.reverse()
        return path

    @staticmethod
    def GetCommonBaseType(types):
        print(f'tipo de types es {type(types)} en GetCommonBaseType')
        paths = [ Utils.PathToObjet(typex) for typex in types ]
        tuples = zip(*paths)

        for i, t in enumerate(tuples):
            gr = itertools.groupby(t)
            if len(list(gr)) > 1:
                return paths[0][i-1]

        print(f'tipo de paths[0][-1] es {type(paths[0][-1])} en GetCommonBaseType')
        return paths[0][-1]

    @staticmethod
    def GetType(typex : Type, current_type : Type) -> Type:
        return current_type if typex == SelfType() else typex

    @staticmethod
    def IsBasicType(type_name : str):
        return type_name in ['String', 'Int', 'Object', 'Bool', 'SELF_TYPE', 'IO']
