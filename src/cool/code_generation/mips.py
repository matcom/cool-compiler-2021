from ast import List


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dotdata: List["DataNode"], dottext: List["InstructionNode"]):
        self.dotdata = dotdata
        self.dottext = dottext


class DataNode(Node):
    def __init__(self):
        pass


class InstructionNode(Node):
    def __init__(self):
        pass
