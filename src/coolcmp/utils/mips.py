from __future__ import annotations

from coolcmp.utils import ast


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, data, types, functions):
        self.data = data
        self.types = types
        self.functions = functions


class FunctionNode(Node):
    def __init__(self, name, params, local_vars):
        self.name = name
        self.params = params
        self.local_vars = local_vars
        self.instructions = []

    def parameter_address(self, name):
        """
        Get the
        """


class InstructionNode(Node):
    pass


class DataNode(Node):
    def __init__(self, label):
        self.label = label


class StringNode(DataNode):
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value


class SWNode(Node):
    def __init__(self, reg, address):
        self.reg = reg
        self.address = address


class LINode(Node):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value


class Type:
    def __init__(self, label, address, attrs, methods, index, default=[]):
        self.label = label
        self.address = address
        self.attrs = attrs
        self.default_attrs = dict(default)
        self.methods = methods
        self.index = index

    def length(self):
        return len(self.attrs)

    def __str__(self):
        return f"{self.label}-{self.address}-{self.attrs}-{self.default_attrs}-{self.methods}-{self.index}"
