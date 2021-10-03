from ..cool_type_build_in_manager import build_in_type
from ..type import Type

@build_in_type
class Int(Type):
    def __init__(self):
        super().__init__("Int")
    
    @property
    def is_shield(self):
        return True