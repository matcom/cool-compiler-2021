from MIPS.ast import *

def builder_proto(class_tag):
    return [
        DataNode('Object_proto', [
            DataValuesNode('word', class_tag['Object']),
            DataValuesNode('word', 3),
            DataValuesNode('word', 'Object_disp'),
            DataValuesNode('word', -1)]),
        DataNode('IO_proto', [
            DataValuesNode('word', class_tag['IO']),
            DataValuesNode('word', 3),
            DataValuesNode('word', 'IO_disp'),
            DataValuesNode('word', -1)]),
        DataNode('Int_proto', [
            DataValuesNode('word', class_tag['Int']),
            DataValuesNode('word', 4),
            DataValuesNode('word', 'Int_disp'),
            DataValuesNode('word', 0),
            DataValuesNode('word', -1)]),
        DataNode('String_proto', [
            DataValuesNode('word', class_tag['String']),
            DataValuesNode('word', 5),
            DataValuesNode('word', 'String_disp'),
            DataValuesNode('word', 'Int_proto'),
            DataValuesNode('byte', 0),
            DataValuesNode('word', -1)]),
        DataNode('Bool_proto', [
            DataValuesNode('word', class_tag['Bool']),
            DataValuesNode('word', 4),
            DataValuesNode('word', 'Bool_disp'),
            DataValuesNode('word', 0),
            DataValuesNode('word', -1)]),
    ]