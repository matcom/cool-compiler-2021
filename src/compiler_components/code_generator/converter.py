from .converter_utils import *


class Converter:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = [CilDataNode('_empty', '')]
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        basic_types(self)

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    @property
    def labels(self):
        return self.current_function.labels
