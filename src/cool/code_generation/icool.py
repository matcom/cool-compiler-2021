import cool.semantics.utils.astnodes as cool


class VoidNode(cool.AtomicNode):
    def __init__(self):
        super().__init__("null")
