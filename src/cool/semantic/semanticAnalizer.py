from cool.semantic.type_builder import TypeBuilder
from cool.semantic.type_checker import TypeChecker
from cool.semantic.type_collector import TypeCollector



def run_semantic_pipeline(ast):
    errors = []
    # ============== COLLECTING TYPES ===============
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print_error(errors)

    # =============== BUILDING TYPES ================
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    actual_counter = builder.counter
    print_error(errors)
    
    # =============== CHECKING TYPES ================
    checker = TypeChecker(context, errors,actual_counter)
    scope = checker.visit(ast) 
    print_error(errors)
    return context,scope

def print_error(errors):
    if errors:
        print(errors[0])
        raise Exception()