from .typeCollectorpy import TypeCollector


def main_semantic(ast):
    errors = []

    types = TypeCollector(ast)


if __name__ == "__main__":
    pass
