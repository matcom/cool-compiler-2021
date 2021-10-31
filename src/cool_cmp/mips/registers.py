from mips.error.errors import RegisterInvalidArgError

class Reg:
    """
    Provides names for MIPS registers
    
    Example:
    ```python
    v0 = Reg.v(0) # v0 = "$v0"
    v0 = Reg.v(2) # Raises a RegisterInvalidArgError
    ```
    """
    @staticmethod
    def __ranged_register(name, inf, sup, arg):
        if arg < inf or arg > sup:
            raise RegisterInvalidArgError(name,inf,sup,arg)
        return f"${name}{arg}"
    
    @staticmethod
    def __register(name):
        return f"${name}"
    
    @staticmethod
    def raw(arg:int):
        return Reg.__ranged_register("",0,31,arg)
    
    @staticmethod
    def zero():
        return Reg.__register("zero")
    
    @staticmethod
    def v(arg:int):
        return Reg.__ranged_register("v",0,1,arg)

    @staticmethod
    def a(arg:int):
        return Reg.__ranged_register("a",0,3,arg)
    
    @staticmethod
    def t(arg:int):
        return Reg.__ranged_register("t",0,9,arg)
    
    @staticmethod
    def s(arg:int):
        return Reg.__ranged_register("s",0,7,arg)
    
    @staticmethod
    def ra():
        return Reg.__register("ra")
    