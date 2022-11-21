from ..cool_type_build_in_manager import build_in_type
from ..type import Type
from ..tools import type_body_def
from . import *
@build_in_type
class IO(Type):
    def __init__(self):
        super().__init__("IO")
        type_body_def(self)
        
    def out_string(self):
        self.define_method("out_string", [("x", String())], Self())
    
    def out_int(self):
        self.define_method("out_int", [("x", Int())], Self())

    def in_string(self):
        self.define_method("in_string", [], String())

    def in_int(self):
        self.define_method("in_int", [], Int())
