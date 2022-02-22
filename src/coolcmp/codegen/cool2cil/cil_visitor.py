class CILVisitor:

    def __init__(self):
        self.function_id: int = -1

    @property
    def next_function_id(self) -> int:
        self.function_id += 1
        return self.function_id
