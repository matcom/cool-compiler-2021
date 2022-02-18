

def semanticAnalizer(ast):
    errors = []

    typeCollector = TypeCollector(errors)
    typeCollector.visit(ast)
    context = typeCollector.context

    typeBuilder = TypeBuilder(context, errors)
    typeBuilder.visit(ast)

    typeInferer = TypeInferer(context, errors)
    scope = typeInferer.visit(ast)

    typeChecker = TypeChecker(context, errors)
    typeChecker.visit(ast, scope)

    return ast, errors, context, scope
    

