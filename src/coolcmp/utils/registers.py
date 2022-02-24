DW = 4


class Register:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"reg_{self.name}"


T = [Register(f"t{i}") for i in range(9)]
ARG = [Register(f"a{i}") for i in range(4)]
ZERO = Register("zero")
LOW = Register("low")
V0 = Register("v0")
V1 = Register("v1")
A0 = Register("a0")
FP = Register("fp")
SP = Register("sp")
RA = Register("ra")
