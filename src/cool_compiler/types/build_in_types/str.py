from ..cool_type_build_in_manager import build_in_type
from ..type import Type
from ..tools import type_body_def
from . import *

@build_in_type
class String(Type):
    def __init__(self):
        super().__init__("String")
        type_body_def(self)
            
    @property
    def is_shield(self):
        return True

    def length(self):
        self.define_method("length", [], Int())
    
    def concat(self):
        self.define_method("concat", [("s", self)], self)

    def substr(self):
        self.define_method("substr", [("i", Int()), ("l", Int())], self )

