class Register:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"${self.name}"


# Double word
dw = 4

# Temporal
t0 = Register("t0")
t1 = Register("t1")
t2 = Register("t2")

# Argument
a0 = Register("a0")
a1 = Register("a1")
a2 = Register("a2")

# Zero
zero = Register("zero")

# Return
v0 = Register("v0")

# Frame Pointer
fp = Register("fp")

# Stack Pointer
sp = Register("sp")

# RA
ra = Register("ra")
