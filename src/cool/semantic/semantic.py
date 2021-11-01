from .typeCollector import TypeCollector
from .typeChecker import TypeChecker
from .typeBuilder import TypeBuilder
from .collectVariables import VariableCollector


def main_semantic(ast, debug=False):
    if debug:
        print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('=============== VAR COLLECTOR ================')
    checker = VariableCollector(context, errors)
    scope = checker.visit(ast)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('=============== CHECKING TYPES ================')
    checker = TypeChecker(context, errors)
    checker.visit(ast, scope)
    if debug:
        print('Errors: [')
        for error in errors:
            print('\t', error)
        print(']')
        print('Context:')
        print(context)
        print('Scope:')
        print(scope)
    return ast, errors, context, scope


if __name__ == "__main__":
    pass
