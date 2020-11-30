from src.cool_tokenizer import tokenize_cool_text
from src.cool_grammar import define_cool_grammar
from src.cool_visitor import FormatVisitor

from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger

from src.shift_reduce_parsers import LR1Parser, DerivationTree
from src.errors import parsing_table_error, Error

from src.cmp.evaluation import evaluate_reverse_parse
 

def run_pipeline(text):
    # define grammar
    grammar, idx, num = define_cool_grammar()

    # tokenize text
    tokens = tokenize_cool_text(grammar, text, idx, num)

    # try:
    parser = LR1Parser(grammar)
    parse, operations = parser([t.token_type for t in tokens])
    # print("\n".join(repr(x) for x in parse))
    # print(operations)

    ast = evaluate_reverse_parse(parse, operations, tokens)

    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

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

    # formatter = FormatVisitor()
    # tree = formatter.visit(ast)
    # print(tree)
    #         derivation_list = parser(text)
    #         derivation_tree_aut = DerivationTree(derivation_list[0], G)

    # except Error as err:
    #     print(err)


# def run_pipeline_cmp_tools(text):
#     # only for testing
#     # define grammar
#     grammar, idx, num = define_cool_grammar()

#     # tokenizer
#     tokens = tokenize_cool_text(grammar, text, idx, num)

#     # lexical an
#     from src.cmp.tools.parsing import LR1Parser

#     parser = LR1Parser(grammar)
#     parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
#     print("\n".join(repr(x) for x in parse))
#     # print(operations)

#     ast = evaluate_reverse_parse(parse, operations, tokens)

#     formatter = FormatVisitor()
#     tree = formatter.visit(ast)
#     print(tree)


# run_pipeline_cmp_tools(text)