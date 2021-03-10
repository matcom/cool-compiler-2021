from typing import Tuple

class ICoolToken:
    """
    Cool Token Interface
    """

    def set_lex(self, lex:str):
        raise NotImplementedError()

    def get_lex(self)->str:
        raise NotImplementedError()

    def set_type(self, typex:str):
        raise NotImplementedError()

    def get_type(self)->str:
        raise NotImplementedError()

    def set_position(self, line:int, column:int):
        raise NotImplementedError

    def get_position(self)->Tuple[int,int]:
        raise NotImplementedError

    def __str__(self):
        return f"{self.get_lex()}:{self.get_type()} Line:{self.get_position()[0]} Column:{self.get_position()[1]}"

    def __repr__(self):
        return str(self)