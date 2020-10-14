from cool_tokenizer import tokenize_cool_text
from cool_grammar import define_cool_grammar
from cool_visitor import FormatVisitor

from shift_reduce_parsers import LR1Parser, DerivationTree
from errors import parsing_table_error, Error

from cmp.evaluation import evaluate_reverse_parse

text = """
class Cons inherits List {
    xcar : Int ;
    xcdr : List ;

    isNill ( ) : Bool {
        false
    } ;

    init ( hd : Int , tl : List ) : Cons {
        {
            xcar <- hd ;
            xcdr <- tl ;
            self ;
        }
    } ;
} ;
"""

# text = """
# class Cons inherits List {
#     xcar : Int ;
#     xcdr : List ;

#     isNill ( ) : Bool {
#         false
#     } ;
# } ;
# """

# text = """
# class Cons inherits List {
#     xcar : Int ;
#     xcdr : List ;
# } ;
# """


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
    formatter = FormatVisitor()
    tree = formatter.visit(ast)
    print(tree)
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
#     from cmp.tools.parsing import LR1Parser

#     parser = LR1Parser(grammar)
#     parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True)
#     print("\n".join(repr(x) for x in parse))
#     # print(operations)

#     ast = evaluate_reverse_parse(parse, operations, tokens)

#     formatter = FormatVisitor()
#     tree = formatter.visit(ast)
#     print(tree)


run_pipeline(text)

# run_pipeline_cmp_tools(text)

