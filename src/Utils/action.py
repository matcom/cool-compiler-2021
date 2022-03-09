class Action(tuple):
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'

    def __str__(self):
        try:
            action, tag = self
            return f"{'S' if action == Action.SHIFT else 'OK' if action == Action.OK else ''}{tag}"
        except:
            return str(tuple(self))

    __repr__ = __str__