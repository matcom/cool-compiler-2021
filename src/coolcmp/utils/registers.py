DW = 4


class Register:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"reg_{self.name}"


T = [Register(f"t{i}") for i in range(9)]
V0 = Register("v0")
