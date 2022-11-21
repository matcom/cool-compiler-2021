from ..cool_type_build_in_manager import build_in_type
from ..type import Type

@build_in_type
class Self(Type):
    def __init__(self):
        super().__init__("SELF_TYPE")
    
    @property
    def is_shield(self):
        return True
    
    @property
    def is_self_type(self):
        return True

    def real_type(self, possible):
        return possible