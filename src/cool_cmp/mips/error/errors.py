INVALID_REGISTER_ARGUMENTS = "Register {0} is in range {1} and {2}, given {3}"

class MipsError(Exception):
    ERROR_TEMPLATE = ""
    
    def __str__(self) -> str:
        return self.ERROR_TEMPLATE.format(*self.args)

class RegisterInvalidArgError(MipsError):
    ERROR_TEMPLATE = INVALID_REGISTER_ARGUMENTS
    def __init__(self, name, inf, sup, current) -> None:
        self.name = name
        self.inf = inf
        self.sup = sup
        self.current = current
        super().__init__(name, inf, sup, current)
