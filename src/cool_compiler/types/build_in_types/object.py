from ..cool_type_build_in_manager import build_in_type
from ..type import Type
from ..tools import type_body_def
from . import *

@build_in_type
class Object(Type):
    def __init__(self):
        super().__init__("Object")
        type_body_def(self)
        
    def copy(self):
        self.define_method("copy", [], Self())

    def abort(self):
        self.define_method("abort", [], self )

    def type_name(self):
        self.define_method("type_name", [], String())