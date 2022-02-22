from compiler.cmp.grammar import G
from compiler.lexer.lexer import tokenize_text, pprint_tokens
from compiler.cmp.tools import LR1Parser
from compiler.cmp.evaluation import evaluate_reverse_parse
from compiler.visitors.formatter import FormatVisitor
from compiler.visitors.type_collector import TypeCollector
from compiler.visitors.type_builder import TypeBuilder
from compiler.visitors.type_checker import TypeChecker
from compiler.visitors.type_inferencer import TypeInferencer
from compiler.visitors.cil_formatter import PrintCILVisitor
from compiler.visitors.cool2cil import COOLToCILVisitor


def run_pipeline(G, text):
    print('=================== TEXT ======================')
    print(text)
    print('================== TOKENS =====================')
    tokens = list(tokenize_text(text))
    pprint_tokens(tokens)
    print('=================== PARSE =====================')
    parser = LR1Parser(G)
    parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
    print('\n'.join(repr(x) for x in parse))
    print('==================== AST ======================')
    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
    print('============== COLLECTING TYPES ===============')
    errors = []
    collector = TypeCollector(errors)
    collector.visit(ast)
    context = collector.context
    print('Errors:', errors)
    print('Context:')
    print(context)
    print('=============== BUILDING TYPES ================')
    builder = TypeBuilder(context, errors)
    builder.visit(ast)
    manager = builder.manager
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    print('Context:')
    print(context)
    print('=============== CHECKING TYPES ================')
    checker = TypeChecker(context, manager, [])
    scope = checker.visit(ast)
    print('=============== INFERING TYPES ================')
    temp_errors = []
    inferencer = TypeInferencer(context, manager, temp_errors)
    inferencer.visit(ast, scope)
    print('Errors: [')
    for error in temp_errors:
        print('\t', error)
    print(']')
    print('=============== LAST CHECK ================')
    errors.extend(temp_errors)
    checker = TypeChecker(context, manager, errors)
    checker.visit(ast)
    print('Errors: [')
    for error in errors:
        print('\t', error)
    print(']')
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    #print(tree)

    print('=============== CIL CODE ================')
    cil_visitor = COOLToCILVisitor(context) 
    cil_ast = cil_visitor.visit(ast,scope)
    cil_formatter =  PrintCILVisitor()
    print(cil_formatter.visit(cil_ast))
    return ast


text = '''
class Main inherits IO {
    number: Int <- 5;

    main (a:Int,b:Int) : Int {
        (new Main).suma(a+2,b+1)
    };

    suma (a:Int, b:Int) : Int{
        a+b
    };

    
};
'''




ast = run_pipeline(G, text)