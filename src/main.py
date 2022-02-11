from src.lexical_analizer import tokenize_cool_text
from src.cool_grammar import define_cool_grammar
from src.cool_visitor import FormatVisitorST

from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger

from src.shift_reduce_parsers import LR1Parser, DerivationTree
from src.errors import parsing_table_error, Error

from src.cmp.evaluation import evaluate_reverse_parse

from src.ui import print_array, print_grammar, print_tset


""" # Cool Intrepreter """

def run_pipeline(text):
    main_error1 = ["A class Main with a method main most be provided"]
    main_error2 = ['"main" method in class Main does not receive any parameters']
    # define grammar
    grammar, idx, string, num = define_cool_grammar()

    # try:
    tokens = tokenize_cool_text(grammar, idx, string, num, text)
    parser = LR1Parser(grammar)
    parse, operations = parser([t.token_type for t in tokens])

    # print("\n".join(repr(x) for x in parse))
    # print(operations)

    ast = evaluate_reverse_parse(parse, operations, tokens)
    formatter = FormatVisitorST()
    tree = formatter.visit(ast)

    print("Initial AST")
    print_array(tree)

    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    if errors != [] and errors != main_error1 and errors != main_error2:
        print("---------ERRORS----------")
        print_array(errors)
    else:
        if errors == main_error1 or errors == main_error2:
            errors = []

        tset_builder = TSetBuilder(context, errors)
        tset = tset_builder.visit(ast, None)

        tset_reducer = TSetReducer(context, errors)
        reduced_set = tset_reducer.visit(ast, tset)

        tset_merger = TSetMerger(context, errors)
        tset_merger.visit(ast, reduced_set)

        collector = TypeCollector(errors)
        collector.visit(ast)

        context = collector.context

        builder = TypeBuilder(context, errors)
        builder.visit(ast)

        checker = TypeChecker(context, errors)
        checker.visit(ast, None)

        if errors != [] and errors != main_error1 and errors != main_error2:
            print("----------ERRORS-----------")
            print_array(errors)

        print("Reduced Sets")
        print(reduced_set)

        tree = formatter.visit(ast)
        print("Final Tree:")
        print_array(tree)

    # except Error as error:
    #     st.header("Sorry an error occur while tokenizing text:")
    #     st.write(str(error))



