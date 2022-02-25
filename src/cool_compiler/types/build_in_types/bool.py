from ..cool_type_build_in_manager import build_in_type
from ..type import Type
from ..tools import type_body_def

@build_in_type
class Bool(Type):
    def __init__(self):
        super().__init__("Bool")
        type_body_def(self)

    @property
    def is_shield(self):
        return True
    
    def value(self):
        self.define_attribute("value", self)